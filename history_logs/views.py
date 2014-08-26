from django.shortcuts import render, render_to_response, redirect, RequestContext
from django.db import transaction, connection
from django.db.models import Sum, Avg
from django.http import  HttpResponseRedirect, HttpResponse
from django.conf import settings
from django.conf.urls.static import static
from rbmo.models import (UserGroup,
                         Groups,
                         Agency,
                         MPFRO, 
                         MonthlyReqSubmitted,
                         QuarterlyReq,
                         QuarterReqSubmission,
                         COSSubmission
)
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required, permission_required
from helpers.helpers import *
from datetime import datetime, date
from decimal import *
import time
import sys


SYSTEM_NAME = 'e-RBMO Data Management System'

@login_required(login_url='/admin/')
@transaction.atomic
def summary(request):
    context = RequestContext(request)
    cursor = connection.cursor()
    year = datetime.today().year
    month = datetime.today().month
    day = datetime.today().day

    date_query = '''select monthly_req_submitted.*, agency.id, agency.name as agency_name, auth_user.id, auth_user.first_name as first_name, auth_user.last_name
    from monthly_req_submitted inner join agency
    on agency.id = monthly_req_submitted.agency_id
    inner join auth_user on
    auth_user.id = monthly_req_submitted.user_id
    where year(date_submitted)=%s
    and month(date_submitted)=%s
    '''

    qrs_query = '''
   select quarter_req_submitted.*, agency.id, agency.name as agency_name, auth_user.id, auth_user.first_name, auth_user.last_name,
       quarterly_req.name as requirement_name
from quarter_req_submitted inner join agency
	on agency.id = quarter_req_submitted.agency_id
	inner join auth_user on
	auth_user.id = quarter_req_submitted.user_id
	inner join quarterly_req on quarterly_req.id = quarter_req_submitted.requirement_id 
where extract(year from date_submitted)=%s 
    and extract(month from date_submitted)=%s
    '''
    
    monthly_rep_submitted = None
    quarter_rep_submitted = None
    

    if request.method=="POST":
        date_filter_option = request.POST.get('filter_option')
        if date_filter_option == "month":
            month_year = request.POST.get('date').split('-')
            year = month_year[0]
            month = month_year[1]
            cursor.execute(date_query, [year, month])
            monthly_rep_submitted = dictfetchall(cursor)
            cursor.execute(qrs_query, [year, month])
            quarter_rep_submitted = dictfetchall(cursor)
        else:
            date = request.POST.get('date').split('-')
            year = int(date[0])
            month = int(date[1])
            day = int(date[2])
            date_query += " and extract(day from date_submitted)=%s"
            qrs_query += " and extract(day from date_submitted)=%s"
            cursor.execute(date_query, [year, month, day])
            monthly_rep_submitted = dictfetchall(cursor)
            cursor.execute(qrs_query, [year, month, day])
            quarter_rep_submitted = dictfetchall(cursor)
        
    else:
        date_query += " and extract(day from date_submitted)=%s"
        qrs_query += " and extract(day from date_submitted)=%s"
        cursor.execute(date_query, [year, month, day])
        monthly_rep_submitted = dictfetchall(cursor)
        cursor.execute(qrs_query, [year, month, day])
        quarter_rep_submitted = dictfetchall(cursor)

    transaction_summary = []
    print monthly_rep_submitted
    for report in monthly_rep_submitted:
        transaction_summary.append(
            {'date' : report['date_submitted'],
             'agency_name'  : report['agency_name'],
             'doc_submitted': 'Monthly Report',
             'receiver'     : report['first_name'] + ' ' + report['last_name']
            }
        )

    for report in quarter_rep_submitted:
        transaction_summary.append(
            {'date' : report['date_submitted'],
             'agency_name'  : report['agency_name'],
             'doc_submitted': report['requirement_name'],
             'receiver'     : report['first_name'] + ' ' + report['last_name']
            }
        )


    data = {'system_name' : SYSTEM_NAME,
            'allowed_tabs': get_allowed_tabs(request.user.id),
            'transaction_summary' : transaction_summary
           }

    return render_to_response('./transaction/summary.html', data, context)

from django.shortcuts import render
from django.shortcuts import render, render_to_response, redirect, RequestContext
from django.db import transaction, connection
from django.db.models import Sum, Avg
from django.http import  HttpResponseRedirect, HttpResponse
from django.conf import settings
from django.conf.urls.static import static
from rbmo.models import (Agency,
                         MonthlyReqSubmitted,
                         QuarterlyReq,
                         QuarterReqSubmission,
                         COSSubmission,
)

from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required, permission_required
from helpers.helpers import (getMonthLookup, 
                             quarterofMonth,
                             dictfetchall,
                             stringify_month)
from datetime import datetime, date
from decimal import *
import time
import sys


SYSTEM_NAME = 'e-RBMO Data Management System'

month_lookup = getMonthLookup()
quarters = {1: '1st Quarter', 2: '2nd Quarter', 3: '3rd Quarter', 4: 'Last Quarter'}


@login_required(login_url = '/admin/')
@transaction.atomic
def manageAgencyDocs(request):
    context = RequestContext(request)
    try:
        current_year = datetime.today().year
        agency_id = 0
        if 'admin_agency_id' in request.session:
            agency_id = request.session['admin_agency_id']
        else:
            agency_id = request.GET.get('agency_id')

        year = request.GET.get('year', datetime.today().year)
        years = []
        while current_year>=2013:
            years.append(current_year)
            current_year-=1
        #get the agency
        agency = Agency.objects.get(id=agency_id)
        #year
        monthly   = getAgencyMonthlyReq(year, agency)
        quarterly = QuarterlyReq.objects.all()
        q1_req_s  = getSumittedQReq(year, agency, 1) #1st quarter submitted requirements
        q2_req_s  = getSumittedQReq(year, agency, 2) #2nd quarter submitted requirements
        q3_req_s  = getSumittedQReq(year, agency, 3) #3rd quarter submitted requirements
        q4_req_s  = getSumittedQReq(year, agency, 4) #4th quarter submitted requirements
        #get submitted contract of service
        cos_submitted = COSSubmission.objects.filter(date_submitted__year=year, agency=agency)
        #store current agency session
        if 'agency_id' not in request.session:
            request.session['admin_agency_id'] = agency_id

        data = {'system_name'  : SYSTEM_NAME,
                'agency_tab'   : 'reqs',
                'allowed_tabs' : get_allowed_tabs(request.user.id),
                'agency'       : agency,
                'years'        : years,
                'year'         : year,
                'monthly'      : monthly,
                'quarterly'    : quarterly,
                'q1_req_s'     : q1_req_s,
                'q2_req_s'     : q2_req_s,
                'q3_req_s'     : q3_req_s,
                'q4_req_s'     : q4_req_s,
                'cos_submitted': cos_submitted}

        return render_to_response('./admin/agency_docs_recording.html', data, context)
    except: #Agency.DoesNotExist
        return HttpResponseRedirect('/admin/agencies')  


@login_required(login_url='/admin/')
def submitMPFR(request):
    agency_id = request.POST.get('agency_id')
    year = request.POST.get('year')
    agency = Agency.objects.get(id=agency_id)
    months = request.POST.getlist('month[]')

    for month in months:
        monthly_req_submit = MonthlyReqSubmitted(year=year,
                                                 agency = agency,
                                                 date_submitted = datetime.today(),
                                                 month = month,
                                                 user = request.user
        )
        monthly_req_submit.save()
    return HttpResponseRedirect('/admin/manage_agency_docs?agency_id='+str(agency.id))



@login_required(login_url='/admin/')
def delMonthReqs(request):
    try:
        month_req_id = request.GET.get('req_id')
        print month_req_id
        month_req_submitted = MonthlyReqSubmitted.objects.get(id=month_req_id)
        month_req_submitted.delete()
        return HttpResponseRedirect("/admin/manage_agency_docs?agency_id="+str(month_req_submitted.agency.id))
    except:
       return HttpResponse("<h3>Error</h3><p>Invalid Request Found.</p>")


@login_required(login_url='/admin/')
def delQuarterSubmittedReqs(request):
    '''
    this function  delete the quarterly requirement submitted by
    an agency if it is mistakenly checked
    '''
    try:
        q_req_sub_id = request.GET.get("q_req_sub")
        q_req_submitted  = QuarterReqSubmission.objects.get(id = q_req_sub_id)
        q_req_submitted.delete()
        return HttpResponseRedirect("/admin/manage_agency_docs?agency_id="+str(q_req_submitted.agency.id))
    except:
       return HttpResponse("<h3>Error</h3><p>Invalid Request Found.</p>")

@login_required(login_url='/admin/')
def delCOSSubmitted(request):
    try:
        cos_submit_id = request.GET.get("cos_submit_id")
        cos = COSSubmission.objects.get(id=cos_submit_id)
        cos.delete()
        return HttpResponseRedirect("/admin/manage_agency_docs?agency_id="+str(cos.agency.id))
    except:
       return HttpResponse("<h3>Error</h3><p>Invalid Request Found.</p>")

def getSubmittedReqs(agency, year, month):
    #monthly requirements
    submitted_reqs = []
    mrs = isMonthlyRepSubmitted(agency, year, month-1) 
    if mrs:
        submitted_reqs.append({'name':stringify_month(month-1)+' Performance Report of Operation',
                               'date_submitted' : mrs.date_submitted})
    #quarterly requirements
    quarter = quarterofMonth(month)
    if quarter==4:
        year-=1
    qrs = getQuarterReqSubmitted(agency, year, quarter)
    for qr in qrs:
        submitted_reqs.append({'name': qr.requirement.name,
                               'date_submitted' : qr.date_submitted})
    
    return submitted_reqs

def getLackingReqs(agency, year, month):
    lacking_reqs = []
    required_month = 1
    if month==1:
        required_month = 12
        year -=1
    else:
        required_month = month-1
        
    if not isMonthlyRepSubmitted(agency, year, required_month):
        lacking_reqs.append(stringify_month(required_month)+ '-' + str(year) +' Performance Report of Operation')
    #quarter requirements
    quarter = quarterofMonth(month)
    quarter_reqs = getLackingQuarterReqs(agency, year, quarter)
    for req in quarter_reqs:
        lacking_reqs.append(str(year)+'-'+quarters[quarter]+' '+req['name'])
    return lacking_reqs
    

def isMonthlyRepSubmitted(agency, year, month):
    try:
        mrs = MonthlyReqSubmitted.objects.get(agency=agency, year=year, month=month)
        return mrs
    except MonthlyReqSubmitted.DoesNotExist:
        return None


def getQuarterReqSubmitted(agency, year, quarter):
    try:
        qrs = QuarterReqSubmission.objects.filter(agency=agency, year=year, quarter=quarter) 
        return qrs
    except QuarterReqSubmission.DoesNotExist:
        return None

def getLackingQuarterReqs(agency, year, quarter):
    cursor = connection.cursor()
    query = '''
            select * from quarterly_req 
              where id not in (select requirement_id from 
                               quarter_req_submitted 
                                 where agency_id=%s 
                                       and year=%s
                                       and quarter=%s)
            '''
    cursor.execute(query,[agency.id, year, quarter])
    return dictfetchall(cursor)


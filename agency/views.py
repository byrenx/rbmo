from django.shortcuts import render, render_to_response, redirect, RequestContext
from django.db import transaction, connection
from django.http import  HttpResponseRedirect, HttpResponse
from django.conf import settings
from django.conf.urls.static import static
from .forms import (BudgetProposalForm, LoginForm)
from rbmo.models import UserGroup, Groups, Agency, Notification, AllotmentReleases
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required, permission_required
from helpers.helpers import *
from datetime import date


"""
@login_required(login_url='/admin/')
def budgetProposal(request):
    context = RequestContext(request)
    data = {'system_name'   : SYSTEM_NAME,
            'proposal_form' : BudgetProposalForm(),
            
    }

    if request.method == 'POST':
        pass
"""
def login(request):
    context = RequestContext(request)
    data = {'form' : LoginForm()}
    if request.method=="POST":
        loginform = LoginForm(request.POST)
        if loginform.is_valid():
            email = loginform.cleaned_data['email']
            accesskey = loginform.cleaned_data['acces_key']
            try:
                agency = Agency.objects.get(email=email,acces_key=accesskey)
                request.session['agency_id'] = agency.id
                return HttpResponseRedirect('/agency/home')
            except Agency.DoesNotExist:
                data['e_msg'] = "Invalid Email or Password"
                return render_to_response('./agency/login.html', data, context)
        else:
            context = RequestContext(request)
            data['e_msg'] = "Invalid Email or Password"
            return render_to_response('./agency/login.html', data, context)
    else:
        return render_to_response('./agency/login.html', data, context)
    

def home(request):
    if "agency_id" in request.session:
        getToday = request.GET.get('today')
        today = date.today()
        agency_id = request.session["agency_id"]
        agency = Agency.objects.get(id=agency_id)
        if getToday == 'all':
            notification = Notification.objects.filter(agency=agency)
            context = RequestContext(request)
            data = {'system_name' : agency.name, 'email' : agency.email,
                    'notification' : notification,
                    'Tmsg' : "All Available Notification"}
            return render_to_response('./agency/AgencyHome.html', data, context)
        elif getToday == 'today':
            notification = Notification.objects.filter(agency=agency,date_notify=today)
            context = RequestContext(request)
            data = {'system_name' : agency.name, 'email' : agency.email,
                    'notification' : notification, 'today' : today,
                    'Tmsg' : "Today's Notification"}
            return render_to_response('./agency/AgencyHome.html', data, context)
        else:
            notification = Notification.objects.filter(agency=agency,date_notify=today)
            context = RequestContext(request)
            data = {'system_name' : agency.name, 'email' : agency.email,
                    'notification' : notification, 'today' : today}
            return render_to_response('./agency/AgencyHome.html', data, context)
    else:
        return HttpResponseRedirect('/agency/login')
def requirements(request):
    if "agency_id" in request.session:
        agency_id = request.session["agency_id"]
        agency = Agency.objects.get(id=agency_id)
        
        
        context = RequestContext(request)
        data = {'system_name' : agency.name, 'email' : agency.email}
        return render_to_response('./agency/Requirements.html', data, context)
    else:
        return HttpResponse('????')
@transaction.atomic        
def balance(request):

    if "agency_id" in request.session:

        agency_id = request.session["agency_id"]
        agency = Agency.objects.get(id=agency_id)
        context = RequestContext(request)
        getYear = request.GET.get('year')

        if getYear is not None:
            context = RequestContext(request)
            data = {'system_name' : agency.name, 'email' : agency.email}
            cursor = connection.cursor()
            query = '''
                    select allocation, 
                    sum(total) AS total_budget
                    from wfp_data 
                    WHERE agency_id=%s
                    AND year=%s
                    GROUP BY allocation'''
            cursor.execute(query, [agency_id, getYear])
            data['wfp'] = dictfetchall(cursor)
            query = '''        
                    select allocation, 
                    sum(amount_release) AS total_released
                    from allotmentreleases 
                    WHERE agency_id=%s 
                    AND year=%s
                    GROUP BY allocation
                    '''
            cursor.execute(query, [agency_id, getYear])
            data['releases'] = dictfetchall(cursor)
            total = 0
            totalRelease = 0
            PS = 0
            MOOE = 0
            CO = 0
            PSR = 0
            MOOE = 0
            COR = 0
            if data['wfp'] is not None:
                for wfpcompute in data['wfp']:
                    if wfpcompute['allocation'] == 'PS':
                        total += wfpcompute['total_budget']
                        PS = wfpcompute['total_budget']
                    elif wfpcompute['allocation'] == 'MOOE':
                        total += wfpcompute['total_budget']
                        MOOE = wfpcompute['total_budget']
                    elif wfpcompute['allocation'] == 'CO':
                        total += wfpcompute['total_budget']
                        CO = wfpcompute['total_budget']
                data['total'] = total
            else:
                context = RequestContext(request)
                data = {'system_name' : agency.name, 'email' : agency.email,
                        'error' : 'Records not Found!'}
                return render_to_response('./agency/Balances.html', data, context)
            if data['releases'] is not None:
                for compute in data['releases']:
                    if compute['allocation'] == 'PS':
                        totalRelease += compute['total_released']
                        PSR = compute['total_released']
                    elif compute['allocation'] == 'MOOE':
                        totalRelease += compute['total_released']
                        MOOER = compute['total_released']
                    elif compute['allocation'] == 'CO':
                        totalRelease += compute['total_released']
                        COR = compute['total_released']
                data['totalRelease'] = totalRelease
                ps_remaining = 0
                MOOE_remaining = 0
                CO_remaining = 0
                if PS and PSR is not None:
                    ps_remaining = PS - PSR
                    data['ps_remaining'] = ps_remaining
                    data['PS'] = PS
                    data['PSR'] = PSR
                if MOOE and MOOER is not None:
                    MOOE_remaining = MOOE - MOOER    
                    data['MOOE_remaining'] = MOOE_remaining
                    data['MOOE'] = MOOE
                    data['MOOER'] = MOOER
                if CO and COR is not None:
                    CO_remaining = CO - COR
                    data['CO_remaining'] = CO_remaining
                    data['CO'] = CO
                    data['COR'] = COR
                    overall_balance = data['total'] - data['totalRelease']
                    data['overall_balance'] = overall_balance
                    data['success'] = 'Results found! for the year: '+getYear
                return render_to_response('./agency/Balances.html', data, context)
            else:
                context = RequestContext(request)
                data = {'system_name' : agency.name, 'email' : agency.email,
                        'error' : 'Records not Found!'}
                return render_to_response('./agency/Balances.html', data, context)
        else:
            context = RequestContext(request)
            data = {'system_name' : agency.name, 'email' : agency.email,
                    'error' : 'Welcome!'}
            return render_to_response('./agency/Balances.html', data, context)
    else:
        context = RequestContext(request)
        data = {'system_name' : agency.name, 'email' : agency.email}
        return render_to_response('./agency/Balances.html', data, context)
    
@transaction.atomic
def approved(request):
    if "agency_id" in request.session:
        agency_id = request.session["agency_id"]
        agency = Agency.objects.get(id=agency_id)
        
        
        context = RequestContext(request)
        data = {'system_name' : agency.name, 'email' : agency.email}
        return render_to_response('./agency/approved.html', data, context)
    else:
        return HttpResponse('????')

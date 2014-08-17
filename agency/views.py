from django.shortcuts import render, render_to_response, redirect, RequestContext
from django.db import transaction, connection
from django.db.models import Sum, Avg
from django.http import  HttpResponseRedirect, HttpResponse
from django.conf import settings
from django.conf.urls.static import static
from .forms import (BudgetProposalForm, LoginForm)
from requirements.views import (getSubmittedReqs,
                                getLackingReqs)
from rbmo.forms import MonthForm
from rbmo.models import UserGroup, Groups, Agency, Notification, AllotmentReleases, WFPData, AllotmentReleases
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required, permission_required
from helpers.helpers import *
from datetime import date


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
        year = int(request.POST.get('year', datetime.today().year))
        month = int(request.POST.get('month', datetime.today().month))
        
        #submitted requirements
        srs = getSubmittedReqs(agency, year, month)
        #lacking requirements
        lrs = getLackingReqs(agency, year, month)
        data = {'system_name'    : agency.name,
                'email'          : agency.email,
                'month_form'     : MonthForm({'month': month}),
                'submitted_reqs' : srs,
                'lacking_reqs'   : lrs}

        return render_to_response('./agency/Requirements.html', data, context)
    else:
        return HttpResponse('????')


@transaction.atomic        
def balance(request):

    if "agency_id" in request.session:
        agency_id = request.session["agency_id"]
        agency = Agency.objects.get(id=agency_id)
        context = RequestContext(request)
        year = request.POST.get('year', datetime.today().year)
        #ps_total_budget and release
        ps_total = WFPData.objects.filter(agency=agency, year=year, allocation='PS').aggregate(Sum('total'))
        ps_release = AllotmentReleases.objects.filter(agency=agency, year=year,allocation='PS').aggregate(Sum('amount_release'))
        ps_bal = numify(ps_total['total__sum']) - numify(ps_release['amount_release__sum'])
        #mooe total budget and release
        mooe_total = WFPData.objects.filter(agency=agency, year=year, allocation='MOOE').aggregate(Sum('total'))
        mooe_release = AllotmentReleases.objects.filter(agency=agency, year=year, allocation='MOOE').aggregate(Sum('amount_release'))
        mooe_bal = numify(mooe_total['total__sum']) - numify(mooe_release['amount_release__sum'])
        #co total budget and release
        co_total =  WFPData.objects.filter(agency=agency, year=year, allocation='CO').aggregate(Sum('total'))
        co_release = AllotmentReleases.objects.filter(agency=agency, year=year, allocation='CO').aggregate(Sum('amount_release'))
        co_bal = numify(co_total['total__sum']) - numify(co_release['amount_release__sum'])
        balances = [{'allocation': 'PS', 
                     'beginning_bal': numify(ps_total['total__sum']), 
                     'release': numify(ps_release['amount_release__sum']), 
                     'ending_bal':ps_bal},
                    {'allocation': 'MOOE', 
                     'beginning_bal': numify(mooe_total['total__sum']), 
                     'release': numify(mooe_release['amount_release__sum']), 
                     'ending_bal':mooe_bal},
                    {'allocation': 'CO', 
                     'beginning_bal': numify(co_total['total__sum']), 
                     'release': numify(co_release['amount_release__sum']), 
                     'ending_bal':co_bal},
                    {'allocation'   : 'Total',
                     'beginning_bal': numify(ps_total['total__sum']) + numify(mooe_total['total__sum']) + numify(co_total['total__sum']),
                     'release': numify(ps_release['amount_release__sum']) + numify(mooe_release['amount_release__sum']) + numify(co_release['amount_release__sum']),
                     'ending_bal' : ps_bal + mooe_bal + co_bal}
                   ]
        data = {'system_name' : agency.name,
                'email'       : agency.email,
                'balances'    : balances,
                'cur_date'    : time.strftime('%B %d %Y'),
                'year'        : year 
               }
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

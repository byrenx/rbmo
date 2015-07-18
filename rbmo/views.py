#django imports
from django.shortcuts import render, render_to_response, redirect, RequestContext
from django.http import  HttpResponseRedirect, HttpResponse
from django.db import transaction, connection
from django.db.models import Sum, Avg
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, permission_required
from django.core import serializers
from django.conf import settings
from django.conf.urls.static import static

#models
from rbmo.models import (User,
                         UserGroup,
                         Groups,
                         Agency,
                         Sector,
                         MPFRO, 
                         MonthlyReqSubmitted,
                         QuarterlyReq,
                         QuarterReqSubmission,
                         AllotmentReleases,
                         WFPData,
                         COSSubmission,
                         PerformanceReport,
                         PerformanceTarget,
                         CoRequest
)
#project subpackages, forms, views etc
from helpers.helpers import *

from fund.views import isMRS, is_allQRS, lqm, getReleaseAmount, getBudget, getRelease

from .forms import (UserForm, LoginForm, AgencyForm, 
                    MonthForm, ChangePassForm, AllocationMonthYearForm)
from fund.forms import MCASearchForm

#python libraries
from datetime import datetime, date
from decimal import *
import time
import sys
import hashlib
import json

SYSTEM_NAME = 'e-RBMO Data Management System'

months = ['jan', 'feb', 'mar', 'apr', 'may', 'jun',
          'jul', 'aug', 'sept', 'oct', 'nov', 'dec' ]

month_acc_dict = {1: 'jan_acc', 2: 'feb_acc', 3: 'mar_acc', 4: 'apr_acc',
                  5: 'may_acc', 6: 'jun_acc', 7: 'jul_acc', 8: 'aug_acc',
                  9: 'sept_acc', 10: 'oct_acc', 11: 'nov_acc', 12: 'dec_acc'
}

wfp_month_lookup = {1: 'jan', 2: 'feb', 3: 'mar', 4: 'apr',
                  5: 'may', 6: 'jun', 7: 'jul', 8: 'aug',
                  9: 'sept', 10: 'oct', 11: 'nov', 12: 'dec'
}



def home(request):
    context = RequestContext(request)
    data = {'system_name': SYSTEM_NAME}
    return render_to_response('home.html', data, context)

def logout_user(request):
    logout(request)
    data = {'system_name': SYSTEM_NAME}
    return HttpResponseRedirect('home')



@login_required(login_url='/main/')
def submitCOS(request):#submit Contract of Service
    submit = request.POST.get('cos_submit')
    agency_id = request.POST.get('agency_id')
    try:
        if submit is not None and agency_id is not None:
            today = datetime.today()
            agency = Agency.objects.get(id=agency_id)
            cos_submit = COSSubmission(agency=agency, date_submitted=today)
            cos_submit.save()
            return HttpResponseRedirect('/main/manage_agency_docs/'+str(agency.id)+'/'+str(today.year))
        else:
            return HttpResponseRedirect('/agencies')
    except:
        return HttpResponseRedirect('/agencies')

 
def index(request):
    context = RequestContext(request)
    data = {'system_name': SYSTEM_NAME,
            'form': LoginForm()
    }
    if request.method=='POST':
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            user = authenticate(password=login_form.cleaned_data['password'], username=login_form.cleaned_data['email'])
            if user is not None and user.is_active:
                login(request, user)
                return HttpResponseRedirect('/main/home')
            else:
                data['e_msg'] = "Invalid Email or Password"
                return render_to_response('./main/login.html', data, context)
        else:
            data['frm_errors'] = login_form.errors
            return render_to_response('./main/login.html', data, context)
    else:
        return render_to_response('./main/login.html', data, context)


@login_required(login_url='/main')
def main(request):
    context = RequestContext(request)
    cursor = connection.cursor()

    line_agencies = []
    local_agencies = []
    
    year = datetime.today().year
    total_ps = 0
    total_mooe = 0
    total_co = 0
    total_balance = 0
    count = 1

    #line agencies
    agencies = Agency.objects.filter(a_type=2, parent_key = 0).order_by('name')
    for agency in agencies:
        agency_balances = {}
        agency_balances['count'] = count
        agency_balances['agency_id'] = agency.id
        agency_balances['agency_name'] = agency.name
        '''
        total budget
        '''
        ps_budget = getBudget(agency.id, 'PS', year)
        ps_release = getRelease(agency, 'PS', year)
        ps_balance = ps_budget-ps_release

        mooe_budget = getBudget(agency.id, 'MOOE', year)
        mooe_release = getRelease(agency, 'MOOE', year)
        mooe_balance = mooe_budget - mooe_release

        co_budget = getBudget(agency.id, 'CO', year) 
        co_release = getRelease(agency, 'CO', year)
        co_balance = co_budget - co_release

        agency_bal = ps_balance + mooe_balance + co_balance
        
        agency_balances['ps']    = ps_balance
        agency_balances['mooe']  = mooe_balance
        agency_balances['co']    = co_balance
        agency_balances['balance'] = agency_bal
        agency_balances['sub_agencies'] = []
        #sub agencies
        sub_agencies = Agency.objects.filter(parent_key=agency.id).order_by('name')
        sub_count = 0
        for sub_agency in sub_agencies:
            sub_count += 1
            sub_agency_balances = {}
            sub_agency_balances['count'] = str(count)+'.'+str(sub_count)
            sub_agency_balances['agency_id'] = sub_agency.id
            sub_agency_balances['agency_name'] = sub_agency.name
            '''
            total budget
            '''
            sub_ps_budget = getBudget(sub_agency.id, 'PS', year)
            sub_ps_release = getRelease(sub_agency, 'PS', year)
            sub_ps_balance = sub_ps_budget-sub_ps_release
            
            sub_mooe_budget = getBudget(sub_agency.id, 'MOOE', year)
            sub_mooe_release = getRelease(sub_agency, 'MOOE', year)
            sub_mooe_balance = sub_mooe_budget - sub_mooe_release
            
            sub_co_budget = getBudget(sub_agency.id, 'CO', year) 
            sub_co_release = getRelease(sub_agency, 'CO', year)
            sub_co_balance = sub_co_budget - sub_co_release
            
            suba_bal = sub_ps_balance + sub_mooe_balance + sub_co_balance
            sub_agency_balances['ps']    = sub_ps_balance
            sub_agency_balances['mooe']  = sub_mooe_balance
            sub_agency_balances['co']    = sub_co_balance
            sub_agency_balances['balance'] = suba_bal
            
            agency_balances['sub_agencies'].append(sub_agency_balances)
            total_ps   += sub_ps_balance
            total_mooe += sub_mooe_balance
            total_co   += sub_co_balance
            total_balance += suba_bal


        line_agencies.append(agency_balances)
        total_ps   += ps_balance
        total_mooe += mooe_balance
        total_co   += co_balance
        total_balance += agency_bal
        count += 1


    #local agencies
    agencies = Agency.objects.filter(a_type=1, parent_key = 0).order_by('name')
    for agency in agencies:
        agency_balances = {}
        agency_balances['count'] = count
        agency_balances['agency_id'] = agency.id
        agency_balances['agency_name'] = agency.name
        '''
        total budget
        '''
        ps_budget = getBudget(agency.id, 'PS', year)
        ps_release = getRelease(agency, 'PS', year)
        ps_balance = ps_budget-ps_release

        mooe_budget = getBudget(agency.id, 'MOOE', year)
        mooe_release = getRelease(agency, 'MOOE', year)
        mooe_balance = mooe_budget - mooe_release

        co_budget = getBudget(agency.id, 'CO', year) 
        co_release = getRelease(agency, 'CO', year)
        co_balance = co_budget - co_release

        agency_bal = ps_balance + mooe_balance + co_balance
        
        agency_balances['ps']    = ps_balance
        agency_balances['mooe']  = mooe_balance
        agency_balances['co']    = co_balance
        agency_balances['balance'] = agency_bal
        agency_balances['sub_agencies'] = []
        #sub agencies
        sub_agencies = Agency.objects.filter(parent_key=agency.id).order_by('name')
        sub_count = 0
        for sub_agency in sub_agencies:
            sub_count += 1
            sub_agency_balances = {}
            sub_agency_balances['count'] = str(count)+'.'+str(sub_count)
            sub_agency_balances['agency_id'] = sub_agency.id
            sub_agency_balances['agency_name'] = sub_agency.name
            '''
            total budget
            '''
            sub_ps_budget = getBudget(sub_agency.id, 'PS', year)
            sub_ps_release = getRelease(sub_agency, 'PS', year)
            sub_ps_balance = sub_ps_budget-sub_ps_release
            
            sub_mooe_budget = getBudget(sub_agency.id, 'MOOE', year)
            sub_mooe_release = getRelease(sub_agency, 'MOOE', year)
            sub_mooe_balance = sub_mooe_budget - sub_mooe_release
            
            sub_co_budget = getBudget(sub_agency.id, 'CO', year) 
            sub_co_release = getRelease(sub_agency, 'CO', year)
            sub_co_balance = sub_co_budget - sub_co_release
            
            suba_bal = sub_ps_balance + sub_mooe_balance + sub_co_balance
            sub_agency_balances['ps']    = sub_ps_balance
            sub_agency_balances['mooe']  = sub_mooe_balance
            sub_agency_balances['co']    = sub_co_balance
            sub_agency_balances['balance'] = suba_bal
            
            agency_balances['sub_agencies'].append(sub_agency_balances)
            total_ps   += sub_ps_balance
            total_mooe += sub_mooe_balance
            total_co   += sub_co_balance
            total_balance += suba_bal


        local_agencies.append(agency_balances)
        total_ps   += ps_balance
        total_mooe += mooe_balance
        total_co   += co_balance
        total_balance += agency_bal
        count += 1

    data = {'year'          : year,
            'system_name'   : SYSTEM_NAME,
            'allowed_tabs'  : get_allowed_tabs(request.user.id),
            'line_agencies' : line_agencies,
            'local_agencies': local_agencies,
            'total_sum'     :{'total_ps'  : total_ps,
                              'total_mooe' : total_mooe,
                              'total_co' : total_co,
                              'total_balance' : total_balance},
            'today'         : time.strftime('%D %d, %Y')
    }

    return render_to_response('./main/home.html', data, context)


def getagencyBalances(year):
    agency_balances = []
    agencies = Agency.objects.all()
    for agency in agencies:
        #ps
        allocation = Allocation.objecst.get(name='PS')
        query = '''
        select ((tab.jan+tab.feb+tab.mar+tab.apr+tab.may+tab.jun+tab.jul+tab.aug+tab.sept+tab.oct+tab.nov+tab.dec)-sum(total_release)) as balance
        from total_approved_budget tab, total_release_util tru
        where tab.year = 2014 and tru.year=%y
        and tab.agency_id=1 and tru.agency_id=%s
        and tab.allocation_id=1 and tru.allocation_id=%s;
        '''
        cursor.execute(query, [year, agency.id, allocation.id])
        #mooe
        #co


@login_required(login_url='/main/')
def users(request):
    context = RequestContext(request)
    data = { 'page_title': 'Registered Users',
             'system_name': SYSTEM_NAME}
    users = User.objects.all()
    data['users'] = users  
    data['allowed_tabs'] = get_allowed_tabs(request.user.id)
    return render_to_response('./main/users.html', data, context)


@login_required(login_url='/main/')
@transaction.atomic
def addEditUser(request):
    context = RequestContext(request)
    data = {'page_title': 'Add System User',
            'system_name': SYSTEM_NAME,
            'page': 'users',
            'form' : UserForm(),
            'action': request.POST.get('action', 'add')
    }
    if not has_permission(request.user.id, 'record', 'user'):
        return HttpResponseRedirect('/main/')
        
    data['allowed_tabs'] = get_allowed_tabs(request.user.id)

    if request.method=='POST':
        user_form = UserForm(request.POST)
        #add user
        if data['action']=='add' and user_form.is_valid():
            user = User(email = user_form.cleaned_data['email'],
                        username=  user_form.cleaned_data['email'],
                        first_name = user_form.cleaned_data['first_name'],
                        last_name = user_form.cleaned_data['last_name']
            )
            user.set_password(user.first_name)
            user.save()
            u_group = UserGroup(user = user,
                                group = user_form.cleaned_data['group']
            )
            u_group.save()
            data['s_msg'] = "New User Succesfully saved"
            return render_to_response('./main/user_form.html', data, context)
        elif data['action']=='edit' and user_form.is_valid():#edit user
            user = User.objects.get(id=request.POST.get('user_id'))
            user.email = user_form.cleaned_data['email']
            user.first_name = user_form.cleaned_data['first_name']
            user.last_name = user_form.cleaned_data['last_name']

            u_group = UserGroup.objects.get(user = user)
            u_group.group = user_form.cleaned_data['group']
            u_group.save()

            user.save()
            data['s_msg'] = "User Succesfully updated"
            return render_to_response('./main/user_form.html', data, context)
        else:#invalid form inputs
            data['frm_errors'] = user_form.errors
            data['form'] = user_form
            return render_to_response('./main/user_form.html', data, context)
    else:
        data['action'] = request.GET.get('action', 'add')
        if data['action']=='edit':
            user_id = request.GET.get('u_id')
            try:
                data['page_title'] = 'Edit System User'
                user = User.objects.get(id=user_id)
                u_group = UserGroup.objects.get(user=user)
                data['form'] = UserForm({'email'      : user.username,
                                         'first_name' : user.first_name,
                                         'last_name'  : user.last_name,
                                         'group'      : u_group.group
                                     })
                data['user_id'] = user.id 
                return render_to_response('./main/user_form.html', data, context)
            except:
                return render_to_response('./main/user_form.html', data, context)
        else:
            return render_to_response('./main/user_form.html', data, context)


def changeUserStatus(request):
    try:
        user_id = int(request.GET.get("user_id"))
        status = int(request.GET.get("status"))
        user = User.objects.get(id=user_id)
        user.is_active = status
        user.save()
        return HttpResponse(status)
    except:
        return HttpResponse(0)

@login_required(login_url='/main/')
@transaction.atomic
def agencies(request):
    context = RequestContext(request)

    if 'main_agency_id' in request.session:
        del request.session['main_agency_id']

    data = {'page'         : 'agencies',
            'system_name'  : SYSTEM_NAME,
            'allowed_tabs' : get_allowed_tabs(request.user.id),
            'sectors'      : Sector.objects.all()
     }

    
    if has_permission(request.user.id, 'record', 'agency'):
        data['has_add'] = 'true'

    if request.method=='POST':
        agency_search = request.POST.get('agency')
        data['agencies'] = Agency.objects.filter(name__contains=agency_search)
    else:
        data['agencies'] = Agency.objects.order_by('name')
    return render_to_response('./main/agencies.html', data, context)


@login_required(login_url='/main/')
def getAgenciesbySector(request):
    context = RequestContext(request)
    try:
        sectors_selected = request.POST.getlist('sector[]')
        agencies = Agency.objects.filter(sector__in = sectors_selected).order_by('name')

        data = {'page'             : 'agencies',
                'agencies'         : agencies,
                'system_name'      : SYSTEM_NAME,
                'sectors'          : Sector.objects.all(),
                'sectors_selected' : [int(x) for x in sectors_selected],
                'allowed_tabs'     : get_allowed_tabs(request.user.id)
        }

        if has_permission(request.user.id, 'record', 'agency'):
            data['has_add'] = 'true'

        return render_to_response('./main/agencies.html', data, context)
    except Agency.DoesNotExist:
        return HttpResponse('Error 404 Page not Found')




@login_required(login_url='/main/')
def addEditAgency(request):
    context = RequestContext(request)
    data = {'form': AgencyForm(),
            'mode': request.GET.get('action', 'add'),
            'system_name': SYSTEM_NAME
    }
    if not has_permission(request.user.id, 'record', 'agency'):
        return HttpResponseRedirect('/main/agencies')

    data['allowed_tabs'] = get_allowed_tabs(request.user.id)

    if request.method == 'POST':
        action = request.POST.get('action', 'add')
        agency_frm = AgencyForm(request.POST)
        if action=='add' and agency_frm.is_valid():
            addAgency(request, agency_frm)
            data['s_msg'] = 'New Agency/Office was succesfully added.'
            return render_to_response('./main/agency_form.html', data, context)
        elif action=='edit' and agency_frm.is_valid():
            agency_id = request.POST.get('id')
            agency = Agency.objects.get(id=agency_id)
            agency.name = agency_frm.cleaned_data['name']
            agency.email = agency_frm.cleaned_data['email']
            agency.sector = agency_frm.cleaned_data['sector']
            agency.a_type = agency_frm.cleaned_data['a_type']
            agency.parent_key = request.POST.get('head_agency')
            agency.save()
            data['s_msg'] = 'Agency/Office was succesfully Updated.'
            return render_to_response('./main/agency_form.html', data, context)
        else:
            data['frm_errors'] = agency_frm.errors
            data['form'] = agency_frm
            return render_to_response('./main/agency_form.html', data, context)
    else:
        data['action'] = request.GET.get('action', 'add')
        print request.GET
        if data['action']=='edit':
            try:
                agency_id = request.GET.get('a_id')
                agency = Agency.objects.get(id=agency_id)
                data['form'] = AgencyForm({'name'  : agency.name,
                                           'email' : agency.email,
                                           'sector': agency.sector,
                                           'a_type': agency.a_type
                                       })
                
                data['agency_id'] = agency.id
                data['parent_key'] = agency.parent_key
                data['agencies_selection'] = Agency.objects.exclude(id=agency.id).order_by('name')
                return render_to_response('./main/agency_form.html', data, context)
            except Agency.DoesNotExist:
                return render_to_response('./main/agency_form.html', data, context)
        else:
            data['agencies_selection'] = Agency.objects.all().order_by('name')
            return render_to_response('./main/agency_form.html', data, context)


@login_required(login_url='/main/')
def deleteAgency(request, agency_id):
    #try:
        context = RequestContext(request)
        agency  = Agency.objects.get(id=agency_id)
        a_name  = agency.name
        data = {'system_name'   : SYSTEM_NAME,
                'allowed_tabs'  : get_allowed_tabs(request.user.id),

                'links'         : [{'url'   : '/main/agencies',
                                    'label' : 'Back to List of Agencies'}]}
        if hasCurrRecord(agency):
            data['rm_err'] = "Agency named '"+a_name+"' cannot be removed due to the ff. records this agency may have: "
        else:
            agency.delete()
            data['s_msg'] = "Agency named '"+a_name+"' succesfully removed from the list of agencies"

        return render_to_response('response.html', data, context)
#    except:
  #      return HttpResponseRedirect('/main/agencies')

def hasCurrRecord(agency):
    year = datetime.today().year
    #if has requirment record
    mrec = MonthlyReqSubmitted.objects.filter(agency=agency)
    qrec = QuarterReqSubmission.objects.filter(agency=agency)
    crec = COSSubmission.objects.filter(agency=agency)
    #if has wfprecord
    wfprec = WFPData.objects.filter(agency=agency)
    #if has request
    request = CoRequest.objects.filter(agency=agency)
    #if has allotment releases received
    releases = AllotmentReleases.objects.filter(agency=agency)
    if len(mrec)>0 or len(qrec)>0 or len(crec)>0 or len(wfprec)>0 or len(request)>0 or len(releases)>0:
        return True
    else:
        return False
    
    
    



def hasWFP(year, agency):
    return WFPData.objects.filter(year=year, agency=agency)
    


@login_required(login_url = '/main/')
@transaction.atomic
def manageAgencyDocs(request, agency_id, year = datetime.today().year):
    context = RequestContext(request)
    if "year" in request.GET:
        year = request.GET.get("year")
        #    try:
    current_year = datetime.today().year
    years = []
    while current_year>=2013:
        years.append(current_year)
        current_year-=1
    #get the agency
    agency = Agency.objects.get(id=agency_id)
    #year
    monthly   = getAgencyMonthlyReq(year, agency)
    quarter_of_month = exactQuarterofMonth(datetime.today().month)
    q_reqs  = getSumittedQReq(year, agency, quarter_of_month) #1st quarter submitted requirements
    #get submitted contract of service
    cos_submitted = COSSubmission.objects.filter(date_submitted__year=year, agency=agency)

    data = {'system_name'  : SYSTEM_NAME,
            'current_tab'  : "Requirements",
            'allowed_tabs' : get_allowed_tabs(request.user.id),
            'agency_tabs'  : getAgencyTabs(request.user.id, agency.id),
            'agency'       : agency,
            'years'        : years,
            'year'         : year,
            'monthly'      : monthly,
            'q_reqs'       : q_reqs,
            'cos_submitted': cos_submitted,
            'quarter_req_submitted' : getSubmittedQuarterReq(year, agency, quarter_of_month)}
    
    return render_to_response('./main/agency_docs_recording.html', data, context)
    #except: #Agency.DoesNotExist
    #    return HttpResponseRedirect('/main/agencies')  


def getSumittedQReq(year, agency, quarter):
    quarter_req_submitted = QuarterReqSubmission.objects.filter(year=year, agency=agency, quarter=quarter)

    quarter_submitted = []
    for qrs in quarter_req_submitted:
        quarter_submitted.append(qrs.requirement.id)
    return quarter_submitted


def getSubmittedQuarterReq(year, agency, quarter):
    query = "SELECT quarter_req_submitted.*, quarterly_req.id as q_id, quarterly_req.name  FROM quarter_req_submitted RIGHT OUTER JOIN quarterly_req ON quarter_req_submitted.year = %s AND quarter_req_submitted.quarter = %s AND agency_id = %s AND quarterly_req.id = quarter_req_submitted.requirement_id"

    quarter_req_submitted = QuarterReqSubmission.objects.raw(query, [year, quarter, agency.id])
    return quarter_req_submitted


def getDisplaySubmittedQReq(request):
    context = RequestContext(request)
    try:
        year = request.GET.get("year")
        agency_id = request.GET.get("agency_id")
        quarter = request.GET.get("quarter")
        agency = Agency.objects.get(id=agency_id)
        submitted_req = getSubmittedQuarterReq(year, agency, quarter)
        q_reqs = getSumittedQReq(year, agency, quarter)
        data = {'quarter_req_submitted' : submitted_req,
                'q_reqs'                : q_reqs}
        return render_to_response("./main/submitted_qreqtable.html", data, context)
    except:
        return HttpResponse("</h3>Error</h3><p>Invalid Request Found</p>")


@login_required(login_url='/main/')
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
    return HttpResponseRedirect('/main/manage_agency_docs/'+str(agency.id)+'/')


def getAgencyMonthlyReq(year, agency):
    try:
        submitted = MonthlyReqSubmitted.objects.filter(year=year, agency=agency).order_by('month')
        req_submitted = {}
        for i in range(1, 13):
            found = 0
            for submit in submitted:
                if i==submit.month:
                    req_submitted[i] = {'id'     : submit.id,
                                        'status' : 'ok',
                                        'date_submitted' : submit.date_submitted,
                                        'receiver' : submit.user.first_name + ' ' + submit.user.last_name}                        
                    found=1
                    break
            if found==0:
                req_submitted[i] = {'status': 'none'}
            
        return req_submitted
    except MonthlyReqSubmitted.DoesNotExist:
        return None

@transaction.atomic
def saveSubmitReqs(request):
    context = RequestContext(request)
    
    if request.method == 'POST':
        print 'recording'
        agency = Agency.objects.get(id=request.POST.get('agency_id'))
        today = datetime.now()
        for doc in request.POST.getlist('docs[]'):
            document = Documents.objects.get(id=doc)
            doc_submit = DocsSubmitted(agency=agency, doc=document, date_submitted=today.strftime('%Y-%m-%d %I:%M'))
            doc_submit.save()
        return HttpResponseRedirect('/main/manage_agency_docs?agency_id='+str(agency.id))


@login_required(login_url='/main/')
def delSubmitReqs(request):
    docs_sub_id = request.GET.get('doc_sub')
    doc_sub = DocsSubmitted.objects.get(id=docs_sub_id)
    agency_id = doc_sub.agency.id
    doc_sub.delete()
    return HttpResponseRedirect('/main/manage_agency_docs?agency_id='+str(agency_id))

@transaction.atomic
def addAgency(request, agency_frm):
    h = hashlib.sha256()
    h.update(agency_frm.cleaned_data['email'])
    password = h.hexdigest()
    agency = Agency(name = agency_frm.cleaned_data['name'],
                    email = agency_frm.cleaned_data['email'],
                    sector = agency_frm.cleaned_data['sector'],
                    acces_key = password,
                    a_type = agency_frm.cleaned_data['a_type'],
                    parent_key = request.POST.get('head_agency')
                )
    agency.save()


def reqsStats(year):
    cursor = connection.cursor()
    stats_list = []
    req_stats_query = '''
    select agency.name, 
    (select count(*) from documents)-(select count(*) from docs_submitted where agency_id=agency.id and extract(year from date_submitted)=%s)
    from agency
    '''
    cursor.execute(req_stats_query, [year])
    for agency in cursor.fetchall():
        stats_list.append({'agency_name': agency[0], 'stat': agency[1]})
    return stats_list



@login_required(login_url='/main/')
@transaction.atomic
def mpfroReports(request, agency_id):
    context = RequestContext(request)
    cursor = connection.cursor()
    try:
        month = datetime.today().month
        year = datetime.today().year
        if request.method=='POST':
            year = request.POST.get('year')
            month = request.POST.get('month')

        agency = Agency.objects.get(id=agency_id)        
        perf_accs_query = "select '"+months[int(month)-1]+"' as budget, "
        perf_accs_query+= "wfp_data.activity, "
        perf_accs_query+= "performance_report.* "
        perf_accs_query+= "from performance_report inner join wfp_data on "
        perf_accs_query+= "wfp_data.id = performance_report.activity_id "
        perf_accs_query+= "and wfp_data.agency_id = %s "
        perf_accs_query+= "and performance_report.year=%s "
        perf_accs_query+= "and performance_report.month=%s"

        cursor.execute(perf_accs_query, [agency.id, year, month])
        perf_accs = dictfetchall(cursor)
        monthly_acts_reports = []
        for acc in perf_accs:
            query = "select indicator, "+months[int(month)-1]+" as target, "+month_acc_dict[int(month)]+" as acc from performancetarget where wfp_activity_id=%s"
            cursor.execute(query, [acc['activity_id']])
            indicators_accs = []
            for indicator in dictfetchall(cursor):
                indicators_accs.append({'indicator': indicator['indicator'],
                                       'target'   : indicator['target'],
                                       'acc'      : indicator['acc'],
                                       'variance' : indicator['acc']-indicator['target']
                                   }
                                  )
            monthly_acts_reports.append({'id'       : acc['id'],
                                         'activity' : acc['activity'],
                                         'received' : acc['received'],
                                         'incurred' : acc['incurred'],
                                         'remaining': numify(acc['received'])-numify(acc['incurred']),
                                         'remarks'  : acc['remarks'],
                                         'indicator_count' : (len(indicators_accs) + 1),
                                         'indicators_accs' : indicators_accs
                                     })
    
        yrs_query = "select distinct(year) from performance_report"
        cursor.execute(yrs_query)
        data = {'system_name'   : SYSTEM_NAME,
                'agency'        : agency,
                'agency_tabs'   : getAgencyTabs(request.user.id, agency.id),
                'current_tab'   : "Monthly Report of Operation",
                'years'         : dictfetchall(cursor),
                'monthly_acts_reports':monthly_acts_reports,
                'str_month'     : stringify_month(int(month)),
                'month_form'    : MonthForm({'month': month}),
                'year'          : year
            }
        
        return render_to_response('./main/monthly_reps.html', data, context)
    except Agency.DoesNotExist:
        return HttpResponseRedirect('/main/agencies')


@login_required(login_url="/main/")
def mpfro_form(request, agency_id):
    cursor = connection.cursor()
    context = RequestContext(request)
    try:
        agency = Agency.objects.get(id=agency_id)
        data = {'system_name' : SYSTEM_NAME,
                'agency_id'   : agency_id,
                'allowed_tabs': get_allowed_tabs(request.user.id),
                'agency_tabs' : getAgencyTabs(request.user.id, agency.id),
                'current_tab' : "Monthly Report of Operation"
        } 
    
        this_year = datetime.today().year
        data['years'] = [this_year, (this_year-1)]
        action = request.GET.get('action', 'add')
        agency = Agency.objects.get(id=data['agency_id'])
        data['action'] = action
        data['agency'] = agency
        data['month_form'] = MonthForm({'month': datetime.today().month})
        
        if action == 'add':
            year = datetime.today().year
            acts_query = "select id, activity from wfp_data where agency_id=%s and year=%s and wfp_data.id not in (select activity_id from performance_report where performance_report.year=%s and performance_report.month=%s)"
            cursor.execute(acts_query, [agency.id, year, year, datetime.today().month])
            activities = dictfetchall(cursor)
            data['year'] = year
            data['activities'] = activities
            return render_to_response('./main/mpfro_form.html', data, context)
        else: #edit
            mpfro_id = request.GET.get('mpfro_id')
            activity_info = PerformanceReport.objects.get(id = mpfro_id)
            accs_query = "select id, indicator, "+wfp_month_lookup[activity_info.month]+" as target," + month_acc_dict[activity_info.month] + " as accomplished from performancetarget where wfp_activity_id = %s"
            cursor.execute(accs_query, [activity_info.activity.id])
            performance_accs = dictfetchall(cursor)
            data['activity_info'] = activity_info
            data['performance_accs'] = performance_accs
            data['str_month'] = stringify_month(activity_info.month)
            return render_to_response('./main/mpfro_form.html', data, context)
    except Agency.DoesNotExist and PerformanceReport.DoesNotExist:
        return HttpResponse('Page Not Found Error!')


@login_required(login_url='/main/')
@transaction.atomic
def submitQuarterReq(request):
    agency = Agency.objects.get(id=request.GET.get('agency_id'))
    year = request.GET.get("year")
    action = request.GET.get("action")
    date_submit = request.GET.get("date_submit")



    if action == "add":
        req_id = request.GET.get("req_id")
        quarter = request.GET.get("quarter")
        quarter_submit = QuarterReqSubmission(year = year,
                                              agency = agency,
                                              requirement = QuarterlyReq.objects.get(id=req_id),
                                              quarter = quarter,
                                              date_submitted = date_submit,
                                              user = request.user
                                        )
        quarter_submit.save()

    if action == "edit":
        qrs_id = request.GET.get("qrs_id")
        quarter_submit = QuarterReqSubmission.objects.get(id=qrs_id)
        quarter_submit.date_submitted = date_submit
        quarter_submit.save()
        
    '''
    qReqs_subs = QuarterReqSubmission.objects.select_related('quarterlyreq').filter(year = year, agency=agency)
    json_response = serializers.serialize("json", qReqs_subs)
    
    return HttpResponse(json_response, content_type="application/json")
    '''
    return HttpResponse("success")

@transaction.atomic
def allot_releases(request):
    #generates reports all releases for all agencies
    context = RequestContext(request)
    data = {'system_name': SYSTEM_NAME,
            'allowed_tabs' : get_allowed_tabs(request.user.id)
        }
    data['allowed_tabs'] = get_allowed_tabs(request.user.id)
    line_agencies = []
    total_ps = 0
    total_mooe = 0
    total_co = 0

    #line agencies
    agencies = Agency.objects.filter(a_type=2, parent_key = 0).order_by('name')
    count = 1
    for agency in agencies:
        agency_release = {}
        #get total ps_release
        ps = AllotmentReleases.objects.filter(agency=agency, allocation='PS').aggregate(Sum('amount_release'))
        #get total mooe release
        mooe = AllotmentReleases.objects.filter(agency=agency, allocation='MOOE').aggregate(Sum('amount_release'))
        #get total co release
        co = AllotmentReleases.objects.filter(agency=agency, allocation='co').aggregate(Sum('amount_release'))
        total = numify( ps['amount_release__sum']) + numify( mooe['amount_release__sum']) + numify( co['amount_release__sum'])
        agency_release['count'] = count
        agency_release['name']  = agency.name
        agency_release['ps']    = numify(ps['amount_release__sum'])
        agency_release['mooe']  = numify(mooe['amount_release__sum'])
        agency_release['co']    = numify(co['amount_release__sum'])
        agency_release['total'] = total
        
        #sub agencies
        sub_agencies = Agency.objects.filter(parent_key=agency.id).order_by('name')
        agency_release['sub_agencies'] = []
        sub_count = 0
        for sub_agency in sub_agencies:
            sub_count += 1
            sub_agency_release = {}
            #get total ps_release
            sub_ps = AllotmentReleases.objects.filter(agency=sub_agency, allocation='PS').aggregate(Sum('amount_release'))
            #get total mooe release
            sub_mooe = AllotmentReleases.objects.filter(agency=sub_agency, allocation='MOOE').aggregate(Sum('amount_release'))
            #get total co release
            sub_co = AllotmentReleases.objects.filter(agency=sub_agency, allocation='co').aggregate(Sum('amount_release'))
            sub_total = numify(sub_ps['amount_release__sum']) + numify(sub_mooe['amount_release__sum']) + numify(sub_co['amount_release__sum'])
            sub_agency_release['count'] = str(count)+'.'+str(sub_count)
            sub_agency_release['name']  = sub_agency.name
            sub_agency_release['ps']    = numify(sub_ps['amount_release__sum'])
            sub_agency_release['mooe']  = numify(sub_mooe['amount_release__sum'])
            sub_agency_release['co']    = numify(sub_co['amount_release__sum'])
            sub_agency_release['total'] = sub_total
            
            agency_release['sub_agencies'].append(sub_agency_release)
            total_ps += numify(sub_ps['amount_release__sum'])
            total_mooe += numify(sub_mooe['amount_release__sum'])
            total_co += numify(sub_co['amount_release__sum'])        
        #end of inner for
        line_agencies.append(agency_release)
        total_ps += numify(ps['amount_release__sum'])
        total_mooe += numify( mooe['amount_release__sum'])
        total_co += numify(co['amount_release__sum'])        
        count = count + 1
    
    #local agencies
    local_agencies = []
    agencies = Agency.objects.filter(a_type=1, parent_key = 0).order_by('name')
    count = 1
    for agency in agencies:
        agency_release = {}
        #get total ps_release
        ps = AllotmentReleases.objects.filter(agency=agency, allocation='PS').aggregate(Sum('amount_release'))
        #get total mooe release
        mooe = AllotmentReleases.objects.filter(agency=agency, allocation='MOOE').aggregate(Sum('amount_release'))
        #get total co release
        co = AllotmentReleases.objects.filter(agency=agency, allocation='co').aggregate(Sum('amount_release'))
        total = numify( ps['amount_release__sum']) + numify( mooe['amount_release__sum']) + numify( co['amount_release__sum'])
        agency_release['count'] = count
        agency_release['name']  = agency.name
        agency_release['ps']    = numify(ps['amount_release__sum'])
        agency_release['mooe']  = numify(mooe['amount_release__sum'])
        agency_release['co']    = numify(co['amount_release__sum'])
        agency_release['total'] = total
        
        #sub agencies
        sub_agencies = Agency.objects.filter(parent_key=agency.id).order_by('name')
        agency_release['sub_agencies'] = []
        sub_count = 0
        for sub_agency in sub_agencies:
            sub_count += 1
            sub_agency_release = {}
            #get total ps_release
            sub_ps = AllotmentReleases.objects.filter(agency=sub_agency, allocation='PS').aggregate(Sum('amount_release'))
            #get total mooe release
            sub_mooe = AllotmentReleases.objects.filter(agency=sub_agency, allocation='MOOE').aggregate(Sum('amount_release'))
            #get total co release
            sub_co = AllotmentReleases.objects.filter(agency=sub_agency, allocation='co').aggregate(Sum('amount_release'))
            sub_total = numify(sub_ps['amount_release__sum']) + numify(sub_mooe['amount_release__sum']) + numify(sub_co['amount_release__sum'])
            sub_agency_release['count'] = str(count)+'.'+str(sub_count)
            sub_agency_release['name']  = sub_agency.name
            sub_agency_release['ps']    = numify(sub_ps['amount_release__sum'])
            sub_agency_release['mooe']  = numify(sub_mooe['amount_release__sum'])
            sub_agency_release['co']    = numify(sub_co['amount_release__sum'])
            sub_agency_release['total'] = sub_total
            
            agency_release['sub_agencies'].append(sub_agency_release)
            total_ps += numify(sub_ps['amount_release__sum'])
            total_mooe += numify(sub_mooe['amount_release__sum'])
            total_co += numify(sub_co['amount_release__sum'])        
        #end of inner for
        local_agencies.append(agency_release)
        total_ps += numify(ps['amount_release__sum'])
        total_mooe += numify( mooe['amount_release__sum'])
        total_co += numify(co['amount_release__sum'])        
        count = count + 1
    
    
    data['line_agencies'] = line_agencies
    data['local_agencies'] = local_agencies
    data['grand_total'] = {'ps': total_ps, 'mooe': total_mooe, 'co': total_co, 'total': total_ps+total_mooe+total_co}
    data['today'] = date.today()
    return render_to_response('./main/allotment_releases_report.html', data, context)


def yearly_fund(request):
    cursor = connection.cursor()
    context = RequestContext(request)
    data = {
            'system_name'  : SYSTEM_NAME,
            'allowed_tabs' : get_allowed_tabs(request.user.id),
            'cur_year'     : datetime.today().year
           }
    year = date.today().year 
    year_list = []
    
    yrs_query = "select distinct(year) as year from wfp_data"
    cursor.execute(yrs_query)
    for yr in dictfetchall(cursor):
        year_list.append(yr['year'])

    data['year_choices'] = year_list
    if request.method=="POS":
        pass
    fund_query = '''select (select sum(total) from wfp_data
                            where year=%s and allocation='PS') 
                            as ps_amount,
                            ((select sum(total) from wfp_data
                              where year=%s and allocation='PS')/
                              sum(total)*100) as ps_percentile,
                            (select sum(total) from wfp_data
                              where year=%s and allocation='MOOE') 
                              as mooe_amount,
                            ((select sum(total) from wfp_data
                              where year=%s and allocation='MOOE')/
                              sum(total)*100) as mooe_percentile,
                            (select sum(total) from wfp_data
                              where year=%s and allocation='CO') 
                              as co_amount,
                            ((select sum(total) from wfp_data
                              where year=%s and allocation='CO')/
                              sum(total)*100) as co_percentile,
                            sum(total) as total_fund
                     from wfp_data where year=%s
                 '''
    cursor.execute(fund_query, [year, year, year,year, year, year, year])
    fund_rs = cursor.fetchone()
    fund = {'ps_amount'     : fund_rs[0],
            'ps_percentile' : fund_rs[1],
            'mooe_amount'     : fund_rs[2],
            'mooe_percentile' : fund_rs[3],
            'co_amount'     : fund_rs[4],
            'co_percentile' : fund_rs[5],
            'total_fund'    : fund_rs[6]
           }
    data['fund'] = fund
    return render_to_response('./main/yearly_fund.html', data, context)  



def fundDistribData(year):
    cursor  = connection.cursor()
    data  = {'system_name'  : SYSTEM_NAME,
             'today'        : datetime.today(),
    }


    wfp = WFPData.objects.filter(year=year).aggregate(Sum('total')) 
    total = numify(wfp['total__sum'])
    query = '''select sector.id, sector.name, sum(wfp_data.total) as total
    from sector, agency, wfp_data 
    where sector.id = agency.sector_id and agency.id = wfp_data.agency_id
    and wfp_data.year=%s group by sector.id;
    '''

    cursor.execute(query, year)
    sectors = dictfetchall(cursor)
    sector_budget_percent = []

    for sector in sectors:
        sector_budget_percent.append({'id'      : sector['id'],
                                      'name'    : sector['name'], 
                                      'percent' : int(round((sector['total']/total)*100))})

    years_query = "select distinct(year) from wfp_data"
    cursor.execute(years_query)
    years = dictfetchall(cursor)
    data['years']   = years
    data['sectors'] = sector_budget_percent
    data['year']    = year

    return data
    
    

def fundDistribution(request):
    year  = datetime.today().year 
    context = RequestContext(request)
    if request.method=='POST':
        year = request.POST.get('year', datetime.today().year)

    data = fundDistribData(year)
    data['allowed_tabs'] = get_allowed_tabs(request.user.id)

    return render_to_response('./main/fund_distrib.html', data, context)


def fundDistribPrint(request):
    context = RequestContext(request)
    year  = request.GET.get('year') 
    data = fundDistribData(year)
    
    return render_to_response('./main/fund_distrib_print.html', data, context)
    



@login_required(login_url='/main/')    
@transaction.atomic
def totalMonthlyReleases(request):
    cursor = connection.cursor()
    context = RequestContext(request)
    year = time.strftime('%Y')
    allocation = 'PS'
    cursor.execute("select distinct(year) from allotmentreleases")
    data = {'system_name'  : SYSTEM_NAME,
            'year'         : year,
            'allocation'   : allocation,
            'years'        : dictfetchall(cursor),
            'allowed_tabs' : get_allowed_tabs(request.user.id),
            'today'        : datetime.today(),
            'current_month': datetime.today().month
    }

    if request.method=='POST':
        year  = request.POST.get('year')
        allocation = request.POST.get('allocation')


    agency_monthly_releases = []
    total_monthly_release = {'jan'  : 0, 'feb': 0, 'mar': 0, 'apr': 0,
                             'may'  : 0, 'jun': 0, 'jul': 0, 'aug':0,
                             'sept' : 0, 'oct': 0, 'nov': 0 ,'dec':0}
    count = 1
    grand_total = 0
    agencies = Agency.objects.filter(parent_key=0).order_by('name')
    for agency in agencies:
        agency_release = {}
        agency_release['no'] = count
        agency_release['name'] = agency.name
        agency_release['sub_agencies'] = []
        temp_per_agency_total = 0
        for i in range(1, data['current_month']+1):
            total = AllotmentReleases.objects.filter(agency=agency, month=i, year=year, allocation=allocation).aggregate(Sum('amount_release'))
            agency_release[months[i-1]] = numify(total['amount_release__sum'])
            total_monthly_release[months[i-1]] += numify(total['amount_release__sum'])
            temp_per_agency_total += numify(total['amount_release__sum'])

        #sub_agencies
        sub_agencies = Agency.objects.filter(parent_key=agency.id).order_by('name')
        sub_count = 0
        for sub_agency in sub_agencies:
            sub_count += 1
            sub_agency_release = {}
            sub_agency_release['no'] = str(count)+'.'+str(sub_count)
            sub_agency_release['name'] = sub_agency.name
            sub_agency_total = 0
            for i in range(1, data['current_month']+1):
                sub_total = AllotmentReleases.objects.filter(agency=sub_agency, month=i, year=year, allocation=allocation).aggregate(Sum('amount_release'))
                sub_agency_release[months[i-1]] = numify(sub_total['amount_release__sum'])
                total_monthly_release[months[i-1]] += numify(sub_total['amount_release__sum'])
                sub_agency_total += numify(sub_total['amount_release__sum'])
            #end
            sub_agency_release['total'] = sub_agency_total
            agency_release['sub_agencies'].append(sub_agency_release)
            grand_total += sub_agency_total
            
        agency_release['total'] = temp_per_agency_total
        agency_monthly_releases.append(agency_release)
        grand_total += temp_per_agency_total
        count+=1

    data['agency_monthly_releases'] = agency_monthly_releases
    data['total_monthly_releases']= total_monthly_release
    data['grand_total'] = grand_total
    data['allocation'] = allocation
            
    return render_to_response('./main/total_monthly_release.html', data, context)
    
def agenciesCompReqList(request): 
    context = RequestContext(request)
    allocation = 'MOOE'
    year = datetime.today().year
    month = datetime.today().month
    agency_list = []
    if request.method=='POST':
        allocation = request.POST.get('allocation')
        month = int(request.POST.get('month'))
        year = request.POST.get('year')

    agencies = Agency.objects.all()
    count = 1
        
    for agency in agencies:
        if allocation=='PS' and hasSubmittedCoS(year, agency):
            agency_list.append({'count' : count,
                                'name'  : agency.name})
            count+=1
        if allocation=='MOOE' and is_allQRS(year, month, agency) and isMRS(year, month, agency):
            agency_list.append({'count' : count,
                                'name'  : agency.name})
            count+=1

    form_values = {'allocation': allocation, 'month': month, 'year': year}
    data = {'system_name'  : SYSTEM_NAME,
            'year'         : year,
            'month'        : month,
            'allocation'   : allocation,
            'month_str'    : stringify_month(month),
            'allowed_tabs' : get_allowed_tabs(request.user.id),
            'agencies'     : agency_list,
            'form'         : AllocationMonthYearForm(form_values),
            'total'        : count-1
    }
    return render_to_response('./main/agencies_with_comp_reqs_list.html', data, context)


def agenciesIncReqList(request):
    context = RequestContext(request)
    year = datetime.today().year
    month = datetime.today().month
    agency_list = []
    if request.method=='POST':
        month = int(request.POST.get('month'))

    agencies = Agency.objects.all()
    count = 1
    quarterly_reqs = []
    monthly_reqs = []

    for agency in agencies:
        monthly = isMRS(year, month, agency)
        quarterly = is_allQRS(year, month, agency)
        if not monthly:
            req_name = '%s-%s Monthly Physical and Financial Report' %(stringify_month(month-1), year)
            monthly_reqs.append({'name' : req_name})
           
            count+=1

        if not quarterly:
            quarterly_reqs = lqm(year, month, agency)

        agency_list.append({'count' : count,
                            'name'  : agency.name,
                            'monthly_reqs'   : monthly_reqs,
                            'quarterly_reqs' : quarterly_reqs})
        monthly_reqs = []
        quarter_reqs = []
            
    
    data = {'system_name'  : SYSTEM_NAME,
            'year'         : year,
            'quarter_required': strRequiredQuarter(month, year),
            'month'        : month,
            'month_str'    : stringify_month(month),
            'allowed_tabs' : get_allowed_tabs(request.user.id),
            'agencies'     : agency_list,
            'form'         : MonthForm({'month': month}),
            'total'        : count-1}

    return render_to_response('./main/agencies_with_inc_reqs_list.html', data, context)


@login_required(login_url='/main/')
def changePass(request):
    context = RequestContext(request)
    data = {'system_name'  : SYSTEM_NAME,
            'allowed_tabs' : get_allowed_tabs(request.user.id),
            'form'         : ChangePassForm()
           }
    if request.method=="POST":
        
        current_pass = request.POST.get('current_password')
        new_pass = request.POST.get('new_password')
        confirm_pass = request.POST.get('confirm_password')
        user = User.objects.get(id=request.user.id)
        if user.check_password(current_pass) and new_pass==confirm_pass:
            #change password
            user.set_password(new_pass)
            user.save()
            data['s_msg'] = 'Password succesfully changed'
            return render_to_response('./main/change_pass.html', data, context)
        elif not user.check_password(current_pass):
            #current password does not match
            data['e_msg'] = 'Current Password does not match'
            return render_to_response('./main/change_pass.html', data, context)
        else:
            #new_pass and confirm_pass does not match error
            data['e_msg'] = 'New and Confirm Password mismatch'
            return render_to_response('./main/change_pass.html', data, context)
    else:
        return render_to_response('./main/change_pass.html', data, context)


@login_required(login_url='/main/')
@transaction.atomic
def approvedBudget(request):
    cursor = connection.cursor()
    context = RequestContext(request)
    line_agencies = []
    total_ps    = 0
    total_mooe  = 0
    total_co    = 0
    grand_total = 0
    count = 1
    year = datetime.today().year
    if request.method=="POST":
        year = request.POST.get('year')

    #line agencies
    agencies = Agency.objects.filter(a_type = 2, parent_key = 0).order_by('name')
    for agency in agencies:
        agency_budget = {}
        ps   = WFPData.objects.filter(agency=agency, year=year, allocation='PS').aggregate(ps_total=Sum('total'))
        mooe = WFPData.objects.filter(agency=agency, year=year, allocation='MOOE').aggregate(mooe_total=Sum('total'))
        co   = WFPData.objects.filter(agency=agency, year=year, allocation='CO').aggregate(co_total=Sum('total'))
        agency_budget['count'] = count
        agency_budget['id']    = agency.id
        agency_budget['name']  = agency.name
        agency_budget['ps']    = numify(ps['ps_total'])
        agency_budget['mooe']  = numify(mooe['mooe_total'])
        agency_budget['co']    = numify(co['co_total'])
        agency_budget['total'] = agency_budget['ps'] + agency_budget['mooe'] + agency_budget['co']
        #get sub_agencies
        sub_agencies = Agency.objects.filter(parent_key = agency.id).order_by('name')
        agency_budget['sub_agencies'] = []
        sub_count = 0
        for sub_agency in sub_agencies:
            sub_count += 1
            sub_agency_budget = {}
            sub_ps   = WFPData.objects.filter(agency=sub_agency, year=year, allocation='PS').aggregate(ps_total=Sum('total'))
            sub_mooe = WFPData.objects.filter(agency=sub_agency, year=year, allocation='MOOE').aggregate(mooe_total=Sum('total'))
            sub_co   = WFPData.objects.filter(agency=sub_agency, year=year, allocation='CO').aggregate(co_total=Sum('total'))
            sub_agency_budget['count'] = str(count)+'.'+str(sub_count)
            sub_agency_budget['id']    = sub_agency.id
            sub_agency_budget['name']  = sub_agency.name
            sub_agency_budget['ps']    = numify(sub_ps['ps_total'])
            sub_agency_budget['mooe']  = numify(sub_mooe['mooe_total'])
            sub_agency_budget['co']    = numify(sub_co['co_total'])
            sub_agency_budget['total'] = sub_agency_budget['ps'] + sub_agency_budget['mooe'] + sub_agency_budget['co']
            agency_budget['sub_agencies'].append(sub_agency_budget)    
            total_ps   += numify(sub_ps['ps_total'])
            total_mooe += numify(sub_mooe['mooe_total']) 
            total_co   += numify(sub_co['co_total'])

        line_agencies.append(agency_budget)

        total_ps   += numify(ps['ps_total'])
        total_mooe += numify(mooe['mooe_total']) 
        total_co   += numify(co['co_total'])


        count += 1

    #local agencies
    local_agencies = []
    agencies = Agency.objects.filter(a_type = 1, parent_key = 0).order_by('name')
    count = 1
    for agency in agencies:
        agency_budget = {}
        ps   = WFPData.objects.filter(agency=agency, year=year, allocation='PS').aggregate(ps_total=Sum('total'))
        mooe = WFPData.objects.filter(agency=agency, year=year, allocation='MOOE').aggregate(mooe_total=Sum('total'))
        co   = WFPData.objects.filter(agency=agency, year=year, allocation='CO').aggregate(co_total=Sum('total'))
        agency_budget['count'] = count
        agency_budget['id']    = agency.id
        agency_budget['name']  = agency.name
        agency_budget['ps']    = numify(ps['ps_total'])
        agency_budget['mooe']  = numify(mooe['mooe_total'])
        agency_budget['co']    = numify(co['co_total'])
        agency_budget['total'] = agency_budget['ps'] + agency_budget['mooe'] + agency_budget['co']
        #get sub_agencies
        sub_agencies = Agency.objects.filter(parent_key = agency.id).order_by('name')
        agency_budget['sub_agencies'] = []
        sub_count = 0
        for sub_agency in sub_agencies:
            sub_count += 1
            sub_agency_budget = {}
            sub_ps   = WFPData.objects.filter(agency=sub_agency, year=year, allocation='PS').aggregate(ps_total=Sum('total'))
            sub_mooe = WFPData.objects.filter(agency=sub_agency, year=year, allocation='MOOE').aggregate(mooe_total=Sum('total'))
            sub_co   = WFPData.objects.filter(agency=sub_agency, year=year, allocation='CO').aggregate(co_total=Sum('total'))
            sub_agency_budget['count'] = str(count)+'.'+str(sub_count)
            sub_agency_budget['id']    = sub_agency.id
            sub_agency_budget['name']  = sub_agency.name
            sub_agency_budget['ps']    = numify(sub_ps['ps_total'])
            sub_agency_budget['mooe']  = numify(sub_mooe['mooe_total'])
            sub_agency_budget['co']    = numify(sub_co['co_total'])
            sub_agency_budget['total'] = sub_agency_budget['ps'] + sub_agency_budget['mooe'] + sub_agency_budget['co']
            agency_budget['sub_agencies'].append(sub_agency_budget)    
            total_ps   += numify(sub_ps['ps_total'])
            total_mooe += numify(sub_mooe['mooe_total']) 
            total_co   += numify(sub_co['co_total'])

        local_agencies.append(agency_budget)

        total_ps   += numify(ps['ps_total'])
        total_mooe += numify(mooe['mooe_total']) 
        total_co   += numify(co['co_total'])
        count += 1

    cursor.execute("select distinct(year) from wfp_data")
    years = dictfetchall(cursor)

    total_budget = {'total_ps'   : total_ps,
                    'total_mooe' : total_mooe,
                    'total_co'   : total_co,
                    'grand_total': total_ps+total_mooe+total_co}

    data ={'year'           : year,
           'line_agencies'  : line_agencies,
           'local_agencies' : local_agencies,
           'system_name'    : SYSTEM_NAME,
           'allowed_tabs'   : get_allowed_tabs(request.user.id),
           'total_budget'   : total_budget,
           'years'          : years}

    
    return render_to_response('./main/approved_budget.html', data, context)


def getSubAgencies(count, fetched_agencies, parent_key, sub_agencies, total):
    sub_agencies = []
    sub_count = 0.1
    for agency in fetched_agencies:
        balance = numify(agency['balance'])
        if agency['pa_key'] == parent_key and balance > 0:
            sub_agencies.append({'no'     : count+sub_count, 
                                 'agency' : agency['name'],
                                 'amount' : balance})
            total += balance
            sub_count += 0.1
    return

@transaction.atomic
def savePerformanceReport(request):
    cursor = connection.cursor()
    action = request.POST.get('action')
    
    if action == "add":
        month = int(request.POST.get('month'))
        year = int(request.POST.get('year', datetime.today().year))
        activity = WFPData.objects.get(id=request.POST.get('activity'))
        received = request.POST.get('received')
        incurred = request.POST.get('incurred')
        remarks = request.POST.get('remarks')
        accomplished_target = request.POST.getlist('pt_ids[]')
        
        #update activity
        perf_rep = PerformanceReport(activity = activity,
                                     year = year,
                                     month = month,
                                     received = received,
                                     incurred = incurred,
                                     remarks = remarks
                                )
        perf_rep.save()
        for acc_t in accomplished_target:
            acc_target_query = "update performancetarget set "
            acc_target_query+= month_acc_dict[month] + " = %s "
            acc_target_query+= "where id=%s"
            cursor.execute(acc_target_query, [request.POST.get(acc_t),acc_t])
        
        return HttpResponse('Ok')

    else:
        mpfro_id = request.POST.get('mpfro_id')
        month = int(request.POST.get('month'))
        received = request.POST.get('received')
        incurred = request.POST.get('incurred')
        remarks = request.POST.get('remarks')
        accomplished_target = request.POST.getlist('pt_ids[]')
        
        perf_rep = PerformanceReport.objects.get(id=mpfro_id)
        perf_rep.received = received
        perf_rep.incurred = incurred
        perf_rep.remarks = remarks
        perf_rep.save()

        for acc_t in accomplished_target:
            acc_target_query = "update performancetarget set "
            acc_target_query+= month_acc_dict[month] + " = %s "
            acc_target_query+= "where id=%s"
            cursor.execute(acc_target_query, [request.POST.get(acc_t),acc_t])
        
        return HttpResponse('Ok')
    

def hasSubmittedCoS(year, agency):
    try:
        cos_submitted = COSSubmission.objects.filter(date_submitted__year=year, agency=agency).count()
        return cos_submitted > 0
    except COSSubmission.DoesNotExist:
        return False



@login_required(login_url = '/main')
@transaction.atomic
def smca(request):#schedule of monthly cash allocation
    context = RequestContext(request)
    cursor = connection.cursor()
    data = {'system_name' : SYSTEM_NAME,
            'allowed_tabs': get_allowed_tabs(request.user.id),
            'search_form' : MCASearchForm({'month' : datetime.today().month}),
            'cur_date'    : time.strftime('%B %d, %Y'),
            'year'        : datetime.today().year,
            'month'       : datetime.today().month,
            'allocation'  : 'PS',
    }
    years = []
    for i in range(2013, datetime.today().year+1):
        years.append(i)
    data['years'] = years 

    if request.method=='POST':
        data['month'] = int(request.POST.get('month'))
        data['year']  = int(request.POST.get('year'))
        data['allocation'] = request.POST.get('allocation')
        data['search_form'] = MCASearchForm({'month'      : data['month'],
                                             'allocation' : data['allocation']
                                           })

    quarter = quarterofMonth(data['month'])
    req_year = data['year']
    if quarter == 4:
        req_year-=1
        
    qualified_agencies = []
    agencies = Agency.objects.filter(parent_key = 0)
    if data['allocation']=='PS':
        count = 0
        total = 0
        for agency in agencies:
            sub_agencies = Agency.objects.filter(parent_key = agency.id)
            amount = aps_smca(agency, data['year'], data['month'])
            sub_agency_qualified_count = 0
            qualified_sub_agencies = []
            for sub_agency in sub_agencies:
                sub_amount = aps_smca(sub_agency, data['year'], data['month'])
                if sub_amount > 0:
                    sub_agency_qualified_count += 1
                    qualified_sub_agencies.append({'sub_count' : str(count+1)+"."+str(sub_agency_qualified_count),
                                                   'name'      : sub_agency.name,
                                                   'amount'    : sub_amount})
                    total += sub_amount
            if sub_agency_qualified_count > 0 or amount > 0:
                count+= 1 
                qualified_agencies.append({'count' : count,
                                           'name'  : agency.name,
                                           'amount': amount,
                                           'qualified_sub_agencies' : qualified_sub_agencies})
                total += amount
        data['qualified_agencies'] = qualified_agencies
        data['str_month'] = stringify_month(int (data['month'])) 
        data['total'] = total
        return render_to_response('./main/smca.html', data, context)
    elif data['allocation'] == 'MOOE':
        total = 0
        count = 0
        for agency in agencies:
            sub_agencies = Agency.objects.filter(parent_key = agency.id)
            amount = amooe_smca(agency, data['year'], data['month'])
            sub_agency_qualified_count = 0
            qualified_sub_agencies = []
            for sub_agency in sub_agencies:
                sub_amount = amooe_smca(sub_agency, data['year'], data['month'])
                if sub_amount > 0:
                    sub_agency_qualified_count += 1
                    qualified_sub_agencies.append({'sub_count' : str(count+1)+"."+str(sub_agency_qualified_count),
                                                   'name'      : sub_agency.name,
                                                   'amount'    : sub_amount})
                    total += sub_amount
            if sub_agency_qualified_count > 0 or amount > 0:
                count+= 1 
                qualified_agencies.append({'count' : count,
                                           'name'  : agency.name,
                                           'amount': amount,
                                           'qualified_sub_agencies' : qualified_sub_agencies})
                total += amount
        data['qualified_agencies'] = qualified_agencies
        data['str_month'] = stringify_month(int (data['month'])) 
        data['total'] = total
        return render_to_response('./main/smca.html', data, context)
    else:#CO
        total = 0
        count = 0
        for agency in agencies:
            sub_agencies = Agency.objects.filter(parent_key = agency.id)
            amount = aco_smca(agency, data['year'], data['month'])
            sub_agency_qualified_count = 0
            qualified_sub_agencies = []
            for sub_agency in sub_agencies:
                sub_amount = aco_smca(sub_agency, data['year'], data['month'])
                if sub_amount > 0:
                    sub_agency_qualified_count += 1
                    qualified_sub_agencies.append({'sub_count' : str(count+1)+"."+str(sub_agency_qualified_count),
                                                   'name'      : sub_agency.name,
                                                   'amount'    : sub_amount})
                    total += sub_amount
            if sub_agency_qualified_count > 0 or amount > 0:
                count+= 1 
                qualified_agencies.append({'count' : count,
                                           'name'  : agency.name,
                                           'amount': amount,
                                           'qualified_sub_agencies' : qualified_sub_agencies})
                total += amount
        data['qualified_agencies'] = qualified_agencies
        data['str_month'] = stringify_month(int (data['month'])) 
        data['total'] = total
        return render_to_response('./main/smca.html', data, context)
        

def aps_smca(agency, year, month, allocation = "PS"):
    
    budget = getAllocation(agency, allocation, year, month)
        
    release = AllotmentReleases.objects.filter(agency=agency, allocation=allocation, month=month, year=year).aggregate(Sum('amount_release'))
    amount_release = release['amount_release__sum']
        
    contracts_submitted = COSSubmission.objects.filter(agency=agency, date_submitted__year = year)
    if (numify(budget)-numify(amount_release)) > 0 and len(contracts_submitted) > 0:
        return numify(budget) - numify(amount_release)
    else:
        return 0


def amooe_smca(agency, year, month, allocation='MOOE'):
    budget = getAllocation(agency, allocation, year, month)
    release =  release = AllotmentReleases.objects.filter(agency=agency, allocation=allocation, month=month, year=year).aggregate(Sum('amount_release'))
    amount_release = release['amount_release__sum']
    quarter_requirements = QuarterlyReq.objects.all()
    quarter = quarterofMonth(month)
    quarter_req_submission = None
    if quarter==4:
        quarter_req_submission = QuarterReqSubmission.objects.filter(agency=agency, quarter=quarter, year=(year-1))
        print (year-1)
    else:
        quarter_req_submission = QuarterReqSubmission.objects.filter(agency=agency, quarter=quarter, year=year)
    if len(quarter_requirements)==len(quarter_req_submission) and budget-numify(amount_release) > 0:
        return budget-numify(amount_release)
    else:
        return 0
        
def aco_smca(agency, year, month, allocation='CO'):
    budget = getAllocation(agency, allocation, year, month)
    release =  release = AllotmentReleases.objects.filter(agency=agency, allocation=allocation, month=month, year=year).aggregate(Sum('amount_release'))
    amount_release = release['amount_release__sum']
    if budget - numify(amount_release) > 0:
        return budget - numify(amount_release)
    else:
        return 0


def getAllocation(agency, allocation, year, month):
    budget = 0
    if month==1:
        allocation = WFPData.objects.filter(agency=agency, year = year, allocation=allocation).aggregate(Sum('jan'))
        budget = allocation['jan__sum']
    elif month==2:
        allocation = WFPData.objects.filter(agency=agency, year = year, allocation=allocation).aggregate(Sum('feb'))
        budget = allocation['feb__sum']
    elif month==3:
        allocation = WFPData.objects.filter(agency=agency, year = year, allocation=allocation).aggregate(Sum('mar'))
        budget = allocation['mar__sum']
    elif month==4:
        allocation = WFPData.objects.filter(agency=agency, year = year, allocation=allocation).aggregate(Sum('apr'))
        budget = allocation['apr__sum']
    elif month==5:
        allocation = WFPData.objects.filter(agency=agency, year = year, allocation=allocation).aggregate(Sum('may'))
        budget = allocation['may__sum']
    elif month==6:
        allocation = WFPData.objects.filter(agency=agency, year = year, allocation=allocation).aggregate(Sum('jun'))
        budget = allocation['jun__sum']
    elif month==7:
        allocation = WFPData.objects.filter(agency=agency, year = year, allocation=allocation).aggregate(Sum('jul'))
        budget = allocation['jul__sum']
    elif month==8:
        allocation = WFPData.objects.filter(agency=agency, year = year, allocation=allocation).aggregate(Sum('aug'))
        budget = allocation['aug__sum']
    elif month==9:
        allocation = WFPData.objects.filter(agency=agency, year = year, allocation=allocation).aggregate(Sum('sept'))
        budget = allocation['sept__sum']
    elif month==10:
        allocation = WFPData.objects.filter(agency=agency, year = year, allocation=allocation).aggregate(Sum('oct'))
        budget = allocation['oct__sum']
    elif month==11:
        allocation = WFPData.objects.filter(agency=agency, year = year, allocation=allocation).aggregate(Sum('nov'))
        budget = allocation['nov__sum']
    else:
        allocation = WFPData.objects.filter(agency=agency, year = year, allocation=allocation).aggregate(Sum('dec'))
        budget = allocation['dec__sum']
    return numify(budget)

    

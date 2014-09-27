from django.shortcuts import render, render_to_response, redirect, RequestContext
from django.db import transaction, connection
from django.db.models import Sum, Avg
from django.http import  HttpResponseRedirect, HttpResponse
from django.conf import settings
from django.conf.urls.static import static
from fund.views import getBudget, getRelease
from .forms import (UserForm, LoginForm, AgencyForm, 
                    MonthForm, ChangePassForm, AllocationMonthYearForm)
from rbmo.models import (UserGroup,
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
                         PerformanceTarget
)
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required, permission_required
from helpers.helpers import *
from fund.views import isMRS, is_allQRS, lqm, getReleaseAmount
from fund.forms import MCASearchForm
from datetime import datetime, date
from decimal import *
import time
import sys

# Create your views here.
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


@login_required(login_url='/admin/')
def submitCOS(request):#submit Contract of Service
    submit = request.POST.get('cos_submit')
    agency_id = request.POST.get('agency_id')
    try:
        if submit is not None and agency_id is not None:
            today = datetime.today()
            agency = Agency.objects.get(id=agency_id)
            cos_submit = COSSubmission(agency=agency, date_submitted=today)
            cos_submit.save()
            return HttpResponseRedirect('/admin/manage_agency_docs/'+str(agency.id)+'/'+str(today.year))
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
                return HttpResponseRedirect('/admin/home/')
            else:
                data['e_msg'] = "Invalid Email or Password"
                return render_to_response('./admin/login.html', data, context)
        else:
            data['frm_errors'] = login_form.errors
            return render_to_response('./admin/login.html', data, context)
    else:
        return render_to_response('./admin/login.html', data, context)


@login_required(login_url='/admin/')
def home(request):
    context = RequestContext(request)
    cursor = connection.cursor()

    balances = []
    agencies = Agency.objects.all()
    year = datetime.today().year
    total_budget = 0
    total_release = 0
    total_balance = 0
    for agency in agencies:
        agency_balances = {}
        agency_balances['agency_id'] = agency.id
        agency_balances['agency_name'] = agency.name
        '''
        total budget
        '''
        ps = getBudget(agency.id, 'PS', year)
        mooe = getBudget(agency.id, 'MOOE', year)
        co = getBudget(agency.id, 'CO', year) 
        agency_balances['budget'] = ps + mooe + co
        '''
        total release
        '''
        ps = getRelease(agency, 'PS', year)
        mooe = getRelease(agency, 'MOOE', year)
        co = getRelease(agency, 'CO', year)
        agency_balances['release'] = ps + mooe + co 
        #remaining balance
        agency_balances['balance'] = agency_balances['budget'] - agency_balances['release']
        balances.append(agency_balances)
        total_budget  += agency_balances['budget']
        total_release += agency_balances['release']
        total_balance += agency_balances['balance']
    
    
    data = {'year'         : year,
            'system_name'  : SYSTEM_NAME,
            'allowed_tabs' :get_allowed_tabs(request.user.id),
            'balances'     : balances,
            'total_sum'    :{'total_budget'  : total_budget,
                             'total_release' : total_release,
                             'total_balance' : total_balance},
            'today'        : time.strftime('%D %d, %Y')
        }

    return render_to_response('./admin/home.html', data, context)


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


@login_required(login_url='/admin/')
def users(request):
    context = RequestContext(request)
    data = { 'page_title': 'Registered Users',
             'system_name': SYSTEM_NAME}
    users = User.objects.all()
    data['users'] = users  
    data['allowed_tabs'] = get_allowed_tabs(request.user.id)
    return render_to_response('./admin/users.html', data, context)


@login_required(login_url='/admin/')
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
        return HttpResponseRedirect('/admin/')
        
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
            return render_to_response('./admin/user_form.html', data, context)
        elif data['action']=='edit' and user_form.is_valid():#edit user
            user = User.objects.get(id=request.POST.get('user_id'))
            user.email = user_form.cleaned_data['email']
            user.first_name = user_form.cleaned_data['first_name']
            user.last_name = user_form.cleaned_data['last_name']
            user.save()
            data['s_msg'] = "User Succesfully updated"
            return render_to_response('./admin/user_form.html', data, context)
        else:#invalid form inputs
            data['frm_errors'] = user_form.errors
            data['form'] = user_form
            return render_to_response('./admin/user_form.html', data, context)
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
                return render_to_response('./admin/user_form.html', data, context)
            except:
                return render_to_response('./admin/user_form.html', data, context)
        else:
            return render_to_response('./admin/user_form.html', data, context)


@login_required(login_url='/admin/')
@transaction.atomic
def agencies(request):
    context = RequestContext(request)

    if 'admin_agency_id' in request.session:
        del request.session['admin_agency_id']

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
    return render_to_response('./admin/agencies.html', data, context)


@login_required(login_url='/admin/')
def getAgenciesbySector(request):
    context = RequestContext(request)
    try:
        sectors_selected = request.POST.getlist('sector[]')
        print sectors_selected
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

        return render_to_response('./admin/agencies.html', data, context)
    except Agency.DoesNotExist:
        return HttpResponse('Error 404 Page not Found')

    


@login_required(login_url='/admin/')
def addEditAgency(request):
    context = RequestContext(request)
    data = {'form': AgencyForm(),
            'mode': request.GET.get('action', 'add'),
            'system_name': SYSTEM_NAME
    }
    if not has_permission(request.user.id, 'record', 'agency'):
        return HttpResponseRedirect('/admin/agencies')

    data['allowed_tabs'] = get_allowed_tabs(request.user.id)

    if request.method == 'POST':
        action = request.POST.get('action', 'add')
        agency_frm = AgencyForm(request.POST)
        if action=='add' and agency_frm.is_valid():
            addAgency(request, agency_frm)
            data['s_msg'] = 'New Agency/Office was succesfully added.'
            return render_to_response('./admin/agency_form.html', data, context)
        elif action=='edit' and agency_frm.is_valid():
            agency_id = request.POST.get('id')
            agency = Agency.objects.get(id=agency_id)
            agency.name = agency_frm.cleaned_data['name']
            agency.email = agency_frm.cleaned_data['email']
            agency.sector = agency_frm.cleaned_data['sector']
            #agency.a_type = agency_frm.cleaned_data['a_type']
            #agency.pa_key = request.POST.get('head_agency')
            agency.save()
            data['s_msg'] = 'Agency/Office was succesfully Updated.'
            return render_to_response('./admin/agency_form.html', data, context)
        else:
            data['frm_errors'] = agency_frm.errors
            data['form'] = agency_frm
            return render_to_response('./admin/agency_form.html', data, context)
    else:
        data['action'] = request.GET.get('action', 'add')
        if data['action']=='edit':
            try:
                agency_id = request.GET.get('a_id')
                agency = Agency.objects.get(id=agency_id)
                data['form'] = AgencyForm({'name'  : agency.name,
                                           'email' : agency.email,
                                           'sector': agency.sector
                                           #'a_type': agency.a_type
                                       })
                
                data['agency_id'] = agency.id
             #   data['pa_key'] = agency.pa_key
             #  data['agencies_selection'] = Agency.objects.exclude(id=agency.id)
                return render_to_response('./admin/agency_form.html', data, context)
            except Agency.DoesNotExist:
                return render_to_response('./admin/agency_form.html', data, context)
        else:
            data['agencies_selection'] = Agency.objects.all()
            return render_to_response('./admin/agency_form.html', data, context)


@login_required(login_url = '/admin/')
@transaction.atomic
def manageAgencyDocs(request, agency_id, year = datetime.today().year):
    context = RequestContext(request)
    try:
        current_year = datetime.today().year
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
#        if 'agency_id' not in request.session:
 #           request.session['admin_agency_id'] = agency_id

        data = {'system_name'  : SYSTEM_NAME,
                'current_tab'  : "Requirements",
                'allowed_tabs' : get_allowed_tabs(request.user.id),
                'agency_tabs'  : getAgencyTabs(request.user.id, agency.id),
                'agency'       : agency,
                'years'        : years,
                'year'         : year,
                'monthly'      : monthly,
                'quarterly'    : quarterly,
                'q1_req_s'     : q1_req_s,
                'q2_req_s'     : q2_req_s,
                'q3_req_s'     : q3_req_s,
                'q4_req_s'     : q4_req_s,
                'cos_submitted': cos_submitted,
                'quarter_req_submitted' : getSubmittedQuarterReq(year, agency, 1)}

        return render_to_response('./admin/agency_docs_recording.html', data, context)
    except: #Agency.DoesNotExist
        return HttpResponseRedirect('/admin/agencies')  

def getSumittedQReq(year, agency, quarter):
    quarter_req_submitted = QuarterReqSubmission.objects.filter(year=year, agency=agency, quarter=quarter)

    quarter_submitted = []
    for qrs in quarter_req_submitted:
        quarter_submitted.append(qrs.requirement.id)
    return quarter_submitted


def getSubmittedQuarterReq(year, agency, quarter):
    quarter_req_submitted = QuarterReqSubmission.objects.filter(year=year, agency=agency, quarter=quarter)
    return quarter_req_submitted


def getDisplaySubmittedQReq(request):
    context = RequestContext(request)
    try:
        year = request.GET.get("year")
        agency_id = request.GET.get("agency_id")
        agency = Agency.objects.get(id=agency_id)
        quarter = request.GET.get("quarter")
        submitted_req = getSubmittedQuarterReq(year, agency, quarter)
        data = {'quarter_req_submitted' : submitted_req}
        return render_to_response("./admin/submitted_qreqtable.html", data, context)
    except:
        return HttpResponse("</h3>Error</h3><p>Invalid Request Found</p>")


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
    return HttpResponseRedirect('/admin/manage_agency_docs/'+str(agency.id)+'/')


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
        return HttpResponseRedirect('/admin/manage_agency_docs?agency_id='+str(agency.id))


@login_required(login_url='/admin/')
def delSubmitReqs(request):
    docs_sub_id = request.GET.get('doc_sub')
    doc_sub = DocsSubmitted.objects.get(id=docs_sub_id)
    agency_id = doc_sub.agency.id
    doc_sub.delete()
    return HttpResponseRedirect('/admin/manage_agency_docs?agency_id='+str(agency_id))

@transaction.atomic
def addAgency(request, agency_frm):
    agency = Agency(name = agency_frm.cleaned_data['name'],
                    email = agency_frm.cleaned_data['email'],
                    sector = agency_frm.cleaned_data['sector'],
                    acces_key = str(agency_frm.cleaned_data['email'])+'_1234'
                    #a_type = agency_frm.cleaned_data['a_type'],
                    #pa_key = request.POST.get('head_agency')
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



@login_required(login_url='/admin/')
@transaction.atomic
def mpfroReports(request, agency_id):
    context = RequestContext(request)
    cursor = connection.cursor()
    data  = {'system_name' : SYSTEM_NAME,
             'allowed_tabs': get_allowed_tabs(request.user.id),
             'agency_id'   : agency_id,
             'year'        : datetime.today().year,
             'month'       : datetime.today().month,
             'month_form'  : MonthForm({'month': datetime.today().month})
    }
    try:

        if request.method=='POST':
            data['year'] = request.POST.get('year')
            data['month'] = request.POST.get('month')

        agency = Agency.objects.get(id=data['agency_id'])        
        perf_accs_query = "select "+months[int(data['month'])]+" as budget, "
        perf_accs_query+= "wfp_data.activity, "
        perf_accs_query+= "performance_report.* "
        perf_accs_query+= "from performance_report inner join wfp_data on "
        perf_accs_query+= "wfp_data.id = performance_report.activity_id "
        perf_accs_query+= "and wfp_data.agency_id = %s "
        perf_accs_query+= "and performance_report.year=%s "
        perf_accs_query+= "and performance_report.month=%s"

        cursor.execute(perf_accs_query, [agency.id, data['year'], data['month']])
        perf_accs = dictfetchall(cursor)
        monthly_acts_reports = []
        for acc in perf_accs:
            query = "select indicator, "+months[int(data['month'])-1]+" as target, "+month_acc_dict[int(data['month'])]+" as acc from performancetarget where wfp_activity_id=%s"
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
        data['agency'] = agency
        data['agency_tabs'] = getAgencyTabs(request.user.id, agency.id)
        data['current_tab'] = "Monthly Report of Operation"
        yrs_query = "select distinct(year) from performance_report"
        cursor.execute(yrs_query)
        data['years'] = dictfetchall(cursor)
        data['monthly_acts_reports'] = monthly_acts_reports
        data['str_month'] = stringify_month(int(data['month']))
        return render_to_response('./admin/monthly_reps.html', data, context)
    except:
        return HttpResponseRedirect('/admin/agencies')


@login_required(login_url="/admin/")
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
            return render_to_response('./admin/mpfro_form.html', data, context)
        else: #edit
            mpfro_id = request.GET.get('mpfro_id')
            activity_info = PerformanceReport.objects.get(id = mpfro_id)
            accs_query = "select id, indicator, "+wfp_month_lookup[activity_info.month]+" as target," + month_acc_dict[activity_info.month] + " as accomplished from performancetarget where wfp_activity_id = %s"
            cursor.execute(accs_query, [activity_info.activity.id])
            performance_accs = dictfetchall(cursor)
            data['activity_info'] = activity_info
            data['performance_accs'] = performance_accs
            data['str_month'] = stringify_month(activity_info.month)
            return render_to_response('./admin/mpfro_form.html', data, context)
    except Agency.DoesNotExist and PerformanceReport.DoesNotExist:
        return HttpResponse('Page Not Found Error!')


@login_required(login_url='/admin/')
@transaction.atomic
def submitQuarterReq(request):
    agency = Agency.objects.get(id=request.POST.get('agency_id'))
    year = request.POST.get('year', time.strftime('%Y'))
    quarter_req_submitted = request.POST.getlist('qr[]')
    for quarter in quarter_req_submitted:
        quarter = quarter.split(';')
        quarter_submit = QuarterReqSubmission(year = year,
                                              agency = agency,
                                              requirement = QuarterlyReq.objects.get(id=int(quarter[1])),
                                              quarter = int(quarter[0]),
                                              date_submitted = datetime.now(),
                                              user = request.user
                                          )
        quarter_submit.save()

    return HttpResponseRedirect('/admin/manage_agency_docs/'+str(agency.id)+'/'+str(year)+'/')


@transaction.atomic
def allot_releases(request):
    #generates reports all releases for all agencies
    context = RequestContext(request)
    data = {'system_name': SYSTEM_NAME,
            'allowed_tabs' : get_allowed_tabs(request.user.id)
        }
    data['allowed_tabs'] = get_allowed_tabs(request.user.id)
    agencies_releases = []
    total_ps = 0
    total_mooe = 0
    total_co = 0
    agencies = Agency.objects.all()
    count = 0
    for agency in agencies:
        #get total ps_release
        ps = AllotmentReleases.objects.filter(agency=agency, allocation='PS').aggregate(Sum('amount_release'))
        #get total mooe release
        mooe = AllotmentReleases.objects.filter(agency=agency, allocation='MOOE').aggregate(Sum('amount_release'))
        #get total co release
        co = AllotmentReleases.objects.filter(agency=agency, allocation='co').aggregate(Sum('amount_release'))
        total = numify( ps['amount_release__sum']) + numify( mooe['amount_release__sum']) + numify( co['amount_release__sum'])
        agencies_releases.append({'count' : count,
                                  'agency': agency.name,
                                  'ps'    : numify(ps['amount_release__sum']),
                                  'mooe'  : numify(mooe['amount_release__sum']),
                                  'co'    : numify(co['amount_release__sum']),
                                  'total' : total
                              })
        total_ps = total_ps + numify( ps['amount_release__sum'])
        total_mooe = total_mooe + numify( mooe['amount_release__sum'])
        total_co = total_co + numify( co['amount_release__sum'])        
        count = count + 1
    
    
    data['agencies_releases'] = agencies_releases
    data['grand_total'] = {'ps': total_ps, 'mooe': total_mooe, 'co': total_co, 'total': total_ps+total_mooe+total_co}
    data['today'] = date.today()
    return render_to_response('./admin/allotment_releases_report.html', data, context)


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
    return render_to_response('./admin/yearly_fund.html', data, context)  


def fundDistribution(request):
    cursor  = connection.cursor()
    context = RequestContext(request)
    data  = {'system_name' : SYSTEM_NAME,
             'allowed_tabs' : get_allowed_tabs(request.user.id)
    }

    year  = datetime.today().year 
    wfp = WFPData.objects.filter(year=year).aggregate(Sum('total')) 
    total = numify(wfp['total__sum'])
    query = '''
    select sector.id, sector.name, sum(wfp_data.total) as total
    from sector, agency, wfp_data 
    where sector.id = agency.sector_id and agency.id = wfp_data.agency_id 
    group by sector.id;
    '''

    cursor.execute(query)
    sectors = dictfetchall(cursor)
    sector_budget_percent = []

    for sector in sectors:
        sector_budget_percent.append({'id'      : sector['id'],
                                      'name'    : sector['name'], 
                                      'percent' : int(round((sector['total']/total)*100))})
    data['sectors'] = sector_budget_percent
    return render_to_response('./admin/fund_distrib.html', data, context)


@login_required(login_url='/admin/')    
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

    agencies = Agency.objects.all()
    agency_monthly_releases = []
    total_monthly_release = {'jan' : 0, 'feb': 0, 'mar': 0, 'apr': 0,
                           'may' : 0, 'jun': 0, 'jul': 0, 'aug':0,
                           'sept' : 0, 'oct': 0, 'nov': 0 ,'dec':0}
    count = 1
    grand_total = 0
    for agency in agencies:
        agency_release = {}
        agency_release['no'] = count
        agency_release['name'] = agency.name
        temp_per_agency_total = 0
        for i in range(1, data['current_month']):
            total = AllotmentReleases.objects.filter(agency=agency, month=i, year=year, allocation=allocation).aggregate(Sum('amount_release'))
            agency_release[months[i-1]] = numify(total['amount_release__sum'])
            total_monthly_release[months[i-1]] += numify(total['amount_release__sum'])
            temp_per_agency_total += numify(total['amount_release__sum'])
        agency_release['total'] = temp_per_agency_total
        agency_monthly_releases.append(agency_release)
        grand_total += temp_per_agency_total
        count+=1
    data['agency_monthly_releases'] = agency_monthly_releases
    data['total_monthly_releases']= total_monthly_release
    data['grand_total'] = grand_total
    data['allocation'] = allocation
            
    return render_to_response('./admin/total_monthly_release.html', data, context)
    
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
    return render_to_response('./admin/agencies_with_comp_reqs_list.html', data, context)


def agenciesIncReqList(request):
    context = RequestContext(request)
    year = datetime.today().year
    month = datetime.today().month
    agency_list = []
    if request.method=='POST':
        month = int(request.POST.get('month'))

    agencies = Agency.objects.all()
    count = 1
    for agency in agencies:
        monthly = isMRS(year, month, agency)
        quarterly = is_allQRS(year, month, agency)
        if not monthly or not quarterly:
            lack_reqs = lqm(year, month, agency)
            if not monthly:
                req_name = '%s - Monthly Physical and Financial Report' %(stringify_month(month-1))
                lack_reqs.append({'name' : req_name})
            agency_list.append({'count' : count,
                                'name'  : agency.name,
                                'reqs'  : lack_reqs
                            })
            count+=1
    
    data = {'system_name'  : SYSTEM_NAME,
            'year'         : year,
            'month'        : month,
            'month_str'    : stringify_month(month),
            'allowed_tabs' : get_allowed_tabs(request.user.id),
            'agencies'     : agency_list,
            'form'         : MonthForm({'month': month}),
            'total'        : count-1
    }
    return render_to_response('./admin/agencies_with_inc_reqs_list.html', data, context)


@login_required(login_url='/admin/')
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
            return render_to_response('./admin/change_pass.html', data, context)
        elif not user.check_password(current_pass):
            #current password does not match
            data['e_msg'] = 'Current Password does not match'
            return render_to_response('./admin/change_pass.html', data, context)
        else:
            #new_pass and confirm_pass does not match error
            data['e_msg'] = 'New and Confirm Password mismatch'
            return render_to_response('./admin/change_pass.html', data, context)
    else:
        return render_to_response('./admin/change_pass.html', data, context)


@login_required(login_url='/admin/')
@transaction.atomic
def approvedBudget(request):
    cursor = connection.cursor()
    context = RequestContext(request)
    agencies_app_budget = []
    total_ps    = 0
    total_mooe  = 0
    total_co    = 0
    grand_total = 0
    count = 1

    query = '''select agency.*, 
    (select sum(wfp_data.total) from wfp_data where wfp_data.agency_id=agency.id and year=%s and allocation='PS') as ps,
    (select sum(wfp_data.total) from wfp_data where wfp_data.agency_id=agency.id and year=%s and allocation='MOOE') as mooe,
    (select sum(wfp_data.total) from wfp_data where wfp_data.agency_id=agency.id and year=%s and allocation='CO') as co
    from agency'''

    yrs_query = "select distinct(year) from wfp_data"
    cursor.execute(yrs_query)
    years = dictfetchall(cursor)
    year = datetime.today().year
    if request.method=='POST':
        year  = request.POST.get('year')
    
    cursor.execute(query, [year, year, year])
    agencies_budget = dictfetchall(cursor)
    
    for agency in agencies_budget:
        agencies_app_budget.append({
            'count' : count,
            'id'    : agency['id'],
            'name'  : agency['name'],
            'ps'    : numify(agency['ps']),
            'mooe'  : numify(agency['mooe']),
            'co'    : numify(agency['co']),
            'total' : numify(agency['ps']) + numify(agency['mooe']) + numify(agency['co'])
        })
        total_ps   += numify(agency['ps']) 
        total_mooe += numify(agency['mooe']) 
        total_co   += numify(agency['co']) 
        grand_total+= total_ps + total_mooe + total_co 
        count+=1
        
    total_budget = {'total_ps'   : total_ps,
                    'total_mooe' : total_mooe,
                    'total_co'   : total_co,
                    'grand_total': grand_total
                }

    data ={'year' : year,
           'agencies_app_budget' : agencies_app_budget,
           'system_name'     : SYSTEM_NAME,
           'allowed_tabs'    : get_allowed_tabs(request.user.id),
           'total_budget'    : total_budget,
           'years'           : years
    }
    return render_to_response('./admin/approved_budget.html', data, context)
    

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
    
    if data['allocation']=='PS':
        query  = "select agency.* , (select sum("+ wfp_month_lookup[data['month']] +") "
        query += "from wfp_data where year=%s and agency_id=agency.id "
        query += "and allocation='PS') as amount, "
        query += "(select sum(amount_release) from allotmentreleases where "
        query += "agency_id=agency.id and allocation='PS' "
        query += "and month=%s and year=%s) as total_release from agency order by agency.name"
        cursor.execute(query, [data['year'], data['month'], data['year']])
        data['allocation_str'] = "Personnel Services"
        agencies = dictfetchall(cursor)

    elif data['allocation'] == 'MOOE':
        month_req = data['month']-1
        if month_req == 0:
            month_req = 12
        
        query  = "select agency.* , "
        query += "(select sum("+ wfp_month_lookup[data['month']] +") "
        query += "from wfp_data where "
        query += "year=%s and agency_id=agency.id and allocation='MOOE') "
        query += "as amount , " #year
        query += "(select sum(amount_release) from allotmentreleases where "
        query += "agency_id=agency.id and allocation='MOOE' "
        query += "and month=%s and year=%s) as total_release " #year
        query += "from agency, monthly_req_submitted where "
        query += "(select count(*) from quarterly_req)= "
        query += "(select count(*) from quarter_req_submitted "
        query += "where year=%s and quarter=%s and agency_id=agency.id) " #req_year
        query += "and monthly_req_submitted.agency_id=agency.id "
        query += "and month=%s and  year=%s group by agency.id order by agency.name " #req_year
        cursor.execute(query, [data['year'],
                               data['month'],
                               data['year'],
                               req_year,
                               quarter,
                               month_req,
                               req_year
                           ]
        )
        data['allocation_str'] = "Maintenance and other Operating Expenses"
        agencies = dictfetchall(cursor)
    else:
        query = "select agency.* , (select sum("+ wfp_month_lookup[data['month']] +") "
        query+= "from wfp_data where year=%s and agency_id=agency.id "
        query+= "and allocation='CO') as amount, "
        query+= "(select sum(amount_release) from allotmentreleases where "
        query+= "agency_id=agency.id and allocation='co' "
        query+= "and month=%s and year=%s) as total_release from agency order by agency.name"
        cursor.execute(query, [data['year'], data['month'], data['year']])
        agencies = dictfetchall(cursor)
        data['allocation_str'] = "Capital Outlay"
    
    agencies_allocation = []
    locally_funded = []
    count = 1
    total = 0
    for agency in agencies:
        balance = numify(agency['amount']) - numify(agency['total_release'])
        '''
        if agency['a_type'] == "lf":
        
           if agency['pa_key'] == 0 and balance > 0:
               sub_agencies = []
               locally_funded.append({'no'     : count, 
                                      'agency' : agency['name'],
                                      'amount' : balance})
               getSubAgencies(count, agencies, agency['id'], sub_agencies, total)
               if len(sub_agencies) > 0:
                   locally_funded.append({'sub_agencies' : sub_agencies})
                   count += 1
        total += balance
        '''

        if balance > 0:
            agencies_allocation.append({
                'no'     : count,
                'agency' : agency['name'],
                'amount' : balance
            })
            count+=1
        total += balance


    data['agencies']  = agencies_allocation
    data['str_month'] = stringify_month(data['month'])
    data['total'] = total
    return render_to_response('./admin/smca.html', data, context)


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

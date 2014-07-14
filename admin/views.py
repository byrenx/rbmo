from django.shortcuts import render, render_to_response, redirect, RequestContext
from django.db import transaction, connection
from django.db.models import Sum, Avg
from django.http import  HttpResponseRedirect, HttpResponse
from django.conf import settings
from django.conf.urls.static import static
from .forms import (UserForm, LoginForm, AgencyForm, MonthForm)
from rbmo.models import (UserGroup,
                         Groups,
                         Agency,
                         WFPSubmission,
                         MPFRO, 
                         MPFRSubmission,
                         QuarterlyReq,
                         QuarterReqSubmission,
                         AllotmentReleases,
                         WFPData,
                         COSSubmission
)
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required, permission_required
from helpers.helpers import *
from fund.views import isMRS, is_allQRS, lqm
from datetime import datetime, date
from decimal import *
import time
import sys

# Create your views here.
SYSTEM_NAME = 'RBMO Management System'
months = ['jan', 'feb', 'mar', 'apr', 'may', 'jun',
          'jul', 'aug', 'sept', 'oct', 'nov', 'dec' ]


@login_required(login_url='/admin/')
def submitCOS(request):#submit Contract of Service
    submit = request.POST.get('cos_submit')
    agency_id = request.POST.get('agency_id')
    if submit is not None and agency_id is not None:
        today = datetime.today()
        agency = Agency.objects.get(id=agency_id)
        cos_submit = COSSubmission(agency=agency, date_submitted=today)
        cos_submit.save()
    return HttpResponseRedirect('/admin/manage_agency_docs?agency_id='+str(agency.id)+'&year='+str(today.year))

 
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
    data = {'page': 'users',
            'system_name': SYSTEM_NAME
        }
    data['allowed_tabs'] = get_allowed_tabs(request.user.id)
    data['year'] = time.strftime('%Y')
    
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
    if not has_permission(request.user.id, 'add', 'user'):
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
        return render_to_response('./admin/user_form.html', data, context)


@login_required(login_url='/admin/')
def agencies(request):
    context = RequestContext(request)
    data = {'page': 'agencies',
            'system_name': SYSTEM_NAME
    }
    data['allowed_tabs'] = get_allowed_tabs(request.user.id)

    if has_permission(request.user.id, 'add', 'agency'):
        data['has_add'] = 'true'

    if request.method=='POST':
        pass
    else:
        data['agencies'] = Agency.objects.all()
        return render_to_response('./admin/agencies.html', data, context)


@login_required(login_url='/admin/')
def addEditAgency(request):
    context = RequestContext(request)
    data = {'form': AgencyForm(),
            'mode': request.GET.get('mode', 'add'),
            'system_name': SYSTEM_NAME
    }
    if not has_permission(request.user.id, 'add', 'agency'):
        return HttpResponseRedirect('/admin')

    data['allowed_tabs'] = get_allowed_tabs(request.user.id)

    if request.method == 'POST':
        action = request.POST.get('action', 'add')
        agency_frm = AgencyForm(request.POST)
        if action=='add' and agency_frm.is_valid():
            addAgency(agency_frm)
            data['s_msg'] = 'New Agency/Office was succesfully added.'
            return render_to_response('./admin/agency_form.html', data, context)
        elif action=='edit' and agency_frm.is_valid():
            pass
        else:
            data['frm_errors'] = agency_frm.errors
            data['form'] = agency_frm
            return render_to_response('./admin/agency_form.html', data, context)
    else:
        return render_to_response('./admin/agency_form.html', data, context)

@login_required(login_url='/admin/')
def agencyMainPage(request):
    context = RequestContext(request)
    cursor  = connection.cursor()
    data = {'agency_id'  : request.GET.get('agency_id'),
            'system_name': SYSTEM_NAME
    }
    data['allowed_tabs'] = get_allowed_tabs(request.user.id)
    try:
        agency = Agency.objects.get(id=data['agency_id'])
        data['agency'] = agency
        return render_to_response('./admin/agency_main_page.html', data, context)
    except Agency.DoesNotExist:
        return render_to_response('./admin/agency_main_page.html', data, context)


@login_required(login_url = '/admin/')
@transaction.atomic
def manageAgencyDocs(request):
    context = RequestContext(request)
    data = {'system_name': SYSTEM_NAME,
            'agency_id'  : request.GET.get('agency_id'),
            'agency_tab' : 'reqs',
            'year'       : request.GET.get('year', time.strftime('%Y'))
    }
    data['allowed_tabs'] = get_allowed_tabs(request.user.id)

    try:
        current_year = datetime.today().year
        years = []
        while current_year>=2013:
            years.append(current_year)
            current_year-=1
        data['years'] = years
        #get the agency
        agency = Agency.objects.get(id=data['agency_id'])
        data['agency'] = agency
        #year
        data['monthly'] = getAgencyMonthlyReq(data['year'], agency)
        data['quarterly'] = QuarterlyReq.objects.all()
        data['wfp_submit'] =  getWfpSubmission(data['year'], agency)       
        data['q1_req_s'] = getSumittedQReq(data['year'], agency, 1) #1st quarter submitted requirements
        data['q2_req_s'] = getSumittedQReq(data['year'], agency, 2) #2nd quarter submitted requirements
        data['q3_req_s'] = getSumittedQReq(data['year'], agency, 3) #3rd quarter submitted requirements
        data['q4_req_s'] = getSumittedQReq(data['year'], agency, 4) #4th quarter submitted requirements
        #get submitted contract of service
        data['cos_submitted'] = COSSubmission.objects.filter(date_submitted__year=data['year'], agency=agency)
        return render_to_response('./admin/agency_docs_recording.html', data, context)
    except Agency.DoesNotExist:
        return render_to_response('./admin/agency_docs_recording.html', data, context)  

def getSumittedQReq(year, agency, quarter):
    quarter_req_submitted = QuarterReqSubmission.objects.filter(year=year, agency=agency, quarter=quarter)
    quarter_submitted = []
    for qrs in quarter_req_submitted:
        quarter_submitted.append(qrs.requirement.id)
    return quarter_submitted


def getWfpSubmission(year, agency):
    try:
        wfp_submit = WFPSubmission.objects.get(year=year, agency=agency)
        return wfp_submit
    except WFPSubmission.DoesNotExist:
        return None    

@login_required(login_url='/admin/')
def submitMPFR(request):
    agency_id = request.POST.get('agency_id')
    year = request.POST.get('year')
    agency = Agency.objects.get(id=agency_id)
    #monthly physical and financial report

    try:
        monthlyReq = MPFRSubmission.objects.get(year=year, agency=agency)
    except MPFRSubmission.DoesNotExist:
        monthlyReq = MPFRSubmission(year = year,
                                    agency = agency
        )
        
    months = request.POST.getlist('month[]')
    for month in months:
        if month == '1':
            monthlyReq.jan = datetime.now()
        elif month == '2':
            monthlyReq.feb = datetime.now()
        elif month == '3':
            monthlyReq.mar = datetime.now()
        elif month == '4':
            monthlyReq.apr = datetime.now()
        elif month == '5':
            monthlyReq.may = datetime.now()
        elif month == '6':
            monthlyReq.jun = datetime.now()
        elif month == '7':
            monthlyReq.jul = datetime.now()
        elif month == '8':
            monthlyReq.aug = datetime.now()
        elif month == '9':
            monthlyReq.sept = datetime.now()
        elif month == '10':
            monthlyReq.oct = datetime.now()
        elif month == '11':
            monthlyReq.nov = datetime.now()
        else:
            monthlyReq.dec = datetime.now()
        monthlyReq.save()
    return HttpResponseRedirect('/admin/manage_agency_docs?agency_id='+str(agency.id))

@login_required(login_url='/admin/')
def submitWFPReq(request):
    if request.method == 'POST':
        year = request.POST.get('year')
        agency_id = request.POST.get('agency_id')
        wfp_submit = request.POST.get('wfp_submit', '0')
        if wfp_submit == '1':
            #submit
            wfp = WFPSubmission(date_submitted=datetime.now(),
                                year = year,
                                agency = Agency.objects.get(id=agency_id)
            )
            wfp.save()
            return HttpResponseRedirect('/admin/manage_agency_docs?agency_id='+str(agency_id))

def getAgencyMonthlyReq(year, agency):
    try:
        mpfr = MPFRSubmission.objects.get(year=year, agency=agency)
        return mpfr
    except MPFRSubmission.DoesNotExist:
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
def addAgency(agency_frm):
    agency = Agency(name = agency_frm.cleaned_data['name'],
                    email = agency_frm.cleaned_data['email'],
                    sector = agency_frm.cleaned_data['sector']
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


def mpfro(request):
    context = RequestContext(request)
    data  = {'system_name' : SYSTEM_NAME,
             'agency_id'   : request.GET.get('agency_id'),
             'year'        : request.GET.get('year', time.strftime('%Y')),
             'month'       : request.GET.get('month', time.strftime('%M')),
    }
    try:
        agency = Agency.objects.get(id=data['agency_id'])
        data['agency'] = agency
        mpfro = MPFRO.objects.filter(agency=agency, year=data['year'], month=data['month'])
        return render_to_response('./admin/monthly_reps.html', data, context)
    except Agency.DoesNotExist:
        pass


def mpfro_form(request):
    context = RequestContext(request)
    data = {'system_name': SYSTEM_NAME,
            'agency_id'  : request.GET.get('agency_id')
            
        }
    if request.method=='POST':
        return HttpResponse('sas')
    else:
        try:
            agency = Agency.objects.get(id=data['agency_id'])
            data['agency'] = agency
            data['year'] = time.strftime('%Y')
            return render_to_response('./admin/mpfro_form.html', data, context)
        except Agency.DoesNotExist:
            return HttpResponse('none')


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
                                              date_submitted = datetime.now()
                                          )
        quarter_submit.save()

    return HttpResponseRedirect('/admin/manage_agency_docs?agency_id='+str(agency.id)+'&year='+str(year))


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

# def yearly_fund_home(request):
#     data = {
#             'system_name'  : SYSTEM_NAME,
#             'allowed_tabs' : get_allowed_tabs(request.user.id)}

#     year = datetime.year
#     i = 2005
#     year_list = []
#     while i <= year:
#         year_list.append(i)
#         i = i + 1
#     for x in year_list:
#         print x, 'Month'
#     data['year_choices'] = year_list
#     return render(request,'./admin/yearly_fund.html', data)

def yearly_fund(request):
    data = {
            'system_name'  : SYSTEM_NAME,
            'allowed_tabs' : get_allowed_tabs(request.user.id)}
    year = date.today().year 
    i = 2010
    year_list = []
    while year >= i :
        year_list.append(year)
        year = year - 1
    data['year_choices'] = year_list
    if request.method == 'GET':
        allocate=request.GET.get('allocate')
        year_choose = request.GET.get('year_choose')
        cursor = connection.cursor()
            
        if allocate == 'all':
            data['allocate_name'] = 'PS, MOOE, and CO'
            ps_query = '''
            SELECT sum(jan) as 'jan', sum(feb) as 'feb', sum(mar) as 'mar',
                sum(apr) as 'apr', sum(may) as 'may', sum(jun) as 'jun', sum(jul) as 'jul',
                sum(aug) as 'aug', sum(sept) as 'sept', sum(oct) as 'oct', sum(nov) as 'nov',
                sum(`dec`) as 'dec' FROM wfp_data
            where year=%s;
            '''
            month=['January','February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
            result =[]
            cursor.execute(ps_query,[year_choose])
            ps_month = cursor.fetchone()
            for i in range(1, 13):
                release = AllotmentReleases.objects.filter(month=i, year=year_choose).aggregate(Sum('amount_release'))
           
                result.append({'month':month[i-1], 'amount':ps_month[i-1],'release':numify(release['amount_release__sum']),'balance':ps_month[i-1]-numify(release['amount_release__sum'])})
            
            data['result'] = result
        elif allocate == 'CO' or allocate == 'MOOE' or allocate == 'PS':   
            if allocate == 'CO':
                data['allocate_name'] = 'CO'
            elif allocate == 'MOOE':
                data['allocate_name'] = 'MOOE'
            elif allocate == 'PS':
                data['allocate_name'] = 'PS'
            ps_query = '''
            SELECT sum(jan) as 'jan', sum(feb) as 'feb', sum(mar) as 'mar',
                sum(apr) as 'apr', sum(may) as 'may', sum(jun) as 'jun', sum(jul) as 'jul',
                sum(aug) as 'aug', sum(sept) as 'sept', sum(oct) as 'oct', sum(nov) as 'nov',
                sum(`dec`) as 'dec' FROM wfp_data
            where allocation = %s and year=%s;
            '''
            month=['January','February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
            result =[]
            cursor.execute(ps_query,[allocate,year_choose])
            ps_month = cursor.fetchone()
            for i in range(1, 13):
                release = AllotmentReleases.objects.filter(allocation=allocate, month=i, year=year_choose).aggregate(Sum('amount_release'))
           
                result.append({'month':month[i-1], 'amount':ps_month[i-1],'release':numify(release['amount_release__sum']),'balance':ps_month[i-1]-numify(release['amount_release__sum'])})
            
            data['result'] = result

    return render(request,'./admin/yearly_fund.html', data)  


def fundDistribution(request):
    cursor  = connection.cursor()
    context = RequestContext(request)
    data  = {'system_name' : SYSTEM_NAME,
             'allowed_tabs' : get_allowed_tabs(request.user.id)
    }

    year  = time.strftime('%Y') 
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
    data = {'system_name' : SYSTEM_NAME,
            'year'        : year,
            'allocation'  : allocation,
            'years'       : dictfetchall(cursor),
            'allowed_tabs' : get_allowed_tabs(request.user.id)
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
        for i in range(1, 13):
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
        if monthly and quarterly:
            agency_list.append({'count' : count,
                                'name'  : agency.name})
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

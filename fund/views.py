from django.shortcuts import render, render_to_response, redirect, RequestContext
from django.db import transaction, connection
from django.db.models import Sum, Avg
from django.http import  HttpResponseRedirect, HttpResponse
from django.conf import settings
from django.conf.urls.static import static
from .forms import *
from rbmo.models import (Agency, 
WFPData,
MonthlyReqSubmitted,
QuarterlyReq,
QuarterReqSubmission,
AllotmentReleases,
COSSubmission
)
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required, permission_required
from helpers.helpers import *
from datetime import datetime, date
import time

# Create your views here.
SYSTEM_NAME = 'RBMO Management System'
MONTHS = ['jan', 'feb', 'mar', 'apr', 'may', 'jun',
          'jul', 'aug', 'sept', 'oct', 'nov', 'dec' ]

@login_required(login_url='/admin/')
@transaction.atomic
def allotmentReleases(request):
    context       = RequestContext(request)
    allotments    = {}
    total_release = 0
    total_PS      = 0
    total_MOOE    = 0
    total_CO      = 0
    year = datetime.today().year
    
    try:
        agency                  = Agency.objects.get(id=request.GET.get('agency_id'))
        wfp_data_PS             = WFPData.objects.filter(agency=agency, year=year, allocation='PS').aggregate(total_sum = Sum('total'))
        wfp_data_MOOE           = WFPData.objects.filter(agency=agency, year=year, allocation='MOOE').aggregate(total_sum = Sum('total'))
        wfp_data_CO             = WFPData.objects.filter(agency=agency, year=year, allocation='CO').aggregate(total_sum = Sum('total'))
        allotment_releases      = AllotmentReleases.objects.filter(agency=agency).order_by('year', 'month')
        remaining_balance       = numify(wfp_data_PS['total_sum']) + numify(wfp_data_MOOE['total_sum']) + numify(wfp_data_CO['total_sum'])
        total_remaining_balance = remaining_balance
        
        for allotment_release in allotment_releases:
            if allotment_release.allocation == 'PS':
                total_PS = total_PS + allotment_release.amount_release
            elif allotment_release.allocation == 'MOOE':
                total_MOOE = total_MOOE + allotment_release.amount_release
            else:
                total_CO = total_CO + allotment_release.amount_release
                
            total_release                    = total_release + allotment_release.amount_release
            total_remaining_balance          = total_remaining_balance - allotment_release.amount_release
            allotments[allotment_release.id] =  {
                'date_release'      : allotment_release.date_release,
                'ada_no'            : allotment_release.ada_no,
                'particulars'       : stringify_month(allotment_release.month),
                'total_release'     : total_release,
                'remaining_balance' : total_remaining_balance,
                'allocation'        : {
                'name'              : allotment_release.allocation,
                'amount_release'    : allotment_release.amount_release,
                },
            }
        
        total_PS_balance   = numify(wfp_data_PS['total_sum']) - total_PS
        total_MOOE_balance = numify(wfp_data_MOOE['total_sum']) - total_MOOE
        total_CO_balance   = numify(wfp_data_CO['total_sum']) - total_CO
        
        data = {
            'system_name'             : SYSTEM_NAME,
            'agency'                  : agency,
            'allotments'              : allotments,
            'wfp_data_PS'             : wfp_data_PS,
            'wfp_data_MOOE'           : wfp_data_MOOE,   
            'wfp_data_CO'             : wfp_data_CO,
            'remaining_balance'       : remaining_balance,
            'total_remaining_balance' : total_remaining_balance,
            'total_release'           : total_release,
            'total_PS'                : total_PS,
            'total_MOOE'              : total_MOOE,
            'total_CO'                : total_CO,
            'total_PS_balance'        : total_PS_balance,
            'total_MOOE_balance'      : total_MOOE_balance,
            'total_CO_balance'        : total_CO_balance,
            'allowed_tabs'            : get_allowed_tabs(request.user.id),
            'cur_date'                : date.today(),
            'year'                    : year
        }

        #get releases
        return render_to_response('./fund/allotment_releases.html', data, context)
    except Agency.DoesNotExist:
        return HttpResponseRedirect('/admin/agencies')


@login_required(login_url='/admin/')
@transaction.atomic
def monthlyAlloc(request):
    context = RequestContext(request)
    data = {'system_name' : SYSTEM_NAME,
            'c_year'      : time.strftime('%Y'),
            'allowed_tabs': get_allowed_tabs(request.user.id),
            'cur_date'    : time.strftime('%B %d, %Y')
    }

    unsubmitted_reqs = []
    agency_id = None
    year = datetime.today().year
    month = datetime.today().month
    allocation = 'MOOE'
        
    if request.method == 'POST':
        agency_id = request.POST.get('agency_id')
        allocation = request.POST.get('allocation')
        year = int(request.POST.get('year'))
        month = int(request.POST.get('month'))
    else: #no post request sent
        #gather default data to display
        agency_id = request.GET.get('agency_id')

    try:
        agency = Agency.objects.get(id=agency_id)
        monthly_alloc_stat = {}
        
        if allocation == 'PS':
            data['amount'] = gettotalAllocation(year, month, agency, 'PS')
            has_cos = hasCOSSubmitted(agency, year)
            if has_cos==False:
                monthly_alloc_stat['stat'] = 'PENDING'
                unsubmitted_reqs.append({'name': 'Contract of Service'})
            elif data['amount'] > 0:
                monthly_alloc_stat['stat'] = 'PROCESSED'
            else:
                monthly_alloc_stat['stat'] = 'NO ALLOCATED FUND'
        elif allocation == 'MOOE':
            unsubmitted_reqs = lqm(year, month, agency)
            data['amount'] = gettotalAllocation(year, month, agency, 'MOOE')
            if len(unsubmitted_reqs)==0 and isMRS(year, month, agency) and data['amount']>0:
                monthly_alloc_stat['stat'] = 'PROCESSED'
            elif data['amount']==0:
                monthly_alloc_stat['stat'] = 'NO ALLOCATED FUND'
            else:
                if isMRS(year, month, agency)==False:
                    unsubmitted_reqs.append({'name':'Monthly Physical and Financial Report'})
                monthly_alloc_stat['stat'] = 'PENDING'
                monthly_alloc_stat['quarter_reqs'] = unsubmitted_reqs

        else: #CO
            data['amount'] = gettotalAllocation(year, month, agency, 'CO')
            if data['amount'] > 0:
                monthly_alloc_stat['stat'] = 'PROCESSED'
            else:
                monthly_alloc_stat['stat'] = 'NO ALLOCATED FUND'
        
                
        if alreadyRelease(year, month, agency, allocation) and data['amount']-getReleaseAmount(year, month, agency, allocation)<=0:
            monthly_alloc_stat['stat'] = 'RELEASED' 
            data['monthly_alloc_stat'] = monthly_alloc_stat

        data['agency'] = agency
        data['allocation'] = allocation
        data['form']   = MCASearchForm({'month': month, 'allocation' : allocation})
        data['year'] = year
        data['month_str'] = stringify_month(month)
        data['amount'] = numify(data['amount'])-numify(getReleaseAmount(year, month, agency, allocation))
        data['monthly_alloc_stat'] = monthly_alloc_stat
        
        return render_to_response('./fund/monthly_allocation.html', data, context)
    except Agency.DoesNotExist:
        return HttpResponseRedirect('/admin/agencies')
        
    """
    if request.method=='POST':
        allocation = request.POST.get('allocation')
        monthly_alloc_stat = {}
        agency = Agency.objects.get(id=request.POST.get('agency_id'))
        data['agency'] = agency
        year = int(request.POST.get('year'))
        month = int(request.POST.get('month'))
        data['month_str'] = stringify_month(month)
        data['year'] = year

        
        data['form']   = MCASearchForm({'month': month, 'allocation' : allocation})
        
        if allocation == 'PS':
            data['amount'] = gettotalAllocation(year, month, agency, 'PS')
            has_cos = hasCOSSubmitted(agency, year)
            if has_cos==False:
                monthly_alloc_stat['stat'] = 'PENDING'
                unsubmitted_reqs.append({'name': 'Contract of Service'})
            elif data['amount'] > 0:
                monthly_alloc_stat['stat'] = 'PROCESSED'
            else:
                monthly_alloc_stat['stat'] = 'NO ALLOCATED FUND'
        elif allocation == 'MOOE':
            unsubmitted_reqs = lqm(year, month, agency)
            data['amount'] = gettotalAllocation(year, month, agency, 'MOOE')
            if len(unsubmitted_reqs)==0 and isMRS(year, month, agency) and data['amount']>0:
                monthly_alloc_stat['stat'] = 'PROCESSED'
            elif data['amount']==0:
                monthly_alloc_stat['stat'] = 'NO ALLOCATED FUND'
            else:
                if isMRS(year, month, agency)==False:
                    unsubmitted_reqs.append({'name':'Monthly Physical and Financial Report'})
                monthly_alloc_stat['stat'] = 'PENDING'
                monthly_alloc_stat['quarter_reqs'] = unsubmitted_reqs

        else: #CO
            data['amount'] = gettotalAllocation(year, month, agency, 'CO')
            if data['amount'] > 0:
                monthly_alloc_stat['stat'] = 'PROCESSED'
            else:
                monthly_alloc_stat['stat'] = 'NO ALLOCATED FUND'
        
                
        if alreadyRelease(year, month, agency, allocation) and data['amount']-getReleaseAmount(year, month, agency, allocation)<=0:
            monthly_alloc_stat['stat'] = 'RELEASED' 
            data['monthly_alloc_stat'] = monthly_alloc_stat
        data['amount'] = numify(data['amount'])-numify(getReleaseAmount(year, month, agency, allocation))
        data['monthly_alloc_stat'] = monthly_alloc_stat
        data['allocation'] = allocation
        return render_to_response('./fund/monthly_allocation.html', data, context)
    else: # if no post request was submitted
        try:
            agency = Agency.objects.get(id=request.GET.get('agency_id'))
            data['agency'] = agency
            data['form']   = MCASearchForm({'month': datetime.today().month, 'allocation' : 'MOOE'})
            return render_to_response('./fund/monthly_allocation.html', data, context)
        except Agency.DoesNotExist:
            return HttpResponseRedirect('/admin/agencies')
    """

def hasCOSSubmitted(agency, year):
    try:
        cos_submit = COSSubmission.objects.filter(date_submitted__year=year)
        return True
    except COSSubmission.DoesnNotExist:
        return False

def gettotalAllocation(year, month, agency, allocation):
    try:
        if month == 1:
            budget = WFPData.objects.filter(year=year, agency=agency, allocation=allocation).aggregate(Sum('jan'))
            return numify(budget['jan__sum'])
            
        elif month == 2:
            budget = WFPData.objects.filter(year=year, agency=agency, allocation=allocation).aggregate(Sum('feb'))
            return numify(budget['feb__sum'])
        elif month == 3:            
            budget = WFPData.objects.filter(year=year, agency=agency, allocation=allocation).aggregate(Sum('mar'))
            return numify(budget['mar__sum'])

        elif month == 4:
            budget = WFPData.objects.filter(year=year, agency=agency, allocation=allocation).aggregate(Sum('apr'))
            return numify(budget['apr__sum'])

        elif month == 5:
            budget = WFPData.objects.filter(year=year, agency=agency, allocation=allocation).aggregate(Sum('may'))
            return numify(budget['may__sum'])

        elif month == 6:
            budget = WFPData.objects.filter(year=year, agency=agency, allocation=allocation).aggregate(Sum('jun'))
            return numify(budget['jun__sum'])

        elif month == 7:
            budget = WFPData.objects.filter(year=year, agency=agency, allocation=allocation).aggregate(Sum('jul'))
            return numify(budget['jul__sum'])

        elif month == 8:
            budget = WFPData.objects.filter(year=year, agency=agency, allocation=allocation).aggregate(Sum('aug'))
            return numify(budget['aug__sum'])

        elif month == 9:
            budget = WFPData.objects.filter(year=year, agency=agency, allocation=allocation).aggregate(Sum('sept'))
            return numify(budget['sept__sum'])

        elif month == 10:
            budget = WFPData.objects.filter(year=year, agency=agency, allocation=allocation).aggregate(Sum('oct'))
            return numify(budget['oct__sum'])

        elif month == 11:
            budget = WFPData.objects.filter(year=year, agency=agency, allocation=allocation).aggregate(Sum('nov'))
            return numify(budget['nov__sum'])

        elif month == 12:
            budget = WFPData.objects.filter(year=year, agency=agency, allocation=allocation).aggregate(Sum('dec'))
            return numify(budget['dec__sum'])

    except WFPData.DoesNotExist:
        return 0

def getYearsMOOEAlloc(agency):
    cursor = connection.cursor()
    query = '''
            select distinct(year) from wfp_data 
            where agency_id=%s and allocation=%s
            '''
    cursor.execute(query, [agency.id, 'MOOE'])
    return dictfetchall(cursor)
        
def alreadyRelease(year, month, agency, allocation):
    try:
        release = AllotmentReleases.objects.get(year=year, month=month, agency=agency, allocation=allocation)
        return True
    except AllotmentReleases.DoesNotExist:
        return False

def getReleaseAmount(year, month, agency, allocation):
    try:
        allotment_release = AllotmentReleases.objects.filter(year=year, month=month, agency=agency, allocation=allocation).aggregate(Sum('amount_release'))
        return allotment_release['amount_release__sum']
    except AllotmentReleases.DoesNotExist:
        return 0

def lqm(year, month, agency): #querying for lacking quarterly requirements
    cursor = connection.cursor()
    #quarterly
    query = '''
    select * from quarterly_req 
    where id not in 
    (select requirement_id from quarter_req_submitted where year=%s and quarter=%s and agency_id=%s)
    '''
    if month<=3:
        cursor.execute(query, [year-1, 4, agency.id])
        return dictfetchall(cursor)
    elif month>3 and month<=6:
        cursor.execute(query, [year, 1, agency.id])
        return dictfetchall(cursor)
    elif month>6 and month<=9:
        cursor.execute(query, [year, 2, agency.id])
        return dictfetchall(cursor)
    elif month>9 and month<=12:
        cursor.execute(query, [year, 3, agency.id])
        return dictfetchall(cursor)
    else:
        return [{'name': month}]
        

def isMRS(year, month, agency):#is requisite month report was submitted
    try:
        if month==1:
            monthly_req_submit = MonthlyReqSubmitted.objects.get(year=year-1, month=12, agency=agency)
        else:
            monthly_req_submit = MonthlyReqSubmitted.objects.get(year=year, month=month-1, agency=agency)
        return True
    except MonthlyReqSubmitted.DoesNotExist:
        return False


def is_allQRS(year, month, agency): # is all quarter requirement submitted    
    cursor = connection.cursor()
    q_reqs = QuarterlyReq.objects.all().count() #count of all quarterly reqs
    q_req_subs = 0
    qrs_query = '''select count(distinct(requirement_id)) as count
    from quarter_req_submitted where quarter=%s and agency_id=%s
    and year=%s
    '''
    
    if month<=3:
        cursor.execute(qrs_query, [year-1, 4, agency.id])
        qrs_count = numify(cursor.fetchone()[0])
        return (q_reqs-qrs_count == 0)
    elif month>3 and month<=6:
        cursor.execute(qrs_query, [year, 1, agency.id])
        qrs_count = numify(cursor.fetchone()[0])
        return (q_reqs-qrs_count == 0)
    elif month>6 and month<=9:
        cursor.execute(qrs_query, [year, 2, agency.id])
        qrs_count = numify(cursor.fetchone()[0])
        return (q_reqs-qrs_count == 0)
    elif month>9 and month<=12:
        cursor.execute(qrs_query, [year, 3, agency.id])
        qrs_count = numify(cursor.fetchone()[0])
        return (q_reqs-qrs_count == 0)

@login_required(login_url='/admin/')
def fundReleaseForm(request):

    context = RequestContext(request)

    data = {'system_name' : SYSTEM_NAME,
            'agency_id'   : request.GET.get('agency_id'),
            'year'        : time.strftime('%Y'),
            'agency_tab'  : 'fund_rel',
            'allowed_tabs': get_allowed_tabs(request.user.id)
    }


    release_form = AllotmentReleaseForm({'month': datetime.today().month})
    data['form'] = release_form
    if request.method == 'POST':
        allot_release_form = AllotmentReleaseForm(request.POST)

        if allot_release_form.is_valid():
            allot_release = AllotmentReleases(
                ada_no = allot_release_form.cleaned_data['ada'],
                agency = Agency.objects.get(id=request.POST.get('agency_id')),
                allocation = request.POST.get('allocation'),
                month = allot_release_form.cleaned_data['month'],
                year = request.POST.get('year'),
                date_release = datetime.today(),
                amount_release = allot_release_form.cleaned_data['amount']
            )
            
            budget = gettotalAllocation(int(allot_release.year), int(allot_release.month), allot_release.agency, allot_release.allocation)
            #getRelease
            release = getReleaseAmount(int(allot_release.year), int(allot_release.month), allot_release.agency, allot_release.allocation)
            balance = numify(budget)-numify(release)
            if budget==0:
                data['e_msg'] = 'No Alloted amount for %s - %s' %(stringify_month(int(allot_release.month)), allot_release.allocation)
            elif balance <=0 :
                data['e_msg'] = 'No Remaining Balance for %s - %s Allocation. The full amount already released' %(stringify_month(int(allot_release.month)), allot_release.allocation)
            elif allot_release.amount_release<=0:
                data['e_msg'] = 'Please Enter a valid amount'
            elif allot_release.amount_release>balance:
                data['e_msg'] = 'The amount you enter an amount that does not exceeds the allotment balance' %(stringify_month(int(allot_release.month)), allot_release.allocation)
            else:
                allot_release.save()
                data['s_msg'] = 'Fund Release was succesfully saved'

            data['agency'] = allot_release.agency
            return render_to_response('./fund/fund_release_form.html', data, context)
        else:
            data['errors'] = fund_release_form.errors
            return render_to_response('./fund/fund_release_form.html', data, context)
            
    elif data['agency_id'] is None:
        return HttpResponseRedirect('/admin/agencies')
    else:
        agency = Agency.objects.get(id=data['agency_id'])
        data['agency'] = agency
        return render_to_response('./fund/fund_release_form.html', data, context)   

@login_required(login_url='/admin/')
@transaction.atomic
def agenciesBudgetSummary(request):
    context = RequestContext(request)
    cursor = connection.cursor()
    data = {'year'         : request.GET.get('year', time.strftime('%Y')),
            'system_name'  : SYSTEM_NAME,
            'allowed_tabs' :get_allowed_tabs(request.user.id)
        }

    balances = []
    agencies = Agency.objects.all()
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
        ps = getBudget(agency.id, 'PS', data['year'])
        mooe = getBudget(agency.id, 'MOOE', data['year'])
        co = getBudget(agency.id, 'CO', data['year']) 
        agency_balances['budget'] = ps + mooe + co
        '''
        total release
        '''
        ps = getRelease(agency, 'PS', data['year'])
        mooe = getRelease(agency, 'MOOE', data['year'])
        co = getRelease(agency, 'CO', data['year'])
        agency_balances['release'] = ps + mooe + co 
        #remaining balance
        agency_balances['balance'] = agency_balances['budget'] - agency_balances['release']
        balances.append(agency_balances)
        total_budget  += agency_balances['budget']
        total_release += agency_balances['release']
        total_balance += agency_balances['balance']

    years_query = "select distinct(year) as year from wfp_data"
    cursor.execute(years_query)
    data['years'] = dictfetchall(cursor)
    data['balances'] = balances
    data['total_sum'] = {'total_budget'  : total_budget,
                         'total_release' : total_release,
                         'total_balance' : total_balance
    }
    data['today'] = date.today()
    return render_to_response('./fund/running_balances.html', data, context)

def getBudget(agency, allocation, year):
    cursor=connection.cursor()
    #total allocation query

    budget = WFPData.objects.filter(agency=agency, year=year, allocation=allocation).aggregate(Sum('total'))
    return numify(budget['total__sum'])
    

def getRelease(agency, allocation, year):
    release = AllotmentReleases.objects.filter(year=year, allocation=allocation, agency=agency).aggregate(Sum('amount_release'))
    return numify(release['amount_release__sum'])
    
    
def getFundStatus(request):
    context = RequestContext(request)
    cursor = connection.cursor()
    releases_query ='''
    select sum(amount) from fund_releases 
    where budgetallocation_id in (select id from budget_allocation where agency_id=%s and year=%s and allocation_id=(select id from allocation where name=%s)) 
    '''
 
    data = {'agency_id' : request.GET.get('agency_id'),
            'year' : request.GET.get('year', time.strftime('%Y'))
    }
    agency = Agency.objects.get(id=data['agency_id'])
    data['agency'] = agency
    # PS
    total_ps = BudgetAllocation.objects.filter(agency=agency, year=data['year'], allocation__name='PS').aggregate(Sum('total'))
    data['total_ps'] = numify(total_ps['total__sum'])
    #MOOE
    total_mooe = BudgetAllocation.objects.filter(agency=agency, year=data['year'], allocation__name='MOOE').aggregate(Sum('total'))
    data['total_mooe'] = numify(total_mooe['total__sum'])
    #CO
    total_co = BudgetAllocation.objects.filter(agency=agency, year=data['year'], allocation__name='CO').aggregate(Sum('total'))
    data['total_co'] = numify(total_co['total__sum'])
    #PS release and balance
    cursor.execute(releases_query, [data['agency_id'], data['year'], 'PS'])
    data['total_ps_release'] = numify(cursor.fetchone()[0])
    data['bal_ps'] = data['total_ps'] - data['total_ps_release']
    #PS release and balance
    cursor.execute(releases_query, [data['agency_id'], data['year'], 'MOOE'])
    data['total_mooe_release'] = numify(cursor.fetchone()[0])
    data['bal_mooe'] = data['total_mooe'] - data['total_mooe_release']
    #PS release and balance
    cursor.execute(releases_query, [data['agency_id'], data['year'], 'CO'])
    data['total_co_release'] = numify(cursor.fetchone()[0])
    data['bal_co'] = data['total_co'] - data['total_co_release']
    
    return render_to_response('./fund/status_of_funds.html', data, context)

def getAllocatedBudget(request):
    cursor = connection.cursor()
    data = {'agency_id'  : request.GET.get('agency_id'),
            'allocation' : Allocation.objects.get(id=request.GET.get('allocation')),
            'month' : request.GET.get('month'),
            'year'  : request.GET.get('year')
    }

    agency = Agency.objects.get(id=data['agency_id'])
    amount = 0
    balance = 0
    allowed = 'no'
    if data['month'] == '1':
        budget = WFPData.objects.filter(allocation=data['allocation'], year=data['year'], agency=agency).aggregate(Sum('jan'))
        amount = numify(budget['jan__sum'])
    elif data['month'] == '2':
        budget = WFPData.objects.filter(allocation=data['allocation'], year=data['year'], agency=agency).aggregate(Sum('feb'))
        amount = numify(budget['feb__sum'])
    elif data['month'] == '3':
        budget = WFPData.objects.filter(allocation=data['allocation'], year=data['year'], agency=agency).aggregate(Sum('mar'))
        amount = numify(budget['mar__sum'])
    elif data['month'] == '4':
        budget = WFPData.objects.filter(allocation=data['allocation'], year=data['year'], agency=agency).aggregate(Sum('apr'))
        amount = numify(budget['apr__sum'])
    elif data['month'] == '5':
        budget = WFPData.objects.filter(allocation=data['allocation'], year=data['year'], agency=agency).aggregate(Sum('may'))
        amount = numify(budget['may__sum'])
    elif data['month'] == '6':
        budget = WFPData.objects.filter(allocation=data['allocation'], year=data['year'], agency=agency).aggregate(Sum('jun'))
        amount = numify(budget['jun__sum'])
    elif data['month'] == '7':
        budget = WFPData.objects.filter(allocation=data['allocation'], year=data['year'], agency=agency).aggregate(Sum('jul'))
        amount = numify(budget['jul__sum'])
    elif data['month'] == '8':
        budget = WFPData.objects.filter(allocation=data['allocation'], year=data['year'], agency=agency).aggregate(Sum('aug'))
        amount = numify(budget['aug__sum'])
    elif data['month'] == '9':
        budget = WFPData.objects.filter(allocation=data['allocation'], year=data['year'], agency=agency).aggregate(Sum('sept'))
        amount = numify(budget['sept__sum'])
    elif data['month'] == '10':
        budget = WFPData.objects.filter(allocation=data['allocation'], year=data['year'], agency=agency).aggregate(Sum('oct'))
        amount = numify(budget['oct__sum'])
    elif data['month'] == '11':
        budget = WFPData.objects.filter(allocation=data['allocation'], year=data['year'], agency=agency).aggregate(Sum('nov'))
        amount = numify(budget['nov__sum'])
    elif data['month'] == '12':
        budget = WFPData.objects.filter(allocation=data['allocation'], year=data['year'], agency=agency).aggregate(Sum('dec'))
        amount = numify(budget['dec__sum'])

    if isAllowedForRelease(data['month'], agency, data['year']):
        allowed = 'yes'
    else:
        allowed = 'no'
    release = FundReleaseUtilize.objects.filter(agency=agency, year=data['year'], month=data['month'],  
                                                allocation=data['allocation']).aggregate(Sum('amount_release'))
    balance = numify(amount) - numify(release['amount_release__sum'])
    response = '{"amount": "%s", "balance": "%s", "allowed": "%s"}' %(amount, balance, allowed)

    return HttpResponse(response)

def isAllowedForRelease(month, agency, year):
    if month=='1':
        return True
    else:
        try:
            mpfr = MPFRSubmission.objects.get(year=year, agency=agency)
            if month=='2' and mpfr.jan is not None:
                print mpfr.jan
                return True
            elif month=='3' and mpfr.feb is not None:
                return True
            elif month=='4' and mpfr.mar is not None:
                return True
            elif month=='5' and mpfr.apr is not None:
                return True
            elif month=='6' and mpfr.may is not None:
                return True
            elif month=='7' and mpfr.jun is not None:
                return True
            elif month=='8' and mpfr.jul is not None:
                return True
            elif month=='9' and mpfr.aug is not None:
                return True
            elif month=='10' and mpfr.sept is not None:
                return True
            elif month=='11' and mpfr.oct is not None:
                return True
            elif month=='12' and mpfr.nov is not None:
                return True
            else:
                return False
        except MPFRSubmission.DoesNotExist:
            return False    

    
@login_required(login_url='/admin/')
def viewFundStatDetails(request):
    cursor = connection.cursor()
    context = RequestContext(request)
    data = {'agency_id' : request.GET.get('agency_id'),
            'year'      : request.GET.get('year', time.strftime('%Y')),
            'allocation': request.GET.get('allocation', 'PS')
    }

    releases_query ='''
    select fr.date_release, ba.activity ,fr.amount
    from fund_releases fr inner join budget_allocation ba on 
    fr.budgetallocation_id=ba.id and ba.agency_id=%s and ba.year=%s
    inner join allocation a on
    ba.allocation_id=a.id and a.name=%s
    '''
    
    agency = Agency.objects.get(id = data['agency_id'])
    total_ps = BudgetAllocation.objects.filter(agency = agency, year = data['year'], allocation__name = data['allocation']).aggregate(Sum('total'))
    data['total'] = numify(total_ps['total__sum'])
    temp_total = data['total']
    details = []
    cursor.execute(releases_query, [data['agency_id'], data['year'], data['allocation']])
    for release in cursor.fetchall():
        temp_total = temp_total-release[2]
        details.append({'release_date'   : release[0],
                        'activity'       : release[1],
                        'release_amount' : release[2],
                        'balance'        : temp_total
                    })
    data['fund_stat_details'] = details
        
    return render_to_response('./fund/fund_stat_details.html', data, context)


@login_required(login_url='/admin/')
def AgenciesbalanceSumm(request):
    context = RequestContext(request)
    cursor = connection.cursor()
    data = {
        'year' : request.GET.get('year', time.strftime('%Y')),
        'system_name' : SYSTEM_NAME,
    }
    query = '''
    SELECT *, (ps+mooe+co) AS total
    FROM fund_balances WHERE year=%s
    '''
    cursor.execute(query, [data['year']])
    data['balances'] = dictfetchall(cursor)
    return render_to_response('./fund/running_balances.html', data, context)

def getAllotmentBal(request):
    context = RequestContext(request)

    year = int(request.GET.get('year'))
    allocation = request.GET.get('allocation')
    month = int(request.GET.get('month'))
    agency = Agency.objects.get(id=request.GET.get('agency_id'))
    balance = 0.00
    try:
        #budget
        budget = gettotalAllocation(year, month, agency, allocation)
        #getRelease
        release = getReleaseAmount(year, month, agency, allocation)
        balance = budget-numify(release)
        return HttpResponse(balance)
    except:
        return HttpResponse(balance)

    

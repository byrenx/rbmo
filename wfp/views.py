from django.shortcuts import render, render_to_response, redirect, RequestContext
import time
from django.db import transaction, connection
from django.http import  HttpResponseRedirect, HttpResponse
from django.conf import settings
from django.conf.urls.static import static
from rbmo.models import Agency, WFPData, PerformanceTarget, CoRequest, PerformanceReport
from django.contrib.auth.models import User
from .forms import WFPForm, CORequestForm, YearSelectForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required, permission_required
from django.views.decorators.http import require_http_methods
from helpers.helpers import * 
from datetime import datetime, date
import json

SYSTEM_NAME = 'e-RBMO Data Management System'

months = ['January', 'February', 'March', 'April', 
          'May', 'June', 'July', 'August', 'September', 
          'October', 'November', 'December']

@login_required(login_url='/admin/')
@transaction.atomic
def wfpForm(request, agency_id):
    context = RequestContext(request)
    try:
        agency = Agency.objects.get(id=agency_id)
        data = {'system_name'  : SYSTEM_NAME,
                'allowed_tabs' : get_allowed_tabs(request.user.id),
                'current_year' : time.strftime('%Y'),
                'current_tab'  : "WFP",
                'agency_tabs'  : getAgencyTabs(request.user.id, agency.id),
                'form'         : WFPForm(),
                'agency'       : agency}
    
        if request.method=='POST':
            wfp_form = WFPForm(request.POST)
            if wfp_form.is_valid():
                saveWFPData(request, wfp_form, request.POST.get('year'), request.POST.get('agency'))
                data['s_msg'] = 'WFP Entry was succesfully saved'
                data['agency'] = Agency.objects.get(id=request.POST.get('agency'))
                return render_to_response('./wfp/wfp_form.html', data, context)
            else:
                data['frm_errors'] = wfp_form.errors
                data['form'] = wfp_form
                return render_to_response('./wfp/wfp_form.html', data, context)
        else:
            return render_to_response('./wfp/wfp_form.html', data, context)
    except Agency.DoesNotExist:
        return HttpResponseRedirect('/admin/agencies')
    
@login_required(login_url='/admin/')
@transaction.atomic
def viewWFP(request, agency_id):
    context = RequestContext(request)
    cursor = connection.cursor()
    year = datetime.today().year
    if "year" in request.GET:
        year = request.GET.get("year")
    
    try:
        current_year = datetime.today().year
        form_yr_sel = YearSelectForm({'year' : year})
        agency = Agency.objects.get(id = agency_id)
        data = {'system_name'  : SYSTEM_NAME,
                'current_tab'  : 'WFP',
                'agency'       : agency,
                'allowed_tabs' : get_allowed_tabs(request.user.id),
                'agency_tabs'  : getAgencyTabs(request.user.id, agency.id),
                'years'        : getYears(agency_id),
                'current_year' : current_year,
                'year'         : year,
                'pss'          : getProgActs('PS', agency, year),
                'mooes'        : getProgActs('MOOE', agency, year),
                'cos'          : getProgActs('CO', agency, year),
                'form_yr_sel'  : form_yr_sel 
        }
        return render_to_response('./wfp/agency_wfp_info.html', data, context)
    except Agency.DoesNotExist:
        return HttpResponseRedirect('/admin/agencies')
            
def getYears(agency_id):
    cursor = connection.cursor()
    query = '''select distinct(year) from wfp_data where agency_id=%s'''
    cursor.execute(query, [agency_id])
    return dictfetchall(cursor)

def getProgActs(allocation, agency, year):
    cursor = connection.cursor()
    query = '''
    select distinct(program) from wfp_data
    where allocation=%s and agency_id=%s and year=%s
    '''
    cursor.execute(query, [allocation, agency.id, year])
    prog_acts = []
    maj_prog = cursor.fetchall()
    for prog in maj_prog:
        acts = []
        activities = WFPData.objects.filter(agency=agency, allocation=allocation , year=year, program=prog[0])
        for act in activities:
            acts.append({'id' : act.id,
                         'activity' : act.activity
                     })
        prog_acts.append({'prog' : prog[0],
                    'acts' : acts
                })
    return prog_acts
    

@transaction.atomic
def getWFPData(request):
    data = {}
    context = RequestContext(request)
    wfp_id  = request.GET.get('wfp_id')
    q_targets = []
    wfp     = WFPData.objects.get(id=wfp_id)
    perf_targets = PerformanceTarget.objects.filter(wfp_activity=wfp.id)
    
    for target in perf_targets:
        q_targets.append({'id'       : target.id,
                          'indicator': target.indicator,
                          'q1'       : target.jan+target.feb+target.mar,
                          'q2'       : target.apr+target.may+target.jun,
                          'q3'       : target.jul+target.aug+target.sept,
                          'q4'       : target.oct+target.nov+target.dec,
                      })

    data['wfp'] = wfp
    data['perf_targets'] = q_targets

    return render_to_response('./wfp/wfp_prog_detail.html', data, context)


'''
helper functions
'''
@transaction.atomic
def saveWFPData(request, wfp_form, year, agency_id):
    wfp = WFPData(
        year = year,
        program = wfp_form.cleaned_data['program'],
        activity = wfp_form.cleaned_data['activity'],
        allocation = request.POST.get('allocation'),
        agency = Agency.objects.get(id=agency_id),
        jan = wfp_form.cleaned_data['jan'],
        feb = wfp_form.cleaned_data['feb'],
        mar = wfp_form.cleaned_data['mar'],
        apr = wfp_form.cleaned_data['apr'],
        may = wfp_form.cleaned_data['may'],
        jun = wfp_form.cleaned_data['jun'],
        jul = wfp_form.cleaned_data['jul'],
        aug = wfp_form.cleaned_data['aug'],
        sept = wfp_form.cleaned_data['sept'],
        oct = wfp_form.cleaned_data['oct'],
        nov = wfp_form.cleaned_data['nov'],
        dec = wfp_form.cleaned_data['dec']
    )
    wfp.total = wfp.jan + wfp.feb + wfp.mar + wfp.apr + wfp.may + wfp.jun + wfp.jul + wfp.aug + wfp.sept + wfp.oct + wfp.nov + wfp.dec

    wfp.save()
    #save performance indicator
    perf_indics = request.POST.getlist('pis[]')
    for pi in perf_indics:
        pi_info = pi.split(';')
        perf_target = PerformanceTarget(wfp_activity=wfp,
                                        indicator=pi_info[0],
                                        jan=pi_info[1],
                                        feb=pi_info[2],
                                        mar=pi_info[3],
                                        apr=pi_info[4],
                                        may=pi_info[5],
                                        jun=pi_info[6],
                                        jul=pi_info[7],
                                        aug=pi_info[8],
                                        sept=pi_info[9],
                                        oct=pi_info[10],
                                        nov=pi_info[11],
                                        dec=pi_info[12]
        )
        perf_target.save()
        

@transaction.atomic
def printWFPData(request):
    context = RequestContext(request)
    agency = Agency.objects.get(id=request.GET.get('agency_id'))
    year = request.GET.get('year') 
    
    pss = getProgOverview('PS', agency, year)
    mooes = getProgOverview('MOOE', agency, year)
    cos = getProgOverview('CO', agency, year)
    wfp_total = getWFPTotal(agency, year)

    
    data = {'system_name' : SYSTEM_NAME,
            'agency'      : agency,
            'year'        : year,
            'cur_date'    : time.strftime('%B %d, %Y'),
            'pss'         : pss,
            'mooes'       : mooes,
            'cos'         : cos,
            'wfp_total'   : wfp_total}
    
    return render_to_response('./wfp/wfp_print.html',data, context)


@login_required(login_url='/admin/')
def viewApprovedBudget(request):
    context = RequestContext(request)
    data = {'system_name'  : SYSTEM_NAME}
    cursor = connection.cursor()
    data['allowed_tabs'] = get_allowed_tabs(request.user.id)
    try:
        agency = Agency.objects.get(id=request.GET.get('agency_id'))
        data['agency'] = agency
        return render_to_response('./wfp/approved_budget.html', data, context)
    except Agency.DoesNotExist:
        return render_to_response('./wfp/approved_budget.html', data, context)


@transaction.atomic
def updateMonthlyAmount(request):
    month  = int(request.GET.get('month'))
    wfp_id = int(request.GET.get('id_wfp'))
    amount = eval(request.GET.get('amount'))
    print amount
    
    try:
        wfp = WFPData.objects.get(id=wfp_id)
        
        if month==1:
            wfp.jan = amount
        elif month==2:
            wfp.feb = amount
        elif month==3:
            wfp.mar = amount
        elif month==4:
            wfp.apr = amount
        elif month==5:
            wfp.may = amount
        elif month==6:
            wfp.jun = amount
        elif month==7:
            wfp.jul = amount
        elif month==8:
            wfp.aug = amount
        elif month==9:
            wfp.sept = amount
        elif month==10:
            wfp.oct = amount
        elif month==11:
            wfp.nov = amount
        else:
            wfp.dec = amount
            print wfp.jan, wfp.feb
        wfp.total = float(wfp.jan) + float(wfp.feb) + float(wfp.mar) + float(wfp.apr) + float(wfp.may) + float(wfp.jun) + float(wfp.jul) + float(wfp.aug) + float(wfp.sept) + float(wfp.oct) + float(wfp.nov) + float(wfp.dec)
        wfp.save()
        return HttpResponse('Updated')
    except WFPData.DoesNotExist:
        return HttpResponse('Error')
    
def updateActivity(request):
    try:
        wfp_id   = request.GET.get('wfp_id')
        activity = request.GET.get('activity')
        program = request.GET.get('program')
        allocation = request.GET.get('allocation')

        wfp = WFPData.objects.get(id=wfp_id)
        wfp.activity = activity
        wfp.program = program
        wfp.allocation = allocation
        wfp.save()
        return HttpResponse(activity);
    except WFPData.DoesNotExist:
        return HttpResponse('Error')

@login_required(login_url='/home')
@transaction.atomic
def delActivity(request):
    activity_id = request.GET.get('activity_id')
    
    try:
        wfp_activity = WFPData.objects.get(id=activity_id)
        performance_targets = PerformanceTarget.objects.filter(wfp_activity=wfp_activity).delete()
        performance_report = PerformanceReport.objects.filter(activity=wfp_activity).delete()
        wfp_activity.delete()
        return HttpResponse('ok')
    except WFPData.DoesNotExist:
        return HttpResponseRedirect('/home')
        

def delPerfTarget(request):
    try:
        pi_id = request.GET.get('id')
        perf_target = PerformanceTarget.objects.get(id=pi_id).delete()
        return HttpResponse('Deleted')
    except:
        return HttpResponse('Error')

def addEditPerfTarget(request):
    try:
        action = request.GET.get('action')
        print action
        if action == 'add':
            wfp_id = request.GET.get('id_wfp')
            wfp = WFPData.objects.get(id=wfp_id)
            perf_target = PerformanceTarget(wfp_activity  = wfp,
                                            indicator = request.GET.get('indicator'),
                                            jan = request.GET.get('jan', 0),
                                            feb = request.GET.get('feb', 0),
                                            mar = request.GET.get('mar', 0),
                                            apr = request.GET.get('apr', 0),
                                            may = request.GET.get('may', 0),
                                            jun = request.GET.get('jun', 0),
                                            jul = request.GET.get('jul', 0),
                                            aug = request.GET.get('aug', 0),
                                            sept = request.GET.get('sept', 0),
                                            oct = request.GET.get('oct', 0),
                                            nov = request.GET.get('nov', 0),
                                            dec = request.GET.get('dec', 0)
                                        )
            perf_target.save()
            json_response = json.dumps({'action'    : 'add',
                                        'id'        : perf_target.id,
                                        'wfp_id'    : perf_target.wfp_activity.id,
                                        'indicator' : perf_target.indicator,
                                        'jan'       : perf_target.jan,
                                        'feb'       : perf_target.feb,
                                        'mar'       : perf_target.mar,
                                        'apr'       : perf_target.apr,
                                        'may'       : perf_target.may,
                                        'jun'       : perf_target.jun,
                                        'jul'       : perf_target.jul,
                                        'aug'       : perf_target.aug,
                                        'sept'      : perf_target.sept,
                                        'oct'       : perf_target.oct,
                                        'nov'       : perf_target.nov,
                                        'dec'       : perf_target.dec})
            return HttpResponse(json_response, content_type = "application/json")
        else:#edit
            id = request.GET['id_ppt']
            perf_target = PerformanceTarget.objects.get(id = id)
            perf_target.indicator = request.GET['indicator']
            perf_target.jan = request.GET['jan']
            perf_target.feb = request.GET['feb']
            perf_target.mar = request.GET['mar']
            perf_target.apr = request.GET['apr']
            perf_target.may = request.GET['may']
            perf_target.jun = request.GET['jun']
            perf_target.jul = request.GET['jul']
            perf_target.aug = request.GET['aug']
            perf_target.sept = request.GET['sept']
            perf_target.oct = request.GET['oct']
            perf_target.nov = request.GET['nov']
            perf_target.dec = request.GET['dec']
            perf_target.save()

            json_response = json.dumps({'action'    : 'edit',
                                        'id'        : perf_target.id,
                                        'wfp_id'    : perf_target.wfp_activity.id,
                                        'indicator' : perf_target.indicator,
                                        'jan'       : perf_target.jan,
                                        'feb'       : perf_target.feb,
                                        'mar'       : perf_target.mar,
                                        'apr'       : perf_target.apr,
                                        'may'       : perf_target.may,
                                        'jun'       : perf_target.jun,
                                        'jul'       : perf_target.jul,
                                        'aug'       : perf_target.aug,
                                        'sept'      : perf_target.sept,
                                        'oct'       : perf_target.oct,
                                        'nov'       : perf_target.nov,
                                        'dec'       : perf_target.dec})
            return HttpResponse(json_response, content_type = "application/json")
        
    except WFPData.DoesNotExist:
        return HttpResponse('Error')
        
        
def getPerformanceAcc(request):
    context = RequestContext(request)
    data = {}
    activity = WFPData.objects.get(id=request.GET.get('activity'))
    month = request.GET.get('month', datetime.today().month)
    try:
        perf_targets = []
        targets = PerformanceTarget.objects.filter(wfp_activity=activity)
        for target in targets:
            month = int(month)
            if month==1:
                perf_targets.append({'id'       : target.id,
                                     'indicator': target.indicator,
                                     'target'   : target.jan
                                    })
            elif month==2:
                perf_targets.append({'id'       : target.id,
                                     'indicator': target.indicator,
                                     'target'   : target.feb
                })
            elif month==3:
                perf_targets.append({'id'       : target.id,
                                     'indicator': target.indicator,
                                     'target'   : target.mar
                })
            elif month==4:
                perf_targets.append({'id'       : target.id,
                                     'indicator': target.indicator,
                                     'target'   : target.apr
                                 })
            elif month==5:
                perf_targets.append({'id'       : target.id,
                                     'indicator': target.indicator,
                                     'target'   : target.may
                                 })
            elif month==6:
                perf_targets.append({'id'       : target.id,
                                     'indicator': target.indicator,
                                     'target'   : target.jun
                                 })
            elif month==7:
                perf_targets.append({'id'       : target.id,
                                     'indicator': target.indicator,
                                     'target'   : target.jul
                                 })
            elif month==8:
                perf_targets.append({'id'       : target.id,
                                     'indicator': target.indicator,
                                     'target'   : target.aug
                                 })
            elif month==9:
                perf_targets.append({'id'       : target.id,
                                     'indicator': target.indicator,
                                     'target'   : target.sept
                                 })
            elif month==10:
                perf_targets.append({'id'       : target.id,
                                     'indicator': target.indicator,
                                     'target'   : target.oct
                                 })
            elif month==11:
                perf_targets.append({'id'       : target.id,
                                     'indicator': target.indicator,
                                     'target'   : target.nov
                                 })
            else:
                perf_targets.append({'id'       : target.id,
                                     'indicator': target.indicator,
                                     'target'   : target.nov
                                 })
        data['perf_targets'] = perf_targets
        return render_to_response('./admin/performance_acc.html', data, context)
    except PerformanceTarget.DoesNotExist:
        return render_to_response('./admin/performance_acc.html', data, context)



'''
helper methods
'''
def getProgOverview(allocation, agency, year):
    cursor = connection.cursor()
    #wfp_data = WFPData.objects.filter(agency = agency, year = year, allocation = allocation)
    query = '''
    select distinct(program) from wfp_data
    where allocation=%s and agency_id=%s and year=%s
    '''
    cursor.execute(query, [allocation, agency.id, year])
    prog_acts = []
    maj_prog = cursor.fetchall()
    for prog in maj_prog:
        acts = []
        activities = WFPData.objects.filter(agency=agency, allocation=allocation , year=year, program=prog[0])
        for act in activities:
            physical_targets = PerformanceTarget.objects.filter(wfp_activity = act)
            targets = []

            if len(physical_targets) > 0:
                target_count = 1
                for target in physical_targets:
                    if target_count == 1:
                        acts.append({'activity'  : act.activity,
                                     'indicator' : target.indicator,
                                     'q1'        : target.jan+target.feb+target.mar,
                                     'q2'        : target.apr+target.may+target.jun,
                                     'q3'        : target.jul+target.aug+target.sept,
                                     'q4'        : target.oct+target.nov+target.dec,
                                     'jan' : act.jan,
                                     'feb' : act.feb,
                                     'mar' : act.mar,
                                     'apr' : act.apr,
                                     'may' : act.may,
                                     'jun' : act.jun,
                                     'jul' : act.jul,
                                     'aug' : act.aug,
                                     'sept': act.sept,
                                     'oct' : act.oct,
                                     'nov' : act.nov,
                                     'dec' : act.dec,
                                     'total' : act.total})
                    else:
                        acts.append({'activity'  : '',
                                     'indicator' : target.indicator,
                                     'q1'        : target.jan+target.feb+target.mar,
                                     'q2'        : target.apr+target.may+target.jun,
                                     'q3'        : target.jul+target.aug+target.sept,
                                     'q4'        : target.oct+target.nov+target.dec,
                                     'jan' : '',
                                     'feb' : '',
                                     'mar' : '',
                                     'apr' : '',
                                     'may' : '',
                                     'jun' : '',
                                     'jul' : '',
                                     'aug' : '',
                                     'sept': '',
                                     'oct' : '',
                                     'nov' : '',
                                     'dec' : '',
                                     'total' : ''})
                    target_count += 1
            else:#no monthly physical targets
                acts.append({'activity'  : act.activity,
                             'indicator' : '',
                             'q1'        : '',
                             'q2'        : '',
                             'q3'        : '',
                             'q4'        : '',
                             'jan' : act.jan,
                             'feb' : act.feb,
                             'mar' : act.mar,
                             'apr' : act.apr,
                             'may' : act.may,
                             'jun' : act.jun,
                             'jul' : act.jul,
                             'aug' : act.aug,
                             'sept': act.sept,
                             'oct' : act.oct,
                             'nov' : act.nov,
                             'dec' : act.dec,
                             'total' : act.total})
        prog_acts.append({'prog' : prog[0], 'acts' : acts})
    return prog_acts


@transaction.atomic
def getWFPTotal(agency, year):
    cursor = connection.cursor()
    query = '''
            select sum(jan) as jan_total, sum(feb) as feb_total, sum(mar) as mar_total,
                   sum(apr) as apr_total, sum(may) as may_total, sum(jun) as jun_total,
                   sum(jul) as jul_total, sum(aug) as aug_total, sum(sept) as sept_total,
                   sum(oct) as oct_total, sum(nov) as nov_total, sum(`dec`) as dec_total,
                   sum(total) as total
            from wfp_data
                 where agency_id=%s and year=%s
            '''

    cursor.execute(query, [agency.id, year])    
    return dictfetchall(cursor)[0]
    



'''
CO Request views
'''

@login_required(login_url='/admin/')        
def coRequests(request, agency_id):
    cursor = connection.cursor()
    context = RequestContext(request)

    try:
        agency = Agency.objects.get(id=agency_id)
        year = 0
        month = 0
        co_requests = None
        if request.method == 'POST':
            year_month = request.POST.get('month').split('-')
            year = int(year_month[0])
            month = int(year_month[1])
        else:
            year  = int(datetime.today().year)
            month = int(datetime.today().month)
            #get current month and year
        co_requests = CoRequest.objects.filter(date_received__year=year, date_received__month=month, agency=agency)
        data = {'system_name'  : SYSTEM_NAME,
                'allowed_tabs' : get_allowed_tabs(request.user.id),
                'agency'       : agency,
                'agency_tabs'  : getAgencyTabs(request.user.id, agency.id),
                'current_tab'  : "CO Requests",
                'co_requests'  : co_requests,
                'year'         : year,
                'month'        : month,
                'month_str'    : months[month-1]}

        return render_to_response('./wfp/co_request.html', data, context)
    except Agency.DoesNotExist:
        return HttpResponseRedirect("/admin/agencies")

    
@login_required(login_url='/admin/')
def coRequestForm(request, agency_id = None, co_id=None):
    context = RequestContext(request)

    data  = {'system_name' : SYSTEM_NAME,
             'agency_id'   : agency_id,
             'action'      : request.GET.get('action')             
    }
    
    try:
        data['allowed_tabs'] = get_allowed_tabs(request.user.id)
        agency = Agency.objects.get(id=data['agency_id'])
        data['agency'] = agency
        data['agency_tabs'] = getAgencyTabs(request.user.id, agency.id)
        data['current_tab'] = "CO Requests"
        
        if request.method == 'POST':
            co_request_form = CORequestForm(request.POST)
            action = request.POST.get('form_action', 'add')
            if action == 'add' and co_request_form.is_valid():
                agency = Agency.objects.get(id=request.POST.get('agency_id'))
                date_rcv = request.POST.get('date_received')
                addCORequest(co_request_form, agency, date_rcv, request)
                data['s_msg'] = 'New request succesfully Saved'
                data['form']  = CORequestForm()
                return render_to_response('./wfp/co_request_form.html', data, context)
            elif action == 'edit' and co_request_form.is_valid():#edit
                try:
                    co_id = request.POST.get('co_id')
                    co_request = CoRequest.objects.get(id=co_id)
                    co_request.date_received = co_request_form.cleaned_data['date_received']
                    co_request.subject = co_request_form.cleaned_data['action']
                    co_request.subject = co_request_form.cleaned_data['subject']
                    co_request.status = co_request_form.cleaned_data['status']
                    co_request.remarks = co_request_form.cleaned_data['remarks']
                    co_request.save()
                    data['co_id'] = co_request.id
                    data['form_action'] = action
                    data['form'] = co_request_form
                    data['s_msg'] = 'Request Successfully updated!'
                    return render_to_response('./wfp/co_request_form.html', data, context)
                except CoRequest.DoesNotExist:
                    return HttpResponse('<h3>Invalid Request</h3>')
            else:
                return HttpResponse(action)
#        elif request.GET.get()
        else:
            action = request.GET.get('action', 'add')
            if action=='edit':
                co_request = CoRequest.objects.get(id=co_id)
                form = CORequestForm({'date_received' : co_request.date_received,
                                      'subject'       : co_request.subject,
                                      'action'        : co_request.action,
                                      'status'        : co_request.status,
                                      'remarks'       : co_request.remarks})
                data['form'] = form
                data['co_id'] = co_request.id
            else:
                data['form']   = CORequestForm()

            data['form_action'] = action
            return render_to_response('./wfp/co_request_form.html', data, context)
    except Agency.DoesNotExist:
        return HttpResponseRedirect("/admin/agencies")

def addCORequest(request_form, agency, date_rcv, request):
    co_request = CoRequest(date_received = date_rcv,
                           agency = agency,
                           subject = request_form.cleaned_data['subject'],
                           action = request_form.cleaned_data['action'],
                           status = request_form.cleaned_data['status'],
                           remarks = request_form.cleaned_data['remarks'],
                           user = request.user
                )
    co_request.save()

def delCoRequest(request, co_id):
    try:
        co_request = CoRequest.objects.get(id=co_id)
        agency_id = co_request.agency.id
        co_request.delete()
        return HttpResponseRedirect("/agency/wfp/co_request/"+str(agency_id)+"/")
    except:
        pass
    
def getProgPT(request):
    context = ReuestContext(request)
    prog_id = request.GET.get("prog_id")
    performance_targets = PerformanceTarget.objects.filter(wfp_activity = prog_id)
    pt_list = []
    for pt in performance_targets:
        pt_list.append({'id' : pt.id,
                        'indicator' : pt.indicator,
                        'q1'   : pt.jan + pt.feb + pt.mar,
                        'q2'   : pt.apr + pt.may + pt.jun,
                        'q3'   : pt.jul + pt.aug + pt.sept,
                        'q4'   : pt.oct + pt.nov + pt.dec})
    return render_to_response("./wfp/performance_targets.html", data, context)


def getPerfTarget(request):
    context = RequestContext(request)
    target_id = request.GET.get("target_id")
    pf = PerformanceTarget.objects.get(id = target_id)
    json_response = json.dumps({'id'  : pf.id, 
                                'indicator': pf.indicator, 
                                'jan' : pf.jan,
                                'feb' : pf.feb,
                                'mar' : pf.mar,
                                'apr' : pf.apr,
                                'may' : pf.may,
                                'jun' : pf.jun,
                                'jul' : pf.jul,
                                'aug' : pf.aug,
                                'sept': pf.sept,
                                'oct' : pf.oct,
                                'nov' : pf.nov,
                                'dec' : pf.dec})
    return HttpResponse(json_response, content_type = 'application/json')


def getUnreportedPrograms(request):
    #returns list of unreported programs of agency in the specified month
    #request params: agency, year and month
    agency = Agency.objects.get(id=request.GET.get('agency_id'))
    year = int(request.GET.get('year'))
    month = 5

    reported_programs = PerformanceReport.objects.filter(month = month, activity__agency = agency, year = year)
    print repr(reported_programs)
    programs = WFPData.objects.filter(agency = agency, year = year).exclude(id__in = reported_programs.values_list("activity__id"))
    
    prog_list = []
    for prog in programs:
        prog_list.append({'id'       : prog.id,
                          'activity' : prog.activity})
    json_response = json.dumps(prog_list)
    return HttpResponse(json_response, content_type="application/json");


def getURLPhysicalTargets(request):
    program_id = request.GET.get('program_id')
    targets_list = getPhysicalTargets(program_id)
    json_response = json.dumps(targets_list)
    return HttpResponse(json_response, content_type="application/json")


@require_http_methods(["POST"])
def updateAccTarget(request):
    request_body = json.loads(request.body)
    indicator = PeroformanceTarget.objects.get(id=request_body['indicator_id']);
    month = request_body['month']
    if month == 1:
        indicator.jan_acc = request_body['acc']
    elif month == 2:
        indicator.feb_acc = request_body['acc']
    elif month == 3:
        indicator.mar_acc = request_body['acc']
    elif month == 4:
        indicator.apr_acc = request_body['acc']
    elif month == 5:
        indicator.may_acc = request_body['acc']
    elif month == 6:
        indicator.jun_acc = request_body['acc']
    elif month == 7:
        indicator.jul_acc = request_body['acc']
    elif month == 8:
        indicator.aug_acc = request_body['acc']
    elif month == 9:
        indicator.sept_acc = request_body['acc']
    elif month == 10:
        indicator.oct_acc = request_body['acc']
    elif month == 11:
        indicator.nov_acc = request_body['acc']
    elif month == 12:
        indicator.dec_acc = request_body['acc']
    indicator.save()

    json_response = json.dumps({'id': indicator.id,
                                'indicator': indicator.indicator,
                                'jan': indicator.jan,
                                'jan_acc': indicator.jan_acc,
                                'feb': indicator.feb,
                                'feb_acc': indicator.feb_acc,
                                'mar': indicator.mar,
                                'mar_acc': indicator.mar_acc,
                                'apr': indicator.apr,
                                'apr_acc': indicator.apr_acc,
                                'may': indicator.may,
                                'may_acc': indicator.may_acc,
                                'jun': indicator.jun,
                                'jun_acc': indicator.jun_acc,
                                'jul': indicator.jul,
                                'jul_acc': indicator.jul_acc,
                                'aug': indicator.aug,
                                'aug_acc': indicator.aug_acc,
                                'sept': indicator.sept,
                                'sept_acc': indicator.sept_acc,
                                'oct' : indicator.oct,
                                'oct_acc': indicator.oct_acc,
                                'nov' : indicator.nov,
                                'nov_acc': indicator.nov_acc,
                                'dec': indicator.dec,
                                'dec_acc': indicator.dec_acc})

    return HttpResponse(status=200)

@require_http_methods(["GET"])
def getPerformanceIndicator(request, indicator_id):
    indicator = PerformanceTarget.objects.get(id = target_id)
    json_response = json.dumps({'id': indicator.id,
                                'indicator': indicator.indicator,
                                'jan': indicator.jan,
                                'jan_acc': indicator.jan_acc,
                                'feb': indicator.feb,
                                'feb_acc': indicator.feb_acc,
                                'mar': indicator.mar,
                                'mar_acc': indicator.mar_acc,
                                'apr': indicator.apr,
                                'apr_acc': indicator.apr_acc,
                                'may': indicator.may,
                                'may_acc': indicator.may_acc,
                                'jun': indicator.jun,
                                'jun_acc': indicator.jun_acc,
                                'jul': indicator.jul,
                                'jul_acc': indicator.jul_acc,
                                'aug': indicator.aug,
                                'aug_acc': indicator.aug_acc,
                                'sept': indicator.sept,
                                'sept_acc': indicator.sept_acc,
                                'oct' : indicator.oct,
                                'oct_acc': indicator.oct_acc,
                                'nov' : indicator.nov,
                                'nov_acc': indicator.nov_acc,
                                'dec': indicator.dec,
                                'dec_acc': indicator.dec_acc})
    return HttpResponse(json_response, content_type='application/json')

@require_http_methods(["GET"])
def getPhysicalTargets(program_id):
    program = WFPData.objects.get(id = program_id)
    targets = PerformanceTarget.objects.filter(wfp_activity = program)
    targets_list = []
    for target in targets:
        targets_list.append({'id'         : target.id,
                             'indicator'  : target.indicator,
                             'jan'        : target.jan,
                             'jan_acc'    : target.jan_acc,
                             'feb'        : target.feb,
                             'feb_acc'    : target.feb_acc,
                             'mar'        : target.mar,
                             'mar_acc'    : target.mar_acc,
                             'apr'        : target.apr,
                             'apr_acc'    : target.apr_acc,
                             'may'        : target.may,
                             'may_acc'    : target.may_acc,
                             'jun'        : target.jun,
                             'jun_acc'    : target.jun_acc,
                             'jul'        : target.jul,
                             'jul_acc'    : target.jul_acc,
                             'aug'        : target.aug,
                             'aug_acc'    : target.aug_acc,
                             'sept'       : target.sept,
                             'sept_acc'   : target.sept_acc,
                             'oct'        : target.oct,
                             'oct_acc'    : target.oct_acc,
                             'nov'        : target.nov,
                             'nov_acc'    : target.nov_acc,
                             'dec'        : target.dec,
                             'dec_acc'    : target.dec_acc
                         })
    return targets_list
    

@require_http_methods(["GET"])
def getPerformanceReport(request, report_id):
    report = PerformanceReport.objects.get(id = report_id)
    json_response = json.dumps({'id' : report.id,
                                'month': report.month,
                                'year': report.year,
                                'received': report.received,
                                'incurred': report.incurred,
                                'remarks': report.remarks})
    return HttpResponse(json_response, content_type='application/json')


@require_http_methods(["POST"])
def updatePerformanceReport(request):
    request_body = json.loads(request.body)
    report = PerformanceReport(id = request_body['id'])
    report.received = float(request_body['receied'])
    report.incurred = float(request_body['incurred'])
    report.remarks = request_body['remarks']
    report.save()
    
    data = json.dumps({'id' : report.id,
                       'received': report.received,
                       'incurred': report.incurred,
                       'remarks' : report.remarks})
    return HttpResponse(data, content_type='application/json')
    

    

    

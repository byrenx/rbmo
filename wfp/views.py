from django.shortcuts import render, render_to_response, redirect, RequestContext
import time
from django.db import transaction, connection
from django.http import  HttpResponseRedirect, HttpResponse
from django.conf import settings
from django.conf.urls.static import static
from rbmo.models import Agency, WFPData, PerformanceTarget, CoRequest, PerformanceReport
from django.contrib.auth.models import User
from .forms import WFPForm, CORequestForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required, permission_required
from helpers.helpers import has_permission, get_allowed_tabs, dictfetchall
from datetime import datetime, date

SYSTEM_NAME = 'e-RBMO Data Management System'

months = ['January', 'February', 'March', 'April', 
          'May', 'June', 'July', 'August', 'September', 
          'October', 'November', 'December']

@login_required(login_url='/admin/')
@transaction.atomic
def wfpForm(request):
    context = RequestContext(request)
    data = {'system_name':SYSTEM_NAME,
            'agency_id': request.GET.get('agency_id')
    }
    data['allowed_tabs'] = get_allowed_tabs(request.user.id)
    data['current_year'] = time.strftime('%Y')
    data['form'] = WFPForm()
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
        try:
            data['agency'] = Agency.objects.get(id=data['agency_id'])
            return render_to_response('./wfp/wfp_form.html', data, context)
        except Agency.DoesNotExist:
            return HttpResponseRedirect('/admin/agencies')
    
@login_required(login_url='/admin/')
@transaction.atomic
def viewWFP(request):
    context = RequestContext(request)
    cursor = connection.cursor()

    if 'admin_agency_id' not in request.session:
        return HttpResponseRedirect('/admin/agencies')
    else:
        try:
            current_year = datetime.today().year
            agency_id = 0
            year = datetime.today().year

            if request.method=='POST':
                year = request.POST.get('year')
                agency_id = request.POST.get('agency_id')
            else:
                agency_id = request.session['admin_agency_id']

            agency = Agency.objects.get(id = agency_id)
            data = {'system_name'  : SYSTEM_NAME,
                    'agency_tab'   : 'wfp',
                    'agency'       : agency,
                    'allowed_tabs' : get_allowed_tabs(request.user.id),
                    'years'        : getYears(agency_id),
                    'current_year' : current_year,
                    'year'         : year,
                    'pss'          : getProgActs('PS', agency, year),
                    'mooes'        : getProgActs('MOOE', agency, year),
                    'cos'          : getProgActs('CO', agency, year)
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


@login_required(login_url='/admin/')        
def coRequests(request):
    cursor = connection.cursor()
    context = RequestContext(request)
    data  = {'system_name' : SYSTEM_NAME,
             'agency_id'   : request.GET.get('agency_id')}

    try:
        data['allowed_tabs'] = get_allowed_tabs(request.user.id)
        agency = Agency.objects.get(id=data['agency_id'])
        data['agency'] = agency
        year = 0
        month = 0
        co_requests = None
        if request.method == 'POST':
            year_month = request.POST.get('month').split('-')
            year = int(year_month[0])
            month = int(year_month[1])
        else:
            year  = int(time.strftime('%Y'))
            month = int(time.strftime('%m'))
            #get current month and year
        co_requests = CoRequest.objects.filter(date_received__year=year, date_received__month=month, agency=agency)
        data['co_requests'] = co_requests
        data['year'] = year
        data['month'] = month
        data['month_str'] = months[month-1]
        
        return render_to_response('./wfp/co_request.html', data, context)
    except Agency.DoesNotExist:
        return HttpResponseRedirect("/admin/agencies")

    
@login_required(login_url='/admin/')
def coRequestForm(request):
    context = RequestContext(request)
    data  = {'system_name' : SYSTEM_NAME,
             'agency_id'   : request.GET.get('agency_id'),
             'action'      : request.GET.get('action')
    }
    
    try:
        data['allowed_tabs'] = get_allowed_tabs(request.user.id)
        agency = Agency.objects.get(id=data['agency_id'])
        data['agency'] = agency
        
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
                return HttpResponse('edit')
            else:
                return HttpResponse(action)
#        elif request.GET.get()
        else:
            data['form_action'] = request.GET.get('form_action', 'add')
            data['form']   = CORequestForm()
            return render_to_response('./wfp/co_request_form.html', data, context)
    except Agency.DoesNotExist:
        return HttpResponseRedirect("/admin/agencies")

def addCORequest(request_form, agency, date_rcv, request):
    co_request = CoRequest(date_received = date_rcv,
                           agency = agency,
                           subject = request_form.cleaned_data['subject'],
                           action = request_form.cleaned_data['action'],
                           status = request_form.cleaned_data['status'],
                           user = request.user
                )
    co_request.save()

@transaction.atomic
def updateMonthlyAmount(request):
    month  = int(request.GET.get('month'))
    wfp_id = int(request.GET.get('id_wfp'))
    amount = eval(request.GET.get('amount'))
    
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

        wfp.total = wfp.jan + wfp.feb + wfp.mar + wfp.apr + wfp.may + wfp.jun + wfp.jul + wfp.aug + wfp.sept + wfp.oct + wfp.nov + wfp.dec
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

def addPerfTarget(request):
    try:
        wfp_id = request.GET.get('id_wfp')
        wfp = WFPData.objects.get(id=wfp_id)
        perf_target = PerformanceTarget(wfp_activity  = wfp,
                                        indicator = request.GET.get('pi'),
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
        return HttpResponse('Added')
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
            for target in physical_targets:
                targets.append({'indicator': target.indicator,
                                'q1'       : target.jan+target.feb+target.mar,
                                'q2'       : target.apr+target.may+target.jun,
                                'q3'       : target.jul+target.aug+target.sept,
                                'q4'       : target.oct+target.nov+target.dec})
            acts.append({'activity'         : act,
                         'physical_targets' : targets
                     })
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
    

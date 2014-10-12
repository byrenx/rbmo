from django.shortcuts import render, render_to_response, redirect, RequestContext
from django.db import transaction, connection
from django.db.models import Sum, Avg
from django.http import  HttpResponseRedirect, HttpResponse
from django.conf import settings
from django.conf.urls.static import static
from .forms import (BudgetProposalForm, LoginForm, ChangePassForm, YearFilterForm)
from requirements.views import (getSubmittedReqs,
                                getLackingReqs)
from rbmo.forms import MonthForm
from rbmo.models import (UserGroup, Groups, Agency, 
                         Notification, AllotmentReleases, WFPData, 
                         AllotmentReleases, PerformanceReport)

from wfp.views import getProgOverview, getWFPTotal
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required, permission_required
from helpers.helpers import *
from datetime import date, datetime
import hashlib

months = getMonthLookup()
month_acc_dict = {1: 'jan_acc', 2: 'feb_acc', 3: 'mar_acc', 4: 'apr_acc',
                  5: 'may_acc', 6: 'jun_acc', 7: 'jul_acc', 8: 'aug_acc',
                  9: 'sept_acc', 10: 'oct_acc', 11: 'nov_acc', 12: 'dec_acc'
}


def login(request):
    context = RequestContext(request)
    h = hashlib.sha256()
    data = {'form' : LoginForm()}
    if request.method=="POST":
        loginform = LoginForm(request.POST)
        if loginform.is_valid():
            email = loginform.cleaned_data['email']
            h.update(loginform.cleaned_data['acces_key'])
            accesskey = h.hexdigest()
            print loginform.cleaned_data['acces_key']
            print accesskey
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

        years = []
        while year >= 2014:
            years.append(year)
            year-=1

        data = {'system_name'    : agency.name,
                'email'          : agency.email,
                'month_form'     : MonthForm({'month': month}),
                'str_month'      : stringify_month(month),
                'submitted_reqs' : srs,
                'lacking_reqs'   : lrs,
                'page'           : 'requirements',
                'year'           : year,
                'years'          : years}

        return render_to_response('./agency/Requirements.html', data, context)
    else:
        return HttpResponse('????')


@transaction.atomic        
def balance(request):
    if "agency_id" in request.session:
        cursor = connection.cursor()
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
                     'ending_bal':co_bal}                   
                   ]
        total_balance =  {'allocation'   : 'Total',
                     'beginning_bal': numify(ps_total['total__sum']) + numify(mooe_total['total__sum']) + numify(co_total['total__sum']),
                     'release': numify(ps_release['amount_release__sum']) + numify(mooe_release['amount_release__sum']) + numify(co_release['amount_release__sum']),
                     'ending_bal' : ps_bal + mooe_bal + co_bal}


        cursor.execute("select distinct(year) from wfp_data where agency_id=%s", agency.id)
        years = dictfetchall(cursor)
        data = {'system_name' : agency.name,
                'email'       : agency.email,
                'balances'    : balances,
                'total_balance': total_balance,
                'cur_date'    : time.strftime('%B %d, %Y'),
                'year'        : year,
                'page'        : 'balance',
                'years'       : years
               }
        return render_to_response('./agency/Balances.html', data, context)
        
                    
@transaction.atomic
def approved(request):
    if "agency_id" in request.session:
        context = RequestContext(request)
        agency_id = request.session["agency_id"]
        agency = Agency.objects.get(id=agency_id)
        year = request.POST.get('year', datetime.today().year)

        pss = getProgOverview('PS', agency, year)
        mooes = getProgOverview('MOOE', agency, year)
        cos = getProgOverview('CO', agency, year)
        wfp_total = getWFPTotal(agency, year)

        data = {'system_name' : agency.name, 
                'email'       : agency.email,
                'page'        : 'wfp',
                'cur_date'    : time.strftime('%B %d, %Y'),
                'pss'         : pss,
                'mooes'       : mooes,
                'cos'         : cos,
                'year'        : year,
                'agency'      : agency,
                'wfp_total'   : wfp_total,
                'year_form'   : YearFilterForm({'year' : year})
        }

        return render_to_response('./agency/approved.html', data, context)
    else:
        return HttpResponseRedirect('/')



def allotmentReleases(request):
    context       = RequestContext(request)
    allotments    = {}
    total_release = 0
    total_PS      = 0
    total_MOOE    = 0
    total_CO      = 0
    year = request.POST.get('year',datetime.today().year)
    
    try:
        if "agency_id" in request.session:
            agency                  = Agency.objects.get(id=request.session['agency_id'])
            wfp_data_PS             = WFPData.objects.filter(agency=agency, year=year, allocation='PS').aggregate(total_sum = Sum('total'))
            wfp_data_MOOE           = WFPData.objects.filter(agency=agency, year=year, allocation='MOOE').aggregate(total_sum = Sum('total'))
            wfp_data_CO             = WFPData.objects.filter(agency=agency, year=year, allocation='CO').aggregate(total_sum = Sum('total'))
            allotment_releases      = AllotmentReleases.objects.filter(agency=agency, year=year).order_by('year', 'month')
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
                'system_name'             : agency.name,
                'agency'                  : agency,
                'email'                   : agency.email,
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
                'year'                    : year,
                'page'                    : 'releases'
            }

            #get releases
            return render_to_response('./agency/allotment_releases.html', data, context)
    except Agency.DoesNotExist:
        return HttpResponseRedirect('/admin/agencies')


def monthlyReports(request):
    try:
        cursor = connection.cursor()
        context = RequestContext(request)
        if "agency_id" in request.session:
            agency = Agency.objects.get(id=request.session['agency_id'])
            year = int(request.POST.get('year', datetime.today().year))
            month = int(request.POST.get('month', datetime.today().month))

            perf_accs_query = "select "+months[month]+" as budget, "
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
                query = "select indicator, "+months[month-1]+" as target, "+month_acc_dict[month]+" as acc from performancetarget where wfp_activity_id=%s"
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
            data = {'system_name' : agency.name,
                    'email'  : agency.email,
                    'agency' : agency,
                    'years'  : dictfetchall(cursor),
                    'monthly_acts_reports' : monthly_acts_reports,
                    'str_month' : stringify_month(month),
                    'year'   : year,
                    'month_form' : MonthForm({'month' : month})
            }
            
            return render_to_response('./agency/monthly_reports.html', data, context)
    except Agency.DoesNotExist:
        pass



def mpfro_form(request):
    cursor = connection.cursor()
    context = RequestContext(request)

    this_year = datetime.today().year
    years = [this_year, (this_year-1)]
    try:
        if "agency_id" in request.session:
            action = request.GET.get('action', 'add')
            agency = Agency.objects.get(id=request.session['agency_id'])
          
            if action == 'add':
                year = datetime.today().year
                acts_query = "select id, activity from wfp_data where agency_id=%s and year=%s and wfp_data.id not in (select activity_id from performance_report where performance_report.year=%s and performance_report.month=%s)"
                cursor.execute(acts_query, [agency.id, year, year, datetime.today().month])
                activities = dictfetchall(cursor)
                data = {'system_name': agency.name,
                        'email'      : agency.email,
                        'action'     : action,
                        'agency'     : agency,
                        'month_form' : MonthForm({'month': datetime.today().month}),
                        'year'       : year,
                        'activities' : activities,
                        'years'      : [2014]
                }

                return render_to_response('./agency/mpfro_form.html', data, context)
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

        return HttpResponseRedirect('/agency/monthly_reports')
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
        
        return HttpResponseRedirect('/agency/monthly_reports')


def logout(request):
    if "agency_id" in request.session:
        del request.session['agency_id']
    return HttpResponseRedirect('/home')

    
    
def changePass(request):
    context = RequestContext(request)
    h = hashlib.sha256()
    if "agency_id" in request.session:
        try:
            agency = Agency.objects.get(id = request.session['agency_id'])
            data = {'system_name' : agency.name,
                    'email'       : agency.email,
                    'agency'      : agency,
                    'form'        : ChangePassForm({'agency_id' : agency.id})
            }
            
            if request.method=='POST':
                cp_form = ChangePassForm(request.POST)
                if cp_form.is_valid():
                    access_key = agency.acces_key
                    h.update(cp_form.cleaned_data['current_accesskey'])
                    current_key = h.hexdigest()
                    new_key = cp_form.cleaned_data['new_accesskey']
                    confirm_key = cp_form.cleaned_data['confirm_accesskey']
                    if access_key!=current_key:
                        data['e_msg']  = 'Current access key does not match'
                        return render_to_response("./agency/change_pass.html", data, context)
                    elif new_key != confirm_key:
                        data['e_msg']  = 'New access key confirmation mismatch'
                        return render_to_response("./agency/change_pass.html", data, context)
                    elif len(new_key) < 8:
                        data['e_msg']  = 'New access key must be at least 8 characters long'
                        return render_to_response("./agency/change_pass.html", data, context)
                    else:
                        h1 = hashlib.sha256()
                        h1.update(new_key)
                        agency.acces_key = h1.hexdigest()
                        agency.save()
                        data['s_msg']  = 'Access key successfully changed'
                        return render_to_response("./agency/change_pass.html", data, context)
                
            return render_to_response("./agency/change_pass.html", data, context)
        except Agency.DoesNotExist:
            return HttpRsponseRedirect('/home')
    else:
        return HttpRsponseRedirect('/home')


from django.conf.urls import patterns, include, url
from wfp.views import *
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
                       url(r'^wfp_form/(?P<agency_id>[0-9]+)/$', wfpForm),
                       url(r'^wfpinfo/(?P<agency_id>[0-9]+)/$', viewWFP),
                       url(r'^wfpdetail$', getWFPData),
                       url(r'^wfp_print$', printWFPData),
                       url(r'^approved_budget$', viewApprovedBudget),
                       url(r'^update_monthly_amount$', updateMonthlyAmount),
                       url(r'^update_activity$', updateActivity),
                       url(r'^delete_perf_target$', delPerfTarget),
                       url(r'^performance_target$', addEditPerfTarget),
                       url(r'^get_performance_acc$', getPerformanceAcc),
                       url(r'^delete_activity$', delActivity),
                       url(r'^co_request/(?P<agency_id>[0-9]+)/$', coRequests),
                       url(r'^co_request_form/(?P<agency_id>[0-9]+)/$', coRequestForm),
                       url(r'^co_request_form/(?P<agency_id>[0-9]+)/(?P<co_id>[0-9]+)/$', coRequestForm),
                       url(r'^del_co_request/(?P<co_id>[0-9]+)', delCoRequest),
                       #new urls
                       url(r'^get/performance/target/$', getPerfTarget),
                       #get Programs jax call
                       url(r'^get/unreportedprograms/$', getUnreportedPrograms),
                       url(r'^get/program/physicaltargets/$', getURLPhysicalTargets),
                       url(r'^get/performance_indicator/(?P<indicator_id>[0-9]+)$', getPerformanceIndicator),
                       url(r'^get/performance_report/(?P<report_id>[0-9]+)$', getPerformanceReport),
                       url(r'^update/performance_report/(?P<report_id>[0-9]+)$', updatePerformanceReport),                       
                       url(r'^update/accomplished_targets$', updateAccTarget),                       
)

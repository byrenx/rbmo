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
    url(r'^co_request/(?P<agency_id>[0-9]+)/$', coRequests),
    url(r'^co_request_form$', coRequestForm),
    url(r'^update_monthly_amount$', updateMonthlyAmount),
    url(r'^update_activity$', updateActivity),
    url(r'^delete_perf_target$', delPerfTarget),
    url(r'^add_performance_target$', addPerfTarget),
    url(r'^get_performance_acc$', getPerformanceAcc),
    url(r'^delete_activity$', delActivity),
)

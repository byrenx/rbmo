from django.conf.urls import patterns, include, url
from fund.views import *
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^fund_release$', fundReleaseForm),
    url(r'^monthly_alloc$', monthlyAlloc),
    url(r'^get_budget$', getAllocatedBudget),
    url(r'^view_fund_status$',  getFundStatus),
    url(r'^view_fstat_detail$',  viewFundStatDetails),
    url(r'^running_balances$',  agenciesBudgetSummary),
    url(r'^allotment_releases$',  allotmentReleases),
)

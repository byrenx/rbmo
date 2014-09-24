from django.conf.urls import patterns, include, url
from .views import *
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', index),
    url(r'^home/$', home),
    url(r'^users/$', users),
    url(r'^add_edit_user$', addEditUser),
    url(r'^agencies$', agencies),
    url(r'^pm_agency$', addEditAgency),
    url(r'^agencies_by_sector$', getAgenciesbySector),
    url(r'^manage_agency_docs/(?P<agency_id>[0-9]+)/$',  manageAgencyDocs),
    url(r'^manage_agency_docs/(?P<agency_id>[0-9]+)/(?P<year>[0-9]{4})/$',  manageAgencyDocs),
    url(r'^submit_monthly_mpfr$',  submitMPFR),
    url(r'^submit_requirements$', saveSubmitReqs),
    url(r'^delete_requirement$', delSubmitReqs),
    url(r'^monthly_reports/(?P<agency_id>[0-9]+)/$', mpfroReports),
    url(r'^monthly_reports_form$', mpfro_form),
    url(r'^submit_quarter_reqs$', submitQuarterReq),
    url(r'^allot_releases$', allot_releases),
    url(r'^yearly_fund$', yearly_fund),
    url(r'^fund_distrib$', fundDistribution),
    url(r'^total_monthly_release$', totalMonthlyReleases),
    url(r'^submit_cos$', submitCOS),
    url(r'^agencies_with_compreqs$', agenciesCompReqList),
    url(r'^agencies_with_increqs$', agenciesIncReqList),
    url(r'^change_password$', changePass),
    url(r'^approved_budget$', approvedBudget),
    url(r'^smca$', smca),
    url(r'^add_performance_report', savePerformanceReport),
    url(r'^display_sub_qreqs', getDisplaySubmittedQReq),
)

from rest_framework import routers
from django.conf.urls import patterns, include, url
from .views import *
from django.contrib import admin
from agency.views import *
admin.autodiscover()


router = routers.DefaultRouter()
router.register(r'agencies', AgencyViewSet)
router.register(r'performance_reports', PerformaceReportViewSet)

urlpatterns = patterns('',
                       url(r'^$', home),
                       url(r'^api/', include(router.urls)),
                       url(r'^home$', home),
                       url(r'^logout$', logout_user),
                       url(r'^agency/wfp/', include('wfp.urls')),
                       url(r'^agency/fund/', include('fund.urls')),
                       url(r'^agency/', include('agency.urls')),
                       url(r'^history/', include('history_logs.urls')),
                       url(r'^requirements/', include('requirements.urls')),
                       url(r'^main$', index),
                       url(r'^main/home$', main),
                       url(r'^main/users/$', users),
                       url(r'^main/add_edit_user$', addEditUser),
                       url(r'^main/change_status$', changeUserStatus),
                       url(r'^main/agencies$', agencies),
                       url(r'^main/pm_agency$', addEditAgency),
                       url(r'^main/rm_agency/(?P<agency_id>[0-9]+)/?', deleteAgency),
                       url(r'^main/agencies_by_sector$', getAgenciesbySector),
                       url(r'^main/manage_agency_docs/(?P<agency_id>[0-9]+)/$',  manageAgencyDocs),
                       url(r'^main/manage_agency_docs/(?P<agency_id>[0-9]+)/(?P<year>[0-9]{4})/$',  manageAgencyDocs),
                       url(r'^main/submit_monthly_mpfr$',  submitMPFR),
                       url(r'^main/submit_requirements$', saveSubmitReqs),
                       url(r'^main/delete_requirement$', delSubmitReqs),
                       url(r'^main/monthly_reports/(?P<agency_id>[0-9]+)/$', mpfroReports),
                       url(r'^main/monthly_reports_form/(?P<agency_id>[0-9]+)/$', mpfro_form),
                       url(r'^main/submit_quarter_reqs$', submitQuarterReq),
                       url(r'^main/allot_releases$', allot_releases),
                       url(r'^main/yearly_fund$', yearly_fund),
                       url(r'^main/fund_distrib$', fundDistribution),
                       url(r'^main/total_monthly_release$', totalMonthlyReleases),
                       url(r'^main/submit_cos$', submitCOS),
                       url(r'^main/agencies_with_compreqs$', agenciesCompReqList),
                       url(r'^main/agencies_with_increqs$', agenciesIncReqList),
                       url(r'^main/change_password$', changePass),
                       url(r'^main/approved_budget$', approvedBudget),
                       url(r'^main/smca$', smca),
                       url(r'^main/add_performance_report', savePerformanceReport),
                       url(r'^main/display_sub_qreqs', getDisplaySubmittedQReq),
                       url(r'^main/fund_distrib_print', fundDistribPrint),

)

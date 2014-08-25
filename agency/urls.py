from django.conf.urls import patterns, include, url
from agency.views import *
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
        url(r'^login$', login),
        url(r'^home$', requirements),
        url(r'^requirements',requirements),
        url(r'^balance',balance),
        url(r'^approved',approved),
        url(r'^releases',allotmentReleases),
        url(r'^monthly_reports', monthlyReports),
        url(r'^monthly_report_form', mpfro_form),
        url(r'^add_performance_report', savePerformanceReport),
        url(r'^logout', logout)
)

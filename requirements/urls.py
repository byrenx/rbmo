from django.conf.urls import patterns, include, url
from .views import *
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', manageAgencyDocs),
    url(r'^delete_month_sub_req$', delMonthReqs),
)

from django.conf.urls import patterns, include, url
from .views import *
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'rbmo.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    #url(r'^admin/', include(admin.site.urls)),
    url(r'^$', home),
    url(r'^home$', home),
    url(r'^logout$', logout_user),
    url(r'^admin/', include('admin.urls')),
    url(r'^agency/wfp/', include('wfp.urls')),
    url(r'^agency/fund/', include('fund.urls')),
    url(r'^agency/', include('agency.urls')),
    url(r'^transaction/', include('transaction.urls')),
)

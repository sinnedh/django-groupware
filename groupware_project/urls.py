from django.conf.urls.static import static

from django.conf.urls import patterns, include, url

#from django.contrib import admin
#admin.autodiscover()

urlpatterns = patterns('',
    url(r'^accounts/', include('accounts.urls', namespace='accounts')),
    url(r'^groupcalendar/', include('groupcalendar.urls', namespace='groupcalendar')),
    url(r'^groupcontacts/', include('groupcontacts.urls', namespace='groupcontacts')),
    url(r'^', include('commons.urls', namespace='commons')),
#    url(r'^admin/', include(admin.site.urls)),
)

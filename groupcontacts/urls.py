from django.conf import settings
from django.conf.urls.static import static

from django.conf.urls import patterns, include, url

from groupcontacts.views import ContactDetail, ContactList, ContactUpdate
#from django.contrib import admin
#admin.autodiscover()

urlpatterns = patterns('',
#    url(r'^$', 'groupcontacts.views.list', name='home'),
    url(r'contact/$', ContactList.as_view(), name='contact_list'),
    url(r'contact/(?P<pk>\d+)/detail/$', ContactDetail.as_view(), name='contact_detail'),
    url(r'contact/(?P<pk>\d+)/$', ContactUpdate.as_view(), name='contact_update'),
)

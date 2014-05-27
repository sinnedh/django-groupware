from django.conf import settings
from django.conf.urls.static import static

from django.conf.urls import patterns, include, url

#from django.contrib import admin
#admin.autodiscover()

urlpatterns = patterns('',
    # TODO:  add to calender urls file
    url(r'^$', 'commons.views.start', name='start'),
)

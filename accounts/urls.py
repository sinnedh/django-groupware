from django.conf import settings
from django.conf.urls.static import static

from django.conf.urls import patterns, include, url

#from django.contrib import admin
#admin.autodiscover()

urlpatterns = patterns('',
    # TODO:  add to calender urls file
    url(r'^login/?$', 'django.contrib.auth.views.login', {
        'template_name': 'accounts/login.html'}, name='login'),
    url(r'^logout/?$', 'accounts.views.logout_view', name='logout'),
)

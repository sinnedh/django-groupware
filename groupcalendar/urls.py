from django.conf import settings
from django.conf.urls.static import static

from django.conf.urls import patterns, include, url

from groupcalendar.views import EventDetail, EventCreate, EventUpdate, EventDelete
from groupcalendar.views import CalendarList, CalendarDetail, CalendarCreate, CalendarUpdate, CalendarDelete

#from django.contrib import admin
#admin.autodiscover()

urlpatterns = patterns('',
    # TODO:  add to calender urls file
    url(r'^$', 'groupcalendar.views.actual_day', name='home'),

    url(r'^day$', 'groupcalendar.views.actual_day', name='day'),
    url(r'^day/(?P<year>\d+)/(?P<month>\d+)/(?P<day>\d+)$', 'groupcalendar.views.day', name='day'),

    url(r'^week$', 'groupcalendar.views.actual_week', name='week'),
    url(r'^week/(?P<year>\d+)/(?P<week>\d+)$', 'groupcalendar.views.week', name='week'),

    url(r'^month$', 'groupcalendar.views.actual_month', name='month'),
    url(r'^month/(?P<year>\d+)/(?P<month>\d+)$', 'groupcalendar.views.month', name='month'),


    url(r'event/(?P<pk>\d+)/detail/$', EventDetail.as_view(), name='event_detail'),
    url(r'event/add/$', EventCreate.as_view(), name='event_add'),
    url(r'event/add/(?P<year>\d+)/(?P<month>\d+)/(?P<day>\d+)/$', EventCreate.as_view(), name='event_add'),
    url(r'event/add/(?P<year>\d+)/(?P<month>\d+)/(?P<day>\d+)/(?P<hour>\d+)/$', EventCreate.as_view(), name='event_add'),
    url(r'event/(?P<pk>\d+)/$', EventUpdate.as_view(), name='event_update'),
    url(r'event/(?P<pk>\d+)/delete/$', EventDelete.as_view(), name='event_delete'),

    url(r'calendar/$', CalendarList.as_view(), name='calendar_list'),
    url(r'calendar/(?P<pk>\d+)/detail/$', CalendarDetail.as_view(), name='calendar_detail'),
    url(r'calendar/add/$', CalendarCreate.as_view(), name='calendar_add'),
    url(r'calendar/(?P<pk>\d+)/$', CalendarUpdate.as_view(), name='calendar_update'),
    url(r'calendar/(?P<pk>\d+)/delete/$', CalendarDelete.as_view(), name='calendar_delete'),

    url(r'^week_test$', 'groupcalendar.views.week_test', name='week_test'),
)

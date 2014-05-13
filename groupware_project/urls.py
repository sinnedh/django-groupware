from django.conf import settings
from django.conf.urls.static import static

from django.conf.urls import patterns, include, url


#from django.contrib import admin
#admin.autodiscover()

urlpatterns = patterns('',

    # TODO:  add to calender urls file
    url(r'^groupcalendar/', include('groupcalendar.urls', namespace='groupcalendar')),
    url(r'^groupcontacts/', include('groupcontacts.urls', namespace='groupcontacts')),
#    url(r'^blog/', include('blog.urls')),
#    url(r'^admin/', include(admin.site.urls)),
#    static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
)

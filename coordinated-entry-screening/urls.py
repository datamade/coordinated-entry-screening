from django.conf.urls import include, url
from django.contrib import admin
from django.conf import settings

from rapidsms import views as rapidsms_views
from profiler.views import profile_twilio_backend

admin.autodiscover()

urlpatterns = [
    url(r'^profile-twilio-backend/', profile_twilio_backend, name='profile_twilio_backend'),
    url(r'^admin/', admin.site.urls),

    # RapidSMS core URLs
    url(r'^accounts/', include('rapidsms.urls.login_logout')),
    url(r'^$', rapidsms_views.dashboard, name='rapidsms-dashboard'),

    # RapidSMS contrib app URLs
    url(r'^httptester/', include('rapidsms.contrib.httptester.urls')),
    url(r'^messagelog/', include('rapidsms.contrib.messagelog.urls')),
    url(r'^messaging/', include('rapidsms.contrib.messaging.urls')),
    url(r'^registration/', include('rapidsms.contrib.registration.urls')),

    # Third party URLs
    url(r'^selectable/', include('selectable.urls')),
    url(r'^surveys/', include('decisiontree.urls')),
    url(r'^backend/twilio/', include('rtwilio.urls')),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
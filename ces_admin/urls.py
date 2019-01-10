from django.conf.urls import url
from django.contrib.auth.decorators import login_required

from ces_admin.views import ces_login, ces_logout, pong
from ces_admin.views import DashboardView

urlpatterns = [
    url(r'^ces-login/$', ces_login, name='ces_login'),
    url(r'^ces-logout/$', ces_logout, name='ces_logout'),
    url(r'^dashboard/$', login_required(DashboardView.as_view(), login_url='/ces-login/'), name='dashboard'),
    url(r'^pong/$', pong,),
]
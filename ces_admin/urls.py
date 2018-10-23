from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^ces-login/$', views.ces_login, name='ces_login'),
    url(r'^ces-logout/$', views.ces_logout, name='ces_logout'),
    url(r'^ces-admin/$', views.ces_admin, name='ces_admin'),
]
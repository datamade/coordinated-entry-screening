from django.conf.urls import url
from django.views.generic import TemplateView

from .views import IndexView

urlpatterns = [
    url(r'^$', IndexView.as_view(), name='index'),
    url(r'^about/$', TemplateView.as_view(template_name="ces_client/about.html"), name='about'),
    url(r'^contact/$', TemplateView.as_view(template_name="ces_client/contact.html"), name='contact'),
]

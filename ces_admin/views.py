from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render
from django.views.generic.base import TemplateView

from .mixins import DashboardContextMixin


def ces_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            if user is not None:
                login(request, user)
                return HttpResponseRedirect(reverse('dashboard'))
    else:
        form = AuthenticationForm()
    return render(request, 'ces_admin/ces-login.html', {'form': form})

def ces_logout(request):
    logout(request)
    return HttpResponseRedirect('/')

class DashboardView(DashboardContextMixin, TemplateView):
    template_name = 'ces_admin/ces-dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context.update(self.sessions_in_progress())
        context.update(self.canceled_sessions_chart())
        context.update(self.canceled_sessions_numbers())
        context.update(self.completed_sessions_chart())
        context.update(self.completed_sessions_numbers())
        context.update(self.recommendations())
        
        return context

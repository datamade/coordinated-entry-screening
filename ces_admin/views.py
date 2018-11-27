from collections import namedtuple
import json
import datetime

from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render
from django.db import connection
from django.db.models import Q
from django.views.generic.base import TemplateView

from decisiontree.models import Session

from .utils import prepare_data


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

class DashboardContextMixin(object):
    query_for_session_data = '''
        SELECT message.text, count(state.name) as count, state.name
        FROM decisiontree_session as session
        JOIN decisiontree_treestate as state
        ON session.{state_type}=state.id
        JOIN decisiontree_message as message
        ON state.message_id=message.id
        {where_clause}
        GROUP BY state.name, message.text
        ORDER BY count DESC
    '''

    one_day_ago = datetime.datetime.now() - datetime.timedelta(days=1)

    def sessions_in_progress(self):
        '''
        This function gets context data for sessions that are "in progress,"
        i.e., not canceled, not completed, and opened in the last 24 hours.
        '''
        context = {}

        with connection.cursor() as cursor:
            context['open_sessions'] = Session.objects.filter(state_id__isnull=False, last_modified__gte=self.one_day_ago).count()

            query = self.query_for_session_data.format(state_type='state_id',
                                                       where_clause='''WHERE session.state_id is not null
                                                                       AND session.last_modified >= (NOW() - INTERVAL '24 hour')''')

            _, open_sessions_map = prepare_data(cursor, query)
            context['open_sessions_map'] = open_sessions_map

        return context

    def canceled_sessions(self):
        '''
        This function gets context data for sessions that the user either canceled (e.g., by typing "end")
        or abandoned 24 hours after starting.
        '''
        context = {}

        with connection.cursor() as cursor:
            context['canceled_sessions'] = Session.objects.filter(Q(state_id__isnull=True, canceled=True) | Q(state_id__isnull=False, last_modified__lt=self.one_day_ago)).count()

            query = self.query_for_session_data.format(state_type='state_at_close_id',
                                                       where_clause='''WHERE (session.state_id is null
                                                                       AND session.canceled=True)
                                                                       OR (session.state_id is not null
                                                                       AND session.last_modified < (NOW() - INTERVAL '24 hour'))''')


            canceled_sessions_chart, canceled_sessions_map = prepare_data(cursor, query)
            context['canceled_sessions_chart'] = canceled_sessions_chart
            context['canceled_sessions_map'] = canceled_sessions_map

        return context

    def completed_sessions(self):
        '''
        This function gets context data for sessions that the user completed
        by answering all relevant questions in the survey
        '''
        context = {}

        with connection.cursor() as cursor:
            context['completed_sessions'] = Session.objects.filter(state_id__isnull=True, canceled=False).count()

            query = self.query_for_session_data.format(state_type='state_at_close_id',
                                                       where_clause='''WHERE session.state_id is null
                                                                       AND session.canceled=False''')

            completed_sessions_chart, completed_sessions_map = prepare_data(cursor, query)
            context['completed_sessions_chart'] = completed_sessions_chart
            context['completed_sessions_map'] = completed_sessions_map

        return context

    def recommendations(self):
        '''
        This function returns data for the all resources recommended (regardless of session type).
        '''
        context = {}

        with connection.cursor() as cursor:
            query_for_recommendation_chart = '''
                SELECT message.text, count(message.text) as count, state.name
                FROM decisiontree_session as session
                JOIN decisiontree_entry as entry
                ON session.id = entry.session_id
                JOIN decisiontree_transition as transition
                ON transition.id = entry.transition_id
                JOIN decisiontree_treestate as state
                ON state.id = transition.next_state_id
                JOIN decisiontree_message as message
                ON message.id = state.message_id
                WHERE message.recommendation=True
                GROUP BY message.text, state.name
                ORDER BY count DESC
            '''
            resources_chart, resources_map = prepare_data(cursor, query_for_recommendation_chart, False)
            context['resources_chart'] = resources_chart
            context['resources_map'] = resources_map

        return context

class DashboardView(DashboardContextMixin, TemplateView):
    template_name = 'ces_admin/ces-dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context.update(self.sessions_in_progress())
        context.update(self.canceled_sessions())
        context.update(self.completed_sessions())
        context.update(self.recommendations())

        return context

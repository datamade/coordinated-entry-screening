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

class DashboardView(TemplateView):
    template_name = 'ces_admin/ces-dashboard.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        base_query = '''
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

        with connection.cursor() as cursor:
            # Sessions that are in progress
            context['open_sessions'] = Session.objects.filter(state_id__isnull=False, last_modified__gte=one_day_ago).count()

            query_chart = base_query.format(state_type='state_id',
                                            where_clause="WHERE session.state_id is not null " +
                                                         "AND session.last_modified >= (NOW() - INTERVAL '24 hour')")

            open_sessions_chart, open_sessions_map = prepare_data(cursor, query_chart)
            context['open_sessions_chart'] = json.dumps(open_sessions_chart)
            context['open_sessions_map'] = json.dumps(open_sessions_map)

            # Sessions that the user either canceled (e.g., by typing "end") or abandoned 24 hours after starting.
            context['canceled_sessions'] = Session.objects.filter(Q(state_id__isnull=True, canceled=True) | Q(state_id__isnull=False, last_modified__lt=one_day_ago)).count()

            query_chart = base_query.format(state_type='state_at_close_id',
                                            where_clause="WHERE (session.state_id is null " +
                                                         "AND session.canceled=True) " +
                                                         "OR (session.state_id is not null " +
                                                         "AND session.last_modified < (NOW() - INTERVAL '24 hour'))")

            canceled_sessions_chart, canceled_sessions_map = prepare_data(cursor, query_chart)
            context['canceled_sessions_chart'] = json.dumps(canceled_sessions_chart)
            context['canceled_sessions_map'] = json.dumps(canceled_sessions_map)

            # Sessions that the user completed, e.g., by answering all questions in the survey
            context['completed_sessions'] = Session.objects.filter(state_id__isnull=True, canceled=False).count()

            query_chart = base_query.format(state_type="state_at_close_id",
                                            where_clause="WHERE session.state_id is null " +
                                                         "AND session.canceled=False")

            completed_sessions_chart, completed_sessions_map = prepare_data(cursor, query_chart)
            context['completed_sessions_chart'] = json.dumps(completed_sessions_chart)
            context['completed_sessions_map'] = json.dumps(completed_sessions_map)

            # Recommendations
            query_chart = '''
                SELECT message.text, count(message.text) as count, state.name 
                FROM decisiontree_session as session 
                JOIN decisiontree_entry as entry 
                ON session.id=entry.session_id 
                JOIN decisiontree_transition as transition 
                ON transition.id=entry.transition_id 
                JOIN decisiontree_treestate as state 
                ON state.id=transition.next_state_id 
                JOIN decisiontree_message as message 
                ON message.id=state.message_id
                WHERE message.recommendation=True
                GROUP BY message.text, state.name
                ORDER BY count DESC
            '''
            resources_chart, resources_map = prepare_data(cursor, query_chart)
            context['resources_chart'] = json.dumps(resources_chart)
            context['resources_map'] = json.dumps(resources_map)           

        return context
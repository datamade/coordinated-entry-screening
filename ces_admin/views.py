from collections import namedtuple

from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render
from django.db import connection

from decisiontree.models import Session

from .utils import make_namedtuple


def ces_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            if user is not None:
                login(request, user)
                return HttpResponseRedirect(reverse('ces_admin'))
    else:
        form = AuthenticationForm()
    return render(request, 'ces_admin/ces-login.html', {'form': form})

def ces_logout(request):
    logout(request)
    return HttpResponseRedirect('/')

@login_required(login_url='/ces-login/')
def ces_admin(request):
    with connection.cursor() as cursor:
        base_query = '''
            SELECT session.start_date, session.last_modified, message.text
            FROM decisiontree_session as session
            JOIN decisiontree_treestate as state
            ON session.{state_type}=state.id
            JOIN decisiontree_message as message
            ON state.message_id=message.id
            {where_clause}
        '''

        # Sessions that are in progress
        query_open_sessions = base_query.format(state_type='state_id',
                                                where_clause='WHERE session.state_id is not null')
        open_sessions = make_namedtuple(cursor, query_open_sessions)

        # Sessions that the user completed, e.g., by answering all questions in the survey
        query_closed_sessions = base_query.format(state_type='state_at_close_id',
                                                  where_clause='WHERE session.state_id is null ' +
                                                               'AND session.canceled=False')
        closed_sessions = make_namedtuple(cursor, query_closed_sessions)


        # Sessions that the user canceled, e.g., by typing "end"
        query_canceled_sessions = base_query.format(state_type='state_at_close_id',
                                                    where_clause='WHERE session.state_id is null ' +
                                                                 'AND session.canceled=True')
        canceled_sessions = make_namedtuple(cursor, query_canceled_sessions)


    return render(request, 'ces_admin/ces-dashboard.html', {
            'open_sessions': open_sessions,
            'closed_sessions': closed_sessions,
            'canceled_sessions': canceled_sessions,
        })
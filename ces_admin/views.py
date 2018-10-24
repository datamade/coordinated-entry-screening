from collections import namedtuple

from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render
from django.db import connection

from decisiontree.models import Session


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
        query_open_sessions ='''
            SELECT session.start_date, session.last_modified, message.text
            FROM decisiontree_session as session
            JOIN decisiontree_treestate as state
            ON session.state_id=state.id
            JOIN decisiontree_message as message
            ON state.message_id=message.id 
            WHERE session.canceled is not True
        '''
        
        cursor.execute(query_open_sessions)
        fields = cursor.description
        nt_result = namedtuple('Session', [col[0] for col in fields])
        open_sessions = [nt_result(*row) for row in cursor.fetchall()]

    return render(request, 'ces_admin/ces-dashboard.html', {
            "open_sessions": open_sessions,
        })
import pytest
import json

from django.urls import reverse

from ces_admin.utils import prepare_data

def test_open_web_sessions(auth_client, db_setup):
    '''
    This tests for "web sessions" (and the other that follow) use 
    the db_setup fixture, which instantiates a database with
    one of each type of web session. 
    '''
    response = _get_dashboard_helper(auth_client)
    assert response.context['web_open_sessions'] == 1

def test_canceled_web_sessions(auth_client, db_setup):
    response = _get_dashboard_helper(auth_client)
    assert response.context['web_canceled_sessions'] == 1

def test_completed_web_sessions(auth_client, db_setup):
    response = _get_dashboard_helper(auth_client)
    assert response.context['web_completed_sessions'] == 1

def test_open_sms_sessions(auth_client, sms_connection, session):
    response = _get_dashboard_helper(auth_client)
    assert response.context['sms_open_sessions'] == 0 

    session_info = { 'connection_id': sms_connection.id }
    session.build(**session_info)
    response = _get_dashboard_helper(auth_client)
    assert response.context['sms_open_sessions'] == 1 

def test_canceled_sms_sessions(auth_client, sms_connection, session):
    response = _get_dashboard_helper(auth_client)
    assert response.context['sms_canceled_sessions'] == 0 

    session_info = { 
        'connection_id': sms_connection.id,
        'canceled': True,
        'state_id': None,
    }
    session.build(**session_info)
    response = _get_dashboard_helper(auth_client)
    assert response.context['sms_canceled_sessions'] == 1

def test_completed_sms_sessions(auth_client, sms_connection, session):
    response = _get_dashboard_helper(auth_client)
    assert response.context['sms_completed_sessions'] == 0 

    session_info = { 
        'connection_id': sms_connection.id,
        'canceled': False,
        'state_id': None,
    }
    session.build(**session_info)
    response = _get_dashboard_helper(auth_client)
    assert response.context['sms_completed_sessions'] == 1

def _get_dashboard_helper(auth_client):
    url = reverse('dashboard')
    response = auth_client.get(url)

    assert response.status_code == 200

    return response
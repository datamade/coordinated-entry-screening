import pytest

from django.urls import reverse

from ces_admin.utils import prepare_data

def test_open_sessions(auth_client, db_setup):
    response = _get_dashboard_helper(auth_client)
    assert response.context['open_sessions'] == 1

def test_canceled_sessions(auth_client, db_setup):
    response = _get_dashboard_helper(auth_client)
    assert response.context['canceled_sessions'] == 1

def test_completed_sessions(auth_client):
    response = _get_dashboard_helper(auth_client)

    assert response.context['completed_sessions'] == 0

def _get_dashboard_helper(auth_client):
    url = reverse('dashboard')
    response = auth_client.get(url)

    assert response.status_code == 200

    return response
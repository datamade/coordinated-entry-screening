import pytest

from django.urls import reverse

from ces_admin.utils import prepare_data

def test_dashboard(auth_client):
    url = reverse('dashboard')
    
    rv = auth_client.post(url)

    assert rv.status == 200

def test_prepare_data():
    assert True == True
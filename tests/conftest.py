import pytest

from pytest_django.fixtures import db
from django.contrib.auth.models import User

@pytest.fixture
@pytest.mark.django_db
def auth_client(db, client):
    User.objects.create_user(username='admin', password='password')
    client.login(username='admin', password='password')
    
    return client
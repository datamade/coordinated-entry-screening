import pytest
from random import randrange
from datetime import datetime, timedelta

from pytest_django.fixtures import db

from django.contrib.auth.models import User
from rapidsms.models import Connection, Backend
from decisiontree.models import Session, TreeState, Message, Tree

@pytest.fixture
@pytest.mark.django_db
def db_setup(db, session):
    '''
    Populate the database with one open, canceled, and completed session.
    '''
    open_session = {
        'last_modified': (datetime.now() - timedelta(hours=5)),
    }

    session.build(**open_session)

    canceled_session = {
        'canceled': True,
        'state_id': None,
    }

    session.build(**canceled_session)


@pytest.fixture
@pytest.mark.django_db
def auth_client(db, client):
    User.objects.create_user(username='admin', password='password')
    client.login(username='admin', password='password')
    
    return client

@pytest.fixture
@pytest.mark.django_db
def message(db):
    message_info = {
        'id': 1, 
        'text': 'How old are you?',
    }

    message = Message.objects.create(**message_info)
    message.save()

    return message

@pytest.fixture
@pytest.mark.django_db
def tree_state(db, message):
    state_info = {
        'id': 1, 
        'name': 'age question',
        'message_id': message.id,
    }

    state = TreeState.objects.create(**state_info)
    state.save()

    return state

@pytest.fixture
@pytest.mark.django_db
def tree(db, tree_state):
    tree_info = {
        'id': 1, 
        'summary': 'CES survey',
        'trigger': 'start',
        'root_state_id': tree_state.id,
    }

    tree = Tree.objects.create(**tree_info)
    tree.save()

    return tree

@pytest.fixture
@pytest.mark.django_db
def connection(db, message):
    backend = Backend.objects.create(name='twilio-backend')

    connection_info = {
        'id': 1, 
        'created_on': '2018-08-15 16:10:32.180409-05',
        'backend_id': backend.id,
    }

    connection = Connection.objects.create(**connection_info)
    connection.save()

    return connection

@pytest.fixture
@pytest.mark.django_db
def session(db, tree_state, connection, tree):
    class SessionFactory():
        def build(self, **kwargs):
            session_info = {
                'id': randrange(1000000),
                'last_modified': '2018-10-26 13:14:29.629877-05', 
                'state_id': tree_state.id,
                'tree_id': tree.id,
                'num_tries': 0,
                'connection_id': connection.id,
            }

            session_info.update(**kwargs)

            session = Session.objects.create(**session_info)
            session.save()

            return session 

    return SessionFactory()

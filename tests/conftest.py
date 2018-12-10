import pytest
from random import randrange
from datetime import datetime, timedelta

from pytest_django.fixtures import db

from django.contrib.auth.models import User
from rapidsms.models import Connection, Backend
from rapidsms.messages.incoming import IncomingMessage
from decisiontree.models import Session, TreeState, Message, Tree, Transition, Answer

@pytest.fixture
@pytest.mark.django_db
def db_setup(db, session):
    '''
    Populate the database with one open, canceled, and completed web session.
    '''
    initial_session = session.build() # Default session fixture creates an on open session

    canceled_session = {
        'canceled': True,
        'state_id': None,
        'state_at_close': initial_session.state,
    }
    session.build(**canceled_session)

    completed_session = {
        'canceled': False,
        'state_id': None,
        'state_at_close': initial_session.state,
    }
    session.build(**completed_session)

@pytest.fixture
@pytest.mark.django_db
def session(db, tree_state, web_connection, tree):
    class SessionFactory():
        def build(self, **kwargs):
            '''
            This creates an "open" session.
            '''
            state = tree_state.build()

            session_info = {
                'id': randrange(1000000),
                'last_modified': (datetime.now() - timedelta(hours=5)), 
                'state_id': state.id,
                'tree_id': tree.id,
                'num_tries': 0,
                'connection_id': web_connection.id,
            }

            session_info.update(**kwargs)

            session = Session.objects.create(**session_info)

            return session 

    return SessionFactory()

@pytest.fixture
@pytest.mark.django_db
def auth_client(db, client):
    User.objects.create_user(username='admin', password='password')
    client.login(username='admin', password='password')
    
    return client

@pytest.fixture
@pytest.mark.django_db
def message(db):
    class MessageFactory():
        def build(self, **kwargs):

            message_info = {
                'id': 1, 
                'text': 'Hi there. Glad to hear from you! \
                         Type "1" to get started.',
            }

            message_info.update(**kwargs)

            message, _ = Message.objects.get_or_create(**message_info)

            return message

    return MessageFactory()

@pytest.fixture
def incoming_message(db, web_connection):
    '''
    Factory for instantiating an IncomingMessage, i.e., the message
    from the user, which gets sent to the app (...or B.E.N.).
    '''
    class IncomingMessageFactory():
        def build(self, **kwargs):

            message_info = {
                'text': 'connect',
                'connection': web_connection
            }

            incoming_message = IncomingMessage(**message_info)

            return incoming_message

    return IncomingMessageFactory()

@pytest.fixture
@pytest.mark.django_db
def tree_state(db, message):
    class TreeStateFactory():
        def build(self, **kwargs):
            msg = message.build()
            state_info = {
                'id': 1, 
                'name': 'welcome',
                'message_id': msg.id,
            }

            state_info.update(**kwargs)

            state, _ = TreeState.objects.get_or_create(**state_info)

            return state

    return TreeStateFactory()

@pytest.fixture
@pytest.mark.django_db
def transition(db, tree_state, message):
    '''
    This fixture builds a transition.
    https://github.com/datamade/rapidsms-decisiontree-app/blob/master/decisiontree/models.py#L181
    
    This transition moves the user from the welcome message 
    (i.e., 'Hi there. Glad to hear from you! Type "1" to get started.') 
    to the first survey question (see below).

    The user would make this transition by typing "1" 
    (see `answer_to_move_between_states` below).
    '''
    current_state = tree_state.build()

    next_message_info = {
        'id': 2,
        'text': 'First, I need to know where you are. \
                 Are you in the city or the suburbs? Type 1 or 2.',
    }
    next_message = message.build(**next_message_info)
    next_state_info = {
        'id': 2, 
        'name': 'location',
        'message_id': next_message.id,
    }
    next_state = tree_state.build(**next_state_info)

    answer_to_move_between_states = Answer.objects.create(answer='1', type='A')

    transition_info = {
        'id': 1,
        'current_state': current_state,
        'next_state': next_state,
        'answer': answer_to_move_between_states
    }
    transition = Transition.objects.create(**transition_info)

    return transition

@pytest.fixture
@pytest.mark.django_db
def tree(db, tree_state):
    state = tree_state.build()

    tree_info = {
        'id': 1, 
        'summary': 'CES survey',
        'trigger': 'connect',
        'root_state_id': state.id,
    }

    tree = Tree.objects.create(**tree_info)

    return tree

@pytest.fixture
@pytest.mark.django_db
def sms_connection(db):
    backend = Backend.objects.create(name='twilio-backend')

    connection_info = {
        'id': 1, 
        'created_on': '2018-08-15 16:10:32.180409-05',
        'backend_id': backend.id,
        'identity': '+19998887777'
    }

    connection = Connection.objects.create(**connection_info)

    return connection

@pytest.fixture
@pytest.mark.django_db
def web_connection(db):
    backend = Backend.objects.create(name='fake-backend')

    connection_info = {
        'id': 2, 
        'created_on': '2018-09-15 16:10:32.180409-05',
        'backend_id': backend.id,
        'identity': 'web-5na9276lkul6etdtxnrzep7dihfzql0w'
    }

    connection = Connection.objects.create(**connection_info)

    return connection

from datetime import datetime, timedelta
from mock import patch

from django.core.management import call_command

from decisiontree.models import Session


def test_hash_closed_session(sms_connection, session):
    last_modified = datetime.now() - timedelta(hours=1)

    with patch('django.utils.timezone.now', return_value=last_modified):
        session_info = { 
            'connection_id': sms_connection.id, 
            'state_id': None,
        }
        sms_session = session.build(**session_info)

        assert sms_session.connection.identity == '+19998887777'

        call_command('hash_identities')
        sms_session.connection.refresh_from_db()
        
        assert sms_session.connection.identity != '+19998887777'


def test_hash_abandoned_session(sms_connection, session):
    last_modified = datetime.now() - timedelta(hours=25)

    with patch('django.utils.timezone.now', return_value=last_modified):
        session_info = { 'connection_id': sms_connection.id }
        sms_session = session.build(**session_info)

        assert sms_session.connection.identity == '+19998887777'

        call_command('hash_identities')
        sms_session.connection.refresh_from_db()
        
        assert sms_session.connection.identity != '+19998887777'

def test_hash_open_session(sms_connection, session):
    last_modified = datetime.now() - timedelta(hours=1)

    with patch('django.utils.timezone.now', return_value=last_modified):
        session_info = { 'connection_id': sms_connection.id }
        sms_session = session.build(**session_info)

        assert sms_session.connection.identity == '+19998887777'

        call_command('hash_identities')
        sms_session.connection.refresh_from_db()
        
        assert sms_session.connection.identity == '+19998887777'

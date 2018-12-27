import pytest
from datetime import datetime, timedelta
from mock import patch

from django.core.management import call_command

from rapidsms.models import Connection
from decisiontree.models import Session


@pytest.mark.parametrize('hours,state_id', [
    (1, None),
    (25, 1),
])
def test_hash_closed_session(hours, state_id, sms_connection, session):
    '''
    Test that the script hashes closed (state_id of None) 
    and abandoned sessions (last_modified more than 24 hours ago).
    '''
    last_modified = datetime.now() - timedelta(hours=hours)

    with patch('django.utils.timezone.now', return_value=last_modified):
        session_info = { 
            'connection_id': sms_connection.id, 
            'state_id': state_id,
        }
        sms_session = session.build(**session_info)

        assert sms_session.connection.identity == '+19998887777'

        call_command('hash_identities')
        sms_session.connection.refresh_from_db()
        
        assert sms_session.connection.identity != '+19998887777'

def test_hash_open_session(sms_connection, session):
    '''
    Test that the script does NOT hash open sessions.
    '''
    last_modified = datetime.now() - timedelta(hours=1)

    with patch('django.utils.timezone.now', return_value=last_modified):
        session_info = { 'connection_id': sms_connection.id }
        sms_session = session.build(**session_info)

        assert sms_session.connection.identity == '+19998887777'

        call_command('hash_identities')
        sms_session.connection.refresh_from_db()
        
        assert sms_session.connection.identity == '+19998887777'

def test_hash_web_session(db_setup):
    '''
    Test that the script does NOT hash web sessions. 
    '''
    web_sessions = Session.objects.filter(connection__identity__startswith='web')

    for session in web_sessions:
        identity_before_running_command = session.connection.identity
        call_command('hash_identities')
        session.connection.refresh_from_db()
        
        assert session.connection.identity == identity_before_running_command
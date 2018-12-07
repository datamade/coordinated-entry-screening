import pytest

from django.conf import settings

from ces_client.utils import WebRouter

def test_make_answers(transition):
    '''
    Test that make_answers returns a list of dictionaries 
    with an option to continue ("1") and an option to exit (i.e., the end trigger).
    ''' 
    web_router = WebRouter()
    answers = web_router.make_answers(transition.current_state)

    assert any(dict['value'] == '1' for dict in answers)
    assert any(dict['value'] == settings.DECISIONTREE_SESSION_END_TRIGGER for dict in answers)

def test_find_user_state(db_setup, incoming_message):
    '''
    This test uses the three session in `db_setup`, which includes three sessions, created in 
    the order: open, canceled, completed. All sessions do not go beyond the "welcome" state.

    Test that find_user_state returns the "welcome" state and flags it as a closing state.
    '''
    web_router = WebRouter()
    msg = incoming_message.build()

    state, closing_state = web_router.find_user_state(msg)

    assert state.name == "welcome"
    assert closing_state == True

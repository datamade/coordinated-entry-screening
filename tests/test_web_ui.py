import pytest
import json

from django.urls import reverse

def test_get_index(auth_client):
    url = reverse('index')
    response = auth_client.get(url)

    assert response.status_code == 200

def test_first_question(auth_client, tree, transition):
    '''
    Test that the app effectively moves the user from 
    one question to another via a valid answer.
    '''
    _start_tree(auth_client, tree)
    url = reverse('index')
    response = auth_client.post(url, {'user_input': '1'})

    assert response.status_code == 200

    message_from_ben = json.loads(response.content.decode('utf-8'))['text'].replace('\n', '')

    assert transition.next_state.message.text == message_from_ben

def _start_tree(auth_client, tree):
    url = reverse('index')
    response = auth_client.post(url, {'user_input': 'start'})

    assert response.status_code == 200

    message_from_ben = json.loads(response.content.decode('utf-8'))['text'].replace('\n', '')

    assert tree.root_state.message.text in message_from_ben

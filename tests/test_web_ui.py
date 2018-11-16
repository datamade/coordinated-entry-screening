import pytest
import json

from django.urls import reverse

def test_get_index(auth_client):
    url = reverse('index')
    response = auth_client.get(url)

    assert response.status_code == 200

def test_first_question(auth_client, tree):
    _start_tree(auth_client, tree)

    url = reverse('index')
    response = auth_client.post(url, {'user_input': '1'})

    assert response.status_code == 200

    # TODO: Make a transition
    message_from_ben = json.loads(response.content.decode('utf-8'))['text'].replace('\n', '')


def _start_tree(auth_client, tree):
    url = reverse('index')
    response = auth_client.post(url, {'user_input': 'start'})

    assert response.status_code == 200

    message_from_ben = json.loads(response.content.decode('utf-8'))['text'].replace('\n', '')

    assert message_from_ben == tree.root_state.message.text

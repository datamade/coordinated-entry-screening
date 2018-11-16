import json


from django.shortcuts import render
from django.views import View
from django.test.utils import override_settings
from django.http import HttpResponse

from rapidsms.messages.incoming import IncomingMessage
from rapidsms.models import Connection, Backend
from rapidsms.tests.harness import MockRouter

from decisiontree import conf
from decisiontree.models import Session 
from decisiontree.app import App


class IndexView(View):
    template_name = "ces_client/index.html"
    registered_functions = {}
    session_listeners = {}

    def get(self, request, *args, **kwargs):
        # Delete the session key, if the user refreshes the page.
        request.session.flush()
        request.session.cycle_key()

        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        
        backend, _ = Backend.objects.get_or_create(name='fake-backend')
        identity = 'web-{}'.format(request.session.session_key)
        connection, _ = Connection.objects.get_or_create(identity=identity, backend=backend)

        message_from_ben = None

        user_input = request.POST.get('user_input')
        if user_input:
            msg = IncomingMessage(text=user_input, connection=connection)
            message_from_ben = self._create_msg_from_ben(msg)

        return HttpResponse(
            json.dumps({"text": message_from_ben}),
            content_type="application/json"
        )

    def _create_msg_from_ben(self, msg):
        decision_app = App(router=MockRouter())
        # The app evaluates to True (if it can send a message), or False (if it does not).
        # If False, then the user did not enter valid input, i.e., a trigger word for a state.
        # When False, send an "invalid message" warning of some sort.
        if decision_app.handle(msg):
            sessions = msg.connection.session_set.all().select_related('state')
            session = sessions.latest('start_date')
            state = session.state 
            if not state:
                state = session.state_at_close 

            return decision_app._concat_answers(state.message.text, state)
        else:
            return 'I am sorry. I do not understand.'

import datetime
import logging
import re

from django.http import HttpResponse
from django.shortcuts import render
from django.utils.translation import ugettext as _
from django.views import View

from rapidsms.apps.base import AppBase
from rapidsms.messages import OutgoingMessage, IncomingMessage
from rapidsms.messages.incoming import IncomingMessage
from rapidsms.models import Connection

from decisiontree import conf
from decisiontree.models import Entry, Session, TagNotification, Transition
from decisiontree.signals import session_end_signal
from decisiontree.utils import get_survey
from decisiontree.app import App


logger = logging.getLogger(__name__)

class IndexView(View):
    template_name = "ces_client/index.html"
    registered_functions = {}
    session_listeners = {}

    def get(self, request, *args, **kwargs):
        # A valid IncomingMessage needs: (1) text, and (2) a connection.
        # A connection needs: contact=self.contact, backend=self.backend, identity='1112223333'.
        from rapidsms.models import Connection
        connection = Connection(identity='web-interface')
        # The message text will be whatever the user submits via a form.
        msg = IncomingMessage(text='start', connection=connection)

        # Do we need a real router?
        from rapidsms.tests.harness import MockRouter
        decision_app = App(router=MockRouter())

        # What happens after calling `handle`? This function returns True or False,
        # after processing the message. How can we get the response text?
        decision_app.handle(msg)

        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):

        return render(request, self.template_name)

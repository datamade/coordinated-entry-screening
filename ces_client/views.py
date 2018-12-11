import json

from django.shortcuts import render
from django.views import View
from django.test.utils import override_settings
from django.http import HttpResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import ensure_csrf_cookie

from rapidsms.messages.incoming import IncomingMessage
from rapidsms.models import Connection, Backend
from decisiontree import conf
from decisiontree.models import Session 

from .utils import WebRouter


class IndexView(View):
    template_name = "ces_client/index.html"
    registered_functions = {}
    session_listeners = {}
    web_router = WebRouter()

    @method_decorator(ensure_csrf_cookie)
    def get(self, request, *args, **kwargs):
        # Delete the session key, if the user refreshes the page.
        request.session.flush()
        request.session.cycle_key()

        return render(request, self.template_name)

    @method_decorator(ensure_csrf_cookie)
    def post(self, request, *args, **kwargs):
        backend, _ = Backend.objects.get_or_create(name='fake-backend')
        identity = 'web-{}'.format(request.session.session_key)
        connection, _ = Connection.objects.get_or_create(identity=identity, backend=backend)
        
        user_input = request.POST.get('user_input')
        msg = IncomingMessage(text=user_input, connection=connection)
        
        message_from_ben, answers = self.web_router.create_msg_from_ben(msg)

        return HttpResponse(
            json.dumps({"text": message_from_ben, 'answers': answers}),
            content_type="application/json",
        )

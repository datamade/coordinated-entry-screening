from django.conf import settings

from rapidsms.tests.harness import MockRouter
from decisiontree.models import Transition
from decisiontree.app import App

class WebRouter(App):
    def __init__(self):
        router = MockRouter()

    def create_msg_from_ben(self, msg):
        '''
        The text-messaging and web tool use the decisiontree-app to process incoming messages
        by creating and updating entries in the database, e.g., updating a Session:
        https://github.com/datamade/rapidsms-decisiontree-app/blob/master/decisiontree/app.py
        
        This function does the following:
        (1) instantiates an App, but does not direct data to Twilio (hence the mock router).
        (2) calls the `handle` function, which processes the user input.
        (3) determines how B.E.N. should respond, based on the user's input, session, and state.

        This function expects three types of responses from the user:
        (1) an answer to a question in the middle of a survey
        (2) an answer to a question at the end of a survey
        (3) a directive to exit the survey (i.e., by clicking the end triggger word, "Goodbye")
        '''
        super().handle(msg)

        answers = []
        
        if msg.text == settings.DECISIONTREE_SESSION_END_TRIGGER:
            return settings.DECISIONTREE_SESSION_END_MESSAGE, answers

        state, closing_state = self.find_user_state(msg)

        if not closing_state:
            text = state.message.text
            prepped_text = self.prep_text_for_botui(text)
            answers = self.make_answers(state)
            
            return prepped_text, answers
        else:
            # If the user does not have a closing_state, they completed the survey.
            # They should receive a list of resources and/or a "bye" message from B.E.N.
            prepped_text = self.prep_text_for_botui(state.message.text)
            return prepped_text, answers

    def find_user_state(self, msg):
        sessions = msg.connection.session_set.all().select_related('state')
        session = sessions.latest('start_date')
        state = session.state 
        closing_state = False

        if not state:
            state = session.state_at_close
            closing_state = True
        
        return state, closing_state

    def make_answers(self, state):
        answers = []
        transition_set = Transition.objects.filter(current_state=state).order_by('answer')

        for t in transition_set:
            answers.append({'text': t.answer.helper_text().replace('Type', 'Click'),
                            'value': t.answer.answer})
        
        answers.append({'text': 'Goodbye!',
                        'value': settings.DECISIONTREE_SESSION_END_TRIGGER})

        return answers

    @staticmethod
    def prep_text_for_botui(text):
        '''
        This function prepares the message text (as returned from the database)
        for the BotUI object (see: index.html and bot-utils.js).

        BotUI can handle html. So, this function replaces `\n` with 
        the `<br>` tag.

        The web interface also requires users to "click" rather than "type."
        This function changes the text accordingly.
        '''
        text_with_br = text.replace('\n', '<br>')
        prepped_text = text_with_br.replace('Type', 'Click')

        return prepped_text
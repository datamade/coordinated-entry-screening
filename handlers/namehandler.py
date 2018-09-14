#!/usr/bin/env python
from rapidsms.contrib.handlers.handlers.base import BaseHandler

from decisiontree.models import Transition, Entry
from decisiontree.utils import concat_answers

class NameHandler(BaseHandler):
    """
    Handle input for a question about the user's name. 
    The handler assumes that such a question includes the phrase "your name."
    The handler assumes that the user wants to opt-out of answering by typing "1."
    Note: the question for determining the user's name should not be the first one in the survey.
    """
    @classmethod
    def dispatch(cls, router, msg):
        sessions = msg.connection.session_set.open().select_related('state')
        session = sessions.latest('start_date')
        current_question = session.state.message.text
        
        if 'your name' in current_question.lower() and msg.text != '1':
            session.user_name = msg.text
            # Go to next state, i.e., the state achieved via the transition from hitting "1"
            transition = Transition.objects.get(current_state=session.state, answer__answer="1")
            session.state = transition.next_state
            session.save()
            # Create an entry
            last_entry = Entry.objects.filter(session=session).order_by('sequence_id').last()
            if last_entry:
                sequence = last_entry.sequence_id + 1
            entry = Entry.objects.create(session=session, sequence_id=sequence,
                                         transition=transition,
                                         text=msg.text)
            # Send a "thank you" response and a response with the next question.
            response = concat_answers(session.state.message.text, session.state)
            msg.respond('Great. Thank you for sharing, {}.'.format(msg.text))
            msg.respond(response)

            return True
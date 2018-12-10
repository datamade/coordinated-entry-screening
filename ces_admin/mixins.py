import datetime

from django.db import connection
from django.db.models import Q

from decisiontree.models import Session

from .utils import prepare_data

class DashboardContextMixin(object):
    query_for_session_data = '''
        SELECT message.text, count(state.name) as count, state.name
        FROM decisiontree_session as session
        JOIN decisiontree_treestate as state
        ON session.{state_type}=state.id
        JOIN decisiontree_message as message
        ON state.message_id=message.id
        JOIN rapidsms_connection as connection
        ON session.connection_id=connection.id
        {where_clause}
        GROUP BY state.name, message.text
        ORDER BY count DESC
    '''

    @property
    def one_day_ago(self):
        return datetime.datetime.now() - datetime.timedelta(days=1)

    @property
    def all_web_sessions(self):
        return Session.objects.filter(connection__identity__contains='web').count()

    @property
    def all_sms_sessions(self):
        return Session.objects.exclude(connection__identity__contains='web').count()

    def sessions_in_progress(self):
        '''
        This function gets the number of sessions that are "in progress,"
        i.e., not canceled, not completed, and opened in the last 24 hours.
        '''
        context = {}

        open_sessions = Session.objects.filter(state_id__isnull=False, last_modified__gte=self.one_day_ago)
        
        context['sms_open_sessions'] = open_sessions.exclude(connection__identity__contains='web').count()
        context['web_open_sessions'] = open_sessions.filter(connection__identity__contains='web').count()

        return context

    def canceled_sessions_chart(self):
        '''
        This function gets HighCharts data for sessions that the user either canceled (e.g., by typing "end")
        or abandoned 24 hours after starting.
        '''
        context = {}
        where_clause = '''WHERE ((session.state_id is null
                       AND session.canceled=True)
                       OR (session.state_id is not null
                       AND session.last_modified < (NOW() - INTERVAL '24 hour')))'''

        with connection.cursor() as cursor:
            #  Web
            web_where_clause = where_clause + " AND connection.identity LIKE 'web-%'"
            query = self.query_for_session_data.format(state_type='state_at_close_id',
                                                       where_clause=web_where_clause)

            web_canceled_sessions_chart, web_canceled_sessions_map = prepare_data(cursor, query)
            context['web_canceled_sessions_chart'] = web_canceled_sessions_chart
            context['web_canceled_sessions_map'] = web_canceled_sessions_map

            # SMS
            sms_where_clause = where_clause + " AND connection.identity NOT LIKE 'web-%'"
            query = self.query_for_session_data.format(state_type='state_at_close_id',
                                                       where_clause=sms_where_clause)

            sms_canceled_sessions_chart, sms_canceled_sessions_map = prepare_data(cursor, query)
            context['sms_canceled_sessions_chart'] = sms_canceled_sessions_chart
            context['sms_canceled_sessions_map'] = sms_canceled_sessions_map

        return context

    def canceled_sessions_numbers(self):
        context = {}
        # Count
        canceled_sessions = Session.objects.filter(Q(state_id__isnull=True, canceled=True) | \
                                                   Q(state_id__isnull=False, last_modified__lt=self.one_day_ago))
        
        context['sms_canceled_sessions'] = canceled_sessions.exclude(connection__identity__contains='web').count()
        context['web_canceled_sessions'] = canceled_sessions.filter(connection__identity__contains='web').count()

        # Percentage
        if self.all_web_sessions > 0:
            context['web_percentage_canceled'] = (context['web_canceled_sessions'] / self.all_web_sessions) * 100

        if self.all_sms_sessions > 0:
            context['sms_percentage_canceled'] = (context['sms_canceled_sessions'] / self.all_sms_sessions) * 100

        return context

    def completed_sessions_chart(self):
        '''
        This function gets context data for sessions that the user completed
        by answering all relevant questions in the survey
        '''
        context = {}
        where_clause='''WHERE session.state_id is null
                        AND session.canceled=False'''
        # Chart data
        with connection.cursor() as cursor:
            web_where_clause = where_clause + " AND connection.identity LIKE 'web-%'"
            query = self.query_for_session_data.format(state_type='state_at_close_id',
                                                       where_clause=web_where_clause)

            web_completed_sessions_chart, web_completed_sessions_map = prepare_data(cursor, query)
            context['web_completed_sessions_chart'] = web_completed_sessions_chart
            context['web_completed_sessions_map'] = web_completed_sessions_map

            sms_where_clause = where_clause + " AND connection.identity NOT LIKE 'web-%'"
            query = self.query_for_session_data.format(state_type='state_at_close_id',
                                                       where_clause=sms_where_clause)

            sms_completed_sessions_chart, sms_completed_sessions_map = prepare_data(cursor, query)
            context['sms_completed_sessions_chart'] = sms_completed_sessions_chart
            context['sms_completed_sessions_map'] = sms_completed_sessions_map

        return context

    def completed_sessions_numbers(self):
        context = {}
        # Count
        completed_sessions = Session.objects.filter(state_id__isnull=True, canceled=False)
        context['web_completed_sessions'] = completed_sessions.filter(connection__identity__contains='web').count()
        context['sms_completed_sessions'] = completed_sessions.exclude(connection__identity__contains='web').count()

        # Percentage
        if self.all_web_sessions > 0:
            context['web_percentage_complete'] = (context['web_completed_sessions'] / self.all_web_sessions) * 100

        if self.all_sms_sessions > 0:
            context['sms_percentage_complete'] = (context['sms_completed_sessions'] / self.all_sms_sessions) * 100

        return context

    def recommendations(self):
        '''
        This function returns data for the all resources recommended (regardless of session type).
        '''
        context = {}

        with connection.cursor() as cursor:
            query_for_recommendation_chart = '''
                SELECT message.text, count(message.text) as count, state.name
                FROM decisiontree_session as session
                JOIN decisiontree_entry as entry
                ON session.id = entry.session_id
                JOIN decisiontree_transition as transition
                ON transition.id = entry.transition_id
                JOIN decisiontree_treestate as state
                ON state.id = transition.next_state_id
                JOIN decisiontree_message as message
                ON message.id = state.message_id
                JOIN rapidsms_connection as connection
                ON session.connection_id=connection.id
                WHERE message.recommendation=True
                AND {type}
                GROUP BY message.text, state.name
                ORDER BY count DESC
            '''

            web_query = query_for_recommendation_chart.format(type="connection.identity LIKE 'web-%'")
            web_resources_chart, web_resources_map = prepare_data(cursor, web_query, False)
            context['web_resources_chart'] = web_resources_chart
            context['web_resources_map'] = web_resources_map

            sms_query = query_for_recommendation_chart.format(type="connection.identity NOT LIKE 'web-%'")
            sms_resources_chart, sms_resources_map = prepare_data(cursor, sms_query, False)
            context['sms_resources_chart'] = sms_resources_chart
            context['sms_resources_map'] = sms_resources_map

        return context

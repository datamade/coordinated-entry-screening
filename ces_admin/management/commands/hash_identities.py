import datetime
import hashlib

from django.core.management.base import BaseCommand
from django.db.models import Q
from  django.contrib.auth.hashers import make_password, check_password

from rapidsms.models import Connection
from decisiontree.models import Session

class Command(BaseCommand):
    help = '''
        This command hashes identities (i.e., phone numbers) of users
        who canceled, completed, or abandoned the survey.  
        '''

    def handle(self, *args, **options):
        # five_minutes_ago excludes sessions from the last five minutes, 
        # since Rapidsms and Twilio may have a communication delay, during which
        # our app still needs access to the unhashed phone number.   
        five_minutes_ago = datetime.datetime.now() - datetime.timedelta(minutes=5)
        one_day_ago = datetime.datetime.now() - datetime.timedelta(days=1)

        filter_for_canceled_or_completed = Q(session__state_id__isnull=True, \
                                             session__last_modified__lte=five_minutes_ago)
        filter_for_abandoned = Q(session__last_modified__lte=one_day_ago)

        # Use the `startswith` filter to exclude sessions that 
        # have already been hased or are websessions. 
        sms_connections = Connection.objects \
                                    .filter(filter_for_canceled_or_completed | filter_for_abandoned) \
                                    .filter(identity__startswith='+1') \
                                    .distinct()

        for connection in sms_connections:
            identity = connection.identity
            hashed_identity = make_password(identity)

            connection.identity = hashed_identity
            connection.save()

            self.stdout.write(self.style.SUCCESS('Successfully hashed identity'))
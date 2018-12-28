import csv

from django.core.management.base import BaseCommand

from decisiontree.models import Tree, TreeState

class Command(BaseCommand):
    help = '''
        Imports a CSV file (provided by CSH) to create Tree objects 
        with location-specific trigger words.

        Add the CSV file in the data directory, and run the command like this:

        `python manage.py port_location_codes <name_of_file>.csv`

        The command expects the database to have TreeState objects with the following names:
        (1) Welcome (city)
        (2) Welcome (suburbs)
        '''
    
    def add_arguments(self, parser):
        parser.add_argument('csvfile', help='Name of CSV file to port')

    def handle(self, *args, **options):
        csvfile_name = options['csvfile']

        with open('data/{}'.format(csvfile_name)) as csvfile:
            reader = csv.DictReader(csvfile)

            for row in reader:
                root_state = TreeState.objects.filter(name__icontains='Welcome') \
                                              .filter(name__icontains=row['location_type'].lower()) \
                                              .first()

                tree_info = {
                    'trigger': row['code'],
                    'root_state': root_state,
                    'summary': row['location_type'],
                }
                tree, created = Tree.objects.get_or_create(**tree_info)

                if created:
                    self.stdout.write(self.style.NOTICE('Created {}'.format(tree)))

        self.stdout.write(self.style.SUCCESS('Successfully processed CSV!'))

import csv
import sys
import os

def import_codes():
    '''
    Imports a csv file to create Tree objects with location-specific trigger words.

    The command expects the database to have a TreeState object with the name: "Welcome (city)."
    This differentiates it from the generic TreeState (i.e., the one called "Welcome", 
    triggered by the keyword "connect").
    '''
    reader = csv.DictReader(sys.stdin)

    for row in reader:
        root_state = TreeState.objects.filter(name__icontains='Welcome (city)').first()

        padded_code = row['Code'].zfill(4)
        
        tree_info = {
            'trigger': padded_code,
            'root_state': root_state,
            'summary': 'city',
        }

        tree, created = Tree.objects.get_or_create(**tree_info)

        if created:
            sys.stdout.write('Created {}'.format(tree))

    sys.stdout.write('Successfully processed CSV!')

if __name__ == "__main__":
    sys.path.append('..')
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "coordinated-entry-screening.settings")

    from django.core.wsgi import get_wsgi_application
    application = get_wsgi_application()

    from decisiontree.models import Tree, TreeState

    import_codes()
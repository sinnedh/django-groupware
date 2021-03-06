import sys

from utils import dt

from django.core.management.base import NoArgsCommand
from django.contrib.auth.models import User

from groupcontacts.models import Contact, Address

class Command(NoArgsCommand):
    help = 'Load sample data into the db'

    def handle_noargs(self, **options):
        self.stdout.write('Checking for existing data ...')
        try:
            cal = Contact.objects.get(firstname='Heidi', lastname='Heida')
            self.stdout.write('It looks like you already have loaded this sample data, quitting.')
            sys.exit(1)
        except Contact.DoesNotExist:
            self.stdout.write('No sample data found in db.')
            self.stdout.write('Install it...')

        self.stdout.write('Create Contacts ...')
        contact1 = Contact(firstname='Heidi', lastname='Heida')
        contact1.save()
        contact1 = Contact(firstname='Peter', lastname='Peterle')
        contact1.save()

        self.stdout.write('Create Addresses ...')
        address1 = Address(street='Musterstr. 33', postcode='12345', city='Möringen')
        address1.contact = contact1
        address1.save()

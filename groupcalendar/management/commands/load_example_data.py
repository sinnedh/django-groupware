import sys
import datetime

from utils import dt

from django.core.management.base import NoArgsCommand
from django.contrib.auth.models import User

from groupcalendar.models import Calendar, Recurrence, Event

class Command(NoArgsCommand):
    help = 'Load sample data into the db'

    def handle_noargs(self, **options):
        self.stdout.write('Checking for existing data ...')
        try:
            cal = Calendar.objects.get(name='Example Calendar', color='ff0000')
            self.stdout.write('It looks like you already have loaded this sample data, quitting.')
            sys.exit(1)
        except Calendar.DoesNotExist:
            self.stdout.write('No sample data found in db.')
            self.stdout.write('Install it...')

        self.stdout.write('Create User ...')
        user1 = User.objects.create_user('user1',
                                         'lennon@thebeatles.com',
                                         'userpassword')
        user1.save()

        self.stdout.write('Create Example Calendar ...')
        cal = Calendar(name='Example Calendar', color='dddddd')
        cal.save()

        self.stdout.write('The Example Calendar is created.')

        event = Event(recurrence=None,
                      name='Example Single Event',
                      calendar=cal
                      )
        event.start = dt(2014, 5, 1, 17)
        event.end = dt(2014, 5, 1, 19)
        event.save()
        event.create_and_save_occurences()

        rec = Recurrence(frequency='DAILY',
#            start=datetime.datetime(2014, 3, 30, 13),
            count=10)
        rec.save()

        event = Event(recurrence=rec,
                      name='Example Daily Event',
                      calendar=cal)
        event.start = dt(2014, 5, 1, 13)
        event.end = dt(2014, 5, 1, 18)
        event.save()
        event.create_and_save_occurences()




        """
        'Do we need to install the most common rules?'
        try:
            rule = Rule.objects.get(name="Daily")
        except Rule.DoesNotExist:
            print "Need to install the basic rules"
            rule = Rule(frequency = "YEARLY", name = "Yearly", description = "will recur once every Year")
            rule.save()
            print "YEARLY recurrence created"
            rule = Rule(frequency = "MONTHLY", name = "Monthly", description = "will recur once every Month")
            rule.save()
            print "Monthly recurrence created"
            rule = Rule(frequency = "WEEKLY", name = "Weekly", description = "will recur once every Week")
            rule.save()
            print "Weekly recurrence created"
            rule = Rule(frequency = "DAILY", name = "Daily", description = "will recur once every Day")
            rule.save()
            print "Daily recurrence created"
        print "Rules installed."

        print "Create some events"
        rule = Rule.objects.get(frequency="WEEKLY")
        data = {
                'title': 'Exercise',
                'start': datetime.datetime(2008, 11, 3, 8, 0),
                'end': datetime.datetime(2008, 11, 3, 9, 0),
                'end_recurring_period' : datetime.datetime(2009, 6, 1, 0, 0),
                'rule': rule,
                'calendar': cal
               }
        event = Event(**data)
        event.save()

        data = {
                'title': 'Exercise',
                'start': datetime.datetime(2008, 11, 5, 15, 0),
                'end': datetime.datetime(2008, 11, 5, 16, 30),
                'end_recurring_period' : datetime.datetime(2009, 6, 1, 0, 0),
                'rule': rule,
                'calendar': cal
               }
        event = Event(**data)
        event.save()

        data = {
                'title': 'Exercise',
                'start': datetime.datetime(2008, 11, 7, 8, 0),
                'end': datetime.datetime(2008, 11, 7, 9, 30),
                'end_recurring_period' : datetime.datetime(2009, 6, 1, 0, 0),
                'rule': rule,
                'calendar': cal
               }
        event = Event(**data)
        event.save()

        rule = Rule.objects.get(frequency="MONTHLY")
        data = {
                'title': 'Pay Mortgage',
                'start': datetime.datetime(2008, 11, 1, 14, 0),
                'end': datetime.datetime(2008, 11, 1, 14, 30),
                'end_recurring_period' : datetime.datetime(2009, 10, 2, 0, 0),
                'rule': rule,
                'calendar': cal
               }
        event = Event(**data)
        event.save()

        rule = Rule.objects.get(frequency="YEARLY")
        data = {
                'title': "Rock's Birthday Party",
                'start': datetime.datetime(2008, 12, 11, 19, 0),
                'end': datetime.datetime(2008, 12, 11, 23, 59),
                'end_recurring_period' : datetime.datetime(2009, 12, 22, 0, 0),
                'rule': rule,
                'calendar': cal
               }
        event = Event(**data)
        event.save()

        data = {
                'title': 'Christmas Party',
                'start': datetime.datetime(2008, 12, 25, 19, 30),
                'end': datetime.datetime(2008, 12, 25, 23, 59),
                'end_recurring_period' : datetime.datetime(2010, 12, 31, 0, 0),
                'rule': rule,
                'calendar': cal
               }
        event = Event(**data)
        event.save()

        data = {
                'title': 'New Pinax site goes live',
                'start': datetime.datetime(2009, 1, 6, 11, 0),
                'end': datetime.datetime(2009, 1, 6, 12, 00),
                'end_recurring_period' : datetime.datetime(2009, 1, 7, 0, 0),
                'calendar': cal
               }
        event = Event(**data)
        event.save()
        """


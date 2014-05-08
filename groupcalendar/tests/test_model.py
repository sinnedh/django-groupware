# -*- coding: utf-8 -*-
import datetime

from utils import dt

from django.test import TestCase

from groupcalendar.models import Calendar, Recurrence, Event, Occurence

class OccurenceTest(TestCase):
    def setUp(self):
        self.cal1 = Calendar(name='cal1', color='dddddd')
        self.cal1.save()
        self.events = (Event(name='e0'),
                       Event(name='e1'),
                       Event(name='e2'),
                       Event(name='e3'),
                       Event(name='e4'),
                       Event(name='e5'),
                       Event(name='e6'))

        # event that starts before and ends after on April 1
        self.events[0].start = dt(2014, 3, 30, 15)
        self.events[0].end = dt(2014, 4, 4, 12)
        # event that starts and ends on April 1
        self.events[1].start = dt(2014, 4, 1, 10)
        self.events[1].end = dt(2014, 4, 1, 17)
        # event that starts before and ends on April 1
        self.events[2].start = dt(2014, 3, 30, 10)
        self.events[2].end = dt(2014, 4, 1, 12)
        # event that starts on and ends after April 1
        self.events[3].start = dt(2014, 4, 1, 10)
        self.events[3].end = dt(2014, 4, 3, 12)
        # event that starts and ends after April 1
        self.events[4].start = dt(2014, 3, 20, 10)
        self.events[4].end = dt(2014, 3, 25, 14)
        # event that starts and ends after April 1
        self.events[5].start = dt(2014, 4, 3, 10)
        self.events[5].end = dt(2014, 4, 3, 14)
        # daily event with one occurence on April 1
        self.events[6].start = dt(2014, 3, 25, 10)
        self.events[6].end = dt(2014, 3, 25, 14)
        self.events[6].recurrence = Recurrence(frequency='DAILY', count=10)

        for e in self.events:
            e.calendar = self.cal1
            e.save()
            e.create_and_save_occurences()

    def tearDown(self):
        for e in self.events:
            del e

    def test_get_occurences_for_day(self):
        occurences = Occurence.get_occurences_for_day(datetime.date(2014, 4, 1))
        self.assertEqual(list(occurences),
                         [self.events[2].occurence_set.all()[0],
                          self.events[0].occurence_set.all()[0],
                          self.events[1].occurence_set.all()[0],
                          self.events[3].occurence_set.all()[0],
                          self.events[6].occurence_set.all()[7]])


class RecurrenceTest(TestCase):
#    def setUp(self):
#    def tearDown(self):

    def test_monthly_recurrence(self):
        """
        Test basic rules:
        """
        r = Recurrence(frequency='MONTHLY',
                 start=datetime.datetime(2014, 1, 1),
                 count=3)
        self.assertEqual(list(r.get_startdates()), [
            datetime.datetime(2014, 1, 1, 0, 0),
            datetime.datetime(2014, 2, 1, 0, 0),
            datetime.datetime(2014, 3, 1, 0, 0)])

        r = Recurrence(frequency='MONTHLY',
                 start=datetime.datetime(2014, 1, 1),
                 until=datetime.datetime(2014, 4, 1))
        self.assertEqual(list(r.get_startdates()), [
            datetime.datetime(2014, 1, 1, 0, 0),
            datetime.datetime(2014, 2, 1, 0, 0),
            datetime.datetime(2014, 3, 1, 0, 0),
            datetime.datetime(2014, 4, 1, 0, 0)])

        """
        Verify that when 'until' and 'count' are set use the minimum of both:
        """
        r = Recurrence(frequency='MONTHLY',
                 start=datetime.datetime(2014, 1, 1),
                 until=datetime.datetime(2014, 3, 1), count=10)
        self.assertEqual(list(r.get_startdates()), [
            datetime.datetime(2014, 1, 1, 0, 0),
            datetime.datetime(2014, 2, 1, 0, 0),
            datetime.datetime(2014, 3, 1, 0, 0)])
        r = Recurrence(frequency='MONTHLY',
                 start=datetime.datetime(2014, 1, 1),
                 until=datetime.datetime(2014, 3, 1), count=2)
        self.assertEqual(list(r.get_startdates()), [
            datetime.datetime(2014, 1, 1, 0, 0),
            datetime.datetime(2014, 2, 1, 0, 0)])

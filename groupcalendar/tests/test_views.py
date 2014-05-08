# -*- coding: utf-8 -*-
from utils import dt

from django.core.urlresolvers import reverse
from django.test import TestCase
from django.test.utils import override_settings

from groupcalendar.models import Calendar, Event


@override_settings(DEBUG=False, DEBUG_TOOLBAR_CONFIG={})
class GroupCalendarViewTests(TestCase):
    def _generate_default_calendar(self):
        calendar = Calendar(name='calendar', color='dddddd')
        calendar.save()
        return calendar

    def _generate_default_event(self):
        event = Event(name='event', calendar=self.cal1)
        event.start = dt(2014, 4, 1, 12)
        event.end = dt(2014, 4, 1, 15)
        event.save()
        event.create_and_save_occurences()
        return event

    def setUp(self):
        self.cal1 = Calendar(name='cal1', color='dddddd')
        self.cal1.save()

    def tearDown(self):
        del self.cal1


    def test_calendar_list(self):
        response = self.client.get(reverse('groupcalendar:calendar_list'))
        self.assertContains(response, 'Add calendar')

    def test_calendar_add(self):
        response = self.client.get(reverse('groupcalendar:calendar_add'))
        self.assertContains(response, 'form')
        # TODO: continue

    def test_calendar_detail(self):
        calendar = self._generate_default_calendar()
        response = self.client.get(reverse('groupcalendar:calendar_detail',
            args={calendar.id}), follow=True)
        self.assertContains(response, calendar.name)
        # TODO: continue

    def test_calendar_update(self):
        calendar = self._generate_default_calendar()
        response = self.client.get(reverse('groupcalendar:calendar_update',
            args={calendar.id}), follow=True)
        self.assertContains(response, 'form')
        # TODO: continue

    def test_calendar_delete(self):
        calendar = self._generate_default_calendar()
        self.assertEqual(1, len(Calendar.objects.filter(id=calendar.id)))
        response = self.client.get(reverse('groupcalendar:calendar_delete',
            args={calendar.id}), follow=True)
        post_response = self.client.post(reverse('groupcalendar:calendar_delete',
            args=(calendar.id,)), follow=True)
        self.assertRedirects(post_response, reverse('groupcalendar:calendar_list'), status_code=302)
        self.assertEqual(0, len(Calendar.objects.filter(id=calendar.id)))
        # TODO: test that calendar that have associated events are not deleted



    def test_event_add(self):
        response = self.client.get(reverse('groupcalendar:event_add'))
        self.assertContains(response, 'form')
        # TODO: continue

    def test_event_detail(self):
        event = self._generate_default_event()
        response = self.client.get(reverse('groupcalendar:event_detail',
            args={event.id}), follow=True)
        self.assertContains(response, event.name)
        # TODO: continue

    def test_event_update(self):
        event = self._generate_default_event()
        response = self.client.get(reverse('groupcalendar:calendar_update',
            args={event.id}), follow=True)
        self.assertContains(response, 'form')
        # TODO: continue

    def test_event_delete(self):
        event = self._generate_default_event()
        self.assertEqual(1, len(Event.objects.filter(id=event.id)))
        response = self.client.get(reverse('groupcalendar:calendar_delete',
            args={event.id}), follow=True)
        post_response = self.client.post(reverse('groupcalendar:calendar_delete',
            args=(event.id,)), follow=True)
        self.assertRedirects(post_response, reverse('groupcalendar:calendar_list'), status_code=302)
        self.assertEqual(0, len(Event.objects.filter(id=event.id)))



    def test_home_view(self):
        response = self.client.get(reverse('groupcalendar:home'))
        self.assertContains(response, 'Daily')
        self.assertContains(response, 'Weekly')
        self.assertContains(response, 'Monthly')

    def test_month_view(self):
        response = self.client.get(reverse('groupcalendar:month'))
        self.assertContains(response, 'Monthly view')

    def test_week_view(self):
        response = self.client.get(reverse('groupcalendar:week'))
        self.assertContains(response, 'Weekly view')

    def test_day_view(self):
        response = self.client.get(reverse('groupcalendar:day'))
        self.assertContains(response, 'Daily view')

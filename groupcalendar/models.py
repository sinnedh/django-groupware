import datetime
from dateutil import rrule

from django.contrib.auth.models import User, Group
from django.core.urlresolvers import reverse
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _


class Calendar(models.Model):
    name = models.CharField(max_length=200)
    color = models.CharField(max_length=6)
    description = models.TextField(_('description'), blank=True)

    def get_absolute_url(self):
        return reverse('groupcalendar:calendar_detail', kwargs={'pk': self.pk})

    def __unicode__(self):
        return self.name

class Recurrence(models.Model):
    FREQUENCIES = (
        ('YEARLY', _('Yearly')),
        ('MONTHLY', _('Monthly')),
        ('WEEKLY', _('Weekly')),
        ('DAILY', _('Daily')),
        ('HOURLY', _('Hourly')),
        )

    start = models.DateTimeField(_('start'), blank=True, null=True)
    frequency = models.CharField(_('frequency'), max_length=7,
                                 choices=FREQUENCIES)
    until = models.DateTimeField(_('end'), blank=True, null=True)
    count = models.IntegerField(default=0)
    interval = models.CommaSeparatedIntegerField(max_length='30')

    def get_startdates(self):
        frequency = rrule.__getattribute__(self.frequency)
        return list(rrule.rrule(frequency,
                    until=self.until,
                    dtstart=self.start,
                    count=self.count))

    def __unicode__(self):
        return '%s: %d, %s, %s' % (self.frequency,
                       self.count,
                       self.until,
                       self.interval)


class Event(models.Model):
    recurrence = models.ForeignKey(Recurrence, blank=True, null=True)
    name = models.CharField(max_length=200)
    description = models.TextField(_('description'), blank=True)
    place = models.TextField(_('place'), blank=True)
    calendar = models.ForeignKey(Calendar)
    start = models.DateTimeField(_('start'))
    end = models.DateTimeField(_('end'))
    whole_day = models.BooleanField(_('whole day'), default=False)
    created_by = models.ForeignKey(User, verbose_name=_('created by'), null=True) #TODO: must not be NULL
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def create_and_save_occurences(self):
        occurences = self.create_occurences()
        for o in occurences:
            o.save()
        return occurences

    """
    def update_and_save_occurences(self):
        duration = self.end - self.start
        for o in self.occurence_set.all():
            o.start = self.start
            o.end = self.start + duration
            o.save()
    """

    def delete_occurences(self):
        for o in self.occurence_set.all():
            o.delete()

    def create_occurences(self):
        occurences =[]
        # no recurrence, create a single occurence:
        if self.recurrence is None:
            o = Occurence(start=self.start, end=self.end)
            o.event = self
            occurences.append(o)
        # handle reccurence
        else:
            self.recurrence.start = self.start
            duration = self.end - self.start
            for rec_start in self.recurrence.get_startdates():
                o = Occurence()
                o.start = rec_start
                o.end = rec_start + duration
                o.event = self
                occurences.append(o)
        return occurences

    def get_absolute_url(self):
        return reverse('groupcalendar:event_detail', kwargs={'pk': self.pk})


class Occurence(models.Model):
    event = models.ForeignKey(Event)
    start = models.DateTimeField(_('start'))
    end = models.DateTimeField(_('end'))

    def __unicode__(self):
        return '%d: %s' % (self.id, self.start)

    @staticmethod
    def get_occurences_for_day(date):
        from_datetime = timezone.make_aware(
            datetime.datetime.combine(date, datetime.time.min),
            timezone.get_current_timezone())
        to_datetime = timezone.make_aware(
            datetime.datetime.combine(date, datetime.time.max),
            timezone.get_current_timezone())
        return Occurence.objects.filter(start__lte=to_datetime,
                end__gte=from_datetime).order_by('start')


class EventParticipantUser(models.Model):
    event = models.ForeignKey(Event)
    participant = models.ForeignKey(User, verbose_name=_('participant'))


class EventParticipantGroup(models.Model):
    event = models.ForeignKey(Event)
    participants = models.ForeignKey(Group, verbose_name=_('participants'))

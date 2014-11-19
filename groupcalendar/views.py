import calendar
import datetime

from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import render
from django.utils import timezone
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.utils.translation import ugettext_lazy as _

from groupcalendar.models import Occurence, Event, Calendar
from groupcalendar.forms import EventAddForm
from accounts.mixins import LoginRequiredMixin


class OverviewCalendar(LoginRequiredMixin, calendar.HTMLCalendar):
    def __init__(self, actual_date, firstweekday=0):
        self.actual_date = actual_date
        self.firstweekday = firstweekday  # 0 = Monday, 6 = Sunday

    def formatday(self, day, weekday):
        """
        Return a day as a table cell.
        """
        if day == 0:
            return '<td class="noday">&nbsp;</td>'

        day_repr = DayRepresentation(datetime.date(
            self.actual_date.year, self.actual_date.month, day))
        if day == self.actual_date.day and day_repr.date == timezone.now().date():
            return '<td class="%s"><span class="label label-danger">%s</span></td>' % (self.cssclasses[weekday], day)
        elif day == self.actual_date.day:
            return '<td class="%s"><span class="label label-primary">%s</span></td>' % (self.cssclasses[weekday], day)
        td_classes = [self.cssclasses[weekday]]
        if day_repr.date == timezone.now().date():
            td_classes.append('today')

        args = (' '.join(td_classes),
                reverse_lazy('groupcalendar:day', kwargs={
                    'year': self.actual_date.year,
                    'month': self.actual_date.month,
                    'day': day
                }),
                day)

        if day_repr.date == timezone.now().date():
            return '<td class="%s "><a href="%s" class="text-danger">%d</a></td>' % args
        else:
            return '<td class="%s "><a href="%s">%d</a></td>' % args

    def formatmonthname(self, theyear, themonth, withyear=True):
        return ''


class MonthlyCalendar(calendar.HTMLCalendar):
    def __init__(self, actual_date, firstweekday=0):
        self.actual_date = actual_date
        self.firstweekday = firstweekday  # 0 = Monday, 6 = Sunday

    def formatday(self, day, weekday):
        """
        Return a day as a table cell.
        """
        if day == 0:
            return '<td class="noday">&nbsp;</td>'

        day_repr = DayRepresentation(datetime.date(
            self.actual_date.year, self.actual_date.month, day))
        day_repr.load_occurences()
        occurences = day_repr.get_occurences_for_day()

        td_classes = [self.cssclasses[weekday]]
        args = (
            reverse_lazy('groupcalendar:day', kwargs={
                'year': self.actual_date.year,
                'month': self.actual_date.month,
                'day': day
            }),
            day)

        li = '<div class="list-group">'
        if day_repr.date == timezone.now().date():
            li += '<a class="list-group-item list-group-item-danger" href="%s">%d</a>' % args
            td_classes.append(' today ')
        else:
            li += '<a class="list-group-item list-group-item-info" href="%s">%d</a>' % args

        for o in occurences:
            li += '<a href="%s" class="list-group-item small"><small>' % (
                reverse_lazy('groupcalendar:event_detail', kwargs={
                    'pk': o.event.pk}),
                )
            li += o.event.name
#            li += '<button type="button" class="btn btn-default" data-container="body" data-toggle="popover" data-placement="top" data-content="Vivamus sagittis lacus vel augue laoreet rutrum faucibus.">Popover on top</button>'
            li += '</small></s>'
        li += '</div>'

        return '<td class="%s">%s</td>' % (
            ' '.join(td_classes),
            li)

    def formatmonthname(self, theyear, themonth, withyear=True):
        return ''


class DayRepresentation:
    def __init__(self, date):
        self.date = date
        self.occurences = []

    def load_occurences(self):
        self.occurences = Occurence.get_occurences_for_day(self.date)

    def get_occurences_for_starthour(self, starthour):
        index = self.hours.index(starthour)
        if index >= len(self.hours) - 1:
            endhour = 23
        else:
            endhour = self.hours[index+1]
        return self.get_occurences_between_hours(starthour, endhour)

    def get_occurences_between_hours(self, starthour, endhour):
        start_datetime = timezone.make_aware(
            datetime.datetime.combine(self.date, datetime.time(starthour, 0)),
            timezone.get_current_timezone())
        end_datetime = timezone.make_aware(
            datetime.datetime.combine(self.date, datetime.time(endhour, 0)),
            timezone.get_current_timezone())
        return self.get_occurences_between(start_datetime, end_datetime)

    def get_occurences_between(self, starttime, endtime):
        occurences = []
        for o in self.occurences:
            if o.start >= starttime and o.start < endtime and not o.event.whole_day:
                occurences.append(o)
        return occurences

    def get_occurences_for_day(self):
        return self.occurences

    def get_occurences_for_whole_day(self):
        occurences = []
        for o in self.occurences:
            if o.event.whole_day:
                occurences.append(o)
        return occurences


"""
Event based class views
"""


class EventDetail(DetailView):
    model = Event

    def get_context_data(self, **kwargs):
        context = super(EventDetail, self).get_context_data(**kwargs)
        context['title'] = _('Manage event')
        context['subtitle'] = _('Show details')
        return context


class EventCreate(CreateView):
    form_class = EventAddForm
    model = Event
    fields = ['name', 'start', 'end', 'description', 'place', 'url', 'calendar']
    success_url = reverse_lazy('groupcalendar:home')

    def get(self, *args, **kwargs):
        hour = 0
        if 'hour' in kwargs:
            hour = int(kwargs['hour'])
        if 'year' in kwargs and 'month' in kwargs and 'day' in kwargs:
            self.date = datetime.datetime(year=int(kwargs['year']),
                                          month=int(kwargs['month']),
                                          day=int(kwargs['day']),
                                          hour=hour)
        else:
            self.date = timezone.now().date()
        return super(EventCreate, self).get(args, kwargs)

    def get_initial(self):
        initial = super(EventCreate, self).get_initial()
        initial = initial.copy()
        if hasattr(self, 'date'):
            initial['day'] = self.date
            initial['start'] = self.date
            initial['end'] = self.date
        return initial

    def get_form_class(self):
        form_class = super(EventCreate, self).get_form_class()
        return form_class

    def get_context_data(self, **kwargs):
        context = super(EventCreate, self).get_context_data(**kwargs)
        context['title'] = _('Manage event')
        context['subtitle'] = _('Create')
        return context

    def form_valid(self, form):
        response = super(EventCreate, self).form_valid(form)
        self.object.create_and_save_occurences()
        return response

    """
    Save the created_by field:
    def form_valid(self, form):
        try:
            user = User.objects.get(email=form.cleaned_data['email'])
        except User.DoesNotExist:
            user = User.objects.create_user(form.cleaned_data['email'], form.cleaned_data['email'])
        form.instance.user = user
        return super(ProjectCreateDetails, self).form_valid(form)
    """


class EventUpdate(UpdateView):
    form_class = EventAddForm
    model = Event
    fields = ['name', 'start', 'end', 'description', 'place', 'url', 'calendar']

    def get_context_data(self, **kwargs):
        context = super(EventUpdate, self).get_context_data(**kwargs)
        context['title'] = _('Manage event')
        context['subtitle'] = _('Update')
        return context

    def form_valid(self, form):
        response = super(EventUpdate, self).form_valid(form)
        self.object.delete_occurences()
        self.object.create_and_save_occurences()
        return response


class EventDelete(DeleteView):
    model = Event
    # TODO: set to startpage or last view
    success_url = reverse_lazy('groupcalendar:home')

    def get_context_data(self, **kwargs):
        context = super(EventDelete, self).get_context_data(**kwargs)
        context['title'] = _('Manage event')
        context['subtitle'] = _('Delete')
        return context


"""
Calendar based class views
"""


class CalendarList(ListView):
    model = Calendar

    def get_context_data(self, **kwargs):
        context = super(CalendarList, self).get_context_data(**kwargs)
        context['title'] = _('Manage calendars')
        context['subtitle'] = _('List')
        return context


class CalendarDetail(DetailView):
    model = Calendar

    def get_context_data(self, **kwargs):
        context = super(CalendarDetail, self).get_context_data(**kwargs)
        context['title'] = _('Manage calendars')
        context['subtitle'] = _('Show details')
        return context


class CalendarCreate(CreateView):
    model = Calendar
    fields = ['name', 'description', 'color']
    success_url = reverse_lazy('groupcalendar:calendar_list')

    def get_context_data(self, **kwargs):
        context = super(CalendarCreate, self).get_context_data(**kwargs)
        context['title'] = _('Manage calendars')
        context['subtitle'] = _('Create')
        return context


class CalendarUpdate(LoginRequiredMixin, UpdateView):
    model = Calendar
    fields = ['name', 'description', 'color']
    success_url = reverse_lazy('groupcalendar:calendar_list')

    def get_context_data(self, **kwargs):
        context = super(CalendarUpdate, self).get_context_data(**kwargs)
        context['title'] = _('Manage calendars')
        context['subtitle'] = _('Update')
        return context


class CalendarDelete(LoginRequiredMixin, DeleteView):
    model = Calendar
    success_url = reverse_lazy('groupcalendar:calendar_list')

    def get_context_data(self, **kwargs):
        context = super(CalendarDelete, self).get_context_data(**kwargs)
        context['title'] = _('Manage calendars')
        context['subtitle'] = _('Delete')
        return context


"""
Other views
"""


@login_required
def home(request):
    import django
    context = {'dump': django.get_version()}
    return render(request, 'groupcalendar/home.html', context)


@login_required
def actual_day(request):
    today = timezone.now().date()
    return day(request, today.year, today.month, today.day)


@login_required
def day(request, year, month, day):
    date = datetime.date(int(year), int(month), int(day))
    occurences = Occurence.get_occurences_for_day(date)
    myCal = OverviewCalendar(date, calendar.MONDAY)
    context = {
        'date': date,
        'occurences': occurences,
        'calendar': myCal.formatmonth(date.year, date.month)
    }
    return render(request, 'groupcalendar/day.html', context)


@login_required
def actual_week(request):
    today = timezone.now().date()
    return week(request, today.year, today.isocalendar()[1])


@login_required
def week(request, year, week):
    date = datetime.date(int(year), int(1), 1)
    date += datetime.timedelta(weeks=int(week)-1)
    year = date.year
    week_nr = date.isocalendar()[1]
    firstday = date - datetime.timedelta(days=date.isocalendar()[2] - 1)
    context = {
        'week_nr': week_nr,
        'date': date,
        'firstday': firstday,
        'lastday': firstday + datetime.timedelta(days=6),
        'hours': [0, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 19, 23],
        'days': (
            DayRepresentation(firstday),
            DayRepresentation(firstday + datetime.timedelta(days=1)),
            DayRepresentation(firstday + datetime.timedelta(days=2)),
            DayRepresentation(firstday + datetime.timedelta(days=3)),
            DayRepresentation(firstday + datetime.timedelta(days=4)),
            DayRepresentation(firstday + datetime.timedelta(days=5)),
            DayRepresentation(firstday + datetime.timedelta(days=6))
            )
    }
    for i, day in enumerate(context['days']):
        day.hours = context['hours']
        day.load_occurences()
    return render(request, 'groupcalendar/week.html', context)


@login_required
def actual_month(request):
    today = timezone.now().date()
    return month(request, today.year, today.month)


@login_required
def month(request, year, month):
    date = datetime.date(int(year), int(month), 1)
    myCal = MonthlyCalendar(date, calendar.MONDAY)
    context = {
        'date': date,
        'calendar': myCal.formatmonth(date.year, date.month)
    }
    return render(request, 'groupcalendar/month.html', context)


@login_required
def week_test(request):
    context = {
        'visible_daily_timerange': range(0, 24),
        'days': ['Mon', 'Tue', 'Wed', 'Thursday', 'Fri', 'Sat', 'Sun']
    }
    return render(request, 'groupcalendar/week_test.html', context)

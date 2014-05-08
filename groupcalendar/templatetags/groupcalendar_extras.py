from dateutil.relativedelta import relativedelta

from django import template

register = template.Library()

@register.filter(name='events_for_hour')
def events_for_hour(day, hour):
    return day.get_occurences_for_starthour(hour)

@register.filter(name='nextmonth')
def nextmonth(value):
    value += relativedelta(months=+1)
    return value

@register.filter(name='prevmonth')
def prevmonth(value):
    value += relativedelta(months=-1)
    return value


@register.filter(name='nextweek')
def nextweek(value):
    value += relativedelta(weeks=+1)
    return value

@register.filter(name='prevweek')
def prevweek(value):
    value += relativedelta(weeks=-1)
    return value


@register.filter(name='nextday')
def nextday(value):
    value += relativedelta(days=+1)
    return value

@register.filter(name='prevday')
def prevday(value):
    value += relativedelta(days=-1)
    return value


@register.filter(name='ymd_link')
def ymd_link(value):
    return '/%s/%s/%s' % (value.year, value.month, value.day)

@register.filter(name='yw_link')
def yw_link(value):
    return '/%s/%s' % (value.year, value.isocalendar()[1])

@register.filter(name='ym_link')
def ym_link(value):
    return '/%s/%s' % (value.year, value.month)

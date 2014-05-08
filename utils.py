import datetime
from django.utils.timezone import utc

def dt(y, m, d, h=0, mi=0, sec=0, ms=0):
    """
    This is a wrapper function to avoid calling the datetime with the tzinfo
    argument every time.
    """
    return datetime.datetime(y, m, d, h, mi, sec, ms, utc)

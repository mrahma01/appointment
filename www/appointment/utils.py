import re
import random
import string
import datetime
from datetime import timedelta

from django.conf import settings


def get_random(limit):
    fn = lambda: \
        random.choice(string.lowercase + string.uppercase + string.digits)
    value = ''.join(fn() for i in range(limit))
    return value


def get_time_slot():
    FULL_DAY = settings.LAST_APPOINTMENT - settings.FIRST_APPOINTMENT
    now = datetime.datetime(2013, 1, 1, settings.FIRST_APPOINTMENT)
    end = now + timedelta(hours=FULL_DAY)
    slot = now
    time_slot = [now.strftime("%H:%M")]
    while slot < end:
        slot = slot + timedelta(minutes=settings.APPOINTMENT_INTERVAL)
        time_slot.append(slot.strftime("%H:%M"))
    return time_slot


def is_email(email):
    pattern = '[\.\w]{1,}[@]\w+[.]\w+'
    if re.match(pattern, email):
        return True
    else:
        return False


def get_monthly_calendar():
    """Return a month in list of dates"""
    today = datetime.datetime.today()
    return [today + timedelta(days=i) for i in range(1, 31)]

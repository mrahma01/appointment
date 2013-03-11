import re
import random
import string
from datetime import datetime, timedelta

from django.conf import settings


def get_random(limit):
    fn = lambda: \
        random.choice(string.lowercase + string.uppercase + string.digits)
    value = ''.join(fn() for i in range(limit))
    return value


def get_time_slot():
    FULL_DAY = settings.APPOINTMENT_END - settings.APPOINTMENT_START
    now = datetime(2013, 1, 1, settings.APPOINTMENT_START)
    end = now + timedelta(hours=FULL_DAY)
    slot = now
    time_slot = [now.strftime("%H:%M")]
    while slot < end:
        slot = slot + timedelta(minutes=settings.APPOINTMENT_INTERVAL)
        time_slot.append(slot.strftime("%H:%M"))
    return time_slot


def validate_email(email):
    pattern = '[\.\w]{1,}[@]\w+[.]\w+'
    if re.match(pattern, email):
        print email
        return True
    else:
        return False

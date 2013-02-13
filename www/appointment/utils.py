import random
import string
from datetime import datetime, timedelta


def get_random(limit):
    fn = lambda: \
            random.choice(string.lowercase + string.uppercase + string.digits)
    value = ''.join(fn() for i in range(limit))
    return value


def get_time_slot():
    now = datetime(2013, 1, 1, 7, 45)
    end = now + timedelta(hours=9)
    slot = now
    time_slot = []
    while slot < end:
        slot = slot + timedelta(minutes=15)
        time_slot.append(slot.strftime("%H:%M"))
    return time_slot

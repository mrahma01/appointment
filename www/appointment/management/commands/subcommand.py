from django.core.management.base import BaseCommand, CommandError
from datetime import datetime, timedelta

from appointment.models import TimeSlot


class DynamicCommand(BaseCommand):
    def handle(self, *args, **options):
        argument = args[0]
        extra_args = args[1:]

        if hasattr(self, argument):
            class_method = getattr(self, argument)
            class_method(extra_args) if extra_args else class_method()
        else:
            pass


class Command(DynamicCommand):

    def set_time_slot(self, *args):
        print "Writing time slots"
        now = datetime(2013, 2, 9, 8, 00)
        end = now + timedelta(hours=9)
        slot = now
        while slot<end:
            t = TimeSlot.objects.get_or_create(time_start=slot.strftime("%H:%M"))
            slot = slot + timedelta(minutes=15)

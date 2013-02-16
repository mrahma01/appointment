from django.db import models
from django.db.models.signals import post_save, pre_save
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.dispatch import receiver

from appointment import utils


class UserProfile(models.Model):
    user = models.OneToOneField(User)
    postcode = models.CharField(max_length=8)

    def __unicode__(self):
        return "%s" % self.user


def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

post_save.connect(create_user_profile, sender=User)


class TimeSlot(models.Model):
    slot_serial = models.CharField(max_length=3)
    time_start = models.TimeField()

    def __unicode__(self):
        return "%s" % self.time_start


class Appointment(models.Model):
    SUBMITTED = 'submitted'
    CONFIRMED = 'confirmed'
    MODIFIED = 'modified'
    DELETED = 'deleted'
    STATUS_CHOICE = (
        (SUBMITTED, 'Submitted'),
        (CONFIRMED, 'Confirmed'),
        (MODIFIED, 'Modified'),
        (DELETED, 'Deleted'),
    )

    ts = utils.get_time_slot()
    TIMESLOT = tuple(zip(ts, ts))
    RANDOM_KEY = 'VdTrwIMknrd'  # utils.get_random(11)

    email = models.EmailField(max_length=100)
    time_slot = models.CharField(max_length=11, choices=TIMESLOT)
    date_selected = models.DateField()
    appointment_key = models.CharField(max_length=11, default=RANDOM_KEY, editable=False)
    appointment_status = models.CharField(max_length=11, choices=STATUS_CHOICE,
                                            default=SUBMITTED)
    date_created = models.DateField(auto_now_add=True)
    date_modified = models.DateField(auto_now=True)

    def __unicode__(self):
        return "%s at %s on %s" % (self.email, self.time_slot, self.date_selected)

    @property
    def username(self):
        return self.email.split('@')[0]  # get first part of the email as name

    def get_absolute_url(self):
        return reverse('add-appointment')

    def get_confirmation_url(self):
        return reverse('confirm-appointment', kwargs={'key': self.appointment_key})


# @receiver(pre_save)
def find_duplicate_key(sender, instance, **kwargs):
    key = instance.appointment_key
    obj = Appointment.objects.filter(appointment_key=key)
    if obj:
        while True:
            key = utils.get_random(11)
            obj = Appointment.objects.filter(appointment_key=key)
            if not obj:
                instance.appointment_key = key
                break

pre_save.connect(find_duplicate_key, sender=Appointment)


# @receiver(post_save)
def send_confirmation_email(sender, instance, created, **kwargs):
    if created:
        from appointment.service import EmailService
        EmailService().send_confirmation(instance)

post_save.connect(send_confirmation_email, sender=Appointment)

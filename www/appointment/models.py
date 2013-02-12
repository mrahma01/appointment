from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse

class UserProfile(models.Model):
    user = models.OneToOneField(User)
    postcode = models.CharField(max_length=8)

    def __unicode__(self):
        return "%s" %self.user

def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

post_save.connect(create_user_profile, sender=User)


class TimeSlot(models.Model):
    slot_serial = models.CharField(max_length=3)
    time_start = models.TimeField()

    def __unicode__(self):
        return "%s" %self.time_start


class Appointment(models.Model):
    SUBMITTED = 'submitted'
    CONFIRMED = 'confirmed'
    MODIFIED = 'modified'
    DELETED = 'deleted'
    STATUS_CHOICE = (
        (SUBMITTED ,'Submitted'),
        (CONFIRMED,'Confirmed'),
        (MODIFIED ,'Modified'),
        (DELETED ,'Deleted'),
    )

    email = models.EmailField(max_length=100)
    time_slot = models.ForeignKey(TimeSlot)
    date_selected = models.DateField()
    appointment_key = models.CharField(max_length=11)
    appointment_status = models.CharField(max_length=11, choices=STATUS_CHOICE, 
                                            default=CONFIRMED)
    date_created = models.DateField(auto_now_add=True)
    date_modified = models.DateField(auto_now=True)

    def get_absolute_url(self):
        return reverse('add-appointment')    

    def get_confirmation_url(self):
        return reverse('confirm-appointment', kwargs={'key': self.appointment_key})

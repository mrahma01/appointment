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
    user = models.ForeignKey(User)
    time_slot = models.ForeignKey(TimeSlot)
    date_created = models.DateField()

    def get_absolute_url(self):
        return reverse('add-appointment')    

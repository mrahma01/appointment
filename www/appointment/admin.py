from django.contrib import admin
from appointment.models import Appointment


class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('email', 'time_slot', 'date_selected', 'appointment_key', 'appointment_status', 'date_created', 'date_modified')

admin.site.register(Appointment, AppointmentAdmin)

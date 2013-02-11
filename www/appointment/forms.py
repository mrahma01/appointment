from django import forms
from appointment.models import Appointment

class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ('email', 'time_slot', 'date_selected')

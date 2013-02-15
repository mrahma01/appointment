from django import forms
from appointment.models import Appointment


class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ('email', 'time_slot', 'date_selected')

    def __init__(self, *args, **kwargs):
        super(AppointmentForm, self).__init__(*args, **kwargs)
        self.fields['time_slot'].empty_label = None

from django import forms
from appointment.models import Appointment
from appointment.service import AppointmentService


class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ('email', 'time_slot', 'date_selected')

    def __init__(self, *args, **kwargs):
        super(AppointmentForm, self).__init__(*args, **kwargs)
        self.fields['time_slot'].empty_label = None

    def clean(self):
        cleaned_data = super(AppointmentForm, self).clean()
        date = cleaned_data['date_selected']
        slot = cleaned_data['time_slot']
        if not AppointmentService().is_booking_allowed(date, slot):
            raise forms.ValidationError("Sorry, Maximum appointment has been booked for this slot")
        return cleaned_data

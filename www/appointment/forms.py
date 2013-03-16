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
        self.fields['date_selected'].widget.attrs['readonly'] = True

    def clean(self):
        cleaned_data = super(AppointmentForm, self).clean()
        if 'date_selected' not in cleaned_data:
            raise forms.ValidationError("Valid date is dd/mm/yyyy")
        print cleaned_data
        date = cleaned_data['date_selected']
        slot = cleaned_data['time_slot']
        if not AppointmentService().is_booking_allowed(date, slot):
            raise forms.ValidationError("Sorry, Maximum appointment has been booked for this slot")
        return cleaned_data

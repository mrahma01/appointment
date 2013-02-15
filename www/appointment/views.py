from django.views.generic.edit import CreateView
from django.views.generic.base import TemplateView

from appointment.models import Appointment
from appointment.forms import AppointmentForm
from appointment.service import EmailService


class AppointmentCreateView(CreateView):
    form_class = AppointmentForm
    model = Appointment
    emailservice = EmailService()


class AppointmentConfirmView(TemplateView):
    template_name = 'appointment/confirmation.html'

    def get_context_data(self, **kwargs):
        context = super(AppointmentConfirmView, self).get_context_data(**kwargs)
        key = context['params']['key']
        print key

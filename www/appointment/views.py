from django.views.generic.edit import CreateView
from django.views.generic.base import TemplateView

from appointment.models import Appointment
from appointment.forms import AppointmentForm
from appointment.service import EmailService
from appointment import utils


class AppointmentCreateView(CreateView):
    form_class = AppointmentForm
    model = Appointment
    emailservice = EmailService()

    def form_valid(self, form):
        print self.request
        obj = form.save(commit=False)
        obj.appointment_key = utils.get_random(11)
        self.emailservice.send_confirmation(self.request, obj)
        return super(AppointmentCreateView, self).form_valid(form)


class AppointmentConfirmView(TemplateView):
    template_name = 'appointment/confirmation.html'

    def get_context_data(self, **kwargs):
        context = super(AppointmentConfirmView, self).get_context_data(**kwargs)
        key = context['params']['key']


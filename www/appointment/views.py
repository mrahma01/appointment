from django.views.generic.edit import CreateView

from appointment.models import Appointment
from appointment.forms import AppointmentForm
from appointment.service import EmailService
from appointment import utils

class AppointmentCreateView(CreateView):
    form_class = AppointmentForm
    model = Appointment
    emailservice = EmailService()
    
    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.appointment_key = utils.get_random(11)
        self.emailservice.send_confirmation(obj)
        return super(AppointmentCreateView, self).form_valid(form)

class AppointmentConfirmView(CreateView):
    pass

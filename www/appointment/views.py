from django.views.generic.edit import CreateView

from appointment.models import Appointment
from appointment.forms import AppointmentForm
from appointment import email_service

class AppointmentCreateView(CreateView):
    form_class = AppointmentForm
    model = Appointment
    
    
    def form_valid(self, form):
        obj = form.save(commit=False)
        print 'send confirmation email'
        email_service.send_confirmation(obj)
        return super(AppointmentCreateView, self).form_valid(form)



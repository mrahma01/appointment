from django.views.generic.edit import CreateView
from django.core.mail import send_mail

from appointment.models import Appointment
from appointment import email_service

class AppointmentCreateView(CreateView):
    model = Appointment
    
    def form_valid(self, form):
        obj = form.save(commit=False)
        print 'send confirmation email'
        email_service.send_confirmation(obj)
        return super(AppointmentCreateView, self).form_valid(form)



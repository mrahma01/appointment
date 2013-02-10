from django.views.generic.edit import CreateView
from django.core.mail import send_mail

from appointment.models import Appointment
from appointment import email_servie

class AppointmentCreateView(CreateView):
    model = Appointment
    
    def clean_email(self):
        print 'bar'

    def form_valid(self, form):
        obj = form.save(commit=False)
        print 'send confirmation email'
        email_service.send(obj)
        return super(AppointmentCreateView, self).form_valid(form)



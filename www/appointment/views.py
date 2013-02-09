from django.views.generic.edit import CreateView
from appointment.models import Appointment

class AppointmentCreateView(CreateView):
    model = Appointment



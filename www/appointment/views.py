from django.views.generic.edit import CreateView
from django.views.generic.base import TemplateView
from django.views.generic import ListView

from appointment.models import Appointment
from appointment.forms import AppointmentForm
from appointment.service import AppointmentService
from appointment.utils import is_email


class AppointmentCreateView(CreateView):
    form_class = AppointmentForm
    model = Appointment

    def get_initial(self):
        initial = super(AppointmentCreateView, self).get_initial()
        key = self.request.GET.get('key', '')
        obj = AppointmentService().get_booking_by_key(key)
        if obj:
            initial = initial.copy()
            initial['email'] = obj.email
            initial['time_slot'] = obj.time_slot
            initial['date_selected'] = obj.date_selected
        return initial


class AppointmentConfirmView(TemplateView):
    template_name = 'appointment/confirmation.html'

    def get_context_data(self, **kwargs):
        context = super(AppointmentConfirmView, self).get_context_data(**kwargs)
        key = context['params']['key']
        try:
            obj = Appointment.objects.filter(appointment_key=key)
            if obj:
                obj = AppointmentService().update_appointment(obj[0])
                context['obj'] = obj
        except Exception, e:
            print e

        return context


class AppointmentListView(ListView):
    model = Appointment
    template_name = 'appointment/appointment_list.html'

    def get_queryset(self):
        email = self.request.GET.get('email', 'email')
        key = self.request.GET.get('key', 'key')
        if is_email(email):
            if AppointmentService().has_confirmed_booking(email, key):
                return AppointmentService().get_booking_by_email(email)

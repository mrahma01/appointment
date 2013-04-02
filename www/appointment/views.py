from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.base import TemplateView
from django.views.generic import ListView
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect

from appointment.models import Appointment
from appointment.forms import AppointmentForm
from appointment.service import AppointmentService
from appointment.utils import is_email


class AppointmentListView(ListView):
    model = Appointment
    template_name = 'appointment/appointment_list.html'

    def get_queryset(self):
        email = self.request.GET.get('email', '')
        key = self.request.GET.get('key', '')
        if is_email(email):
            if AppointmentService().has_confirmed_booking(email, key):
                return AppointmentService().get_booking_by_email(email)


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

    def get_context_data(self, **kwargs):
        context = super(AppointmentCreateView, self).get_context_data(**kwargs)
        key = self.request.GET.get('key', '')
        obj = AppointmentService().get_booking_by_key(key)
        if obj:
            context['delete_key'] = True
        return context

    def post(self, *args, **kwargs):
        key = self.request.GET.get('key', '')
        try:
            obj = Appointment.objects.filter(appointment_key=key)
            if obj:
                obj = AppointmentService().update_appointment(obj[0], self.request)
                return HttpResponseRedirect("%s?email=%s&key=%s" % (reverse('appointment-list'), obj.email, obj.appointment_key))
        except Exception, e:
            print e
        return super(AppointmentCreateView, self).post(self.request, args, kwargs)


class AppointmentConfirmView(TemplateView):
    template_name = 'appointment/confirmation.html'

    def get_context_data(self, **kwargs):
        context = super(AppointmentConfirmView, self).get_context_data(**kwargs)
        key = context['key']
        try:
            obj = Appointment.objects.filter(appointment_key=key)
            if obj:
                obj = AppointmentService().confirm_appointment(obj[0])
                context['obj'] = obj
        except Exception, e:
            print e

        return context


class AppointmentUpdateView(UpdateView):
    model = Appointment
    form_class = AppointmentForm
    success_url = '/appointment/'
    slug_field = 'appointment_key'

    def get_queryset(self, *args, **kwargs):
        object = AppointmentService().get_confirmed_booking()
        return object


class AppointmentDeleteView(DeleteView):
    model = Appointment
    form_class = AppointmentForm
    success_url = '/appointment/'
    slug_field = 'appointment_key'

    def get_queryset(self, *args, **kwargs):
        object = AppointmentService().get_confirmed_booking()
        return object

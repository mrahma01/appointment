from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.template import Context
from django.conf import settings
from appointment.models import Appointment


class EmailService(object):

    def send_confirmation(self, obj):
        text_only = get_template('appointment/emails/confirmation.txt')
        html_only = get_template('appointment/emails/confirmation.html')

        base_uri = settings.ABSOLUTE_URI

        c = Context({'user': obj.username, 'key': obj.appointment_key,
                    'base_uri': base_uri})
        subject, from_email, to = 'Appointment Confirmation', \
            settings.FROM_EMAIL, obj.email
        text_content = text_only.render(c)
        html_content = html_only.render(c)
        msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
        msg.attach_alternative(html_content, "text/html")
        msg.send()

    def send_ticket(self, obj):
        text_only = get_template('appointment/emails/confirmation_ticket.txt')
        html_only = get_template('appointment/emails/confirmation_ticket.html')

        c = Context({'obj': obj})
        subject, from_email, to = 'Appointment Pass', settings.FROM_EMAIL, \
            obj.email
        text_content = text_only.render(c)
        html_content = html_only.render(c)
        msg = EmailMultiAlternatives(subject, text_content, from_email, [to, ])
        msg.attach_alternative(html_content, "text/html")
        msg.send()


class AppointmentService(object):

    def update_appointment(self, obj):
        obj.appointment_status = 'confirmed'
        obj.save()
        return obj

    def get_slot_booking_count(self, date, slot):
        """
        return the number of booking made on a day on a slot
        """
        return Appointment.objects.filter(date_selected=date, time_slot=slot).count()

    def is_booking_allowed(self, date, slot):
        """
        return if appointment slot is available to book.
        It compares with the settings for the maximum number for a slot allowed.
        """
        return self.get_slot_booking_count(date, slot) < settings.MAX_APPOINTMENT_PER_SLOT

    def has_confirmed_booking(self, email, key):
        return Appointment.objects.filter(email=email, appointment_key=key, appointment_status='confirmed')

    def get_booking_by_email(self, email):
        return Appointment.objects.filter(email=email, appointment_status='confirmed')

    def get_booking_by_key(self, key):
        obj = Appointment.objects.filter(appointment_key=key, appointment_status='confirmed')
        if obj:
            return obj[0]

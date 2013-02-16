from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.template import Context
from django.conf import settings


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

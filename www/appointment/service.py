from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.template import Context
from django.conf import settings

class EmailService(object):

    def send_confirmation(self, request, obj):
        text_only = get_template('appointment/emails/confirmation.txt')
        html_only = get_template('appointment/emails/confirmation.html')
        
        name = obj.email.split('@')[0] #get first part of the email as name

        base_uri = request.build_absolute_uri('/')[:-1]

        c = Context({'user': name, 'key': obj.appointment_key, 
            'base_uri':base_uri})
        subject, from_email, to = 'Appointment Confirmation', \
                                    settings.FROM_EMAIL, obj.email
        text_content = text_only.render(c)
        html_content = html_only.render(c)
        msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
        msg.attach_alternative(html_content, "text/html")
        msg.send()

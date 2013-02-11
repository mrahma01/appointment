from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.template import Context
from django.conf import settings

def send_confirmation(obj):
    text_only = get_template('appointment/emails/confirmation.txt')
    html_only = get_template('appointment/emails/confirmation.html')
    
    name = obj.email.split('@')[0] #get first part of the email as name

    c = Context({'user':name, 'link':obj.email})
    subject, from_email, to = 'Appointment Confirmation', settings.FROM_EMAIL, obj.email
    text_content = text_only.render(c)
    html_content = html_only.render(c)
    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    msg.attach_alternative(html_content, "text/html")
    msg.send()

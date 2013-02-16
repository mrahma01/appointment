from django.utils import unittest
from django.test.client import Client
from appointment.models import Appointment


class AppointmentCreateViewTest(unittest.TestCase):

    def setUp(self):
        self.c = Client()

    def test_add_url(self):
        response = self.c.get('/appointment/add/')
        self.assertEqual(response.status_code, 200)

    def test_confirmation_url(self):
        response = self.c.get('/appointment/confirm/asdf1234asd/')
        self.assertEqual(response.status_code, 200, 'key must be 11 char long')

        response = self.c.get('/appointment/confirm/asdf1234/')
        self.assertEqual(response.status_code, 404, 'key should not be 11 char long')

    def test_add_appointment_has_key(self):
        """If key exist update the status"""
        resp = self.c.post('/appointment/add/', {u'time_slot': [u'11:30'], u'email': [u'muhammad.m.rahman@live.com'], u'date_selected': [u'2012-12-12']})
        obj = Appointment.objects.all()[0]
        key = obj.__dict__['appointment_key']
        self.assertEqual(key, resp.context['key'])

    def test_does_not_save_with_duplicate_key(self):
        """If key already exist it will generate a new one"""
        pass

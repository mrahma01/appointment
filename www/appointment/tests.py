from django.utils import unittest
from django.test.client import Client


class AppointmentCreateViewTest(unittest.TestCase):
    fixtures = ['time_slot.json']

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

    def test_add_appointment_generate_key(self):
        """If key exist update the status"""
        response = self.c.post('/appointment/add/', {u'time_slot': [u'11:30'], u'email': [u'muhammad.m.rahman@live.com'], u'date_selected': [u'2012-12-12']})
        self.assertTrue('key' in response.context)

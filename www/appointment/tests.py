import datetime

from django.conf import settings
from django.utils import unittest
from django.test import TestCase
from django.test.client import Client
from django.core.urlresolvers import reverse
from django.core import mail
from django_dynamic_fixture import G

from appointment.models import Appointment
from appointment.service import AppointmentService, EmailService
from appointment.forms import AppointmentForm
from appointment.utils import *


class BaseTest(unittest.TestCase):

    def setUp(self):
        self.c = Client()


class ViewAppointmentTest(BaseTest):

    def test_appointment_list(self):
        response = self.c.get(reverse('appointment-list'))
        self.assertEquals(response.status_code, 200)

        G(Appointment, email='m@m.com', appointment_key='12hj12hj12j', appointment_status='confirmed')
        response = self.c.get("%s?email=m@m.com&key=12hj12hj12j" % reverse('appointment-list'))
        self.assertTrue('m@m.com' in response.content)

        G(Appointment, email='m@m.com', appointment_key='12hj12hj12j', appointment_status='confirmed')
        response = self.c.get("%s?email=m@m.com" % reverse('appointment-list'))
        self.assertTrue('m@m.com' not in response.content)

        G(Appointment, email='m@m.com', appointment_key='123iop123io')
        response = self.c.get("%s?email=m@m.com&key=123iop123io" % reverse('appointment-list'))
        self.assertTrue('m@m.com' not in response.content)


class AddAppointmentTest(BaseTest):

    def test_add_url(self):
        response = self.c.get(reverse('add-appointment'))
        self.assertEqual(response.status_code, 200)

    def test_add_appointment_has_key(self):
        """Appointment key will be generated by default"""
        app = G(Appointment, appointment_key='bCfm393Rmox')
        self.assertIsNotNone(app.appointment_key)

    def test_appointment_key_is_unique(self):
        """If key already exist it will generate a new one"""
        ap1 = G(Appointment, appointment_key='bCfm393Rmox')
        ap2 = G(Appointment, appointment_key='bCfm393Rmox')
        self.assertNotEqual(ap1.appointment_key, ap2.appointment_key)

    def test_max_appointment_booked(self):
        """ if MAX_APPOINTMENT_PER_SLOT has reached it will
            raise a validation error"""
        G(Appointment, time_slot='08:00', date_selected='2012-12-12')
        G(Appointment, time_slot='08:00', date_selected='2012-12-12')
        G(Appointment, time_slot='08:00', date_selected='2012-12-12')
        postdata = {
            'time_slot': u'08:00',
            'email': u'muhammad.m.rahman@live.com',
            'date_selected': datetime.date(2012, 12, 12)
        }
        form = AppointmentForm(postdata)
        self.assertFalse(form.is_valid())

    def test_appointment_has_calendar(self):
        """ Add appointment view must show a 30 days calendar starting from today """
        pass


class ConfirmAppointmentTest(BaseTest):

    def test_confirmation_url(self):
        G(Appointment, appointment_key='bCfm393Rmox')
        response = self.c.get(reverse('confirm-appointment', kwargs={'key': 'bCfm393Rmox'}))
        self.assertEqual(response.status_code, 200, 'key must be 11 char long')

        response = self.c.get(reverse('confirm-appointment', kwargs={'key': 'asdf123asdf'}))
        self.assertEqual(response.status_code, 200, 'Appointment will not be found')


class AppointmentServiceTest(BaseTest):

    def test_update_status(self):
        """Update status for submitted appointment when confirmed"""
        app = G(Appointment)
        self.assertEqual('submitted', app.appointment_status)

        AppointmentService().confirm_appointment(app)
        self.assertEqual('confirmed', app.appointment_status)

    def test_get_slot_booking_count(self):
        """ Return total number of slot booked on a time slot"""
        G(Appointment)
        G(Appointment)
        G(Appointment)
        self.assertEqual(AppointmentService().get_slot_booking_count('2012-12-12', '08:00'), 3)

    def test_has_confirmed_booking(self):
        G(Appointment, email='m@m.com', appointment_key='12hj12hj12j', appointment_status='confirmed')
        self.assertTrue(AppointmentService().has_confirmed_booking('m@m.com', '12hj12hj12j'))
        G(Appointment, email='m@m.com', appointment_key='12hj12hj12a')
        self.assertFalse(AppointmentService().has_confirmed_booking('m@m.com', '12hj12hj12a'))

    def test_get_booking_by_email(self):
        G(Appointment, email='m@m.com', appointment_status='confirmed')
        self.assertTrue(AppointmentService().get_booking_by_email('m@m.com'))
        G(Appointment, email='a@a.com', appointment_status='submitted')
        self.assertFalse(AppointmentService().get_booking_by_email('a@a.com'))

    def test_get_booking_by_key(self):
        G(Appointment, appointment_key='12hj12hj12a', appointment_status='confirmed')
        self.assertTrue(AppointmentService().get_booking_by_key('12hj12hj12a'))
        G(Appointment, appointment_key='bCfm393Rxxx')
        self.assertFalse(AppointmentService().get_booking_by_key('bCfm393Rxxx'))

    def test_get_confirmed_bookings(self):
        self.assertEqual(2, AppointmentService().get_confirmed_bookings().count())

    def test_get_month_appointments(self):
        """ Will show a list of dates, time_slots, and status in a dictionary for a month starting from today """
        pass


class EmailServiceTest(TestCase):

    def test_send_confirmation_email(self):
        app = G(Appointment)
        EmailService().send_confirmation(app)
        self.assertEqual(mail.outbox[0].subject, 'Appointment Confirmation')

    def test_send_confirmation_ticket(self):
        app = G(Appointment)
        EmailService().send_ticket(app)
        self.assertEqual(mail.outbox[1].subject, 'Appointment Pass')


class UtilTest(TestCase):

    def test_get_random(self):
        """Test randmon has correct number of characters"""
        self.assertEqual(9, get_random(9).__len__())
        self.assertNotEqual(10, get_random(9).__len__())

    def test_get_time_slot(self):
        """Test if the correct number of slot returned"""
        settings.FIRST_APPOINTMENT = 9
        settings.LAST_APPOINTMENT = 17
        settings.APPOINTMENT_INTERVAL = 60
        self.assertEqual(9, get_time_slot().__len__())
        self.assertNotEqual(8, get_time_slot().__len__())

    def test_is_email(self):
        """Check if string is email (almost valid[check RFC 2822])"""
        self.assertTrue(is_email('mmrs151@gmail.com'))
        self.assertTrue(is_email('mmrs151@yahoo.co.uk'))
        self.assertFalse(is_email('mmrs151@gmailcom'))
        self.assertFalse(is_email('mmrs151gmail.com'))
        self.assertFalse(is_email(''))
        self.assertFalse(is_email(' @ . '))

    def test_get_monthly_calendar(self):
        """Check if returns a 30 days calendar"""
        self.assertEqual(30, get_monthly_calendar().__len__())
        self.assertNotEqual(31, get_monthly_calendar().__len__())

from django.conf.urls.defaults import url, patterns, include
from appointment.views import AppointmentCreateView, AppointmentConfirmView


urlpatterns = patterns('',
    url(r'^add/$', AppointmentCreateView.as_view(), name='add-appointment'),
    url(r'^confirm/(?P<key>\w{11})/$', AppointmentCreateView.as_view(), name='confirm-appointment'),
)

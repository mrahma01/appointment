from django.conf.urls.defaults import url, patterns
from appointment.views import AppointmentCreateView, AppointmentConfirmView, AppointmentListView


urlpatterns = patterns('',
    url(r'^$', AppointmentListView.as_view(), name='appointment-list'),
    url(r'^add/$', AppointmentCreateView.as_view(), name='add-appointment'),
    url(r'^confirm/(?P<key>\w{11})/$', AppointmentConfirmView.as_view(), name='confirm-appointment'),
)

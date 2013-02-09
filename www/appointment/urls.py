from django.conf.urls.defaults import url, patterns, include
from appointment.views import AppointmentCreateView

urlpatterns = patterns('',
    url(r'^add/$', AppointmentCreateView.as_view(), name='add-appointment'),
)

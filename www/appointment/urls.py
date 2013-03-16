from django.conf.urls.defaults import url, patterns
from appointment import views


urlpatterns = patterns('',
    url(r'^$', views.AppointmentListView.as_view(), name='appointment-list'),
    url(r'^add/$', views.AppointmentCreateView.as_view(), name='add-appointment'),
    url(r'^confirm/(?P<key>\w{11})/$', views.AppointmentConfirmView.as_view(), name='confirm-appointment'),
)

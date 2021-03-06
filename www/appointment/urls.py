from django.conf.urls import url, patterns
from appointment import views


urlpatterns = patterns('',
    url(r'^$', views.AppointmentListView.as_view(), name='appointment-list'),
    url(r'^add/$', views.AppointmentCreateView.as_view(), name='add-appointment'),
    url(r'^confirm/(?P<key>\w{11})/$', views.AppointmentConfirmView.as_view(), name='confirm-appointment'),
    url(r'^update/(?P<slug>\w{11})/$', views.AppointmentUpdateView.as_view(), name='update-appointment'),
    url(r'^delete/(?P<slug>\w{11})/$', views.AppointmentDeleteView.as_view(), name='delete-appointment'),
)

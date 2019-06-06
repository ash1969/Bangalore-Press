from django.conf.urls import url
from django.urls import path
from . import views

app_name = 'cal'
urlpatterns = [
    url(r'^calendar/$', views.CalendarView.as_view(), name='calendar'),
    url(r'^festival/detail/(?P<event_id>\d+)/$', views.festival_detail, name='event_edit'),
    path('upcoming_festival/<int:event_id>/', views.festival_detail, name='upcoming_festival'),
    path('authenticate/', views.authentication, name='authentication'),
]
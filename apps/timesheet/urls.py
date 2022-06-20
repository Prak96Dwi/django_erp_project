""" apps/timesheet/urls.py """
from django.urls import path
from . import views


urlpatterns = [
	# Timesheet URL
    path('timesheet/record/', views.timesheet_record, name='timesheet_record'),
    path('timesheet/start/', views.start_time, name='start-time'),
    path('timesheet/finish/', views.finish_time, name='finish-time'),
]

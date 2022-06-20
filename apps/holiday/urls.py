""" apps/holiday/urls.py """
from django.urls import path
from . import views


urlpatterns = [
	# Holiday and Leave URL
    path('holidays/', views.holiday_display, name='holidays_page'),
    path('attendance/leave/info', views.leave_info, name='leave_information'),
    path('attendance/remove-holiday/<int:pk>/', views.remove_holiday, name='remove-holiday'),
]

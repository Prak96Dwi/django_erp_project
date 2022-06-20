""" apps/attendance/urls.py """
from django.urls import path
from . import views, api_views, ajax_views


urlpatterns = [
    # Notification URL
    path('notifications/page/',
        views.notifications_page,
        name='notifications_page'
    ),

    path('not/read/<int:id1>/<int:id2>/',
        views.delete_notification,
        name='make_read'
    ),

    # Attendance URL
    path('attendance/information',
        views.attendance_form,
        name='attendance_information'
    ),

    # API
    path('api/v1/posts',
        api_views.DataCollection.as_view(),
        name='data_collection'
    ),

    path('api/get-data',
        api_views.PostCollection.as_view(),
        name='post_collection'
    ),

    # AJAX
    path('attendance/ajax/employee-names/',
        ajax_views.load_names,
        name='employee_load_names'
    ),

    path('attendance/ajax/employee-names-monthly/',
        ajax_views.load_names_monthly,
        name='load_names_monthly'
    ),

    path('att/ajax/timesheet/record/',
        ajax_views.emp_timesheet_record,
        name='emp_timesheet_record'
    )
]

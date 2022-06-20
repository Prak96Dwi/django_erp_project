""" apps/leave/urls.py """
from django.urls import path
from . import views


urlpatterns = [
    # Leave URL
    path('leave/form',
        views.leave_request_form,
        name='leave_request_form'
    ),

    path('leave/success',
        views.leave_form_success,
        name='leave_request_approval'
    ),

    # TL approve path
    path('att/tl/not/<int:id>/<int:id2>/',
        views.tl_leave,
        name='tl-leave'
    ),

    path('attendance/tl/approve/<int:id1>/<int:id2>/',
        views.tl_leave_approve,
        name='tl-approve'
    ),

    path('attendance/tl/not-approve/<int:id1>/<int:id2>/',
        views.tl_leave_not_approve,
        name='tl-not-approve'
    ),

    # HR approve path
    path('att/hr/not/<int:id1>/<int:id2>/',
        views.hr_leave,
        name='hr-leave'
    ),

    path('attendance/approve/hr/<int:id1>/<int:id2>/',
        views.hr_leave_approve,
        name='hr-approve'
    ),

    path('attendance/hr/not-approve/<int:id1>/<int:id2>/',
        views.hr_not_approve,
        name='hr-not-approve'
    ),
]

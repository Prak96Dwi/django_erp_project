""" apps/core/urls.py """
from django.urls import path
from . import views


urlpatterns = [
    path('profile/', 
        views.Profile.as_view(),
        name='user_profile'
    ),

    path('designation-update/',
        views.designation_update,
        name='user_designation_update'
    )
]

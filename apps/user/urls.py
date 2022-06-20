""" apps/core/urls.py """
from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.conf.urls.static import static

from . import views


urlpatterns = [
    path('', csrf_exempt(views.Login.as_view()), name='login'),
    path('index/', views.index, name='index'),
    path('accounts/signup/', views.Sign_up.as_view(), name='sign_up'),

    # # Ajax Call
    path('ajax/load-names/', views.ajax_load_names, name='ajax_load_names'),
]

if settings.DEBUG:
    # pylint: disable = invalid-name
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )

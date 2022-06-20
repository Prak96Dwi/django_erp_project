""" apps/attendance/admin.py """
from django.contrib import admin
from apps.holiday.models import (
	Holiday
)


admin.site.register(Holiday)

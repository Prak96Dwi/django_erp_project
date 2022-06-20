""" apps/attendance/admin.py """
from django.contrib import admin
from apps.leave.models import (
	Leave
)


admin.site.register(Leave)

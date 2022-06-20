""" apps/attendance/admin.py """
from django.contrib import admin
from apps.timesheet.models import (
	Timesheet
)


admin.site.register(Timesheet)

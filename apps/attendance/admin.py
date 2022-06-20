""" apps/attendance/admin.py """
from django.contrib import admin
from apps.attendance.models import (
	Attendance, Record
)


admin.site.register(Attendance)

admin.site.register(Record)

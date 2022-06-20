"""attendance.models.py

This module contains model classes such as -
    * Attendance
    * Datewise

"""
# Importing Core Django modules
from django.conf import settings
from django.db.models import (
	Model,
	CASCADE,
	TimeField,
	CharField,
	DateField,
	ForeignKey
)


class Attendance(Model):
	"""Attendance model class

	This class instance would be created when the employee stand
	in front of camera to give attendance.

	Attributes
	------------
	1. timestamp : str
	2. employee_id : foreignkey

	"""
	# Time when the employee gives her attendance
	# in front of camera
	attendance_time = TimeField(auto_now_add=True)
	# id of Attendance model intance
	employee = ForeignKey(
		settings.AUTH_USER_MODEL,
	    on_delete=CASCADE,
		related_name='employee_attendance',
	)

	def __str__(self):
		""" string representation of AttendanceData instance """
		return f'{self.employee}'


class Record(Model):
	"""Attendance Record model class

	This class contains the attendance record of each employee
	datewise.

	"""

	# Name of the employee
	user = ForeignKey(
		settings.AUTH_USER_MODEL,
	    on_delete=CASCADE, 
		related_name='user_email'
	)

	# date when the employee check-in and check-out
	date = DateField(auto_now_add=True)

	# week when the employee chenk-in and check-out
	week = CharField(max_length=50)

	# Time when the employee comes to the office
	# and starts its work.
	time_in = TimeField(null=False)

	# Time when the employee going from the office
	# and finished her work.
	time_out = TimeField(null=False)

	# Work Status of the employee i.e. he/she is working or not
	work_status = CharField(max_length=500)

	def __str__(self):
		""" string representation of Datewise instance. """
		return f'{self.user.email}'

	#===============================================================================
	def is_month_exist(self, month) -> bool:
		"""
		Checks whether the record are of existing months or not.

		Arguments
		-----------
		1. month : month

		Returns
		--------
		bool : True, if the record month is same as that of the given
			required month. Otherwise False.

		"""
		if self.date.month == int(month):
			return True
		return False

	#================================================================================
	def is_year_exist(self, year) -> bool:
		"""
		Check whether the record are of existing year or not.

		Arguments
		----------
		1. year : str
		    Year of attendance.

		Returns
		---------
		bool : True, if the record year is same as that of the given
		       required year. Otherwise False.

		"""
		if self.date.year == int(year):
			return True
		return False

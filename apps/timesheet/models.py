"""
    This modules contains classes of employee timesheet
    * Timesheet
"""

from django.conf import settings
from django.db.models import (
	Model,
	CASCADE,
	ForeignKey,
	DateField,
	TimeField
)


class Timesheet(Model):
	"""Timesheeet model class

	This Timesheet model is for counting the hours the employee had
	done the work. excluding the gossip time and lunch time.
	This model instance is created when the user clicks on start time
	button and updates further.

	"""
	# User object of an employee
	user = ForeignKey(
		settings.AUTH_USER_MODEL,
	    on_delete=CASCADE, 
		related_name='user_timesheet'
	)
	# Date when the instance is created.
	date = DateField(auto_now_add=True)
	# Time when the user starts the work.
	start_time = TimeField(auto_now_add=True)
	# Time when the user finishes the work
	finish_time = TimeField(null=True)
	# Total time of the user worked in a office 
	total_time = TimeField(null=True)

	def __str__(self):
		""" string representation of timesheet instance """
		return f'{self.user.name}'

	#==========================================================================================
	def fullname(self):
		"""
		This method returns full name of the employee.
		"""
		return f'{self.user.first_name} {self.user.last_name}'

	#==========================================================================================
	def get_email(self):
		"""
		This method returns email of the employee.
		"""
		return f'{self.user.email}'

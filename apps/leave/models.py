"""
    This module contains employee leave related classes
    * Leave

"""

from django.conf import settings 
from django.db.models import (
	Model,
	CASCADE,
	ForeignKey,
	DateField,
	BooleanField,
	TextField
)


class Leave(Model):
	"""Leave model class

	Leave request of employee. This class intance will be created when the
	employee sends a request to its tech leader and hr for leave. When the user
	request for leave one notification is sent to the hr and tech lead for approval.

	"""
	# Name of the employee
	PENDING = 'Pending'
	Approved = 'Approved'

	user = ForeignKey(
		settings.AUTH_USER_MODEL,
	    on_delete=CASCADE, 
		related_name='user_leave'
	)

	# Date when the employee request for leave
	request_date = DateField(auto_now_add=True)

	# Date from when the employee want a leave
	leave_from = DateField()

	# Date till the emaployee wants a leave
	to = DateField()

	# hr approval is the boolean field whether the hr approved the leave request
	# of employee or not.
	hr_approval = BooleanField(default=PENDING)

	# tl_approval is the bool field whether the tech lead approved the teave request
	# of employee or not.
	tl_approval = BooleanField(default=PENDING)
	# Reason why the employee wants a holiday.
	reason = TextField(max_length=1500)

	def __str__(self):
		""" string representation of Leave instance. """
		return f'{self.user.email}'

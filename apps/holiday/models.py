"""
   This module contains some holiday related classes
   * Holiday

"""
from django.db.models import (
	Model,
	DateField,
	CharField
)


class Holiday(Model):
	"""Holiday model class

	Admin can fill the Holiday form which should should be holiday.

	"""
	# Date of Holiday.
	date = DateField()
	# occasion of Holiday for example - Diwali, Holi, etc.
	occasion = CharField(max_length=500)

	def __str__(self):
		""" string representation of Holiday instance """
		return f'{self.date} {self.occasion}'

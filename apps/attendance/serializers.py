""" apps/attendance/serializers.py """

# Importing django-restframework
from rest_framework import serializers
from rest_framework.parsers import JSONParser

from apps.user.models import CustomUser

from .models import Attendance


class UserSerializer(serializers.ModelSerializer):
	"""
	This serialze the custom user objects

	"""
	class Meta:
		""" CustomUser meta class """
		model = CustomUser
		fields = ['id', 'email', 'image', 'encod_image']


class AttendanceSerializer(serializers.ModelSerializer):

	class Meta:
		model = Attendance
		fields = '__all__'

	


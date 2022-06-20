"""
	This view module contains API classes.
    * Datacollection
    * PostCollection

"""
# Imporing django-restframework
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from apps.user.models import CustomUser

# Importing this app modules
from .serializers import UserSerializer, AttendanceSerializer
from .models import Record, Attendance


class DataCollection(APIView):

	def get(self, request, format=None):
		users = CustomUser.objects.all()
		serializer = UserSerializer(snippets, many=True)
		return Response(serializer.data)


class PostCollection(APIView):
    serializer_class = AttendanceSerializer
    def post(self, request, format=None):
        data = request.data
        serializer = self.serializer_class(data=data)
        if serializer.is_valid():
            serializer.save()
            ele = request.data['timestamp']
            time_obj, time_obj2, date_obj = formatted_time(ele)
            obj3 = Record.obj.objects.filter(name=request.data['emp']).filter(date=date_obj)
            if obj3:
                # Update the record of Saturday and Sunday
                if calendar.day_name[date_obj.weekday()] == ('Saturday' or 'Sunday'):
                    if obj3[0].time_in != "-----":
                        user_attendance_update(obj3, time_obj, time_obj2)
                    else:
                        weekend_attendance_update(obj3, time_obj2)
                else:                    
                    user_attendance_update(obj3, time_obj, time_obj2)

            else:
                Record.objects.create(
                    name=request.data['emp'],
                    date=date_obj,
                    week=calendar.day_name[date_obj.weekday()],
                    time_in=time_obj2,
                    time_out=time_obj2,
                    work_status='Working'
                )

                # If the particular week is Saturday or Sunday
                if calendar.day_name[date_obj.weekday()] == 'Friday':
                    weekday_attendance_record(date_obj, request.data['emp'])

                # If a particular month have 1st day
                if date_obj.day == 1:
                    holiday_attendance_record(request.data['emp'],date_obj)

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

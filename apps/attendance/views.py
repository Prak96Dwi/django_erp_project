""" apps/attendance/views.py """

# Importing models from user app
from apps.user.models import CustomUser

# Importing models from chat app
from apps.chat.views import filter_channel_names

# Imporing Core django modules
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.http.response import HttpResponse, HttpResponseBadRequest
from django.views.generic import TemplateView, View
from django.views.generic.edit import FormView
from django.views import View
from django.core.paginator import Paginator
from django.core.serializers.json import DjangoJSONEncoder
from django.db.models import Q
from django.conf import settings
from django.core.mail import send_mail

# Importing core python modules
import json
import datetime
import time
import calendar
from notifications.signals import notify
from dateutil import tz

from .models import Attendance, Record

from .utils import (
    display_empname, filter_attendance_name, attendance_form_filter
)


def formatted_time(ele):
    """
    Returns the formatted time and date
    """
    num = ele.rfind('(')
    ele2, ele3 = ele[:num - 1], ele[num+1:len(ele)-1]
    date_obj = datetime.datetime.strptime(ele2, '%d-%b-%Y').date()
    time_obj = datetime.datetime.strptime(ele3, '%H:%M:%S.%f').time()
    time_obj2 = time_obj.strftime("%I:%M %p")
    return time_obj, time_obj2, date_obj


def user_attendance_update(obj3, time_obj, time_obj2):
    ''' Updates the time out and work Status of the employees attendance record '''
    t2 = datetime.datetime.strptime(obj3[0].time_in, '%I:%M %p')
    t3 = datetime.timedelta(hours = time_obj.hour,minutes = time_obj.minute) - datetime.timedelta(hours = t2.hour, minutes = t2.minute)
    if t3 >= datetime.timedelta(hours = 4) and t3 <= datetime.timedelta(hours = 5):
        obj3.update(time_out = time_obj2, work_status = "Half Day Working")
    elif t3 >= datetime.timedelta(hours = 7) and t3 <= datetime.timedelta(hours = 10):
        obj3.update(time_out = time_obj2, work_status = "Full Day Working")
    else:
        pass


def weekday_attendance_record(date_obj, nm):
    """
    Updates the weekend record of employee
    """
    for i in range(1,3):
        Record.objects.create(
                    name=nm,
                    date=datetime.date(date_obj.year, date_obj.month, date_obj.day + i),
                    week=calendar.day_name[datetime.date(date_obj.year, date_obj.month, date_obj.day + i).weekday()],
                    time_in="-----",
                    time_out="-----",
                    work_status='Weekend'
        )


def weekend_attendance_update(obj3, time_obj2):
    obj3.update(time_in = time_obj2)


def holiday_attendance_record(nm, date_obj):
    ''' Updates the holiday record of employee '''
    month_list = []

    for ele in Holiday.objects.all():
        month_list.append({'day': ele.date.day, 'month': ele.date.month, 'year': ele.date.year })

    for ele1 in month_list:
        if date_obj.month == ele1['month']:
            obj6 = Holiday.objects.get(date = datetime.date(ele1['year'], ele1['month'], ele1['day']))
            Record.obj.objects.create(
                name=nm,
                date=obj6.date,
                week=calendar.day_name[obj6.date.weekday()],
                time_in="-----",
                time_out="-----",
                work_status='Holiday'
            )


def get_dates(week, month, year=2021):
    return calendar.monthcalendar(year,month)[week]


def attendance_form(request):
    ''' User can search attendance record w.r.t. monthly , weekly, yearly and of juniors also. '''

    context = display_empname()
    context1 = filter_attendance_name(request)
    data = attendance_form_filter(context, context1)
    onelink, multilink = filter_channel_names(request)
    mydict = {'onelink': onelink, 'multilink': multilink}
    return render(request, 'attendance/attendance_form.html', {**data, **mydict})


def record_updation(obj6):
    current_time = datetime.datetime.now()
    for ob in obj6:
        if ob.finish_time == '':
            # obj1 = TimeSheet.objects.get(id = ob.id)
            start_tm = datetime.datetime.strptime(str(ob.start_time), "%H:%M:%S").time()
            t1 = datetime.timedelta(hours = current_time.hour, minutes = current_time.minute)
            t2 = datetime.timedelta(hours = start_tm.hour, minutes = start_tm.minute)
            time_diff = t1 - t2
            ob.total_time = str(datetime.datetime.strptime(str(time_diff), "%H:%M:%S").time())
            ob.save()
    return obj6


# Nofications methods
def notifications_page(request):
    ''' This function display the notifications '''
    data = request.user.notifications.unread()
    onelink, multilink = filter_channel_names(request)
    mydict = {'onelink': onelink, 'multilink': multilink, 'data': data}
    # mydict = {'onelink': onelink, 'multilink': multilink}
    return render(request, 'attendance/notifications.html', mydict)


def delete_notification(request, id1, id2):
    """
    Makes the particular object of notifications as read

    """
    user = get_object_or_404(CustomUser, pk=id2)
    obj = user.notifications.unread()
    for i in obj:
        if i.id == id1:
            i.mark_as_read()
    return redirect('/attendance/notifications_page')

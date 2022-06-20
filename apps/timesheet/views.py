""" apps/timesheet/views.py """
from django.shortcuts import render


def start_button_status(request):
    obj1 = TimeSheet.objects.filter(
        user=request.user.id,
        date=datetime.datetime.now()
    )

    if obj1:
        if obj1[0].finish_time == '':
            return {'Start': "True", "Finish": ""}
        else:
            return {'Start': "True", "Finish": "True"}
    return {'Start': "", "Finish": ""}


def timesheet_record(request):
    context =  display_empname()
    context1 = filter_attendance_name(request)
    data = attendance_form_filter(context, context1)
    btndict = start_button_status(request)
    mydata = {**data, **btndict}
    onelink, multilink = filter_channel_names(request)
    mydict = {'onelink': onelink, 'multilink': multilink}
    # return render(request, 'attendance/timesheet_record.html', mydict)
    return render(request, 'attendance/timesheet_record.html', {**mydata, **mydict})


def start_time(request):
    obj1 = CustomUser.objects.get(id=request.user.id)
    start_tm = str(datetime.datetime.now().time())[:8]

    user = CustomUser.objects.get(email=request.user.email)
    obj2 = TimeSheet.objects.filter(
    	user=user,
        date=datetime.datetime.now()
    )

    if not obj2:
        TimeSheet.objects.create(
        	user=obj1,
            name=request.user.first_name +" "+ request.user.last_name,
            start_time=start_tm
        )
    return redirect('/timesheet/record')
    # return redirect('/timesheet/form')


def finish_time(request):
    current_time = datetime.datetime.now()
    obj2 = CustomUser.objects.get(id = request.user.id)
    obj3 = TimeSheet.objects.get(
        user=obj2,
        date=datetime.datetime.now()
    )
    obj3.finish_time = str(datetime.datetime.now().time())[:8]
    start_tm = datetime.datetime.strptime(str(obj3.start_time), "%H:%M:%S").time()
    t1 = datetime.timedelta(hours = current_time.hour, minutes = current_time.minute)
    t2 = datetime.timedelta(hours = start_tm.hour, minutes = start_tm.minute)
    time_diff = t1 - t2
    obj3.total_time = str(datetime.datetime.strptime(str(time_diff), "%H:%M:%S").time())
    obj3.save()
    return redirect('/timesheet/record')
    # return redirect('/timesheet/form')

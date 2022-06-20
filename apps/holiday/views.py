""" apps/holiday/views.py """
from django.shortcuts import render


def holiday_display(request):
    ''' This function will display holiday list '''

    if request.method == "POST":
        Holiday.objects.create(
        	date=request.POST.get('calen1'),
        	occasion = request.POST.get('occassion')
        )
        subject = 'Holiday Alert'
        message = """ On occassion of """+str(request.POST['occassion'])+ """ there is holiday tomorrow .
         Let your client's be informed. Have a good time , """+str(request.POST['occassion'])+""" to all
         in advance.
         """
        email_from = settings.EMAIL_HOST_USER
        recipient_list = ["anushtha.shree321@gmail.com", "alban.shhai32@gmail.com"]

        date_obj1 = datetime.datetime.strptime(request.POST['calen1'], '%Y-%m-%d').date()

        time_diff = date_obj1 - datetime.date.today()
        if time_diff ==  datetime.timedelta(1):
            mail_for_leave(subject, message, email_from, recipient_list)

    data = HolidayData.objects.all()
    onelink, multilink = filter_channel_names(request)
    mydict = {'onelink': onelink, 'multilink': multilink, 'data': data}
    return render(request, 'attendance/holiday.html',mydict)


def leave_info(request):
    ''' This function will display leave information of a particular employee '''
    nm = request.user.username
    obj1 = Leave.objects.filter(name=request.user.username)
    obj2 = obj1.exclude(hr_approval='Not Approved')
    obj3 = obj2.exclude(tl_approval='Not Approved').order_by('-leave_to')

    onedict = display_empname()
    onelink, multilink = filter_channel_names(request)
    mydict = {'onelink': onelink, 'multilink': multilink}
    alldict = {**mydict, **onedict}
    objectdict = {'data': obj3}
    return render(request, 'attendance/leaveinfo.html', {**alldict, **objectdict})


def remove_holiday(request, pk):
    ''' This function will call when particular holiday object have been delete '''
    obj1 = Holiday.objects.get(id=pk)
    obj1.delete()
    return redirect('/attendance/holidays')

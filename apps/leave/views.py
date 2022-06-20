"""
"""

from django.shortcuts import render, get_object_or_404
from django.conf import settings
from django.core.mail import send_mail

from .models import Leave
from .utils import (
    display_employee_names, filter_channel_names, mail_for_leave
)


def leave_request_form(request):
    ''' Function to display Leave Request Form '''
    
    if request.method == 'POST':
        starting_date_of_leave, last_date_of_leave =  request.POST.get('calen1'), request.POST.get('last_date_of_leave')
        hiring_manager_email, tech_lead_email = request.POST.get('hr'), request.POST.get('tl')
        reason_for_leave = request.POST.get('reason')

        # Retreiving a record from CustomUser
        hiring_manager = CustomUser.objects.get(email=hiring_manager_email)
        tech_lead = CustomUser.objects.get(email=tech_lead_email)

        # Creating a attendance record of employee
        Leave.objects.create(
			user=request.user,
			request_date=starting_date_of_leave,
			leave_from=starting_date_of_leave,
			to=last_date_of_leave,
			reason=reason_for_leave
		)

        # Sending notification to the Tech Lead or Project Manager
        message = f'{starting_date_of_leave}@{last_date_of_leave}'

        message_description = f'''
                {request.user.get_full_name()} wants to take leave from 
                {starting_date_of_leave} to {last_date_of_leave} 
                because {reason_for_leave}
            '''

        send_notification_to_tech_lead_and_hiring_manager(
            request,
            tech_lead,
            message,
            message_description,
            hiring_manager
        )

        # Sending email to tl and hr
        # mail_for_leave(message_description, hiring_manager_email, tech_lead_email)

        return redirect('leave_request_approval')
    onedict = display_employee_names()
    onelink, multilink = filter_channel_names(request)
    mydict = {'onelink': onelink, 'multilink': multilink}
    return render(request, 'leave/leave_form.html', {**mydict, **onedict})


def leave_form_success(request):
    ''' Function ensuring that Request have been sent successfully by displaying this message'''
    return render(request, 'attendance/leave_success.html', {})


def tl_leave(request, id, id2):
    ''' Displaying the particular notifications of TL/PM '''
    user = get_object_or_404(CustomUser, pk=id2)
    obj = user.notifications.unread()
    mydata = not_object(obj, id)
    return render(request, 'attendance/tl_leave.html', mydata)


def tl_leave_approve(request,  id1, id2):
    ''' This is a AJAX function and this will call when the TL/PM will approve the 
          leave request. '''
    data = request.user.notifications.unread()
    user = get_object_or_404(CustomUser, pk=id2)
    obj = user.notifications.unread()
    mydata = not_object(obj, id1)

    date1 = mydata['verb'][:mydata['verb'].rfind('@')]
    date2 = mydata['verb'][mydata['verb'].rfind('@') + 1:]

    # Updating the attendance record as Approved and timestamp
    object1 = Leave.objects.get(name = mydata['actor'], leave_from = date1)
    object1.tl_approval = 'Approved'
    object1.leave_request_date = mydata['timestamp']
    object1.save()

    # Sending notifications to HR or CTO after receiving by TL or PM
    object2 = CustomUser.objects.get(email = request.user.email)
    sender = CustomUser.objects.get(email = mydata['actor'])
    recp2 = CustomUser.objects.get(email = mydata['action_object'])
    data1 = str(sender)+" wants to take leave from "+str(date1)+" to "+str(date2)+" because "+ str(object1.leave_reason) +" and  approved by "+str(request.user.email)
    notify.send(sender = sender,
                recipient = recp2,
                verb = mydata['verb'],
                description = data1)

    # Sending notifications to the user who requests for leave
    data2 = str(object2)+" Approved your Leave Request"
    notify.send(sender = object2,
               recipient = sender,
               verb = "Response "+ mydata['verb'],
               description = data2)

    # Unread the particular object of notification
    delete_not_object(obj, id1)

    return render(request, 'attendance/notifications.html', {'data': data})


def tl_leave_not_approve(request, id1, id2):
    ''' This is a AJAX function and this will call when the TL/PM will not approve the 
          leave request. '''
    data = request.user.notifications.unread()
    user = get_object_or_404(CustomUser, pk=id2)
    obj = user.notifications.unread()
    mydata = not_object(obj, id1)

    date1 = mydata['verb'][:mydata['verb'].rfind('@')]
    date2 = mydata['verb'][mydata['verb'].rfind('@') + 1:]

    object2 = CustomUser.objects.get(email = request.user.email)

    # Updating the attendance record as Approved and timestamp
    object1 = Leave.objects.get(name = mydata['actor'], leave_from = date1)
    object1.tl_approval = 'Not Approved'
    object1.leave_request_date = mydata['timestamp']
    object1.save()
    sender = CustomUser.objects.get(email = mydata['actor'])
    recp2 = CustomUser.objects.get(email = mydata['action_object'])
    data1 = str(sender)+" wants to take leave from "+str(date1)+" to "+str(date2)+" but not approved by "+str(request.user.email)

    # Sending notification to the HR or CTO
    notify.send(sender = sender, 
                recipient = recp2, 
                verb = mydata['verb'],
                description = data1)

    # Sending notification to the user who requested for leave
    data2 = str(object2)+" Not Approved your Leave Request"
    notify.send(sender = object2,
               recipient = sender,
               verb = "Response "+ mydata['verb'],
               description = data2)

    # Unread the particular object of notification
    delete_not_object(obj, id1)

    return render(request, 'attendance/notifications.html', {'data': data})


def hr_leave_approve(request, id1, id2):
    ''' This is a AJAX function and this will call when the CTO/HR will approve the 
          leave request. '''
    data = request.user.notifications.unread()
    user = get_object_or_404(CustomUser, pk=id2)
    obj = user.notifications.unread()
    mydata = not_object(obj, id1)


    date1 = mydata['verb'][:mydata['verb'].rfind('@')]
    date2 = mydata['verb'][mydata['verb'].rfind('@') + 1:]

    # Updating the attendance record as Approved and timestamp
    object1 = Leave.objects.get(name=mydata['actor'], leave_from=date1)
    object1.hr_approval = 'Approved'
    object1.save()

    # Creating a attendance record of user as Dayoff
    date_obj1 = datetime.datetime.strptime(date1, '%Y-%m-%d').date()
    date_obj2 = datetime.datetime.strptime(date2, '%Y-%m-%d').date()
    date_diff = datetime.timedelta(days = date_obj2.day) - datetime.timedelta(days = date_obj1.day)
    num = 0
    if date_diff.days == 0:
        Record.objects.create(
            name=mydata['actor'].username[:mydata['actor'].username.rfind('@')],
            date=date_obj1,
            week=calendar.day_name[date_obj1.weekday()],
            time_in="-----",
            time_out="-----",
            work_status='Leave'
        )

    for i in range(0,date_diff.days + 1):
        mydate = date_obj1.day + num
        Record.objects.create(
            name=mydata['actor'].username[:mydata['actor'].username.rfind('@')],
            date=datetime.date(2021, date_obj1.month, mydate),
            week=calendar.day_name[datetime.date(2021, 3, mydate).weekday()],
            time_in="-----",
            time_out="-----",
            work_status='Leave'
        )
        num = num + 1

    # Sending notification to the user who requested for leave
    object2 = CustomUser.objects.get(email = request.user.email)
    data2 = str(object2)+" Approved your Leave Request"
    recp = get_object_or_404(CustomUser, email=mydata['actor'])
    notify.send(sender = object2,
               recipient = recp,
               verb = "Response "+ mydata['verb'],
               description = data2)

    subject = 'Leave Request Accepted'
    message = "Your Leave Request have been approved by both "+str(request.user.email)+ " and your Tech Lead"
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [mydata['actor']]
    mail_for_leave(subject, message, email_from, recipient_list)

    # Making a particular notification object as read
    delete_not_object(obj, id1)

    return render(request, 'attendance/notifications.html', {'data': data})


def hr_leave(request, id1, id2):
    ''' Displaying the particular notifications of HR/ CTO '''
    user = get_object_or_404(CustomUser, pk=id2)
    obj = user.notifications.unread()
    mydata = not_object(obj, id1)
    return render(request, 'attendance/hr_leave.html', mydata)


def hr_not_approve(request, id1, id2):
    ''' This is a AJAX function and this will call when the CTO/HR will NOT approve the 
          leave request. '''
    data = request.user.notifications.unread()
    user = get_object_or_404(CustomUser, pk=id2)
    obj = user.notifications.unread()
    mydata = not_object(obj, id1)

    date1 = mydata['verb'][:mydata['verb'].rfind('@')]
    date2 = mydata['verb'][mydata['verb'].rfind('@') + 1:]

    # Updating the attendance record as Approved and timestamp
    object1 = Leave.objects.get(name=mydata['actor'], leave_from=date1)
    object1.hr_approval = 'Not Approved'
    object1.save()

     # Sending notification to the user who requested for leave
    object2 = CustomUser.objects.get(email = request.user.email)
    recp = CustomUser.objects.get(email = mydata['actor'])
    data2 = str(object2)+" Not Approved your Leave Request"
    notify.send(sender = object2,
                recipient = recp,
                verb = "Response "+ mydata['verb'],
                description = data2)

    # Making a particular notification object as read
    delete_not_object(obj, id1)

    return render(request, 'attendance/notifications.html', {'data': data})

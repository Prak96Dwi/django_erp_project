""" apps/attendance/ajax_views.py """
from apps.user.models import CustomUser

from django.http import JsonResponse
from .models import Record


def load_names(request):
    ''' AJAX function so that user can display attendance record weekly '''
    name, week, month = request.GET.get('name'), request.GET.get('week'), request.GET.get('month')
    tup, dict2, week_data  = [], {}, []
    attendance_records = Record.objects.filter(name=name[:name.rfind('@')])

    # Filter data monthly as per individual user
    for record in attendance_records:
        if record.date.month == int(month):
            tup.append(record.id)
    obj2 = Record.objects.filter(id__in=tup)

    # Calling function so that we can get dates as per week
    obj3 = get_dates(int(week), int(month))

    # Filtering data weekly as per individual user
    for ele1 in obj2:
        if ele1.date.day in obj3:
            week_data.append(ele1.id)
    obj4 = Record.objects.filter(id__in=week_data)

    # Filtering the records yearly
    obj5 = [ele.date for ele in obj4 if ele.date.year == int(request.GET.get('year'))]
    obj6 = Record.objects.filter(date__in=obj5).order_by('date')

    # Converting the record in list data type
    obj7 = list(obj6.values())

    return JsonResponse(obj7, safe=False)


def load_names_monthly(request):
    """
    Function to display user's attendance record monthly.

    """
    # Retreiving name, week and month
    email = request.GET.get('name')
    week = request.GET.get('week')
    month = request.GET.get('month')
    year = request.GET.get('year')

    list_of_records = []
    # Retreiving user object
    user = CustomUser.objects.get(email=email)

    # Filtering the attendance record of particular employee.
    attendance_records = Record.objects.filter(user=user)

    if year and month: # If year and month both exists

        # List of records of particular user having required year.
        list_of_records_of_particular_year = [
                record for record in attendance_records \
                if record.is_year_exist(year)
        ]

        # List of records of particular user having required month.
        list_of_records_of_particular_month = [
            record.id for record in list_of_records_of_particular_year \
            if record.is_month_exist(month)
        ]

    # Ordered list of records of particular year and month
    # according to data
    list_of_records_in_ordered_date = list(Record.filter(
        id__in=list_of_records_of_particular_month
    ).order_by('date').values())

    return JsonResponse(list_of_records_in_ordered_date, safe=False)


def emp_timesheet_record(request):
    name, week, month = request.GET.get('name'), request.GET.get('week'), request.GET.get('month')
    list_of_record_ids = []
    user = CustomUser.objects.get(email=name)
    obj3 = TimeSheet.objects.filter(user=user)

    # Filter data monthly as per individual user
    for ele in obj3:
        if ele.date.month == int(month):
            list_of_record_ids.append(ele.id)
    obj4 = TimeSheet.objects.filter(id__in=tup)

    # Filtering the attendance record yearly 
    obj5 = [ele.id for ele in obj4 if ele.date.year == int(request.GET.get('year'))]
    obj6 = TimeSheet.objects.filter(id__in=obj5).order_by('date')
    obj7 = record_updation(obj6)
    # obj7 = TimeSheet.objects.filter(id__in = obj5).order_by('date')

    # Converting the record in list data type
    obj8 = list(obj7.values())
    return JsonResponse(obj8, safe=False)

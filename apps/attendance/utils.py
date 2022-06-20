""" apps/attendance/utils.py """
from apps.user.models import CustomUser
from apps.heirarchy.models import Heirarchy

from django.conf import settings


def display_empname():
    all_members = CustomUser.objects.all()
    PM,Web,CTO,TL,DIR = [],[],[],[],[]
    for member in all_members:
        if member.designation == settings.PROJECT_MANAGER:
            PM.append(member)
        elif member.designation == settings.WEB_DEVELOPER:
            Web.append(member)
        elif member.designation == settings.CHEIF_TECHNICAL_OFFICER:
            CTO.append(member)
        elif member.designation == settings.DIRECTOR:
            DIR.append(member)
        else:
            TL.append(member)
    return {
    	'all_members': all_members,
    	'PM': PM, 
    	'Web':Web,
    	'CTO':CTO,
    	'DIR':DIR,
    	'TL': TL
    }


def filter_attendance_name(request):
    """
    Filter attendance name according to their Heirarchy
    """
    if request.user.designation == settings.DIRECTOR:
        newlist = CustomUser.objects.all()
    else:
        mylist = [request.user.id]
        for ele in Heirarchy.objects.filter(usernm__username = request.user.username):
            obj2 = CustomUser.objects.get(username = ele.child)
            mylist.append(obj2.id)
            for ele2 in Heirarchy.objects.filter(usernm__username = ele.child):
                obj3 = CustomUser.objects.get(username = ele2.child)
                mylist.append(obj3.id)
                for ele3 in Heirarchy.objects.filter(usernm__username = ele2.child):
                    obj4 = CustomUser.objects.get(username = ele3.child)
                    mylist.append(obj4.id)
        newlist = CustomUser.objects.filter(id__in = mylist)
    return newlist


def attendance_form_filter(context, context1):
    """
    Returns a list of objects according to their designation
    """
    Web = [ele for ele in context['Web'] if ele in context1]
    DIR = [ele for ele in context['DIR'] if ele in context1]
    TL  = [ele for ele in context['TL']  if ele in context1]
    PM  = [ele for ele in context['PM'] if ele in context1]
    CTO = [ele for ele in context['CTO'] if ele in context1]
    return {'Web': Web, 'DIR': DIR, 'TL':TL, 'PM': PM, 'CTO': CTO}

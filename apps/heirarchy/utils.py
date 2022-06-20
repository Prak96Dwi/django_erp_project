""" apps/core/utils.py """

# importing Django Core modules
from django.conf import settings

# Importing other apps modules
from apps.user.models import CustomUser
from apps.chat.models import ChatGroupList

# Importing native app modules
from .models import Heirarchy


def filter_name(request):
	"""
	This function is called when the index page is open.
	In this function contains only if-else condition. In which
	if condition is checcks if the user is director, then it will
	returns all custom user objects. Otherwise, it will check its designation
	and returns lists of members coming under request users child.

	Returns : list
	1. all_members : list of users objects.

	"""
	if request.user.designation == settings.DIRECTOR:
		all_members = CustomUser.objects.all()
	else:
		obj1 = Heirarchy.objects.filter(child__email=request.user.email)
		obj5 = CustomUser.objects.filter(email=obj1[0].email)
		mylist = [obj5[0].id, request.user.id]
		for ele in Heirarchy.objects.filter(parent__email=request.user.email):
			obj2 = CustomUser.objects.get(email=ele.child)
			mylist.append(obj2.id)
			for ele2 in Heirarchy.objects.filter(parent__email=ele.child):
				obj3 = CustomUser.objects.get(email=ele2.child)
				mylist.append(obj3.id)
				for ele3 in Heirarchy.objects.filter(parent__email=ele2.child):
					obj4 = CustomUser.objects.get(email=ele3.child)
					mylist.append(obj4.id)
		all_members = CustomUser.objects.filter(id__in=mylist).order_by('designation')
	return all_members


def web_developers_list(all_members):
	"""
	This function returns web developer list.

	"""
	return [
		member for member in all_members \
		if member.designation == settings.WEB_DEVELOPER
	]


def cheif_technical_officers_list(all_members):
	"""
	This function returns Chief Technical Officer lsit.

	"""
	return [
		member for member in all_members \
		if member.designation == settings.CHEIF_TECHNICAL_OFFICER
	]


def directors_list(all_members):
	"""
	This function returns Directors list.

	"""
	return [
		member for member in all_members \
		if member.designation == settings.DIRECTOR
	]


def tech_leaders_list(all_members):
	"""
	This function returns Tech Leaders list.

	"""
	return [
		member for member in all_members \
		if member.designation == settings.TECH_LEADER
	]


def project_managers_list(all_members):
	"""
	This function returns project manager lists.

	"""
	return [
		member for member in all_members \
		if member.designation == settings.PROJECT_MANAGER
	]


def form_data_filter(all_members):
	"""
	This function filters users on the basis of their designation.

	Parameters
	-----------
	1. all_members : list of all the Custom Users.

	Attributes
	1. Web : list of all Web Developers.
	2. DIR : list of all Directors.
	3. TL : list of all Tech Leaders.
	4. PM : list of all Project managers.
	5. CTO : list of all Chief Technical Officers.

	Returns : dict
	Dictionary of web, TL, CTO, DIR and PM.

	"""
	Web = web_developers_list(all_members)
	DIR = directors_list(all_members)
	TL  = tech_leaders_list(all_members)
	PM  = project_managers_list(all_members)
	CTO = cheif_technical_officers_list(all_members)
	return {'Web': Web, 'DIR': DIR, 'TL':TL, 'PM': PM, 'CTO': CTO}


def filter_channel_names(request):
	"""
	"""
	chatlink = ChatGroupList.objects.all()
	mylink, onelink, multilink = [], [], []

	for obj in chatlink:
	    if request.user in obj.member_name.all():
	        mylink.append(obj)

	for obj1 in mylink:
	    if obj1.member_name.all().count() > 2:
	    	multilink.append(obj1)
	    else:
	    	onelink.append(obj1)
	return onelink, multilink


def display_employee_names():
	"""
	"""
	all_members = CustomUser.objects.all()
	PM, Web, CTO, TL, DIR = [], [], [], [], []
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

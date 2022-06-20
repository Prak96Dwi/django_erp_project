""" apps/heirarchy/views.py """

# Importing Core Django modules
from django.shortcuts import render, redirect
from django.views.generic.base import View
from django.http import HttpResponseRedirect

from apps.user.models import CustomUser

from .utils import (
    display_employee_names, filter_channel_names,
    filter_name, form_data_filter
)
from .models import Heirarchy


class Profile(View):
    """
    This function is create a designation heirarchy of the users.
    """
    template_name = 'heirarchy/profile.html'

    def get(self, request, *args, **kwargs):
        """
        This method renders profile form. So that the admin can assign designation
        to its employee.

        """
        context =  display_employee_names()
        onelink, multilink = filter_channel_names(request)

        mydict = {'onelink': onelink, 'multilink': multilink}
        return render(request, self.template_name, {**context, **mydict})

    def post(self, request):
        """
        When user assigns a post to a user then
        to a user by filling a form then this post
        request is called.

        Permissions
        -----------
        Permission to fill this form is allowed only to
        the admin who can assign post to an organsation.

        Redirects
        ----------
        when form fill successfully then it redirects
        to the home page.

        """
        # Retreiving parent id under which the admin is posting
        # another one
        parent_id = int(request.POST.get('parent_id'))
        # Retreiving parent and child user object
        parent_user = get_object_or_404(CustomUser, pk=parent_id)

        child_list = request.POST.getlist('child_list')

        for child in child_list:
            child_user = get_object_or_404(CustomUser, pk=int(child))
            # Creating Heirarchy object
            Heirarchy.objects.create(
                parent=parent_user,
                child=child_user
            )
        return redirect('index')


def designation_update(request):
    """
    This function is used to update the designation of the user and 
    update the User Heirarchy.

    when method == POST:
    1 First we retreive parent email, child email
      and designation of a user. Then, fetching parent, child object from
      CustomUser Model and then updating child object designation as per the
      admin have choosen in the form.

    2. Then, after 

    """
    if request.method == 'POST':
        # Fetching parent name
        parent_email = request.POST.get('parent')
        # Fetching child name
        child_email = request.POST.get('child')
        # Designation of a child user
        designation = request.POST.get('designation')

        parent = get_object_or_404(CustomUser, email=parent_email)

        # Updating designation of child user
        child = get_object_or_404(CustomUser, email=child_email)
        child.update_designation(designation)

        # Updating the Heirarchy data
        parent_heirarchy = Heirarchy.objects.filter(parent=parent)
        child_heirarchy = Heirarchy.objects.get(child=child)

        for heirarchy in parent_heirarchy:
            # updates parent heirarchies
            heirarchy.update_parent(child_heirarchy)

        # Updating Userheirarchy record
        # child_heirarchy.usernm_id = 
        # child_heirarchy.save()

        # Send email to a child user who is been promoted
        child.send_email_to_user()

        return redirect('index')

    context =  display_employee_names()
    onelink, multilink = filter_channel_names(request)
    mydict = {'onelink': onelink, 'multilink': multilink}
    context1 = filter_name(request)
    context2 = form_data_filter(context1)
    return render(request, 'heirarchy/designation_update.html', {**mydict, **context2})

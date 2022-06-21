""" apps/core/views.py """
# Importing Django modules
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, JsonResponse
from django.contrib.auth import authenticate, login
from django.views.generic.base import View
from django.views.generic.edit import FormView
from django.conf import settings

# Importing core app modules
from .utils import (
    filter_name,
    form_data_filter,
    filter_channel_names,
    display_employee_names,
)
from .forms import LoginForm, UserRegistrationForm
from .models import CustomUser


def index(request):
    """Home Page of this site

    Renders home page having data of heirarchy model.

    ** Context **

    """
    all_members = filter_name(request)
    context2 = form_data_filter(all_members)
    onelink, multilink = filter_channel_names(request)
    mydict = {"onelink": onelink, "multilink": multilink}
    return render(request, "user/index.html", {**mydict, **context2})


class Sign_up(FormView):
    """Login page of this site

    This class renders the signup form. Displaying the
    registration form demands for some inputs for registration.

    """

    # Specify name of template
    template_name = "user/sign_up.html"

    # Specify the form you want to use
    form_class = UserRegistrationForm

    # url to redirect after successfully updating details
    success_url = "/index/"

    def form_valid(self, form):
        """
        This method is called when the data is clean and
        form is valid.
        """
        user = form.save()
        user.calculate_face_encoding()
        user.resize_profile_image()
        return super().form_valid(form)


class Login(View):
    """Login class

    This class renders login form in get request and
    post request is called when user submits the form.

    """

    form_class = LoginForm
    # Login template page
    template_name = "registration/login.html"

    def get(self, request):
        """
        Renders login form
        """
        login_form = self.form_class()
        return render(request, self.template_name, {"login_form": login_form})

    def post(self, request):
        """
        This method is called when user submits login form.
        Then form is validated and the inputs email and password is authenticated
        and login. If email and password is invalid then it renders the login form
        with display the error on top of submit button.

        Arguments
        ----------
        1. email : email
            User email
        2. password : password
            User login password

        Redirects
        ---------
        Redirects to the home page or index page of this site.

        """
        login_form = self.form_class(request.POST)
        if login_form.is_valid():
            email = login_form.cleaned_data.get("email")
            password = login_form.cleaned_data.get("password")
            # Authenticating email and password of user
            user = authenticate(request, email=email, password=password)
            if user is not None:  # If user is not None
                login(request, user)  # login the user
                return redirect("index")
            return render(request, self.template_name, {"login_form": login_form})
        return render(request, self.template_name, {"login_form": login_form})


def ajax_load_names(request):
    """
    This function is used to pass the record
    of the user on ajax request.
    """
    usernmId = request.GET.get("usernmId")
    dict2, choice = {}, []
    custom_users = CustomUser.objects.all()
    user = CustomUser.objects.filter(id=usernmId).first()
    for i in custom_users:
        if user.designation == "Project Manager" and i.designation == "Tech Leader":
            choice.append(
                {
                    "id": i.id,
                    "name": i.get_full_name(),
                    "designation": i.designation,
                    "first_name": i.first_name,
                    "last_name": i.last_name,
                }
            )
        elif (
            user.designation == "Director"
            and i.designation == "Cheif Technical Officer"
        ):
            choice.append(
                {
                    "id": i.id,
                    "name": i.get_full_name(),
                    "designation": i.designation,
                    "first_name": i.first_name,
                    "last_name": i.last_name,
                }
            )
        elif (
            user.designation == "Cheif Technical Officer"
            and i.designation == "Project Manager"
        ):
            choice.append(
                {
                    "id": i.id,
                    "name": i.get_full_name(),
                    "designation": i.designation,
                    "first_name": i.first_name,
                    "last_name": i.last_name,
                }
            )
        elif user.designation == "Tech Leader" and i.designation == "Web Developer":
            choice.append(
                {
                    "id": i.id,
                    "name": i.get_full_name(),
                    "designation": i.designation,
                    "first_name": i.first_name,
                    "last_name": i.last_name,
                }
            )
        elif (
            user.designation == "Cheif Technical Officer"
            and i.designation != "Director"
        ):
            choice.append(
                {
                    "id": i.id,
                    "name": i.get_full_name(),
                    "designation": i.designation,
                    "first_name": i.first_name,
                    "last_name": i.last_name,
                }
            )
    return JsonResponse(choice, safe=False)

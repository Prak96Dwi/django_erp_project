""" apps/user/forms.py """

# Importing Django core modules
from django import forms
from django.conf import settings
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import gettext as _
from django.contrib.auth import authenticate

# Importing this app modules
from .models import CustomUser


class UserRegistrationForm(UserCreationForm):
    """UserRegistration Form class

    This form class contains some attributes of user such as
    1. designation : str
        Designation of user
    2. first_name : str
        First name of user
    3. last_name : str
        Last name of user
    4. email : email
        Email of user
    5. password : str
    6. designation : str
        Designation of user Ex: Web Developer, Cheif Technical Officer, etc.

    """

    DESIGNATION_CHOICES = [
        (settings.WEB_DEVELOPER, settings.WEB_DEVELOPER),
        (settings.PROJECT_MANAGER, settings.PROJECT_MANAGER),
        (settings.TECH_LEADER, settings.TECH_LEADER),
        (settings.CHEIF_TECHNICAL_OFFICER, settings.CHEIF_TECHNICAL_OFFICER),
        (settings.DIRECTOR, settings.DIRECTOR),
    ]

    # Dropdown of designations
    designation = forms.CharField(
        max_length=100, widget=forms.Select(choices=DESIGNATION_CHOICES)
    )

    class Meta:  # pylint: disable=too-few-public-methods
        """Custom user meta class"""

        model = CustomUser
        fields = [
            "first_name",
            "last_name",
            "email",
            "password1",
            "password2",
            "designation",
            "image",
        ]

    def clean(self):
        """
        Validating form fields
        """
        cleaned_data = super().clean()
        email = cleaned_data.get("email")

        # Checking whether the email exist or not.
        user = CustomUser.objects.filter(email=email).exists()

        # Validating Profile Image of a user.
        profile_image = cleaned_data.get("image")

        if not profile_image:  # If profile image is not uploaded.
            raise ValidationError(
                _("Please upload your image in jpeg or png."), code="invalid"
            )

        # Validating profile image extension.
        image_extension = profile_image.content_type.split("/")[1]

        if image_extension not in ("jpeg", "png"):
            # profile image should be in jpeg or png format.
            raise ValidationError(_("Image should be in jpeg or png."), code="invalid")

        if user:  # user is True
            raise ValidationError(_("Email is already registered."), code="invalid")

        return self.cleaned_data


class LoginForm(forms.Form):
    """LoginForm class

    Login form attributes are:
    1. email : email
        Email of user
    2. password : str
        Password of user

    """

    email = forms.EmailField(
        max_length=50,
        widget=forms.EmailInput(
            attrs={"class": "form-control", "placeholder": "Enter User Email"}
        ),
    )

    password = forms.CharField(
        max_length=15,
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "Password"}
        ),
    )

    def clean(self):
        """
        Validating form fields
        """
        cleaned_data = super().clean()
        password = cleaned_data.get("password")  # passowrd of user
        email = cleaned_data.get("email")  # email of user
        # Checking whether the email exist or not.
        try:
            user = CustomUser.objects.get(email=email)
        # pylint: disable=no-member
        except CustomUser.DoesNotExist:  # If user not exist.
            raise ValidationError(_("Email is invalid"), code="invalid")

        # Checking that email and password is matching or not
        user = authenticate(email=email, password=password)
        if user is None:
            raise ValidationError(
                _("Email and password is not matching. "), code="invalid"
            )

        return self.cleaned_data

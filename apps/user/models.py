""" core/models.py

This module contains two model classes
    * CustomUser
    * UserHeirarchy

and non-model class
    * EmailBackend

"""
# Django core modules
from django.db.models import (
    Model,
    CharField,
    BooleanField,
    ImageField,
    EmailField,
)
from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.core.mail import send_mail

# Importing Pillow image.
from PIL import Image
import face_recognition


class MyUserManager(BaseUserManager):
    """
    Customer Registration manager
    """

    def create_user(self, email, password=None, **kwargs):
        """
        Creates and saves a User with the given email,and password.
        """
        if not email:
            raise ValueError("Users must have an email address")

        user = self.model(email=self.normalize_email(email))

        if kwargs.get("first_name"):
            user.first_name = kwargs.get("first_name")
        if kwargs.get("last_name"):
            user.last_name = kwargs.get("last_name")
        if kwargs.get("email"):
            user.email = kwargs.get("email")
        if kwargs.get("designation"):
            user.designation = kwargs.get("designation")
        if kwargs.get("is_active"):
            user.is_active = kwargs.get("is_active")
        if kwargs.get("is_staff"):
            user.is_staff = kwargs.get("is_staff")
        if kwargs.get("is_admin"):
            user.is_admin = kwargs.get("is_admin")

        user.is_admin = False
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(email, password=password)
        user.designation = settings.DIRECTOR
        user.is_admin = True
        user.is_staff = True
        user.is_active = True
        user.save(using=self._db)
        return user


class CustomUser(AbstractBaseUser):
    """
    This is the user model which contains many fields such
        1. first_name : str
                First name of user
        2. last_name : str
                Last name of user
        3. email : str
                Email of a user
        4. designation : str
                Designation of a user
        5. password : str
                Password of a user

    """

    # First Name of user
    first_name = CharField(max_length=50, null=False)

    # Last name of user
    last_name = CharField(max_length=50, null=False)

    # Email of the user
    email = EmailField(
        max_length=50,
        unique=True,
    )

    # Designation of a user Eg: Web Developer, Cheif Technical Officer, etc.
    designation = CharField(max_length=50, blank=True)

    # Image of a user whose image would be taken during attendance.
    image = ImageField(upload_to="profiles", null=True)

    # Encoded image of a user whose image would be taken during attendance.
    encod_image = CharField(max_length=2500, null=True)

    is_active = BooleanField(default=True)

    is_staff = BooleanField(default=False)  # a admin user; non super-user

    is_admin = BooleanField(default=False)  # a superuser

    objects = MyUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    # ========================================================================================
    def get_full_name(self) -> str:
        """
        This method will return full name of a user.
        """
        # The user is identified by their email address
        return f"{self.first_name} {self.last_name}"

    # ======================================================================================
    def get_short_name(self) -> str:
        """
        This method returns email of a user.
        """
        return self.email

    # =====================================================================================
    def resize_profile_image(self):
        """
        Resize the profile image uploaded by admin.

        Resize the image as per the specific height and width
        and saves it.

        """
        image = Image.open(self.image.path)  # Open image using self

        image_height_and_width = (
            settings.PROFILE_IMAGE_HEIGHT,
            settings.PROFILE_IMAGE_WIDTH,
        )

        image.thumbnail(image_height_and_width)
        image.save(self.image.path)  # saving image at the same path

    # ====================================================================================
    def calculate_face_encoding(self):
        """
        This function calculates face encoding
        of a person when the admin or hr uploads
        employee image.

        Updates encode_image field of CustomUser instance.

        """
        image = face_recognition.load_image_file(self.image.path)
        self.encod_image = face_recognition.face_encodings(image)[0]
        self.save()

    # ==================================================================================
    def update_designation(self, designation):
        """
        Updates designation of a user with the given designation.

        Argument
        ----------
        designation : str
            designation of a user e.g. Project Manager, Web Developer, Tech Lead,
            Cheif Technical Officer etc.

        """
        self.designation = designation
        self.save()

    # ==================================================================================
    def send_email_to_user(self):
        """
        send email to the user who is been promoted.
        to a new designation.

        """
        subject = 'Hi user'
        message = f'You have been promoted.'
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [self.email, ]
        try:
            send_mail(subject, message, email_from, recipient_list)
        except:
            return


    def __str__(self) -> str:
        """string representation of Customer instance"""
        return f"{self.first_name} {self.last_name}"


class Profile(Model):
    """
    This class user profile attributes.

    Attributes
    ------------
    1. full_name : str
        full name of a user.
    2. email : email
        email of a user.
    3. address : str
        address of a user
    4. phone_number : str
        phone number of user
    5. district : str
        district of a user.
    6. state : str
        state of a user
    7. country : str
        country of a user.

    """

    full_name = CharField(max_length=299, null=False)

    email = EmailField(null=False, max_length=299, unique=True)

    address = CharField(max_length=299, null=False)

    phone_number = CharField(max_length=100, null=False)

    district = CharField(max_length=100, null=False)

    state = CharField(max_length=299, null=False)

    country = CharField(max_length=299, null=False)

    def __str__(self):
        """string representation of Profile instance"""
        return f"{self.email}"

"""
	This signal modules will invoke when admin will create user object.
	This module will create profile object and send email to the
	registered user.

"""
# Importing core django modules
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from django.core.mail import send_mail

from .models import CustomUser, Profile


@receiver(post_save, sender=CustomUser)
def at_ending_save(sender, instance, created, **kwargs):
	# When CustomUser object is created. Then, this method will invoke
	if created and not instance.is_admin:# If user object is created.
		# Creating profile object
		Profile.objects.create(
			full_name=instance.get_full_name(),
			email=instance.email
		)

		# Sending email to a registered user
		subject = 'welcome to 6DegreeIT Solutions Private Limited'
		message = f"""
		Hi {instance.get_full_name()}, thankyou for taking interest in
		this blog.
		"""
		email_from = settings.EMAIL_HOST_USER
		recipient_list = [instance.email, ]
		send_mail(subject, message, email_from, recipient_list)

"""chat/models.py

This module contains models classes related to chat such as
    1. GroupMessage
    2. OnetoOneMessage
    3. ChatGroupList

"""
from django.db.models import (
	Model,
	CASCADE,
	CharField,
	IntegerField,
	TextField,
	TimeField,
	BooleanField,
	ImageField,
	DateField,
	ManyToManyField
)
from apps.user.models import CustomUser


class GroupMessage(Model):
	"""GroupMessage model class

	This class contains the instances of the messages
	sent in groups by the user.

	Attributes
	------------
	1. user_id : int
	    user id who is sending message to others in a group.
	2. name : str
	    name of a group where message is sending
	3. message : str
	    content of a message which is sent by the user
	4. time : time
	    time when the user sends the message to other members
	5. group_id : int
	    id of a group where messages is sent

	"""
	user_id = IntegerField()
	name = CharField(max_length=100)
	message = TextField()
	time = TimeField(auto_now=True)
	group_id = IntegerField()


class OnetoOneMessage(Model):
	"""OnetoOneGroup model class

	This class contains the instances of message sent
	by the one person to the other person individually.

	Attributes
	-----------
	1. user_id : int
	    Id of a user who is sending message.
	2. name : str
	    Full name of user who is sending message.
	3. message : str
	    Content of a message sent by the user to other person.
	4. time : time
	    Time when the user sent message to other person.
	5. group_id : int
	    Group id is the room of two users are communicating.

	"""
	user_id = IntegerField()
	name = CharField(max_length=100)
	message = TextField()
	time = TimeField(auto_now=True)
	group_id = IntegerField()


class ChatGroupList(Model):
	"""
	ChatGroup model class

	This class contains instances of group created for one to one person chat
	or one to many person chat messaging.

	Attributes
	-----------
	1. date : date
	    Date when the group is created.
	2. time : time
	    Time when the group is created.
	3. name : str
	    Name of user who is creating a group for individual chatting
	    or group chatting.
	4. members : instahces of user
	    Members of user instances of group create including instance of
	    user also.
	5. group_name : str
	    Name of a group.
	6. description : str
	    Description of a group contains reason and objective that why the
	    user had create this group.
	7. mute_notifications ; bool
	    notification of a group.
	8. icon : image
	    Icon of a group.

	"""
	date = DateField(auto_now=True)
	time = TimeField(auto_now=True)
	name = CharField(max_length=100)
	members = ManyToManyField(CustomUser)
	group_name = CharField(max_length=500)
	description = TextField(blank=True, help_text="description of the group")
	mute_notifications = BooleanField(default=False, help_text="disable notification if true")
	icon = ImageField(help_text="Group icon", blank=True, upload_to="chartgroup")

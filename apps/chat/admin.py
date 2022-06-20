""" apps/chat/admin.py """
from django.contrib import admin
from .models import  (
	GroupMessage, ChatGroupList, OnetoOneMessage
)


admin.site.register(GroupMessage)

admin.site.register(ChatGroupList)

admin.site.register(OnetoOneMessage)

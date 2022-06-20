""" apps/user/models.py

This module contains two model classes
    * UserHeirarchy

"""
# Django core modules
from django.db.models import (
    Model,
    ForeignKey,
    CASCADE
)
from django.conf import settings


class Heirarchy(Model):
    """
    UserHeirarchy model class
    UserHeirarchy model is designed so that user can assign post that who will work
    under who. Like child user will work under parent user.
    
    For Example :
    If John Doe (Project Lead) is parent user than Sonal Doe (Web Developer)
    is child user.

    Attributes :
    --------------
    1. parent : CustomUser intance foreign key
        This is the instance of CustomUser.
    2. child : CustomUser instance foreign key
        This is the instance of CustomUser.

    """

    # Like Director is the parent of every user profile
    parent = ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=CASCADE,
        related_name='user_name',
        null=True
    )

    # Junior Web developer is the child of every user. 
    child = ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=CASCADE,
        related_name='child_name',
        null=True
    )

    def __str__(self):
        """ string representation of UserHeirarchy instance """
        return f'{self.parent} {self.child}'

    def update_parent(self, child_heirarchy):
        """
        This method updates child_heirarchy of a child.

        """
        self.parent = child_heirarchy.child
        self.save()

""" Models to store Justletic user accounts """

from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser, PermissionsMixin, BaseUserManager
)

class UserManager(BaseUserManager):

    """Manager to create Justletic user accounts"""

    def create_user(self,email, password=None):
        """Method to create a Justletic user account"""
        user = self.model(email=email)

        user.set_password(password)
        user.save()
        return user

class User(AbstractBaseUser, PermissionsMixin):

    """Model to store Justletic user accounts"""

    email = models.EmailField(unique=True)

    USERNAME_FIELD = 'email'

    objects = UserManager()

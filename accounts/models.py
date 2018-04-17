""" Models to store Justletic user accounts """

from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser, PermissionsMixin
)

class User(AbstractBaseUser, PermissionsMixin):

    """Model to store Justletic user accounts"""

    email = models.EmailField(unique=True)

    USERNAME_FIELD = 'email'

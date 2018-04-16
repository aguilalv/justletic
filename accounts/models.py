""" Models to store Justletic user accounts """

from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser, PermissionsMixin
)

class User(AbstractBaseUser, PermissionsMixin):

    """Tests for accounts models"""

    email = models.EmailField(unique=True)

    USERNAME_FIELD = 'email'

from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser, PermissionsMixin
)

class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)

    USERNAME_FIELD = 'email'

"""Factories to initialise Justletic Accounts database in tests"""
from factory import DjangoModelFactory, PostGenerationMethodCall
from .models import User

class UserFactory(DjangoModelFactory):

    """Factory to initialise Justletic Users database in tests"""

    class Meta:
        model = User

    email = 'edith@mailinator.com'
    password = PostGenerationMethodCall('set_password', f'{email[0]}pwd')

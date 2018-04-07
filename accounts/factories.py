from factory import DjangoModelFactory, PostGenerationMethodCall
from .models import User

class UserFactory(DjangoModelFactory):
    class Meta:
        model = User

    email = 'edith@mailinator.com'
    password = PostGenerationMethodCall('set_password', f'{email[0]}pwd')

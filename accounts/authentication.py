from django.shortcuts import get_object_or_404

from .models import User

class JustleticAuthenticationBackend(object):

    def authenticate(self, email, password):
        try:
            user = User.objects.get(email=email)
            if user.check_password(password):
                return user
            else:
                return None
        except User.DoesNotExist:
            return None

    def get_user(self,user_id):
        return get_object_or_404(User, pk=user_id)

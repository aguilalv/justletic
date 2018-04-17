"""Justletic authentication backend"""
from django.shortcuts import get_object_or_404

from .models import User

class JustleticAuthenticationBackend(object):

    """Justletic authentication backend"""

    @staticmethod
    def authenticate(email, password):
        """Check that user exists in the database and the password is correct"""
        try:
            user = User.objects.get(email=email)
            if user.check_password(password):
                return user
            return None
        except User.DoesNotExist:
            return None

    @staticmethod
    def get_user(user_id):
        """Return a user given its primary key (if the user exists)"""
        return get_object_or_404(User, pk=user_id)

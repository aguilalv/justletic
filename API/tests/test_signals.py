"""Unit tests for API signal handlers"""
from django.test import TestCase
from django.contrib import auth
from rest_framework.authtoken.models import Token

class SaveUserSignalTest(TestCase):

    """Tests for handler of the save user signal"""

    def create_user(self, email, password):
        """Helper function to create a user"""
        user_model = auth.get_user_model()
        self.existing_user = user_model.objects.create_user(
            username=email, email=email, password=password
        )

    def test_token_created_when_new_user_created(self):
        """Test API.signals.createusertoken creates new token when new user created"""
        self.create_user("edith@mailinator.com", "epwd")
        self.assertEqual(Token.objects.count(),1)
    
    def test_token_created_associated_with_new_user(self):
        """Test API.signals.createusertoken creates new token when new user created"""
        self.create_user("edith@mailinator.com", "epwd")
        self.assertIsNot(Token.objects.filter(user__pk=self.existing_user.pk).first(),None)

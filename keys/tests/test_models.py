"""Unit tests for Keys models"""
from django.test import TestCase
from django.contrib import auth

from ..models import Key


class KeyModelTest(TestCase):

    """Unit tests for keys Key model"""

    def test_saving_and_retrieving_keys(self):
        """Test that Key model can be saved and retrieved"""
        user_model = auth.get_user_model() 
        existing_user = user_model.objects.create_user(
            username='edith@mailinator.com',
            email='edith@mailinator.com',
            password='epwd'
        )
        key = Key(user=existing_user,token='abcd',strava_id='10')
        key.save()

        saved_key = Key.objects.all()[0]
        self.assertEqual(saved_key, key)
        self.assertEqual(saved_key.user, existing_user)
        self.assertEqual(saved_key.token, 'abcd') 
        self.assertEqual(saved_key.strava_id, '10') 

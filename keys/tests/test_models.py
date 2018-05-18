"""Unit tests for Keys models"""
from django.test import TestCase

from ..models import Key

from accounts.models import User
from accounts.factories import UserFactory as AccountsUserFactory

class KeyModelTest(TestCase):

    """Unit tests for keys Key model"""

    def test_saving_and_retrieving_keys(self):
        """Test that Key model can be saved and retrieved"""
        existing_user = AccountsUserFactory.create(
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

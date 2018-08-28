"""Unit tests for Keys models"""
from django.test import TestCase
from django.contrib import auth

from ..models import Key


class KeyModelTest(TestCase):

    """Unit tests for keys Key model"""

    def setUp(self):
        """Create a user in the database befor runinng each test"""
        user_model = auth.get_user_model()
        self.existing_user = user_model.objects.create_user(
            username="edith@mailinator.com",
            email="edith@mailinator.com",
            password="epwd",
        )

    def test_saving_and_retrieving_strava_keys(self):
        """Test keys.models.Key is saved and retrieved"""
        key = Key(
            user=self.existing_user, 
            token="abcd", 
            refresh_token="",
            strava_id="10", 
            service=Key.STRAVA
        )
        key.save()

        saved_key = Key.objects.all()[0]
        self.assertEqual(saved_key, key)
        self.assertEqual(saved_key.user, self.existing_user)
        self.assertEqual(saved_key.token, "abcd")
        self.assertEqual(saved_key.refresh_token, "")
        self.assertEqual(saved_key.strava_id, "10")
        self.assertEqual(saved_key.service, Key.STRAVA)

    def test_saving_and_retrieving_spotify_keys(self):
        """Test keys.models.Key is saved and retrieved"""
        key = Key(
            user=self.existing_user, 
            token="abcd",
            refresh_token="efgh",
            strava_id="", 
            service=Key.SPOTIFY,
        )
        key.save()

        saved_key = Key.objects.all()[0]
        self.assertEqual(saved_key, key)
        self.assertEqual(saved_key.user, self.existing_user)
        self.assertEqual(saved_key.token, "abcd")
        self.assertEqual(saved_key.refresh_token, "efgh")
        self.assertEqual(saved_key.strava_id, "")
        self.assertEqual(saved_key.service, Key.SPOTIFY)

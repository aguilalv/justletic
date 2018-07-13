"""Unit tests for API app serializers"""
from django.test import TestCase
from django.contrib import auth
from rest_framework.authtoken.models import Token

from keys.models import Key

class KeyDetailTest(TestCase):

    """Tests for API requests related to details of a 'Key' resource"""
    
    def create_user(self, email, password):
        """Helper function to create a user"""
        user_model = auth.get_user_model()
        self.existing_user = user_model.objects.create_user(
            username=email, email=email, password=password
        )

    def setUp(self):
        """Create a 'Key' resource in the database"""
        self.create_user("edith@mailinator.com", "epwd")
        self.existing_user_token, created = Token.objects.get_or_create(user=self.existing_user)
        self.existing_key = Key(
            user = self.existing_user,
            token = 'expected_token',
            strava_id = 'expected_strava_id'
        )
        self.existing_key.save()
    
    def test_GET_returns_status_200_for_right_token(self):
        """Test API.views.KeyDetail returns status 200 when receives correct token"""
        response = self.client.get("/API/key/", HTTP_AUTHORIZATION = f'Token {self.existing_user_token}')
        self.assertEqual(response.status_code, 200)

    def test_GET_returns_status_401_when_no_token(self):
        """Test API.views.KeyDetail returns status 401 when no token received"""
        response = self.client.get("/API/key/")
        self.assertEqual(response.status_code, 401)

    def test_GET_returns_status_401_for_wrong_token(self):
        """Test API.views.KeyDetail returns status 401 when incorrect token received"""
        response = self.client.get("/API/key/", HTTP_AUTHORIZATION = f'Token wrongtoken1234')
        self.assertEqual(response.status_code, 401)

    def test_GET_returns_key_for_right_token(self):
        """Test API.views.KeyDetail returns Key associated to authenticated athlete"""
        response = self.client.get("/API/key/", HTTP_AUTHORIZATION = f'Token {self.existing_user_token}')
        received = response.content.decode("utf-8")
        self.assertIn('"token":"expected_token"',received)
        self.assertIn('"strava_id":"expected_strava_id"',received)
    
    def test_GET_returns_error_when_no_token(self):
        """Test API.views.KeyDetail error when no token received"""
        response = self.client.get("/API/key/")
        converted = response.content.decode("utf-8")
        self.assertEqual(
            converted,
            '{"detail":"Authentication credentials were not provided."}' 
        )

    def test_GET_returns_error_when_for_wrong_token(self):
        """Test API.views.KeyDetail error when wrong token received"""
        response = self.client.get("/API/key/", HTTP_AUTHORIZATION = f'Token wrongtoken1234')
        converted = response.content.decode("utf-8")
        self.assertEqual(converted,'{"detail":"Invalid token."}')


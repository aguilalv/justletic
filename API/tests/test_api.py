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
            token = 'test_token',
            strava_id = 'test_strava_id'
        )
        self.existing_key.save()
    
    def test_GET_returns_status_200_for_right_token(self):
        """Test API.views.KeyDetail returns status 200 when receives correct token"""
        response = self.client.get("/API/key/", HTTP_AUTHORIZATION = f'Token {self.existing_user_token}')
        self.assertEqual(response.status_code, 200)

    def test_GET_returns_status_401_when_no_token(self):
        """Test API.views.KeyDetail returns status 401 when receives correct token"""
        response = self.client.get("/API/key/")
        self.assertEqual(response.status_code, 401)



#    def test_GET_returns_key_for_authenticated_user(self):
#        """Test API.views.KeyDetail returns Key associated to authenticated athlete"""
#        response = self.client.get("/API/Key/")
#        #self.assertTemplateUsed(response, "login.html")
#        self.fail("Finish this test!!")
    

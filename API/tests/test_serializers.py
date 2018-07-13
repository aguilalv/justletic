"""Unit tests for API serializers"""
from django.test import TestCase
from django.contrib import auth

from keys.models import Key
from API.serializers import KeySerializer

class KeySerializerTest(TestCase):

    """Tests for API serializers of a 'Key' resource"""
    
    def create_user(self, email, password):
        """Helper function to create a user"""
        user_model = auth.get_user_model()
        self.existing_user = user_model.objects.create_user(
            username=email, email=email, password=password
        )

    def setUp(self):
        """Create a 'Key' resource in the database"""
        self.create_user("edith@mailinator.com", "epwd")
        self.existing_key = Key(
            user = self.existing_user,
            token = 'expected_token',
            strava_id = 'expected_strava_id'
        )
        self.existing_key.save()
    
    def test_converts_key_model_to_dictionary(self):
        """Test API.serializers.KeySerializer converts a 'Key' object to a dictionary correctly"""
        serializer = KeySerializer(self.existing_key)
        self.assertEqual(
            {'token':self.existing_key.token,'strava_id':self.existing_key.strava_id},
            serializer.data
        )
    
#    def test_converts_dictionary_to_model(self):
#        """Test API.serializers.KeySerializer converts a dictionary into a 'Key' object"""
#        serializer = KeySerializer(self.existing_key)
#        self.assertEqual(
#            {'token':self.existing_key.token,'strava_id':self.existing_key.strava_id},
#            serializer.data
#        )

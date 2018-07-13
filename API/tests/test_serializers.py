"""Unit tests for API serializers"""
from django.test import TestCase
from django.contrib import auth
from rest_framework.utils.serializer_helpers import ReturnList

from keys.models import Key
from API.serializers import KeySerializer, UserSerializer

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

class UserSerializerTest(TestCase):

    """Tests for API serializers of a 'User' resource"""
    
    def create_user(self, email, password):
        """Helper function to create a user"""
        user_model = auth.get_user_model()
        return user_model.objects.create_user(
            username=email, email=email, password=password
        )

    def setUp(self):
        """Create a 'Key' resource in the database"""
        self.first_user = self.create_user("edith@mailinator.com", "epwd")
        self.second_user = self.create_user("joe@mailinator.com", "jpwd")
        self.third_user = self.create_user("tom@mailinator.com", "tpwd")
    
    def test_converts_user_model_to_dictionary(self):
        """Test API.serializers.UserSerializer converts a 'User' object to a dictionary correctly"""
        serializer = UserSerializer(self.first_user)
        self.assertEqual(
            {
                'id':self.first_user.id,
                'username':self.first_user.username
            },
            serializer.data
        )
    
    def test_converts_queryset_to_list(self):
        """Test API.serializers.UserSerializer converts a 'User' queryset to a list correctly"""
        user_model = auth.get_user_model()
        serializer = UserSerializer(user_model.objects.all(),many=True)
        self.assertEqual(len(serializer.data),3)
        self.assertIs(type(serializer.data),ReturnList)

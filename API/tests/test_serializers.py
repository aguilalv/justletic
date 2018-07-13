"""Unit tests for API serializers"""
from django.test import TestCase
from django.contrib import auth
from rest_framework.utils.serializer_helpers import ReturnList
from rest_framework.authtoken.models import Token

from keys.models import Key
from API.serializers import KeySerializer, UserSerializer, TokenSerializer

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

class TokenSerializerTest(TestCase):

    """Tests for API serializers of a 'Token' resource"""
    
    def create_user(self, email, password):
        """Helper function to create a user"""
        user_model = auth.get_user_model()
        return user_model.objects.create_user(
            username=email, email=email, password=password
        )
    
    def setUp(self):
        """Create several users in the database"""
        self.existing_users = []
        self.existing_users_tokens = []
        for i in range(3):
            self.existing_users.append(
                self.create_user(f"{i}@mailinator.com", f"{i}pwd")
            )
            token, created = Token.objects.get_or_create(user=self.existing_users[i])
            self.existing_users_tokens.append(token)

    def test_converts_token_model_to_dictionary(self):
        """Test API.serializers.TokenSerializer converts a 'Token' object to a dictionary correctly"""
        serializer = TokenSerializer(self.existing_users_tokens[0])
        self.assertEqual(
            self.existing_users_tokens[0].key,
            serializer.data.get('key')
        )
        self.assertEqual(
            self.existing_users_tokens[0].user_id,
            serializer.data.get('user_id')
        )
    
    def test_converts_token_queryset_to_list(self):
        """Test API.serializers.TokenSerializer converts a 'Token' queryset to a list correctly"""
        serializer = TokenSerializer(Token.objects.all(),many=True)
        self.assertEqual(
            len(serializer.data),
            len(self.existing_users_tokens)
        )
        self.assertIs(type(serializer.data),ReturnList)

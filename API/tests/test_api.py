"""Unit tests for API app views"""
import json

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

    def test_GET_returns_error_when_wrong_token(self):
        """Test API.views.KeyDetail returns error for wrong token"""
        response = self.client.get("/API/key/", HTTP_AUTHORIZATION = f'Token wrongtoken1234')
        converted = response.content.decode("utf-8")
        self.assertEqual(converted,'{"detail":"Invalid token."}')

class UserListTest(TestCase):
    
    """Tests for API requests for User Lists"""
    
    def create_user(self, email, password):
        """Helper function to create a user"""
        user_model = auth.get_user_model()
        return user_model.objects.create_user(
            username=email, email=email, password=password
        )

    def setUp(self):
        """Create two standard users and a root user in the database"""
        self.existing_users = []
        self.existing_users_tokens = []
        for i in range(3):
            self.existing_users.append(
                self.create_user(f"{i}@mailinator.com", f"{i}pwd")
            )
            token, created = Token.objects.get_or_create(user=self.existing_users[i])
            self.existing_users_tokens.append(token)
        
        self.root_user = self.create_user(f"root@mailinator.com", f"rootpwd")
        self.root_user.is_staff = True
        self.root_user.save()
        self.root_user_token, created = Token.objects.get_or_create(user=self.root_user)
    
    def test_GET_returns_status_200_for_right_token(self):
        """Test API.views.KeyDetail returns status 200 when receives correct token"""
        response = self.client.get("/API/user/", HTTP_AUTHORIZATION = f'Token {self.root_user_token}')
        self.assertEqual(response.status_code, 200)

    def test_GET_returns_status_401_when_no_token(self):
        """Test API.views.KeyDetail returns status 401 when no token received"""
        response = self.client.get("/API/user/")
        self.assertEqual(response.status_code, 401)

    def test_GET_returns_status_401_for_wrong_token(self):
        """Test API.views.KeyDetail returns status 401 when incorrect token received"""
        response = self.client.get("/API/user/", HTTP_AUTHORIZATION = f'Token wrongtoken1234')
        self.assertEqual(response.status_code, 401)

    def test_GET_returns_status_403_for_non_root_token(self):
        """Test API.views.KeyDetail returns status 403 when token with no root permissions received"""
        response = self.client.get("/API/user/", HTTP_AUTHORIZATION = f'Token {self.existing_users_tokens[0]}')
        self.assertEqual(response.status_code, 403)
    
    def test_GET_returns_user_list_for_right_token(self):
        """Test API.views.KeyDetail returns list of users when correct token received"""
        response = self.client.get("/API/user/", HTTP_AUTHORIZATION = f'Token {self.root_user_token}')
        received = response.content.decode("utf-8")
        data_received = json.loads(received)
        assert len(data_received.keys()) == 1
        assert 'users' in data_received.keys()
        list_received = data_received['users']
        # Total users will be list of regular users and the root user
        self.assertEqual(len(list_received),len(self.existing_users)+1)
        for i, user in enumerate(self.existing_users):
            self.assertEqual(list_received[i].get('id'),user.id)
            self.assertEqual(list_received[i].get('username'),user.username)

    def test_GET_returns_error_when_wrong_token(self):
        """Test API.views.UserList returns error for wrong token"""
        response = self.client.get("/API/user/", HTTP_AUTHORIZATION = f'Token wrongtoken1234')
        converted = response.content.decode("utf-8")
        self.assertEqual(converted,'{"detail":"Invalid token."}')

    def test_GET_returns_error_when_no_token(self):
        """Test API.views.UserList returns error for wrong token"""
        response = self.client.get("/API/user/")
        converted = response.content.decode("utf-8")
        self.assertEqual(
            converted,
            '{"detail":"Authentication credentials were not provided."}' 
        )

    def test_GET_returns_error_when_non_admin_token(self):
        """Test API.views.UserList returns error for wrong token"""
        response = self.client.get("/API/user/", HTTP_AUTHORIZATION = f'Token {self.existing_users_tokens[0]}')
        converted = response.content.decode("utf-8")
        self.assertEqual(converted,'{"detail":"You do not have permission to perform this action."}')

class TokenListTest(TestCase):
    
    """Tests for API requests for Token Lists"""

    def create_user(self, email, password):
        """Helper function to create a user"""
        user_model = auth.get_user_model()
        return user_model.objects.create_user(
            username=email, email=email, password=password
        )

    def setUp(self):
        """Create two standard users and a root user in the database"""
        self.existing_users = []
        self.existing_users_tokens = []
        for i in range(3):
            self.existing_users.append(
                self.create_user(f"{i}@mailinator.com", f"{i}pwd")
            )
            token, created = Token.objects.get_or_create(user=self.existing_users[i])
            self.existing_users_tokens.append(token)
        
        self.root_user = self.create_user(f"root@mailinator.com", f"rootpwd")
        self.root_user.is_staff = True
        self.root_user.save()
        self.root_user_token, created = Token.objects.get_or_create(user=self.root_user)

    def test_GET_returns_status_200_for_right_token(self):
        """Test API.views.TokenList returns status 200 when receives correct token"""
        response = self.client.get("/API/token/", HTTP_AUTHORIZATION = f'Token {self.root_user_token}')
        self.assertEqual(response.status_code, 200)

    def test_GET_returns_status_401_when_no_token(self):
        """Test API.views.TokenList returns status 401 when no token received"""
        response = self.client.get("/API/token/")
        self.assertEqual(response.status_code, 401)

    def test_GET_returns_status_401_for_wrong_token(self):
        """Test API.views.TokenList returns status 401 when incorrect token received"""
        response = self.client.get("/API/token/", HTTP_AUTHORIZATION = f'Token wrongtoken1234')
        self.assertEqual(response.status_code, 401)

    def test_GET_returns_status_403_for_non_root_token(self):
        """Test API.views.TokenList returns status 403 when token with no root permissions received"""
        response = self.client.get("/API/token/", HTTP_AUTHORIZATION = f'Token {self.existing_users_tokens[0]}')
        self.assertEqual(response.status_code, 403)
    
    def test_GET_returns_token_list_for_right_token(self):
        """Test API.views.TokenList returns list of tokens when correct token received"""
        response = self.client.get("/API/token/", HTTP_AUTHORIZATION = f'Token {self.root_user_token}')
        received = response.content.decode("utf-8")
        data_received = json.loads(received)
        assert len(data_received.keys()) == 1
        assert 'tokens' in data_received.keys()
        list_received = data_received['tokens']
        # Total users will be list of regular users and the root user
        self.assertEqual(len(list_received),len(self.existing_users_tokens)+1)
        for i, user in enumerate(self.existing_users):
            self.assertEqual(list_received[i].get('user_id'),user.id)
            self.assertEqual(
                list_received[i].get('key'),
                self.existing_users_tokens[i].key
            )
    
    def test_GET_returns_error_when_wrong_token(self):
        """Test API.views.TokenList returns error for wrong token"""
        response = self.client.get("/API/token/", HTTP_AUTHORIZATION = f'Token wrongtoken1234')
        converted = response.content.decode("utf-8")
        self.assertEqual(converted,'{"detail":"Invalid token."}')

    def test_GET_returns_error_when_no_token(self):
        """Test API.views.TokenList returns error for wrong token"""
        response = self.client.get("/API/token/")
        converted = response.content.decode("utf-8")
        self.assertEqual(
            converted,
            '{"detail":"Authentication credentials were not provided."}' 
        )

    def test_GET_returns_error_when_non_admin_token(self):
        """Test API.views.TokenList returns error for wrong token"""
        response = self.client.get("/API/token/", HTTP_AUTHORIZATION = f'Token {self.existing_users_tokens[0]}')
        converted = response.content.decode("utf-8")
        self.assertEqual(converted,'{"detail":"You do not have permission to perform this action."}')

"""Unit tests for logs for accounts app views"""
import os
from unittest.mock import patch, call

from django.test import TestCase
from django.contrib import auth

class LoginViewTest(TestCase):

    """Tests for logs in Login view"""

    def setUp(self):
        """Create a user in the database befor runinng each test"""
        user_model = auth.get_user_model()
        self.existing_user = user_model.objects.create_user(
            "edith@mailinator.com", "edith@mailinator.com", "epwd"
        )

    @patch("accounts.views.logger")
    def test_correct_password_calls_logger(self,mock_logger):
        """Test login view calls logger when receives correct password"""
        self.client.post(
            "/accounts/login",
            data={"email": "edith@mailinator.com", "password": "epwd"},
        )
#        user = auth.get_user(self.client)
        self.assertEqual(mock_logger.info.called,True)
        message_used = mock_logger.info.call_args
        self.assertEqual(call("accounts.views.login - end"),message_used)

#    def test_wrong_password_XXX(self):
#
#    def test_non_existing_user_XXX(self):

class LogoutViewTest(TestCase):

    """Tests for logs in Login view"""

    def setUp(self):
        user_model = auth.get_user_model()
        self.existing_user = user_model.objects.create_user(
            "edith@mailinator.com", "edith@mailinator.com", "epwd"
        )
        auth.authenticate(
            username=self.existing_user.email, password=self.existing_user.password
        )
        self.client.login(username="edith@mailinator.com", password="epwd")

    @patch("accounts.views.logger")
    def test_calls_logger(self,mock_logger):
        """Test logout view calls logger"""
        self.client.post("/accounts/logout")
        self.assertEqual(mock_logger.info.called,True)
        message_used = mock_logger.info.call_args
        self.assertEqual(call("accounts.views.logout - end"),message_used)

class CreateNewStravaUserTest(TestCase):

    """Tests for logs in Create New Strava User view"""
    @patch("accounts.views.logger")
    def test_user_does_not_exist_calls_logger(self,mock_logger):
        """Test CreateNewStravaUser view calls logger when called for user that does not exist"""
        response = self.client.post(
            "/accounts/new/strava", data={"email": "edith@mailinator.com"}
        )
        self.assertEqual(mock_logger.info.called,True)
        message_used = mock_logger.info.call_args
        self.assertEqual(call("accounts.views.createnewstravauser - end"),message_used)

#    def test_does_not_create_user_if_exists(self):
#        """ Test that create new strava user does not create a new user if one with requested email already exists """
#        self.fail()

#    def test_redirects_to_login_page_if_user_exists(self):

"""Unit tests for logs for accounts app views"""
import os
from unittest.mock import patch, call, Mock

from django.test import TestCase
from django.contrib import auth

class LoginViewTest(TestCase):

    """Tests for logs in Login view"""

    def setUp(self):
        """Create a user in the database before runinng each test"""
        user_model = auth.get_user_model()
        self.existing_user = user_model.objects.create_user(
            "edith@mailinator.com", "edith@mailinator.com", "epwd"
        )

    @patch("accounts.views.logger.bind")
    def test_correct_password_calls_logger(self,mock_logger_bind):
        """Test accounts.views.login calls logger info when receives correct password"""
        bound_logger = Mock()
        mock_logger_bind.return_value=bound_logger
        self.client.post(
            "/accounts/login",
            data={"email": "edith@mailinator.com", "password": "epwd"},
        )
        self.assertEqual(bound_logger.info.called,True)
        message_used = bound_logger.info.call_args
        self.assertEqual(call("Successful login"),message_used)

    @patch("accounts.views.logger.bind")
    def test_correct_password_binds_user_name(self,mock_logger_bind):
        """Test accounts.views.login binds username when receives correct password"""
        self.client.post(
            "/accounts/login",
            data={"email": "edith@mailinator.com", "password": "epwd"},
        )
        self.assertEqual(mock_logger_bind.called,True)
        data_added = mock_logger_bind.call_args
        self.assertEqual(call(user="edith@mailinator.com"),data_added)

#    def test_wrong_password_XXX(self):
#
#    def test_non_existing_user_XXX(self):

class LogoutViewTest(TestCase):

    """Tests for logs in logout view"""

    def setUp(self):
        """Create a user in the database before runinng each test"""
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
        """Test accounts.views.logout calls logger info"""
        self.client.post("/accounts/logout")
        self.assertEqual(mock_logger.info.called,True)
        message_used = mock_logger.info.call_args
        self.assertEqual(call("Logout"),message_used)

class CreateNewStravaUserTest(TestCase):

    """Tests for logs in Create New Strava User view"""
    @patch("accounts.views.logger.bind")
    def test_user_does_not_exist_calls_logger(self,mock_logger_bind):
        """Test accounts.views.CreateNewStravaUser calls logger when called for user that does not exist"""
        bound_logger = Mock()
        mock_logger_bind.return_value=bound_logger
        response = self.client.post(
            "/accounts/new/strava", data={"email": "edith@mailinator.com"}
        )
        self.assertEqual(len(bound_logger.info.mock_calls),2)
        self.assertEqual(
            call("User created"),
            bound_logger.info.mock_calls[0]
        )
        self.assertEqual(
            call("Successful login"),
            bound_logger.info.mock_calls[1]
        )
            
#    def test_redirects_to_login_page_if_user_exists(self):


class ChangePasswordViewTest(TestCase):

    """Tests for logs in accounts change_password view"""

    def setUp(self):
        """Create a user in the database before runinng each test"""
        user_model = auth.get_user_model()
        self.existing_user = user_model.objects.create_user(
            "edith@mailinator.com", "edith@mailinator.com", "epwd"
        )

    @patch("accounts.views.logger.bind")
    def test_post_calls_logger_if_user_logged_in(self,mock_logger_bind):
        """Test accounts.views.change_password calls logger.info (usr logged in)"""
        bound_logger = Mock()
        mock_logger_bind.return_value=bound_logger
        self.client.login(username=self.existing_user.email, password="epwd")
        response = self.client.post(
            "/accounts/change-password",
            data={"password": "newpwd","next": "home"},
        )
        self.assertEqual(bound_logger.info.called,True)
        message_used = bound_logger.info.call_args
        self.assertEqual(call("Password changed"),message_used)

    @patch("accounts.views.logger.bind")
    def test_post_binds_username(self,mock_logger_bind):
        """Test accounts.views.change_password binds username (user logged in)"""
        self.client.login(username=self.existing_user.email, password="epwd")
        response = self.client.post(
            "/accounts/change-password",
            data={"password": "newpwd","next": "home"},
        )
        self.assertEqual(mock_logger_bind.called,True)
        data_added = mock_logger_bind.call_args
        self.assertEqual(call(user="edith@mailinator.com"),data_added)

"""Unit tests for accounts app views"""
import os
from urllib.parse import urlencode
from unittest.mock import patch

from django.test import TestCase
from django.utils.html import escape
from django.contrib import auth
from django.urls import reverse

from ..views import LOGIN_ERROR

from utils.strava_utils import STRAVA_CLIENT_ID, STRAVA_AUTHORIZE_URL
from keys.forms import HeroForm


class LoginViewTest(TestCase):

    """Tests for accounts login view"""

    def setUp(self):
        """Create a user in the database befor runinng each test"""
        user_model = auth.get_user_model()
        self.existing_user = user_model.objects.create_user(
            "edith@mailinator.com", "edith@mailinator.com", "epwd"
        )

    def test_post_logs_user_in_if_password_correct(self):
        """Test that a POST request with existing user and correct password, logs the user in"""
        self.client.post(
            "/accounts/login",
            data={"email": "edith@mailinator.com", "password": "epwd"},
        )
        user = auth.get_user(self.client)
        self.assertTrue(user.is_authenticated)
        self.assertEqual(user.email, self.existing_user.email)

    #    def test_post_success_redirects_to_user_summary(self):

    def test_post_success_renders_home_page(self):
        """Test that a successful login renders the home page"""
        response = self.client.post(
            "/accounts/login",
            data={"email": "edith@mailinator.com", "password": "epwd"},
        )
        self.assertTemplateUsed(response, "home.html")

    def test_post_wrong_password_renders_home_page(self):
        """Test that a post request with existing user and wrong password renders the home page"""
        response = self.client.post(
            "/accounts/login",
            data={"email": "edith@mailinator.com", "password": "wrongpwd"},
        )
        self.assertTemplateUsed(response, "home.html")

    def test_post_wrong_password_shows_error(self):
        """Test that a post request with existing user and wrong password displays an error"""
        response = self.client.post(
            "/accounts/login",
            data={"email": "edith@mailinator.com", "password": "wrongpwd"},
        )
        expected_error = escape(LOGIN_ERROR)
        self.assertContains(response, expected_error)

    def test_post_non_existing_user_renders_home_page(self):
        """Test that a post request with non existing user renders the home page"""
        response = self.client.post(
            "/accounts/login",
            data={"email": "non_existent@non.com", "password": "wrongpwd"},
        )
        self.assertTemplateUsed(response, "home.html")

    def test_post_non_existing_user_shows_error(self):
        """Test that a post request with non existing user shows an error message"""
        response = self.client.post(
            "/accounts/login",
            data={"email": "non_existent@non.com", "password": "wrongpwd"},
        )
        expected_error = escape(LOGIN_ERROR)
        self.assertContains(response, expected_error)


class LogoutViewTest(TestCase):

    """Tests for accounts logout view"""

    def setUp(self):
        user_model = auth.get_user_model()
        self.existing_user = user_model.objects.create_user(
            "edith@mailinator.com", "edith@mailinator.com", "epwd"
        )
        auth.authenticate(
            username=self.existing_user.email, password=self.existing_user.password
        )
        self.client.login(username="edith@mailinator.com", password="epwd")

    def test_redirects_to_home_page(self):
        """Test that logout view redirects to the home page"""
        response = self.client.post("/accounts/logout")
        self.assertRedirects(response, reverse("home"))

    def test_logs_user_out(self):
        """Test that logout view logs the current user out"""
        self.client.post("/accounts/logout")
        user = auth.get_user(self.client)
        self.assertFalse(user.is_authenticated)


class CreateNewStravaUserTest(TestCase):

    """ Tests for accounts create_new_strava_user view """

    def test_creates_user_if_doesnt_exist(self):
        """ Test that create new strava user view creates a new user if one with the requested email address does not exist """
        user_model = auth.get_user_model()
        self.assertEqual(user_model.objects.count(), 0)

        self.client.post("/accounts/new/strava", data={"email": "edith@mailinator.com"})

        self.assertEqual(user_model.objects.count(), 1)
        new_user = user_model.objects.first()
        self.assertEqual(new_user.email, "edith@mailinator.com")

    def test_logs_user_in(self):
        """ Test that create new strava user view logs in the user with the requested email address  """
        self.client.post("/accounts/new/strava", data={"email": "edith@mailinator.com"})

        user = auth.get_user(self.client)
        self.assertTrue(user.is_authenticated)
        self.assertEqual(user.email, "edith@mailinator.com")

    @patch("accounts.views.strava_oauth_code_request_url")
    def test_gets_url_to_request_code_from_strava_utils_module(self, mock):
        """Test that create new strava user view calls the strava utils
        helper module to get the url to request an oAuth code"""
        mock.return_value = "www.google.com"
        response = self.client.post(
            "/accounts/new/strava", data={"email": "edith@mailinator.com"}
        )
        self.assertTrue(mock.called)

    @patch("accounts.views.strava_oauth_code_request_url")
    def test_redirects_to_url_returned_by_strava_utils_module(self, mock):
        """Test that create new strava user view redirects to the url
        returned by the strava utils helper module"""
        mock.return_value = "http://www.google.com"
        response = self.client.post(
            "/accounts/new/strava", data={"email": "edith@mailinator.com"}
        )
        self.assertRedirects(
            response, "http://www.google.com", fetch_redirect_response=False
        )

    def test_renders_home_if_empty_email(self):
        """ Test that create new strava user view renders home
        if it receives an empty email"""
        response = self.client.post("/accounts/new/strava", data={"email": ""})
        self.assertTemplateUsed(response, "home.html")

    def test_shows_message_if_empty_email(self):
        """ Test that create new strava user view shows an error message
        if it receives an empty email"""
        expected_error = escape(HeroForm.EMAIL_FIELD_ERROR)
        response = self.client.post("/accounts/new/strava", data={"email": ""})
        self.assertContains(response, expected_error)

    def test_renders_home_if_invalid_email_format(self):
        """ Test that create new strava user view renders home
        if it receives an empty email"""
        response = self.client.post(
            "/accounts/new/strava", data={"email": "wrong_format_email"}
        )
        self.assertTemplateUsed(response, "home.html")

    def test_shows_message_if_empty_email(self):
        """ Test that create new strava user view shows an error message
        if it receives an empty email"""
        expected_error = escape(HeroForm.EMAIL_FIELD_ERROR)
        response = self.client.post(
            "/accounts/new/strava", data={"email": "wrong_format_email"}
        )
        self.assertContains(response, expected_error)


#    def test_does_not_create_user_if_exists(self):
#        """ Test that create new strava user does not create a new user if one with requested email already exists """
#        self.fail()

#    def test_redirects_to_login_page_if_user_exists(self):

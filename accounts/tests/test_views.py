"""Unit tests for accounts app views"""
import os
from urllib.parse import urlencode
from unittest.mock import patch

from django.test import TestCase
from django.utils.html import escape
from django.contrib import auth
from django.urls import reverse

from ..views import LOGIN_ERROR
from ..forms import LoginForm

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

    def test_get_renders_login_template(self):
        """Test accounts.views.login renders login template"""
        response = self.client.get("/accounts/login")
        self.assertTemplateUsed(response, "login.html")

    def test_get_uses_login_form(self):
        """Test accounts.views.login uses login form"""
        response = self.client.get("/accounts/login")
        form_used = response.context['login_form']
        self.assertIsInstance(form_used, LoginForm)
        
    def test_post_logs_user_in_if_password_correct(self):
        """Test accounts.views.login logs the user in when receives existing user and correct password"""
        self.client.post(
            "/accounts/login",
            data={"email": "edith@mailinator.com", "password": "epwd"},
        )
        user = auth.get_user(self.client)
        self.assertTrue(user.is_authenticated)
        self.assertEqual(user.email, self.existing_user.email)

    #    def test_post_success_redirects_to_user_summary(self):

    def test_post_success_renders_home_page(self):
        """Test accounts.views.login renders the home page after successful login"""
        response = self.client.post(
            "/accounts/login",
            data={"email": "edith@mailinator.com", "password": "epwd"},
        )
        self.assertTemplateUsed(response, "home.html")

    def test_post_wrong_password_renders_home_page(self):
        """Test accounts.views.loging renders the home page when receives existing user and wrong password"""
        response = self.client.post(
            "/accounts/login",
            data={"email": "edith@mailinator.com", "password": "wrongpwd"},
        )
        self.assertTemplateUsed(response, "home.html")

    def test_post_wrong_password_shows_error(self):
        """Test accounts.views.login renders expectec error when receives existing user and wrong password"""
        response = self.client.post(
            "/accounts/login",
            data={"email": "edith@mailinator.com", "password": "wrongpwd"},
        )
        expected_error = escape(LOGIN_ERROR)
        self.assertContains(response, expected_error)

    def test_post_non_existing_user_renders_home_page(self):
        """Test accounts.views.login renders home page when receives non-existing user"""
        response = self.client.post(
            "/accounts/login",
            data={"email": "non_existent@non.com", "password": "wrongpwd"},
        )
        self.assertTemplateUsed(response, "home.html")

    def test_post_non_existing_user_shows_error(self):
        """Test accounts.views.login shows expected message when receives non-existing user"""
        response = self.client.post(
            "/accounts/login",
            data={"email": "non_existent@non.com", "password": "wrongpwd"},
        )
        expected_error = escape(LOGIN_ERROR)
        self.assertContains(response, expected_error)


class LogoutViewTest(TestCase):

    """Tests for accounts logout view"""

    def setUp(self):
        """Create a user in the database befor runinng each test"""
        user_model = auth.get_user_model()
        self.existing_user = user_model.objects.create_user(
            "edith@mailinator.com", "edith@mailinator.com", "epwd"
        )
        auth.authenticate(
            username=self.existing_user.email, password=self.existing_user.password
        )
        self.client.login(username="edith@mailinator.com", password="epwd")

    def test_redirects_to_home_page(self):
        """Test accounts.views.logout redirects to home page"""
        response = self.client.post("/accounts/logout")
        self.assertRedirects(response, reverse("home"))

    def test_logs_user_out(self):
        """Test accounts.views.logout logs current user out"""
        self.client.post("/accounts/logout")
        user = auth.get_user(self.client)
        self.assertFalse(user.is_authenticated)


class CreateNewStravaUserTest(TestCase):

    """ Tests for accounts create_new_strava_user view """

    def test_creates_user_if_doesnt_exist(self):
        """ Test accounts.views.create_new_strava_user creates new user if one with the requested email address does not exist """
        user_model = auth.get_user_model()
        self.assertEqual(user_model.objects.count(), 0)

        self.client.post("/accounts/new/strava", data={"email": "edith@mailinator.com"})

        self.assertEqual(user_model.objects.count(), 1)
        new_user = user_model.objects.first()
        self.assertEqual(new_user.email, "edith@mailinator.com")

    def test_logs_user_in(self):
        """ Test accounts.views.create_new_strava_user logs in user with requested email address"""
        self.client.post("/accounts/new/strava", data={"email": "edith@mailinator.com"})

        user = auth.get_user(self.client)
        self.assertTrue(user.is_authenticated)
        self.assertEqual(user.email, "edith@mailinator.com")

    @patch("accounts.views.strava_oauth_code_request_url")
    def test_gets_url_to_request_code_from_strava_utils_module(self, mock):
        """Test accounts.views.create_new_strava_user calls strava utils helper module to get url to request oAuth code"""
        mock.return_value = "www.google.com"
        response = self.client.post(
            "/accounts/new/strava", data={"email": "edith@mailinator.com"}
        )
        self.assertTrue(mock.called)

    @patch("accounts.views.strava_oauth_code_request_url")
    def test_redirects_to_url_returned_by_strava_utils_module(self, mock):
        """Test accounts.views.create_new_strava_user redirects to url returned by strava utils helper module"""
        mock.return_value = "http://www.google.com"
        response = self.client.post(
            "/accounts/new/strava", data={"email": "edith@mailinator.com"}
        )
        self.assertRedirects(
            response, "http://www.google.com", fetch_redirect_response=False
        )

    def test_renders_home_if_empty_email(self):
        """Test accounts.views.create_new_strava_user renders home if receives empty email"""
        response = self.client.post("/accounts/new/strava", data={"email": ""})
        self.assertTemplateUsed(response, "home.html")

    def test_shows_message_if_empty_email(self):
        """Test accounts.views.create_new_strava_user shows error message if receives empty email"""
        expected_error = escape(HeroForm.EMAIL_FIELD_ERROR)
        response = self.client.post("/accounts/new/strava", data={"email": ""})
        self.assertContains(response, expected_error)

    def test_renders_home_if_invalid_email_format(self):
        """ Test accounts.views.create_new_strava_user renders home if receives email in an invalid format"""
        response = self.client.post(
            "/accounts/new/strava", data={"email": "wrong_format_email"}
        )
        self.assertTemplateUsed(response, "home.html")

    def test_shows_message_if_invalid_email_format(self):
        """ Test accounts.views.create_new_strava_user shows error message if receives email in an invalid format"""
        expected_error = escape(HeroForm.EMAIL_FIELD_ERROR)
        response = self.client.post(
            "/accounts/new/strava", data={"email": "wrong_format_email"}
        )
        self.assertContains(response, expected_error)


#    def test_does_not_create_user_if_exists(self):
#        """ Test that create new strava user does not create a new user if one with requested email already exists """
#        self.fail()

#    def test_redirects_to_login_page_if_user_exists(self):


class ChangePasswordViewTest(TestCase):

    """Tests for accounts change_password view"""

    def setUp(self):
        """Create a user in the database befor runinng each test"""
        user_model = auth.get_user_model()
        self.existing_user = user_model.objects.create_user(
            "edith@mailinator.com", "edith@mailinator.com", "epwd"
        )

    def test_post_sets_password_to_received(self):
        """Test accounts.views.change_password set received password for logged in user"""
        auth.authenticate(
            username=self.existing_user.email, password=self.existing_user.password
        )
        self.client.login(username=self.existing_user.email, password="epwd")
        response = self.client.post(
            "/accounts/change-password",
            data={"password": "newpwd","next": "home"},
        )
        user_model = auth.get_user_model()
        user_affected = user_model.objects.filter(email=self.existing_user.email)[0]
        self.assertTrue(user_affected.check_password("newpwd"))

    def test_redirects_to_next(self):
        """Test accounts.views.change_password redirects to url received as next"""
        expected_redirect = "home"
        auth.authenticate(
            username=self.existing_user.email, password=self.existing_user.password
        )
        self.client.login(username=self.existing_user.email, password="epwd")
        response = self.client.post(
            "/accounts/change-password",
            data={"password": "newpwd","next": expected_redirect},
        )
        self.assertRedirects(response, reverse(expected_redirect))

    def test_same_user_is_logged_in_after_call(self):
        """Test accounts.views.change_password maintains the same user logged in in the session after being called"""
        auth.authenticate(
            username=self.existing_user.email, password=self.existing_user.password
        )
        self.client.login(username=self.existing_user.email, password="epwd")
        response = self.client.post(
            "/accounts/change-password",
            data={"password": "newpwd","next": "home"},
        )
        logged_in_user = auth.get_user(self.client)
        self.assertEqual(logged_in_user,self.existing_user)

#   def test_xxx_when_no_user_logged_in(self):


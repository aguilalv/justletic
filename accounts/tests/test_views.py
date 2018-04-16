"""Unit tests for accounts app views"""
from django.test import TestCase
from django.utils.html import escape
from django.contrib import auth
from django.urls import reverse

from keys.factories import UserFactory as KeysUserFactory
from ..views import LOGIN_ERROR
from ..factories import UserFactory as AccountsUserFactory

class LoginViewTest(TestCase):

    """Tests for accounts login view"""

    def setUp(self):
        """Create a user in the database befor runinng each test"""
        self.existing_user = AccountsUserFactory.create(
            email='edith@mailinator.com',
            password='epwd'
        )
        #TODO Create keys/user to redirect to (need to refactor this out)
        self.existing_keysuser = KeysUserFactory.create()

    def test_post_logs_user_in_if_password_correct(self):
        """Test that a POST request with existing user and correct password, logs the user in"""
        self.client.post(
            '/accounts/login',
            data={'email': 'edith@mailinator.com', 'password': 'epwd'}
        )
        user = auth.get_user(self.client)
        self.assertTrue(user.is_authenticated)

#    def test_post_success_redirects_to_user_summary(self):
#        response = self.client.post(
#            '/accounts/login',
#            data={'email': 'edith@mailinator.com','password': 'epwd'}
#        )
#        self.assertRedirects(response,f'/users/{self.existing_user.id}/')

    def test_post_success_redirects_to_home_page(self):
        """Test that a successful log in redirects the user to the home page"""
        response = self.client.post(
            '/accounts/login',
            data={'email': 'edith@mailinator.com', 'password': 'epwd'}
        )
        self.assertRedirects(response, reverse('home'))

    def test_post_wrong_password_renders_home_page(self):
        """Test that a post request with existing user and wrong password renders the home page"""
        response = self.client.post(
            '/accounts/login',
            data={'email': 'edith@mailinator.com', 'password': 'wrongpwd'}
        )
        self.assertTemplateUsed(response, 'home.html')

    def test_post_wrong_password_shows_error(self):
        """Test that a post request with existing user and wrong password displays an error"""
        response = self.client.post(
            '/accounts/login',
            data={'email': 'edith@mailinator.com', 'password': 'wrongpwd'}
        )
        expected_error = escape(LOGIN_ERROR)
        self.assertContains(response, expected_error)

    def test_post_non_existing_user_renders_home_page(self):
        """Test that a post request with non existing user renders the home page"""
        response = self.client.post(
            '/accounts/login',
            data={'email': 'non_existent@non.com', 'password': 'wrongpwd'}
        )
        self.assertTemplateUsed(response, 'home.html')

    def test_post_non_existing_user_shows_error(self):
        """Test that a post request with non existing user shows an error message"""
        response = self.client.post(
            '/accounts/login',
            data={'email': 'non_existent@non.com', 'password': 'wrongpwd'}
        )
        expected_error = escape(LOGIN_ERROR)
        self.assertContains(response, expected_error)

class LogoutViewTest(TestCase):

    """Tests for accounts logout view"""

    def setUp(self):
        self.existing_user = AccountsUserFactory.create(
            email='edith@mailinator.com',
            password='epwd'
        )
        auth.authenticate(
            email=self.existing_user.email,
            password=self.existing_user.password
        )
        self.client.login(email='edith@mailinator.com', password='epwd')

    def test_renders_home_page(self):
        """Test that logout view renders the home page"""
        response = self.client.post(
            '/accounts/logout'
        )
        self.assertTemplateUsed(response, 'home.html')

    def test_logs_user_out(self):
        """Test that logout view logs the current user out"""
        self.client.post(
            '/accounts/logout'
        )
        user = auth.get_user(self.client)
        self.assertFalse(user.is_authenticated)

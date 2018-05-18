"""Unit tests for accounts app views"""
import os
from urllib.parse import urlencode

from django.test import TestCase
from django.utils.html import escape
from django.contrib import auth
from django.urls import reverse

from ..models import User
from ..views import LOGIN_ERROR
from ..factories import UserFactory as AccountsUserFactory

from keys.views import STRAVA_CLIENT_ID, STRAVA_AUTHORIZE_URL

class LoginViewTest(TestCase):

    """Tests for accounts login view"""

    def setUp(self):
        """Create a user in the database befor runinng each test"""
        self.existing_user = AccountsUserFactory.create(
            email='edith@mailinator.com',
            password='epwd'
        )

    def test_post_logs_user_in_if_password_correct(self):
        """Test that a POST request with existing user and correct password, logs the user in"""
        self.client.post(
            '/accounts/login',
            data={'email': 'edith@mailinator.com', 'password': 'epwd'}
        )
        user = auth.get_user(self.client)
        self.assertTrue(user.is_authenticated)
        self.assertEqual(user.email, self.existing_user.email)

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

    def test_redirects_to_home_page(self):
        """Test that logout view redirects to the home page"""
        response = self.client.post(
            '/accounts/logout'
        )
        self.assertRedirects(response, reverse('home'))

    def test_logs_user_out(self):
        """Test that logout view logs the current user out"""
        self.client.post(
            '/accounts/logout'
        )
        user = auth.get_user(self.client)
        self.assertFalse(user.is_authenticated)

class CreateNewStravaUserTest(TestCase):

    """ Tests for accounts create_new_strava_user view """

    def test_creates_user_if_doesnt_exist(self):
        """ Test that create new strava user view creates a new user if one with the requested email address does not exist """
        self.assertEqual(User.objects.count(), 0)

        self.client.post(
            '/accounts/new/strava',
            data={'email':'edith@mailinator.com'}
        ) 
        
        self.assertEqual(User.objects.count(), 1)
        new_user = User.objects.first()
        self.assertEqual(new_user.email, 'edith@mailinator.com')

    
    def test_logs_user_in(self):
        """ Test that create new strava user view logs in the user with the requested email address  """
        self.client.post(
            '/accounts/new/strava',
            data={'email':'edith@mailinator.com'}
        ) 
        
        user = auth.get_user(self.client)
        self.assertTrue(user.is_authenticated)
        self.assertEqual(user.email, 'edith@mailinator.com')

    def test_redirects_to_request_strava_code(self):
        """ Test that create new strava user view redirects to the Strava url used to request a code for token exchange"""
        response = self.client.post(
            '/accounts/new/strava',
            data={'email':'edith@mailinator.com'}
        )
    
        parameters_dict = {
            'client_id': STRAVA_CLIENT_ID,
            'redirect_uri' : os.environ['STRAVA_REDIRECT_URI'], 
            'response_type' : 'code',
            'scope' : 'view_private'
        }
        parameters = urlencode(parameters_dict)
        url = f'{STRAVA_AUTHORIZE_URL}?{parameters}'
        
        self.assertRedirects(response,url,fetch_redirect_response=False)

#    def test_xxx_if_email_is_empty(self):
#        """ Test that create new strava user view does xxx if email is empty """
#        self.fail()

#    def test_does_not_create_user_if_exists(self):
#        """ Test that create new strava user does not create a new user if one with requested email already exists """
#        self.fail()

#    def test_redirects_to_login_page_if_exists(self):
        

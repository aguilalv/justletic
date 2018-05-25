"""Unit Tests for Keys views"""
from unittest.mock import patch, call

from django.test import TestCase
from django.utils.html import escape
from django.contrib import auth

from ..models import Key
from accounts.factories import UserFactory as AccountsUserFactory

from utils.strava_utils import STRAVA_AUTH_ERROR

class HomePageTest(TestCase):

    """Unit Tests for the Home Page view"""

    def test_uses_home_template(self):
        """Test that home page view renders the right template"""
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'home.html')

class StravaTokenExchangeView(TestCase):

    """Unit test for Keys.StravaTokenExchange view"""

    def create_user_and_login(self,email,password):
        """Helper function to create a user and log it in"""
        self.existing_user = AccountsUserFactory.create(
            email=email,
            password=password
        )
        auth.authenticate(
            email=self.existing_user.email,
            password=self.existing_user.password
        )
        self.client.login(email='edith@mailinator.com', password='epwd')

    def setUp(self):
        """Create a user in the database and log it in before runinng each test"""
        self.create_user_and_login('edith@mailinator.com','epwd')

    @patch('keys.views.exchange_strava_code')
    def test_calls_exchange_strava_code_helper_function(self,mock):
        """Test that it calls the exchange strava code helper function"""
        mock.return_value = ('Token','Strava_id')
        response = self.client.get('/users/stravatokenexchange?state=&code=abc123')
        self.assertTrue(mock.called) 
    
    @patch('keys.views.exchange_strava_code')
    def test_exchange_strava_code_receives_code_from_request(self,mock):
        """Test that it calls the exchange strava code helper function"""
        mock.return_value = ('Token','Strava_id')
        response = self.client.get('/users/stravatokenexchange?state=&code=abc123')
        code = mock.call_args
        self.assertEqual(code,call('abc123'))

    @patch('keys.views.exchange_strava_code')
    def test_shows_error_message_when_receives_none_as_token(self,mock):
        """Test that when view receives None as token it displasys an error"""
        mock.return_value = (None,'2')
        expected_error = escape(STRAVA_AUTH_ERROR)
        response = self.client.get('/users/stravatokenexchange?state=&code=abc123')
        self.assertContains(response, expected_error)

    @patch('keys.views.exchange_strava_code')
    def test_shows_error_message_when_receives_none_as_strava_id(self,mock):
        """Test that when view receives None as strava_id it displasys an error"""
        mock.return_value = ('2',None)
        expected_error = escape(STRAVA_AUTH_ERROR)
        response = self.client.get('/users/stravatokenexchange?state=&code=abc123')
        self.assertContains(response, expected_error)

    @patch('keys.views.exchange_strava_code')
    def test_stores_token_and_strava_id_in_database(self,mock):
        """Test that Strava Token Exchange view stores the new token and the 
        users strava id in the database"""
        mock.return_value = ('Token','Strava_id')
        
        self.assertEqual(Key.objects.count(),0)

        response = self.client.get('/users/stravatokenexchange?state=&code=abc123')         
        self.assertEqual(Key.objects.count(),1)
        self.assertEqual(Key.objects.all()[0].token,'Token')
        self.assertEqual(Key.objects.all()[0].strava_id,'Strava_id')

    @patch('keys.views.exchange_strava_code')
    def test_links_token_and_stravaid_to_logged_in_user(self,mock):
        """Test that Strava Token Exchange view links in the database
        the token and strava id  with the user that is logged in"""
        mock.return_value = ('Token','Strava_id')
       
        response = self.client.get('/users/stravatokenexchange?state=&code=abc123')         
        stored_key = Key.objects.all()[0]
        self.assertEqual(stored_key.user.email,'edith@mailinator.com')
        self.assertEqual(stored_key.token,'Token')
        self.assertEqual(stored_key.strava_id,'Strava_id')

    @patch('keys.views.exchange_strava_code')
    def test_render_congratulations_message_on_success(self,mock):
        """Test that the view renders a congratulations message
        after a successful token exchange"""
        mock.return_value = ('Token','Strava_id')
        
        response = self.client.get('/users/stravatokenexchange?state=&code=abc123')         
        self.assertTemplateUsed(response, 'congratulations.html')

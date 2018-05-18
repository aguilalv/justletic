"""Unit Tests for Keys views"""
from django.test import TestCase
from django.utils.html import escape
from urllib.parse import parse_qsl
from django.contrib import auth

import httpretty
import os

from ..views import STRAVA_AUTH_ERROR
from ..models import Key
from accounts.factories import UserFactory as AccountsUserFactory

class HomePageTest(TestCase):

    """Unit Tests for the Home Page view"""

    def test_uses_home_template(self):
        """Test that home page view renders the right template"""
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'home.html')

class StravaTokenExchangeView(TestCase):

    """Unit test for Keys.StravaTokenExchange view"""

    @httpretty.activate
    def test_sends_get_request_with_code_received(self):
        """Test that when receiving a code the view sends request to exchange for a token"""
        existing_user = AccountsUserFactory.create(
            email='edith@mailinator.com',
            password='epwd'
        )
        auth.authenticate(
            email=existing_user.email,
            password=existing_user.password
        )
        self.client.login(email='edith@mailinator.com', password='epwd')
        
        exchange_url = 'www.strava.com/oauth/token'
        expected_parameters = {
            'client_id': '15873', 
            'client_secret': os.environ['STRAVA_CLIENT_SECRET'], 
            'code': 'abc123',
        }
        
        mock_body = '''
            {"access_token":"87a407fc475a61ef97265b4bf8867f3ecfc102af",
            "token_type":"Bearer",
            "athlete":
            {"id":1234567,
                "username":"edith",
                "resource_state":2,
                "firstname":"Edith",
                "lastname":"Jones",
                "city":"London",
                "state":"England",
                "country":"United Kingdom",
                "sex":"F",
                "premium":false,
                "created_at":"2014-06-21T21:36:33Z",
                "updated_at":"2018-04-26T20:20:03Z",
                "badge_type_id":0,
                "profile_medium":"https://dgalywyr863hv.cloudfront.net/pictures/athletes/5331809/5624577/1/medium.jpg",
                "profile":"https://dgalywyr863hv.cloudfront.net/pictures/athletes/5331809/5624577/1/large.jpg",
                "friend":null,
                "follower":null,
                "email":"edith@mailinator.com"}}
        '''   
        httpretty.register_uri(
            httpretty.POST,
            'https://' + exchange_url,
            body = mock_body
        )

        self.client.get('/users/stravatokenexchange?state=&code=abc123') 
       
        requested_url = httpretty.last_request().headers.get('Host') +\
            httpretty.last_request().path
        self.assertEqual(exchange_url,requested_url) 

        sent_parameters = dict(parse_qsl(httpretty.last_request().body.decode()))
        self.assertEqual(
            sent_parameters,
            expected_parameters
        ) 
      
    @httpretty.activate
    def test_shows_error_message_when_receives_error_code(self):
        """Test that when view receives an error it displays a message"""
        existing_user = AccountsUserFactory.create(
            email='edith@mailinator.com',
            password='epwd'
        )
        auth.authenticate(
            email=existing_user.email,
            password=existing_user.password
        )
        self.client.login(email='edith@mailinator.com', password='epwd')
        
        expected_error = escape(STRAVA_AUTH_ERROR)
        text_to_receive = '''
            {
                "message":"Bad Request",
                "errors":[{
                    "resource":"Application",
                    "field":"client_id",
                    "code":"invalid"
                }]
            }'''

        httpretty.register_uri(
            httpretty.POST,
            'https://www.strava.com/oauth/token',
            body = text_to_receive
        )

        response = self.client.get('/users/stravatokenexchange?state=&code=abc123')
        self.assertContains(response, expected_error)
    
    @httpretty.activate
    def test_render_congratulations_message_on_success(self):
        """Test that the view renders a congratulations message
        after a successful token exchange"""
        existing_user = AccountsUserFactory.create(
            email='edith@mailinator.com',
            password='epwd'
        )
        auth.authenticate(
            email=existing_user.email,
            password=existing_user.password
        )
        self.client.login(email='edith@mailinator.com', password='epwd')
        
        exchange_url = 'www.strava.com/oauth/token'
        expected_parameters = {
            'client_id': '15873', 
            'client_secret': os.environ['STRAVA_CLIENT_SECRET'], 
            'code': 'abc123',
        }
        
        mock_body = '''
            {"access_token":"87a407fc475a61ef97265b4bf8867f3ecfc102af",
            "token_type":"Bearer",
            "athlete":
            {"id":1234567,
                "username":"edith",
                "resource_state":2,
                "firstname":"Edith",
                "lastname":"Jones",
                "city":"London",
                "state":"England",
                "country":"United Kingdom",
                "sex":"F",
                "premium":false,
                "created_at":"2014-06-21T21:36:33Z",
                "updated_at":"2018-04-26T20:20:03Z",
                "badge_type_id":0,
                "profile_medium":"https://dgalywyr863hv.cloudfront.net/pictures/athletes/5331809/5624577/1/medium.jpg",
                "profile":"https://dgalywyr863hv.cloudfront.net/pictures/athletes/5331809/5624577/1/large.jpg",
                "friend":null,
                "follower":null,
                "email":"edith@mailinator.com"}}
        '''   
        httpretty.register_uri(
            httpretty.POST,
            'https://' + exchange_url,
            body = mock_body
        )
        
        response = self.client.get('/users/stravatokenexchange?state=&code=abc123')         
        self.assertTemplateUsed(response, 'congratulations.html')
    
    @httpretty.activate
    def test_stores_token_in_database(self):
        """Test that Strava Token Exchange view stores the new token 
        in the database associated ot the logged in user"""
        existing_user = AccountsUserFactory.create(
            email='edith@mailinator.com',
            password='epwd'
        )
        auth.authenticate(
            email=existing_user.email,
            password=existing_user.password
        )
        self.client.login(email='edith@mailinator.com', password='epwd')
        
        exchange_url = 'www.strava.com/oauth/token'
        expected_parameters = {
            'client_id': '15873', 
            'client_secret': os.environ['STRAVA_CLIENT_SECRET'], 
            'code': 'abc123',
        }
        
        mock_body = '''
            {"access_token":"87a407fc475a61ef97265b4bf8867f3ecfc102af",
            "token_type":"Bearer",
            "athlete":
            {"id":1234567,
                "username":"edith",
                "resource_state":2,
                "firstname":"Edith",
                "lastname":"Jones",
                "city":"London",
                "state":"England",
                "country":"United Kingdom",
                "sex":"F",
                "premium":false,
                "created_at":"2014-06-21T21:36:33Z",
                "updated_at":"2018-04-26T20:20:03Z",
                "badge_type_id":0,
                "profile_medium":"https://dgalywyr863hv.cloudfront.net/pictures/athletes/5331809/5624577/1/medium.jpg",
                "profile":"https://dgalywyr863hv.cloudfront.net/pictures/athletes/5331809/5624577/1/large.jpg",
                "friend":null,
                "follower":null,
                "email":"edith@mailinator.com"}}
        '''   
        httpretty.register_uri(
            httpretty.POST,
            'https://' + exchange_url,
            body = mock_body
        )
       
        self.assertEqual(Key.objects.count(),0)

        response = self.client.get('/users/stravatokenexchange?state=&code=abc123')         
        self.assertEqual(Key.objects.count(),1)
        self.assertEqual(Key.objects.all()[0].token,'87a407fc475a61ef97265b4bf8867f3ecfc102af')
       
    @httpretty.activate
    def test_stores_stravaid_in_database(self):
        """Test that Strava Token Exchange view stores the Strava Id 
        in the database associated ot the logged in user"""
        existing_user = AccountsUserFactory.create(
            email='edith@mailinator.com',
            password='epwd'
        )
        auth.authenticate(
            email=existing_user.email,
            password=existing_user.password
        )
        self.client.login(email='edith@mailinator.com', password='epwd')
        
        exchange_url = 'www.strava.com/oauth/token'
        expected_parameters = {
            'client_id': '15873', 
            'client_secret': os.environ['STRAVA_CLIENT_SECRET'], 
            'code': 'abc123',
        }
        
        mock_body = '''
            {"access_token":"87a407fc475a61ef97265b4bf8867f3ecfc102af",
            "token_type":"Bearer",
            "athlete":
            {"id":1234567,
                "username":"edith",
                "resource_state":2,
                "firstname":"Edith",
                "lastname":"Jones",
                "city":"London",
                "state":"England",
                "country":"United Kingdom",
                "sex":"F",
                "premium":false,
                "created_at":"2014-06-21T21:36:33Z",
                "updated_at":"2018-04-26T20:20:03Z",
                "badge_type_id":0,
                "profile_medium":"https://dgalywyr863hv.cloudfront.net/pictures/athletes/5331809/5624577/1/medium.jpg",
                "profile":"https://dgalywyr863hv.cloudfront.net/pictures/athletes/5331809/5624577/1/large.jpg",
                "friend":null,
                "follower":null,
                "email":"edith@mailinator.com"}}
        '''   
        httpretty.register_uri(
            httpretty.POST,
            'https://' + exchange_url,
            body = mock_body
        )
       
        self.assertEqual(Key.objects.count(),0)

        response = self.client.get('/users/stravatokenexchange?state=&code=abc123')         
        self.assertEqual(Key.objects.count(),1)
        self.assertEqual(Key.objects.all()[0].strava_id,'1234567')
    
    @httpretty.activate
    def test_links_token_and_stravaid_to_logged_in_user(self):
        """Test that Strava Token Exchange view links in the database
        the token received with the user that is logged in"""
        existing_user = AccountsUserFactory.create(
            email='edith@mailinator.com',
            password='epwd'
        )
        auth.authenticate(
            email=existing_user.email,
            password=existing_user.password
        )
        self.client.login(email='edith@mailinator.com', password='epwd')

        exchange_url = 'www.strava.com/oauth/token'
        expected_parameters = {
            'client_id': '15873', 
            'client_secret': os.environ['STRAVA_CLIENT_SECRET'], 
            'code': 'abc123',
        }
        
        mock_body = '''
            {"access_token":"87a407fc475a61ef97265b4bf8867f3ecfc102af",
            "token_type":"Bearer",
            "athlete":
            {"id":1234567,
                "username":"edith",
                "resource_state":2,
                "firstname":"Edith",
                "lastname":"Jones",
                "city":"London",
                "state":"England",
                "country":"United Kingdom",
                "sex":"F",
                "premium":false,
                "created_at":"2014-06-21T21:36:33Z",
                "updated_at":"2018-04-26T20:20:03Z",
                "badge_type_id":0,
                "profile_medium":"https://dgalywyr863hv.cloudfront.net/pictures/athletes/5331809/5624577/1/medium.jpg",
                "profile":"https://dgalywyr863hv.cloudfront.net/pictures/athletes/5331809/5624577/1/large.jpg",
                "friend":null,
                "follower":null,
                "email":"edithi2@mailinator.com"}}
        '''   
        httpretty.register_uri(
            httpretty.POST,
            'https://' + exchange_url,
            body = mock_body
        )
       
        response = self.client.get('/users/stravatokenexchange?state=&code=abc123')         
        stored_key = Key.objects.all()[0]
        self.assertEqual(stored_key.user.email,'edith@mailinator.com')
        self.assertEqual(stored_key.token,'87a407fc475a61ef97265b4bf8867f3ecfc102af')
        self.assertEqual(stored_key.strava_id,'1234567')

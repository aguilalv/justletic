"""Unit Tests for Keys views"""
from django.test import TestCase
from django.utils.html import escape
from unittest.mock import patch, call
from urllib.parse import parse_qsl

import httpretty
import os

from ..models import Key, User
from ..views import EMAIL_ERROR, STRAVA_AUTH_ERROR


class HomePageTest(TestCase):

    """Unit Tests for the Home Page view"""

    def test_uses_home_template(self):
        """Test that home page view renders the right template"""
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'home.html')

class UserViewTest(TestCase):

    """Unit tests for the UserView view"""

    def test_uses_user_template(self):
        """Test that user view renders the right template"""
        user = User.objects.create(email='emailey 1')
        response = self.client.get(f'/users/{user.id}/')

        self.assertTemplateUsed(response, 'user.html')

    def test_displays_only_keys_for_that_user(self):
        """Test that user view displays keys for user and not others"""
        correct_user = User.objects.create(email='emailey 1')
        wrong_user = User.objects.create(email='emailey 2')

        Key.objects.create(value='value 1', user=correct_user)
        Key.objects.create(value='value 2', user=correct_user)

        Key.objects.create(value='other value 1', user=wrong_user)
        Key.objects.create(value='other value 2', user=wrong_user)

        response = self.client.get(f'/users/{correct_user.id}/')

        self.assertContains(response, 'value 1')
        self.assertContains(response, 'value 2')
        self.assertNotContains(response, 'other value 1')
        self.assertNotContains(response, 'other value 2')


class NewUserTest(TestCase):

    """Unit tests for the NewUser view"""

    def test_post_saves_email_and_key(self):
        """Test that saves email and key when receives a POST request"""
        self.client.post('/users/new', data={'email': 'edith@mailinator.com'})

        self.assertEqual(User.objects.count(), 1)
        new_user = User.objects.all()[0]
        self.assertEqual(new_user.email, 'edith@mailinator.com')

        self.assertEqual(Key.objects.count(), 1)
        new_key = Key.objects.all()[0]
        self.assertEqual(new_key.value, 'e1234')
        self.assertEqual(new_key.user, new_user)

    def test_post_redirects_after_save(self):
        """Test that redirects to user details view after receiving a POST request"""
        response = self.client.post('/users/new', data={'email': 'edith@mailinator.com'})
        user = User.objects.first()

        self.assertRedirects(response, f'/users/{user.id}/')

    def post_empty_email(self):
        """Send a post request with an empty email [Helper method]"""
        return self.client.post('/users/new', data={'email': ''})

    def test_for_empty_email_renders_home_page(self):
        """Test that renders the home page when receiving a POST request with empty email"""
        response = self.post_empty_email()
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')

    def test_for_empty_email_shows_error_on_page(self):
        """Test that displays an error message when receives a POST request with empty email"""
        response = self.post_empty_email()
        expected_error = escape(EMAIL_ERROR)
        self.assertContains(response, expected_error)

    def test_form_empty_email_notthing_saved_to_db(self):
        """Test nothing is saved to database when receives a POST request with empty email"""
        self.post_empty_email()
        self.assertEqual(User.objects.count(), 0)

class NewServiceTest(TestCase):

    """Unit tests for the NewService view"""

    def test_can_save_post_request_to_an_existing_user(self):
        """Test that it obtains the right key and saves it associating it withthe right user"""
        correct_user = User()
        correct_user.email = 'anne@mailinator.com'
        correct_user.save()

        self.client.post(
            f'/users/{correct_user.id}/add_service'
        )

        self.assertEqual(Key.objects.count(), 1)
        new_key = Key.objects.first()
        self.assertEqual(new_key.value, 'n1234')
        self.assertEqual(new_key.user, correct_user)

    def test_redirects_to_user_view(self):
        """Test that it redirects to user details view"""
        correct_user = User()
        correct_user.email = 'anne@mailinator.com'
        correct_user.save()

        response = self.client.post(
            f'/users/{correct_user.id}/add_service'
        )

        self.assertRedirects(response, f'/users/{correct_user.id}/')
    
class StravaTokenExchangeView(TestCase):

    """Unit test for Keys.StravaTokenExchange view"""

    @httpretty.activate
    def test_sends_get_request_with_code_received(self):
        """Test that when receiving a code the view sends request to exchange for a token"""
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

#    def test_stores_token_in_database(self, mock_requests):
#        """Test that """

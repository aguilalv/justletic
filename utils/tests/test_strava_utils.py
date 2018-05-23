"""Unit tests for Strava Utils module"""
import httpretty
import os
from urllib.parse import parse_qsl, urlparse, parse_qs

from django.test import TestCase
    
from utils.strava_utils import (
    request_strava_oauth_code,
    exchange_strava_code,
    strava_oauth_code_request_url
)
from utils.strava_utils import (
    STRAVA_AUTHORIZE_URL, 
    STRAVA_CLIENT_ID,
    STRAVA_CODE_EXCHANGE_URL
)

class StravaOAuthCodeRequestUrl(TestCase):
    
    """Unit Tests for helper function that returns oAuth Code
    request URL"""

    def test_returns_strava_authorization_url(self):
        """ Test that StravaOAuthCodeRequest helper function 
        returns the url to request a code to Strava"""
        expected_parameters = {
            'client_id': STRAVA_CLIENT_ID,
            'redirect_uri': os.environ['STRAVA_REDIRECT_URI'], 
            'response_type': 'code',
            'scope': 'view_private'
        }
        url = urlparse(
            strava_oauth_code_request_url()
        )
        parameters = parse_qs(url.query)
        
        self.assertEqual(
            STRAVA_AUTHORIZE_URL,
            f'{url.scheme}://{url.netloc}{url.path}'
        )
        self.assertEqual(
            len(expected_parameters.keys()),    
            len(parameters.keys())
        )
        self.assertEqual(
            expected_parameters['client_id'],
            parameters['client_id'][0]
        )
        self.assertEqual(
            expected_parameters['redirect_uri'],
            parameters['redirect_uri'][0]
        )
        self.assertEqual(
            expected_parameters['response_type'],
            parameters['response_type'][0]
        )
        self.assertEqual(
            expected_parameters['scope'],
            parameters['scope'][0]
        )



class RequestStravaOAuthCodeTest(TestCase):
    
    """Unit Tests for helper function that requests oAuth Code"""

    @httpretty.activate
    def test_sends_request_to_strava_for_code(self):
        """ Test that RequestOAuthCode helper function 
        sends request for a code to Strava"""
        httpretty.register_uri(
            httpretty.POST,
            STRAVA_AUTHORIZE_URL,
            body = ''
        )

        request_strava_oauth_code()
    
        expected_parameters = {
            'client_id': STRAVA_CLIENT_ID,
            'redirect_uri' : os.environ['STRAVA_REDIRECT_URI'], 
            'response_type' : 'code',
            'scope' : 'view_private'
        }

        self.assertNotIsInstance(
            httpretty.last_request(),
            httpretty.HTTPrettyRequestEmpty
        )
        requested_url = 'https://'+\
            httpretty.last_request().headers.get('Host') +\
            httpretty.last_request().path
        sent_parameters = dict(
            parse_qsl(httpretty.last_request().body.decode())
        )

        self.assertEqual(STRAVA_AUTHORIZE_URL,requested_url) 
        self.assertEqual(
            sent_parameters,
            expected_parameters
        )

class ExchangeStravaCode(TestCase):

    """Unit tests for helper function that exchanges Strava code for Token"""
    def register_token_exchange_url_in_httpretty(self):
        mock_body = (
            '{"access_token":"87a407fc475a61ef97265b4bf8867f3ecfc102af",'
            '"token_type":"Bearer",'
            '"athlete":'
            '{"id":1234567,'
                '"username":"edith",'
                '"resource_state":2,'
                '"firstname":"Edith",'
                '"lastname":"Jones",'
                '"city":"London",'
                '"state":"England",'
                '"country":"United Kingdom",'
                '"sex":"F",'
                '"premium":false,'
                '"created_at":"2014-06-21T21:36:33Z",'
                '"updated_at":"2018-04-26T20:20:03Z",'
                '"badge_type_id":0,'
                '"profile_medium":"https://dgalywyr863hv.cloudfront.net/pictures/athletes/5331809/5624577/1/medium.jpg",'
                '"profile":"https://dgalywyr863hv.cloudfront.net/pictures/athletes/5331809/5624577/1/large.jpg",'
                '"friend":null,'
                '"follower":null,'
                '"email":"edith@mailinator.com"}}'
        )
        httpretty.register_uri(
            httpretty.POST,
            STRAVA_CODE_EXCHANGE_URL,
            body = mock_body
        )
            
    def register_token_exchange_url_in_httpretty_return_error(self):
        mock_body = (
            '{'
                '"message":"Bad Request",'
                '"errors":[{'
                    '"resource":"Application",'
                    '"field":"client_id",'
                    '"code":"invalid"'
                '}]'
            '}'
        )
        httpretty.register_uri(
            httpretty.POST,
            STRAVA_CODE_EXCHANGE_URL,
            body = mock_body
        )


    @httpretty.activate
    def test_sends_get_request_with_code_received(self):
        """Test that exchange strava token helper function sends get
        request to exchange code for token"""
        self.register_token_exchange_url_in_httpretty()
        
        expected_parameters = {
            'client_id': STRAVA_CLIENT_ID,
            'client_secret': os.environ['STRAVA_CLIENT_SECRET'], 
            'code': 'abc123',
        }
        
        exchange_strava_code(code='abc123')
        
        self.assertNotIsInstance(
            httpretty.last_request(),
            httpretty.HTTPrettyRequestEmpty
        )
        requested_url = 'https://'+\
            httpretty.last_request().headers.get('Host') +\
            httpretty.last_request().path
        sent_parameters = dict(
            parse_qsl(httpretty.last_request().body.decode())
        )

        self.assertEqual(STRAVA_CODE_EXCHANGE_URL,requested_url) 
        self.assertEqual(
            sent_parameters,
            expected_parameters
        )

    @httpretty.activate
    def test_returns_token_and_strava_id(self):
        self.register_token_exchange_url_in_httpretty()
        
        token_received,strava_id_received = exchange_strava_code(code='abc123')

        self.assertEqual(
            token_received,
            "87a407fc475a61ef97265b4bf8867f3ecfc102af"
        )
        self.assertEqual(
            strava_id_received,
            1234567
        )
    
    @httpretty.activate
    def test_returns_none_and_none_when_error(self):
        self.register_token_exchange_url_in_httpretty_return_error()
        token_received,strava_id_received = exchange_strava_code(code='abc123')
        self.assertIsNone(token_received)
        self.assertIsNone(strava_id_received)

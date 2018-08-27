"""Unit tests for Spotify Utils module"""

import os
import httpretty

from urllib.parse import parse_qsl, urlparse, parse_qs
from django.test import TestCase
    
from utils.spotify_utils import (
    request_spotify_oauth_code,
    exchange_spotify_code,
)
from utils.spotify_utils import (
    SPOTIFY_AUTHORIZE_URL, 
    SPOTIFY_CLIENT_ID,
    SPOTIFY_CODE_EXCHANGE_URL,
)

class RequestSpotifyOAuthCodeTest(TestCase):
    
    """Unit Tests for helper function that requests oAuth Code from Spotify"""

    @httpretty.activate
    def test_sends_request_to_spotify_for_code(self):
        """ Test that RequestOAuthCode helper function 
        sends request for a code to Spotify"""
        httpretty.register_uri(
            httpretty.POST,
            SPOTIFY_AUTHORIZE_URL,
            body = ''
        )

        request_spotify_oauth_code()
    
        expected_parameters = {
            'client_id': SPOTIFY_CLIENT_ID,
            'redirect_uri': os.environ['SPOTIFY_REDIRECT_URI'], 
            'response_type': 'code',
            'scope': 'user-read-recently-played user-top-read'
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

        self.assertEqual(SPOTIFY_AUTHORIZE_URL,requested_url) 
        self.assertEqual(
            sent_parameters,
            expected_parameters
        )

class ExchangeSpotifyCode(TestCase):

    """Unit tests for helper function that exchanges Spotify code for Token"""

    def register_token_exchange_url_in_httpretty(self):
        mock_body = (
            '{'
                '"access_token": "NgCXRKMxYjw",'
                '"token_type": "Bearer",'
                '"scope": "user-read-recently-played user-top-read",'
                '"expires_in": 3600,'
                '"refresh_token": "NgAagAUm_SHo"'
            '}'
        )
        httpretty.register_uri(
            httpretty.POST,
            SPOTIFY_CODE_EXCHANGE_URL,
            body = mock_body
        )

    def register_token_exchange_url_in_httpretty_return_error(self):
        httpretty.register_uri(
            httpretty.POST,
            SPOTIFY_CODE_EXCHANGE_URL,
            body = {},
            status = 400
        )
    
    @httpretty.activate
    def test_sends_get_request_with_code_received(self):
        """Test that exchange spotify token helper function sends get
        request to exchange code for token"""
        self.register_token_exchange_url_in_httpretty()
        
        expected_body_parameters = {
            'client_id': SPOTIFY_CLIENT_ID,
            'client_secret': os.environ['SPOTIFY_CLIENT_SECRET'], 
            'grant_type': 'authorization_code',
            'code': 'abc123',
            'redirect_uri': os.environ['SPOTIFY_REDIRECT_URI'], 
        }
       
        exchange_spotify_code(code='abc123')
        
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
        self.assertEqual(SPOTIFY_CODE_EXCHANGE_URL,requested_url) 

        request_body = httpretty.last_request().parse_request_body(httpretty.last_request().body)
        
        for key in expected_body_parameters:
            self.assertEqual(
                expected_body_parameters[key],
                request_body[key][0]
            )
    
    @httpretty.activate
    def test_returns_token_and_refresh_token(self):
        self.register_token_exchange_url_in_httpretty()
        
        token_received,refresh_token_received = exchange_spotify_code(code='abc123')

        self.assertEqual(
            token_received,
            "NgCXRKMxYjw"
        )
        self.assertEqual(
            refresh_token_received,
            "NgAagAUm_SHo"
        )
    
    @httpretty.activate
    def test_returns_none_and_none_when_error(self):
        self.register_token_exchange_url_in_httpretty_return_error()
        token_received,refresh_token_received = exchange_spotify_code(code='abc123')
        self.assertIsNone(token_received)
        self.assertIsNone(refresh_token_received)

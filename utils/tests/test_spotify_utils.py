"""Unit tests for Spotify Utils module"""

import os
import httpretty

from urllib.parse import parse_qsl, urlparse, parse_qs
from django.test import TestCase
    
from utils.spotify_utils import (
    request_spotify_oauth_code,
#    exchange_spotify_code,
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

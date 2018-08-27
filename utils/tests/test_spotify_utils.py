"""Unit tests for Spotify Utils module"""

import os
from urllib.parse import parse_qsl, urlparse, parse_qs

from django.test import TestCase
    
from utils.spotify_utils import (
#    request_spotify_oauth_code,
#    exchange_spotify_code,
    spotify_oauth_code_request_url,
)
from utils.spotify_utils import (
    SPOTIFY_AUTHORIZE_URL, 
    SPOTIFY_CLIENT_ID,
    SPOTIFY_CODE_EXCHANGE_URL,
)

class SpotifyOAuthCodeRequestUrl(TestCase):
    
    """Unit Tests for helper function that returns oAuth Code
    request URL for Spotify"""

    def test_returns_spotify_authorization_url(self):
        """ Test that SpotifyOAuthCodeRequest helper function 
        returns the url to request a code to Spotify"""
        expected_parameters = {
            'client_id': SPOTIFY_CLIENT_ID,
            'redirect_uri': os.environ['SPOTIFY_REDIRECT_URI'], 
            'response_type': 'code',
            'scope': 'user-read-recently-played user-top-read'
        }
        url = urlparse(
            spotify_oauth_code_request_url()
        )
        parameters = parse_qs(url.query)
        
        self.assertEqual(
            SPOTIFY_AUTHORIZE_URL,
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

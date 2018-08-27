
import os
import requests

from urllib.parse import urlencode

SPOTIFY_AUTH_ERROR = "Oops, something went wrong asking Spotify about you ..."
SPOTIFY_CLIENT_ID = '1aaa5ce0611f42cea3b4eeff885b807d'
SPOTIFY_CODE_EXCHANGE_URL = 'https://accounts.spotify.com/api/token' 
SPOTIFY_AUTHORIZE_URL = 'https://accounts.spotify.com/authorize'

def spotify_oauth_code_request_url():
    parameters_dict = {
        'client_id': SPOTIFY_CLIENT_ID,
        'redirect_uri': os.environ['SPOTIFY_REDIRECT_URI'], 
        'response_type': 'code',
        'scope': 'user-read-recently-played user-top-read'
    }
    parameters = urlencode(parameters_dict)
    return f'{SPOTIFY_AUTHORIZE_URL}?{parameters}'

def request_spotify_oauth_code():
    parameters = {
        'client_id': SPOTIFY_CLIENT_ID,
        'redirect_uri': os.environ['SPOTIFY_REDIRECT_URI'], 
        'response_type': 'code',
        'scope': 'user-read-recently-played user-top-read'
    }
    response = requests.post(SPOTIFY_AUTHORIZE_URL, parameters)

def exchange_spotify_code(code):
    data = {
        'client_id': SPOTIFY_CLIENT_ID,
        'client_secret': os.environ['SPOTIFY_CLIENT_SECRET'], 
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': os.environ['SPOTIFY_REDIRECT_URI'], 
    }
    
    response = requests.post(SPOTIFY_CODE_EXCHANGE_URL, data = data) 
   
    if response.status_code != 200:
        return (None, None)
    else:
        data_received = response.json()
        token_received = data_received.get('access_token')
        refresh_token_received = data_received.get('refresh_token')
        return (token_received, refresh_token_received)

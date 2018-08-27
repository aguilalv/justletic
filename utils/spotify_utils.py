
import os
import requests

from urllib.parse import urlencode

SPOTIFY_AUTH_ERROR = "Oops, something went wrong asking Spotify about you ..."
SPOTIFY_CLIENT_ID = '1aaa5ce0611f42cea3b4eeff885b807d'
SPOTIFY_CODE_EXCHANGE_URL = 'https://www.strava.com/oauth/token' 
SPOTIFY_AUTHORIZE_URL = 'https://accounts.spotify.com/authorize'

def request_spotify_oauth_code():
    parameters = {
        'client_id': SPOTIFY_CLIENT_ID,
        'redirect_uri': os.environ['SPOTIFY_REDIRECT_URI'], 
        'response_type': 'code',
        'scope': 'user-read-recently-played user-top-read'
    }
    response = requests.post(SPOTIFY_AUTHORIZE_URL, parameters)

""" Views to manage Keys for Justletic external services """
import requests
import os

from django.shortcuts import render
from django.http import HttpResponse

from .models import Key
from accounts.models import User

STRAVA_AUTH_ERROR = "Oops, something went wrong asking Strava about you ..."
STRAVA_CLIENT_ID = '15873'
STRAVA_TOKEN_EXCHANGE_URL = 'https://www.strava.com/oauth/token' 
STRAVA_AUTHORIZE_URL = 'https://www.strava.com/oauth/authorize'

def home_page(request):
    """Render Justletic home page"""
    return render(request, 'home.html')

def strava_token_exchange(request):
    """Receives Strava authorisation code and sends request for user token"""
    code = request.GET.get('code')
    parameters = {
        'client_id': STRAVA_CLIENT_ID,
        'client_secret': os.environ['STRAVA_CLIENT_SECRET'], 
        'code': code
    }

    response = requests.post(STRAVA_TOKEN_EXCHANGE_URL, parameters)
    
    data_received = response.json()
    if 'errors' not in data_received:
        token_received = data_received.get('access_token')
        logged_in_user = request.user 
        new_key = Key(user=logged_in_user,token=token_received)
        new_key.save()
        return render(request, 'congratulations.html')
    else:
        return render(request, 'home.html', {'error': STRAVA_AUTH_ERROR})

""" Views to manage Keys for Justletic external services """
from django.shortcuts import render

import requests
import os

STRAVA_AUTH_ERROR = "It seems like there was a problem ..."

def home_page(request):
    """Render Justletic home page"""
    return render(request, 'home.html')

def strava_token_exchange(request):
    """Receives Strava authorisation code and sends request for user token"""

    code = request.GET.get('code')
    parameters = {
        'client_id': '15873',
        'client_secret': os.environ['STRAVA_CLIENT_SECRET'], 
        'code': code
    }

    response = requests.post('https://www.strava.com/oauth/token', parameters)
    
    data_received = response.json()
    if 'errors' not in data_received:
        return render(request, 'congratulations.html')
    else:
        return render(request, 'home.html', {'error': STRAVA_AUTH_ERROR})

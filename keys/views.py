""" Views to manage Keys for Justletic external services """
import requests
import os

from django.shortcuts import render
from django.http import HttpResponse

from .models import Key
from accounts.models import User

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
        token_received = data_received.get('access_token')
        logged_in_user = request.user 

        print(f'>>> {logged_in_user}')

        new_key = Key(user=logged_in_user,token=token_received)
        new_key.save()
        return render(request, 'congratulations.html')
    else:
        return render(request, 'home.html', {'error': STRAVA_AUTH_ERROR})

""" Views to manage Keys for Justletic external services """
import requests
import os

from django.shortcuts import render
from django.http import HttpResponse

from .models import Key
from accounts.models import User

from utils.strava_utils import STRAVA_AUTH_ERROR
from utils.strava_utils import exchange_strava_code, get_strava_activities 

def home_page(request):
    """Render Justletic home page"""
    return render(request, 'home.html')

def strava_token_exchange(request):
    """Receives Strava authorisation code and sends request for user token"""
    code = request.GET.get('code')

    token,strava_id = exchange_strava_code(code)

    if not token or not strava_id:
        return render(request, 'home.html', {'error': STRAVA_AUTH_ERROR})

    logged_in_user = request.user 
    new_key = Key(
        user=logged_in_user,
        token=token,
        strava_id=strava_id
    )
    new_key.save()

    activities = get_strava_activities(token)

    return render(
        request,
        'congratulations.html',
        {'last_activity_distance':activities[0].get('distance')/1000}
    )

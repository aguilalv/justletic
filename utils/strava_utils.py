import os
import requests
from urllib.parse import urlencode
import json

STRAVA_AUTH_ERROR = "Oops, something went wrong asking Strava about you ..."
STRAVA_CLIENT_ID = '15873'
STRAVA_CODE_EXCHANGE_URL = 'https://www.strava.com/oauth/token' 
STRAVA_AUTHORIZE_URL = 'https://www.strava.com/oauth/authorize'
STRAVA_GET_ACTIVITIES_URL = 'https://www.strava.com/api/v3/athlete/activities'

def strava_oauth_code_request_url():
    parameters_dict = {
        'client_id': STRAVA_CLIENT_ID,
        'redirect_uri': os.environ['STRAVA_REDIRECT_URI'], 
        'response_type': 'code',
        'scope': 'view_private'
    }
    parameters = urlencode(parameters_dict)
    return f'{STRAVA_AUTHORIZE_URL}?{parameters}'

def request_strava_oauth_code():
    
    parameters = {
        'client_id': STRAVA_CLIENT_ID,
        'redirect_uri': os.environ['STRAVA_REDIRECT_URI'], 
        'response_type': 'code',
        'scope': 'view_private'
    }
    response = requests.post(STRAVA_AUTHORIZE_URL, parameters)

def exchange_strava_code(code):
    parameters = {
        'client_id': STRAVA_CLIENT_ID,
        'client_secret': os.environ['STRAVA_CLIENT_SECRET'], 
        'code': code
    }

    response = requests.post(STRAVA_CODE_EXCHANGE_URL, parameters)
    
    data_received = response.json()

    if 'errors' in data_received:
        return (None, None)
    else:
        token_received = data_received.get('access_token')
        id_received = data_received.get('athlete').get('id')
        return (token_received, id_received)

def get_strava_activities(token):
    headers = {'Authorization': 'Bearer ' + token}
    response = requests.get(STRAVA_GET_ACTIVITIES_URL, headers=headers)
    received = json.loads(response.text)
    activities = []
    for item in received:
        activity = {}
        activity['platform'] = 'Strava'
        activity['distance'] = item.get('distance')
        activity['moving_time'] = item.get('moving_time')
        activity['elevation_gain'] = item.get('total_elevation_gain')
        activity['type'] = item.get('type')
        activity['strava_id'] = item.get('id')
        activity['start_date_local'] = item.get('start_date_local')
        activity['average_heartrate'] = item.get('average_heartrate')
        activity['average_cadence'] = item.get('average_cadence')
        activities.append(activity)
    return activities

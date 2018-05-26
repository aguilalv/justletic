"""Unit tests for Strava Utils module"""
import httpretty
import os
from urllib.parse import parse_qsl, urlparse, parse_qs

from django.test import TestCase
    
from utils.strava_utils import (
    request_strava_oauth_code,
    exchange_strava_code,
    strava_oauth_code_request_url,
    get_strava_activities
)
from utils.strava_utils import (
    STRAVA_AUTHORIZE_URL, 
    STRAVA_CLIENT_ID,
    STRAVA_CODE_EXCHANGE_URL,
    STRAVA_GET_ACTIVITIES_URL
)

class StravaOAuthCodeRequestUrl(TestCase):
    
    """Unit Tests for helper function that returns oAuth Code
    request URL"""

    def test_returns_strava_authorization_url(self):
        """ Test that StravaOAuthCodeRequest helper function 
        returns the url to request a code to Strava"""
        expected_parameters = {
            'client_id': STRAVA_CLIENT_ID,
            'redirect_uri': os.environ['STRAVA_REDIRECT_URI'], 
            'response_type': 'code',
            'scope': 'view_private'
        }
        url = urlparse(
            strava_oauth_code_request_url()
        )
        parameters = parse_qs(url.query)
        
        self.assertEqual(
            STRAVA_AUTHORIZE_URL,
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



class RequestStravaOAuthCodeTest(TestCase):
    
    """Unit Tests for helper function that requests oAuth Code"""

    @httpretty.activate
    def test_sends_request_to_strava_for_code(self):
        """ Test that RequestOAuthCode helper function 
        sends request for a code to Strava"""
        httpretty.register_uri(
            httpretty.POST,
            STRAVA_AUTHORIZE_URL,
            body = ''
        )

        request_strava_oauth_code()
    
        expected_parameters = {
            'client_id': STRAVA_CLIENT_ID,
            'redirect_uri' : os.environ['STRAVA_REDIRECT_URI'], 
            'response_type' : 'code',
            'scope' : 'view_private'
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

        self.assertEqual(STRAVA_AUTHORIZE_URL,requested_url) 
        self.assertEqual(
            sent_parameters,
            expected_parameters
        )

class ExchangeStravaCode(TestCase):

    """Unit tests for helper function that exchanges Strava code for Token"""
    def register_token_exchange_url_in_httpretty(self):
        mock_body = (
            '{"access_token":"87a407fc475a61ef97265b4bf8867f3ecfc102af",'
            '"token_type":"Bearer",'
            '"athlete":'
            '{"id":1234567,'
                '"username":"edith",'
                '"resource_state":2,'
                '"firstname":"Edith",'
                '"lastname":"Jones",'
                '"city":"London",'
                '"state":"England",'
                '"country":"United Kingdom",'
                '"sex":"F",'
                '"premium":false,'
                '"created_at":"2014-06-21T21:36:33Z",'
                '"updated_at":"2018-04-26T20:20:03Z",'
                '"badge_type_id":0,'
                '"profile_medium":"https://dgalywyr863hv.cloudfront.net/pictures/athletes/5331809/5624577/1/medium.jpg",'
                '"profile":"https://dgalywyr863hv.cloudfront.net/pictures/athletes/5331809/5624577/1/large.jpg",'
                '"friend":null,'
                '"follower":null,'
                '"email":"edith@mailinator.com"}}'
        )
        httpretty.register_uri(
            httpretty.POST,
            STRAVA_CODE_EXCHANGE_URL,
            body = mock_body
        )
            
    def register_token_exchange_url_in_httpretty_return_error(self):
        mock_body = (
            '{'
                '"message":"Bad Request",'
                '"errors":[{'
                    '"resource":"Application",'
                    '"field":"client_id",'
                    '"code":"invalid"'
                '}]'
            '}'
        )
        httpretty.register_uri(
            httpretty.POST,
            STRAVA_CODE_EXCHANGE_URL,
            body = mock_body
        )


    @httpretty.activate
    def test_sends_get_request_with_code_received(self):
        """Test that exchange strava token helper function sends get
        request to exchange code for token"""
        self.register_token_exchange_url_in_httpretty()
        
        expected_parameters = {
            'client_id': STRAVA_CLIENT_ID,
            'client_secret': os.environ['STRAVA_CLIENT_SECRET'], 
            'code': 'abc123',
        }
        
        exchange_strava_code(code='abc123')
        
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
        self.assertEqual(STRAVA_CODE_EXCHANGE_URL,requested_url) 
        self.assertEqual(
            sent_parameters,
            expected_parameters
        )

    @httpretty.activate
    def test_returns_token_and_strava_id(self):
        self.register_token_exchange_url_in_httpretty()
        
        token_received,strava_id_received = exchange_strava_code(code='abc123')

        self.assertEqual(
            token_received,
            "87a407fc475a61ef97265b4bf8867f3ecfc102af"
        )
        self.assertEqual(
            strava_id_received,
            1234567
        )
    
    @httpretty.activate
    def test_returns_none_and_none_when_error(self):
        self.register_token_exchange_url_in_httpretty_return_error()
        token_received,strava_id_received = exchange_strava_code(code='abc123')
        self.assertIsNone(token_received)
        self.assertIsNone(strava_id_received)

class GetStravaActivities(TestCase):
    
    def register_get_activities_url_in_httpretty_success(self):
        mock_body = (
            '[{'
                '"resource_state":2,'
                '"athlete":{'
                    '"id":21400992,'
                    '"resource_state":1'
                '},'
                '"name":"Evening Run",'
                '"distance":7972.5,'
                '"moving_time":2909,'
                '"elapsed_time":2909,'
                '"total_elevation_gain":110.0,'
                '"type":"Run",'
                '"workout_type":3,'
                '"id":1574689979,'
                '"external_id":"2701804443.fit",'
                '"upload_id":1693199790,'
                '"start_date":"2018-05-15T18:12:19Z",'
                '"start_date_local":"2018-05-15T19:12:19Z",'
                '"timezone":"(GMT+00:00) Europe/London",'
                '"utc_offset":3600.0,'
                '"start_latlng":['
                    '51.579065,'
                    '-0.150119'
                '],'
                '"end_latlng":['
                    '51.579198,'
                    '-0.150102'
                '],'
                '"location_city":null,'
                '"location_state":null,'
                '"location_country":"Reino Unido",'
                '"start_latitude":51.579065,'
                '"start_longitude":-0.150119,'
                '"achievement_count":0,'
                '"kudos_count":0,'
                '"comment_count":0,'
                '"athlete_count":2,'
                '"photo_count":0,'
                '"map":{'
                    '"id":"a1574689979",'
                    '"summary_polyline":"c`yyHfi\\\\mAs@aFhDkCbJiFrCaMaHuF{YyBo@iBmUaFoHmNcJJqEcJcOkEcV~AwGgCgG{E_JgBKaC|W}AlAuB_FlCkH}AiFu@sPbEmKsDwPtXlXfDnHbBhOsDba@nG~PdApH]dEbNdI|FtIbB`TxAHxDjXzF`HnG~A`HuBnAeJlE{DfBf@",'
                    '"resource_state":2'
                '},'
                '"trainer":false,'
                '"commute":false,'
                '"manual":false,'
                '"private":false,'
                '"flagged":false,'
                '"gear_id":null,'
                '"from_accepted_tag":false,'
                '"average_speed":2.741,'
                '"max_speed":11.6,'
                '"average_cadence":79.1,'
                '"average_temp":22.0,'
                '"has_heartrate":true,'
                '"average_heartrate":151.1,'
                '"max_heartrate":161.0,'
                '"elev_high":103.0,'
                '"elev_low":38.2,'
                '"pr_count":0,'
                '"total_photo_count":0,'
                '"has_kudoed":false'
            '}]'            
        )
        httpretty.register_uri(
            httpretty.GET,
            STRAVA_GET_ACTIVITIES_URL,
            body = mock_body
        )

    @httpretty.activate
    def test_sends_request_to_strava_for_activities(self):
        """ Test that GetAthleteActivities sends request for activities to Strava"""
        self.register_get_activities_url_in_httpretty_success()
        activities = get_strava_activities(token="87a407fc475a61ef97265b4bf8867f3ecfc102af")
        
        self.assertNotIsInstance(
            httpretty.last_request(),
            httpretty.HTTPrettyRequestEmpty
        )
        requested_url = 'https://'+\
            httpretty.last_request().headers.get('Host') +\
            httpretty.last_request().path
        self.assertEqual(requested_url,STRAVA_GET_ACTIVITIES_URL)

    @httpretty.activate
    def test_sends_token_in_authorization_header(self):
        """ Test that GetAthleteActivities includes token in Authorization header"""
        self.register_get_activities_url_in_httpretty_success()
        activities = get_strava_activities(token="87a407fc475a61ef97265b4bf8867f3ecfc102af")
        
        authorization_header_sent = httpretty.last_request().headers.get('Authorization')
        self.assertEqual(
            authorization_header_sent,
            'Bearer 87a407fc475a61ef97265b4bf8867f3ecfc102af'
        )

    @httpretty.activate
    def test_returns_list_with_length_the_number_of_activities(self):
        """ Test that GetAthleteActivities returns a list with activities"""
        self.register_get_activities_url_in_httpretty_success()
        activities = get_strava_activities(token="87a407fc475a61ef97265b4bf8867f3ecfc102af")
        
        self.assertIs(type(activities),list)
        self.assertEqual(len(activities),1)

    @httpretty.activate
    def test_returns_dictionary_for_each_activity(self):
        """ Test that GetAthleteActivities returns a list with activities"""
        self.register_get_activities_url_in_httpretty_success()
        activities = get_strava_activities(token="87a407fc475a61ef97265b4bf8867f3ecfc102af")
        
        activity = activities[0]
        self.assertIs(type(activity),dict)
        self.assertEqual(activity.get('distance'),7972.5)
        self.assertEqual(activity.get('moving_time'),2909)
        self.assertEqual(activity.get('elevation_gain'),110.0)
        self.assertEqual(activity.get('type'),"Run")
        self.assertEqual(activity.get('strava_id'),1574689979)
        self.assertEqual(activity.get('platform'),"Strava")
        self.assertEqual(activity.get('start_date_local'),"2018-05-15T19:12:19Z")
        self.assertEqual(activity.get('average_heartrate'),151.1)
        self.assertEqual(activity.get('average_cadence'),79.1)

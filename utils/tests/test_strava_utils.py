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
    
    def register_get_activities_url_in_httpretty_success_return_one(self):
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

    def register_get_activities_url_in_httpretty_success_return_zero(self):
        mock_body = ('[]')            
        httpretty.register_uri(
            httpretty.GET,
            STRAVA_GET_ACTIVITIES_URL,
            body = mock_body
        )
    
    def register_get_activities_url_in_httpretty_success_return_two(self):
        mock_body = (
            '[{'
                '"resource_state":2,'
                '"athlete":{'
                    '"id":21400992,'
                    '"resource_state":1'
                '},'
                '"name":"Evening Run 2",'
                '"distance":10123.5,'
                '"moving_time":3601,'
                '"elapsed_time":3601,'
                '"total_elevation_gain":0.0,'
                '"type":"Run",'
                '"workout_type":3,'
                '"id":1234567890,'
                '"external_id":"12344567.fit",'
                '"upload_id":1234,'
                '"start_date":"2018-05-18T18:12:19Z",'
                '"start_date_local":"2018-05-18T19:12:19Z",'
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
                '"max_speed":11.0,'
                '"average_cadence":82.1,'
                '"average_temp":32.0,'
                '"has_heartrate":true,'
                '"average_heartrate":151.1,'
                '"max_heartrate":161.0,'
                '"elev_high":103.0,'
                '"elev_low":38.2,'
                '"pr_count":0,'
                '"total_photo_count":0,'
                '"has_kudoed":false'
            '},'
            '{'
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
    
    def register_get_activities_url_in_httpretty_success_many_unordered(self):
        mock_body = (
            '[{'
                '"distance":1000,'
                '"moving_time":1000,'
                '"total_elevation_gain":1.0,'
                '"type":"Run",'
                '"id":1111111111,'
                '"start_date_local":"2018-05-28T19:12:19Z",'
                '"average_speed":1.000,'
                '"average_cadence":10.0'
            '},'
            '{'
                '"distance":2000,'
                '"moving_time":2000,'
                '"total_elevation_gain":2.0,'
                '"type":"Run",'
                '"id":2222222222,'
                '"start_date_local":"2016-05-28T19:12:19Z",'
                '"average_speed":2.000,'
                '"average_cadence":20.0'
            '},'
            '{'
                '"distance":3000,'
                '"moving_time":3000,'
                '"total_elevation_gain":3.0,'
                '"type":"Run",'
                '"id":3333333333,'
                '"start_date_local":"2018-05-28T21:12:19Z",'
                '"average_speed":3.000,'
                '"average_cadence":30.0'
            '},'
            '{'
                '"distance":4000,'
                '"moving_time":4000,'
                '"total_elevation_gain":4.0,'
                '"type":"Run",'
                '"id":4444444444,'
                '"start_date_local":"2018-02-28T19:12:19Z",'
                '"average_speed":4.000,'
                '"average_cadence":40.0'
            '},'
            '{'
                '"distance":5000,'
                '"moving_time":5000,'
                '"total_elevation_gain":5.0,'
                '"type":"Run",'
                '"id":555555555,'
                '"start_date_local":"2018-05-15T19:12:19Z",'
                '"average_speed":5.000,'
                '"average_cadence":50.0'
            '},'
            '{'
                '"distance":6000,'
                '"moving_time":6000,'
                '"total_elevation_gain":6.0,'
                '"type":"Run",'
                '"id":6666666666,'
                '"start_date_local":"2018-05-28T19:09:19Z",'
                '"average_speed":6.000,'
                '"average_cadence":60.0'
            '}]'            
        )
        httpretty.register_uri(
            httpretty.GET,
            STRAVA_GET_ACTIVITIES_URL,
            body = mock_body
        )
    
    def register_get_activities_url_in_httpretty_fault(self):
        mock_body = ('{'
            '"errors":"The set of errors associated with this fault",'
            '"message":"This is the message of the fault"'
        '}')
        httpretty.register_uri(
            httpretty.GET,
            STRAVA_GET_ACTIVITIES_URL,
            body = mock_body,
            status = 401
        )
                
    @httpretty.activate
    def test_sends_request_to_strava_for_activities(self):
        """ Test that GetAthleteActivities sends request for activities to Strava"""
        self.register_get_activities_url_in_httpretty_success_return_one()
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
        self.register_get_activities_url_in_httpretty_success_return_one()
        activities = get_strava_activities(token="87a407fc475a61ef97265b4bf8867f3ecfc102af")
        
        authorization_header_sent = httpretty.last_request().headers.get('Authorization')
        self.assertEqual(
            authorization_header_sent,
            'Bearer 87a407fc475a61ef97265b4bf8867f3ecfc102af'
        )

    @httpretty.activate
    def test_returns_list_with_length_the_number_of_activities_one_activity(self):
        """ Test that GetAthleteActivities returns a list with activities"""
        self.register_get_activities_url_in_httpretty_success_return_one()
        activities = get_strava_activities(token="87a407fc475a61ef97265b4bf8867f3ecfc102af")
        
        self.assertIs(type(activities),list)
        self.assertEqual(len(activities),1)

    @httpretty.activate
    def test_returns_list_with_length_the_number_of_activities_two_activities(self):
        """ Test that GetAthleteActivities returns a list with activities"""
        self.register_get_activities_url_in_httpretty_success_return_two()
        activities = get_strava_activities(token="87a407fc475a61ef97265b4bf8867f3ecfc102af")
        
        self.assertIs(type(activities),list)
        self.assertEqual(len(activities),2)
    
    @httpretty.activate
    def test_returns_dictionary_for_each_activity_one_activity(self):
        """ Test that GetAthleteActivities returns a list with activities"""
        self.register_get_activities_url_in_httpretty_success_return_one()
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
    
    @httpretty.activate
    def test_returns_dictionary_for_each_activity_two_activities(self):
        """ Test that GetAthleteActivities returns a list with activities"""
        self.register_get_activities_url_in_httpretty_success_return_two()
        activities = get_strava_activities(token="87a407fc475a61ef97265b4bf8867f3ecfc102af")
        
        activity = activities[1]
        self.assertIs(type(activity),dict)
        self.assertEqual(activity.get('distance'),10123.5)
        self.assertEqual(activity.get('moving_time'),3601)
        self.assertEqual(activity.get('elevation_gain'),0.0)
        self.assertEqual(activity.get('type'),"Run")
        self.assertEqual(activity.get('strava_id'),1234567890)
        self.assertEqual(activity.get('platform'),"Strava")
        self.assertEqual(activity.get('start_date_local'),"2018-05-18T19:12:19Z")
        self.assertEqual(activity.get('average_heartrate'),151.1)
        self.assertEqual(activity.get('average_cadence'),82.1)

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
    
    @httpretty.activate
    def test_returned_activity_list_in_ascending_order_by_date(self):
        """ Test that GetAthleteActivities returns a list with activities"""
        self.register_get_activities_url_in_httpretty_success_many_unordered()
        activities = get_strava_activities(token="87a407fc475a61ef97265b4bf8867f3ecfc102af")
        for i in range(1,len(activities)):
            self.assertLess(
                activities[i-1].get('start_date_local'),
                activities[i].get('start_date_local')
            )
#            print(f"{i-1} >> {activities[i-1].get('start_date_local')}")
#            print(f"{i} >> {activities[i].get('start_date_local')}")
#            print(f"{activities[i-1].get('start_date_local') > activities[i].get('start_date_local')}")
#            print(f"-------------------------------------")
#        self.fail('xxx')


    @httpretty.activate
    def test_returns_empty_list_when_no_activities(self):
        """ Test that GetAthleteActivities returns an empty list when there are no activities"""
        self.register_get_activities_url_in_httpretty_success_return_zero()
        activities = get_strava_activities(token="87a407fc475a61ef97265b4bf8867f3ecfc102af")
        self.assertEqual(activities,[])

    @httpretty.activate
    def test_returns_none_on_error(self):
        """Test that GetAthleteActivities returns None when receives a fault"""
        self.register_get_activities_url_in_httpretty_fault()
        activities = get_strava_activities(token="87a407fc475a61ef97265b4bf8867f3ecfc102af")
        self.assertEqual(activities,None)

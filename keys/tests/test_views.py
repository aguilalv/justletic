"""Unit Tests for Keys views"""
from django.test import TestCase
from django.utils.html import escape
from urllib.parse import parse_qsl
from django.contrib import auth

import httpretty
import os

from ..models import Key
from accounts.factories import UserFactory as AccountsUserFactory

from utils.strava_utils import STRAVA_AUTH_ERROR, STRAVA_CODE_EXCHANGE_URL
from utils.strava_utils import STRAVA_GET_ACTIVITIES_URL, STRAVA_CLIENT_ID

class HomePageTest(TestCase):

    """Unit Tests for the Home Page view"""

    def test_uses_home_template(self):
        """Test that home page view renders the right template"""
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'home.html')

class StravaTokenExchangeView(TestCase):

    """Unit test for Keys.StravaTokenExchange view"""

    def create_user_and_login(self,email,password):
        """Helper function to create a user and log it in"""
        self.existing_user = AccountsUserFactory.create(
            email=email,
            password=password
        )
        auth.authenticate(
            email=self.existing_user.email,
            password=self.existing_user.password
        )
        self.client.login(email='edith@mailinator.com', password='epwd')

    def register_token_exchange_url_in_httpretty(self):
        mock_body = '''
            {"access_token":"87a407fc475a61ef97265b4bf8867f3ecfc102af",
            "token_type":"Bearer",
            "athlete":
            {"id":1234567,
                "username":"edith",
                "resource_state":2,
                "firstname":"Edith",
                "lastname":"Jones",
                "city":"London",
                "state":"England",
                "country":"United Kingdom",
                "sex":"F",
                "premium":false,
                "created_at":"2014-06-21T21:36:33Z",
                "updated_at":"2018-04-26T20:20:03Z",
                "badge_type_id":0,
                "profile_medium":"https://dgalywyr863hv.cloudfront.net/pictures/athletes/5331809/5624577/1/medium.jpg",
                "profile":"https://dgalywyr863hv.cloudfront.net/pictures/athletes/5331809/5624577/1/large.jpg",
                "friend":null,
                "follower":null,
                "email":"edith@mailinator.com"}}
        '''   
        httpretty.register_uri(
            httpretty.POST,
            STRAVA_CODE_EXCHANGE_URL,
            body = mock_body
        )
    
    def register_get_activities_url_in_httpretty(self):
        mock_body = '''
            [{"resource_state":2,
                "athlete":{
                    "id":21400992,
                    "resource_state":1
                },
                "name":"Evening Run",
                "distance":7972.5,
                "moving_time":2909,
                "elapsed_time":2909,
                "total_elevation_gain":110.0,
                "type":"Run",
                "workout_type":3,
                "id":1574689979,
                "external_id":"2701804443.fit",
                "upload_id":1693199790,
                "start_date":"2018-05-15T18:12:19Z",
                "start_date_local":"2018-05-15T19:12:19Z",
                "timezone":"(GMT+00:00) Europe/London",
                "utc_offset":3600.0,
                "start_latlng":[51.579065,-0.150119],
                "end_latlng":[51.579198,-0.150102],
                "location_city":null,
                "location_state":null,
                "location_country":"Reino Unido",
                "start_latitude":51.579065,
                "start_longitude":-0.150119,
                "achievement_count":0,
                "kudos_count":0,
                "comment_count":0,
                "athlete_count":2,
                "photo_count":0,
                "map":{
                    "id":"a1574689979",
                    "summary_polyline":"c`yyHfi\\\\mAs@aFhDkCbJiFrCaMaHuF{YyBo@iBmUaFoHmNcJJqEcJcOkEcV~AwGgCgG{E_JgBKaC|W}AlAuB_FlCkH}AiFu@sPbEmKsDwPtXlXfDnHbBhOsDba@nG~PdApH]dEbNdI|FtIbB`TxAHxDjXzF`HnG~A`HuBnAeJlE{DfBf@",
                    "resource_state":2
                },
                "trainer":false,
                "commute":false,
                "manual":false,
                "private":false,
                "flagged":false,
                "gear_id":null,
                "from_accepted_tag":false,
                "average_speed":2.741,
                "max_speed":11.6,
                "average_cadence":79.1,
                "average_temp":22.0,
                "has_heartrate":true,
                "average_heartrate":151.1,
                "max_heartrate":161.0,
                "elev_high":103.0,
                "elev_low":38.2,
                "pr_count":0,
                "total_photo_count":0,
                "has_kudoed":false
            }]
        '''   
        httpretty.register_uri(
            httpretty.GET,
            STRAVA_GET_ACTIVITIES_URL,
            body = mock_body
        )

    def setUp(self):
        """Create a user in the database and log it in before runinng each test"""
        self.create_user_and_login('edith@mailinator.com','epwd')

    @httpretty.activate
    def test_sends_get_request_with_code_received(self):
        """Test that when receiving a code the view sends request to exchange for a token"""
        self.register_token_exchange_url_in_httpretty()
        expected_parameters = {
            'client_id': STRAVA_CLIENT_ID,
            'client_secret': os.environ['STRAVA_CLIENT_SECRET'], 
            'code': 'abc123',
        }

        self.client.get('/users/stravatokenexchange?state=&code=abc123') 
       
        requested_url = 'https://'+httpretty.last_request().headers.get('Host') +\
            httpretty.last_request().path
        sent_parameters = dict(parse_qsl(httpretty.last_request().body.decode()))

        self.assertEqual(STRAVA_CODE_EXCHANGE_URL,requested_url) 
        self.assertEqual(
            sent_parameters,
            expected_parameters
        ) 
      
    @httpretty.activate
    def test_shows_error_message_when_receives_error_code(self):
        """Test that when view receives an error it displays a message"""
        expected_error = escape(STRAVA_AUTH_ERROR)
        text_to_receive = '''
            {
                "message":"Bad Request",
                "errors":[{
                    "resource":"Application",
                    "field":"client_id",
                    "code":"invalid"
                }]
            }'''

        httpretty.register_uri(
            httpretty.POST,
            'https://www.strava.com/oauth/token',
            body = text_to_receive
        )

        response = self.client.get('/users/stravatokenexchange?state=&code=abc123')
        self.assertContains(response, expected_error)
    
    @httpretty.activate
    def test_render_congratulations_message_on_success(self):
        """Test that the view renders a congratulations message
        after a successful token exchange"""
        self.register_token_exchange_url_in_httpretty()
        
        response = self.client.get('/users/stravatokenexchange?state=&code=abc123')         
        self.assertTemplateUsed(response, 'congratulations.html')
    
    @httpretty.activate
    def test_stores_token_and_strava_id_in_database(self):
        """Test that Strava Token Exchange view stores the new token and the 
        users strava id in the database"""
        self.register_token_exchange_url_in_httpretty()
        
        self.assertEqual(Key.objects.count(),0)

        response = self.client.get('/users/stravatokenexchange?state=&code=abc123')         
        self.assertEqual(Key.objects.count(),1)
        self.assertEqual(Key.objects.all()[0].token,'87a407fc475a61ef97265b4bf8867f3ecfc102af')
        self.assertEqual(Key.objects.all()[0].strava_id,'1234567')
       
    @httpretty.activate
    def test_links_token_and_stravaid_to_logged_in_user(self):
        """Test that Strava Token Exchange view links in the database
        the token and strava id  with the user that is logged in"""
        self.register_token_exchange_url_in_httpretty()
       
        response = self.client.get('/users/stravatokenexchange?state=&code=abc123')         
        stored_key = Key.objects.all()[0]
        self.assertEqual(stored_key.user.email,'edith@mailinator.com')
        self.assertEqual(stored_key.token,'87a407fc475a61ef97265b4bf8867f3ecfc102af')
        self.assertEqual(stored_key.strava_id,'1234567')

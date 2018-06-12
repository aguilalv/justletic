"""Unit Tests for logs for Keys views"""
from unittest.mock import patch, call

from django.test import TestCase
from django.contrib import auth

class HomePageTest(TestCase):

    """Unit Tests for logs in the Home Page view"""

    @patch("keys.views.logger")
    def test_calls_logger(self,mock_logger):
        """Test that keys.home view calls logger.info"""
        response = self.client.get("/")
        self.assertEqual(mock_logger.info.called,True)
        message_used = mock_logger.info.call_args
        self.assertEqual(call("keys.views.home - end"),message_used)


class StravaTokenExchangeView(TestCase):

    """Unit test for logs in Keys.StravaTokenExchange view"""

    def create_user_and_login(self, email, password):
        """Helper function to create a user and log it in"""
        user_model = auth.get_user_model()
        self.existing_user = user_model.objects.create_user(
            username=email, email=email, password=password
        )
        auth.authenticate(
            username=self.existing_user.email, password=self.existing_user.password
        )
        self.client.login(username="edith@mailinator.com", password="epwd")

    def setUp(self):
        """Create a user in the database and log it in before runinng each test"""
        self.create_user_and_login("edith@mailinator.com", "epwd")

    @patch("keys.views.logger")
    @patch("keys.views.exchange_strava_code")
    @patch("keys.views.get_strava_activities")
    def test_calls_logger_when_receives_correct_token(
        self,mock_get_activities,mock_exchange_code,mock_logger):
        """Test that keys.StravaTokenExchange view calls logger info"""
        mock_exchange_code.return_value = ("Token", "Strava_id")
        response = self.client.get("/users/stravatokenexchange?state=&code=abc123")
        self.assertEqual(mock_logger.info.called,True)
        message_used = mock_logger.info.call_args
        self.assertEqual(call("keys.views.stravatokenexchange - end"),message_used)

    @patch("keys.views.logger")
    @patch("keys.views.exchange_strava_code")
    @patch("keys.views.get_strava_activities")
    def test_calls_logger_when_receives_none_as_token(
        self,mock_get_activities,mock_exchange_code,mock_logger):
        """Test that keys.StravaTokenExchange view calls logger info when receives none as token"""
        mock_exchange_code.return_value = (None, "2")
        response = self.client.get("/users/stravatokenexchange?state=&code=abc123")
        self.assertEqual(mock_logger.info.called,True)
        message_used = mock_logger.info.call_args
        self.assertEqual(call("keys.views.stravatokenexchange - error"),message_used)

    @patch("keys.views.logger")
    @patch("keys.views.exchange_strava_code")
    @patch("keys.views.get_strava_activities")
    def test_calls_logger_when_receives_none_as_strava_id(
        self,mock_get_activities,mock_exchange_code,mock_logger):
        """Test that keys.StravaTokenExchange view calls logger info when receives none as strava id"""
        mock_exchange_code.return_value = ("2", None)
        response = self.client.get("/users/stravatokenexchange?state=&code=abc123")
        self.assertEqual(mock_logger.info.called,True)
        message_used = mock_logger.info.call_args
        self.assertEqual(call("keys.views.stravatokenexchange - error"),message_used)

    @patch("keys.views.logger")
    @patch("keys.views.exchange_strava_code")
    @patch("keys.views.get_strava_activities")
    def test_calls_loger_when_receives_strava_activities_ok(
        self, mock_get_activities, mock_exchange_code, mock_logger):
        """Test that keys.StravaTokenExchange calls logger info when receives strava activities ok"""
        expected_km_number = 3.14
        mock_exchange_code.return_value = ("Token", "Id")
        mock_get_activities.return_value = [
            {
                "distance": expected_km_number * 1000,
                "moving_time": 100,
                "elevation_gain": 100,
                "type": "Run",
                "strava_id": 1574689979,
                "platform": "Strava",
                "start_date_local": "2018-05-15T19:12:19Z",
                "average_heartrate": 151.1,
                "average_cadence": 79.1,
            }
        ]
        response = self.client.get("/users/stravatokenexchange?state=&code=abc123")
        self.assertEqual(mock_logger.info.called,True)
        message_used = mock_logger.info.call_args
        self.assertEqual(call("keys.views.stravatokenexchange - end"),message_used)

    @patch("keys.views.logger")
    @patch("keys.views.exchange_strava_code")
    @patch("keys.views.get_strava_activities")
    def test_calls_loger_when_receives_none_as_strava_activities(
        self, mock_get_activities, mock_exchange_code, mock_logger):
        """Test that keys.StravaTokenExchange calls logger info when receives strava activities ok"""
        mock_exchange_code.return_value = ("Token", "Id")
        mock_get_activities.return_value = None
        response = self.client.get("/users/stravatokenexchange?state=&code=abc123")
        self.assertEqual(mock_logger.info.called,True)
        message_used = mock_logger.info.call_args
        self.assertEqual(call("keys.views.stravatokenexchange - error"),message_used)

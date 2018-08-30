"""Tests for logs in Keys views"""
from unittest.mock import patch, call, Mock

from django.test import TestCase
from django.contrib import auth

class StravaTokenExchangeView(TestCase):

    """Tests for logs in Keys.views.StravaTokenExchange view"""

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
        """Create a user and log it in before runinng each test"""
        self.create_user_and_login("edith@mailinator.com", "epwd")

    @patch("keys.views.logger.bind")
    @patch("keys.views.exchange_strava_code")
    @patch("keys.views.get_strava_activities")
    def test_calls_logger_on_success(
        self, mock_get_activities, mock_exchange_code, mock_logger_bind
    ):
        """Test keys.views.StravaTokenExchanges calls logger info"""
        bound_logger = Mock()
        mock_logger_bind.return_value = bound_logger

        mock_exchange_code.return_value = ("Token", "Strava_id")
        response = self.client.get("/keys/stravatokenexchange?state=&code=abc123")
        info_calls = bound_logger.mock_calls
        self.assertEqual(len(info_calls),2)
        self.assertEqual(call("Access to Strava authorised"),info_calls[0])
        self.assertEqual(call("Strava activity summary received"),info_calls[1])

    @patch("keys.views.logger")
    @patch("keys.views.exchange_strava_code")
    @patch("keys.views.get_strava_activities")
    def test_binds_logged_in_user(
        self, mock_get_activities, mock_exchange_code, mock_logger
    ):
        """Test keys.views.StravaTokenExchanges binds logged in user to logger"""
        mock_exchange_code.return_value = ("Token", "Strava_id")
        response = self.client.get("/keys/stravatokenexchange?state=&code=abc123")
        self.assertTrue(mock_logger.bind.called)
        user_bound = mock_logger.bind.call_args
        self.assertEqual(call(user='edith@mailinator.com'),user_bound)
    
    @patch("keys.views.logger.bind")
    @patch("keys.views.exchange_strava_code")
    @patch("keys.views.get_strava_activities")
    def test_calls_logger_when_receives_none_as_token(
        self, mock_get_activities, mock_exchange_code, mock_logger_bind
    ):
        """Test keys.views.StravaTokenExchanges calls logger info when receives error token"""
        bound_logger = Mock()
        mock_logger_bind.return_value = bound_logger

        mock_exchange_code.return_value = (None, "2")
        response = self.client.get("/keys/stravatokenexchange?state=&code=abc123")
        self.assertTrue(bound_logger.info.called)
        message_used = bound_logger.info.call_args
        self.assertEqual(call("Received Strava error in token exchange"),message_used)

    @patch("keys.views.logger.bind")
    @patch("keys.views.exchange_strava_code")
    @patch("keys.views.get_strava_activities")
    def test_calls_logger_when_receives_none_as_strava_id(
        self, mock_get_activities, mock_exchange_code, mock_logger_bind
    ):
        """Test keys.views.StravaTokenExchanges calls logger when receives error token"""
        bound_logger = Mock()
        mock_logger_bind.return_value = bound_logger

        mock_exchange_code.return_value = ("2",None)
        response = self.client.get("/keys/stravatokenexchange?state=&code=abc123")
        self.assertTrue(bound_logger.info.called)
        message_used = bound_logger.info.call_args
        self.assertEqual(call("Received Strava error in token exchange"),message_used)

    @patch("keys.views.logger.bind")
    @patch("keys.views.exchange_strava_code")
    @patch("keys.views.get_strava_activities")
    def test_renders_home_when_receives_none_as_activities(
            self, mock_get_activities, mock_exchange_code, mock_logger_bind
    ):
        """Test keys.views.StravaTokenExchanges calls logger info when receives error activity summary"""
        bound_logger = Mock()
        mock_logger_bind.return_value = bound_logger
        mock_exchange_code.return_value = ("Token", "Id")
        mock_get_activities.return_value = None
        response = self.client.get("/keys/stravatokenexchange?state=&code=abc123")
        info_calls = bound_logger.mock_calls
        self.assertEqual(len(info_calls),2)
        self.assertEqual(call("Access to Strava authorised"),info_calls[0])
        self.assertEqual(call("Received Strava error for activity summary"),info_calls[1])


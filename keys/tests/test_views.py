"""Unit Tests for Keys views"""
from unittest.mock import patch, call

from django.test import TestCase
from django.utils.html import escape
from django.contrib import auth

from ..models import Key
from ..forms import HeroForm

from utils.strava_utils import STRAVA_AUTH_ERROR
from accounts.forms import LoginForm, ChangePasswordForm

class HomePageTest(TestCase):

    """Unit Tests for the Home Page view"""

    def test_uses_home_template(self):
        """Test keys.views.home renders right template"""
        response = self.client.get("/")
        self.assertTemplateUsed(response, "home.html")

    def test_uses_hero_form(self):
        """Test keys.views.home uses the hero form"""
        response = self.client.get("/")
        form_used = response.context['hero_form']
        self.assertIsInstance(form_used, HeroForm)
    
    def test_uses_login_form(self):
        """Test keys.views.home uses the login form"""
        response = self.client.get("/")
        form_used = response.context['login_form']
        self.assertIsInstance(form_used, LoginForm)

class StravaTokenExchangeView(TestCase):

    """Unit test for Keys.StravaTokenExchange view"""

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

    @patch("keys.views.exchange_strava_code")
    @patch("keys.views.get_strava_activities")
    def test_calls_exchange_strava_code_helper_function(
        self, mock_get_activities, mock_exchange_code
    ):
        """Test keys.views.strava_token_exchange calls exchange strava code helper function"""
        mock_exchange_code.return_value = ("Token", "Strava_id")
        response = self.client.get("/users/stravatokenexchange?state=&code=abc123")
        self.assertTrue(mock_exchange_code.called)

    @patch("keys.views.exchange_strava_code")
    @patch("keys.views.get_strava_activities")
    def test_exchange_strava_code_receives_code_from_request(
        self, mock_get_activities, mock_exchange_code
    ):
        """Test keys.views.strava_token_exchange sends code received to exchange strava code helper function"""
        mock_exchange_code.return_value = ("Token", "Strava_id")
        response = self.client.get("/users/stravatokenexchange?state=&code=abc123")
        used_args = mock_exchange_code.call_args
        self.assertEqual(used_args, call("abc123"))

    @patch("keys.views.exchange_strava_code")
    @patch("keys.views.get_strava_activities")
    def test_shows_error_message_when_receives_none_as_token(
        self, mock_get_activities, mock_exchange_code
    ):
        """Test keys.views.strava_token_exchange displays error when receives None as token"""
        mock_exchange_code.return_value = (None, "2")
        expected_error = escape(STRAVA_AUTH_ERROR)
        response = self.client.get("/users/stravatokenexchange?state=&code=abc123")
        self.assertContains(response, expected_error)

    @patch("keys.views.exchange_strava_code")
    @patch("keys.views.get_strava_activities")
    def test_shows_error_message_when_receives_none_as_strava_id(
        self, mock_get_activities, mock_exchange_code
    ):
        """Test keys.views.strava_token_exchange displays error when receives None as strava_id"""
        mock_exchange_code.return_value = ("2", None)
        expected_error = escape(STRAVA_AUTH_ERROR)
        response = self.client.get("/users/stravatokenexchange?state=&code=abc123")
        self.assertContains(response, expected_error)

    @patch("keys.views.exchange_strava_code")
    @patch("keys.views.get_strava_activities")
    def test_stores_token_and_strava_id_in_database(
        self, mock_get_activities, mock_exchange_code
    ):
        """Test keys.views.strava_token_exchange stores token and strava id received"""
        mock_exchange_code.return_value = ("Token", "Strava_id")

        self.assertEqual(Key.objects.count(), 0)

        response = self.client.get("/users/stravatokenexchange?state=&code=abc123")
        self.assertEqual(Key.objects.count(), 1)
        self.assertEqual(Key.objects.all()[0].token, "Token")
        self.assertEqual(Key.objects.all()[0].strava_id, "Strava_id")

    @patch("keys.views.exchange_strava_code")
    @patch("keys.views.get_strava_activities")
    def test_links_token_and_stravaid_to_logged_in_user(
        self, mock_get_activities, mock_exchange_code
    ):
        """Test keys.views.strava_token_exchange linkss token and id to user logged in"""
        mock_exchange_code.return_value = ("Token", "Strava_id")

        response = self.client.get("/users/stravatokenexchange?state=&code=abc123")
        stored_key = Key.objects.all()[0]
        self.assertEqual(stored_key.user.email, "edith@mailinator.com")
        self.assertEqual(stored_key.token, "Token")
        self.assertEqual(stored_key.strava_id, "Strava_id")

    @patch("keys.views.exchange_strava_code")
    @patch("keys.views.get_strava_activities")
    def test_uses_congratulations_template_on_success(
        self, mock_get_activities, mock_exchange_code
    ):
        """Test keys.views.strava_token_exchange renders right template"""
        mock_exchange_code.return_value = ("Token", "Strava_id")

        response = self.client.get("/users/stravatokenexchange?state=&code=abc123")
        self.assertTemplateUsed(response, "congratulations.html")

    @patch("keys.views.exchange_strava_code")
    @patch("keys.views.get_strava_activities")
    def test_includes_change_password_form_on_succes(
        self, mock_get_activities, mock_exchange_code
    ):
        """ Test keys.view.strava_token_exchange includes change_password form in the context on success"""
        mock_exchange_code.return_value = ("Token", "Strava_id")
        response = self.client.get("/users/stravatokenexchange?state=&code=abc123")
        form_used = response.context['change_password_form']
        self.assertIsInstance(form_used, ChangePasswordForm)
    
    @patch("keys.views.exchange_strava_code")
    @patch("keys.views.get_strava_activities")
    def test_calls_get_strava_activities_on_success(
        self, mock_get_activities, mock_exchange_code
    ):
        """Test keys.views.strava_token_exchange calls get strava activities helper after succesful exchange"""
        mock_exchange_code.return_value = ("Token", "Strava_id")

        response = self.client.get("/users/stravatokenexchange?state=&code=abc123")
        self.assertTrue(mock_get_activities.called)

    @patch("keys.views.exchange_strava_code")
    @patch("keys.views.get_strava_activities")
    def test_calls_get_strava_activities_with_token_argument(
        self, mock_get_activities, mock_exchange_code
    ):
        """Test keys.views.strava_token_exchange sends token received to get strava activities helper after succesful exchange"""
        mock_exchange_code.return_value = ("Token", "Strava_id")

        response = self.client.get("/users/stravatokenexchange?state=&code=abc123")
        used_args = mock_get_activities.call_args
        self.assertEqual(used_args, call("Token"))

    @patch("keys.views.exchange_strava_code")
    @patch("keys.views.get_strava_activities")
    def test_shows_km_from_last_activity_on_success(
        self, mock_get_activities, mock_exchange_code
    ):
        """Test keys.views.strava_token_exchange renders distance from last run"""
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
        self.assertContains(response, expected_km_number)

    @patch("keys.views.exchange_strava_code")
    @patch("keys.views.get_strava_activities")
    def test_renders_home_on_failure(self, mock_get_activities, mock_exchange_code):
        """Test keys.views.strava_token_exchange renders home if receives error activity summary"""
        mock_exchange_code.return_value = ("Token", "Id")
        mock_get_activities.return_value = None
        response = self.client.get("/users/stravatokenexchange?state=&code=abc123")
        self.assertTemplateUsed(response, "home.html")

    @patch("keys.views.exchange_strava_code")
    @patch("keys.views.get_strava_activities")
    def test_shows_message_on_failure(self, mock_get_activities, mock_exchange_code):
        """Test keys.views.strava_token_exchange displays error if receives error activity summary"""
        mock_exchange_code.return_value = ("Token", "Id")
        mock_get_activities.return_value = None
        expected_error = escape(STRAVA_AUTH_ERROR)
        response = self.client.get("/users/stravatokenexchange?state=&code=abc123")
        self.assertContains(response, expected_error)

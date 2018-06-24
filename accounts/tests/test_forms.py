"""Unit tests for Accounts forms"""
from django.test import TestCase

from ..forms import LoginForm


class LoginFormTest(TestCase):

    """Unit tests for accounts LoginForm form"""
    
    def test_correct_inputs_pass_validation(self):
        """Test accounts.forms.login_form validation with correct inputs passes"""
        form_data = {"email": "edith@mailinator.com", "password": "epwd"}
        form = LoginForm(data=form_data)
        self.assertEqual(form.is_valid(), True)

    def test_empty_email_fails_validation(self):
        """Test accounts.forms.login_form validation with empty email fails"""
        form_data = {"email": "", "password": "epwd"}
        form = LoginForm(data=form_data)
        self.assertEqual(form.is_valid(), False)

    def test_empty_password_fails_validation(self):
        """Test accounts.forms.login_form validation with empty password fails"""
        form_data = {"email": "edith@mailinator.com", "password": ""}
        form = LoginForm(data=form_data)
        self.assertEqual(form.is_valid(), False)
    
    def test_wrong_format_email_fails_validation(self):
        """Test accounts.forms.login_form validation with wrong email fails"""
        form_data = {"email": "aaa", "password": "epwd"}
        form = LoginForm(data=form_data)
        self.assertEqual(form.is_valid(), False)

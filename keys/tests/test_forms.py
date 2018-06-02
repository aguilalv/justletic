"""Unit tests for Keys forms"""
from django.test import TestCase

from ..forms import HeroForm

class HeroFormTest(TestCase):

    """Unit tests for keys HeroForm form"""

    def test_empty_email_fails_validation(self):
        """Test that validation of a form with email field empty fails"""
        form_data = {
            'email': ''
        }
        form = HeroForm(data=form_data) 
        self.assertEqual(form.is_valid(),False)

    def test_wrong_format_email_fails_validation(self):
        """Test that validation of a form with wrong format email field fails"""
        form_data = {
            'email': 'aaaa'
        }
        form = HeroForm(data=form_data) 
        self.assertEqual(form.is_valid(),False)

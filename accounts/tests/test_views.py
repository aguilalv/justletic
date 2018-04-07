from django.test import TestCase
from django.utils.html import escape
from django.contrib import auth
from django.urls import reverse

from ..factories import UserFactory as AccountsUserFactory
from keys.factories import UserFactory as KeysUserFactory

class LoginViewTest(TestCase):

    def setUp(self):
        # Create factory default user [email=edith@mailinator.com/password = epwd]
        self.existing_user = AccountsUserFactory.create()
        # Create keys/user to redirect to (need to refactor this out)
        self.existing_keysuser = KeysUserFactory.create()

    def test_POST_logs_user_in_if_password_correct(self):
        response = self.client.post(
            '/accounts/login', 
            data={'email': 'edith@mailinator.com','password': 'epwd'}
        )
        user = auth.get_user(self.client)
        self.assertTrue(user.is_authenticated)

#    def test_POST_success_redirects_to_user_summary(self):
#        response = self.client.post(
#            '/accounts/login', 
#            data={'email': 'edith@mailinator.com','password': 'epwd'}
#        )
#        self.assertRedirects(response,f'/users/{self.existing_user.id}/')

    def test_POST_success_redirects_to_home_page(self):
        response = self.client.post(
            '/accounts/login', 
            data={'email': 'edith@mailinator.com','password': 'epwd'}
        )
        self.assertRedirects(response,reverse('home'))
    
    def test_POST_fail_renders_home_page(self):
        response = self.client.post(
            '/accounts/login', 
            data={'email': 'edith@mailinator.com','password': 'wrongpwd'}
        )
        self.assertTemplateUsed(response, 'home.html')
    
    def test_POST_fail_shows_error(self):
        response = self.client.post(
            '/accounts/login', 
            data={'email': 'edith@mailinator.com','password': 'wrongpwd'}
        )
        expected_error = escape("Ooops, wrong user or password")
        self.assertContains(response, expected_error)

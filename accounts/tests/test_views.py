from django.test import TestCase
from django.utils.html import escape
from django.contrib import auth
from django.urls import reverse

from ..views import LOGIN_ERROR

from ..factories import UserFactory as AccountsUserFactory
from keys.factories import UserFactory as KeysUserFactory

class LoginViewTest(TestCase):

    def setUp(self):
        self.existing_user = AccountsUserFactory.create(
            email='edith@mailinator.com',
            password='epwd'
        )
        #TODO Create keys/user to redirect to (need to refactor this out)
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
    
    def test_POST_wrong_password_renders_home_page(self):
        response = self.client.post(
            '/accounts/login', 
            data={'email': 'edith@mailinator.com','password': 'wrongpwd'}
        )
        self.assertTemplateUsed(response, 'home.html')
    
    def test_POST_wrong_password_shows_error(self):
        response = self.client.post(
            '/accounts/login', 
            data={'email': 'edith@mailinator.com','password': 'wrongpwd'}
        )
        expected_error = escape(LOGIN_ERROR)
        self.assertContains(response, expected_error)

    def test_POST_non_existing_user_renders_home_page(self):
        response = self.client.post(
            '/accounts/login', 
            data={'email': 'non_existent@non.com','password': 'wrongpwd'}
        )
        self.assertTemplateUsed(response, 'home.html')

    def test_POST_non_existing_user_shows_error(self):
        response = self.client.post(
            '/accounts/login', 
            data={'email': 'non_existent@non.com','password': 'wrongpwd'}
        )
        expected_error = escape(LOGIN_ERROR)
        self.assertContains(response, expected_error)

class LogoutViewTest(TestCase):

    def setUp(self):
        self.existing_user = AccountsUserFactory.create(
            email='edith@mailinator.com',
            password='epwd'
        )
        user = auth.authenticate(
            email = self.existing_user.email,
            password = self.existing_user.password
        )
        self.client.login(email='edith@mailinator.com',password='epwd')
    
    def test_renders_home_page(self):
        response = self.client.post(
            '/accounts/logout' 
        )
        self.assertTemplateUsed(response, 'home.html')

    def test_logs_user_out(self):
        response = self.client.post(
            '/accounts/logout' 
        )
        user = auth.get_user(self.client)
        self.assertFalse(user.is_authenticated)
        

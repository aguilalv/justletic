from django.urls import resolve
from django.test import TestCase
from django.http import HttpRequest

from .models import Key,User

class HomePageTest(TestCase):

    def test_uses_home_template(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'home.html')
    
    def test_GET_does_not_save(self):
        self.client.get('/')
        self.assertEqual(Key.objects.all().count(),0)


class UserSummaryViewTest(TestCase):

    def test_uses_user_template(self):
        response = self.client.get('/users/the-only-user/')
        self.assertTemplateUsed(response, 'user.html')
    
    def test_displays_all_keys(self):
        user = User()
        user.email = 'emailey 1'
        user.save()

        Key.objects.create(value='value1', user=user)
        Key.objects.create(value='value2', user=user)

        response = self.client.get('/users/the-only-user/')

        self.assertContains(response, 'value1')
        self.assertContains(response, 'value2')


class NewUserTest(TestCase):

    def test_POST_saves_email_and_key(self):
        response = self.client.post('/users/new', data={'email': 'edith@mailinator.com'})
        
        self.assertEqual(User.objects.count(), 1)
        new_user = User.objects.all()[0]
        self.assertEqual(new_user.email, 'edith@mailinator.com')
        
        self.assertEqual(Key.objects.count(), 1)
        new_key = Key.objects.all()[0]
        self.assertEqual(new_key.value, 'e1234')
        self.assertEqual(new_key.user, new_user)

    def test_POST_redirects_after_save(self):
        response = self.client.post('/users/new', data={'email': 'edith@mailinator.com'})
        
        self.assertRedirects(response, '/users/the-only-user/')


class UserAndKeyModelTest(TestCase):

    def test_saving_and_retrieving_keys(self):
        user = User()
        user.save()

        first_key = Key()
        first_key.value = 'First'
        first_key.user = user
        first_key.save()

        second_key = Key()
        second_key.value = 'Second'
        second_key.user = user
        second_key.save()

        saved_user = User.objects.all()[0]
        self.assertEqual(saved_user, user)

        saved_keys = Key.objects.all()
        self.assertEqual(saved_keys.count(), 2)

        first_saved_key = saved_keys[0]
        second_saved_key = saved_keys[1]
        self.assertEqual(first_saved_key.value, first_key.value)
        self.assertEqual(first_saved_key.user, first_key.user)
        self.assertEqual(second_saved_key.value, second_key.value)
        self.assertEqual(second_saved_key.user, second_key.user)


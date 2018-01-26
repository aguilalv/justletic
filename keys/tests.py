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


class UserViewTest(TestCase):

    def test_uses_user_template(self):
        user = User.objects.create(email= 'emailey 1')
        response = self.client.get(f'/users/{user.id}/')
        
        self.assertTemplateUsed(response, 'user.html')
    
    def test_displays_only_keys_for_that_user(self):
        correct_user = User.objects.create(email= 'emailey 1')
        wrong_user = User.objects.create(email= 'emailey 2')

        Key.objects.create(value='value 1', user=correct_user)
        Key.objects.create(value='value 2', user=correct_user)

        Key.objects.create(value='other value 1', user=wrong_user)
        Key.objects.create(value='other value 2', user=wrong_user)

        response = self.client.get(f'/users/{correct_user.id}/')

        self.assertContains(response, 'value 1')
        self.assertContains(response, 'value 2')
        self.assertNotContains(response, 'other value 1')
        self.assertNotContains(response, 'other value 2')


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
        user = User.objects.first()

        self.assertRedirects(response,f'/users/{user.id}/')

class NewServiceTest(TestCase):
    
    def test_can_save_POST_request_to_an_existing_user(self):
        other_user = User.objects.create()
        correct_user = User()
        correct_user.email = 'anne@mailinator.com'
        correct_user.save()

        self.client.post(
            f'/users/{correct_user.id}/add_service'
        )

        self.assertEqual(Key.objects.count(), 1)
        new_key = Key.objects.first()
        self.assertEqual(new_key.value, 'n1234')
        self.assertEqual(new_key.user, correct_user)

    def test_redirects_to_user_view(self):
        other_user = User.objects.create()
        correct_user = User()
        correct_user.email = 'anne@mailinator.com'
        correct_user.save()
        
        response = self.client.post(
            f'/users/{correct_user.id}/add_service'
        )

        self.assertRedirects(response,f'/users/{correct_user.id}/')

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


from django.test import TestCase
from django.utils.html import escape
from ..models import Key,User

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

    def test_validation_errors_are_sent_back_to_home_page_template(self):
        response = self.client.post('/users/new', data={'email': ''})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')
        expected_error = escape("You need to enter a valid email")
        self.assertContains(response, expected_error)

    def test_invalid_users_are_not_saved(self):
        response = self.client.post('/users/new', data={'email': ''})
        self.assertEqual(User.objects.count(), 0)

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

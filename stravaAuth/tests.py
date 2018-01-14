from django.urls import resolve
from django.test import TestCase
from django.http import HttpRequest

from stravaAuth.models import Key

class HomePageTest(TestCase):

    def test_uses_home_template(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'home.html')

    def test_can_save_a_POST_request(self):
        response = self.client.post('/', data={'email': 'edit@mailinator.com'})
        self.assertIn('edit@mailinator.com', response.content.decode())
        self.assertTemplateUsed(response,'home.html')

class KeyModelTest(TestCase):

    def test_saving_and_retrieving_items(self):
        first_key = Key()
        first_key.email = 'first_email@mailinator.com'
        first_key.text = '1'
        first_key.save()

        second_key = Key()
        second_key.email = 'second_email@mailinator.com'
        second_key.text = '2'
        second_key.save()

        saved_keys = Key.objects.all()
        self.assertEqual(saved_keys.count(),2)

        first_saved_key = saved_keys[0]
        second_saved_key = saved_keys[1]
        self.assertEqual (first_saved_key.email, 'first_email@mailinator.com')
        self.assertEqual (first_saved_key.text, '1')
        self.assertEqual (second_saved_key.email, 'second_email@mailinator.com')
        self.assertEqual (second_saved_key.text, '2')





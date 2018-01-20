from django.urls import resolve
from django.test import TestCase
from django.http import HttpRequest

from keys.models import Key

class HomePageTest(TestCase):

    def test_uses_home_template(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'home.html')
    
    def test_GET_does_not_save(self):
        self.client.get('/')
        self.assertEqual(Key.objects.all().count(),0)

    def test_GET_displays_all_keys(self):
        Key.objects.create(email='emailey1')
        Key.objects.create(email='emailey2')

        response = self.client.get('/')

        self.assertIn ('emailey1',response.content.decode())
        self.assertIn ('emailey2',response.content.decode())

    def test_POST_saves_email(self):
        response = self.client.post('/', data={'email': 'edith@mailinator.com'})
        
        self.assertEqual(Key.objects.count(),1)
        new_key = Key.objects.all()[0]
        self.assertEqual(new_key.email, 'edith@mailinator.com')

    def test_POST_redirects_after_save(self):
        response = self.client.post('/', data={'email': 'edith@mailinator.com'})
        
        self.assertEqual(response.status_code,302)
        self.assertEqual(response['location'],'/')


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





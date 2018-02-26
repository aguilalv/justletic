from unittest import skip
from django.test import TestCase
from django.core.exceptions import ValidationError
from ..models import Key,User

class UserAndKeyModelTest(TestCase):

    def test_saving_and_retrieving_keys(self):
        user = User(email='edith@mailinator.com')
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

    def test_cannot_save_empty_email(self):
        user = User(email='')
        with self.assertRaises(ValidationError):
            user.full_clean()
            user.save()

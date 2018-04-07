from django.test import TestCase
from ..models import User

class UserModelTest(TestCase):

    def test_saving_and_retrieving_users(self):
        user = User(email='edith@mailinator.com')
        user.save()
        
        saved_user = User.objects.all()[0]
        self.assertEqual(saved_user, user)

    def test_saving_and_checking_password(self):
        user = User(email='edith@mailinator.com')
        user.set_password('epwd')
        user.save()

        saved_user = User.objects.all()[0]
        self.assertTrue(saved_user.check_password('epwd'))
        self.assertFalse(saved_user.check_password('other'))


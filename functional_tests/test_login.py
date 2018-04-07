from selenium.webdriver.common.keys import Keys
from unittest import skip

from .base import FunctionalTest
from accounts.factories import UserFactory as AccountsUserFactory
from keys.factories import UserFactory as KeysUserFactory


class LoginTest(FunctionalTest):
    
    def setUp(self):
        self.user = AccountsUserFactory.create()
        KeysUserFactory.create(id=self.user.id)
        return super(LoginTest, self).setUp()
    
    
    @skip("Test still not implemented")
    def test_can_create_new_user(self):
        pass
    
    
    def test_existing_user_can_login_with_correct_password(self):
        # Edith goes to the justletic page
        # she notices a "Log in" button in the navbar for the first time
        # when she clicks the log in button a modal appears
        self.browser.get(self.live_server_url)
        login_link = self.browser.find_element_by_id('id_login_button')
        login_link.click()
        modal = self.browser.find_element_by_id('id_login_modal')
        self.assertTrue(modal.is_displayed())

        # It's telling her to enter her email address and password, 
        # so she does and clicks the button
        email_in = self.browser.find_element_by_id('id_modal_email_in')
        password_in = self.browser.find_element_by_id('id_modal_password_in')
        submit_btn = self.browser.find_element_by_id('id_modal_button')
        email_in.send_keys('edith@mailinator.com')
        password_in.send_keys('epwd')
        submit_btn.click() 

        # The navbar menu indicates she is now logged in
        logout = self.browser.find_element_by_id('id_logout_button')
        logged_in_email = self.browser.find_element_by_id('id_logged_in_email').text
        self.assertEqual(logged_in_email,'edith@mailinator.com')

        # In the future may want to check that she has been redirected to her summary pagee

    @skip("Test still not implemented")
    def test_existing_user_cannot_login_with_incorrect_password(self):
        pass
    
    @skip("Test still not implemented")
    def test_logged_in_user_can_logout(self):
        pass

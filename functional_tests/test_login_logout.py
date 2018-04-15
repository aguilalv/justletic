from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import WebDriverException
from unittest import skip

from accounts.views import LOGIN_ERROR

from .base import FunctionalTest
from accounts.factories import UserFactory as AccountsUserFactory
from keys.factories import UserFactory as KeysUserFactory


class LoginTest(FunctionalTest):
    
    def setUp(self):
        self.user = AccountsUserFactory.create(
            email='edith@mailinator.com',
            password='epwd'
        )
        KeysUserFactory.create(id=self.user.id)
        return super(LoginTest, self).setUp()

    def test_existing_user_can_login_with_correct_password(self):
        # Edith goes to the justletic page and logs in with her password
        self.login_helper('edith@mailinator.com','epwd')

        # The navbar menu indicates she is now logged in
        self.wait_for(lambda: self.browser.find_element_by_id('id_logout_button'))
        self.wait_for(lambda: self.assertEqual(
            self.browser.find_element_by_id('id_logged_in_email').text,
            'edith@mailinator.com'
        ))

        # In the future may want to check that she has been redirected to her summary pagee
        ### TODO

        #Satisfied she goes to sleep    

    def test_existing_user_cannot_login_with_incorrect_password(self):
        # Edith is an existint justletic user (created in set-up)
        # she goes to the justletic page and tries to log in
        # but she enters the wrong password by mistake
        self.login_helper('edith@mailinator.com','wrongpwd')

        # The home page refreshes, and there is an error message
        self.wait_for(lambda: self.assertEqual(
            self.browser.find_element_by_css_selector('.alert-danger').text,
            LOGIN_ERROR
        )) 

        # She tries again with the right password and this time it works
        # The navbar menu indicates she is now logged in
        self.login_helper('edith@mailinator.com','epwd')
        self.wait_for(lambda: self.browser.find_element_by_id('id_logout_button'))
        self.wait_for(lambda: self.assertEqual(
            self.browser.find_element_by_id('id_logged_in_email').text,
            'edith@mailinator.com'
        ))

        # Satisfied she goes to sleep

    def test_logged_in_user_can_logout(self):
        # Edith is an existint justletic user (created in set-up)
        # she is already logged in to Justletic
        self.login_helper('edith@mailinator.com','epwd')

        # She notices a logout button in the navigation bar
        # And clicks on it
        logout_button = self.wait_for(lambda: self.browser.find_element_by_id('id_logout_button'))
        logout_button.click()

        # She notices she has been sent back to the home page
        # and notices she is not logged in anymore
        # because she can see a log in button and she cannot see her email anymore
        self.wait_for(lambda: self.browser.find_element_by_id('id_login_button'))
        with self.assertRaises(WebDriverException):
            self.wait_for(
                lambda: self.browser.find_element_by_id('id_logged_in_email').text
            )

    def test_non_existing_user_cannot_login(self):
        # Francis is still not registered with Justletic
        # he goes to the justletic page and tries to log in
        self.login_helper('francis@mailinator.com','epwd')

        # The home page refreshes, and there is an error message
        self.wait_for(lambda: self.assertEqual(
            self.browser.find_element_by_css_selector('.alert-danger').text,
            LOGIN_ERROR
        )) 

    def login_helper(self, email, password):
        # User notices a "Log in" button in the navbar
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
        email_in.send_keys(email)
        password_in.send_keys(password)
        submit_btn.click() 

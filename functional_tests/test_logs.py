"""Functional tests for logging in and logging out of Justletic"""

from selenium.common.exceptions import WebDriverException
from django.contrib import auth

from accounts.views import LOGIN_ERROR
from .base import FunctionalTest

from unittest import skip

class LogsTest(FunctionalTest):

    """Functional tests for Justletic Logs"""

    def setUp(self):
        """Create a registered user as set-up for all tests"""
        user_model = auth.get_user_model()
        self.existing_user = user_model.objects.create_user(
            'edith@mailinator.com',
            'edith@mailinator.com',
            'epwd'
        )
        return super(LogsTest, self).setUp()

    def tearDown(self):
        return super(LogsTest, self).tearDown()

    def login_helper(self, email, password):
        """Try to log in a user with email and password received as parameters"""
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
    
    @skip('This test needs fixing')
    def test_info_logs_sent_to_terminal_with_right_format(self):
        """Test that logs are sent to terminal (user log in case used as test)"""
        
        with self.assertLogs('',level='INFO') as captured_logs:
            # Edith is an existint justletic user (created in set-up)
            # Edith goes to the justletic page and logs in with her password
            self.login_helper('edith@mailinator.com', 'epwd')

        # An systems admin that was casually looking at the console sees 2 messages with the expected format
    
        print(f'>>> {captured_logs.records}')

        self.assertEqual(captured_logs.records[0].msg,"keys.views.home - end")
        logged_message = captured_logs.records[1].msg 
        self.assertIn("{", logged_message)
        self.assertIn('"event": "Successful login"', logged_message)
        self.assertIn('"logger": "accounts.views"', logged_message)
        self.assertIn('"timestamp":', logged_message)
        self.assertIn('"user": "edith@mailinator.com"', logged_message)
        self.assertIn("}", logged_message)
        
        #Satisfied she goes to sleep (and the admin too)

    @skip('This test needs fixing')
    def test_error_logs_sent_to_terminal_with_right_format(self):
        """Test that logs are sent to terminal (bad user log in case as test)"""
        with self.assertLogs('',level='ERROR') as captured_logs:
            # Edith is an existint justletic user (created in set-up)
            # she goes to the justletic page and tries to log in
            # but she enters the wrong password by mistake
            self.login_helper('edith@mailinator.com', 'wrongpwd')

        # An systems admin that was casually looking at the console sees 2 messages with the expected format
        
        print(f'>>> {captured_logs.records}')
        
        self.assertEqual(captured_logs.records[0].msg,"keys.views.home - end")
        logged_message = captured_logs.records[1].msg 
        self.assertIn("{", logged_message)
        self.assertIn('"email": "edith@mailinator.com"', logged_message)
        self.assertIn('"event": "Failed login attempt"', logged_message) 
        self.assertIn('"logger": "accounts.views"', logged_message)
        self.assertIn('"password": "wrongpwd"', logged_message)
        self.assertIn('"timestamp":', logged_message)
        self.assertIn('}', logged_message)

#        # An error message is logged in the server console
#        # The format of the messages is xxx
#        # Satisfied she goes to sleep

    @skip('This test needs fixing')
    def test_successful_login_after_failed_does_not_include_old_password(self):
        """Test that email used for a failed log-in is not logged in the next successful log-in"""
        
        with self.assertLogs('',level='INFO') as captured_logs:
            # Edith tries to log in to Justletic but tpyes her pwd wrong
            self.login_helper('edith@mailinator.com', 'wrongpwd')

        print(f'<1> {captured_logs.records}')
        logged_message = captured_logs.records[0].msg 
        self.assertIn('"email": "edith@mailinator.com"', logged_message) 
        
        with self.assertLogs('',level='INFO') as captured_logs:
            # She then logs-in with the right password
            self.login_helper('edith@mailinator.com', 'epwd')
        
        # The new log messages don't contain any traces from the wrong attempt
        print(f'<2> {captured_logs.records}')
        logged_message = captured_logs.records[0].msg 
        self.assertNotIn('"email": "edith@mailinator.com"', logged_message) 
        self.assertNotIn('"password": "wrongpwd"', logged_message)

        #Satisfied she goes to sleep (and the admin too)

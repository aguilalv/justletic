"""Functional tests for adding services to Justletic"""
import time
import os

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException
from unittest import skip

from .base import FunctionalTest

class NewVisitorTest(FunctionalTest):

    """ Functional tests for adding services to Justletic """

    def setUp(self):
        """Revoke Justletic access to Strava before all tests"""
        super().setUp()
        os.environ['STRAVA_REDIRECT_URI'] = f'{self.live_server_url}/keys/stravatokenexchange'
        self.strava_revoke_access()

    def tearDown(self):
        """Revoke Justletic access to Strava after all tests"""
        self.strava_revoke_access()
        super().tearDown()

    def strava_login(self):
        """Logs in to strava"""
        self.browser.get('http://strava.com')
        try:
            login_button = self.wait_for(lambda:
                self.browser.find_element_by_link_text('Log In')
            )
            if login_button:
                login_button.click()
                email_in = self.wait_for(lambda:
                    self.browser.find_element_by_id('email')
                )
                password_in = self.wait_for(lambda:
                    self.browser.find_element_by_id('password')
                )
                email_in.send_keys('edith@mailinator.com')
                password_in.send_keys(os.environ['STRAVA_TEST_USER_PASSWORD'])
                password_in.send_keys(Keys.ENTER)
        except NoSuchElementException:
            pass

    def strava_logout(self):
        """Logs out from Strava"""
        logged_out = False
        self.browser.get('http://www.strava.com')
        try:
            menu_button = self.wait_for(lambda:
                self.browser.find_element_by_class_name('btn-mobile-menu')
            )
            if menu_button.is_displayed():
                menu_button.click()
                logout_link = self.wait_for(lambda: 
                    self.browser.find_element_by_link_text('Log Out')
                )
                logout_link.click()
                logged_out = True
        except NoSuchElementException:
            pass
        if not logged_out:
            try:
                menu = self.browser.find_element_by_class_name('user-menu')
                logout_link = self.browser.find_element_by_link_text('Log Out')
                actions = ActionChains(self.browser)
                actions.move_to_element(menu)
                actions.click(logout_link)
                actions.perform()
            except NoSuchElementException:
                pass
        
        login_button = self.wait_for(lambda:
            self.browser.find_element_by_link_text('Log In')
        )

    def strava_revoke_access(self):
        """Checks if Justletic is authorised in Strava for the test user
        and revokes access if it was authorised"""
        self.strava_login()
        self.browser.get('https://www.strava.com/settings/apps')
        if self.browser.current_url == 'https://www.strava.com/settings/apps':
            revoke_access_button = self.wait_for(lambda:
                self.browser.find_element_by_class_name('revoke-access')
            )
            revoke_access_button.click()
        self.strava_logout()

    def test_can_authorise_a_strava_account(self):
        """ Test that a user can authorise Justletic to access her Strava data"""
        # Edith has heard about a cool new online training app. She goes
        # to check out its homepge
        self.browser.get(self.live_server_url)

        # She notices the page title mention its name "Justletic"
        # and the header says "Ahieve your goals"
        self.wait_for(lambda: self.assertIn(
            'Justletic',
            self.browser.title
        ))
        header_text = self.browser.find_element_by_class_name('intro-heading').text
        self.assertIn('ACHIEVE YOUR GOALS', header_text)

        # She is invited to enter her email straight away
        inputbox = self.browser.find_element_by_id('id_email_in')
        self.assertEqual(
            inputbox.get_attribute('placeholder'),
            'Enter your email'
        )

        # She types "edith@mailinator.com"" into a text box
        inputbox.send_keys('edith@mailinator.com')

        # When she hits enter, she is redirected to a Strava page to authorise
        # accessing some of her data
        inputbox.send_keys(Keys.ENTER)
        self.wait_for(lambda: self.assertRegex(
            self.browser.current_url,
            '.+strava.+'
        ))

        # Edith enters her email and her Strava password and hits ENTER
        
        email_in = self.wait_for(lambda:
            self.browser.find_element_by_id('email')
        )
        password_in = self.browser.find_element_by_id('password')
        email_in.send_keys('edith@mailinator.com')
        password_in.send_keys(os.environ['STRAVA_TEST_USER_PASSWORD'])
        password_in.send_keys(Keys.ENTER)

        # She then accepts to authorise Justletic to access her Strava data
        time.sleep(3) # Wait_for will get any button in the page before refreshing
        buttons = self.wait_for(lambda:
            self.browser.find_elements_by_xpath("//button")
        )
        for element in buttons:
            if element.text == 'Authorize':
                authorize_button = element
        authorize_button.click()

        # She is redirected to a Justletic page that congratulates her
        self.wait_for(lambda: self.assertIn(
            'Justletic',
            self.browser.title
        ))
        self.assertEqual(
            self.browser.find_element_by_tag_name('h3').text,
            'CONGRATULATIONS'
        )

        # Edith sees that Justletic can now tell her how many Km she run in her
        # last session
        self.assertRegex(
            self.browser.find_element_by_tag_name('h4').text,
            '.+7.97 Km.+'
        )
        

        # Satisfied she goes to sleep

    @skip('Email input not processed - Skip until functionality added')
    def test_cannot_use_empty_email(self):
        """Test that a user cannot use an empty email to create an account"""
        # Edith goes to the homepage and accidentally tries to submit
        # an empty email. She hits Enter on the empty input box
        self.browser.get(self.live_server_url)
        inputbox = self.browser.find_element_by_id('id_email_in')
        inputbox.send_keys(Keys.ENTER)

        # The home page refreshes, and there is an error message saying
        # that email cannot be blank
        self.wait_for(lambda: self.assertEqual(
            self.browser.find_element_by_css_selector('.alert-danger').text,
            EMAIL_ERROR
        ))

        # She tries again with her email and it works
        inputbox = self.browser.find_element_by_id('id_email_in')
        inputbox.send_keys('edith@mailinator.com')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for(lambda: self.assertEqual(
            self.browser.find_element_by_tag_name('h3').text,
            'edith@mailinator.com'
        ))

        # Satisfied she goes to sleep

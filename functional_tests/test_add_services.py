"""Functional tests for adding services to Justletic"""
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from keys.views import EMAIL_ERROR

from .base import FunctionalTest

class NewVisitorTest(FunctionalTest):

    """ Functional tests for adding services to Justletic """

    def test_can_authorise_a_strava_account(self):
        """ Test that a user can authorise Justletic to access her Strava data"""
        # Edith has heard about a cool new online training app. She goes
        # to check out its homepge
        self.browser.get(self.live_server_url)

        # She notices the page title mention its name "Justletic"
        # and the header says "Ahieve your goals"
        self.assertIn('Justletic', self.browser.title)
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

        # When she hits enter, she sees her email and Strava key
        inputbox.send_keys(Keys.ENTER)
        self.wait_for(lambda: self.assertEqual(
            self.browser.find_element_by_tag_name('h3').text,
            'edith@mailinator.com'
        ))
        self.wait_for_row_in_keys_table('e1234')

        # When she hits enter, she is redirected to a Strava page to authorise
        # accessing some of her data

        # She accepts to authorise Justletic to access her Strava data

        # She is redirected to a Justletic page that congratulates her

        # Satisfied she goes to sleep

        # Satisfied she goes to sleep

    def test_multiple_users_show_different_key_lists_at_different_urls(self):
        """ Test that different users have separate services authorised"""
        # Edith has heard about a cool new online training app. She goes
        # Edith authenticates Justletic to access her Strava data
        self.browser.get(self.live_server_url)
        inputbox = self.browser.find_element_by_id('id_email_in')
        inputbox.send_keys('edith@mailinator.com')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for(lambda: self.assertEqual(
            self.browser.find_element_by_tag_name('h3').text,
            'edith@mailinator.com'
        ))
        self.wait_for_row_in_keys_table('e1234')

        # She notices that her summary page has a unique URL
        edith_summary_url = self.browser.current_url
        self.assertRegex(edith_summary_url, '/users/.+')

        # Now a new user, Francis, comes along to the site

        ## Use new browser session to make sure no information of previous
        ## user coming through cookies, etc
        self.browser.quit()
        self.browser = webdriver.Firefox()

        # Francis visits the home page. There is no sign of Edith´s keys
        self.browser.get(self.live_server_url)
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('edith@mailinator.com', page_text)
        self.assertNotIn('e1234', page_text)

        # Francis authenticates his own Strava account
        inputbox = self.browser.find_element_by_id('id_email_in')
        inputbox.send_keys('francis@mailinator.com')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for(lambda: self.assertEqual(
            self.browser.find_element_by_tag_name('h3').text,
            'francis@mailinator.com'
        ))
        self.wait_for_row_in_keys_table('f1234')

        # Francis gets his own unique URL
        francis_summary_url = self.browser.current_url
        self.assertRegex(francis_summary_url, '/users/.+')
        self.assertNotEqual(francis_summary_url, edith_summary_url)

        # Again, there is no trace of Edith´s keys
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('edith@mailinator.com', page_text)
        self.assertNotIn('e1234', page_text)

        # Satisfied, they both go back to sleep

    def test_can_authorise_multiple_services(self):
        """Test that a user can authorise several services"""
        # Edith authenticates Justletic to access her Strava data
        self.browser.get(self.live_server_url)
        inputbox = self.browser.find_element_by_id('id_email_in')
        inputbox.send_keys('edith@mailinator.com')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for(lambda: self.assertEqual(
            self.browser.find_element_by_tag_name('h3').text,
            'edith@mailinator.com'
        ))
        self.wait_for_row_in_keys_table('e1234')

        # She notices that her summary page has a unique url and a link to add another service
        edith_summary_url = self.browser.current_url
        self.assertRegex(edith_summary_url, '/users/.+')
        link = self.browser.find_element_by_id('id_link_add_service')

        # She clicks the link, she sees her email and the keys to her 2 services
        link.click()
        self.wait_for(lambda: self.assertEqual(
            self.browser.find_element_by_tag_name('h3').text,
            'edith@mailinator.com'
        ))
        self.wait_for_row_in_keys_table('e1234')
        self.wait_for_row_in_keys_table('d1234')

        # When she hits enter, she is redirected to a XXX page to authorise
        # accessing some of her data

        # She accepts to authorise Justletic to access her Strava data

        # She is redirected to a Justletic page that congratulates her

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

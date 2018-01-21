from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import WebDriverException
from django.test import LiveServerTestCase
import time

MAX_WAIT = 10

class NewVisitorTest(LiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    def wait_for_row_in_keys_table(self,target_row_text):
        start_time = time.time()
        while True:
            try:
                table = self.browser.find_element_by_id('id_keys_table')
                rows = table.find_elements_by_tag_name('tr')
                self.assertIn(target_row_text,[row.text for row in rows])
                return
            except(AssertionError, WebDriverException) as e:
                if time.time() - start_time > MAX_WAIT:
                    raise e
                time.sleep(0.5)

    def test_can_authorise_a_strava_account(self):
        # Edith has heard about a cool new online training app. She goes
        # to check out its homepge
        self.browser.get(self.live_server_url)

        # She notices the page title and header mention its name "Justletic"
        self.assertIn('Justletic', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('Justletic',header_text)

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
        self.wait_for_row_in_keys_table('edith@mailinator.com e1234')
        
        # When she hits enter, she is redirected to a Strava page to authorise
        # accessing some of her data

        # She accepts to authorise Justletic to access her Strava data

        # She is redirected to a Justletic page that congratulates her

        # Satisfied she goes to sleep

    def test_multiple_users_show_different_key_lists_at_different_urls(self):
        # Edith authenticates Justletic to access her Strava data
        self.browser.get(self.live_server_url)
        inputbox = self.browser.find_element_by_id('id_email_in')
        inputbox.send_keys('edith@mailinator.com')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_keys_table('edith@mailinator.com e1234')

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
        self.wait_for_row_in_keys_table('francis@mailinator.com f1234')

        # Francis gets his own unique URL
        francis_summary_url = self.browser.current_url
        self.assertRegex(francis_summary_url, '/users/.+')
        self.assertNotEqual(francis_summary_url, edith_summary_url)

        # Again, there is no trace of Edith´s keys
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('edith@mailinator.com', page_text)
        self.assertNotIn('e1234', page_text)

        # Satisfied, they both go back to sleep

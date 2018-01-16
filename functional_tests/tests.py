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

    def test_can_authorise_a_strava_accoun(self):
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

        # When she hits enter, she sees her email and strava key
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_keys_table('edith@mailinator.com')
        self.wait_for_row_in_keys_table('123456')
        self.fail('Finish the test!')


        # When she hits enter, she is redirected to a Strava page to authorise
        # accessing some of her data

        # She accepts to authorise Justletic to access her Strava data

        # She is redirected to a Justletic page that congratulates her

        # Satisfied she goes to sleep


from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import WebDriverException
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
import time

MAX_WAIT = 10

class NewVisitorTest(StaticLiveServerTestCase):

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
    
    def wait_for_page_element(self,element,target_text):
        start_time = time.time()
        while True:
            try:
                found_text = self.browser.find_element_by_tag_name(element).text
                self.assertEqual(target_text,found_text)
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
 #        header_text = self.browser.find_element_by_tag_name('h1').text
 #        self.assertIn('Justletic',header_text)
 
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
        self.wait_for_page_element('h3', 'edith@mailinator.com')
        self.wait_for_row_in_keys_table('e1234')
         
        # When she hits enter, she is redirected to a Strava page to authorise
        # accessing some of her data
 
        # She accepts to authorise Justletic to access her Strava data

        # She is redirected to a Justletic page that congratulates her
 
        # Satisfied she goes to sleep

    def test_can_authorise_multiple_services(self):
        # Edith authenticates Justletic to access her Strava data
        self.browser.get(self.live_server_url)
        inputbox = self.browser.find_element_by_id('id_email_in')
        inputbox.send_keys('edith@mailinator.com')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_page_element('h3', 'edith@mailinator.com')
        self.wait_for_row_in_keys_table('e1234')

        # She notices that her summary page has a unique url and a link to add another service
        edith_summary_url = self.browser.current_url
        self.assertRegex(edith_summary_url, '/users/.+')
        link = self.browser.find_element_by_id('id_link_add_service')

        # She clicks the link, she sees her email and the keys to her 2 services
        link.click()
        self.wait_for_page_element('h3', 'edith@mailinator.com')
        self.wait_for_row_in_keys_table('e1234')
        self.wait_for_row_in_keys_table('d1234')

        # When she hits enter, she is redirected to a XXX page to authorise
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
        self.wait_for_page_element('h3', 'edith@mailinator.com')
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
        self.wait_for_page_element('h3', 'francis@mailinator.com')
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

    def test_layout_and_styling(self):
        # Edith goes to the home page
        self.browser.get(self.live_server_url)
        self.browser.set_window_size(1024,768)

        # She notices the input box is nicely centered
        inputbox = self.browser.find_element_by_id('id_email_in')
#        self.assertAlmostEqual(
#            inputbox.location['x'] + inputbox.size['width'] / 2,
#            512,
#            delta = 10
#        )

        # She authorises her first service and sees her email address
        # is nicely centered in her user summary page too

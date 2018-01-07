from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import unittest

class NewVisitorTest(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    def test_can_authorise_a_strava_accoun(self):
        # Edith has heard about a cool new online training app. She goes
        # to check out its homepge
        self.browser.get('http://localhost:8000')

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

        # When she hits enter, she is redirected to a Strava page to authorise
        # accessing some of her data
        inputbox.send_keys(Keys.ENTER)
        self.fail('Finish the test!')

        # She accepts to authorise Justletic to access her Strava data

        # She is redirected to a Justletic page that congratulates here

        # Satisfied she goes to sleep

if __name__ == '__main__':
    unittest.main(warnings='ignore')


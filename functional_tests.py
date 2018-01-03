from selenium import webdriver
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
        self.fail('Finish the test!')

        # She is invited to enter her user name straight away

        # She types "edith" into a text box

        # When she hits enter, she is redirected to a Strava page to authorise
        # accessing some of her data

        # She accepts to authorise Justletic to access her Strava data

        # She is redirected to a Justletic page that congratulates here

        # Satisfied she goes to sleep

if __name__ == '__main__':
    unittest.main(warnings='ignore')


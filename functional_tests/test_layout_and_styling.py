from .base import FunctionalTest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

class LayoutAndStylingTest(FunctionalTest):

    def test_layout_and_styling(self):
        # Edith goes to the home page
        self.browser.get(self.live_server_url)
        self.browser.set_window_size(1024,768)

        # She notices the input box is nicely centered
        inputbox = self.browser.find_element_by_id('id_email_in')
        header = self.browser.find_element_by_class_name('intro-heading')
        #print(header.location['x'])
        #print('--')
        #print(header.size['width'])
        self.assertAlmostEqual(
            (header.location['x'] + (header.size['width'] / 2)),
            512,
            delta = 10
        )

        # She authorises her first service and sees her email address
        # is nicely centered in her user summary page too

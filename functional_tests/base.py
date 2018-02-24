from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import WebDriverException
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
import time

MAX_WAIT = 10

class FunctionalTest(StaticLiveServerTestCase):

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

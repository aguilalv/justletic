from selenium.webdriver.common.keys import Keys

from .base import FunctionalTest

class LoginTest(FunctionalTest):
    
#    def test_can_create_new_user(self):
#        pass
    
    
    def test_existing_user_can_login_with_correct_password(self):
        # Edith goes to the justletic page
        # she notices a "Log in" button in the navbar for the first time
        # when she clicks the log in button a modal appears
        self.browser.get(self.live_server_url)
        login_link = self.browser.find_element_by_id('id_login_button')
        login_link.click()
        print(f'--> {self.browser.title}')
        self.fail('Implement the test, PLEASE')
        
        # It's telling her to enter her email address and password, 
        # so she does and hits ENTER


        # She sees her user summary page
        # And the navbar menu indicates she is now logged in


#    def test_existing_user_cannot_login_with_incorrect_password(self):
#        pass

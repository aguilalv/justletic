from selenium.webdriver.common.keys import Keys
import time

@when(u'I visit "{url}"')
def visit(context,url):
    context.browser.get(context.get_url(url))

@then(u'I will see the title "{expected_title}"')
def see_title(context,expected_title):
    title = context.browser.title
    context.test.assertEqual(title,expected_title)

@then(u'I will see "{expected_in_header}" in the header')
def see_in_header(context,expected_in_header):
    header = context.browser.find_element_by_tag_name('h1').text
    context.test.assertIn(header,expected_in_header)
        
#### THIS TESTS ONLY CHECKS FOR A TEXT_BOX WITH A SPECIFIC ID !!!!        
@then(u'I am invited to type in a text box that says "{expected_placeholder}"')
def invited_to_type(context,expected_placeholder):
    inputbox = context.browser.find_element_by_id('id_email_in')
    placeholder = inputbox.get_attribute('placeholder')
    context.test.assertEqual(placeholder,expected_placeholder)

#### THIS TESTS ONLY CHECKS FOR A TEXT_BOX WITH A SPECIFIC ID !!!!        
@when(u'I type "{email_in}" into a text box and press enter')
def type_in_text_box(context,email_in):
    inputbox = context.browser.find_element_by_id('id_email_in')
    inputbox.send_keys(email_in)
    inputbox.send_keys(Keys.ENTER)
    time.sleep(1)


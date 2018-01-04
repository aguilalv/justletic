@when(u'I visit "{url}"')
def visit(context,url):
    context.browser.get(context.get_url(url))

@then(u'I will see the title "{expected_title}"')
def see_title(context,expected_title):
    title = context.browser.title
    context.test.assertEqual(title,expected_title)


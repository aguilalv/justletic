"""
Functional tests for Justletic basic layout and styling
- Minimmum test to check css file loaded properly-
"""
from .base import FunctionalTest

class LayoutAndStylingTest(FunctionalTest):

    """Functional tests for Justletic layout and styling"""

    def test_layout_and_styling(self):
        """Test that header in centered in home page"""
        # Edith goes to the home page
        self.browser.get(self.live_server_url)
        self.browser.set_window_size(1024, 768)

        # She notices the input box is nicely centered
        header = self.browser.find_element_by_class_name('intro-heading')
        self.assertAlmostEqual(
            (header.location['x'] + (header.size['width'] / 2)),
            512,
            delta=10
        )

        # She authorises her first service and sees her email address
        # is nicely centered in her user summary page too

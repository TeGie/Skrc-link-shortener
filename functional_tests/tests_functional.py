import time

from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.common.exceptions import WebDriverException


class FullSiteNavigationTest(LiveServerTestCase):

    def setUp(self):
        # self.browser = webdriver.Firefox()
        self.browser = webdriver.Chrome()

    def tearDown(self):
        self.browser.quit()

    def restart_browser(self):
        self.browser.quit()
        self.browser = webdriver.Firefox()
        # self.browser = webdriver.Chrome()

    @staticmethod
    def wait_for(func, max_wait=10):
        start_time = time.time()
        while True:
            try:
                return func()
            except (AssertionError, WebDriverException) as e:
                if time.time() - start_time > max_wait:
                    raise e
                time.sleep(0.5)

    def find_input_url_and_button(self):
        input_url = self.browser.find_element_by_id('id_url')
        button_submit = self.browser.find_element_by_tag_name('button')
        return input_url, button_submit

    def input_text_and_click_button(self, str_):
        input_url, button_submit = self.find_input_url_and_button()
        input_url.clear()
        input_url.send_keys(str_)
        button_submit.click()

    def test_full_site_navigation(self):
        # She goes to the home page
        self.browser.get(self.live_server_url)

        self.assertEqual('SkrcURL | Home', self.browser.title)

        # She sees input field invites her to type the URL, and the button below
        input_url, button_submit = self.find_input_url_and_button()

        self.assertEqual('URL', input_url.get_attribute('placeholder'))
        self.assertTrue(button_submit.is_displayed())

        # "CSRF token is there but she cannot sees it without checking page source
        csfr = self.browser.find_element_by_xpath("//form/div/input[1]")

        self.assertFalse(csfr.is_displayed())

        # She types url with typo for fun and an error message appears
        self.input_text_and_click_button('http:/www.selenium.org')

        self.wait_for(lambda: self.assertEqual(
            'Enter a valid URL.',
            self.browser.find_elements_by_tag_name('span')[1].text
        ))

        # She pastes favorite link in the input field, clicks the button, and sees
        # message "Done", text of the link she typed, the shortened link, and button "Back"
        self.input_text_and_click_button('http://www.seleniumhq.org/')

        self.wait_for(lambda: self.assertEqual(
            'Done',
            self.browser.find_element_by_id('head-2').text
        ))
        self.wait_for(lambda: self.assertEqual(
            'http://www.seleniumhq.org/',
            self.browser.find_element_by_id('lnk-long-txt').text
        ))
        self.wait_for(lambda: self.assertRegex(
            self.browser.find_element_by_id('lnk-short').text,
            f'{self.live_server_url}/' + '[a-zA-Z0-9]{6}$'
        ))
        self.wait_for(lambda: self.assertRegex(
            self.browser.find_element_by_id('lnk-short').get_attribute('href'),
            f'{self.live_server_url}/' + '[a-zA-Z0-9]{6}/$'
        ))
        self.wait_for(lambda: self.assertEqual(
            'Back',
            self.browser.find_element_by_id('btn-back').text
        ))

        # She clicks the button "Back" and returns to the home page
        self.browser.find_element_by_id('btn-back').click()

        self.wait_for(lambda: self.assertEqual(
            'SkrcURL | Home',
            self.browser.title
        ))

        # She decides to close the browser and reopens the home page maybe in another browser
        self.restart_browser()
        self.browser.get(self.live_server_url)

        # She pastes the same link again, clicks the button, and sees that message has change to "Found"
        self.wait_for(lambda: self.assertIsNotNone(
            self.browser.find_elements_by_id('id_url')
        ))
        self.input_text_and_click_button('http://www.seleniumhq.org/')
        self.wait_for(lambda: self.assertEqual(
            'Found',
            self.browser.find_element_by_id('head-2').text
        ))

        # She clicks the shortened link and browses the site she wanted
        self.browser.find_element_by_id('lnk-short').click()

        self.wait_for(lambda: self.assertIn(
            'Selenium',
            self.browser.title
        ))

        # She backs to the home page, once again pastes the same link, clicks the button,
        # and sees that visits count changes to 1
        self.browser.get(self.live_server_url)
        self.input_text_and_click_button('http://www.seleniumhq.org/')

        self.wait_for(lambda: self.assertEqual(
            'Visits: 1',
            self.browser.find_element_by_id('counter').text
        ))
        # She decides stop playing with that silly site
        self.fail("""More tests!""")

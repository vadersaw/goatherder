import sys

# from django.test import LiveServerTestCase
from django.contrib.staticfiles.testing import StaticLiveServerTestCase

from selenium import webdriver
from selenium.webdriver.common.keys import Keys


class NewVisitorTest(StaticLiveServerTestCase):
    
    @classmethod
    def setUpClass(cls):
        for arg in sys.argv:
            if 'liveserver' in arg:
                cls.server_url = 'http://' + arg.split('=')[1]
                return
        super().setUpClass()
        cls.server_url = cls.live_server_url
        
    @classmethod
    def tearDownClass(cls):
        if cls.server_url == cls.live_server_url:
            super().tearDownClass()
    
    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)
        self.table_id = 'id_list_table'
        self.balls_item1 = 'Buy some BBQ sauce'
        self.balls_item2 = 'Use BBQ to fill a bathtub'
        
    def tearDown(self):
        self.browser.quit()
        
    def check_for_row_in_list_table(self, row_text):
        table = self.browser.find_element_by_id(self.table_id)
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn(row_text, [row.text for row in rows])
        
    def test_can_start_a_list_and_retrieve_it_later(self):
        # Sweet balls wants to check out your awesome new site and goes to your webpage
        self.browser.get(self.server_url)

        # Balls notices the page title and header mention to-do lists, the point of this particular page
        self.assertIn('To-Do', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('To-Do', header_text)
        
        # Balls is invited to enter a to-do item immediately
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertEqual(
                inputbox.get_attribute('placeholder'),
                'Enter a to-do item'
        )
        
        # He types "Buy some BBQ sauce" into a text box
        inputbox.send_keys(self.balls_item1)

        # When he hits enter, he is taken to a new URL, and the now the page lists "1: Buy some BBQ sauce" as an item on the todo list
        inputbox.send_keys(Keys.ENTER)
        balls_list_url = self.browser.current_url
        self.assertRegex(balls_list_url, '/lists/.+')
        self.check_for_row_in_list_table('1: {0}'.format(self.balls_item1))

        # There should still be a box inviting Balls to add more items. He enters, "Use BBQ to fill a bathtub"
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys(self.balls_item2)
        inputbox.send_keys(Keys.ENTER)
        
        # The page updates again, and now has both items listed
        self.check_for_row_in_list_table('1: {0}'.format(self.balls_item1))
        self.check_for_row_in_list_table('2: {0}'.format(self.balls_item2))
        
        # A new user, Deep, comes to the site.
        
        ## We use a new browser session to make sure that no information from the previous session persists
        self.browser.quit()
        self.browser = webdriver.Firefox()
        
        # Deep visits the page and there is no sign of Balls list
        self.browser.get(self.server_url)
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn(self.balls_item1, page_text)
        self.assertNotIn(self.balls_item2, page_text)
        
        # Deep starts a new list by entering the first item. He could give a phuk. 
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Buy tigerblood')
        inputbox.send_keys(Keys.ENTER)
        
        # Deep gets his own unique URL
        deep_list_url = self.browser.current_url
        self.assertRegex(deep_list_url, '/lists/.+')
        self.assertNotEqual(balls_list_url, deep_list_url)
        
        # Again, lets verify there is no trace of balls list items
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn(self.balls_item1, page_text)
        self.assertIn('Buy tigerblood', page_text)

        # Satisfied, they both head off to read Reddit
        # self.fail('Finish the test!')
        
    def test_layout_and_styling(self):
        # Deep goes the home page
        self.browser.get(self.server_url)
        self.browser.set_window_size(1024, 768)
        
        # Deep notices the input box is nicely centered
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertAlmostEqual(
            inputbox.location['x'] + inputbox.size['width'] / 2, 
            512, 
            delta=5
        )
        
        inputbox.send_keys('testing\n')
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertAlmostEqual(
            inputbox.location['x'] + inputbox.size['width'] / 2, 
            512, 
            delta=5
        )
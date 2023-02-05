from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import WebDriverException
import time
MAX_WAIT = 10

class NewVisitorTest(StaticLiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()
    
    def tearDown(self):
        self.browser.quit()

    def test_layout_and_styling(self):

        self.browser.get(self.live_server_url)
        self.browser.set_window_size(1024, 768)

        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertAlmostEqual(
            inputbox.location['x'] + inputbox.size['width'] / 2, 
            512,
            delta=10
        )

        inputbox.send_keys('testing')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: testing')
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertAlmostEqual(
            inputbox.location['x'] + inputbox.size['width'] / 2, 
            512,
            delta=10
        )


    def wait_for_row_in_list_table(self, row_text):
        start_time = time.time()
        while True:
            try:  
                table = self.browser.find_element_by_id('id_list_table')
                rows = table.find_elements_by_tag_name('tr')
                self.assertIn(row_text, [row.text for row in rows])
                return
            except (AssertionError, WebDriverException) as e:
                if time.time() - start_time > MAX_WAIT:
                    raise e
                time.sleep(0.5)

    def test_can_start_a_list_and_retrieve_it_later(self):
        #new online to-do app, visit the homepage
        self.browser.get(self.live_server_url)

        self.assertIn('To-Do', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('To-Do', header_text)

        #adding a "buy groceries"-item to the list
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertEqual(
            inputbox.get_attribute('placeholder'),
            'Enter a to-do item'
        )

        #adding another item named "buy new shoes"
        inputbox.send_keys('buy new shoes')

        #page updates and shows the item
        # in list format as '1: buy new shows'
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: buy new shoes')

        #the input mask is still there waiting for another item
        #input is 'buy new shoe laces'
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('buy new shoe laces')
        inputbox.send_keys(Keys.ENTER)

        #page updates again and shows both items
        self.wait_for_row_in_list_table('1: buy new shoes')
        self.wait_for_row_in_list_table('2: buy new shoe laces')

    def test_mulitple_users_can_start_lists_at_different_urls(self):

        #Edith starts a new to-do list
        self.browser.get(self.live_server_url)
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('buy new shoes')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: buy new shoes')

        #returns a unique url with the list for each user
        edith_list_url = self.browser.current_url
        self.assertRegex(edith_list_url, '/lists/.+')

        #not a new user, Francis visits the site

        ## We use a new browser session to make sure that no information
        ## of Edith's is incoming from cookies etc
        self.browser.quit()
        self.browser = webdriver.Firefox()

        #Francis visits the homepage. There is no sign of Edith's list
        self.browser.get(self.live_server_url)
        page_text = self.browser.find_elements_by_id('id_new_item')
        self.assertNotIn('buy new shoes', page_text)
        self.assertNotIn('buy new shoe laces', page_text)

        #Francis starts a new list by entering a new item
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('buy milk')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: buy milk')

        #Francis gets his own unique URL
        francis_list_url = self.browser.current_url
        self.assertRegex(francis_list_url, '/lists/.+')
        self.assertNotEqual(francis_list_url, edith_list_url)

        #no trace of Edith's list
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('buy new shoes', page_text)
        self.assertIn('buy milk', page_text)
        
        #visiting that url shows the same items that were saved 

        #closing the window


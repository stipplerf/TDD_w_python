from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

class NewVisitorTest(LiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()
    
    def tearDown(self):
        self.browser.quit()

    def check_for_row_in_list_table(self, row_text):
        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn(row_text, [row.text for row in rows])
    
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
        time.sleep(1)
        self.check_for_row_in_list_table('1: buy new shoes')

        #the input mask is still there waiting for another item
        #input is 'buy new shoe laces'
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('buy new shoe laces')
        inputbox.send_keys(Keys.ENTER)
        time.sleep(1)

        #page updates again and shows both items
        self.check_for_row_in_list_table('1: buy new shoes')
        self.check_for_row_in_list_table('2: buy new shoe laces')

        #returns a unique url with the list for each user
        self.fail('Finish the test!')
        #visiting that url shows the same items that were saved 

        #closing the window


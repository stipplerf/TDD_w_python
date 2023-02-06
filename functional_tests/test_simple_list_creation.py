from .base import FunctionalTest
from selenium.webdriver.common.keys import Keys
from selenium import webdriver

class NewVisitorTest(FunctionalTest):

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
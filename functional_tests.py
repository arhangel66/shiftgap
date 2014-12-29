import unittest
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC


class NewVisitorTest(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)

    def tearDown(self):
        self.browser.quit()

    def test_can_enter_a_shift_and_retrieve_it_later(self):
        # Kelsey the manager needs to make a staff schedule online for all the employees to see
        # she navigates to the home page
        self.browser.get('http://localhost:5000')

        # She sees the web app is called 'ShiftGap'
        self.assertIn('ShiftGap', self.browser.title)

        # She clicks on Shifts to go to the main Shifts page
        self.browser.get('http://localhost:5000/shifts')
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('Upcoming Shifts', header_text)

        # She decides to add a shift by clicking the add shift button
        self.browser.find_element_by_xpath('/html/body/div[2]/button').click()
        # element = WebDriverWait(self.browser, 10).until(
        #     self.browser.find_element_by_id('addShiftModal').getCssValue('opacity').equals('1')
        # )
        import time
        time.sleep(2)  # fucking annoying
        # self.browser.implicitly_wait(10)
        modal_header = self.browser.find_element_by_tag_name('h4').text
        self.assertIn('Add a New Shift', modal_header)

        # There is a form that allows her to enter a new shift

        # She enters the start time, end time and date of the shift along with an employee name

        # She can see the list of shifts that she has created

        # After she's done entering shifts for the week, she goes to drink a bottle of champagne

        self.fail('Finish the test')

if __name__ == '__main__':
    unittest.main(warnings='ignore')
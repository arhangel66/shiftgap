import unittest
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC


class NewVisitorTest(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)
        self.base_url = 'http://localhost:5000'

    def tearDown(self):
        self.browser.quit()

    def test_can_enter_a_shift_and_retrieve_it_later(self):
        # Kelsey the manager needs to make a staff schedule online for all the employees to see
        # she navigates to the home page
        self.browser.get(self.base_url)

        # She sees the web app is called 'ShiftGap'
        self.assertIn('ShiftGap', self.browser.title)

        # She clicks on Shifts to go to the main Shifts page
        self.browser.get('http://localhost:5000/shifts')
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('Upcoming Shifts', header_text)

        # She decides to add a shift by clicking the add shift button
        # @TODO make button
        # element = WebDriverWait(self.browser, 10).until(
        #     self.browser.find_element_by_id('addShiftModal').getCssValue('opacity').equals('1')
        # )
        import time

        # There is a form that allows her to enter a new shift
        self.browser.get(self.base_url + "/shifts/create/")
        self.browser.find_element_by_id("id_start_time").click()

        #self.browser.find_element_by_xpath("//tr[5]/td[3]/div").click()
        #self.browser.find_element_by_xpath("//div[3]/div[2]/div/div/div[18]").click()
        self.browser.find_element_by_id("id_end_time").click()
        self.browser.find_element_by_xpath("//div[4]/div/div[2]/table/tbody/tr[5]/td[4]/div").click()
        self.browser.find_element_by_xpath("//div[4]/div[2]/div/div/div[21]").click()
        self.browser.find_element_by_id("id_employee").clear()
        self.browser.find_element_by_id("id_employee").send_keys("Mike")
        self.browser.find_element_by_css_selector("input.btn.btn-primary").click()


        # She enters the start time, end time and date of the shift along with an employee name

        # She can see the list of shifts that she has created

        # After she's done entering shifts for the week, she goes to drink a bottle of champagne

        self.fail('Finish the test')

if __name__ == '__main__':
    unittest.main(warnings='ignore')
import unittest
from selenium import webdriver


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
        self.fail('Finish the test')

if __name__ == '__main__':
    unittest.main(warnings='ignore')

# There is a form that allows her to enter a new shift

# She enters the start time, end time and date of the shift along with an employee name

# She can see the list of shifts that she has created

# After she's done entering shifts for the week, she goes to drink a bottle of champagne
# -*- codeing:utf-8 -*-
# __author__ = 'Buguin'
"""This is a test for base function of issue track system"""
import unittest
from selenium.webdriver.common.keys import Keys
from selenium import webdriver


class NewVisitorTest(unittest.TestCase):

    def setUp(self):
        self.brower = webdriver.Chrome()
        self.brower.implicitly_wait(3)

    def tearDown(self):
        self.brower.quit()

    def test_web_title(self):
        self.brower.get('http://localhost:8000')

        self.assertIn('To-Do', self.brower.title)
        header_text = self.brower.find_element_by_tag_name('h1').text
        self.assertIn('To-Do', header_text)

        inputbox = self.brower.find_element_by_id('id_new_item')
        self.assertEqual(inputbox.get_attribute('placeholder'), 'Enter a to-do item')

        inputbox.send_keys('Bug peacock feathers')

        inputbox.send_keys(Keys.ENTER)
        table = self.brower.find_elements_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertTrue(any(row.text == '1:Bug peacock feathers' for row in rows))

        self.fail('Finish the test')
if __name__ == '__main__':
    unittest.main(warnings='ignore')

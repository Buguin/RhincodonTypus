# -*- codeing:utf-8 -*-
# __author__ = 'Buguin'
"""This is a test for base function of issue track system"""
import unittest
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
        self.fail('Finish the test!')

if __name__ == '__main__':
    unittest.main(warnings='ignore')

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@created: 02.04.19
@author: felix
"""
import unittest
from bs4 import BeautifulSoup
from selenium.webdriver.common.keys import Keys
from selenium_base import SeleniumBase

# 'get_attribute', 'get_property', 'id', 'is_displayed', 'is_enabled', 'is_selected', 'location',
# 'location_once_scrolled_into_view', 'parent', 'rect', 'screenshot', 'screenshot_as_base64',
# 'screenshot_as_png', 'send_keys', 'size', 'submit', 'tag_name', 'text', 'value_of_css_property'


class Sandbox(SeleniumBase):

    def test_get_buttons(self):
        selenium = self.login(self.selenium)
        selenium.get(self.base_url + '/l/errors/')
        page_source = selenium.page_source
        # soup = BeautifulSoup(page_source, features="html.parser")
        # # for link in soup.find_all('a'):
        # #     print(link.get('href'))
        # print(soup.body)
        # selenium.save_screenshot(self.get_picture_name('marketing', 'detail_overview'))
        h1 = selenium.find_elements_by_tag_name('h1')
        for h in h1:
            print(h.text)
        links = selenium.find_elements_by_xpath('.//a')
        for link in links:
            print(link.text, link.get_attribute('href'))
        buttons = selenium.find_elements_by_tag_name('button')
        for btn in buttons:
            if btn.text != '':
                print(btn.text)
                print(btn.is_enabled())
        list_elems = selenium.find_elements_by_xpath('.//li')
        for list_elem in list_elems:
            print(list_elem.text, list_elem.is_displayed())
            print(list_elem.tag_name)
        images = selenium.find_elements_by_tag_name('img')
        for image in images:
            if self.base_url in image.get_attribute('src'):
                print(image.get_attribute('src'), image.is_displayed())
            # if image.is_displayed() and self.base_url in image.get_attribute('src'):
            #     print(image.get_attribute('src'))
        table_data = selenium.find_elements_by_tag_name('td')
        for table_d in table_data:
            print(table_d.text)


if __name__ == '__main__':
    unittest.main()

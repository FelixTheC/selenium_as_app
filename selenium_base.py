#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: felix
"""

import unittest
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class SeleniumBase(unittest.TestCase):

    testuser = 'testuser'
    testpasswd = 'testpasswd'
    testinst = 'inst'
    testhost = 'localhost:8000/accounts/login/DE/de/'
    base_url = 'localhost:8000'

    @classmethod
    def setUpClass(cls):
        date_hour = str(datetime.today().hour)
        date = str(datetime.today().date())
        logfile = '--log-path=' + date + '_' + date_hour + 'chromedriver.log'
        options = webdriver.ChromeOptions()
        options.add_argument('--start-maximized')
        options.add_argument('--ignore-certificate-errors')
        options.add_argument('--test-type')
        cls.selenium = webdriver.Chrome(options=options,
                                        service_args=['--verbose', logfile])
        cls.wait = WebDriverWait(cls.selenium, 10)
        super(SeleniumBase, cls).setUpClass()

    def setUp(self):
        super(SeleniumBase, self).setUp()

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super(SeleniumBase, cls).tearDownClass()

    def login(self, selenium):
        selenium.get(self.testhost)
        try:
            inst = selenium.find_element_by_id('customerid')
            #institution here
            inst.send_keys(self.testinst)
            inst.send_keys(Keys.RETURN)
        except:
            pass
        selenium.implicitly_wait(10)
        user = selenium.find_element_by_id('user')
        passwd = selenium.find_element_by_id('password')
        btn = selenium.find_element_by_id('singlebutton')
        #username goes here
        user.send_keys(self.testuser)
        #password here
        passwd.send_keys(self.testpasswd)
        btn.send_keys(Keys.RETURN)
        selenium.implicitly_wait(10)
        return selenium

    def change_language(self, selenium, language):
        """
        :param selenium: selenium instance
        :param language: can be 'en', 'de', 'cz'
        :return: selenium instance
        """
        # select language
        selenium.find_element_by_class_name('selection').click()
        selenium.find_element_by_xpath(f"//div[@class='options']//a[@data-value='{language}']").click()
        return selenium

    def fill_form(self, selenium, submit_btn_id, **kwargs):
        """
        :param selenium: selenium instance
        :param kwargs: should include the fields and the value
        :return: selenium instance
        """
        for key, val in kwargs.items():
            selenium.find_element_by_name(key).clear().send_keys(val)
        selenium.find_element_by_id(submit_btn_id)
        return selenium

    def click_nodes(self, selenium, click1=True, subnodes=('li2', ), take_picture=False,
                    picture_app=None, picture_name=None):
        """
        :param selenium: selenium instance
        :param click1: class exists in page
        :param subnodes: subnodes
        :param take_picture: should screenshots make
        :param picture_app: name of the app for creating path
        :param picture_name: name of the picture for creating path
        :return: selenium instance
        """
        if click1:
            nodes = selenium.find_elements_by_class_name('click1')
            counter = 0
            for node in nodes:
                node.click()
                selenium.implicitly_wait(10)
                if take_picture and picture_app is not None and picture_name is not None:
                    picture_path = self.get_picture_name(picture_app, picture_name + str(counter))
                    selenium.save_screenshot(picture_path)
                    counter += 1

        for subnode in subnodes:
            snodes = selenium.find_elements_by_class_name(subnode)
            counter
            for snode in snodes:
                snode.click()
                wait = WebDriverWait(timeout=30, driver=selenium)
                wait.until(EC.element_to_be_clickable((By.PARTIAL_LINK_TEXT, 'Details')))
                if take_picture and picture_app is not None and picture_name is not None:
                    picture_path = self.get_picture_name(picture_app, 'subnode_' + picture_name + str(counter))
                    selenium.save_screenshot(picture_path)
                    counter += 1
        return selenium

    def get_amount_node_elem(self, selenium, node_class='click1', slice=None):
        """
        :param selenium: selenium instance
        :param node_class: the class of the app
        :return: length of elements selenium has found
        """
        nodes = selenium.find_elements_by_class_name(node_class)
        if slice is None:
            return len(nodes)
        else:
            return len(nodes[:slice])

    def click_detail_from_node_elem(self, selenium, node_class='li2', node=0):
        """
        :param selenium: selenium instance
        :param node_class: the class of the node
        :param node: element number
        :return: selenium instance
        """
        nodes = selenium.find_elements_by_class_name(node_class)
        nodes[node].click()
        wait = WebDriverWait(timeout=10, driver=selenium)
        element = wait.until(EC.element_to_be_clickable((By.PARTIAL_LINK_TEXT, 'Detail')))
        element.click()
        return selenium

    def click_plot_tabs(self, selenium):
        """
        :param selenium: selenium instance
        :return: selenium instance
        """
        tabs = selenium.find_elements_by_xpath("//div[@class='bk-root']//div[@class='bk-widget']//ul[@class='bk-bs-nav-tabs']//li")
        selenium.implicity_wait(10)
        for tab in tabs:
            tab.click()
        selenium.implicity_wait(0)
        return selenium

    def get_picture_name(self, app, name):
        date_hour = str(datetime.today().hour)
        date = str(datetime.today().date())
        return app + '/log_pics/' + date + '_' + date_hour + '_' + name + '.png'

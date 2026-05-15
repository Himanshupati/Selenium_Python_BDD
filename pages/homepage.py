from typing import Literal
from selenium.webdriver.common.by import By
from pages.BasePage import *
from selenium import webdriver
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.utils import keys_to_typing

class Homepage:
    locators = {
        'XPATH' : {
            'search' : "//input[@id='search']",
            'search2' : "//input[@id='search2']",
            'searchg' : '//textarea[@aria-label="Search"]',
            'search_by_voice' : '//div[@aria-label="Search by voice"]'
        },
        'ID' : {
            'username' : "UserName"
        },
        'CLASS_NAME' : {
            'contact' : "contactus contactus_class"
        },
        'CSS_SELECTOR' : {
            'service' : "#id"
        },
        'NAME' : { },
        'LINK_TEXT': { },
        'PARTIAL_LINK_TEXT' : { },
        'TAG_NAME' : { }
    }

    def __init__(self, driver: WebDriver):  # fixed constructor
        self.driver = driver

    def get_element(self, element_name: Literal['search', 'search2', 'searchg', 'search_by_voice']):
        by_type, locator_value = get_locator_type_and_value(element_name, self.locators)
        print(f"HomePage: Using locator type: '{by_type}' and locator value '{locator_value}' for element: {element_name}")
        return self.driver.find_element(by_type, locator_value)

    def get_elements(self, element_name):
        by_type, locator_value = get_locator_type_and_value(element_name, self.locators)
        print(f"HomePage: Using locator type: '{by_type}' and locator value '{locator_value}' for element: {element_name}")
        return self.driver.find_elements(by_type, locator_value)

    def get_homepage_element_locator_type_and_value(self, element_name: Literal['search', 'search2', 'searchg', 'search_by_voice']):
        ''' Important instruction to use this method: Always add element key from the locator dictionary in the element_name paramter list '''
        by_type, locator_value = get_locator_type_and_value(element_name, self.locators)
        return by_type, locator_value

    def get_homepage_element_locator(self, element_name: Literal['search', 'search2', 'searchg', 'search_by_voice']):
        ''' Important instruction to use this method: Always add element key from the locator dictionary in the element_name paramter list '''
        by_type, locator_value = get_locator_type_and_value(element_name, self.locators)
        return (by_type, locator_value)  # fixed tuple


# <test>
def open_url(browser):
    browser.get('https://www.google.com/')

def test_homepage_step(browser: WebDriver):
    import time
    open_url(browser)
    time.sleep(5)

    homeapge = Homepage(browser)
    search = homeapge.get_element('searchg')

    wait_for_presence(browser, homeapge.get_homepage_element_locator_type_and_value('searchg'))
    highlight_element(browser, homeapge.get_homepage_element_locator_type_and_value('searchg'))
    time.sleep(2)
    unhighlight_element(browser, homeapge.get_homepage_element_locator_type_and_value('searchg'))
    time.sleep(4)

    search.send_keys('abcdefgh')
    time.sleep(3)

    # driver.quit()
    print(homeapge.get_homepage_element_locator_type_and_value('searchg'))

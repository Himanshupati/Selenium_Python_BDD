from typing import Literal
from selenium.webdriver.common.by import By
from pages.BasePage import *
from selenium import webdriver
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.utils import keys_to_typing

class Loginpage:
    locators = {
        'XPATH' : {
            'signin_icon': "//div[@class='nav-items']//a[@href='/account']",
            'email': "//input[@id='user-name']",
            'password': "//input[@id='password']",
            'login_button': "//input[@id='login-button']",
        },
        'ID' : { },
        'CLASS_NAME' : {
            'contact' : "contactus"
        },
        'CSS_SELECTOR' : {
            'service' : "#id"
        },
        'NAME' : { },
        'LINK_TEXT': { },
        'PARTIAL_LINK_TEXT' : { },
        'TAG_NAME' : { }
    }

    def __init__(self, driver: WebDriver):
        self.driver = driver

    def get_element(self, element_name: Literal['search', 'search2', 'searchg', 'search_by_voice']):
        by_type, locator_value = get_locator_type_and_value(element_name, self.locators)
        print(f"HomePage: Using locator type: '{by_type}' and locator value '{locator_value}' for element: {element_name}")
        return self.driver.find_element(by_type, locator_value)

    def get_elements(self, element_name):
        by_type, locator_value = get_locator_type_and_value(element_name, self.locators)
        print(f"HomePage: Using locator type: '{by_type}' and locator value '{locator_value}' for element: {element_name}")
        return self.driver.find_elements(by_type, locator_value)

    def get_loginpage_element_locator_type_and_value(self, element_name: Literal['search', 'search2', 'searchg', 'search_by_voice']):
        ''' Important instruction to use this method: Always add element key from the locator dictionary in the element_name paramter list '''
        by_type, locator_value = get_locator_type_and_value(element_name, self.locators)
        return by_type, locator_value

    def get_loginpage_element_locator(self, element_name: Literal['search', 'search2', 'searchg', 'search_by_voice']):
        ''' Important instruction to use this method: Always add element key from the locator dictionary in the element_name paramter list '''
        by_type, locator_value = get_locator_type_and_value(element_name, self.locators)
        return tuple(by_type, locator_value)


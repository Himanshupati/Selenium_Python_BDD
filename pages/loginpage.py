from typing import Literal
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from pages.BasePage import get_locator_type_and_value


class Loginpage:
    locators = {
        'XPATH': {
            'signin_icon': "//div[@class='nav-items']//a[@href='/account']",
            'email': "//input[@id='user-name']",
            'password': "//input[@id='password']",
            'login_button': "//input[@id='login-button']",
            'Sign_in_button': "//input[@id='login-button']",
        },
        'CLASS_NAME': {
            'contact': "contactus"
        },
        'CSS_SELECTOR': {
            'service': "#id"
        },
        'ID': {

        },
        'NAME': {

        },
        'LINK_TEXT': {

        },
        'PARTIAL_LINK_TEXT': {

        },
        'TAG_NAME': {

        }
    }

    def __init__(self, driver: WebDriver):
        self.driver = driver

    def get_element(self, element_name: str):
        by_type, locator_value = get_locator_type_and_value(element_name, self.locators)
        print(f"[Loginpage] Using locator type: '{by_type}' and value: '{locator_value}' for element: {element_name}")
        return self.driver.find_element(by_type, locator_value)

    def get_elements(self, element_name: str):
        by_type, locator_value = get_locator_type_and_value(element_name, self.locators)
        print(f"[Loginpage] Using locator type: '{by_type}' and value: '{locator_value}' for element: {element_name}")
        return self.driver.find_elements(by_type, locator_value)

    def get_loginpage_element_locator_type_and_value(self, element_name: str):
        """Return (By, locator) tuple for use in explicit waits"""
        return get_locator_type_and_value(element_name, self.locators)

    def get_locator(self, element_name: str):
        """Return (By, locator) tuple for use in explicit waits"""
        by_type, locator_value = get_locator_type_and_value(element_name, self.locators)
        return (by_type, locator_value)

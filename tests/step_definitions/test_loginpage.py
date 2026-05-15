from time import sleep
import pytest
from pytest_bdd import scenarios, given, when, then
from pages.loginpage import Loginpage
from pages.BasePage import *
from conftest import *
import time
from selenium.webdriver import Keys

scenarios('../features/login.feature')

loginpage = None

@pytest.fixture(autouse=True)
def loginpage(browser):
    global loginpage
    loginpage = Loginpage(browser)
    # return Loginpage(browser)
    # loginpagex = Loginpage(browser)

@given('open url')
def open_url(browser, url):
    browser.get(url)

@then('user should navigate to loginpage')
def loginpages(browser):
    print(browser.title)

# Validate login functionality with valid input
@given('User Enter valid email')
def enter_email_id(browser):
    emial_input_locator = loginpage.get_loginpage_element_locator_type_and_value('email')
    enter_text(emial_input_locator, 'standard_user')
    sleep(5)

@given('User Enter valid password')
def enter_password(browser):
    password_input_locator = loginpage.get_loginpage_element_locator_type_and_value('password')
    enter_text(password_input_locator, 'secret_sauce')

@then('User User click on login Icon')
def click_Login_button(browser):
    Login_button = loginpage.get_element('Sign_in_button')
    Login_button.click()













##################################
# Validate login functionality with invalid input
@when('User enters invalid input in email id')
def enter_email_id_invalid(browser):
    emial_input_locator = loginpage.get_loginpage_element_locator_type_and_value('Email')
    enter_text(emial_input_locator, 'abc.com')

@then('User enters invalid input in password')
def enter_password_invalid(browser):
    password_input_locator = loginpage.get_loginpage_element_locator_type_and_value('Password')
    enter_text(password_input_locator, 'abcd1234')

@then('User verify assert message for login with invalid input')
def assert_invalid_login(browser):
    Excepted_message = 'Incorrect email or password.'
    assert_meessage = get_element_text(
        loginpage.get_loginpage_element_locator_type_and_value('asser_invalid_login_message')
    )
    print("Assert invalid login functionality : ", assert_meessage)
    assert assert_meessage == Excepted_message

# Create account - valid input
@given('User click on Create Account Link')
def click_create_account_link(browser):
    create_account_link = loginpage.get_element('Create_account_link')
    force_click(create_account_link)

@when('User enters valid input in First Name')
def enter_First_Name(browser):
    firstname_locator = loginpage.get_loginpage_element_locator_type_and_value('first_name')
    enter_text(firstname_locator, 'Ranjan')

@when('User enters valid input in Last Name')
def enter_Last_Name(browser):
    lastname_locator = loginpage.get_loginpage_element_locator_type_and_value('last_name')
    enter_text(lastname_locator, 'Kumar')

@when('User enters valid input in email id create account')
def enter_Email_id(browser):
    email_id_locator = loginpage.get_loginpage_element_locator_type_and_value('Cust_email')
    enter_text(email_id_locator, 'ranjan@gmail.com')
    sleep(6)

@then('User enters valid input in password create account')
def enter_password_create(browser):
    password_input_locator = loginpage.get_loginpage_element_locator_type_and_value('Cust_Password')
    enter_text(password_input_locator, 'abcdef')

@then('User Select yes checkbox')
def Select_Yes_Checkbox(browser):
    Yes_checkbox = loginpage.get_element('Yes_checkbox')
    force_click(Yes_checkbox)

@then('User click on Create Button')
def click_create_button(browser):
    create_button_element = loginpage.get_element('Create_button')
    force_click(create_button_element)

@then('User verify the create account Sucessfully assert message')
def verify_create_account_success(browser):
    Excepted_message = 'Account'
    assert_meessage = get_element_text(
        loginpage.get_loginpage_element_locator_type_and_value('Asert_message')
    )
    print("Error message on login screen: ", assert_meessage)
    assert assert_meessage == Excepted_message

# Create account - invalid input
@when('User enters invalid input in First Name')
def enter_First_Name_invalid(browser):
    firstname_locator = loginpage.get_loginpage_element_locator_type_and_value('first_name')
    enter_text(firstname_locator, '1234')

@when('User enters invalid input in Last Name')
def enter_Last_Name_invalid(browser):
    lastname_locator = loginpage.get_loginpage_element_locator_type_and_value('last_name')
    enter_text(lastname_locator, '56')

@when('User enters invalid input in email id create account')
def enter_Email_id_invalid(browser):
    email_id_locator = loginpage.get_loginpage_element_locator_type_and_value('Cust_email')
    enter_text(email_id_locator, 'ranjan.com')
    sleep(4)

@then('User enters invalid input in password create account')
def enter_password_create_invalid(browser):
    password_input_locator = loginpage.get_loginpage_element_locator_type_and_value('Cust_Password')
    enter_text(password_input_locator, 'abc')


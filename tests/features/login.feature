@loginpage
Feature: verify loginpage Functionality

  Background:
    Given open url
    Then user should navigate to loginpage

  @login_signin @valid_login
  Scenario: Validate login functionality with valid input
    Given User Enter valid email
    Given User Enter valid password
    Then User User click on login Icon



@ui
Feature: Login

  Scenario: Invalid login
    Given user is on login page
    When user logs in with invalid credentials
    Then error message should be displayed


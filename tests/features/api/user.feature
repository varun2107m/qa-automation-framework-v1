@api
Feature: User API

 Scenario Outline: Get user details
  Given the API client is ready
  When I request user with id <user_id>
  Then response status should be <status>

Examples:
  | user_id | status |
  | 2       | 200    |
  | 999     | 404    |



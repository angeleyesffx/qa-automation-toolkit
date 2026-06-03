Feature: Login functionality
  As a QA engineer
  I want to validate login scenarios
  So that authentication behavior is correct

  Scenario: Successful login with valid credentials
    Given I open the login page
    When I submit valid credentials
    Then I should be redirected to the secure area
    And I should see a successful login message

  Scenario: Login fails with invalid credentials
    Given I open the login page
    When I submit an invalid username and password
    Then I should see an invalid credentials message

  Scenario: Login fails with empty credentials
    Given I open the login page
    When I submit empty credentials
    Then I should see a missing username message

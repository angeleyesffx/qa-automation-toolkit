Feature: Checkbox interactions
  As a QA engineer
  I want to verify checkbox states and interactions
  So that users can toggle options correctly

  Scenario: Validate default checkbox states
    Given I open the checkboxes page
    Then the first checkbox should be unchecked
    And the second checkbox should be checked

  Scenario: Toggle both checkboxes to unchecked
    Given I open the checkboxes page
    When I check the first checkbox
    And I uncheck the second checkbox
    Then both checkboxes should be unchecked

  Scenario: Keep first checkbox checked after toggling second checkbox
    Given I open the checkboxes page
    When I check the first checkbox
    And I uncheck the second checkbox
    Then the first checkbox should stay checked

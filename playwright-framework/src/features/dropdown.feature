Feature: Dropdown selection
  As a QA engineer
  I want to verify dropdown behavior
  So that option selection works as expected

  Scenario: Select Option 1
    Given I open the dropdown page
    When I select "Option 1" from the dropdown
    Then I should see "Option 1" selected

  Scenario: Select Option 2
    Given I open the dropdown page
    When I select "Option 2" from the dropdown
    Then I should see "Option 2" selected

  Scenario: Change selected option
    Given I open the dropdown page
    When I switch from Option 1 to Option 2
    Then the selected dropdown value should be Option 2

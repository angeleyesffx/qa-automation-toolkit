import { Given, Then, When } from '@cucumber/cucumber';
import { expect } from '@playwright/test';
import { DropdownPage } from '../pages/DropdownPage';
import { CustomWorld } from '../support/world';

Given('I open the dropdown page', async function (this: CustomWorld) {
  this.dropdownPage = new DropdownPage(this.page!);
  await this.dropdownPage.open();
});

When('I select {string} from the dropdown', async function (this: CustomWorld, option: string) {
  await this.dropdownPage!.selectOption(option as 'Option 1' | 'Option 2');
});

Then('I should see {string} selected', async function (this: CustomWorld, option: string) {
  await expect(await this.dropdownPage!.getSelectedOption()).toBe(option);
});

When('I switch from Option 1 to Option 2', async function (this: CustomWorld) {
  await this.dropdownPage!.selectOption('Option 1');
  await this.dropdownPage!.selectOption('Option 2');
});

Then('the selected dropdown value should be Option 2', async function (this: CustomWorld) {
  await expect(await this.dropdownPage!.getSelectedOption()).toBe('Option 2');
});

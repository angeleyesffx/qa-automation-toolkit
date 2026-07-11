import { Given, Then, When } from '@cucumber/cucumber';
import { expect } from '@playwright/test';
import { CheckboxesPage } from '../pages/CheckboxesPage';
import { CustomWorld } from '../support/world';

Given('I open the checkboxes page', async function (this: CustomWorld) {
  this.checkboxesPage = new CheckboxesPage(this.page!);
  await this.checkboxesPage.open();
});

Then('the first checkbox should be unchecked', async function (this: CustomWorld) {
  await expect(await this.checkboxesPage!.isCheckboxChecked(0)).toBeFalsy();
});

Then('the second checkbox should be checked', async function (this: CustomWorld) {
  await expect(await this.checkboxesPage!.isCheckboxChecked(1)).toBeTruthy();
});

When('I check the first checkbox', async function (this: CustomWorld) {
  await this.checkboxesPage!.setCheckbox(0, true);
});

When('I uncheck the second checkbox', async function (this: CustomWorld) {
  await this.checkboxesPage!.setCheckbox(1, false);
});

Then('both checkboxes should be unchecked', async function (this: CustomWorld) {
  await expect(await this.checkboxesPage!.isCheckboxChecked(0)).toBeFalsy();
  await expect(await this.checkboxesPage!.isCheckboxChecked(1)).toBeFalsy();
});

Then('the first checkbox should stay checked', async function (this: CustomWorld) {
  await expect(await this.checkboxesPage!.isCheckboxChecked(0)).toBeTruthy();
});

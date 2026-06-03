import { Given, Then, When } from '@cucumber/cucumber';
import { expect } from '@playwright/test';
import { LoginPage } from '../pages/LoginPage';
import { CustomWorld } from '../support/world';

Given('I open the login page', async function (this: CustomWorld) {
  this.loginPage = new LoginPage(this.page!);
  await this.loginPage.open();
});

When('I submit valid credentials', async function (this: CustomWorld) {
  await this.loginPage!.login('tomsmith', 'SuperSecretPassword!');
});

Then('I should be redirected to the secure area', async function (this: CustomWorld) {
  await this.loginPage!.expectSecureAreaLoaded();
});

Then('I should see a successful login message', async function (this: CustomWorld) {
  const flashMessage = await this.loginPage!.getFlashMessage();
  await expect(flashMessage).toContain('You logged into a secure area!');
});

When('I submit an invalid username and password', async function (this: CustomWorld) {
  await this.loginPage!.login('invalid_user', 'invalid_pass');
});

Then('I should see an invalid credentials message', async function (this: CustomWorld) {
  const flashMessage = await this.loginPage!.getFlashMessage();
  await expect(flashMessage).toContain('Your username is invalid!');
});

When('I submit empty credentials', async function (this: CustomWorld) {
  await this.loginPage!.login('', '');
});

Then('I should see a missing username message', async function (this: CustomWorld) {
  const flashMessage = await this.loginPage!.getFlashMessage();
  await expect(flashMessage).toContain('Your username is invalid!');
});

import { expect, Locator, Page } from '@playwright/test';
import { BasePage } from './BasePage';

export class LoginPage extends BasePage {
  private readonly usernameInput: Locator;
  private readonly passwordInput: Locator;
  private readonly loginButton: Locator;
  private readonly flashMessage: Locator;
  private readonly secureAreaHeading: Locator;

  constructor(page: Page) {
    super(page);
    this.usernameInput = page.locator('#username');
    this.passwordInput = page.locator('#password');
    this.loginButton = page.locator('button[type="submit"]');
    this.flashMessage = page.locator('#flash');
    this.secureAreaHeading = page.locator('div.example h2');
  }

  async open(): Promise<void> {
    await this.navigate('/login');
    await expect(this.usernameInput).toBeVisible();
  }

  async login(username: string, password: string): Promise<void> {
    try {
      await this.usernameInput.fill(username);
      await this.passwordInput.fill(password);
      await this.loginButton.click();
    } catch (error) {
      throw new Error(`Unable to perform login: ${String(error)}`);
    }
  }

  async getFlashMessage(): Promise<string> {
    try {
      await expect(this.flashMessage).toBeVisible();
      return (await this.flashMessage.innerText()).replace('×', '').trim();
    } catch (error) {
      throw new Error(`Unable to get flash message: ${String(error)}`);
    }
  }

  async expectSecureAreaLoaded(): Promise<void> {
    try {
      await expect(this.secureAreaHeading).toContainText('Secure Area');
    } catch (error) {
      throw new Error(`Secure area validation failed: ${String(error)}`);
    }
  }
}

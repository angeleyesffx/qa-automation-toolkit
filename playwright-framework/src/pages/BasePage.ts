import { Page } from '@playwright/test';

export class BasePage {
  protected readonly page: Page;
  protected readonly baseUrl = 'https://the-internet.herokuapp.com';

  constructor(page: Page) {
    this.page = page;
  }

  async navigate(path: string): Promise<void> {
    try {
      await this.page.goto(`${this.baseUrl}${path}`, { waitUntil: 'domcontentloaded' });
    } catch (error) {
      throw new Error(`Unable to navigate to path "${path}": ${String(error)}`);
    }
  }
}

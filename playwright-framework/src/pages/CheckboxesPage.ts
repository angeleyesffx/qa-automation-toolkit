import { expect, Locator, Page } from '@playwright/test';
import { BasePage } from './BasePage';

export class CheckboxesPage extends BasePage {
  private readonly checkboxes: Locator;

  constructor(page: Page) {
    super(page);
    this.checkboxes = page.locator('#checkboxes input[type="checkbox"]');
  }

  async open(): Promise<void> {
    await this.navigate('/checkboxes');
    await expect(this.checkboxes).toHaveCount(2);
  }

  async setCheckbox(index: number, checked: boolean): Promise<void> {
    try {
      const checkbox = this.checkboxes.nth(index);
      if (checked) {
        await checkbox.check();
      } else {
        await checkbox.uncheck();
      }
    } catch (error) {
      throw new Error(`Unable to set checkbox ${index}: ${String(error)}`);
    }
  }

  async isCheckboxChecked(index: number): Promise<boolean> {
    try {
      return this.checkboxes.nth(index).isChecked();
    } catch (error) {
      throw new Error(`Unable to get checkbox ${index} state: ${String(error)}`);
    }
  }
}

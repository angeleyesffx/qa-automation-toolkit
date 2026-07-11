import { expect, Locator, Page } from '@playwright/test';
import { BasePage } from './BasePage';

export class DropdownPage extends BasePage {
  private readonly dropdown: Locator;

  constructor(page: Page) {
    super(page);
    this.dropdown = page.locator('#dropdown');
  }

  async open(): Promise<void> {
    await this.navigate('/dropdown');
    await expect(this.dropdown).toBeVisible();
  }

  async selectOption(optionLabel: 'Option 1' | 'Option 2'): Promise<void> {
    try {
      await this.dropdown.selectOption({ label: optionLabel });
    } catch (error) {
      throw new Error(`Unable to select option "${optionLabel}": ${String(error)}`);
    }
  }

  async getSelectedOption(): Promise<string> {
    try {
      const selected = this.dropdown.locator('option:checked');
      return (await selected.innerText()).trim();
    } catch (error) {
      throw new Error(`Unable to read selected option: ${String(error)}`);
    }
  }
}

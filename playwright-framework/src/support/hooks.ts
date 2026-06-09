import {
  After,
  AfterAll,
  Before,
  ITestCaseHookParameter,
  setDefaultTimeout
} from '@cucumber/cucumber';
import { Browser, chromium, firefox, webkit } from '@playwright/test';
import fs from 'node:fs';
import path from 'node:path';
import { CustomWorld } from './world';

setDefaultTimeout(60 * 1000);

let browser: Browser;

Before(async function (this: CustomWorld) {
  const browserName = (process.env.BROWSER ?? 'chromium').toLowerCase();

  if (!browser) {
    if (browserName === 'firefox') {
      browser = await firefox.launch({ headless: true });
    } else if (browserName === 'webkit') {
      browser = await webkit.launch({ headless: true });
    } else {
      browser = await chromium.launch({ headless: true });
    }
  }

  this.browser = browser;
  this.context = await browser.newContext();
  this.page = await this.context.newPage();
});

After(async function (this: CustomWorld, scenario: ITestCaseHookParameter) {
  if (scenario.result?.status === 'FAILED' && this.page) {
    const screenshotDir = path.resolve('reports', 'screenshots');
    if (!fs.existsSync(screenshotDir)) {
      fs.mkdirSync(screenshotDir, { recursive: true });
    }

    const safeName = scenario.pickle.name.replace(/[^a-zA-Z0-9-_]+/g, '_');
    const screenshotPath = path.join(screenshotDir, `${Date.now()}-${safeName}.png`);
    await this.page.screenshot({ path: screenshotPath, fullPage: true });

    const screenshot = fs.readFileSync(screenshotPath);
    await this.attach(screenshot, 'image/png');
  }

  await this.context?.close();
});

AfterAll(async function () {
  await browser?.close();
});

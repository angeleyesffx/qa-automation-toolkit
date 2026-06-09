import { defineConfig, devices } from '@playwright/test';

export default defineConfig({
  testDir: './src/features',
  timeout: 60_000,
  fullyParallel: false,
  reporter: [['html', { outputFolder: 'reports/playwright-html', open: 'never' }]],
  use: {
    baseURL: 'https://the-internet.herokuapp.com',
    trace: 'retain-on-failure',
    screenshot: 'only-on-failure',
    video: 'retain-on-failure'
  },
  projects: [
    {
      name: 'chromium',
      use: { ...devices['Desktop Chrome'] }
    },
    {
      name: 'firefox',
      use: { ...devices['Desktop Firefox'] }
    },
    {
      name: 'webkit',
      use: { ...devices['Desktop Safari'] }
    }
  ]
});

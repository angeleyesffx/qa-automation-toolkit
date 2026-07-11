# Playwright QA Automation Framework

Production-ready QA automation framework using **TypeScript**, **Playwright**, **Cucumber.js**, and the **Page Object Model** pattern.

Author: **Priscilla R Martins**

## Target Application

- https://the-internet.herokuapp.com

## Features Covered

- Login (`/login`): valid login, invalid login, empty credentials
- Checkboxes (`/checkboxes`): default states and state toggling
- Dropdown (`/dropdown`): option selection and value switching

## Tech Stack

- Playwright (Chromium, Firefox, WebKit)
- Cucumber.js (BDD)
- TypeScript

## Project Structure

```text
playwright-framework/
├── src/
│   ├── pages/
│   ├── features/
│   ├── step-definitions/
│   └── support/
├── playwright.config.ts
├── cucumber.config.js
├── package.json
├── tsconfig.json
└── README.md
```

## Run Locally

```bash
cd /tmp/workspace/angeleyesffx/lazy_qa/playwright-framework
npm install
npx playwright install --with-deps
```

Run by browser:

```bash
npm run test:chromium
npm run test:firefox
npm run test:webkit
```

Run all browsers:

```bash
npm run test:all
```

Reports are generated in:

- `reports/cucumber-report.json`
- `reports/cucumber-report-inline.html`
- `reports/screenshots/` (on failures)

## CI/CD

The workflow `.github/workflows/playwright.yml` runs on `ubuntu-latest`, installs Playwright browsers with dependencies, executes tests using a browser matrix (`chromium`, `firefox`, `webkit`), and uploads report artifacts.

module.exports = {
  default: {
    paths: ['src/features/**/*.feature'],
    require: ['src/step-definitions/**/*.ts', 'src/support/**/*.ts'],
    requireModule: ['ts-node/register'],
    format: [
      'progress-bar',
      'json:reports/cucumber-report.json',
      'html:reports/cucumber-report-inline.html'
    ],
    parallel: 1,
    timeout: 60 * 1000
  }
};

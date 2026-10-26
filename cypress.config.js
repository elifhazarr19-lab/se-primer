const { defineConfig } = require('cypress');

module.exports = defineConfig({
  e2e: {
    baseUrl: process.env.BASE_URL || 'https://se-primer-1-282987152472.europe-west2.run.app',
    specPattern: 'cypress/e2e/**/*.cy.js',
    supportFile: false,
    video: true,
    videosFolder: 'cypress/videos',
    defaultCommandTimeout: 10000,
    viewportWidth: 390,
    viewportHeight: 844,
  },
});

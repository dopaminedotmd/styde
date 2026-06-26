const { remote } = require('webdriverio');

const ANDROID = process.env.PLATFORM === 'android';

const sauceOptions = {
  user: process.env.SAUCE_USERNAME,
  key: process.env.SAUCE_ACCESS_KEY,
};

const iosBrowserStack = {
  ...iosOptions,
  'bstack:options': {
    userName: process.env.BROWSERSTACK_USERNAME,
    accessKey: process.env.BROWSERSTACK_ACCESS_KEY,
    projectName: 'YourApp Mobile Tests',
    buildName: `Build ${process.env.BUILD_NUMBER || 'local'}`,
    sessionName: 'iOS E2E Smoke',
    local: false,
    debug: true,
    networkLogs: true,
    consoleLogs: 'info',
  },
};

const androidBrowserStack = {
  ...androidOptions,
  'bstack:options': {
    userName: process.env.BROWSERSTACK_USERNAME,
    accessKey: process.env.BROWSERSTACK_ACCESS_KEY,
    projectName: 'YourApp Mobile Tests',
    buildName: `Build ${process.env.BUILD_NUMBER || 'local'}`,
    sessionName: 'Android E2E Smoke',
    local: false,
    debug: true,
    networkLogs: true,
    consoleLogs: 'info',
    deviceLogs: true,
  },
};

async function runBrowserStackTests() {
  const options = ANDROID ? androidBrowserStack : iosBrowserStack;
  options.capabilities['bstack:options'].sessionName =
    `${process.env.PLATFORM} - ${process.env.SUITE || 'smoke'}`;

  const driver = await remote(options);

  try {
    console.log(`[BrowserStack] Running on ${(ANDROID ? 'Android' : 'iOS')}`);
    const start = Date.now();

    // Login
    if (ANDROID) {
      await driver.$('id=email-input').setValue('test@example.com');
      await driver.$('id=password-input').setValue('password123');
      await driver.$('id=login-button').click();
    } else {
      await driver.$('~email-input').setValue('test@example.com');
      await driver.$('~password-input').setValue('password123');
      await driver.$('~login-button').click();
    }

    await driver.pause(3000);

    const status = ANDROID
      ? await driver.$('id=home-screen').isDisplayed()
      : await driver.$('~home-screen').isDisplayed();

    const elapsed = ((Date.now() - start) / 1000).toFixed(1);
    console.log(`[BrowserStack] Login test: ${status ? 'PASS' : 'FAIL'} (${elapsed}s)`);

    if (!status) throw new Error('Home screen not visible after login');

    // Mark test passed in BrowserStack
    await driver.executeScript(
      'browserstack_executor: {"action": "setSessionStatus", "arguments": {"status":"passed","reason": "All assertions passed"}}'
    );
  } catch (err) {
    console.error(`[BrowserStack] FAILED: ${err.message}`);
    await driver.executeScript(
      'browserstack_executor: {"action": "setSessionStatus", "arguments": {"status":"failed","reason": err.message}}'
    );
    throw err;
  } finally {
    await driver.deleteSession();
  }
}

runBrowserStackTests()
  .then(() => process.exit(0))
  .catch(() => process.exit(1));

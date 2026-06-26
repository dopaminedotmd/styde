const { remote } = require('webdriverio');

const APPIUM_SERVER = process.env.APPIUM_SERVER || 'http://localhost:4723';

const iosOptions = {
  port: 4723,
  capabilities: {
    platformName: 'iOS',
    'appium:automationName': 'XCUITest',
    'appium:deviceName': 'iPhone 15 Pro',
    'appium:platformVersion': '17.2',
    'appium:app': process.env.IOS_APP_PATH,
    'appium:bundleId': 'com.yourapp',
    'appium:waitForIdleTimeout': 500,
    'appium:noReset': false,
    'appium:fullReset': true,
  },
};

const androidOptions = {
  port: 4723,
  capabilities: {
    platformName: 'Android',
    'appium:automationName': 'UiAutomator2',
    'appium:deviceName': 'Pixel_6_API_34',
    'appium:platformVersion': '14',
    'appium:app': process.env.ANDROID_APP_PATH,
    'appium:appPackage': 'com.yourapp',
    'appium:appActivity': 'com.yourapp.MainActivity',
    'appium:noReset': false,
    'appium:fullReset': true,
    'appium:autoGrantPermissions': true,
    'appium:adbExecTimeout': 60000,
  },
};

const CI_PLATFORM = process.env.PLATFORM || 'android';
const TARGET_OPTIONS = CI_PLATFORM === 'ios' ? iosOptions : androidOptions;
const ANDROID = CI_PLATFORM === 'android';

async function waitForElement(driver, selector, timeout = 10000) {
  const element = ANDROID
    ? driver.$(selector)
    : driver.$(`~${selector}`);
  await element.waitForDisplayed({ timeout });
  return element;
}

async function runAppiumTests() {
  const driver = await remote(TARGET_OPTIONS);

  try {
    console.log(`[Appium] Running on ${CI_PLATFORM.toUpperCase()}`);

    // Login flow
    if (ANDROID) {
      await driver.$('id=email-input').setValue('test@example.com');
      await driver.$('id=password-input').setValue('password123');
      await driver.$('id=login-button').click();
    } else {
      await driver.$('~email-input').setValue('test@example.com');
      await driver.$('~password-input').setValue('password123');
      await driver.$('~login-button').click();
    }

    await driver.pause(2000);

    // Verify home screen
    const homeScreen = ANDROID
      ? await driver.$('id=home-screen')
      : await driver.$('~home-screen');
    const isHomeVisible = await homeScreen.isDisplayed();
    console.log(`[Appium] Home screen visible: ${isHomeVisible}`);

    // Navigate tabs
    if (ANDROID) {
      await driver.$('id=tab-search').click();
      await driver.pause(1000);
      await driver.$('id=tab-profile').click();
      await driver.pause(1000);
      await driver.$('id=tab-home').click();
    } else {
      await driver.$('~tab-search').click();
      await driver.pause(1000);
      await driver.$('~tab-profile').click();
      await driver.pause(1000);
      await driver.$('~tab-home').click();
    }

    console.log('[Appium] Tab navigation test PASSED');

    // Screenshot
    await driver.saveScreenshot('.artifacts/appium/screenshot-final.png');
    console.log('[Appium] Screenshot captured');

  } catch (err) {
    console.error(`[Appium] FAILED: ${err.message}`);
    try {
      await driver.saveScreenshot('.artifacts/appium/screenshot-failure.png');
    } catch (_) {}
    throw err;
  } finally {
    await driver.deleteSession();
  }
}

runAppiumTests()
  .then(() => {
    console.log('[Appium] All tests PASSED');
    process.exit(0);
  })
  .catch((err) => {
    console.error(`[Appium] Tests FAILED: ${err.message}`);
    process.exit(1);
  });

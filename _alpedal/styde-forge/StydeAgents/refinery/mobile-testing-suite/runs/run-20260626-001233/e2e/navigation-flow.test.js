const { by, device, element, expect, waitFor } = require('detox');

describe('Navigation Flow', () => {
  beforeAll(async () => {
    await device.launchApp({ delete: true });
    await element(by.id('email-input')).typeText('test@example.com');
    await element(by.id('password-input')).typeText('password123');
    await element(by.id('login-button')).tap();
    await waitFor(element(by.id('home-screen')))
      .toBeVisible()
      .withTimeout(10000);
  });

  it('should show bottom tab bar', async () => {
    await expect(element(by.id('tab-home'))).toBeVisible();
    await expect(element(by.id('tab-search'))).toBeVisible();
    await expect(element(by.id('tab-profile'))).toBeVisible();
  });

  it('should navigate between tabs', async () => {
    await element(by.id('tab-search')).tap();
    await expect(element(by.id('search-screen'))).toBeVisible();
    await element(by.id('tab-profile')).tap();
    await expect(element(by.id('profile-screen'))).toBeVisible();
    await element(by.id('tab-home')).tap();
    await expect(element(by.id('home-screen'))).toBeVisible();
  });

  it('should navigate to detail screen and go back', async () => {
    await expect(element(by.id('home-list-item-0'))).toBeVisible();
    await element(by.id('home-list-item-0')).tap();
    await expect(element(by.id('detail-screen'))).toBeVisible();
    await expect(element(by.id('detail-title'))).toBeVisible();
    await element(by.id('back-button')).tap();
    await expect(element(by.id('home-screen'))).toBeVisible();
  });

  it('should handle deep links', async () => {
    await device.sendUserActivity({
      type: 'url',
      url: 'yourapp://item/42',
    });
    await expect(element(by.id('detail-screen'))).toBeVisible();
    await expect(element(by.id('detail-item-id'))).toHaveText('42');
  });

  it('should swipe back gesture work', async () => {
    await element(by.id('home-list-item-1')).tap();
    await expect(element(by.id('detail-screen'))).toBeVisible();
    await element(by.id('detail-screen')).swipe('right');
    await expect(element(by.id('home-screen'))).toBeVisible();
  });
});

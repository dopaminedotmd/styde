const { by, device, element, expect, waitFor } = require('detox');

describe('Search Flow', () => {
  beforeAll(async () => {
    await device.launchApp({ delete: true });
    await element(by.id('email-input')).typeText('test@example.com');
    await element(by.id('password-input')).typeText('password123');
    await element(by.id('login-button')).tap();
    await waitFor(element(by.id('home-screen')))
      .toBeVisible()
      .withTimeout(10000);
    await element(by.id('tab-search')).tap();
  });

  it('should show search input', async () => {
    await expect(element(by.id('search-input'))).toBeVisible();
    await expect(element(by.id('search-button'))).toBeVisible();
  });

  it('should show empty state initially', async () => {
    await expect(element(by.id('empty-state'))).toBeVisible();
    await expect(element(by.id('empty-state-text'))).toHaveText(
      'Search for items to get started',
    );
  });

  it('should display search results', async () => {
    await element(by.id('search-input')).typeText('test item');
    await element(by.id('search-button')).tap();
    await waitFor(element(by.id('search-results-list')))
      .toBeVisible()
      .withTimeout(5000);
    await expect(element(by.id('search-result-item-0'))).toBeVisible();
  });

  it('should show no results state', async () => {
    await element(by.id('search-input')).clearText();
    await element(by.id('search-input')).typeText('zzzznonexistent');
    await element(by.id('search-button')).tap();
    await waitFor(element(by.id('no-results-state')))
      .toBeVisible()
      .withTimeout(5000);
  });

  it('should debounce search input', async () => {
    await element(by.id('search-input')).clearText();
    await element(by.id('search-input')).typeText('a');
    await element(by.id('search-input')).typeText('b');
    await element(by.id('search-input')).typeText('c');
    await element(by.id('search-button')).tap();
    await expect(element(by.id('search-query-label'))).toHaveText('abc');
  });

  it('should navigate to detail from search results', async () => {
    await element(by.id('search-input')).clearText();
    await element(by.id('search-input')).typeText('test item');
    await element(by.id('search-button')).tap();
    await waitFor(element(by.id('search-results-list')))
      .toBeVisible()
      .withTimeout(5000);
    await element(by.id('search-result-item-0')).tap();
    await expect(element(by.id('detail-screen'))).toBeVisible();
  });
});

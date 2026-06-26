const { by, device, element, expect, waitFor } = require('detox');

describe('Offline Sync', () => {
  beforeAll(async () => {
    await device.launchApp({ delete: true });
    await element(by.id('email-input')).typeText('test@example.com');
    await element(by.id('password-input')).typeText('password123');
    await element(by.id('login-button')).tap();
    await waitFor(element(by.id('home-screen')))
      .toBeVisible()
      .withTimeout(10000);
  });

  it('should show offline banner when disconnected', async () => {
    await device.setStatusBar({
      networkMode: 'airplane-mode',
    });
    await expect(element(by.id('offline-banner'))).toBeVisible();
    await expect(element(by.id('offline-banner-text'))).toHaveText(
      'You are offline. Changes will sync when connected.',
    );
  });

  it('should allow offline item creation', async () => {
    await device.setStatusBar({
      networkMode: 'airplane-mode',
    });
    await element(by.id('create-item-fab')).tap();
    await element(by.id('item-title-input')).typeText('Offline Item');
    await element(by.id('save-item-button')).tap();
    await expect(element(by.id('pending-sync-badge'))).toBeVisible();
  });

  it('should sync queued items on reconnection', async () => {
    await device.setStatusBar({
      networkMode: 'airplane-mode',
    });
    await element(by.id('create-item-fab')).tap();
    await element(by.id('item-title-input')).typeText('Sync Test');
    await element(by.id('save-item-button')).tap();
    await device.setStatusBar({
      networkMode: 'full',
    });
    await waitFor(element(by.id('sync-complete-toast')))
      .toBeVisible()
      .withTimeout(15000);
    await expect(element(by.id('pending-sync-badge'))).not.toBeVisible();
  });

  it('should handle sync conflicts', async () => {
    await element(by.id('create-item-fab')).tap();
    await element(by.id('item-title-input')).typeText('Conflict Item');
    await element(by.id('save-item-button')).tap();
    await device.setStatusBar({
      networkMode: 'airplane-mode',
    });
    await element(by.id('create-item-fab')).tap();
    await element(by.id('item-title-input')).typeText('Conflict Item Modified Offline');
    await element(by.id('save-item-button')).tap();
    await device.setStatusBar({
      networkMode: 'full',
    });
    await waitFor(element(by.id('conflict-resolver-modal')))
      .toBeVisible()
      .withTimeout(10000);
    await expect(element(by.id('conflict-local-version'))).toBeVisible();
    await expect(element(by.id('conflict-remote-version'))).toBeVisible();
    await element(by.id('use-local-version-button')).tap();
    await expect(element(by.id('sync-complete-toast'))).toBeVisible();
  });

  it('should show sync progress indicator', async () => {
    await device.setStatusBar({
      networkMode: 'airplane-mode',
    });
    for (let i = 0; i < 5; i++) {
      await element(by.id('create-item-fab')).tap();
      await element(by.id('item-title-input')).typeText(`Batch Item ${i}`);
      await element(by.id('save-item-button')).tap();
    }
    await device.setStatusBar({
      networkMode: 'full',
    });
    await expect(element(by.id('sync-progress-bar'))).toBeVisible();
    await waitFor(element(by.id('sync-complete-toast')))
      .toBeVisible()
      .withTimeout(20000);
  });
});

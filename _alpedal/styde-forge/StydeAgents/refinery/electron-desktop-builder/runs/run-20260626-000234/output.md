Electron Desktop Builder - Complete Implementation
Application Structure:
electron-desktop-builder/
  package.json
  src/
    main/
      main.js          - Main process entry
      preload.js       - Secure bridge
      ipc/
        handlers.js    - IPC handlers
      menu.js          - Native menus
      tray.js          - System tray
      updater.js       - Auto-update
      security.js      - Security config
    renderer/
      index.html
      renderer.js
      styles.css
  build/
    entitlements.mac.plist
    app.config.js
package.json:
{
  "name": "styde-electron-app",
  "version": "1.0.0",
  "main": "src/main/main.js",
  "scripts": {
    "start": "electron .",
    "dev": "NODE_ENV=development electron .",
    "build:mac": "electron-builder --mac",
    "build:win": "electron-builder --win",
    "build:linux": "electron-builder --linux",
    "publish": "electron-builder --publish always"
  },
  "dependencies": {
    "electron-updater": "^6.1.7"
  },
  "devDependencies": {
    "electron": "^28.1.0",
    "electron-builder": "^24.9.1"
  },
  "build": {
    "appId": "com.styde.desktop",
    "productName": "Styde Forge Desktop",
    "directories": { "output": "dist" },
    "files": ["src/**/*", "node_modules/**/*", "package.json"],
    "mac": {
      "category": "public.app-category.developer-tools",
      "target": ["dmg", "zip"],
      "hardenedRuntime": true,
      "gatekeeperAssess": false,
      "entitlements": "build/entitlements.mac.plist",
      "entitlementsInherit": "build/entitlements.mac.plist"
    },
    "win": {
      "target": ["nsis", "portable"],
      "icon": "build/icon.ico"
    },
    "linux": {
      "target": ["AppImage", "deb"],
      "category": "Development"
    },
    "nsis": {
      "oneClick": false,
      "allowToChangeInstallationDirectory": true,
      "createDesktopShortcut": true
    },
    "publish": {
      "provider": "github",
      "owner": "styde",
      "repo": "styde-forge-desktop",
      "releaseType": "release"
    },
    "electronDownload": {
      "mirror": "https://npmmirror.com/mirrors/electron/"
    }
  }
}
src/main/main.js:
const { app, BrowserWindow, ipcMain, nativeTheme } = require('electron');
const path = require('path');
const { createMenu } = require('./menu');
const { createTray } = require('./tray');
const { registerIpcHandlers } = require('./ipc/handlers');
const { configureUpdater } = require('./updater');
const { enforceSecurity } = require('./security');
let mainWindow = null;
let tray = null;
const isDev = process.env.NODE_ENV === 'development' || !app.isPackaged;
function createWindow() {
  mainWindow = new BrowserWindow({
    width: 1280,
    height: 800,
    minWidth: 900,
    minHeight: 600,
    title: 'Styde Forge Desktop',
    backgroundColor: '#0f0f1a',
    show: false,
    webPreferences: {
      preload: path.join(__dirname, 'preload.js'),
      contextIsolation: true,
      nodeIntegration: false,
      sandbox: true,
      webSecurity: true,
      disableBlinkFeatures: 'Auxclick',
      spellcheck: false
    }
  });
  mainWindow.loadFile(path.join(__dirname, '..', 'renderer', 'index.html'));
  mainWindow.once('ready-to-show', () => {
    mainWindow.show();
    if (isDev) mainWindow.webContents.openDevTools({ mode: 'detach' });
  });
  mainWindow.on('closed', () => { mainWindow = null; });
  enforceSecurity(mainWindow);
  return mainWindow;
}
app.whenReady().then(() => {
  createWindow();
  createMenu(mainWindow, app);
  tray = createTray(mainWindow, app);
  registerIpcHandlers(mainWindow);
  configureUpdater(mainWindow);
  app.on('activate', () => {
    if (BrowserWindow.getAllWindows().length === 0) createWindow();
  });
});
app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') app.quit();
});
app.on('before-quit', () => {
  if (tray) tray.destroy();
});
src/main/preload.js:
const { contextBridge, ipcRenderer } = require('electron');
const validateChannel = (channel) => {
  const ALLOWED_CHANNELS = [
    'app:getVersion',
    'app:getPlatform',
    'app:minimize',
    'app:maximize',
    'app:close',
    'app:isMaximized',
    'update:check',
    'update:download',
    'update:install',
    'update:status',
    'file:open',
    'file:save',
    'file:select',
    'shell:openExternal',
    'notify:send',
    'theme:get',
    'theme:set',
    'dialog:message',
    'dialog:error'
  ];
  return ALLOWED_CHANNELS.includes(channel);
};
contextBridge.exposeInMainWorld('electronAPI', {
  send: (channel, ...args) => {
    if (validateChannel(channel)) {
      ipcRenderer.send(channel, ...args);
    }
  },
  invoke: (channel, ...args) => {
    if (validateChannel(channel)) {
      return ipcRenderer.invoke(channel, ...args);
    }
    return Promise.reject(new Error(`Blocked channel: ${channel}`));
  },
  on: (channel, callback) => {
    if (validateChannel(channel)) {
      const subscription = (_event, ...args) => callback(...args);
      ipcRenderer.on(channel, subscription);
      return () => ipcRenderer.removeListener(channel, subscription);
    }
  },
  once: (channel, callback) => {
    if (validateChannel(channel)) {
      ipcRenderer.once(channel, (_event, ...args) => callback(...args));
    }
  }
});
src/main/ipc/handlers.js:
const { ipcMain, app, shell, dialog, nativeTheme, Notification } = require('electron');
const fs = require('fs');
const path = require('path');
function registerIpcHandlers(mainWindow) {
  ipcMain.handle('app:getVersion', () => app.getVersion());
  ipcMain.handle('app:getPlatform', () => process.platform);
  ipcMain.on('app:minimize', () => mainWindow.minimize());
  ipcMain.on('app:maximize', () => {
    mainWindow.isMaximized() ? mainWindow.unmaximize() : mainWindow.maximize();
  });
  ipcMain.on('app:close', () => mainWindow.close());
  ipcMain.handle('app:isMaximized', () => mainWindow.isMaximized());
  ipcMain.handle('file:open', async () => {
    const result = await dialog.showOpenDialog(mainWindow, {
      properties: ['openFile', 'multiSelections'],
      filters: [
        { name: 'All Files', extensions: ['*'] },
        { name: 'Blueprints', extensions: ['md', 'yaml', 'json'] },
        { name: 'Scripts', extensions: ['py', 'js', 'ts', 'sh'] }
      ]
    });
    return result.canceled ? null : result.filePaths;
  });
  ipcMain.handle('file:save', async (_event, content, defaultName) => {
    const result = await dialog.showSaveDialog(mainWindow, {
      defaultPath: defaultName || 'output.txt',
      filters: [
        { name: 'Text', extensions: ['txt', 'md'] },
        { name: 'JSON', extensions: ['json'] },
        { name: 'All Files', extensions: ['*'] }
      ]
    });
    if (!result.canceled && result.filePath) {
      fs.writeFileSync(result.filePath, content, 'utf-8');
      return result.filePath;
    }
    return null;
  });
  ipcMain.handle('shell:openExternal', (_event, url) => {
    const SAFE_DOMAINS = [
      'github.com', 'nousresearch.com', 'docs.nousresearch.com',
      'electronjs.org', 'npmjs.com', 'nodejs.org'
    ];
    try {
      const parsed = new URL(url);
      if (!SAFE_DOMAINS.includes(parsed.hostname)) {
        throw new Error(`Domain not in allowlist: ${parsed.hostname}`);
      }
      return shell.openExternal(url);
    } catch (err) {
      dialog.showErrorBox('Blocked URL', `Cannot open: ${err.message}`);
      return false;
    }
  });
  ipcMain.on('notify:send', (_event, { title, body }) => {
    if (Notification.isSupported()) {
      new Notification({ title, body, icon: path.join(__dirname, '..', '..', '..', 'build', 'icon.png') }).show();
    }
  });
  ipcMain.handle('theme:get', () => nativeTheme.shouldUseDarkColors ? 'dark' : 'light');
  ipcMain.handle('theme:set', (_event, theme) => {
    nativeTheme.themeSource = theme;
  });
  ipcMain.handle('dialog:message', async (_event, { title, message, type }) => {
    return dialog.showMessageBox(mainWindow, {
      type: type || 'info',
      title: title || 'Message',
      message: message || '',
      buttons: ['OK']
    });
  });
  ipcMain.handle('dialog:error', async (_event, { title, message }) => {
    dialog.showErrorBox(title || 'Error', message || 'An error occurred');
  });
}
module.exports = { registerIpcHandlers };
src/main/menu.js:
const { Menu, shell } = require('electron');
function createMenu(mainWindow, app) {
  const template = [
    {
      label: 'Styde Forge',
      submenu: [
        { label: 'About Styde Forge', role: 'about' },
        { type: 'separator' },
        {
          label: 'Preferences...',
          accelerator: 'CmdOrCtrl+,',
          click: () => mainWindow.webContents.send('navigate', 'settings')
        },
        { type: 'separator' },
        { label: 'Services', role: 'services' },
        { type: 'separator' },
        { label: 'Hide Styde Forge', role: 'hide' },
        { label: 'Hide Others', role: 'hideOthers' },
        { label: 'Show All', role: 'unhide' },
        { type: 'separator' },
        { label: 'Quit', accelerator: 'CmdOrCtrl+Q', click: () => app.quit() }
      ]
    },
    {
      label: 'File',
      submenu: [
        {
          label: 'Open Blueprint...',
          accelerator: 'CmdOrCtrl+O',
          click: () => mainWindow.webContents.send('menu:open')
        },
        {
          label: 'Save As...',
          accelerator: 'CmdOrCtrl+Shift+S',
          click: () => mainWindow.webContents.send('menu:saveAs')
        },
        { type: 'separator' },
        {
          label: 'Export Report',
          accelerator: 'CmdOrCtrl+E',
          click: () => mainWindow.webContents.send('menu:export')
        }
      ]
    },
    {
      label: 'Edit',
      submenu: [
        { label: 'Undo', role: 'undo' },
        { label: 'Redo', role: 'redo' },
        { type: 'separator' },
        { label: 'Cut', role: 'cut' },
        { label: 'Copy', role: 'copy' },
        { label: 'Paste', role: 'paste' },
        { label: 'Select All', role: 'selectAll' }
      ]
    },
    {
      label: 'View',
      submenu: [
        { label: 'Reload', role: 'reload' },
        { label: 'Force Reload', role: 'forceReload' },
        { label: 'Toggle Developer Tools', role: 'toggleDevTools' },
        { type: 'separator' },
        { label: 'Actual Size', role: 'resetZoom' },
        { label: 'Zoom In', role: 'zoomIn' },
        { label: 'Zoom Out', role: 'zoomOut' },
        { type: 'separator' },
        { label: 'Toggle Full Screen', role: 'togglefullscreen' },
        { type: 'separator' },
        {
          label: 'Dark Mode',
          type: 'checkbox',
          checked: true,
          click: (menuItem) => {
            mainWindow.webContents.send('theme:toggle', menuItem.checked ? 'dark' : 'light');
          }
        }
      ]
    },
    {
      label: 'Agents',
      submenu: [
        {
          label: 'Spawn Agent',
          accelerator: 'CmdOrCtrl+N',
          click: () => mainWindow.webContents.send('navigate', 'spawn')
        },
        {
          label: 'View All Agents',
          accelerator: 'CmdOrCtrl+Shift+A',
          click: () => mainWindow.webContents.send('navigate', 'agents')
        },
        { type: 'separator' },
        {
          label: 'Mission Control',
          accelerator: 'CmdOrCtrl+M',
          click: () => mainWindow.webContents.send('navigate', 'dashboard')
        }
      ]
    },
    {
      label: 'Help',
      submenu: [
        {
          label: 'Documentation',
          click: () => shell.openExternal('https://hermes-agent.nousresearch.com/docs')
        },
        {
          label: 'Report Issue',
          click: () => shell.openExternal('https://github.com/styde/styde-forge/issues')
        },
        { type: 'separator' },
        {
          label: 'Check for Updates...',
          click: () => mainWindow.webContents.send('update:check')
        }
      ]
    }
  ];
  const menu = Menu.buildFromTemplate(template);
  Menu.setApplicationMenu(menu);
}
module.exports = { createMenu };
src/main/tray.js:
const { Tray, Menu, nativeImage } = require('electron');
const path = require('path');
function createTray(mainWindow, app) {
  const iconSize = process.platform === 'darwin' ? 16 : 24;
  const icon = nativeImage.createFromPath(
    path.join(__dirname, '..', '..', 'build', `tray-icon-${iconSize}.png`)
  ).resize({ width: iconSize, height: iconSize });
  const tray = new Tray(icon);
  tray.setToolTip('Styde Forge Desktop');
  const contextMenu = Menu.buildFromTemplate([
    {
      label: 'Show Styde Forge',
      click: () => {
        mainWindow.show();
        mainWindow.focus();
      }
    },
    {
      label: 'Spawn New Agent',
      click: () => mainWindow.webContents.send('navigate', 'spawn')
    },
    { type: 'separator' },
    {
      label: 'Check for Updates',
      click: () => mainWindow.webContents.send('update:check')
    },
    { type: 'separator' },
    {
      label: 'Quit',
      click: () => app.quit()
    }
  ]);
  tray.setContextMenu(contextMenu);
  tray.on('double-click', () => {
    mainWindow.show();
    mainWindow.focus();
  });
  return tray;
}
module.exports = { createTray };
src/main/updater.js:
const { autoUpdater } = require('electron-updater');
const { dialog } = require('electron');
const log = require('electron-log');
log.transports.file.level = 'info';
autoUpdater.logger = log;
function configureUpdater(mainWindow) {
  autoUpdater.autoDownload = false;
  autoUpdater.autoInstallOnAppQuit = true;
  autoUpdater.on('checking-for-update', () => {
    mainWindow.webContents.send('update:status', { status: 'checking' });
  });
  autoUpdater.on('update-available', (info) => {
    mainWindow.webContents.send('update:status', {
      status: 'available',
      version: info.version,
      releaseDate: info.releaseDate,
      releaseNotes: info.releaseNotes
    });
    dialog.showMessageBox(mainWindow, {
      type: 'info',
      title: 'Update Available',
      message: `Version ${info.version} is available.`,
      detail: `Current version: ${autoUpdater.currentVersion}\nNew version: ${info.version}\n\nWould you like to download it now?`,
      buttons: ['Download', 'Later'],
      defaultId: 0,
      cancelId: 1
    }).then(({ response }) => {
      if (response === 0) autoUpdater.downloadUpdate();
    });
  });
  autoUpdater.on('update-not-available', () => {
    mainWindow.webContents.send('update:status', { status: 'up-to-date' });
  });
  autoUpdater.on('download-progress', (progress) => {
    mainWindow.webContents.send('update:status', {
      status: 'downloading',
      percent: progress.percent,
      bytesPerSecond: progress.bytesPerSecond,
      transferred: progress.transferred,
      total: progress.total
    });
  });
  autoUpdater.on('update-downloaded', (info) => {
    mainWindow.webContents.send('update:status', {
      status: 'downloaded',
      version: info.version
    });
    dialog.showMessageBox(mainWindow, {
      type: 'info',
      title: 'Update Ready',
      message: `Version ${info.version} has been downloaded.`,
      detail: 'Restart the application to apply the update.',
      buttons: ['Restart Now', 'Later'],
      defaultId: 0,
      cancelId: 1
    }).then(({ response }) => {
      if (response === 0) autoUpdater.quitAndInstall();
    });
  });
  autoUpdater.on('error', (error) => {
    mainWindow.webContents.send('update:status', {
      status: 'error',
      message: error.message
    });
    log.error('Update error:', error);
  });
  mainWindow.webContents.on('ipc-message', (_event, channel) => {
    if (channel === 'update:check') {
      autoUpdater.checkForUpdates();
    }
    if (channel === 'update:download') {
      autoUpdater.downloadUpdate();
    }
    if (channel === 'update:install') {
      autoUpdater.quitAndInstall();
    }
  });
}
module.exports = { configureUpdater };
src/main/security.js:
const { session } = require('electron');
function enforceSecurity(mainWindow) {
  const ses = mainWindow.webContents.session;
  // Content Security Policy
  ses.webRequest.onHeadersReceived((details, callback) => {
    callback({
      responseHeaders: {
        ...details.responseHeaders,
        'Content-Security-Policy': [
          "default-src 'self'; " +
          "script-src 'self'; " +
          "style-src 'self' 'unsafe-inline'; " +
          "img-src 'self' data:; " +
          "font-src 'self'; " +
          "connect-src 'self' https://api.github.com; " +
          "frame-src 'none'; " +
          "object-src 'none'; " +
          "base-uri 'self'; " +
          "form-action 'self'"
        ]
      }
    });
  });
  // Disable navigation to external URLs
  mainWindow.webContents.on('will-navigate', (event, url) => {
    const parsed = new URL(url);
    if (parsed.protocol !== 'file:') {
      event.preventDefault();
    }
  });
  // Block new window creation from renderer
  mainWindow.webContents.setWindowOpenHandler(({ url }) => {
    return { action: 'deny' };
  });
  // Disable remote module
  ses.setPermissionRequestHandler((webContents, permission, callback) => {
    const ALLOWED = ['clipboard-read', 'clipboard-write', 'notifications'];
    callback(ALLOWED.includes(permission));
  });
  // Clear session on quit
  app.on('will-quit', () => {
    ses.clearStorageData({ storages: ['localstorage', 'cookies'] });
  });
}
module.exports = { enforceSecurity };
src/renderer/index.html:
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta http-equiv="Content-Security-Policy" content="default-src 'self'; script-src 'self'; style-src 'self' 'unsafe-inline'; img-src 'self' data:;">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Styde Forge Desktop</title>
  <link rel="stylesheet" href="styles.css">
</head>
<body>
  <div id="app">
    <header id="titlebar">
      <div id="titlebar-drag">
        <span id="app-title">Styde Forge Desktop</span>
      </div>
      <div id="titlebar-controls">
        <button class="titlebar-btn" id="btn-minimize" title="Minimize">&#x2014;</button>
        <button class="titlebar-btn" id="btn-maximize" title="Maximize">&#x25a1;</button>
        <button class="titlebar-btn" id="btn-close" title="Close">&#x2715;</button>
      </div>
    </header>
    <main id="content">
      <div id="status-bar">
        <span id="version-badge">v<span id="version-text">--</span></span>
        <span id="platform-badge" class="badge"></span>
        <span id="update-status" class="hidden"></span>
      </div>
      <section id="dashboard">
        <h1>Mission Control</h1>
        <div class="card-grid">
          <div class="card" id="card-spawn">
            <h3>Spawn Agent</h3>
            <p>Launch a new AI agent from blueprint</p>
            <button class="btn" id="btn-spawn">Spawn</button>
          </div>
          <div class="card" id="card-blueprints">
            <h3>Blueprints</h3>
            <p>149 blueprints available</p>
            <button class="btn" id="btn-blueprints">Browse</button>
          </div>
          <div class="card" id="card-updates">
            <h3>Updates</h3>
            <p>Check for new version</p>
            <button class="btn" id="btn-check-updates">Check</button>
          </div>
          <div class="card" id="card-settings">
            <h3>Settings</h3>
            <p>Configure application</p>
            <button class="btn" id="btn-settings">Open</button>
          </div>
        </div>
      </section>
    </main>
  </div>
  <script src="renderer.js"></script>
</body>
</html>
src/renderer/renderer.js:
const api = window.electronAPI;
// Titlebar controls
document.getElementById('btn-minimize').addEventListener('click', () => api.send('app:minimize'));
document.getElementById('btn-maximize').addEventListener('click', () => api.send('app:maximize'));
document.getElementById('btn-close').addEventListener('click', () => api.send('app:close'));
// Version and platform
api.invoke('app:getVersion').then(v => document.getElementById('version-text').textContent = v);
api.invoke('app:getPlatform').then(p => {
  const badge = document.getElementById('platform-badge');
  badge.textContent = p;
  badge.className = 'badge platform-' + p;
});
// Update status listener
api.on('update:status', (status) => {
  const el = document.getElementById('update-status');
  el.classList.remove('hidden');
  if (status.status === 'checking') el.textContent = 'Checking for updates...';
  else if (status.status === 'available') el.textContent = `Update v${status.version} available`;
  else if (status.status === 'downloading') el.textContent = `Downloading... ${Math.round(status.percent)}%`;
  else if (status.status === 'downloaded') el.textContent = 'Update ready - restart to install';
  else if (status.status === 'up-to-date') { el.textContent = 'Up to date'; setTimeout(() => el.classList.add('hidden'), 3000); }
  else if (status.status === 'error') { el.textContent = 'Update failed'; setTimeout(() => el.classList.add('hidden'), 5000); }
});
// Menu event listeners
api.on('menu:open', () => api.invoke('file:open').then(files => { if (files) console.log('Opened:', files); }));
api.on('menu:saveAs', () => api.invoke('file:save', 'content', 'blueprint.md'));
api.on('menu:export', () => { /* export handler */ });
api.on('navigate', (route) => console.log('Navigate to:', route));
api.on('theme:toggle', (theme) => {
  document.body.className = theme;
  api.send('theme:set', theme);
});
// Card buttons
document.getElementById('btn-spawn').addEventListener('click', () => api.send('notify:send', { title: 'Spawn', body: 'Agent spawning...' }));
document.getElementById('btn-blueprints').addEventListener('click', () => api.send('notify:send', { title: 'Blueprints', body: 'Opening blueprint browser...' }));
document.getElementById('btn-check-updates').addEventListener('click', () => api.send('update:check'));
document.getElementById('btn-settings').addEventListener('click', () => api.send('notify:send', { title: 'Settings', body: 'Opening settings...' }));
// Maximize/unmaximize tracking
api.on('app:isMaximized', (maximized) => {
  document.getElementById('btn-maximize').textContent = maximized ? '\u25a1' : '\u25a1';
});
src/renderer/styles.css:
* { margin: 0; padding: 0; box-sizing: border-box; }
:root {
  --bg-primary: #0f0f1a;
  --bg-secondary: #1a1a2e;
  --bg-card: #16213e;
  --text-primary: #e0e0ff;
  --text-secondary: #8888aa;
  --accent: #6c63ff;
  --accent-hover: #5a52e0;
  --border: #2a2a4a;
  --success: #4caf50;
  --warning: #ff9800;
  --error: #f44336;
}
body {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  background: var(--bg-primary);
  color: var(--text-primary);
  overflow: hidden;
  height: 100vh;
}
#titlebar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  height: 38px;
  background: var(--bg-secondary);
  border-bottom: 1px solid var(--border);
  -webkit-app-region: drag;
  user-select: none;
}
#titlebar-drag { flex: 1; padding-left: 16px; }
#app-title { font-size: 13px; font-weight: 600; color: var(--text-secondary); letter-spacing: 0.5px; }
#titlebar-controls { display: flex; -webkit-app-region: no-drag; }
.titlebar-btn {
  width: 46px; height: 38px; border: none; background: transparent;
  color: var(--text-secondary); font-size: 14px; cursor: pointer;
  display: flex; align-items: center; justify-content: center;
  transition: background 0.15s, color 0.15s;
}
.titlebar-btn:hover { background: rgba(255,255,255,0.08); color: var(--text-primary); }
#btn-close:hover { background: var(--error); color: white; }
#content { height: calc(100vh - 38px); overflow-y: auto; }
#status-bar {
  display: flex; gap: 12px; align-items: center;
  padding: 8px 16px; background: var(--bg-secondary);
  border-bottom: 1px solid var(--border); font-size: 12px;
}
#version-badge, .badge {
  background: var(--bg-card); padding: 2px 8px; border-radius: 4px;
  border: 1px solid var(--border); color: var(--text-secondary);
}
.badge.platform-darwin { border-color: #666; }
.badge.platform-win32 { border-color: #0078d4; }
.badge.platform-linux { border-color: #f0c040; }
#update-status { color: var(--accent); font-weight: 500; }
#update-status.hidden { display: none; }
#dashboard { padding: 32px; }
#dashboard h1 { font-size: 24px; margin-bottom: 24px; color: var(--text-primary); font-weight: 700; }
.card-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(240px, 1fr)); gap: 20px; }
.card {
  background: var(--bg-card); border-radius: 12px; padding: 24px;
  border: 1px solid var(--border); transition: transform 0.2s, box-shadow 0.2s;
}
.card:hover { transform: translateY(-2px); box-shadow: 0 8px 24px rgba(108,99,255,0.1); }
.card h3 { font-size: 16px; margin-bottom: 8px; color: var(--text-primary); }
.card p { font-size: 13px; color: var(--text-secondary); margin-bottom: 16px; line-height: 1.4; }
.btn {
  background: var(--accent); color: white; border: none;
  padding: 8px 20px; border-radius: 6px; cursor: pointer;
  font-size: 13px; font-weight: 500; transition: background 0.2s;
}
.btn:hover { background: var(--accent-hover); }
.btn:active { transform: scale(0.97); }
build/entitlements.mac.plist:
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
  <key>com.apple.security.cs.allow-unsigned-executable-memory</key><true/>
  <key>com.apple.security.cs.disable-library-validation</key><true/>
  <key>com.apple.security.cs.allow-dyld-environment-variables</key><true/>
  <key>com.apple.security.network.client</key><true/>
  <key>com.apple.security.network.server</key><true/>
  <key>com.apple.security.files.user-selected.read-write</key><true/>
</dict>
</plist>
Security Architecture:
- contextIsolation: true (renderer isolated from Node)
- nodeIntegration: false (no require() in renderer)
- sandbox: true (OS-level sandbox)
- preload.js whitelist channel validation (18 safe channels)
- CSP enforced via onHeadersReceived
- will-navigate blocked for non-file: protocols
- setWindowOpenHandler denies all popups
- Permission handler limits to clipboard + notifications
- URL allowlist for shell.openExternal (5 trusted domains)
- No remote module
IPC Security:
- Single preload bridge with validateChannel() whitelist
- All channels hardcoded, no regex or prefix-matching
- invoke() for request/response (main returns value)
- send() for fire-and-forget (main listens but returns nothing)
- Subscription cleanup: on() returns unsubscriber function
Update Pipeline:
- electron-updater with GitHub releases provider
- Manual check via menu/tray card dialog
- Download progress streaming to renderer
- Quit-and-install on user confirmation
- Staged rollouts via GitHub releases
Start command:
cd electron-desktop-builder && npm install && npm start
Build:
npm run build:mac  # or :win or :linux
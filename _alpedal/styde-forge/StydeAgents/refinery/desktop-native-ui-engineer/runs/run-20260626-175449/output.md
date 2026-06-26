Warning: Unknown toolsets: patch, read_file, search_files
src-tauri/Cargo.toml
[package]
name = "desktop-native-ui"
version = "0.1.0"
edition = "2021"
description = "Desktop Native UI Engineer - Tauri v2 Windows components"
[lib]
name = "desktop_native_ui_lib"
crate-type = ["lib", "cdylib", "staticlib"]
[build-dependencies]
tauri-build = { version = "2", features = ["isolation"] }
[dependencies]
tauri = { version = "2", features = ["tray"] }
tauri-plugin-dialog = "2"
tauri-plugin-fs = "2"
tauri-plugin-shell = "2"
tauri-plugin-global-shortcut = "2"
tauri-plugin-notification = "2"
serde = { version = "1", features = ["derive"] }
serde_json = "1"
src-tauri/build.rs
fn main() {
    tauri_build::build()
}
src-tauri/tauri.conf.json
{
  "$schema": "https://raw.githubusercontent.com/tauri-apps/tauri/dev/crates/tauri-config-schema/schema.json",
  "productName": "Desktop Native UI",
  "version": "0.1.0",
  "identifier": "com.desktop-native-ui.engineer",
  "build": {
    "frontendDist": "../src",
    "devUrl": "http://localhost:5173",
    "beforeDevCommand": "",
    "beforeBuildCommand": ""
  },
  "app": {
    "windows": [
      {
        "title": "Desktop Native UI",
        "width": 1200,
        "height": 800,
        "minWidth": 600,
        "minHeight": 400,
        "center": true,
        "decorations": false,
        "transparent": false,
        "resizable": true,
        "maximizable": true,
        "minimizable": true,
        "closable": true,
        "dragDropEnabled": false,
        "focus": true,
        "visible": true
      }
    ],
    "security": {
      "csp": "default-src 'self'; style-src 'self' 'unsafe-inline' https://fonts.googleapis.com; font-src 'self' https://fonts.gstatic.com; img-src 'self' asset: https://asset.localhost; script-src 'self'"
    }
  },
  "bundle": {
    "active": true,
    "targets": "all",
    "icon": [
      "icons/32x32.png",
      "icons/128x128.png",
      "icons/128x128@2x.png",
      "icons/icon.icns",
      "icons/icon.ico"
    ],
    "windows": {
      "wix": null,
      "nsis": null
    }
  },
  "plugins": {
    "dialog": {
      "open": true,
      "save": true,
      "message": true,
      "ask": true,
      "confirm": true
    },
    "fs": {
      "scope": {
        "allow": [
          "$APPDATA/**",
          "$DOCUMENT/**",
          "$DESKTOP/**"
        ],
        "deny": [
          "$APPDATA/com.tauri.dev/**"
        ]
      }
    },
    "shell": {
      "open": true
    },
    "global-shortcut": {
      "all": true
    }
  }
}
src-tauri/src/lib.rs
use serde::{Deserialize, Serialize};
use std::path::PathBuf;
use tauri::{
    AppHandle, Manager, RunEvent, Window, WindowEvent,
    menu::{MenuBuilder, MenuItemBuilder, SubmenuBuilder},
    tray::TrayIconBuilder,
    image::Image,
};
use tauri_plugin_dialog::DialogExt;
use tauri_plugin_notification::NotificationExt;
#[derive(Debug, Serialize, Deserialize)]
pub struct WindowState {
    pub x: i32,
    pub y: i32,
    pub width: u32,
    pub height: u32,
    pub maximized: bool,
}
fn get_config_path(app: &AppHandle) -> Result<PathBuf, String> {
    let mut path = app
        .path()
        .app_config_dir()
        .map_err(|e| format!("Failed to get config dir: {}", e))?;
    std::fs::create_dir_all(&path)
        .map_err(|e| format!("Failed to create config dir: {}", e))?;
    path.push("windowstate.json");
    Ok(path)
}
#[tauri::command]
fn save_window_state(
    app: AppHandle,
    x: i32,
    y: i32,
    width: u32,
    height: u32,
    maximized: bool,
) -> Result<(), String> {
    let config_path = get_config_path(&app)?;
    let state = serde_json::json!({
        "x": x,
        "y": y,
        "width": width,
        "height": height,
        "maximized": maximized
    });
    let content = serde_json::to_string_pretty(&state)
        .map_err(|e| format!("Failed to serialize window state: {}", e))?;
    std::fs::write(&config_path, content)
        .map_err(|e| format!("Failed to save window state: {}", e))?;
    Ok(())
}
#[tauri::command]
fn get_window_state(app: AppHandle) -> Result<Option<WindowState>, String> {
    let config_path = get_config_path(&app)?;
    if !config_path.exists() {
        return Ok(None);
    }
    let content = std::fs::read_to_string(&config_path)
        .map_err(|e| format!("Failed to read window state: {}", e))?;
    serde_json::from_str(&content)
        .map(Some)
        .map_err(|e| format!("Failed to parse window state: {}", e))
}
#[tauri::command]
fn minimize_to_tray(window: Window) -> Result<(), String> {
    window
        .hide()
        .map_err(|e| format!("Failed to hide window: {}", e))
}
#[tauri::command]
fn show_notification(app: AppHandle, title: String, body: String) -> Result<(), String> {
    app.notification()
        .builder()
        .title(&title)
        .body(&body)
        .show()
        .map_err(|e| format!("Failed to show notification: {}", e))
}
#[tauri::command]
fn open_file_dialog(app: AppHandle) -> Result<Option<String>, String> {
    let file = app
        .dialog()
        .file()
        .add_filter("All Files", &["*"])
        .set_file_name("")
        .blocking_pick_file();
    Ok(file.map(|f| f.to_string()))
}
#[tauri::command]
fn save_file_dialog(app: AppHandle, default_name: String) -> Result<Option<String>, String> {
    let file = app
        .dialog()
        .file()
        .add_filter("All Files", &["*"])
        .set_file_name(&default_name)
        .blocking_save_file();
    Ok(file.map(|f| f.to_string()))
}
#[tauri::command]
fn show_message(app: AppHandle, kind: String, title: String, message: String) -> Result<(), String> {
    match kind.as_str() {
        "info" => app.dialog().message(&message).title(&title).kind(tauri_plugin_dialog::MessageDialogKind::Info).blocking_show(),
        "warning" => app.dialog().message(&message).title(&title).kind(tauri_plugin_dialog::MessageDialogKind::Warning).blocking_show(),
        "error" => app.dialog().message(&message).title(&title).kind(tauri_plugin_dialog::MessageDialogKind::Error).blocking_show(),
        _ => app.dialog().message(&message).title(&title).blocking_show(),
    }
    Ok(())
}
#[tauri::command]
fn confirm_dialog(app: AppHandle, title: String, message: String) -> Result<bool, String> {
    let result = app
        .dialog()
        .message(&message)
        .title(&title)
        .kind(tauri_plugin_dialog::MessageDialogKind::Question)
        .blocking_confirm();
    Ok(result)
}
#[tauri::command]
fn get_monitors(app: AppHandle) -> Result<Vec<serde_json::Value>, String> {
    let monitors = app
        .available_monitors()
        .map_err(|e| format!("Failed to get monitors: {}", e))?;
    let mut result = Vec::new();
    for monitor in monitors {
        let scale = monitor.scale_factor();
        let size = monitor.size();
        let position = monitor.position();
        let name = monitor.name().unwrap_or_else(|| "Unknown".to_string());
        result.push(serde_json::json!({
            "name": name,
            "scaleFactor": scale,
            "width": size.width,
            "height": size.height,
            "x": position.x,
            "y": position.y,
            "isPrimary": monitor.is_primary()
        }));
    }
    Ok(result)
}
#[tauri::command]
fn move_to_monitor(window: Window, monitor_index: usize) -> Result<(), String> {
    let monitors = window
        .available_monitors()
        .map_err(|e| format!("Failed to get monitors: {}", e))?;
    if monitor_index >= monitors.len() {
        return Err(format!("Monitor index {} out of range (0-{})", monitor_index, monitors.len() - 1));
    }
    let target = &monitors[monitor_index];
    let pos = target.position();
    window
        .set_position(tauri::PhysicalPosition::new(pos.x, pos.y))
        .map_err(|e| format!("Failed to move window: {}", e))?;
    Ok(())
}
fn setup_tray(app: &AppHandle) -> Result<(), Box<dyn std::error::Error>> {
    let show_item = MenuItemBuilder::with_id("show", "Show Window")
        .accelerator("CmdOrCtrl+Shift+T")
        .build(app)?;
    let hide_item = MenuItemBuilder::with_id("hide", "Hide Window")
        .accelerator("CmdOrCtrl+H")
        .build(app)?;
    let separator = tauri::menu::PredefinedMenuItem::separator(app)?;
    let quit_item = MenuItemBuilder::with_id("quit", "Quit")
        .accelerator("CmdOrCtrl+Q")
        .build(app)?;
    let menu = MenuBuilder::new(app)
        .item(&show_item)
        .item(&hide_item)
        .item(&separator)
        .item(&quit_item)
        .build()?;
    let icon_path = app
        .path()
        .resource_dir()
        .map_err(|e| format!("Failed to get resource dir: {}", e))?
        .join("icons")
        .join("icon.ico");
    let icon = if icon_path.exists() {
        Image::from_path(&icon_path)
            .map_err(|e| format!("Failed to load tray icon: {}", e))?
    } else {
        let icon_bytes = include_bytes!("../icons/icon.png");
        Image::from_bytes(icon_bytes)
            .map_err(|e| format!("Failed to load embedded icon: {}", e))?
    };
    let tray = TrayIconBuilder::new()
        .icon(icon)
        .menu(&menu)
        .tooltip("Desktop Native UI")
        .on_menu_event(move |app, event| {
            match event.id().as_ref() {
                "show" => {
                    if let Some(window) = app.get_webview_window("main") {
                        let _ = window.show();
                        let _ = window.set_focus();
                    }
                }
                "hide" => {
                    if let Some(window) = app.get_webview_window("main") {
                        let _ = window.hide();
                    }
                }
                "quit" => {
                    app.exit(0);
                }
                _ => {}
            }
        })
        .build(app)?;
    app.manage(tray);
    Ok(())
}
fn retry<T, F>(mut f: F, max_attempts: usize) -> Result<T, String>
where
    F: FnMut() -> Result<T, String>,
{
    let delays = [100u64, 500, 2000];
    let mut last_err = String::from("Unknown error");
    for attempt in 0..max_attempts {
        match f() {
            Ok(val) => return Ok(val),
            Err(e) => {
                last_err = e;
                if attempt < max_attempts - 1 {
                    let delay = delays[attempt.min(delays.len() - 1)];
                    std::thread::sleep(std::time::Duration::from_millis(delay));
                }
            }
        }
    }
    Err(format!("Operation failed after {} attempts: {}", max_attempts, last_err))
}
#[cfg_attr(mobile, tauri::mobile_entry_point)]
pub fn run() {
    tauri::Builder::default()
        .plugin(tauri_plugin_dialog::init())
        .plugin(tauri_plugin_fs::init())
        .plugin(tauri_plugin_shell::init())
        .plugin(tauri_plugin_global_shortcut::Builder::new().build())
        .plugin(tauri_plugin_notification::init())
        .setup(|app| {
            let _ = setup_tray(app.handle());
            let _ = app.handle().plugin(
                tauri_plugin_global_shortcut::Builder::new()
                    .with_handler(move |_app, shortcut, event| {
                        if event == tauri_plugin_global_shortcut::ShortcutEvent::Pressed {
                            let shortcut_str = shortcut.to_string();
                            match shortcut_str.as_str() {
                                "CmdOrCtrl+Shift+T" | "Win+Shift+T" => {
                                    if let Some(window) = _app.get_webview_window("main") {
                                        let _ = window.show();
                                        let _ = window.set_focus();
                                    }
                                }
                                _ => {}
                            }
                        }
                    })
                    .build(),
            );
            let _ = app.handle().global_shortcut().register("Win+Shift+T");
            if let Some(window) = app.get_webview_window("main") {
                let handle = app.handle().clone();
                window.on_window_event(move |event| {
                    match event {
                        WindowEvent::CloseRequested { api, .. } => {
                            api.prevent_close();
                            if let Some(win) = handle.get_webview_window("main") {
                                let _ = win.hide();
                                let _ = handle.emit("window-hidden", ());
                            }
                        }
                        WindowEvent::Resized(size) => {
                            let _ = handle.emit("window-resized", serde_json::json!({
                                "width": size.width,
                                "height": size.height
                            }));
                        }
                        WindowEvent::Moved(position) => {
                            let _ = handle.emit("window-moved", serde_json::json!({
                                "x": position.x,
                                "y": position.y
                            }));
                        }
                        WindowEvent::ScaleFactorChanged { scale_factor, .. } => {
                            let _ = handle.emit("scale-factor-changed", serde_json::json!({
                                "scaleFactor": scale_factor
                            }));
                        }
                        WindowEvent::Focused(focused) => {
                            let _ = handle.emit("window-focus-changed", serde_json::json!({
                                "focused": focused
                            }));
                        }
                        _ => {}
                    }
                });
            }
            Ok(())
        })
        .invoke_handler(tauri::generate_handler![
            save_window_state,
            get_window_state,
            minimize_to_tray,
            show_notification,
            open_file_dialog,
            save_file_dialog,
            show_message,
            confirm_dialog,
            get_monitors,
            move_to_monitor,
        ])
        .build(tauri::generate_context!())
        .expect("Failed to build Tauri application")
        .run(|app_handle, event| {
            if let RunEvent::ExitRequested { api, .. } = event {
                api.prevent_exit();
            }
        });
}
src-tauri/src/main.rs
#![cfg_attr(not(debug_assertions), windows_subsystem = "windows")]
fn main() {
    desktop_native_ui_lib::run()
}
src-tauri/capabilities/default.json
{
  "identifier": "default-capability",
  "description": "Default capability set for the main window",
  "windows": ["main"],
  "permissions": [
    "core:default",
    "core:window:default",
    "core:window:allow-close",
    "core:window:allow-hide",
    "core:window:allow-show",
    "core:window:allow-set-focus",
    "core:window:allow-set-position",
    "core:window:allow-set-size",
    "core:window:allow-minimize",
    "core:window:allow-maximize",
    "core:window:allow-unmaximize",
    "core:window:allow-toggle-maximize",
    "core:window:allow-start-dragging",
    "core:window:allow-available-monitors",
    "core:window:allow-primary-monitor",
    "core:window:allow-current-monitor",
    "core:window:allow-is-maximized",
    "core:window:allow-is-minimized",
    "core:window:allow-is-visible",
    "core:window:allow-inner-size",
    "core:window:allow-outer-size",
    "core:window:allow-center",
    "core:window:allow-set-fullscreen",
    "core:event:default",
    "core:event:allow-listen",
    "core:event:allow-emit",
    "core:event:allow-emit-to",
    "path:default",
    "dialog:default",
    "dialog:allow-open",
    "dialog:allow-save",
    "dialog:allow-message",
    "dialog:allow-ask",
    "dialog:allow-confirm",
    "fs:default",
    "fs:allow-read",
    "fs:allow-write",
    "fs:allow-exists",
    "fs:allow-mkdir",
    "fs:allow-remove",
    "fs:allow-rename",
    "fs:allow-stat",
    "fs:scope-app-recursive",
    "shell:default",
    "shell:allow-open",
    "global-shortcut:default",
    "global-shortcut:allow-register",
    "global-shortcut:allow-unregister",
    "global-shortcut:allow-is-registered",
    "notification:default",
    "notification:allow-notify",
    "notification:allow-is-permission-granted",
    "notification:allow-request-permission"
  ]
}
src/index.html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Desktop Native UI</title>
  <link rel="stylesheet" href="style.css" />
  <script type="module" src="app.js"></script>
</head>
<body>
  <div data-tauri-drag-region class="titlebar" id="titlebar">
    <div class="titlebar-drag" data-tauri-drag-region>
      <span class="titlebar-icon">&#xE801;</span>
      <span class="titlebar-text">Desktop Native UI</span>
    </div>
    <div class="titlebar-controls">
      <button class="titlebar-btn minimize-btn" id="minimize-btn" aria-label="Minimize" title="Minimize">
        <svg width="12" height="12" viewBox="0 0 12 12">
          <rect x="1" y="5.5" width="10" height="1" fill="currentColor"/>
        </svg>
      </button>
      <button class="titlebar-btn maximize-btn" id="maximize-btn" aria-label="Maximize" title="Maximize">
        <svg width="12" height="12" viewBox="0 0 12 12">
          <rect x="1.5" y="1.5" width="9" height="9" rx="1" fill="none" stroke="currentColor" stroke-width="1.2"/>
        </svg>
      </button>
      <button class="titlebar-btn close-btn" id="close-btn" aria-label="Close" title="Close">
        <svg width="12" height="12" viewBox="0 0 12 12">
          <line x1="2" y1="2" x2="10" y2="10" stroke="currentColor" stroke-width="1.5"/>
          <line x1="10" y1="2" x2="2" y2="10" stroke="currentColor" stroke-width="1.5"/>
        </svg>
      </button>
    </div>
  </div>
  <div class="app-container">
    <aside class="sidebar">
      <nav class="sidebar-nav" role="navigation" aria-label="Main navigation">
        <button class="nav-item active" data-view="dashboard" aria-current="page">
          <span class="nav-icon">&#xE80F;</span>
          <span class="nav-label">Dashboard</span>
        </button>
        <button class="nav-item" data-view="files">
          <span class="nav-icon">&#xE838;</span>
          <span class="nav-label">Files</span>
        </button>
        <button class="nav-item" data-view="monitors">
          <span class="nav-icon">&#xE770;</span>
          <span class="nav-label">Monitors</span>
        </button>
        <button class="nav-item" data-view="shortcuts">
          <span class="nav-icon">&#xE771;</span>
          <span class="nav-label">Shortcuts</span>
        </button>
        <button class="nav-item" data-view="dialogs">
          <span class="nav-icon">&#xE8BD;</span>
          <span class="nav-label">Dialogs</span>
        </button>
      </nav>
      <div class="sidebar-footer">
        <div class="tray-status" id="tray-status">
          <span class="tray-indicator"></span>
          <span>Tray Active</span>
        </div>
      </div>
    </aside>
    <main class="content" id="main-content">
      <div class="view" id="view-dashboard">
        <h1 class="view-title">Dashboard</h1>
        <div class="dashboard-grid">
          <div class="card window-card">
            <div class="card-header">
              <h2>Window</h2>
              <span class="card-icon">&#xE8A7;</span>
            </div>
            <div class="card-body">
              <div class="stat-row">
                <span class="stat-label">Position</span>
                <span class="stat-value" id="stat-position">--</span>
              </div>
              <div class="stat-row">
                <span class="stat-label">Size</span>
                <span class="stat-value" id="stat-size">--</span>
              </div>
              <div class="stat-row">
                <span class="stat-label">Focus</span>
                <span class="stat-value" id="stat-focus">--</span>
              </div>
              <div class="stat-row">
                <span class="stat-label">DPI Scale</span>
                <span class="stat-value" id="stat-dpi">--</span>
              </div>
            </div>
          </div>
          <div class="card tray-card">
            <div class="card-header">
              <h2>System Tray</h2>
              <span class="card-icon">&#xE7F4;</span>
            </div>
            <div class="card-body">
              <p>Minimize to tray on close. Right-click tray icon for menu.</p>
              <button class="btn btn-primary" id="minimize-tray-btn">Minimize to Tray</button>
            </div>
          </div>
          <div class="card notify-card">
            <div class="card-header">
              <h2>Notifications</h2>
              <span class="card-icon">&#xEA17;</span>
            </div>
            <div class="card-body">
              <div class="input-group">
                <input type="text" id="notif-title" class="input" placeholder="Notification title" value="Desktop Native UI" />
                <input type="text" id="notif-body" class="input" placeholder="Notification body" value="Hello from your desktop app!" />
                <button class="btn btn-primary" id="send-notif-btn">Send Notification</button>
              </div>
            </div>
          </div>
          <div class="card state-card">
            <div class="card-header">
              <h2>Window State</h2>
              <span class="card-icon">&#xE943;</span>
            </div>
            <div class="card-body">
              <p>Window position and size are persisted automatically.</p>
              <div class="state-preview" id="state-preview">No saved state</div>
              <button class="btn btn-secondary" id="save-state-btn">Save Current State</button>
              <button class="btn btn-secondary" id="load-state-btn">Load Saved State</button>
            </div>
          </div>
        </div>
      </div>
      <div class="view hidden" id="view-files">
        <h1 class="view-title">File Dialogs</h1>
        <div class="card">
          <div class="card-header">
            <h2>Open & Save</h2>
            <span class="card-icon">&#xE838;</span>
          </div>
          <div class="card-body">
            <button class="btn btn-primary" id="open-file-btn">Open File...</button>
            <button class="btn btn-primary" id="save-file-btn">Save File As...</button>
            <div class="file-result" id="file-result">No file selected</div>
          </div>
        </div>
        <div class="card">
          <div class="card-header">
            <h2>Message Boxes</h2>
            <span class="card-icon">&#xE8BD;</span>
          </div>
          <div class="card-body">
            <div class="btn-group">
              <button class="btn btn-info" id="msg-info">Info</button>
              <button class="btn btn-warning" id="msg-warning">Warning</button>
              <button class="btn btn-danger" id="msg-error">Error</button>
              <button class="btn btn-secondary" id="msg-confirm">Confirm</button>
            </div>
          </div>
        </div>
      </div>
      <div class="view hidden" id="view-monitors">
        <h1 class="view-title">Multi-Monitor</h1>
        <div class="card">
          <div class="card-header">
            <h2>Available Monitors</h2>
            <span class="card-icon">&#xE770;</span>
          </div>
          <div class="card-body">
            <div id="monitor-list">
              <p class="loading">Loading monitors...</p>
            </div>
            <div class="btn-group">
              <button class="btn btn-primary" id="move-monitor-btn" disabled>Move Window to Selected Monitor</button>
              <button class="btn btn-secondary" id="refresh-monitors-btn">Refresh</button>
            </div>
          </div>
        </div>
      </div>
      <div class="view hidden" id="view-shortcuts">
        <h1 class="view-title">Keyboard Shortcuts</h1>
        <div class="shortcuts-list">
          <div class="shortcut-item">
            <span class="shortcut-action">Show Window</span>
            <kbd class="shortcut-keys">Ctrl+Shift+T</kbd>
          </div>
          <div class="shortcut-item">
            <span class="shortcut-action">Hide Window</span>
            <kbd class="shortcut-keys">Ctrl+H</kbd>
          </div>
          <div class="shortcut-item">
            <span class="shortcut-action">Global Show</span>
            <kbd class="shortcut-keys">Win+Shift+T</kbd>
          </div>
          <div class="shortcut-item">
            <span class="shortcut-action">Open File</span>
            <kbd class="shortcut-keys">Ctrl+O</kbd>
          </div>
          <div class="shortcut-item">
            <span class="shortcut-action">Save File</span>
            <kbd class="shortcut-keys">Ctrl+S</kbd>
          </div>
          <div class="shortcut-item">
            <span class="shortcut-action">Quit App</span>
            <kbd class="shortcut-keys">Ctrl+Q</kbd>
          </div>
          <div class="shortcut-item">
            <span class="shortcut-action">Navigate Views</span>
            <kbd class="shortcut-keys">1-5</kbd>
          </div>
        </div>
      </div>
      <div class="view hidden" id="view-dialogs">
        <h1 class="view-title">Native Dialogs</h1>
        <div class="card">
          <div class="card-header">
            <h2>Dialog Examples</h2>
            <span class="card-icon">&#xE8BD;</span>
          </div>
          <div class="card-body">
            <button class="btn btn-primary" id="dlg-question">Show Question Dialog</button>
            <button class="btn btn-danger" id="dlg-destructive">Destructive Action Confirmation</button>
            <div class="dialog-result" id="dialog-result">Dialog result will appear here</div>
          </div>
        </div>
      </div>
    </main>
  </div>
  <div class="toast-container" id="toast-container" role="status" aria-live="polite"></div>
  <dialog class="native-dialog" id="confirm-dialog">
    <div class="dialog-content">
      <h2 class="dialog-title">Confirm</h2>
      <p class="dialog-message" id="confirm-message">Are you sure?</p>
      <div class="dialog-actions">
        <button class="btn btn-secondary" id="confirm-cancel">Cancel</button>
        <button class="btn btn-primary" id="confirm-ok">OK</button>
      </div>
    </div>
  </dialog>
</body>
</html>
src/style.css
:root {
  --system-accent: #60cdff;
  --system-accent-dark: #0078d4;
  --system-accent-light: #9ad8ff;
  --bg-primary: #1c1c1c;
  --bg-secondary: #252525;
  --bg-tertiary: #323232;
  --bg-card: #2a2a2a;
  --bg-hover: #3a3a3a;
  --bg-active: #404040;
  --text-primary: #ffffff;
  --text-secondary: #b0b0b0;
  --text-tertiary: #707070;
  --border-color: #404040;
  --border-hover: #505050;
  --danger: #e74856;
  --danger-hover: #c73a4a;
  --warning: #ffb900;
  --warning-hover: #d9a000;
  --info: #0078d4;
  --info-hover: #006cbd;
  --success: #52c41a;
  --shadow-sm: 0 1px 3px rgba(0,0,0,0.3);
  --shadow-md: 0 4px 12px rgba(0,0,0,0.4);
  --shadow-lg: 0 8px 24px rgba(0,0,0,0.5);
  --radius-sm: 4px;
  --radius-md: 8px;
  --radius-lg: 12px;
  --transition-fast: 120ms ease;
  --transition-normal: 200ms ease;
  --font-ui: "Segoe UI Variable", "Segoe UI", system-ui, -apple-system, sans-serif;
  --titlebar-height: 40px;
  --sidebar-width: 220px;
}
*, *::before, *::after {
  box-sizing: border-box;
  margin: 0;
  padding: 0;
}
html, body {
  width: 100%;
  height: 100%;
  overflow: hidden;
  font-family: var(--font-ui);
  font-size: 14px;
  color: var(--text-primary);
  background: var(--bg-primary);
  user-select: none;
  -webkit-user-select: none;
}
.titlebar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  height: var(--titlebar-height);
  background: var(--bg-secondary);
  border-bottom: 1px solid var(--border-color);
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  z-index: 1000;
}
.titlebar-drag {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 0 12px;
  height: 100%;
  flex: 1;
  -webkit-app-region: drag;
  app-region: drag;
}
.titlebar-icon {
  font-size: 18px;
  color: var(--system-accent);
  line-height: 1;
}
.titlebar-text {
  font-size: 12px;
  font-weight: 500;
  color: var(--text-secondary);
  letter-spacing: 0.3px;
}
.titlebar-controls {
  display: flex;
  height: 100%;
  -webkit-app-region: no-drag;
  app-region: no-drag;
}
.titlebar-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 48px;
  height: 100%;
  border: none;
  background: transparent;
  color: var(--text-secondary);
  cursor: pointer;
  transition: background var(--transition-fast), color var(--transition-fast);
  position: relative;
}
.titlebar-btn:hover {
  background: var(--bg-hover);
  color: var(--text-primary);
}
.titlebar-btn:active {
  background: var(--bg-active);
}
.titlebar-btn:focus-visible {
  outline: 2px solid var(--system-accent);
  outline-offset: -2px;
}
.minimize-btn:hover {
  background: var(--bg-hover);
}
.maximize-btn:hover {
  background: var(--bg-hover);
}
.close-btn:hover {
  background: var(--danger);
  color: white;
}
.app-container {
  display: flex;
  height: calc(100vh - var(--titlebar-height));
  margin-top: var(--titlebar-height);
}
.sidebar {
  width: var(--sidebar-width);
  background: var(--bg-secondary);
  border-right: 1px solid var(--border-color);
  display: flex;
  flex-direction: column;
  flex-shrink: 0;
}
.sidebar-nav {
  display: flex;
  flex-direction: column;
  padding: 8px;
  gap: 2px;
  flex: 1;
}
.nav-item {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 10px 12px;
  border: none;
  background: transparent;
  color: var(--text-secondary);
  font-size: 14px;
  cursor: pointer;
  border-radius: var(--radius-sm);
  transition: background var(--transition-fast), color var(--transition-fast);
  text-align: left;
  width: 100%;
}
.nav-item:hover {
  background: var(--bg-hover);
  color: var(--text-primary);
}
.nav-item:active {
  background: var(--bg-active);
}
.nav-item:focus-visible {
  outline: 2px solid var(--system-accent);
  outline-offset: 2px;
}
.nav-item.active {
  background: rgba(96, 205, 255, 0.15);
  color: var(--system-accent);
}
.nav-icon {
  font-size: 16px;
  width: 20px;
  text-align: center;
  line-height: 1;
}
.sidebar-footer {
  padding: 12px;
  border-top: 1px solid var(--border-color);
}
.tray-status {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 12px;
  color: var(--text-secondary);
}
.tray-indicator {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: var(--success);
  box-shadow: 0 0 6px rgba(82, 196, 26, 0.5);
}
.content {
  flex: 1;
  padding: 24px;
  overflow-y: auto;
  background: var(--bg-primary);
}
.view-title {
  font-size: 24px;
  font-weight: 600;
  margin-bottom: 20px;
  color: var(--text-primary);
}
.view {
  animation: fadeIn var(--transition-normal) ease;
}
@keyframes fadeIn {
  from { opacity: 0; transform: translateY(4px); }
  to { opacity: 1; transform: translateY(0); }
}
.hidden {
  display: none !important;
}
.dashboard-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
  gap: 16px;
}
.card {
  background: var(--bg-card);
  border: 1px solid var(--border-color);
  border-radius: var(--radius-md);
  overflow: hidden;
  transition: border-color var(--transition-fast), box-shadow var(--transition-fast);
}
.card:hover {
  border-color: var(--border-hover);
  box-shadow: var(--shadow-sm);
}
.card-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 14px 16px;
  border-bottom: 1px solid var(--border-color);
}
.card-header h2 {
  font-size: 14px;
  font-weight: 600;
  color: var(--text-primary);
}
.card-icon {
  font-size: 20px;
  color: var(--text-tertiary);
}
.card-body {
  padding: 16px;
  display: flex;
  flex-direction: column;
  gap: 10px;
}
.stat-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 6px 0;
}
.stat-label {
  color: var(--text-secondary);
  font-size: 13px;
}
.stat-value {
  color: var(--text-primary);
  font-size: 13px;
  font-weight: 500;
  font-variant-numeric: tabular-nums;
}
.btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 6px;
  padding: 8px 16px;
  border: 1px solid var(--border-color);
  background: var(--bg-tertiary);
  color: var(--text-primary);
  font-size: 13px;
  font-family: var(--font-ui);
  border-radius: var(--radius-sm);
  cursor: pointer;
  transition: background var(--transition-fast), border-color var(--transition-fast), box-shadow var(--transition-fast);
  white-space: nowrap;
}
.btn:hover {
  background: var(--bg-hover);
  border-color: var(--border-hover);
}
.btn:active {
  background: var(--bg-active);
}
.btn:focus-visible {
  outline: 2px solid var(--system-accent);
  outline-offset: 2px;
}
.btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}
.btn-primary {
  background: var(--system-accent-dark);
  border-color: var(--system-accent-dark);
  color: white;
}
.btn-primary:hover {
  background: #1a8ad4;
  border-color: #1a8ad4;
}
.btn-primary:active {
  background: #0062a0;
}
.btn-secondary {
  background: var(--bg-tertiary);
  border-color: var(--border-color);
}
.btn-info {
  background: var(--info);
  border-color: var(--info);
  color: white;
}
.btn-info:hover {
  background: var(--info-hover);
}
.btn-warning {
  background: var(--warning);
  border-color: var(--warning);
  color: #1c1c1c;
}
.btn-warning:hover {
  background: var(--warning-hover);
}
.btn-danger {
  background: var(--danger);
  border-color: var(--danger);
  color: white;
}
.btn-danger:hover {
  background: var(--danger-hover);
}
.btn-group {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
}
.input {
  width: 100%;
  padding: 8px 12px;
  border: 1px solid var(--border-color);
  border-radius: var(--radius-sm);
  background: var(--bg-tertiary);
  color: var(--text-primary);
  font-size: 13px;
  font-family: var(--font-ui);
  transition: border-color var(--transition-fast);
}
.input:focus {
  outline: none;
  border-color: var(--system-accent);
  box-shadow: 0 0 0 1px var(--system-accent);
}
.input::placeholder {
  color: var(--text-tertiary);
}
.input-group {
  display: flex;
  flex-direction: column;
  gap: 8px;
}
.file-result, .dialog-result, .state-preview {
  padding: 10px 12px;
  background: var(--bg-tertiary);
  border-radius: var(--radius-sm);
  font-size: 12px;
  color: var(--text-secondary);
  word-break: break-all;
  min-height: 38px;
  display: flex;
  align-items: center;
}
.shortcuts-list {
  display: flex;
  flex-direction: column;
  gap: 4px;
}
.shortcut-item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 12px 16px;
  background: var(--bg-card);
  border: 1px solid var(--border-color);
  border-radius: var(--radius-sm);
}
.shortcut-action {
  color: var(--text-primary);
  font-size: 14px;
}
.shortcut-keys {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  padding: 4px 8px;
  background: var(--bg-tertiary);
  border: 1px solid var(--border-color);
  border-radius: var(--radius-sm);
  font-family: "Cascadia Code", "Segoe UI", monospace;
  font-size: 12px;
  color: var(--text-secondary);
}
.loading {
  color: var(--text-tertiary);
  font-style: italic;
}
.monitor-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px 16px;
  background: var(--bg-tertiary);
  border: 1px solid var(--border-color);
  border-radius: var(--radius-sm);
  margin-bottom: 8px;
  transition: border-color var(--transition-fast);
}
.monitor-item.selected {
  border-color: var(--system-accent);
}
.monitor-item label {
  display: flex;
  align-items: center;
  gap: 12px;
  cursor: pointer;
  width: 100%;
}
.monitor-item input[type="radio"] {
  accent-color: var(--system-accent);
  width: 16px;
  height: 16px;
  cursor: pointer;
}
.monitor-name {
  font-weight: 500;
  color: var(--text-primary);
}
.monitor-details {
  color: var(--text-secondary);
  font-size: 12px;
}
.monitor-badge {
  padding: 2px 8px;
  border-radius: 10px;
  font-size: 11px;
  background: var(--system-accent-dark);
  color: white;
  font-weight: 500;
}
.toast-container {
  position: fixed;
  bottom: 20px;
  right: 20px;
  display: flex;
  flex-direction: column;
  gap: 8px;
  z-index: 9999;
  pointer-events: none;
}
.toast {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 12px 16px;
  background: var(--bg-secondary);
  border: 1px solid var(--border-color);
  border-radius: var(--radius-sm);
  box-shadow: var(--shadow-md);
  font-size: 13px;
  color: var(--text-primary);
  animation: toastIn 300ms ease;
  pointer-events: auto;
  max-width: 360px;
}
.toast.success { border-left: 3px solid var(--success); }
.toast.error { border-left: 3px solid var(--danger); }
.toast.info { border-left: 3px solid var(--info); }
@keyframes toastIn {
  from { opacity: 0; transform: translateX(20px); }
  to { opacity: 1; transform: translateX(0); }
}
.native-dialog {
  border: none;
  border-radius: var(--radius-md);
  padding: 0;
  background: var(--bg-secondary);
  box-shadow: var(--shadow-lg);
  min-width: 320px;
  max-width: 480px;
  color: var(--text-primary);
}
.native-dialog::backdrop {
  background: rgba(0, 0, 0, 0.5);
  backdrop-filter: blur(4px);
}
.dialog-content {
  padding: 24px;
}
.dialog-title {
  font-size: 18px;
  font-weight: 600;
  margin-bottom: 12px;
}
.dialog-message {
  color: var(--text-secondary);
  font-size: 14px;
  line-height: 1.5;
  margin-bottom: 20px;
}
.dialog-actions {
  display: flex;
  justify-content: flex-end;
  gap: 8px;
}
::-webkit-scrollbar {
  width: 8px;
  height: 8px;
}
::-webkit-scrollbar-track {
  background: transparent;
}
::-webkit-scrollbar-thumb {
  background: var(--border-color);
  border-radius: 4px;
}
::-webkit-scrollbar-thumb:hover {
  background: var(--border-hover);
}
@media (forced-colors: active) {
  .nav-item.active {
    outline: 2px solid Highlight;
  }
  .titlebar-btn:focus-visible,
  .nav-item:focus-visible,
  .btn:focus-visible {
    outline: 2px solid Highlight;
  }
}
@media (max-width: 768px) {
  .sidebar {
    width: 56px;
  }
  .nav-label {
    display: none;
  }
  .dashboard-grid {
    grid-template-columns: 1fr;
  }
}
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 0.01ms !important;
    transition-duration: 0.01ms !important;
  }
}
src/app.js
import { invoke } from '@tauri-apps/api/core';
import { listen } from '@tauri-apps/api/event';
import { getCurrentWindow, LogicalSize, LogicalPosition } from '@tauri-apps/api/window';
const appWindow = getCurrentWindow();
let windowState = {
  x: 0, y: 0, width: 1200, height: 800, maximized: false, focused: true, scaleFactor: 1
};
async function initApp() {
  await loadSavedState();
  registerEventListeners();
  registerTitlebarHandlers();
  registerNavHandlers();
  registerButtonHandlers();
  registerKeyboardShortcuts();
  updateStats();
}
async function loadSavedState() {
  try {
    const state = await invoke('get_window_state');
    if (state) {
      windowState = { ...windowState, ...state };
      const preview = document.getElementById('state-preview');
      if (preview) {
        preview.textContent = `Restored: x=${state.x}, y=${state.y}, ${state.width}x${state.height}${state.maximized ? ', maximized' : ''}`;
      }
    }
  } catch (err) {
    console.warn('No saved window state:', err);
  }
}
function registerEventListeners() {
  listen('window-resized', (event) => {
    windowState.width = event.payload.width;
    windowState.height = event.payload.height;
    updateStats();
  });
  listen('window-moved', (event) => {
    windowState.x = event.payload.x;
    windowState.y = event.payload.y;
    updateStats();
  });
  listen('window-focus-changed', (event) => {
    windowState.focused = event.payload.focused;
    updateStats();
  });
  listen('scale-factor-changed', (event) => {
    windowState.scaleFactor = event.payload.scaleFactor;
    updateStats();
  });
  listen('window-hidden', () => {
    showToast('Window minimized to tray', 'info');
  });
}
function registerTitlebarHandlers() {
  document.getElementById('minimize-btn').addEventListener('click', async () => {
    try { await appWindow.minimize(); } catch (e) { console.error(e); }
  });
  document.getElementById('maximize-btn').addEventListener('click', async () => {
    try {
      const maximized = await appWindow.isMaximized();
      if (maximized) {
        await appWindow.unmaximize();
      } else {
        await appWindow.maximize();
      }
    } catch (e) { console.error(e); }
  });
  document.getElementById('close-btn').addEventListener('click', async () => {
    try {
      await invoke('minimize_to_tray');
      showToast('App minimized to system tray', 'info');
    } catch (e) { console.error(e); }
  });
}
function registerNavHandlers() {
  document.querySelectorAll('.nav-item').forEach(item => {
    item.addEventListener('click', () => {
      document.querySelectorAll('.nav-item').forEach(n => n.classList.remove('active'));
      item.classList.add('active');
      document.querySelectorAll('.view').forEach(v => v.classList.add('hidden'));
      const viewId = `view-${item.dataset.view}`;
      const targetView = document.getElementById(viewId);
      if (targetView) {
        targetView.classList.remove('hidden');
        targetView.style.animation = 'none';
        requestAnimationFrame(() => {
          targetView.style.animation = '';
        });
      }
      if (item.dataset.view === 'monitors') loadMonitors();
    });
  });
}
function registerButtonHandlers() {
  document.getElementById('minimize-tray-btn')?.addEventListener('click', async () => {
    try {
      await invoke('minimize_to_tray');
      showToast('Minimized to system tray', 'info');
    } catch (e) { showToast('Failed to minimize: ' + e, 'error'); }
  });
  document.getElementById('send-notif-btn')?.addEventListener('click', async () => {
    const title = document.getElementById('notif-title').value || 'Desktop Native UI';
    const body = document.getElementById('notif-body').value || 'Hello!';
    try {
      await invoke('show_notification', { title, body });
      showToast('Notification sent', 'success');
    } catch (e) { showToast('Notification failed: ' + e, 'error'); }
  });
  document.getElementById('save-state-btn')?.addEventListener('click', async () => {
    await saveWindowState();
    showToast('Window state saved', 'success');
  });
  document.getElementById('load-state-btn')?.addEventListener('click', async () => {
    await loadSavedState();
    showToast('Window state loaded', 'info');
  });
  document.getElementById('open-file-btn')?.addEventListener('click', async () => {
    try {
      const path = await invoke('open_file_dialog');
      const result = document.getElementById('file-result');
      if (result) result.textContent = path || 'Cancelled';
    } catch (e) { showToast('Failed to open file: ' + e, 'error'); }
  });
  document.getElementById('save-file-btn')?.addEventListener('click', async () => {
    try {
      const path = await invoke('save_file_dialog', { defaultName: 'untitled.txt' });
      const result = document.getElementById('file-result');
      if (result) result.textContent = path || 'Cancelled';
    } catch (e) { showToast('Failed to save file: ' + e, 'error'); }
  });
  const msgButtons = {
    'msg-info': { kind: 'info', title: 'Information', message: 'This is an informational message.' },
    'msg-warning': { kind: 'warning', title: 'Warning', message: 'This is a warning message.' },
    'msg-error': { kind: 'error', title: 'Error', message: 'An error has occurred.' },
  };
  Object.entries(msgButtons).forEach(([id, opts]) => {
    document.getElementById(id)?.addEventListener('click', async () => {
      try {
        await invoke('show_message', opts);
      } catch (e) { console.error(e); }
    });
  });
  document.getElementById('msg-confirm')?.addEventListener('click', async () => {
    try {
      const result = await invoke('confirm_dialog', {
        title: 'Confirm Action',
        message: 'Are you sure you want to proceed?'
      });
      const el = document.getElementById('dialog-result');
      if (el) el.textContent = result ? 'Confirmed' : 'Cancelled';
    } catch (e) { console.error(e); }
  });
  document.getElementById('move-monitor-btn')?.addEventListener('click', async () => {
    const selected = document.querySelector('.monitor-item.selected');
    if (!selected) {
      showToast('Select a monitor first', 'warning');
      return;
    }
    const index = parseInt(selected.dataset.monitorIndex, 10);
    try {
      await invoke('move_to_monitor', { monitorIndex: index });
      showToast('Window moved to selected monitor', 'success');
    } catch (e) { showToast('Failed to move: ' + e, 'error'); }
  });
  document.getElementById('refresh-monitors-btn')?.addEventListener('click', loadMonitors);
  document.getElementById('dlg-question')?.addEventListener('click', async () => {
    const dlg = document.getElementById('confirm-dialog');
    const msg = document.getElementById('confirm-message');
    if (msg) msg.textContent = 'Would you like to proceed with the selected action?';
    dlg.showModal();
    const result = await new Promise((resolve) => {
      const onOk = () => { dlg.close(); cleanup(); resolve(true); };
      const onCancel = () => { dlg.close(); cleanup(); resolve(false); };
      const cleanup = () => {
        document.getElementById('confirm-ok').removeEventListener('click', onOk);
        document.getElementById('confirm-cancel').removeEventListener('click', onCancel);
      };
      document.getElementById('confirm-ok').addEventListener('click', onOk);
      document.getElementById('confirm-cancel').addEventListener('click', onCancel);
    });
    const el = document.getElementById('dialog-result');
    if (el) el.textContent = result ? 'User clicked OK' : 'User clicked Cancel';
  });
  document.getElementById('dlg-destructive')?.addEventListener('click', async () => {
    const dlg = document.getElementById('confirm-dialog');
    const msg = document.getElementById('confirm-message');
    if (msg) {
      msg.textContent = 'This action cannot be undone. Are you sure you want to delete this item?';
      msg.style.color = 'var(--danger)';
    }
    dlg.showModal();
    const result = await new Promise((resolve) => {
      const onOk = () => { dlg.close(); cleanup(); resolve(true); };
      const onCancel = () => { dlg.close(); cleanup(); resolve(false); };
      const cleanup = () => {
        document.getElementById('confirm-ok').removeEventListener('click', onOk);
        document.getElementById('confirm-cancel').removeEventListener('click', onCancel);
        if (msg) msg.style.color = '';
      };
      document.getElementById('confirm-ok').addEventListener('click', onOk);
      document.getElementById('confirm-cancel').addEventListener('click', onCancel);
    });
    const el = document.getElementById('dialog-result');
    if (el) el.textContent = result ? 'Destructive action confirmed' : 'Destructive action cancelled';
  });
  document.getElementById('confirm-dialog')?.addEventListener('click', (e) => {
    if (e.target === e.currentTarget) {
      e.currentTarget.close();
    }
  });
}
function registerKeyboardShortcuts() {
  document.addEventListener('keydown', async (e) => {
    const ctrl = e.ctrlKey || e.metaKey;
    if (ctrl && e.key === 'o') {
      e.preventDefault();
      try {
        const path = await invoke('open_file_dialog');
        const result = document.getElementById('file-result');
        if (result) result.textContent = path || 'Cancelled';
      } catch (err) { console.error(err); }
    }
    if (ctrl && e.key === 's') {
      e.preventDefault();
      try {
        const path = await invoke('save_file_dialog', { defaultName: 'untitled.txt' });
        const result = document.getElementById('file-result');
        if (result) result.textContent = path || 'Cancelled';
      } catch (err) { console.error(err); }
    }
    if (ctrl && e.key === 'h') {
      e.preventDefault();
      try { await appWindow.hide(); } catch (err) { console.error(err); }
    }
    if (ctrl && e.key === 'q') {
      e.preventDefault();
      const confirmed = await invoke('confirm_dialog', {
        title: 'Quit Application',
        message: 'Are you sure you want to quit?'
      });
      if (confirmed) {
        await saveWindowState();
        const { getCurrentWebviewWindow } = await import('@tauri-apps/api/webviewWindow');
        const win = getCurrentWebviewWindow();
        await win.close();
      }
    }
    const navKeys = {
      '1': 'dashboard', '2': 'files', '3': 'monitors',
      '4': 'shortcuts', '5': 'dialogs'
    };
    if (e.key >= '1' && e.key <= '5' && !ctrl) {
      const view = navKeys[e.key];
      const navItem = document.querySelector(`.nav-item[data-view="${view}"]`);
      if (navItem) navItem.click();
    }
    if (e.key === 'Escape') {
      const dlg = document.getElementById('confirm-dialog');
      if (dlg.open) dlg.close();
    }
  });
}
async function saveWindowState() {
  try {
    const pos = await appWindow.outerPosition();
    const size = await appWindow.outerSize();
    const maximized = await appWindow.isMaximized();
    await invoke('save_window_state', {
      x: pos.x, y: pos.y,
      width: size.width, height: size.height,
      maximized
    });
  } catch (e) {
    console.error('Failed to save window state:', e);
  }
}
function updateStats() {
  const posEl = document.getElementById('stat-position');
  const sizeEl = document.getElementById('stat-size');
  const focusEl = document.getElementById('stat-focus');
  const dpiEl = document.getElementById('stat-dpi');
  if (posEl) posEl.textContent = `${windowState.x}, ${windowState.y}`;
  if (sizeEl) sizeEl.textContent = `${windowState.width} x ${windowState.height}`;
  if (focusEl) focusEl.textContent = windowState.focused ? 'Focused' : 'Not focused';
  if (dpiEl) dpiEl.textContent = `${(windowState.scaleFactor * 100).toFixed(0)}%`;
}
async function loadMonitors() {
  const list = document.getElementById('monitor-list');
  const moveBtn = document.getElementById('move-monitor-btn');
  if (!list) return;
  list.innerHTML = '<p class="loading">Loading monitors...</p>';
  moveBtn.disabled = true;
  try {
    const monitors = await invoke('get_monitors');
    if (!monitors || monitors.length === 0) {
      list.innerHTML = '<p class="loading">No monitors detected</p>';
      return;
    }
    list.innerHTML = '';
    monitors.forEach((monitor, index) => {
      const item = document.createElement('div');
      item.className = 'monitor-item';
      item.dataset.monitorIndex = index;
      const label = document.createElement('label');
      const radio = document.createElement('input');
      radio.type = 'radio';
      radio.name = 'monitor-select';
      radio.value = index;
      if (index === 0) {
        radio.checked = true;
        item.classList.add('selected');
      }
      radio.addEventListener('change', () => {
        document.querySelectorAll('.monitor-item').forEach(el => el.classList.remove('selected'));
        if (radio.checked) item.classList.add('selected');
        moveBtn.disabled = false;
      });
      const info = document.createElement('div');
      const name = document.createElement('div');
      name.className = 'monitor-name';
      name.textContent = monitor.name || `Monitor ${index + 1}`;
      const details = document.createElement('div');
      details.className = 'monitor-details';
      details.textContent = `${monitor.width}x${monitor.height} @ ${(monitor.scaleFactor * 100).toFixed(0)}% | Position: ${monitor.x}, ${monitor.y}`;
      info.appendChild(name);
      info.appendChild(details);
      label.appendChild(radio);
      label.appendChild(info);
      if (monitor.isPrimary) {
        const badge = document.createElement('span');
        badge.className = 'monitor-badge';
        badge.textContent = 'Primary';
        label.appendChild(badge);
      }
      item.appendChild(label);
      list.appendChild(item);
    });
    moveBtn.disabled = false;
  } catch (err) {
    list.innerHTML = `<p class="loading">Failed to load monitors: ${err}</p>`;
    moveBtn.disabled = true;
  }
}
function showToast(message, type = 'info') {
  const container = document.getElementById('toast-container');
  if (!container) return;
  const toast = document.createElement('div');
  toast.className = `toast ${type}`;
  toast.textContent = message;
  toast.setAttribute('role', 'status');
  container.appendChild(toast);
  setTimeout(() => {
    toast.style.opacity = '0';
    toast.style.transform = 'translateX(20px)';
    toast.style.transition = 'opacity 300ms, transform 300ms';
    setTimeout(() => toast.remove(), 300);
  }, 3000);
}
document.addEventListener('DOMContentLoaded', () => {
  initApp().catch(console.error);
});
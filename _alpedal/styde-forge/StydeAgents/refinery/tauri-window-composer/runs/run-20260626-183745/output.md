Fas 0.5 Design Mockups — Tauri Window Composer
Windows-native chrome spec
Titlebar: Custom HTML/CSS titlebar using Tauri window API, no native decorations. 32px height. Top edge invisible hit zone for resize cursor. Left side: app icon (16x16 scaled from system icon), app name in Segoe UI 12px semibold. Right side: minimize, maximize/restore, close buttons in 46x32px hit targets. Button icons: Segoe MDL2 Assets font glyphs (E921, E922, E923, E8A1 for close). Close button hover: #e81123 background. Buttons use data-tauri-drag-region="false" to exclude from drag. Titlebar uses data-tauri-drag-region="true" to enable window drag. On Windows 11: rounded corners via dwmapi DwmSetWindowAttribute DWMWA_WINDOW_CORNER_PREFERENCE = DWMWCP_ROUND. On Windows 10: sharp corners, full-height 1px border.
Titlebar states: active (background: #1f1f1f), inactive/blurred (background: #2d2d2d, opacity 0.85), maximized (no border radius, titlebar top-edge snap to screen edge). Titlebar text: inactive state gets #666 color.
System menu: right-click on app icon or left-click icon shows context menu with Restore, Move, Size, Minimize, Maximize, Close items using Tauri window API. X button alt+space fallback.
Window chrome: 1px border around entire window using CSS outline or box-shadow. Border color matches titlebar inactive state when window not focused. When focused: border uses accent color from Windows registry HKEY_CURRENT_USER\Software\Microsoft\Windows\DWM\AccentColor. Fallback: #005fb8.
Window resize handles: invisible 4px zones on all edges. Corner handles 8x8px at all four corners. Cursor changes: n-resize, s-resize, e-resize, w-resize, ne-resize, nw-resize, se-resize, sw-resize via CSS cursor property. Use Tauri onResize event for live window size tracking.
Content area: below titlebar. No gap, no padding between titlebar and content. Background: #0d0d0d. Content fills remaining height via flex:1.
System tray icon: custom 16x32px monochrome icon (white logo on transparent, single-color). Tray tooltip: "Styde Forge — Building...". Tray context menu: "Open Forge", "Open Dashboard", "Recent Blueprints" (dynamic submenu last 5), separator line (thin gray 1px), "Check for Updates", separator, "Quit Forge". Tray icon changes based on forge state: idle (full opacity), building (animated — icon swaps every 500ms between two variants for 2px bounce effect), error (red dot overlay in bottom-right corner of icon). Double-click tray icon: restore or focus main window. Tauri app.on-tray-event handler in Rust: TrayIconEvent::DoubleClick -> window.show(), window.set_focus().
Window management: Tauri window event listeners. on-close: intercept close event -> if forge is building or subagents active, show confirmation dialog "Close Forge? Active processes will be terminated." with "Close anyway" and "Minimize to tray" buttons. If no processes: close immediately. on-minimize: allow default minimize. on-hide: triggered by close-to-tray or minimize-to-tray. Window position and size persisted via app handle path, save on every resize and move, restore on launch.
Mouse region management: data-tauri-drag-region on titlebar background. All interactive elements inside titlebar (buttons, icon, text) explicitly set data-tauri-drag-region="false". Content area never draggable. Double-click titlebar: toggle maximize/restore via app.window.toggleMaximize().
Windows-specific: DWM glass effect bypass — set window background to solid #0d0d0d, disable acrylic/blur behind because custom chrome handles it. Snap layout integration on Windows 11: when hovering maximize button, show a 1px border preview overlay simulating snap regions (left/right/quadrant). Not real snap layout dropdown (Tauri limitation), but visual indicator of what happens on maximize.
Edge cases: DPI scaling — titlebar icon and buttons scale with window.devicePixelRatio. Use CSS transform scale for crisp rendering. Multi-monitor: save window position relative to primary display; if saved position outside all monitor bounds on next launch, center on primary. Fullscreen mode: hide titlebar entirely, show content edge-to-edge. Exit fullscreen via F11 or Escape triggers titlebar reappearance with smooth transition.
HTML layout structure:
titlebar (id="titlebar", data-tauri-drag-region="true")
  titlebar-left (flex row, align center)
    app-icon (16x16 img, data-tauri-drag-region="false")
    app-title (span, data-tauri-drag-region="false")
  titlebar-center (flex:1, spacer)
  titlebar-right (flex row)
    minimize-btn (button, data-tauri-drag-region="false")
    maximize-btn (button, data-tauri-drag-region="false")
    close-btn (button, data-tauri-drag-region="false")
content (id="content", flex:1, overflow auto)
CSS variables:
  --chrome-bg-active: #1f1f1f
  --chrome-bg-inactive: #2d2d2d
  --chrome-border: 1px solid rgba(255,255,255,0.08)
  --chrome-accent: var(--accent-color, #005fb8)
  --chrome-close-hover: #e81123
  --chrome-btn-size: 46px
  --chrome-btn-icon-size: 10px
  --titlebar-height: 32px
JavaScript: Tauri invoke() calls for window.setTitle(), window.isMaximized(), window.toggleMaximize(), window.minimize(), window.close(). Custom position tracking: setInterval 5s save position. Window state persistence: JSON in app data dir. On load: read file, validate bounds (checkScreenBounds utility), apply position and size, or center on primary if invalid.
Animations: maximize/restore uses CSS transition on transform (200ms ease). Titlebar background transition between active/inactive states (150ms). Minimize to tray: window fades out 100ms before hide(). Close button: 50ms scale(0.95) on mousedown, release back to 1.0.
Accessibility: titlebar buttons have aria-labels. Close button aria-label="Close window". Minimize aria-label="Minimize to taskbar". Maximize/restore aria-label toggles between "Maximize window" and "Restore window". Focus visible outline on keyboard navigation. Tab order: minimize -> maximize/restore -> close. Escape key focus leaves titlebar buttons, no default close on escape.
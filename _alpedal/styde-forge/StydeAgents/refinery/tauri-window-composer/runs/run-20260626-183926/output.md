teacher feedback accepted. implementing changes.
BLUEPRINT.md:
Blueprint: Forge Desktop Window Composer
Version: 2
Status: spec
file: BLUEPRINT.md
section: Purpose
  Design native desktop window chrome, custom titlebars with OS integration, system tray, window management for Tauri-based Forge app. Feels like a real Windows native app, not a web page in a window.
section: API Surface
  Tauri Commands (Rust backend -> frontend):
  // Window management
  #[tauri::command]
  fn window_get_state() -> WindowState;
  // Returns current window state: { x, y, width, height, maximized, fullscreen, minimized }
  #[tauri::command]
  fn window_minimize(app: tauri::AppHandle);
  #[tauri::command]
  fn window_maximize(app: tauri::AppHandle);
  #[tauri::command]
  fn window_close(app: tauri::AppHandle);
  #[tauri::command]
  fn window_toggle_maximize(app: tauri::AppHandle);
  #[tauri::command]
  fn window_center(app: tauri::AppHandle);
  #[tauri::command]
  fn window_set_size(app: tauri::AppHandle, width: u32, height: u32);
  #[tauri::command]
  fn window_set_position(app: tauri::AppHandle, x: i32, y: i32);
  #[tauri::command]
  fn window_snap_region(app: tauri::AppHandle) -> SnapRegion;
  // Returns available snap zones: { left, right, top, bottom, top_left, top_right, bottom_left, bottom_right }
  // System tray
  #[tauri::command]
  fn tray_set_icon(state: tauri::State<AppState>, icon_name: String);
  #[tauri::command]
  fn tray_show_notification(state: tauri::State<AppState>, title: String, body: String, duration_ms: Option<u64>);
  #[tauri::command]
  fn tray_set_tooltip(state: tauri::State<AppState>, text: String);
  #[tauri::command]
  fn tray_update_menu(items: Vec<TrayMenuItem>);
  // TrayMenuItem: { id, label, disabled, checked, separator }
  // Titlebar integration
  #[tauri::command]
  fn titlebar_set_drag_region(app: tauri::AppHandle, x: f64, y: f64, width: f64, height: f64);
  #[tauri::command]
  fn titlebar_set_app_icon(icon_path: String);
  #[tauri::command]
  fn titlebar_set_title(text: String);
  #[tauri::command]
  fn titlebar_set_theme(theme: TitlebarTheme); // system / light / dark
  #[tauri::command]
  fn titlebar_enable_overlay(state: tauri::State<AppState>) -> TauriResult;
  // Enables per-monitor DPI aware overlay chrome. Returns ok or error code.
  Rust Structs:
  struct WindowState {
      x: i32, y: i32, width: u32, height: u32,
      maximized: bool, fullscreen: bool, minimized: bool,
      monitor_info: MonitorInfo, // { name, scale_factor, work_area }
  }
  struct SnapRegion {
      left: Rect, right: Rect, top: Rect, bottom: Rect,
      top_left: Rect, top_right: Rect,
      bottom_left: Rect, bottom_right: Rect,
  }
  struct Rect { x: i32, y: i32, width: u32, height: u32 }
  struct MonitorInfo { name: String, scale_factor: f64, work_area: Rect }
  struct TrayMenuItem { id: String, label: String, disabled: bool, checked: bool, separator: bool }
  enum TitlebarTheme { System, Light, Dark }
  enum TauriResult { Ok, Error { code: u32, message: String } }
  Frontend Event Listeners (window.onmessage / Tauri event):
  on_window_state_changed(state: WindowState)
  on_tray_click(action: TrayClickAction) // left / right / double
  on_tray_menu_item_clicked(item_id: String)
  on_monitor_changed(monitor: MonitorInfo)
  on_theme_changed(theme: TitlebarTheme)
  on_snap_invoked(region: SnapRegion)
section: DPI and Layout Rules
  rule 1: Custom titlebar must respond to monitor scale factor changes in real time. Listen for on_monitor_changed and re-render chrome at new DPI.
  rule 2: Titlebar height formula: base(32px) * scale_factor. Minimum 32 physical pixels.
  rule 3: Window control buttons (minimize, maximize, close) must be exactly 46px wide at 100% scale. Scale proportionally with DPI.
  rule 4: Hit target for resize edges is 4px at 100% scale, 8px at >= 200%. Corner hit targets are 8px at 100%, 12px at >= 200%.
  rule 5: Snap region indicators rendered at 60% opacity, 2px border, rounded corners 4px. Color follows TitlebarTheme.
  rule 6: All chrome elements must use Tauri physical pixel (px) units, not CSS px. Multiply CSS values by scale_factor.
section: Animation Specs
  animation window_minimize: 200ms ease-out, scale Y -> 0, opacity -> 0
  animation window_restore: 200ms ease-out, scale Y -> 1, opacity -> 1
  animation window_maximize: 150ms ease-in-out, expand from current rect to monitor work area
  animation snap_enter: 100ms ease-out, flash indicator at 100% opacity then settle at 60%
  animation hover_control_button: 80ms linear, background color transition
  animation tray_notification_slide: 250ms ease-out, slide in from right, offset +20px -> 0px
  animation tray_notification_fade: 300ms ease-in, opacity 1 -> 0 (starts after duration_ms elapses)
  rule: animations respect prefers-reduced-motion. If detected, duration = 0ms (instant).
section: Edge Cases
  edge case 1: Window on taskbar (bottom of screen). Snap region top extends to monitor work area top, not screen top. Snap region bottom clipped at taskbar edge.
  edge case 2: Multi-monitor with different scale factors. Window dragged between monitors: re-render titlebar at new DPI within next animation frame. Tauri resize event = trigger recalculation.
  edge case 3: Fullscreen application (e.g. games). System tray must suppress notifications. Check is_window_focused == false + is_fullscreen == true on any monitor -> queue notifications in buffer; show on return.
  edge case 4: RDP / remote desktop. Scale factor changes may be delayed. Poll on_monitor_changed every 2 seconds while remote session is active. Re-render on change.
  edge case 5: Windows high contrast mode. Detect via CSS forced-colors media query. Override theme colors to system high contrast palette. Titlebar buttons remain functional.
  edge case 6: Titlebar drag region overlaps control buttons. Reserve 46px * 3 = 138px on right for buttons. Drag region starts at left of button area.
  edge case 7: Minimize animation on very small windows (< 200px tall). Skip scale animation, just fade opacity 0 in 100ms.
  edge case 8: Snap drag while maximized. When user grabs titlebar and drags, immediately unmaximize with animation to restore rect, then enter snap detection mode.
section: System Tray
  tray default_icon: forge-tray.png (24x24 @96dpi, 32x32 @144dpi)
  tray icons: idle (default), active (running batch), error (forge failure), notification (unread alerts)
  tray menu structure:
    [0] "Open Forge" -> window_show + focus
    [1] separator
    [2] "Run BP Queue" -> tray_run_batch
    [3] "Stop Batch" -> tray_stop_batch (disabled when idle)
    [4] separator
    [5] "Dashboard" -> tray_open_dashboard
    [6] "Command Center" -> tray_open_command_center
    [7] separator
    [8] "Quit" -> app_exit
  tray notification limit: max 5 simultaneous. Queue overflow -> oldest dismissed.
  tray double-click: always shows main window. Not configurable.
section: Custom Titlebar
  elements: app_icon (24x24), title_text, window_control_buttons (minimize, maximize/restore, close)
  drag_region: entire titlebar except control button area (right 138px)
  right_click on titlebar: show system window menu (close, move, size, minimize, maximize, restore)
  double_click on titlebar: toggle maximize/restore
  titlebar_context_actions: if shift+double-click: snap to nearest edge
  theme: system default. Detected via CSS prefers-color-scheme and Tauri theme event.
  custom titlebar replaces native. Decorations: false in tauri.conf.json.
config.yaml:
criteria:
  - name: spec_completeness
    weight: 25
    description: All API endpoints, structs, events, edge cases, DPI rules documented
  - name: native_fidelity
    weight: 25
    description: Behavior matches Windows native chrome (snap, resize, high contrast, multi-dpi)
  - name: structural_clarity
    weight: 20
    description: Scannable sections, concrete signatures, no prose-heap structure
  - name: animation_spec
    weight: 15
    description: Every animation has duration, easing, property; respects reduced-motion
  - name: edge_case_coverage
    weight: 15
    description: Remote desktop, high contrast, multi-monitor dpi mismatch, taskbar overlap, snap while maximized
eval_mode: spec
outputstyle: spec
generations: 1
judge: strict
reviewer_count: 1
review_criteria: [structural_clarity, native_fidelity, api_completeness]
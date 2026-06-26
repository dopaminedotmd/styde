# Tauri Window Composer
**Purpose:** Design native desktop window chrome, titlebars, system tray integration, and desktop-OS-level interaction patterns for Tauri-based Forge desktop app. Feels like a real Windows app, not a web page in a window.
**Persona:** You are a Tauri desktop window composer. Native chrome, custom titlebars with OS integration, system tray, window management. Desktop-first — not a web page in a window. Feels like a real native app.
**Skills:** tauri-development, frontend-design, high-end-visual-design
---
## Titlebar Specification
Custom HTML/CSS titlebar via Tauri window API, no native decorations. 32px height. Top edge 1px invisible hit zone for resize cursor.
Layout:
- Left side: app icon (16x16, scaled from system icon), app name (Segoe UI 12px semibold)
- Right side: minimize, maximize/restore, close buttons (46x32px hit targets)
- Center: flex spacer
Button icons use Segoe MDL2 Assets glyphs (E921, E922, E923, E8A1 for close). Close button hover background: #e81123. Buttons set data-tauri-drag-region="false". Titlebar sets data-tauri-drag-region="true" for window drag.
Titlebar states:
- Active: background #1f1f1f
- Inactive/blurred: background #2d2d2d, opacity 0.85, text color #666
- Maximized: no border radius, titlebar top-edge snapped to screen edge
System menu: right-click or left-click app icon shows context menu (Restore, Move, Size, Minimize, Maximize, Close) via Tauri window API. Win+Alt fallback.
---
## Window Chrome
1px border around entire window using CSS outline. Border color matches titlebar inactive color when unfocused. When focused: accent color from Windows registry HKCU\Software\Microsoft\Windows\DWM\AccentColor. Fallback: #005fb8.
Resize handles: invisible 4px zones on all edges. Corner handles 8x8px at all four corners. CSS cursor changes: n-resize, s-resize, e-resize, w-resize, ne-resize, nw-resize, se-resize, sw-resize. Tauri onResize event for live tracking.
Content area: below titlebar, no gap/padding. Background #0d0d0d. Fills remaining height via flex:1.
Windows 11: rounded corners via dwmapi DwmSetWindowAttribute DWMWA_WINDOW_CORNER_PREFERENCE = DWMWCP_ROUND. Windows 10: sharp corners, full-height 1px border.
---
## System Tray
Custom tray icon: 16x32px monochrome (white logo on transparent, single-color). Tooltip: "Styde Forge — Building...".
Context menu:
- Open Forge
- Open Dashboard
- Recent Blueprints (dynamic submenu, last 5)
- separator (thin gray 1px)
- Check for Updates
- separator
- Quit Forge
Icon states: idle (full opacity), building (animated swap every 500ms between 2 variants, 2px bounce effect), error (red dot overlay bottom-right).
Double-click tray: restore/focus main window. Tauri app.on-tray-event handler in Rust: TrayIconEvent::DoubleClick -> window.show(), window.set_focus().
---
## API Surface
### Tauri Rust Commands (invoke bridge)
```typescript
// Window management
invoke('set_window_title', { title: string }): Promise<void>
invoke('is_maximized'): Promise<boolean>
invoke('toggle_maximize'): Promise<void>
invoke('minimize_window'): Promise<void>
invoke('close_window'): Promise<void>
invoke('restore_window'): Promise<void>
invoke('maximize_window'): Promise<void>
// Window state persistence
invoke('save_window_state', { state: WindowState }): Promise<void>
invoke('load_window_state'): Promise<WindowState | null>
invoke('validate_window_bounds', { rect: Rect }): Promise<Rect>
// System tray
invoke('set_tray_state', { state: 'idle' | 'building' | 'error' }): Promise<void>
invoke('get_recent_blueprints'): Promise<BlueprintMeta[]>
// Snap layout
invoke('preview_snap_zone', { zone: 'left' | 'right' | 'top-left' | 'top-right' | 'bottom-left' | 'bottom-right' | 'center' | 'none' }): Promise<void>
invoke('apply_snap_zone', { zone: SnapZone }): Promise<void>
invoke('get_snap_zones'): Promise<SnapZone[]>
// DPI
invoke('get_dpi_scale'): Promise<number>
invoke('set_dpi_policy', { policy: 'system' | 'per-monitor' | 'per-monitor-v2' }): Promise<void>
// Accessibility
invoke('get_accessibility_settings'): Promise<AccessibilitySettings>
invoke('announce_alert', { message: string }): Promise<void>
```
### Rust Struct Definitions
```rust
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct WindowState {
    pub x: i32,
    pub y: i32,
    pub width: u32,
    pub height: u32,
    pub maximized: bool,
    pub monitor_index: u32,
    pub snap_zone: Option<SnapZone>,
}
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct Rect {
    pub x: i32,
    pub y: i32,
    pub width: u32,
    pub height: u32,
}
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct SnapZone {
    pub zone_type: SnapZoneType,
    pub x: i32,
    pub y: i32,
    pub width: u32,
    pub height: u32,
    pub monitor_handle: isize,
}
#[derive(Debug, Clone, Serialize, Deserialize)]
pub enum SnapZoneType {
    Left,
    Right,
    TopLeft,
    TopRight,
    BottomLeft,
    BottomRight,
    Center,
    Full,
    Custom(Rect),
}
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct AccessibilitySettings {
    pub high_contrast: bool,
    pub reduced_motion: bool,
    pub font_scale: f32,
    pub cursor_size: u8,
}
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct BlueprintMeta {
    pub id: String,
    pub name: String,
    pub version: String,
    pub updated_at: String,
}
```
### Tauri Event System (Frontend <-> Backend)
```typescript
// Events emitted from Rust to frontend
type WindowEvent =
  | { type: 'resized'; rect: Rect }
  | { type: 'moved'; x: number; y: number }
  | { type: 'focus-changed'; focused: boolean }
  | { type: 'theme-changed'; accent: string; theme: 'light' | 'dark' }
  | { type: 'dpi-changed'; scale: number }
  | { type: 'snap-zone-changed'; zone: SnapZone | null }
  | { type: 'tray-state-changed'; state: 'idle' | 'building' | 'error' }
listen('window-event', (event: { payload: WindowEvent }) => void)
```
---
## DPI & Layout Rules
- All titlebar elements scale with window.devicePixelRatio
- Use CSS transform scale for crisp rendering at non-integer ratios
- DPI policies: system-aware via Tauri window.dpi property
- Multi-monitor: save window position relative to primary display. If saved position outside all monitor bounds on next launch, center on primary
- Fullscreen mode: hide titlebar entirely, show content edge-to-edge. Exit via F11 or Escape triggers titlebar reappearance with smooth transition (200ms ease)
---
## Keyboard Shortcuts
| Shortcut | Action |
|----------|--------|
| Win+Up | Maximize window |
| Win+Down | Restore / minimize |
| Win+Left | Snap left (50% width) |
| Win+Right | Snap right (50% width) |
| Win+Shift+Left | Move to left monitor |
| Win+Shift+Right | Move to right monitor |
| Alt+Space | Open system window menu |
| Win+Z | Open snap layout picker (Windows 11) |
| F11 | Toggle fullscreen |
| Escape | Exit fullscreen / close snap preview |
All keyboard shortcuts are intercepted via Tauri global-shortcut plugin, not brute- force window event listeners. On Windows 10, Win+Z and snap layout shortcuts fall back gracefully (no-op with console warning).
---
## Snap Layout Integration (Windows 11)
When hovering maximize button, trigger a 1px border preview overlay showing snap regions:
- Left 50% (highlighted on left-half hover)
- Right 50% (highlighted on right-half hover)
- Quadrant splits: top-left, top-right, bottom-left, bottom-right (highlighted on corner-quarter hover)
- Center (return to floating window on center hover)
The preview overlay is a CSS pseudo-element on the titlebar maximize button, positioned as a floating panel (300x200px) that appears on hover with 100ms fade-in. Snap zones are highlighted with accent-color semi-transparent overlay.
On snap zone selection: window animates to position/size (200ms ease-out CSS transition). Zone allocation uses Tauri window.set_position() and window.set_size() in Rust, respecting Windows monitor work area (excludes taskbar).
Multi-monitor snap preservation: when monitor arrangement changes, restore window to nearest equivalent zone on connected monitor. If no equivalent zone available (e.g. zone only valid at 1920+ width but monitor is 1366), fall back to centered floating at 70% width.
Restore on wake: on system resume (monitor reconnection, wake from sleep), re-evaluate all snapped windows. If zone is still valid (same display arrangement), restore position. If arrangement changed, reflow to best-effort zone or floating as above.
---
## Error Handling
### Recovery Strategies
| Error | Recovery |
|-------|----------|
| Window state file corrupt (JSON parse failure) | Delete file, launch centered on primary at 1200x800 default |
| Saved window position outside all monitors | validateWindowBounds utility returns centered rect on primary. WindowState saved with monitor_index; if index out of range, fall back to primary |
| DPI change during animation | Immediately snap animation to final state, re-render at new scale. CSS transition interrupted by class toggle |
| Tray icon load failure | Silently skip tray setup, log warning. App continues without tray |
| Accent color registry read fails | Use #005fb8 fallback. Cache fallback for session |
| Snap layout zone monitor disconnected | If window was snapped to disconnected monitor, move to primary monitor equivalent zone. If no equivalent, float centered at 1200x800 |
| Crash during build (window chrome still visible) | On next launch, reset window state to defaults (delete corrupted state file), show error toast "Forge recovered from unexpected shutdown" |
### TauriResult Enum
```rust
#[derive(Debug, Serialize, Deserialize)]
pub enum TauriResult<T> {
    Ok(T),
    Err {
        code: u32,
        message: String,
        recovery: Option<String>,
    },
}
// Error codes
const ERR_WINDOW_STATE_CORRUPT: u32 = 1001;
const ERR_WINDOW_BOUNDS_INVALID: u32 = 1002;
const ERR_TRAY_INIT_FAILED: u32 = 2001;
const ERR_DPI_UNSUPPORTED: u32 = 3001;
const ERR_SNAP_ZONE_INVALID: u32 = 4001;
const ERR_ACCENT_READ_FAIL: u32 = 5001;
```
Snap-state persistence: WindowState.snap_zone is saved on every resize/move event (debounced 500ms). On app startup, last saved snap zone is re-applied before window.show() to prevent visual flash. If zone re-application fails, window appears centered at last saved size.
Fallback DPI profile: store last 3 working DPI configurations. If current DPI causes layout overflow (titlebar buttons clip, text truncation), roll back to nearest working profile and flag DPI change via TauriResult warning.
---
## Animation Specs
| Animation | Duration | Easing | Trigger |
|-----------|----------|--------|---------|
| Maximize/restore window | 200ms | ease-out | maximize/restore action |
| Titlebar active/inactive | 150ms | ease | window focus/blur event |
| Minimize to tray | 100ms | ease-in | minimize-to-tray action (fade out) |
| Close button press | 50ms | ease | mousedown (scale 0.95, release back to 1.0) |
| Snap preview panel | 100ms | ease-out | maximize button hover |
| Snap zone apply | 200ms | ease-out | snap zone selection |
| Fullscreen toggle titlebar | 200ms | ease | F11/Escape |
Snap preview panel uses CSS transition on opacity and transform (translateY). All animations respect prefers-reduced-motion media query: if reduced-motion, zero-duration transitions (instant snap).
---
## Edge Cases
- DPI scaling: titlebar icon and buttons scale with window.devicePixelRatio. Use CSS transform scale for crisp rendering
- Multi-monitor: save window position relative to primary; if outside all bounds, center on primary
- Fullscreen mode: hide titlebar completely, show content edge-to-edge. Exit via F11 or Escape restores titlebar with smooth transition
- RDP session: DPI can change mid-session. Listen for dpi-changed event and re-render titlebar at new scale
- High-contrast mode: detect via accessibility settings, swap to high-contrast CSS variables (--chrome-bg-active: Canvas, --chrome-btn-hover: Highlight)
- Window state file I/O: debounced 5s for writes. If write fails (disk full, permissions), retry 3 times then skip persist for that event
---
## HTML Layout Structure
```html
<div id="titlebar" data-tauri-drag-region="true">
  <div id="titlebar-left">
    <img id="app-icon" src="icon.png" width="16" height="16" data-tauri-drag-region="false" />
    <span id="app-title" data-tauri-drag-region="false">Styde Forge</span>
  </div>
  <div id="titlebar-center"></div>
  <div id="titlebar-right">
    <button id="minimize-btn" class="titlebar-btn" data-tauri-drag-region="false" aria-label="Minimize to taskbar">&#xE921;</button>
    <button id="maximize-btn" class="titlebar-btn" data-tauri-drag-region="false" aria-label="Maximize window">&#xE922;</button>
    <button id="close-btn" class="titlebar-btn close-btn" data-tauri-drag-region="false" aria-label="Close window">&#xE8A1;</button>
  </div>
</div>
<div id="content" style="flex: 1; overflow: auto;"></div>
```
---
## CSS Variables
```css
--chrome-bg-active: #1f1f1f;
--chrome-bg-inactive: #2d2d2d;
--chrome-border: 1px solid rgba(255,255,255,0.08);
--chrome-accent: var(--accent-color, #005fb8);
--chrome-close-hover: #e81123;
--chrome-btn-size: 46px;
--chrome-btn-icon-size: 10px;
--titlebar-height: 32px;
```
High-contrast overrides:
```css
@media (prefers-contrast: high) {
  --chrome-bg-active: Canvas;
  --chrome-border: 1px solid ButtonText;
  --chrome-close-hover: Highlight;
}
```
Reduced motion:
```css
@media (prefers-reduced-motion: reduce) {
  * { transition-duration: 0s !important; animation-duration: 0s !important; }
}
```
---
## Accessibility
Titlebar buttons have aria-labels:
- Close: "Close window"
- Minimize: "Minimize to taskbar"
- Maximize: "Maximize window" / "Restore window" (toggles)
Focus visible outline on keyboard navigation. Tab order: minimize -> maximize/restore -> close. Escape key moves focus out of titlebar buttons (does not close window). Space/Enter activates focused button.
When window state changes (maximized, minimized, snapped), announce via aria-live region: "Window maximized", "Window snapped to left half", etc.
---
## JavaScript Window Management
```typescript
// Position tracking (debounced 5s)
let saveTimeout: ReturnType<typeof setTimeout>;
window.addEventListener('resize', () => {
  clearTimeout(saveTimeout);
  saveTimeout = setTimeout(saveWindowState, 5000);
});
// Window state persistence
async function saveWindowState(): Promise<void> {
  const state: WindowState = {
    x: window.screenX,
    y: window.screenY,
    width: window.innerWidth,
    height: window.innerHeight,
    maximized: await invoke('is_maximized'),
    monitor_index: getCurrentMonitorIndex(),
    snap_zone: currentSnapZone,
  };
  await invoke('save_window_state', { state });
}
async function loadAndApplyWindowState(): Promise<void> {
  const state = await invoke('load_window_state');
  if (!state) {
    window.moveTo(centerX, centerY);
    window.resizeTo(1200, 800);
    return;
  }
  const validRect = await invoke('validate_window_bounds', { rect: { x: state.x, y: state.y, width: state.width, height: state.height } });
  window.moveTo(validRect.x, validRect.y);
  window.resizeTo(validRect.width, validRect.height);
  if (state.maximized) await invoke('maximize_window');
  if (state.snap_zone) await invoke('apply_snap_zone', { zone: state.snap_zone });
}
```
```
config.yaml
```
```yaml
blueprint:
  name: tauri-window-composer
  version: 3.0.0
  domain: frontend
  last_reviewed: '2026-06-26'
  review_interval_days: 90
  dependencies: []
  schema_expectations: []
  version_history:
  - from: 1.0.0
    to: 2.0.0
    reason: 'MAJOR: quality gate passed (score=88.6)'
    score: 88.6
    previous_score: null
    timestamp: '2026-06-26T18:39:23Z'
  - from: 2.0.0
    to: 3.0.0
    reason: 'MAJOR: quality gate passed (score=85.8); spec restructure and API surface additions'
    score: 85.8
    previous_score: 88.6
    timestamp: '2026-06-26T18:41:13Z'
agent:
  max_iterations: 10
  timeout_seconds: 300
  retry_on_failure: true
  toolsets:
  - terminal
  - file
  - web
eval:
  outputstyle: spec
  benchmarks: []
  judge_model: deepseek-v4-pro
  min_pass_score: 70
platform:
  targets:
  - windows-11-x86_64
  - windows-10-x86_64
  - windows-10-i686
  build_flags:
    windows:
      features:
      - tray-icon
      - global-shortcut
      - window-dpi
      cflags:
      - DWMAPI_ENABLED
      rust_flags:
      - cfg(target_os = "windows")
  dpi_policies:
    default: system
    available:
    - system
    - per-monitor
    - per-monitor-v2
    fallback_profile_count: 3
window_chrome:
  snap_layout:
    enabled: true
    zones:
    - left
    - right
    - top-left
    - top-right
    - bottom-left
    - bottom-right
    - center
    - full
    preview_fade_ms: 100
    animation_ms: 200
    multi_monitor_preservation: true
    restore_on_wake: true
  keyboard_shortcuts:
    win_arrow: true
    alt_space: true
    win_z: true
    f11_fullscreen: true
    escape_exit_fullscreen: true
    shortcut_plugin: tauri-plugin-global-shortcut
    fallback_behavior: graceful_noop
  accessibility:
    aria_labels: true
    tab_order:
    - minimize
    - maximize
    - close
    escape_no_close: true
    high_contrast_variables: true
    reduced_motion_override: true
    live_region_announcements: true
system_tray:
  icon_size: [16, 32]
  icon_channels: 1
  states:
    idle: full_opacity
    building: animated_swap_500ms
    error: red_dot_overlay
  tooltip: "Styde Forge -- Building..."
  context_menu:
  - Open Forge
  - Open Dashboard
  - Recent Blueprints
  - separator
  - Check for Updates
  - separator
  - Quit Forge
  double_click_restores: true
error_handling:
  recoveries:
    window_state_corrupt: delete_and_default
    bounds_invalid: center_on_primary
    dpi_change_during_animation: snap_final_state
    tray_init_failed: skip_and_log
    accent_read_fail: use_fallback
    snap_zone_disconnected: move_to_primary
    crash_recovery: reset_state_and_toast
  persist_debounce_ms: 500
  retry_count: 3
```
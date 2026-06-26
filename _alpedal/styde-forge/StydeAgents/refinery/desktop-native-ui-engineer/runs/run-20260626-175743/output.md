Warning: Unknown toolsets: patch, read_file, search_files
BLUEPRINT.md
name: desktop-native-ui-engineer
domain: frontend
version: 3
Desktop Native UI Engineer
Domain: frontend Version: 3
Purpose
Builds native-quality desktop user interfaces for Tauri v2 applications on Windows. Produces custom titlebars, system tray integration, native dialogs, context menus, keyboard shortcuts, and proper desktop ergonomics following Fluent Design language. Each task produces a working prototype or standalone component.
Skills
Window
  Custom titlebar with CSS-drawn titlebar buttons (minimize, maximize, close)
  Draggable regions via CSS --tauri-drag-region or data-tauri-drag-region
  Snap layouts integration (Win+Z) via shell:OpenWith
  Window state persistence (position, size, maximized) to local storage or config file
Tray
  System tray icon with .ico file (multi-resolution 16x16 to 64x64)
  Context menu with clickable items and submenus
  Minimize-to-tray on WindowEvent::CloseRequested
  Notification badges with unread count via setIconAsTemplate
Dialogs
  File open dialog with filters
  File save dialog with default path
  Message boxes (info, warning, error, question with Yes/No/Cancel)
  Confirmation dialogs before destructive actions
Shortcuts
  Keyboard shortcuts via tauri accelerator format
  Global hotkeys registered system-wide
  Accelerator keys for menu items
Desktop
  Multi-monitor awareness: get current monitor, place windows on specific monitor
  DPI scaling: respond to scaleFactor changes, use physical/logical pixel mapping
  Proper window management: min/max sizes, aspect ratios, resize constraints
Tauri v2 Plugin Configuration
Required Cargo.toml entries:
  tauri = { version = "2", features = ["tray"] }
  tauri-plugin-dialog = "2"
  tauri-plugin-fs = "2"
  tauri-plugin-shell = "2"
  tauri-plugin-global-shortcut = "2"
  tauri-plugin-notification = "2"
Required tauri.conf.json plugin entries:
  plugins.dialog: open=true, save=true, message=true, ask=true, confirm=true
  plugins.fs.scope.allow: ["$APPDATA/", "$DOCUMENT/", "$DESKTOP/"]
  plugins.fs.scope.deny: ["$APPDATA/com.tauri.dev/"]
  plugins.shell.open: true
  plugins.global-shortcut.all: true
  plugins.notification.all: true
Project Scaffolding Checklist
Every task MUST generate all of these files before any implementation begins:
  package.json (or package manager equivalent with dev script)
  vite.config.ts (with tauri devServer config)
  tsconfig.json (strict mode, DOM lib)
  index.html (single entry point, references src/main.ts or src/main.jsx)
  README.md (build instructions, dependencies, feature description)
  .gitignore (node_modules/, target/, dist/, *.log, .env)
  .editorconfig (indent_style=space, indent_size=2, charset=utf-8)
Verification step before writing any implementation code: confirm each file exists with non-empty content. If any file is missing, stop and scaffold it first.
Output Completeness Gate
Truncation threshold for generated frontend assets must be set to unlimited or at least 100000 characters. Before declaring task complete, scan generated output for truncation markers (three dots at file end, abrupt mid-function cutoffs, /* ... */ ellipsis comments, trailing // ...). If any truncation is detected, retry the generation pass with explicit high-limit instruction. Repeat until no truncation markers remain in any file.
Side-Effect Error Detection
After generating all files and before marking task done, run a diagnostic pass checking for:
  Unresolved icon references (check src/ for icon names not present in src-tauri/icons/)
  Duplicate plugin registrations in main.rs (tauri::Builder::default().plugin() called twice for same plugin)
  Unloaded resource fonts (check CSS @font-face references against actual font files in public/)
  Missing CSS variables referenced in JS (check document.documentElement.style.setProperty calls against CSS :root definitions)
  Orphaned IPC commands registered in main.rs but never invoked from frontend
Consistency and Lint Step
Must execute these exact tool invocations in order:
  1. cargo clippy --all-targets --all-features -- -D warnings (fail on any warning)
  2. eslint src/ --max-warnings=5 (fail if warning count exceeds 5)
  3. stylelint src/**/*.css --quiet-deprecation-warnings (fail on any error)
  4. tsc --noEmit (fail on any type error)
  5. prettier --check src/ (fail on any formatting deviation)
Fail step rule: if any lint tool reports warnings exceeding its threshold, the pipeline iteration is marked as failed. Total warning count across all tools must be zero for a passing iteration.
Move Patterns for Output Cleaning
Before finalizing output, scan generated code for these known AI-ism patterns and remove them:
  Regex: ^(?:\s*\/\*\*?\s*)?(?:Here['']?s|This is|Below is|The following)\s+(?:a|the|my)\s+ (introductory boilerplate)
  Regex: \/\*[\s\S]*?(?:Note|Disclaimer|Important)[\s\S]*?\*\/ (inline disclaimers)
  Regex: \/\/\s*(?:End|EOF|Done|Finish|That['']?s it|This is the end) (trailing NOP comments)
  Regex: \/\/\s*(?:TODO|FIXME|HACK|XXX):?\s*$ (stale todo markers that are not actual work items)
  Regex: \/\/\s*(?:Implementation|Code for|Function to)\s+\S+ (self-referential labels)
  Regex: <!--\s*(?:.*?)(?:comment|note|hint|info)[\s\S]*?--> (HTML annotation leaking)
  Regex: ```[\s\S]*?``` with trailing language labels that duplicate the file extension
Auto-remove all matches silently. If more than 10 matches are found in a single file, flag the file for manual review.
IPC Command Signatures
#[tauri::command]
fn save_window_state(app: tauri::AppHandle, x: i32, y: i32, width: u32, height: u32, maximized: bool) -> Result<()> {
  let config_path = app.path().app_config_dir()?.join("windowstate.json");
  let state = serde_json::json!({ "x": x, "y": y, "width": width, "height": height, "maximized": maximized });
  std::fs::write(&config_path, serde_json::to_string_pretty(&state)?)
    .map_err(|e| format!("Failed to save window state: {}", e))
}
#[tauri::command]
fn get_window_state(app: tauri::AppHandle) -> Result<Option<serde_json::Value>> {
  let config_path = app.path().app_config_dir()?.join("windowstate.json");
  if !config_path.exists() { return Ok(None); }
  let content = std::fs::read_to_string(&config_path)
    .map_err(|e| format!("Failed to read window state: {}", e))?;
  serde_json::from_str(&content)
    .map(Some)
    .map_err(|e| format!("Failed to parse window state: {}", e))
}
#[tauri::command]
fn minimize_to_tray(window: tauri::Window) -> Result<()> {
  window.hide().map_err(|e| format!("Failed to hide window: {}", e))
}
#[tauri::command]
fn show_notification(app: tauri::AppHandle, title: String, body: String) -> Result<()> {
  use tauri_plugin_notification::NotificationExt;
  app.notification()
    .builder()
    .title(&title)
    .body(&body)
    .show()
    .map_err(|e| format!("Failed to show notification: {}", e))
}
Capability Permissions
"desktop-native-ui-engineer" capability must include:
  core:default, core:window:default, core:window:allow-close, core:window:allow-hide, core:window:allow-show, core:window:allow-set-focus, core:window:allow-center
  dialog:default, dialog:allow-open, dialog:allow-save, dialog:allow-message, dialog:allow-ask, dialog:allow-confirm
  fs:default, fs:allow-read, fs:allow-write, fs:allow-exists, fs:scope:recursive
  shell:default, shell:allow-open
  global-shortcut:default, global-shortcut:allow-register, global-shortcut:allow-unregister, global-shortcut:allow-is-registered
  notification:default, notification:allow-notify, notification:allow-is-permission-granted, notification:allow-request-permission
Error Propagation Patterns
Tier 1 (Retry): Transient failures (file locked, network timeout) retry up to 3 times with exponential backoff (100ms, 500ms, 2s).
Tier 2 (Fallback): Missing resource (config file not found, plugin not loaded) use sensible defaults and log warning.
Tier 3 (User-facing): Unrecoverable (permission denied, disk full) show native dialog explaining the issue with actionable options.
All Rust commands return Result. Never panic, never unwrap in production code.
Frontend catches invoke() errors in try/catch and routes to user feedback.
Critical errors emit a tauri event so the app can degrade gracefully.
maxIterationsBeforeAutoFix: 2
When the pipeline completes N iterations without full clearance (lint warnings above threshold, truncation detected, scaffolding incomplete), trigger a forced lint-repair pass. The repair pass runs autofix tools (cargo clippy --fix, eslint --fix, prettier --write) on all generated code, then re-runs the full evaluation. If the repair pass also fails, escalate to the user with a repair log listing each unresolved issue and its file:line location.
Task Execution Pipeline
  Receive task description (YAML or plain text) specifying target feature.
  Analyze task: identify required Tauri plugins, IPC channels, UI components.
  Scaffold: run scaffolding checklist verification before writing any implementation code.
  Implement Rust backend: write #[tauri::command] handlers, register in main.rs Builder.
  Implement frontend: write HTML/CSS/JS for the UI component inside WebView.
  Wire IPC: connect frontend invoke() calls to Rust commands, handle responses/errors.
  Run consistency and lint step: execute all 5 tool invocations, enforce threshold rules.
  Run output completeness gate: verify no truncation markers, no missing files from checklist.
  Run side-effect error detection: scan for icon/plugin/font/variable/orphan issues.
  Run move patterns cleaner: strip AI-ism boilerplate, NOP comments, stale TODOs.
  Test: build with cargo tauri build --debug, verify on actual Windows desktop.
  Deliver: output final source tree, build logs, and a summary of what was produced.
Training Data and Evaluation
Datasets:
  Tauri v2 official API documentation
  Tauri v2 plugin documentation for dialog, fs, shell, global-shortcut, notification
  Real-world open-source Tauri apps (tauri-apps/tauri-demo, zellij-org/zellij)
  Windows Fluent Design guidelines (Microsoft docs)
  Sample projects: Todo desktop app, file explorer, settings panel, media player
Evaluation metrics:
  Task completion rate: percentage of features compiled and run without crashes
  Command accuracy: number of IPC handlers that match spec signatures exactly
  Error recovery rate: percentage of test-generated failures handled without crash
  DPI correctness: UI renders properly at 100%, 125%, 150%, 200% scaling
  Build success rate: cargo tauri build passes on first attempt
  Cleanliness score: number of AI-ism pattern matches detected on generated output
Benchmark plan:
  Run agent on 5 benchmark tasks (titlebar, tray, dialogs, shortcuts, multi-monitor)
  Score each task: binary (compiles + runs) on a standard Windows 11 test VM
  Manual review: does the UI look native? Are all states handled (hover, focus, disabled)?
  Composite score = (compile_rate x 0.25) + (visual_native_score x 0.25) + (error_recovery x 0.15) + (IPC_accuracy x 0.15) + (cleanliness x 0.10) + (scaffolding_completeness x 0.10)
Deliverables
Per task, the agent produces:
  Full Tauri v2 project directory (src-tauri/ with Cargo.toml, main.rs, tauri.conf.json, icons/, capabilities/)
  Frontend source (src/ with HTML, CSS, JS)
  Build artifact (debug binary from cargo tauri build --debug or compile-error logs)
  Test report: which features work, known issues, error scenarios tested
  Acceptance checklist: window behavior, tray behavior, dialog flow, shortcut binding, multi-monitor positioning
Minimum acceptance criteria per artifact:
  Binary compiles without warnings
  All scaffolding checklist files present and non-empty
  No truncation markers in any generated file
  Lint tools pass with zero warnings above threshold
  AI-ism patterns removed from all generated output
  Window opens at correct size/position on primary monitor
  Titlebar buttons work (minimize, maximize/restore, close with confirm if dirty)
  Tray icon appears on right-click minimize
  Shortcuts fire corresponding actions
  Dialogs show native Windows dialogs (not HTML modals)
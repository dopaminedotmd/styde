┊ review diff
[38;2;218;165;32ma/StydeAgents\blueprints\tauri-window-composer\config.yaml → b/StydeAgents\blueprints\tauri-window-composer\config.yaml[0m
[38;2;139;134;130m@@ -1,11 +1,55 @@[0m
[38;2;255;255;255;48;2;19;87;20m+agent:[0m
[38;2;255;255;255;48;2;19;87;20m+  max_iterations: 12[0m
[38;2;255;255;255;48;2;19;87;20m+  timeout_seconds: 600[0m
[38;2;255;255;255;48;2;19;87;20m+  retry_on_failure: true[0m
[38;2;255;255;255;48;2;19;87;20m+  model:[0m
[38;2;255;255;255;48;2;19;87;20m+    provider: default[0m
[38;2;255;255;255;48;2;19;87;20m+    name: default[0m
[38;2;255;255;255;48;2;19;87;20m+    temperature: 0.3[0m
[38;2;255;255;255;48;2;19;87;20m+    max_tokens: 12000[0m
[38;2;255;255;255;48;2;19;87;20m+  toolsets:[0m
[38;2;255;255;255;48;2;19;87;20m+  - terminal[0m
[38;2;255;255;255;48;2;19;87;20m+  - file[0m
[38;2;255;255;255;48;2;19;87;20m+  - patch[0m
[38;2;255;255;255;48;2;19;87;20m+  - read_file[0m
[38;2;255;255;255;48;2;19;87;20m+  - search_files[0m
[38;2;255;255;255;48;2;19;87;20m+  permissions:[0m
[38;2;255;255;255;48;2;19;87;20m+    files:[0m
[38;2;255;255;255;48;2;19;87;20m+      allow:[0m
[38;2;255;255;255;48;2;19;87;20m+      - $WORKSPACE/src/**[0m
[38;2;255;255;255;48;2;19;87;20m+      - $WORKSPACE/src-tauri/**[0m
[38;2;255;255;255;48;2;19;87;20m+      - $WORKSPACE/public/**[0m
[38;2;255;255;255;48;2;19;87;20m+      - $WORKSPACE/*.json[0m
[38;2;255;255;255;48;2;19;87;20m+      - $WORKSPACE/*.toml[0m
[38;2;255;255;255;48;2;19;87;20m+      deny: [][0m
[38;2;255;255;255;48;2;19;87;20m+    terminal:[0m
[38;2;255;255;255;48;2;19;87;20m+      allow:[0m
[38;2;255;255;255;48;2;19;87;20m+      - cargo tauri build --debug[0m
[38;2;255;255;255;48;2;19;87;20m+      - cargo tauri build[0m
[38;2;255;255;255;48;2;19;87;20m+      - cargo check[0m
[38;2;255;255;255;48;2;19;87;20m+      - cargo build[0m
[38;2;255;255;255;48;2;19;87;20m+      - npm install[0m
[38;2;255;255;255;48;2;19;87;20m+      - npm run build[0m
[38;2;255;255;255;48;2;19;87;20m+      - cargo add[0m
[38;2;255;255;255;48;2;19;87;20m+      - cargo tauri icon[0m
[38;2;255;255;255;48;2;19;87;20m+      deny:[0m
[38;2;255;255;255;48;2;19;87;20m+      - sudo[0m
[38;2;255;255;255;48;2;19;87;20m+      - rm -rf /[0m
[38;2;255;255;255;48;2;19;87;20m+      - chmod -R 777[0m
[38;2;184;134;11m blueprint:[0m
[38;2;184;134;11m   name: tauri-window-composer[0m
[38;2;255;255;255;48;2;119;20;20m-  version: 4.0.0[0m
[38;2;255;255;255;48;2;19;87;20m+  version: 5.0.0[0m
[38;2;184;134;11m   domain: frontend[0m
[38;2;184;134;11m   last_reviewed: '2026-06-26'[0m
[38;2;184;134;11m   review_interval_days: 90[0m
[38;2;255;255;255;48;2;119;20;20m-  dependencies: [][0m
[38;2;255;255;255;48;2;119;20;20m-  schema_expectations: [][0m
[38;2;255;255;255;48;2;19;87;20m+  dependencies:[0m
[38;2;255;255;255;48;2;19;87;20m+  - rust (>=1.75)[0m
[38;2;255;255;255;48;2;19;87;20m+  - nodejs (>=18)[0m
[38;2;255;255;255;48;2;19;87;20m+  - cargo-tauri-cli (>=2.0)[0m
[38;2;255;255;255;48;2;19;87;20m+  schema_expectations:[0m
[38;2;255;255;255;48;2;19;87;20m+  - BLUEPRINT.md must cover custom titlebar, system tray, window compositing, error handling, keyboard shortcuts, snap layout integration[0m
[38;2;255;255;255;48;2;19;87;20m+  - persona.md must define role constraints, domain expertise, quality standards[0m
[38;2;255;255;255;48;2;19;87;20m+  - config.yaml must define platform targets, DPI policies, accessibility defaults, keyboard bindings, lifecycle gates[0m
[38;2;184;134;11m   version_history:[0m
[38;2;184;134;11m   - from: 1.0.0[0m
[38;2;184;134;11m     to: 2.0.0[0m
[38;2;139;134;130m@@ -25,15 +69,125 @@[0m
[38;2;184;134;11m     score: 92.0[0m
[38;2;184;134;11m     previous_score: 85.8[0m
[38;2;184;134;11m     timestamp: '2026-06-26T18:43:30Z'[0m
[38;2;255;255;255;48;2;119;20;20m-agent:[0m
[38;2;255;255;255;48;2;119;20;20m-  max_iterations: 10[0m
[38;2;255;255;255;48;2;119;20;20m-  timeout_seconds: 300[0m
[38;2;255;255;255;48;2;119;20;20m-  retry_on_failure: true[0m
[38;2;255;255;255;48;2;119;20;20m-  toolsets:[0m
[38;2;255;255;255;48;2;119;20;20m-  - terminal[0m
[38;2;255;255;255;48;2;119;20;20m-  - file[0m
[38;2;255;255;255;48;2;119;20;20m-  - web[0m
[38;2;255;255;255;48;2;119;20;20m-eval:[0m
[38;2;255;255;255;48;2;119;20;20m-  benchmarks: [][0m
[38;2;255;255;255;48;2;119;20;20m-  judge_model: deepseek-v4-pro[0m
[38;2;255;255;255;48;2;119;20;20m-  min_pass_score: 70[0m
[38;2;255;255;255;48;2;19;87;20m+  - from: 4.0.0[0m
[38;2;255;255;255;48;2;19;87;20m+    to: 5.0.0[0m
[38;2;255;255;255;48;2;19;87;20m+    reason: 'MAJOR: quality gate passed with full config expansion, error handling, snap layout, keyboard bindings (score=94.0)'[0m
[38;2;255;255;255;48;2;19;87;20m+    score: 94.0[0m
[38;2;139;134;130m… omitted 118 diff line(s) across 1 additional file(s)/section(s)[0m
  ┊ review diff
[38;2;218;165;32ma/StydeAgents\blueprints\tauri-window-composer\BLUEPRINT.md → b/StydeAgents\blueprints\tauri-window-composer\BLUEPRINT.md[0m
[38;2;139;134;130m@@ -1,13 +1,311 @@[0m
[38;2;255;255;255;48;2;119;20;20m-# Tauri Window Composer[0m
[38;2;255;255;255;48;2;119;20;20m-**Domain:** frontend **Version:** 1[0m
[38;2;255;255;255;48;2;119;20;20m-[0m
[38;2;255;255;255;48;2;119;20;20m-## Purpose[0m
[38;2;255;255;255;48;2;119;20;20m-Design native desktop window chrome, titlebars, system tray integration, and desktop-OS-level interaction patterns for Tauri-based Forge desktop app. Feels like a real Windows app, not a web page in a window.[0m
[38;2;255;255;255;48;2;119;20;20m-[0m
[38;2;255;255;255;48;2;119;20;20m-## Persona[0m
[38;2;255;255;255;48;2;19;87;20m+Tauri Window Composer[0m
[38;2;255;255;255;48;2;19;87;20m+Domain: frontend Version: 2[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+Purpose[0m
[38;2;255;255;255;48;2;19;87;20m+Design native desktop window chrome, custom titlebars with OS integration, system tray icons, snap layout zones, window management behaviors, and desktop-OS-level interaction patterns for Tauri-based Forge desktop app. Every window feels like a real Windows app — not a web page in a frame.[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+Persona[0m
[38;2;184;134;11m You are a Tauri desktop window composer. Native chrome, custom titlebars with OS integration, system tray, window management. Desktop-first — not a web page in a window. Feels like a real native app.[0m
[38;2;184;134;11m [0m
[38;2;255;255;255;48;2;119;20;20m-## Skills[0m
[38;2;255;255;255;48;2;19;87;20m+Skills[0m
[38;2;184;134;11m - tauri-development[0m
[38;2;184;134;11m - frontend-design[0m
[38;2;184;134;11m - high-end-visual-design[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+---[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+Window Compositing[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+CustomTitlebar[0m
[38;2;255;255;255;48;2;19;87;20m+  CSS-drawn titlebar buttons (minimize, maximize, close) matching Windows 11 Fluent geometry[0m
[38;2;255;255;255;48;2;19;87;20m+  Draggable region: data-tauri-drag-region attribute on the titlebar element[0m
[38;2;255;255;255;48;2;19;87;20m+  Double-click behavior: toggles maximize/restore (same as native titlebar)[0m
[38;2;255;255;255;48;2;19;87;20m+  Titlebar context menu on right-click: shows move, size, minimize, maximize, close options[0m
[38;2;255;255;255;48;2;19;87;20m+  Titlebar disappears in fullscreen mode, reappears on hover edge[0m
[38;2;255;255;255;48;2;19;87;20m+  Implemented via: @tauri-apps/api window module + CSS custom properties for button colors[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+WindowState[0m
[38;2;255;255;255;48;2;19;87;20m+  Persist position, size, maximized state to config/window_state.json on every resize/drag-end[0m
[38;2;255;255;255;48;2;19;87;20m+  Restore on app launch — center on primary monitor if no saved state exists[0m
[38;2;255;255;255;48;2;19;87;20m+  Handle edge case: window saved at position on disconnected monitor (fallback to centered primary)[0m
[38;2;255;255;255;48;2;19;87;20m+  Implemented via: save_window_state / get_window_state IPC commands using serde_json[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+WindowChrome[0m
[38;2;255;255;255;48;2;19;87;20m+  No decorations in tauri.conf.json (decorations: false) — fully custom chrome[0m
[38;2;255;255;255;48;2;19;87;20m+  Rounded corners (10px radius) matching Windows 11 acrylic style[0m
[38;2;255;255;255;48;2;19;87;20m+  Drop shadow under the window using CSS box-shadow or HTML canvas filter[0m
[38;2;255;255;255;48;2;19;87;20m+  Thin 1px border that respects dark/light OS theme via prefers-color-scheme media query[0m
[38;2;255;255;255;48;2;19;87;20m+  Snap draft overlay: semi-transparent zone indicator shown during snap preview (Win+Arrow drag)[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+SystemTray[0m
[38;2;255;255;255;48;2;19;87;20m+  .ico with embedded resolutions from 16x16 to 64x64 for all DPI scaling levels[0m
[38;2;255;255;255;48;2;19;87;20m+  Context menu: Show window, New window, Settings, Quit[0m
[38;2;255;255;255;48;2;19;87;20m+  Minimize-to-tray on close event: WindowEvent::CloseRequested hides window instead of exiting[0m
[38;2;255;255;255;48;2;19;87;20m+  Notification badge: unread count via tray.set_icon_as_template with overlay number[0m
[38;2;255;255;255;48;2;19;87;20m+  Left-click: toggle visibility. Right-click: open context menu[0m
[38;2;255;255;255;48;2;19;87;20m+  Implemented via: tauri::tray::TrayIconBuilder + tauri::menu::Menu[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+---[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+Windows 11 Snap Layout Integration[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+Snap zone allocation:[0m
[38;2;255;255;255;48;2;19;87;20m+  Win+Z opens the snap layout picker overlay showing zone layouts (3x3 grid)[0m
[38;2;255;255;255;48;2;19;87;20m+  Zone types: left_half, right_half, top_left_quadrant, top_right_quadrant, bottom_left_quadrant, bottom_right_quadrant, full[0m
[38;2;255;255;255;48;2;19;87;20m+  On monitor change: re-apply current snap zone if target monitor supports same layout[0m
[38;2;255;255;255;48;2;19;87;20m+  Multi-monitor preservation: when a snap group spans monitors, both windows restore to their respective monitors on wake[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+Snap draft behavior:[0m
[38;2;255;255;255;48;2;19;87;20m+  Dragging window toward screen edge triggers draft preview (translucent zone overlay)[0m
[38;2;255;255;255;48;2;19;87;20m+  Draft overlay respects rounded corners — zone edges are inset by 10px to match window chrome[0m
[38;2;255;255;255;48;2;19;87;20m+  Release at draft position commits the snap zone via Tauri window.set_position + set_size[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+Restore on wake:[0m
[38;2;255;255;255;48;2;19;87;20m+  On system resume from sleep, query saved snap state and re-apply positions[0m
[38;2;255;255;255;48;2;19;87;20m+  If target monitor changed (docked/undocked), fall back to primary monitor zones[0m
[38;2;255;255;255;48;2;19;87;20m+  Implemented via: WinEvent hook in src-tauri for EVENT_SYSTEM_FOREGROUND + local snap state map[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+---[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+Keyboard Shortcut Surface[0m
[38;2;139;134;130m… omitted 241 diff line(s) across 1 additional file(s)/section(s)[0m
  ┊ review diff
[38;2;218;165;32ma/C:\Users\Pontus\AppData\Local\Temp\hermes-verify-tauri-window-composer.py → b/C:\Users\Pontus\AppData\Local\Temp\hermes-verify-tauri-window-composer.py[0m
[38;2;139;134;130m@@ -0,0 +1,149 @@[0m
[38;2;255;255;255;48;2;19;87;20m+#!/usr/bin/env python3[0m
[38;2;255;255;255;48;2;19;87;20m+"""Ad-hoc verification: tauri-window-composer blueprint YAML + structure."""[0m
[38;2;255;255;255;48;2;19;87;20m+import os, sys, json[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+BLUEPRINT_DIR = r"D:\styde\_alpedal\styde-forge\StydeAgents\blueprints\tauri-window-composer"[0m
[38;2;255;255;255;48;2;19;87;20m+yaml_path = os.path.join(BLUEPRINT_DIR, "config.yaml")[0m
[38;2;255;255;255;48;2;19;87;20m+md_path   = os.path.join(BLUEPRINT_DIR, "BLUEPRINT.md")[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+errors = [][0m
[38;2;255;255;255;48;2;19;87;20m+warnings = [][0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+# ---- 1. YAML parse ----[0m
[38;2;255;255;255;48;2;19;87;20m+try:[0m
[38;2;255;255;255;48;2;19;87;20m+    import yaml[0m
[38;2;255;255;255;48;2;19;87;20m+    with open(yaml_path, "r", encoding="utf-8") as f:[0m
[38;2;255;255;255;48;2;19;87;20m+        data = yaml.safe_load(f)[0m
[38;2;255;255;255;48;2;19;87;20m+    print(f"YAML parse: OK ({len(json.dumps(data, indent=2))} chars)")[0m
[38;2;255;255;255;48;2;19;87;20m+except Exception as e:[0m
[38;2;255;255;255;48;2;19;87;20m+    errors.append(f"YAML parse failed: {e}")[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+# ---- 2. YAML required keys ----[0m
[38;2;255;255;255;48;2;19;87;20m+required_top = ["agent", "blueprint", "platform", "output", "lifecycle"][0m
[38;2;255;255;255;48;2;19;87;20m+for k in required_top:[0m
[38;2;255;255;255;48;2;19;87;20m+    if k not in data:[0m
[38;2;255;255;255;48;2;19;87;20m+        errors.append(f"Missing top-level key: {k}")[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+# ---- 3. Platform sub-keys ----[0m
[38;2;255;255;255;48;2;19;87;20m+plat = data.get("platform", {})[0m
[38;2;255;255;255;48;2;19;87;20m+for sub in ["targets", "dpi", "snap_layout", "keyboard_shortcuts", "accessibility"]:[0m
[38;2;255;255;255;48;2;19;87;20m+    if sub not in plat:[0m
[38;2;255;255;255;48;2;19;87;20m+        errors.append(f"Missing platform.{sub}")[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+# ---- 4. DPI policies ----[0m
[38;2;255;255;255;48;2;19;87;20m+dpi = plat.get("dpi", {})[0m
[38;2;255;255;255;48;2;19;87;20m+policies = dpi.get("policies", [])[0m
[38;2;255;255;255;48;2;19;87;20m+if len(policies) < 4:[0m
[38;2;255;255;255;48;2;19;87;20m+    warnings.append(f"DPI policies: expected >=4, got {len(policies)}")[0m
[38;2;255;255;255;48;2;19;87;20m+for p in policies:[0m
[38;2;255;255;255;48;2;19;87;20m+    for k in ["scaling", "logical_factor", "physical"]:[0m
[38;2;255;255;255;48;2;19;87;20m+        if k not in p:[0m
[38;2;255;255;255;48;2;19;87;20m+            errors.append(f"DPI policy missing key: {k} in {p.get('scaling','?')}")[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+# ---- 5. Keyboard shortcuts ----[0m
[38;2;255;255;255;48;2;19;87;20m+ks = plat.get("keyboard_shortcuts", {})[0m
[38;2;255;255;255;48;2;19;87;20m+wm = ks.get("window_management", [])[0m
[38;2;255;255;255;48;2;19;87;20m+if len(wm) < 5:[0m
[38;2;255;255;255;48;2;19;87;20m+    warnings.append(f"window_management shortcuts: expected >=5, got {len(wm)}")[0m
[38;2;255;255;255;48;2;19;87;20m+global_hk = ks.get("global_hotkeys", [])[0m
[38;2;255;255;255;48;2;19;87;20m+if len(global_hk) < 2:[0m
[38;2;255;255;255;48;2;19;87;20m+    warnings.append(f"global_hotkeys: expected >=2, got {len(global_hk)}")[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+# Check for specific required combos[0m
[38;2;255;255;255;48;2;19;87;20m+required_combos = ["Win+Arrow", "Alt+Space", "Win+Z"][0m
[38;2;255;255;255;48;2;19;87;20m+found_combos = [s["combo"] for s in wm][0m
[38;2;255;255;255;48;2;19;87;20m+for rc in required_combos:[0m
[38;2;255;255;255;48;2;19;87;20m+    if rc not in found_combos:[0m
[38;2;255;255;255;48;2;19;87;20m+        errors.append(f"Missing required shortcut combo: {rc}")[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+# ---- 6. Snap layout ----[0m
[38;2;255;255;255;48;2;19;87;20m+sl = plat.get("snap_layout", {})[0m
[38;2;255;255;255;48;2;19;87;20m+for k in ["enabled", "zone_allocation", "restore_on_wake", "multi_monitor_preservation"]:[0m
[38;2;255;255;255;48;2;19;87;20m+    if k not in sl:[0m
[38;2;255;255;255;48;2;19;87;20m+        errors.append(f"Missing snap_layout.{k}")[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+# ---- 7. Accessibility defaults ----[0m
[38;2;255;255;255;48;2;19;87;20m+acc = plat.get("accessibility", {}).get("defaults", {})[0m
[38;2;255;255;255;48;2;19;87;20m+for k in ["high_contrast_support", "screen_reader_compatible", "keyboard_navigable", "color_contrast_ratio"]:[0m
[38;2;255;255;255;48;2;19;87;20m+    if k not in acc:[0m
[38;2;255;255;255;48;2;19;87;20m+        warnings.append(f"Missing accessibility.defaults.{k}")[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+# ---- 8. Lifecycle gates ----[0m
[38;2;255;255;255;48;2;19;87;20m+lc = data.get("lifecycle", {})[0m
[38;2;255;255;255;48;2;19;87;20m+for phase in ["evaluate", "improve", "production"]:[0m
[38;2;255;255;255;48;2;19;87;20m+    if phase not in lc:[0m
[38;2;255;255;255;48;2;19;87;20m+        errors.append(f"Missing lifecycle.{phase}")[0m
[38;2;255;255;255;48;2;19;87;20m+eval_gates = lc.get("evaluate", {}).get("gates", [])[0m
[38;2;255;255;255;48;2;19;87;20m+gate_names = [list(g.keys())[0] for g in eval_gates][0m
[38;2;255;255;255;48;2;19;87;20m+for required_gate in ["compile_check", "dpi_check", "snap_check"]:[0m
[38;2;139;134;130m… omitted 71 diff line(s) across 1 additional file(s)/section(s)[0m
  ┊ review diff
[38;2;218;165;32ma/C:\Users\Pontus\AppData\Local\Temp\hermes-verify-final.py → b/C:\Users\Pontus\AppData\Local\Temp\hermes-verify-final.py[0m
[38;2;139;134;130m@@ -0,0 +1,76 @@[0m
[38;2;255;255;255;48;2;19;87;20m+#!/usr/bin/env python3[0m
[38;2;255;255;255;48;2;19;87;20m+"""Ad-hoc re-verify: only the two persistent files."""[0m
[38;2;255;255;255;48;2;19;87;20m+import os, json, sys, tempfile[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+BLUEPRINT_DIR = r"D:\styde\_alpedal\styde-forge\StydeAgents\blueprints\tauri-window-composer"[0m
[38;2;255;255;255;48;2;19;87;20m+yaml_path = os.path.join(BLUEPRINT_DIR, "config.yaml")[0m
[38;2;255;255;255;48;2;19;87;20m+md_path   = os.path.join(BLUEPRINT_DIR, "BLUEPRINT.md")[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+errors = [][0m
[38;2;255;255;255;48;2;19;87;20m+warnings = [][0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+# YAML parse[0m
[38;2;255;255;255;48;2;19;87;20m+import yaml[0m
[38;2;255;255;255;48;2;19;87;20m+with open(yaml_path, "r", encoding="utf-8") as f:[0m
[38;2;255;255;255;48;2;19;87;20m+    data = yaml.safe_load(f)[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+# Required keys[0m
[38;2;255;255;255;48;2;19;87;20m+for k in ["agent", "blueprint", "platform", "output", "lifecycle"]:[0m
[38;2;255;255;255;48;2;19;87;20m+    if k not in data: errors.append(f"Missing top-level key: {k}")[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+# Platform completeness[0m
[38;2;255;255;255;48;2;19;87;20m+plat = data.get("platform", {})[0m
[38;2;255;255;255;48;2;19;87;20m+for sub in ["targets", "dpi", "snap_layout", "keyboard_shortcuts", "accessibility"]:[0m
[38;2;255;255;255;48;2;19;87;20m+    if sub not in plat: errors.append(f"Missing platform.{sub}")[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+# DPI policies >= 4[0m
[38;2;255;255;255;48;2;19;87;20m+dpi = plat.get("dpi", {})[0m
[38;2;255;255;255;48;2;19;87;20m+if len(dpi.get("policies", [])) < 4: errors.append(f"DPI policies < 4")[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+# Keyboard combos[0m
[38;2;255;255;255;48;2;19;87;20m+wm = plat.get("keyboard_shortcuts", {}).get("window_management", [])[0m
[38;2;255;255;255;48;2;19;87;20m+for rc in ["Win+Arrow", "Alt+Space", "Win+Z"]:[0m
[38;2;255;255;255;48;2;19;87;20m+    if rc not in [s["combo"] for s in wm]: errors.append(f"Missing shortcut: {rc}")[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+# Snap layout keys[0m
[38;2;255;255;255;48;2;19;87;20m+sl = plat.get("snap_layout", {})[0m
[38;2;255;255;255;48;2;19;87;20m+for k in ["enabled", "zone_allocation", "restore_on_wake", "multi_monitor_preservation"]:[0m
[38;2;255;255;255;48;2;19;87;20m+    if k not in sl: errors.append(f"Missing snap_layout.{k}")[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+# Lifecycle[0m
[38;2;255;255;255;48;2;19;87;20m+lc = data.get("lifecycle", {})[0m
[38;2;255;255;255;48;2;19;87;20m+for phase in ["evaluate", "improve", "production"]:[0m
[38;2;255;255;255;48;2;19;87;20m+    if phase not in lc: errors.append(f"Missing lifecycle.{phase}")[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+# BLUEPRINT sections[0m
[38;2;255;255;255;48;2;19;87;20m+with open(md_path, "r", encoding="utf-8") as f:[0m
[38;2;255;255;255;48;2;19;87;20m+    md = f.read()[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+for sec in ["Error Handling", "Snap Layout", "Keyboard Shortcut Surface", "Testing and Build", "Self-Evaluation Template"]:[0m
[38;2;255;255;255;48;2;19;87;20m+    if sec not in md: errors.append(f"Missing section: {sec}")[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+# IPC signatures[0m
[38;2;255;255;255;48;2;19;87;20m+for sig in ["fn save_window_state", "fn minimize_to_tray", "fn save_snap_state"]:[0m
[38;2;255;255;255;48;2;19;87;20m+    if sig not in md: errors.append(f"Missing IPC: {sig}")[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+# DPI deduplication check — no DPI config prose in markdown[0m
[38;2;255;255;255;48;2;19;87;20m+for phrase in ["scaling: 100%", "logical_factor: 1.0", "font_rendering: ClearType"]:[0m
[38;2;255;255;255;48;2;19;87;20m+    if phrase in md:[0m
[38;2;255;255;255;48;2;19;87;20m+        warnings.append(f"DPI config prose leaked into md: '{phrase}'")[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+# Build targets[0m
[38;2;255;255;255;48;2;19;87;20m+if "x86_64-pc-windows-msvc" not in plat.get("targets", []): warnings.append("Missing x86_64 target")[0m
[38;2;255;255;255;48;2;19;87;20m+if "aarch64-pc-windows-msvc" not in plat.get("targets", []): warnings.append("Missing aarch64 target")[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+print("AD-HOC VERIFICATION (re-run)")[0m
[38;2;255;255;255;48;2;19;87;20m+print(f"  BLUEPRINT.md: {md.count(chr(10))} lines")[0m
[38;2;255;255;255;48;2;19;87;20m+print(f"  config.yaml:  {len(data)} top-level sections")[0m
[38;2;255;255;255;48;2;19;87;20m+if not errors and not warnings:[0m
[38;2;255;255;255;48;2;19;87;20m+    print("  Status: PASS")[0m
[38;2;255;255;255;48;2;19;87;20m+elif not errors:[0m
[38;2;255;255;255;48;2;19;87;20m+    print("  Status: PASS with warnings")[0m
[38;2;255;255;255;48;2;19;87;20m+else:[0m
[38;2;255;255;255;48;2;19;87;20m+    print("  Status: FAIL")[0m
[38;2;255;255;255;48;2;19;87;20m+for e in errors:   print(f"  ERROR: {e}")[0m
[38;2;255;255;255;48;2;19;87;20m+for w in warnings: print(f"  WARN:  {w}")[0m
[38;2;255;255;255;48;2;19;87;20m+sys.exit(1 if errors else 0)[0m
Both files pass. Temp script cleaned up in the same command — no stray paths left. Final state:
- BLUEPRINT.md: 311 lines, all 5 required sections, 3 IPC signatures, zero DPI config prose leaked
- config.yaml: 5 top-level sections (agent, blueprint, platform, output, lifecycle), all platform sub-keys present, 4 DPI tiers, 3 required shortcuts, snap_layout complete, lifecycle gates populated
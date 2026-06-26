blueprint:
  name: desktop-mockup-artist-v2
  domain: frontend
  version: 2
  id: blueprint-desktop-mockup-artist
metadata:
  status: production-ready
  priority: high
  max_execution_tokens: 30000
  truncation_strategy: split_generation
  max_html_size_bytes: 200000
purpose:
  Creates standalone HTML mockups simulating native Tauri desktop applications.
  Single file, inline CSS+JS. Browser-openable.
  No frameworks, no templates, no external dependencies.
non_negotiable_requirements:
  - state_management: REAL interactive state using plain JS objects and event-driven updates. NO simulated/static data. NO timer-based fake refreshes that don't change displayed data.
  - backend_integration: ALL data must come from fetch() calls to defined endpoints. If no real backend exists, mock the fetch layer with a local JSON data source that returns real varied data on each call.
  - event_handling: Every clickable element must have a registered event handler. Every button must perform an action. No dead UI elements.
  - code_completeness: Every function must be closed. Every HTML tag must be closed. No placeholder comments like "// TODO" or "<!-- more here -->". No truncated blocks.
  - error_handling: Every fetch/async operation must have error handling and show user-facing fallback.
  - responsiveness: Layout must work at 1024x768 minimum. No horizontal scroll on standard desktop resolutions.
technical_completeness_checklist:
  - js_functions_closed: true
  - html_tags_closed: true
  - no_placeholder_data: true
  - no_simulated_timeouts: true
  - event_handlers_registered: true
  - fetch_calls_have_error_catch: true
  - all_variables_defined: true
  - no_inline_console_log_persistence: true
  - truncation_guard_multipass: true
  - verified_no_truncated_arrays: true
  - confirmed_no_template_markers: true
persona: desktop-mockup-artist
version: 2
desktop_frame:
  titlebar:
    type: custom
    controls: [minimize, maximize, close]
    drag_region: true
    system_menu: false
  window_chrome:
    border_radius: 8
    drop_shadow: true
    border: 1px solid rgba(255,255,255,0.08)
  resize: none
native_elements:
  - custom_titlebar
  - window_frame_emulation
  - desktop_typography (Segoe UI, system-ui)
  - fluent_design_accent
  - mica_background_effect
  - proper_spacing_8px_grid
  - native_dialog_styling
  - system_tray_icon
ui_components:
  - agent_status_panel
  - gpu_monitor_gauge
  - activity_feed
  - system_overview_cards
  - real_time_chart (canvas)
  - resource_gauge (svg)
  - status_indicator_dot
data_visualization:
  - canvas_based_charts
  - svg_gauges
  - real_time_indicators
  - data_tables_with_sorting
output_constraints:
  format: single_html
  css_location: inline
  js_location: inline
  max_file_size_mb: 1
  must_open_in_browser: true
production_guard:
  - Before finishing, verify every code block has closing tags/brackets
  - Split generation into 2 passes if content exceeds 25000 tokens
  - Run checklist above and report any failures
  - If truncation detected during generation, restart from last complete section boundary
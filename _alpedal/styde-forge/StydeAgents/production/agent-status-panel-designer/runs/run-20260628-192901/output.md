Agent Status Panel — mockup specification
mockup_id: forge-agent-status-panel-v1
domain: frontend
phase: fas-0.5
format: spec + ascii wireframe
layout:
  type: dashboard_grid
  columns: 3
  rows: auto
  breakpoints:
    - width_gt: 1200px -> columns: 4
    - width_gt: 800px -> columns: 3
    - width_lt: 800px -> columns: 1
panel_structure:
  top_bar:
    - left: "Forge Agent Status" (h2, sans-serif, weight 600)
    - center: run_selector (dropdown: current_run_id, latest 5 runs)
    - right: global_status_badge (color-coded: green=all_idle, yellow=any_running, red=any_failed)
  stats_row:
    layout: horizontal, 4x stat_cards
    cards:
      - label: "Total Agents"
        value: integer
        icon: grid
      - label: "Running"
        value: integer
        icon: spinner (animated dot pulse)
        color: #3B82F6 (blue)
      - label: "Pending"
        value: integer
        icon: clock
        color: #F59E0B (amber)
      - label: "Completed"
        value: integer
        icon: check-circle
        color: #10B981 (green)
  agent_grid:
    card_template:
      width: 360px
      height: 180px
      padding: 16px
      border_radius: 12px
      background: #1e1e2e (dark theme)
      border: 1px solid #313244
      hover_border: 1px solid #45475a
      shadow: 0 4px 12px rgba(0,0,0,0.3)
      transition: border 0.15s ease
      header:
        - agent_name: string (monospace, weight 600, size 14px)
        - status_dot:
            size: 10px
            border_radius: 50%
            running: background #3B82F6, pulse_animation (1s cycle)
            pending: background #F59E0B, slow_pulse (2s cycle)
            completed: background #10B981, static
            failed: background #EF4444, static
            idle: background #6B7280, static
      score_section:
        layout: centered, large number
        composite_score:
          value: float (0-100)
          precision: 1 decimal
          size: 36px
          weight: 700
          color_gradient:
            - threshold: 85 -> #10B981 (green)
            - threshold: 70 -> #F59E0B (amber)
            - threshold: 0  -> #EF4444 (red)
        label: "COMPOSITE" (uppercase, tracking 2px, size 10px, color #6B7280)
      dimension_bars:
        layout: horizontal, 3 mini bars
        bars:
          - label: "C" (completeness)
          - label: "A" (accuracy)
          - label: "U" (usefulness)
        style:
          height: 4px
          border_radius: 2px
          background_track: #2a2a3e
          fill_color: #a6adc8
          width: 60px
          label_size: 9px
      footer:
        - last_run: timestamp (relative, e.g. "2m ago")
        - blueprint_count: integer + "BPs"
        - action_badge: "PROMOTE" / "ROLLBACK" / "ARCHIVE" (pill, uppercase, size 10px)
    empty_state:
      text: "No agents running. Start a forge run to populate."
      icon: package
      cta: button "New Run"
  detail_expansion:
    trigger: click card
    animation: slide_down (height auto, duration 0.2s)
    expanded_content:
      dimensions_table:
        columns: [dimension, score, trend, change]
        rows:
          - dimension: "Completeness"
          - dimension: "Accuracy"
          - dimension: "Usefulness"
        trend_indicators: arrow_up (green), arrow_down (red), dash (flat)
        change: delta from previous run (+/- x.x)
      subcomponent_list:
        type: inline tags
        max_visible: 6
        overflow: "+N more" tooltip
      action_buttons:
        - "View Logs" -> links to run_log
        - "Promote to Prod" -> confirmation dialog
        - "Re-run" -> triggers new run
  color_palette:
    background: #181825 (base)
    card_bg: #1e1e2e
    text_primary: #cdd6f4
    text_secondary: #6c7086
    accent: #89b4fa
    success: #a6e3a1
    warning: #f9e2af
    danger: #f38ba8
    muted: #45475a
  animations:
    status_pulse: keyframes scale 1.0 -> 1.3 -> 1.0, opacity 0.8 -> 1.0 -> 0.8
    score_roll: counter animation, 0 -> final value over 400ms
    card_enter: fade in + translateY(8px) with stagger (50ms per card)
  responsive_behaviour:
    mobile_single_column: cards stack full width
    tablet_two_up: 2 columns
    desktop_three_up: 3 columns
    wide_four_up: 4 columns
  implementation_notes:
    - use CSS Grid for flexibility, not flexbox for the card layout itself
    - prefer CSS animations over JS-driven animation for status pulse
    - data refresh via Server-Sent Events (SSE) on /api/forge/agent-status/stream
    - composite score color is a computed CSS gradient, no JS colour logic needed
    - promote/rollback badge controlled by backend sending promotion_state field
ASCII wireframe (desktop 3-up):
+------------------------------------------------------------------+
| Forge Agent Status                      [run: forge-20260628]  [?]|
+------------------------------------------------------------------+
| [12 Agents]  [2 Running ...]  [1 Pending]  [9 Completed]         |
+------------------------------------------------------------------+
| +------------------+  +------------------+  +------------------+ |
| | agent-structure-  |  | agent-extract-   |  | agent-score-hol- | |
| | text-v3      [...]|  | transform    [...]|  | ist      [...]   | |
| | 92.6              |  | 88.3              |  | 74.1              | |
| | COMPOSITE         |  | COMPOSITE         |  | COMPOSITE         | |
| | C [====---] A [== |  | C [=====--] A [== |  | C [===----] A [= | |
| | ====--] U [=====- |  | =====] U [======= |  | =====--] U [==== | |
| | ---]              |  | ----]             |  | ----]             | |
| | 2m ago  • 12 BPs  |  | 5m ago  • 8 BPs   |  | 18m ago • 6 BPs  | |
| | [ARCHIVE]         |  | [PROMOTE]         |  | [ROLLBACK]        | |
| +------------------+  +------------------+  +------------------+ |
| +------------------+  +------------------+  +------------------+ |
| | agent-memory-     |  | agent-feedback-  |  | agent-cache-     | |
| | aligner      [...]|  | aggregator   [...]|  | warmer      [...] | |
| | 67.2              |  | 91.0              |  | 79.5              | |
| | COMPOSITE         |  | COMPOSITE         |  | COMPOSITE         | |
| | C [==-----] A [== |  | C [=======-] A [== |  | C [====---] A [= | |
| | =====--] U [===== |  | ======] U [======= |  | =====--] U [==== | |
| | ----]             |  | ----]             |  | ----]             | |
| | 45m ago • 5 BPs   |  | 1h ago  • 15 BPs  |  | 2h ago  • 3 BPs  | |
| | [ARCHIVE]         |  | [ARCHIVE]         |  | [ARCHIVE]         | |
| +------------------+  +------------------+  +------------------+ |
+------------------------------------------------------------------+
Detail panel (expanded view on click):
+------------------------------------------------------------------+
| agent-extract-transform                               [x] close   |
| Composite: 88.3                                      [88.3 -> ...]|
+------------------------------------------------------------------+
| Dimension     |  Score  | Trend | Change                        |
| Completeness  |  90.0   |   up  | +2.4 from previous run        |
| Accuracy      |  85.0   |  flat | -0.3 from previous run        |
| Usefulness    |  90.0   |   up  | +5.1 from previous run        |
+------------------------------------------------------------------+
| Subcomponents: [health-bar] [status-dot] [accessibility]         |
|                [data-contract] [mockup-refs] +2 more             |
+------------------------------------------------------------------+
| [View Logs]  [Promote to Prod]  [Re-run Agent]                  |
+------------------------------------------------------------------+
Deliverable: mockup spec ready for handoff to frontend implementation.
AGENT STATUS PANEL DASHBOARD — FAS 0.5 MOCKUPS
MOCKUP 1: AGENT GRID OVERVIEW
Layout: 4-column responsive grid. Each cell is a 280px x 180px card with 12px border-radius, 1px solid border (#1e293b), background (#0f172a). Gap: 16px.
Card structure (top to bottom, y-coordinates from card top):
y=0 to y=4: Status bar — 4px tall colored strip. Full card width. Color determined by agent health: green (#22c55e) for healthy, amber (#f59e0b) for degraded, red (#ef4444) for critical, gray (#64748b) for idle.
y=12: Agent avatar — 32px circle, left-aligned at x=12. Contains first two letters of agent name in 14px semibold (#f8fafc). Background matches status color at 20% opacity.
y=12: Agent name — x=52. 15px semibold inter, color #f1f5f9. Max width 180px, ellipse overflow.
y=12: Status badge — right-aligned at card-right-margin minus 12. 8px circle + label. Circle color matches status bar. Label text: RUNNING (12px, #22c55e), PENDING (12px, #f59e0b), COMPLETED (12px, #3b82f6), FAILED (12px, #ef4444), IDLE (12px, #64748b).
y=40: Score bar — full width minus 24px margins (256px). 4px tall background track (#1e293b). Fill height 4px, color: gradient from (#22c55e) at 0% to (#3b82f6) at 100%. Fill width = score percentage. Left of bar: Score label text (12px, #94a3b8). Right of bar: numeric score (14px bold, #f1f5f9) — e.g. 92/100.
y=56: Divider — 1px line (#1e293b), width 256px, centered at x=12.
y=64: Metric row 1 — three columns. Each: icon (12px) + value (14px semibold, #e2e8f0) + label (11px, #64748b) stacked vertically. Columns: Tasks (count from active run), Tokens (k used), Time (elapsed mm:ss). Each column width 85px, left-aligned.
y=100: Metric row 2 — three columns same layout. Columns: Quality (current avg score), Speed (tokens/sec), Iterations (loop count).
y=124: Progress bar — full width minus 24px. 6px tall, rounded (#64748b fill at 30% opacity, #3b82f6 at 100%). Label on right: 3/5 (12px, #94a3b8) meaning step 3 of 5.
y=144: Footer strip — 6px tall, background (#0c1322). Contains last-updated timestamp in 10px (#475569): Updated 12s ago. Right-aligned.
Hover state: Card lifts 2px with box-shadow 0 4px 20px rgba(0,0,0,0.4). Border changes to (#334155).
Selected state: Left border 3px solid (#3b82f6) instead of top status bar. Background shifts (#0f172a to #131d31).
Empty state: Card shows dashed border (#1e293b), centered 48px ghost icon (opacity 20%), text below saying No agents running in 13px (#475569). CTA button: + Start Agent (12px, #3b82f6, rounded 6px).
MOCKUP 2: AGENT DETAIL PANEL (RIGHT SIDEBAR)
Slides in from right edge. Width: 420px. Full height (900px). Background (#0f172a). Left border: 1px solid (#1e293b). Scrollable with custom scrollbar (6px, #1e293b track, #334155 thumb, rounded).
y=0 to y=60: Header bar. Fixed position. Background (#0f172a) with bottom border 1px (#1e293b). Padding: 16px horizontal, 12px vertical.
  x=16: Agent avatar 40px circle (same style as grid).
  x=68: Agent name 18px semibold (#f8fafc). Below: role/type label 12px (#64748b).
  Right side: Close button (32x32, icon, #64748b hover #f1f5f9).
y=72: Health indicator row. Three blocks, each 118px wide, 56px tall, background (#0c1322), border-radius 8px. Padding 10px.
  Block 1 (left): Status icon + UP text (13px, #22c55e). Below: Uptime 2h 14m (12px, #64748b).
  Block 2 (center): Timer icon + Tasks label (13px, #64748b). Below: count 18 (24px bold, #f1f5f9).
  Block 3 (right): Score icon + Quality label (13px, #64748b). Below: score 92 (24px bold, #3b82f6).
y=140: Score timeline chart. Width 388px (420-32). Height 120px. Background (#0c1322) border-radius 8px. Padding 16px.
  Y-axis: labels at 0, 50, 100 (10px, #475569). Two horizontal gridlines (1px dashed, #1e293b).
  X-axis: last 10 runs, labeled by run number (10px, #475569), rotated 45 degrees if needed.
  Line: 2px solid (#3b82f6), interpolated between data points. Area fill: gradient from (#3b82f6 at 10% opacity) to (transparent at bottom).
  Current run highlighted with 8px circle dot at data point.
  Tooltip on hover: 12px tooltip box with rounded 6px, background (#1e293b), border (#334155). Shows Run 7 — Score: 92 — 2m ago.
  Below chart: Trend label — Rising +4 from last run (12px, #22c55e) or Falling -3 (12px, #ef4444).
y=272: Detail section label: RUN LOG (11px uppercase, #64748b, tracking 0.5). Below: divider line.
y=286 to y=end: Scrollable run log entries. Each entry:
  56px tall, padding 12px 16px. Alternating background (even: transparent, odd: rgba(30,41,59,0.3)).
  Left: Circle status indicator 8px (#22c55e/#3b82f6/#f59e0b/#ef4444).
  x=32: Run name 13px semibold (#e2e8f0). Max width 300px.
  Below: Timestamp (11px, #475569) + Duration (11px, #475569) separated by a middle dot.
  Right: Score badge 28px wide, 20px tall, rounded 4px, background (#1e293b), text 11px bold (#f1f5f9).
MOCKUP 3: STATUS BANNER & TOP BAR
Full-width banner below main nav. Height: 48px. Background (#0c1322). Bottom border: 1px solid (#1e293b).
Layout (horizontal flex, center-aligned, padding 0 24px):
Left group: Aggregate status indicator. Pulsing 10px circle (#22c55e) with CSS animation duration 2s, opacity pulse 0.4 to 1.0. Text: All Systems Operational (14px, #e2e8f0) or n Degraded (14px, #f59e0b) or n Down (14px, #ef4444). Margin-right: 24px.
Divider: 1px tall line (#1e293b), height 24px, vertical center.
Center group: Count chips. Three chips, each 20px tall padding 6px 10px, rounded 10px.
  Chip 1: Running count. Background rgba(34,197,94,0.15). Text "3 running" (12px, #22c55e).
  Chip 2: Pending count. Background rgba(245,158,11,0.15). Text "2 pending" (12px, #f59e0b).
  Chip 3: Completed today count. Background rgba(59,130,246,0.15). Text "18 completed" (12px, #3b82f6).
Right group (flex, gap 12px, right-aligned):
  Refresh button: 32px, icon only, background (#1e293b) hover (#334155), rounded 6px. Tooltip: Refresh status (12px).
  Filter dropdown: 120px wide, 32px tall, background (#1e293b), border 1px (#334155), rounded 6px, text (12px, #e2e8f0). Options: All Agents, Running Only, Failed Only, By Blueprint.
  View toggle: Two 32x32 icon buttons. Grid icon (active: #3b82f6, inactive: #64748b). List icon (active/inactive same). Background (#1e293b), rounded 6px. Active button has border (#3b82f6).
MOCKUP 4: EMPTY STATE / ONBOARDING VIEW
Full-height page. Centered content area at y=240px (of 900px viewport).
Center column: 420px max width. Centered horizontally.
Great icon: 80px circle (#1e293b background, 30% opacity agent icon #64748b). Centered.
y=24 below icon: Headline — Start Your First Agent (22px, #f1f5f9, semibold).
y=12 below headline: Subtitle — No agents running yet. Create a blueprint or launch from a template to get started. (14px, #64748b, max-width 360px centered).
y=32 below subtitle: CTA Button — 200px wide, 44px tall, background (#3b82f6), hover (#2563eb), border-radius 8px. Text: + New Agent (14px, #ffffff, semibold). Box-shadow on hover: 0 4px 12px rgba(59,130,246,0.3).
y=16 below CTA: Secondary link — Or browse blueprints (13px, #3b82f6). Underline on hover.
y=40 below secondary link: Feature highlights row — three cards side by side, each 116px wide, 80px tall, background (#0c1322), border-radius 8px, border 1px (#1e293b). Padding 8px.
  Card 1: Icon (24px) + title (12px, #e2e8f0) + desc (11px, #64748b). Title: Automated. Desc: no manual oversight.
  Card 2: Icon + title (12px, #e2e8f0) + desc. Title: Trackable. Desc: real-time scores.
  Card 3: Icon + title (12px, #e2e8f0) + desc. Title: Composable. Desc: chain blueprints.
MOCKUP 5: LIST VIEW ALTERNATIVE
When list view toggle is active (mockup 3). Replaces grid.
Full-width table. Header background (#0c1322). Sticky top. 
Columns (left to right):
  Col 1 (40px): Status dot (8px circle) — center aligned.
  Col 2 (180px): Agent Name — 14px semibold (#f1f5f9). Below: type label 11px (#64748b).
  Col 3 (80px): Score — 14px bold (#f1f5f9). Below: trend arrow (12px, #22c55e or #ef4444).
  Col 4 (70px): Tasks — 13px (#e2e8f0).
  Col 5 (90px): Progress — 60px wide progress bar (6px tall) + step label (11px, #64748b) right of bar.
  Col 6 (90px): Duration — 13px (#e2e8f0). Below: started time (11px, #64748b).
  Col 7 (70px): Status badge — chip (same styles as mockup 3 count chips).
  Col 8 (40px): Action — three-dot menu icon, 32x32 (#64748b hover #e2e8f0).
Row height: 52px. Alternating background (#0f172a and #0c1322). Hover: background (#131d31). Selected: left border 3px (#3b82f6).
Column headers: 12px uppercase (#64748b), tracking 0.5, padding 8px 12px. Sortable: click shows up/down arrow indicator (10px, #3b82f6) on active sort column.
Pagination at bottom: 40px tall, centered. Page numbers as circles (24px, #1e293b background, #64748b text). Active page: (#3b82f6 background, white text). Prev/Next arrows (24x24 icons). Text: Showing 1-10 of 47 agents (12px, #64748b).
MOCKUP 6: ANIMATION SPEC
All transitions 200ms ease-in-out unless overridden.
Card hover: transform translateY(-1px), box-shadow change. 200ms.
Status dot pulse: keyframes pulse 2s ease-in-out infinite. 0% opacity 0.4, 50% opacity 1.0, 100% opacity 0.4.
Progress bar fill: width transition 300ms ease-out.
Panel slide-in: right sidebar transform translateX(420px) to translateX(0). 250ms cubic-bezier(0.16, 1, 0.3, 1). On close: reverse 200ms.
Score timeline draw: pathLength animation 800ms ease-out on initial render. Data dots stagger: 50ms delay each.
Count chips: scale(0.95) to scale(1.0) on mount. 150ms ease-out staggered 20ms per chip.
Refresh spinner: rotate 360deg 800ms linear infinite. Only during refresh state.
Tooltip: opacity 0 to 1, 100ms. No delay on hover, 200ms delay on hide.
Skeleton loading: shimmer animation on placeholder cards. background linear-gradient(90deg, #0c1322 25%, #131d31 50%, #0c1322 75%). Background-size 200%. Keyframes: bg-position 200% 0 to -200% 0. 1.2s linear infinite.
TOKEN FAMILIES REQUIRED
animation-timing:
  duration-fast: 100ms
  duration-normal: 200ms
  duration-slow: 300ms
  duration-draw: 800ms
  easing-default: ease-in-out
  easing-spring: cubic-bezier(0.16, 1, 0.3, 1)
  easing-linear: linear
semantic-colors (dark theme):
  surface-base: #0f172a
  surface-elevated: #0c1322
  surface-hover: #131d31
  surface-card: #0f172a
  border-default: #1e293b
  border-hover: #334155
  text-primary: #f8fafc
  text-secondary: #e2e8f0
  text-muted: #94a3b8
  text-subdued: #64748b
  text-disabled: #475569
  status-running: #22c55e
  status-pending: #f59e0b
  status-completed: #3b82f6
  status-failed: #ef4444
  status-idle: #64748b
  accent-primary: #3b82f6
  accent-hover: #2563eb
light mode mapping:
  surface-base -> #ffffff
  surface-elevated -> #f8fafc
  surface-hover -> #f1f5f9
  surface-card -> #ffffff
  border-default -> #e2e8f0
  border-hover -> #cbd5e1
  text-primary -> #0f172a
  text-secondary -> #1e293b
  text-muted -> #475569
  text-subdued -> #94a3b8
  text-disabled -> #cbd5e1
  status colors: same hex values (status colors stay consistent across themes)
  accent-primary: #2563eb
  accent-hover: #1d4ed8
VISUAL SPECS — PIXEL PRECISION
Grid card: 280x180px, border-radius 12px, border 1px solid.
Status bar height: 4px, full card width, no border-radius on top (covered by parent border-radius).
Avatar: 32px circle, font 14px semibold, line-height 32px, text-align center.
Score bar track: 4px tall, full width minus 24px, border-radius 2px (same as track).
Score bar fill: height 4px, border-radius 2px, width = score% of available space.
Progress bar: 6px tall, border-radius 3px, fill same.
Count chip: height 20px, padding 6px 10px, border-radius 10px.
Detail panel: 420px wide, full height, left border 1px solid, no horizontal scroll.
Health block: 118px wide, 56px tall, border-radius 8px, padding 10px.
Timeline chart: 388px wide, 120px tall, border-radius 8px, padding 16px, 2px solid line.
List row: height 52px, no border-radius, left border 3px on selected state.
Page number circle: 24px diameter, border-radius 50%.
Table header: padding 8px 12px, font 12px uppercase tracking 0.5.
Spacing unit: 4px base grid. All margin/padding values are multiples of 4px.
Grid gap: 16px (4 units).
MOCKUP 1 OF 6 — AGENT GRID CARD
--- CORE SPEC ---
Component: agent-card
Container: 280px wide, 340px tall, border-radius 12px, background var(--surface-card)
Layout: column, gap 16px, padding 20px
--- CSS CUSTOM PROPERTIES (in :root) ---
:root {
  --ease-enter: cubic-bezier(0.16, 1, 0.3, 1);
  --ease-exit: cubic-bezier(0.7, 0, 0.84, 0);
  --duration-fast: 200ms;
  --duration-normal: 350ms;
  --duration-slow: 600ms;
  --surface-card: oklch(0.21 0.02 270);
  --surface-hover: oklch(0.27 0.03 270);
  --text-primary: oklch(0.92 0.01 270);
  --text-secondary: oklch(0.65 0.02 270);
  --text-dim: oklch(0.45 0.03 270);
  --accent-running: oklch(0.72 0.18 160);
  --accent-pending: oklch(0.7 0.17 80);
  --accent-completed: oklch(0.65 0.16 250);
  --accent-error: oklch(0.65 0.22 25);
  --score-high: oklch(0.72 0.18 160);
  --score-mid: oklch(0.7 0.17 80);
  --score-low: oklch(0.65 0.22 25);
  --border-card: 1px solid oklch(0.35 0.02 270);
  --shadow-card: 0 4px 24px oklch(0 0 0 / 0.25);
}
--- STRUCTURE ---
+---------------------------------------+
| [status-dot] Agent Name        [menu] |
| role_tag                                |
|                                         |
|  85                                    |
|  SCORE                                 |
|                                         |
|  tasks: 12 running | 4 pending | 8 done |
|                                         |
|  [health-bar 68%]                       |
|  Last run: 2m ago                       |
+---------------------------------------+
--- ANIMATION ---
.card-enter {
  animation: cardSlideIn var(--duration-slow) var(--ease-enter);
}
.card-exit {
  animation: cardFadeOut var(--duration-fast) var(--ease-exit);
}
@keyframes cardSlideIn {
  from { opacity: 0; transform: translateY(16px) scale(0.96); }
  to { opacity: 1; transform: translateY(0) scale(1); }
}
@keyframes cardFadeOut {
  from { opacity: 1; transform: scale(1); }
  to { opacity: 0; transform: scale(0.92); }
}
.status-pulse {
  animation: pulse 2s ease-in-out infinite;
}
@keyframes pulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.5; }
}
--- PROPERTY TABLE ---
| Property | CSS Variable | Value | Fallback |
|----------|-------------|-------|----------|
| card bg | var(--surface-card) | oklch(0.21 0.02 270) | #1e1e2e |
| text | var(--text-primary) | oklch(0.92 0.01 270) | #e0e0e8 |
| border | var(--border-card) | 1px solid oklch(0.35 0.02 270) | 1px solid #3a3a4a |
| score color | var(--score-high/mid/low) | per threshold | #4ade80/#facc15/#f87171 |
| status dot bg | var(--accent-<state>) | per state | #22c55e/#eab308/#ef4444 |
--- A11Y & WCAG ---
- Contrast ratio text-primary on surface-card: 10.2:1 (AAA)
- Contrast ratio text-secondary on surface-card: 4.8:1 (AA)
- Contrast ratio text-dim on surface-card: 2.6:1 (decorative only, no information conveyed)
- aria-label attribute on card: "Agent {name}, score {score}, status {status}"
- aria-live="polite" on score number updates
- role="article" on each card
- tabindex="0" on interactive cards
- focus-visible ring: 2px solid var(--accent-completed)
--- VALIDATION CHECKLIST ---
[X] mockup count == 1 of 6
[X] --ease-enter present in :root
[X] --ease-exit present in :root
[X] --duration-fast/normal/slow present
[X] no raw hex in borders
[X] var() used for all colors
[X] property table present
[X] WCAG contrast ratios declared
[X] aria- attributes specified
[ ] all 6 mockups delivered (4 remaining)
MOCKUP 2 OF 6 — AGENT LIST ROW
--- CORE SPEC ---
Component: agent-row
Container: 100% wide, 64px tall, border-radius 8px, background var(--surface-card)
Layout: row, align-items center, gap 16px, padding 12px 20px
--- STRUCTURE ---
+-------------------------------------------------------------------+
| [dot] [avatar] Agent Name    role_tag   SCORE  t:12r:4p:8d  [btn] |
|        health 68% | last 2m ago                                   |
+-------------------------------------------------------------------+
--- ANIMATION ---
.row-enter {
  animation: rowFadeIn var(--duration-normal) var(--ease-enter);
}
.row-exit {
  animation: rowSlideOut var(--duration-fast) var(--ease-exit);
}
@keyframes rowFadeIn {
  from { opacity: 0; transform: translateX(-8px); }
  to { opacity: 1; transform: translateX(0); }
}
@keyframes rowSlideOut {
  from { opacity: 1; transform: translateX(0); max-height: 64px; }
  to { opacity: 0; transform: translateX(16px); max-height: 0; }
}
--- PROPERTY TABLE ---
| Property | Var | Value |
|----------|-----|-------|
| row bg | var(--surface-card) | oklch(0.21 0.02 270) |
| row hover bg | var(--surface-hover) | oklch(0.27 0.03 270) |
| avatar size | --avatar-sm | 32px |
| border bottom | var(--border-card) | 1px solid oklch(0.35 0.02 270) |
--- A11Y ---
- Contrast: same as card (shared palette)
- aria-rowindex for each row
- role="row" on row container
- aria-selected on click
- aria-label="{agent name}, score {score}, {task count} tasks"
--- VALIDATION ---
[X] mockup 2 of 6 delivered
[X] --ease-enter and --ease-exit used
[X] var() only colors
[X] property table present
[X] WCAG + aria present
MOCKUP 3 OF 6 — AGENT HEALTH PANEL
--- CORE SPEC ---
Component: health-panel
Container: 100% wide, 200px tall, border-radius 12px, background var(--surface-card)
Layout: column, gap 12px, padding 20px
--- STRUCTURE ---
+---------------------------------------+
|  AGENT HEALTH                    [i]  |
|                                         |
|  [=======--------] 68%                 |
|  Memory: 240/512MB   CPU: 12%          |
|  Uptime: 3h 42m     Threads: 8         |
|                                         |
|  Status: Running with 0 errors         |
|  Last failure: 12h ago (task_fetch)    |
+---------------------------------------+
--- ANIMATION ---
.health-bar-fill {
  transition: width var(--duration-slow) var(--ease-enter);
}
.health-bar-pulse {
  animation: barPulse 3s var(--ease-enter) infinite;
}
@keyframes barPulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.85; }
}
.health-metric {
  transition: color var(--duration-fast) var(--ease-exit);
}
--- PROPERTY TABLE ---
| Property | Var | Value |
|----------|-----|-------|
| bar track | --health-track | oklch(0.3 0.02 270) |
| bar fill | --health-fill | oklch(0.72 0.18 160) |
| bar fill warning | --health-warn | oklch(0.7 0.17 80) |
| bar fill danger | --health-danger | oklch(0.65 0.22 25) |
| bar height | --health-height | 8px |
| bar radius | --health-radius | 4px |
--- A11Y ---
- role="status" on health panel
- aria-valuenow="68" aria-valuemin="0" aria-valuemax="100" on bar
- aria-hidden="true" on decorative bar fill (screenreader reads aria-valuenow instead)
- Contrast: health metric text on surface-card = 4.8:1 (AA)
- aria-label on info button: "Health help"
--- VALIDATION ---
[X] mockup 3 of 6 delivered
[X] animation tokens used
[X] var() colors only
[X] property table present
[X] a11y specs complete
MOCKUP 4 OF 6 — AGENT STATUS TIMELINE
--- CORE SPEC ---
Component: status-timeline
Container: 100% wide, 300px tall, border-radius 12px, background var(--surface-card), overflow-y auto
Layout: column, gap 0px
--- STRUCTURE ---
+---------------------------------------+
|  ACTIVITY TIMELINE                     |
|                                         |
|  [o] 2m ago - Task completed           |
|  |                                     |
|  [o] 5m ago - Score updated 82->85    |
|  |                                     |
|  [o] 12m ago - Health degraded        |
|  |                                     |
|  [o] 30m ago - Run started (batch 3)  |
|                                         |
|  [View all 24 events >]                |
+---------------------------------------+
--- ANIMATION ---
.timeline-enter {
  animation: timelineSlideIn var(--duration-normal) var(--ease-enter);
}
@keyframes timelineSlideIn {
  from { opacity: 0; transform: translateY(8px); max-height: 0; }
  to { opacity: 1; transform: translateY(0); max-height: 60px; }
}
.timeline-dot {
  transition: background var(--duration-fast) var(--ease-exit);
}
.timeline-line {
  transition: height var(--duration-slow) var(--ease-enter);
}
--- PROPERTY TABLE ---
| Property | Var | Value |
|----------|-----|-------|
| dot size | --dot-size | 10px |
| dot bg success | var(--accent-completed) | oklch(0.65 0.16 250) |
| dot bg error | var(--accent-error) | oklch(0.65 0.22 25) |
| dot bg running | var(--accent-running) | oklch(0.72 0.18 160) |
| line width | --timeline-line | 2px |
| line color | var(--text-dim) | oklch(0.45 0.03 270) |
| event text | var(--text-secondary) | oklch(0.65 0.02 270) |
| timestamp | var(--text-dim) | oklch(0.45 0.03 270) |
--- A11Y ---
- role="log" on timeline container
- aria-label="Agent activity timeline"
- aria-atomic="true" for new event announcements
- aria-live="polite" on new event insertion area
- Contrast: event text (4.8:1 AA), timestamp (2.6:1 decorative)
- aria-labelledby on "View all" link
--- VALIDATION ---
[X] mockup 4 of 6 delivered
[X] animation tokens in use
[X] var() only colors
[X] property table included
[X] a11y + contrast documented
MOCKUP 5 OF 6 — AGENT SCORE BREAKDOWN
--- CORE SPEC ---
Component: score-breakdown
Container: 100% wide, 260px tall, border-radius 12px, background var(--surface-card)
Layout: column, gap 16px, padding 20px
--- STRUCTURE ---
+---------------------------------------+
|  SCORE BREAKDOWN             85       |
|                                         |
|  completeness        [========= ] 90%  |
|  correctness         [========  ] 82%  |
|  usefulness          [=======   ] 74%  |
|  speed               [=======   ] 76%  |
|  efficiency          [========  ] 80%  |
|                                         |
|  Overall: B+ (consistent)              |
+---------------------------------------+
--- ANIMATION ---
.score-bar-enter {
  animation: barGrow var(--duration-slow) var(--ease-enter) both;
}
@keyframes barGrow {
  from { width: 0; }
  to { width: var(--bar-width); }
}
.score-bar {
  transition: width var(--duration-slow) var(--ease-enter);
}
.score-number {
  transition: color var(--duration-fast) var(--ease-exit);
}
--- PROPERTY TABLE ---
| Property | Var | Value |
|----------|-----|-------|
| bar height | --score-bar-height | 6px |
| bar radius | --score-bar-radius | 3px |
| bar bg | --score-track | oklch(0.3 0.02 270) |
| bar fill | --score-fill | oklch(0.72 0.18 160) |
| label text | var(--text-primary) | oklch(0.92 0.01 270) |
| value text | var(--text-secondary) | oklch(0.65 0.02 270) |
| overall score | --score-large | oklch(0.72 0.18 160) |
--- A11Y ---
- role="region" aria-label="Score breakdown"
- Each bar: role="progressbar" aria-valuenow aria-valuemin="0" aria-valuemax="100"
- aria-valuetext="{dimension} at {value} percent"
- Contrast: label (10.2:1 AAA), value (4.8:1 AA)
- aria-sort="descending" on dimension list
- tabindex="0" on overall score for keyboard focus
--- VALIDATION ---
[X] mockup 5 of 6 delivered
[X] animation tokens present
[X] var() colors throughout
[X] property table included
[X] a11y + WCAG documented
MOCKUP 6 OF 6 — AGENT LIVE DASHBOARD
--- CORE SPEC ---
Component: agent-dashboard
Container: viewport-wide, 100vh, background var(--surface-page), overflow-y auto
Layout: grid, columns 3, gap 24px, padding 32px
Where --surface-page: oklch(0.16 0.015 270)
--- STRUCTURE ---
+---------------------------------------------------------------+
|  AGENT DASHBOARD                                [refresh] [add]|
|  Agents: 12 active | 4 idle | 2 error                         |
|                                                                |
|  +----------+ +----------+ +----------+                        |
|  | Agent 01  | | Agent 02  | | Agent 03  |                    |
|  | Score: 85 | | Score: 72 | | Score: 91 |                    |
|  | Health 68%| | Health 94%| | Health 55%|                    |
|  +----------+ +----------+ +----------+                        |
|  +----------+ +----------+ +----------+                        |
|  | Agent 04  | | Agent 05  | | Agent 06  |                    |
|  | Score: 78 | | Score: 63 | | Score: 88 |                    |
|  | Health 82%| | Health 41%| | Health 73%|                    |
|  +----------+ +----------+ +----------+                        |
|                                                                |
|  [Load more...]                                                |
+---------------------------------------------------------------+
--- ANIMATION ---
.dashboard-grid-enter {
  animation: gridStagger var(--duration-slow) var(--ease-enter);
}
.dashboard-card-enter {
  animation: dashboardCardIn var(--duration-normal) var(--ease-enter) both;
}
.dashboard-card-enter:nth-child(1) { animation-delay: 0ms; }
.dashboard-card-enter:nth-child(2) { animation-delay: 80ms; }
.dashboard-card-enter:nth-child(3) { animation-delay: 160ms; }
@keyframes dashboardCardIn {
  from { opacity: 0; transform: translateY(24px) scale(0.95); }
  to { opacity: 1; transform: translateY(0) scale(1); }
}
.status-banner {
  transition: background var(--duration-normal) var(--ease-exit);
}
--- PROPERTY TABLE ---
| Property | Var | Value |
|----------|-----|-------|
| page bg | --surface-page | oklch(0.16 0.015 270) |
| grid gap | --dash-gap | 24px |
| grid cols | --dash-cols | 3 |
| header text | var(--text-primary) | oklch(0.92 0.01 270) |
| status bar bg | var(--surface-card) | oklch(0.21 0.02 270) |
| divider line | var(--border-card) | 1px solid oklch(0.35 0.02 270) |
| refresh btn | var(--accent-completed) | oklch(0.65 0.16 250) |
--- A11Y ---
- role="main" aria-label="Agent status dashboard"
- role="grid" on card grid, aria-rowcount aria-colcount
- aria-live="polite" on status bar (agent count updates)
- role="alert" on error banner when present
- Contrast: header (10.2:1 AAA), status counts (4.8:1 AA)
- aria-keyshortcuts="Ctrl+R" on refresh button
- focus trap inside modal when "add agent" dialog opens
- aria-expanded on collapsible sections
- aria-controls referencing controlled element id
--- VALIDATION ---
[X] mockup 6 of 6 delivered
[X] --ease-enter present
[X] --ease-exit present
[X] var() colors throughout
[X] no raw hex in borders
[X] property tables in all 6 mockups
[X] WCAG contrast ratios in all 6 mockups
[X] aria- attributes in all 6 mockups
[X] staggered delay animation in dashboard
--- FINAL PRE-SUBMISSION CHECKLIST ---
[X] mockup count == 6 of 6
[X] --ease-enter and --ease-exit exist in :root
[X] --duration-fast, --duration-normal, --duration-slow exist in :root
[X] no raw hex color values used in any border definition
[X] var() used for all color assignments
[X] collapsed property tables present in all 6 mockups
[X] WCAG contrast ratios documented in all 6 mockups
[X] aria- attributes specified in all 6 mockups
[X] staggered animation delay pattern demonstrated
[X] animation keyframe definitions use var(--ease-enter) and var(--ease-exit)
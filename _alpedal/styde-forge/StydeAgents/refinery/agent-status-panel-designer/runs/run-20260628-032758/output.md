AGENT STATUS PANEL — Forge Dashboard Mockup v1
Panel Container:
  title: Agent Status
  subtitle: 8 active agents | 12 total
  layout: grid, 3 columns, 12px gap
  max-height: 480px
  scroll: vertical on overflow
Status Indicators (left dot, 8px diameter):
  color mapping:
    idle:     #6b7280  (gray-500)
    running:  #22c55e  (green-500)  + subtle pulse animation
    pending:  #eab308  (yellow-500) + slow blink 1.5s
    error:    #ef4444  (red-500)    + solid no animation
    completed:#3b82f6  (blue-500)   + check overlay
    blocked:  #a855f7  (purple-500) + lock icon
Agent Card Component:
  structure:
    - status dot + agent name (12px semibold)
    - skill tag (8px pill, gray-700 bg, gray-200 text)
    - score bar: full-width 4px height, colored by tier
    - score number (14px bold, right-aligned)
    - action row: [run] [view log] [promote] buttons
    - last active: relative time ("2m ago", "14s ago")
Score Bar Tier Colors:
  threshold:
    - score: [0, 39]   color: #ef4444  label: poor
    - score: [40, 69]  color: #f97316  label: fair
    - score: [70, 84]  color: #eab308  label: good
    - score: [85, 94]  color: #22c55e  label: great
    - score: [95, 100] color: #06b6d4  label: elite
State Coverage (container-level):
  loading:
    skeleton card: 3 shimmer bars (12px, 8px, 8px heights)
    status dot: gray pulse
    score bar: empty 4px gray track
    no action buttons
  empty:
    text: "No agents running"
    icon: robot face, dimmed
    action: [create new agent] button centered
  error:
    border: 1px solid #ef4444, left red accent bar
    banner: "2 agents failed" with [view errors]
    each failed card: error dot + error message in 11px red text
    retry button on card
Summary Bar (top of panel, sticky):
  four metric tiles, each:
    running:    count in green,   icon: play
    pending:    count in yellow,  icon: clock
    completed:  count in blue,    icon: check-circle
    failed:     count in red,     icon: alert-circle
  aggregate score: large number (48px) centered
    color: gradient through threshold tiers
    label: "Average Agent Score"
Interaction States:
  hover on card: slight lift, box-shadow increase, bg shift to gray-800
  selected card: left accent bar color match to agent tier
  drag reorder: ghost card, opacity 0.5, drop zone highlighted
Responsive Breakpoints:
  >= 1024px: 3 columns, full summary bar
  768-1023px: 2 columns, summary bar collapses to single row flex-wrap
  < 768px: 1 column, summary bar becomes scrollable row, agent cards full-width
Example Card Data (8 agents):
  - name: Teacher Agent    skill: curriculum   score: 92  status: running
  - name: Builder Agent    skill: blueprints   score: 85  status: completed
  - name: Reviewer Agent   skill: lint         score: 73  status: running
  - name: Debug Agent      skill: repair       score: 41  status: pending
  - name: Promoter Agent   skill: gates        score: 96  status: idle
  - name: Planner Agent    skill: strategy     score: 60  status: blocked
  - name: Observer Agent   skill: telemetry    score: 88  status: running
  - name: Gate Agent       skill: deploy       score: 34  status: error
Summary Bar Values for sample:
  running: 3    pending: 1    completed: 1    failed: 1
  avg score: 71  (good tier, yellow range)
States Render Order:
  panel loads -> loading state (2s shimmer) -> empty state (if no agents) OR normal grid
  error state overlays: full panel gets red top border + dismissable error bar
  error bar: "Connection lost — reconnecting..." with spinner, auto-dismiss on reconnect
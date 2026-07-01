Agent Status Panel
Fas 0.5 Mockup Component
State Coverage Matrix
All interactive components must specify these 6 variants: idle, loading, empty, success, error, network-failure
Agent Overview Card (single agent row/card)
  idle: Agent registered, no active tasks. Avatar grey, status dot grey, score shows last-known, task counts 0/0/0, health bar dim
  loading: Agent data fetching. Skeleton placeholder, spinning dot, score pulse animation, task counts as shimmer bars, health bar empty animated stripe
  empty: No agents registered yet. Zero-state illustration, add-agent CTA button centered, no cards visible
  success: Active agent with data. Green status dot, score badge, live task counters, health bar colored, last-seen timestamp
  error: Agent data fetch failure. Red status dot, score shows "---", retry button, health bar red, tooltip with error message on hover
  network-failure: Backend unreachable. Orange warning icon overlay on all agent cards, "Connection lost" banner at top, auto-retry countdown timer, cached data shown with opacity 0.6
Status Indicator (dot/badge per agent)
  idle: Grey dot, 8px, no animation
  loading: Blue dot, 8px, pulsing 1s loop
  empty: N/A (never shown in empty state)
  success: Green dot, 8px, solid
  error: Red dot, 8px, static
  network-failure: Orange dot, 8px, slow blink 2s loop
Score Badge (numeric rating per agent)
  idle: Last-known score in grey, no badge background
  loading: Skeleton circle 32px, no number
  empty: N/A
  success: Score 0-100, color gradient: red 0-40, amber 40-70, green 70-85, emerald 85-100. Badge pill shape
  error: "---" in red, badge pill light red bg
  network-failure: Last-cached score at 60% opacity, badge pill orange border
Task Counter (running / pending / completed)
  idle: "0 running  |  0 pending  |  0 completed" all grey
  loading: Three shimmer bars 40px/30px/50px wide
  empty: N/A
  success: Live counts with color coding: running=blue, pending=amber, completed=green. Animated counter increment on change
  error: "? running  |  ? pending  |  ? completed" in red
  network-failure: Cached counts at 60% opacity, orange warning icon next to each count
Health Bar (agent health visualization)
  idle: Dimmed bar at 50% fill, grey
  loading: Animated indeterminate progress bar (shimmer)
  empty: N/A
  success: Fill 0-100% based on (completed / total tasks). Green gradient. Shows tooltip with health breakdown on hover
  error: Bar empty, red outline, health percentage shows 0%
  network-failure: Bar shows last-cached fill at 60% opacity, orange dashed border
Auto-refresh Polling (panel-level)
  idle: Polling inactive, no timer shown
  loading: Spinning refresh icon, "Updating..." text
  empty: Polling inactive, no timer shown
  success: Green checkmark, "Updated Xs ago", last-refresh timestamp
  error: Red refresh icon, "Update failed", retry button
  network-failure: Orange paused icon, "Retrying in Xs..."
Data Contract Table
AgentCard
  agent_id: string, required, uuid format
  name: string, required, max 64 chars
  status: enum, required, values: idle|loading|empty|success|error|network-failure
  score: number|null, required when status=success, range 0-100
  last_score: number|null, optional, previous score for delta display
  score_delta: number|null, optional, -100 to 100, rendered as arrow indicator
  tasks_running: integer, required, default 0, min 0
  tasks_pending: integer, required, default 0, min 0
  tasks_completed: integer, required, default 0, min 0
  health_pct: integer, required when status=success, 0-100
  last_seen_utc: iso8601|null, required, null if never seen
  error_message: string|null, required when status=error
  error_timestamp: iso8601|null, required when status=error
  agent_type: string, optional, e.g. "teacher"|"critic"|"forger"
  promotion_tier: enum, optional, values: sandbox|staging|production
StatusIndicator
  value: enum, required, values: idle|loading|success|error|network-failure
  size_px: integer, optional, default 8, range 6-16
  animation: enum, optional, values: none|pulse|blink, default none
ScoreBadge
  score: number|null, required
  size: enum, optional, values: sm|md|lg, default md
  show_delta: boolean, optional, default false
  color_scheme: enum, computed, values: red|amber|green|emerald|grey|orange
TaskCounter
  running: integer, required, default 0
  pending: integer, required, default 0
  completed: integer, required, default 0
  show_labels: boolean, optional, default true
  compact: boolean, optional, default false
HealthBar
  value: integer, required, 0-100
  width: string, optional, default "100%"
  height_px: integer, optional, default 8
  show_percentage: boolean, optional, default true
  animated: boolean, optional, default false
AutoRefreshPoller
  status: enum, required, values: idle|loading|success|error|network-failure
  interval_s: integer, required, default 15
  last_refresh_utc: iso8601|null, required
  retry_count: integer, optional, default 0
  next_retry_in_s: integer, optional, default 0
Guidelines
- Status dot always left-aligned before agent name for glanceability
- Card layout: status dot + name | score badge | health bar | task counter | last seen
- Score drives badge color, not agent type
- Empty state shows illustration + "Add your first agent" button, not agent cards
- Network-failure is a panel-level overlay, not per-card — prevents N+1 flash
- Health bar fill formula: completed / (running + pending + completed) * 100
- Auto-refresh stops on error state after 3 consecutive failures; manual retry required
- Tooltip on health bar shows: tasks breakdown, success rate, avg response time
- Color scheme: grey=idle, blue=loading, green=success, red=error, orange=network-failure
- Detail view must not repeat card-level data — show agent history, run logs, score timeline instead
- Transition animations between states: 300ms ease-in-out
- Responsive: grid 1-col mobile, 2-col tablet, 3-col desktop
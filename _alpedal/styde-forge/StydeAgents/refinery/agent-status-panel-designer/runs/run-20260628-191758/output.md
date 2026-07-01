agent-status-panel: forge-dashboard
version: 0.5
status: design-mockup
panel-layout:
  orientation: horizontal-scroll
  max-visible: 6
  card-width: 280px
  card-height: auto
  gap: 16px
  padding: 24px
card-template:
  header:
    agent-name: text-14px-semibold
    agent-avatar: 24px-circle
    status-dot:
      enum: [running, pending, completed, failed, idle, queued]
      colors:
        running: '#22c55e'  # green pulse
        pending: '#f59e0b'  # amber
        completed: '#3b82f6' # blue
        failed: '#ef4444'   # red
        idle: '#6b7280'     # gray
        queued: '#8b5cf6'  # violet
      animation:
        running: pulse-2s
        queued: pulse-4s
        idle: none
        completed: none
        failed: none
        pending: none
  score-area:
    current-score:
      number: 0-100
      font: 32px-bold-mono
      color-gradient:
        threshold-85: '#22c55e'
        threshold-70: '#f59e0b'
        threshold-50: '#ef4444'
        default: '#6b7280'
    peak-score:
      prefix: peak
      font: 11px-regular
      color: '#9ca3af'
    trend:
      direction: [up, down, flat]
      icon:
        up: arrow-up
        down: arrow-down
        flat: dash
      color:
        up: '#22c55e'
        down: '#ef4444'
        flat: '#9ca3af'
  counts-bar:
    layout: horizontal-3-sections
    sections:
      running:
        label: RUN
        color: '#22c55e'
        count: number
      pending:
        label: PND
        color: '#f59e0b'
        count: number
      completed:
        label: DONE
        color: '#3b82f6'
        count: number
    total-label:
      visible: false
  health-bar:
    layout: horizontal-4-dots
    dots:
      - label: memory
        threshold-80-good: true
      - label: tokens
        threshold-80-good: true
      - label: latency
        threshold-200ms-good: true
      - label: quality
        threshold-80-good: true
    dot-colors:
      good: '#22c55e'
      warning: '#f59e0b'
      critical: '#ef4444'
  progress-bar:
    type: agent-cycle-progress
    fills-to: next-milestone
    label:
      format: 'step {current}/{total}'
    color: '#3b82f6'
    bg: '#1f2937'
  timestamp:
    format: 'last eval: {relative}'
    font: 10px-regular
    color: '#6b7280'
status-dot-animations:
  running:
    - keyframes: [0% opacity:1, 50% opacity:0.4, 100% opacity:1]
    - duration: 2s
    - repeat: infinite
  queued:
    - keyframes: [0% opacity:0.6, 50% opacity:1, 100% opacity:0.6]
    - duration: 4s
    - repeat: infinite
example-card:
  agent-name: codereview-v4
  status: running
  current-score: 87
  peak-score: 92
  trend: up
  counts:
    running: 3
    pending: 2
    completed: 14
  health-dots:
    memory: warning
    tokens: good
    latency: good
    quality: good
  progress: 'step 7/15'
  last-eval: '2m ago'
summary-bar:
  layout: top-fixed-sticky
  elements:
    total-agents: number
    agents-running: number-badge-green
    agents-pending: number-badge-amber
    agents-completed: number-badge-blue
    agents-failed: number-badge-red
    avg-score: 0-100
    avg-cycle-time: 'Xm Xs'
empty-state:
  title: No active agents
  subtitle: Start a forge run to see agent status here
  icon: robot-sleeping
interaction:
  click-card: opens agent-detail-panel
  sort-by: [score, name, status, last-eval]
  filter-by-status: multi-select
  auto-refresh: 5s polling
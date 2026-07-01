agent-status-panel:
  version: 1
  theme: dark dashboard
panel-layout:
  type: grid
  columns: 3
  gap: 16px
agent-card:
  width: 360px
  height: auto
  border: 1px solid rgba(255,255,255,0.08)
  border-radius: 12px
  background: rgba(18,18,22,0.95)
  padding: 16px
  header:
    layout: row
    gap: 12px
    align: center
    avatar:
      shape: circle
      size: 36px
      border: 2px solid var(--status-color)
    agent-name:
      font: 15px semi-bold
      color: #e8e8ec
    agent-role:
      font: 12px regular
      color: #8888a0
  status-badge:
    position: top-right
    shape: pill
    padding: 4px 10px
    font: 11px bold
    states:
      running:
        color: #00d4aa
        bg: rgba(0,212,170,0.12)
        pulse: true
      pending:
        color: #f0b429
        bg: rgba(240,180,41,0.12)
        dash: true
      completed:
        color: #22c55e
        bg: rgba(34,197,94,0.12)
      failed:
        color: #ef4444
        bg: rgba(239,68,68,0.12)
      idle:
        color: #6b7280
        bg: rgba(107,114,128,0.12)
  score-bar:
    layout: column
    gap: 6px
    margin-top: 14px
    label-row:
      left: score
      right: value
      font: 12px medium
      color: #a0a0b8
    bar:
      height: 6px
      border-radius: 3px
      background: rgba(255,255,255,0.06)
      fill: var(--score-color)
      thresholds:
        0-60:   #ef4444
        60-75:  #f0b429
        75-90:  #22c55e
        90-100: #00d4aa
  counters:
    layout: row
    gap: 8px
    margin-top: 14px
    justify: space-between
    metric:
      shape: pill
      border: 1px solid rgba(255,255,255,0.06)
      padding: 6px 12px
      align: center
      label:
        font: 10px uppercase
        color: #666680
        letter-spacing: 0.5px
      value:
        font: 16px bold
        color: #e0e0ea
        margin-top: 2px
  health-indicator:
    layout: row
    gap: 8px
    margin-top: 12px
    padding: 10px 12px
    border-radius: 8px
    background: rgba(255,255,255,0.03)
    dot:
      shape: circle
      size: 8px
    states:
      healthy:
        dot-color: #22c55e
        label: Stable
        bg: rgba(34,197,94,0.06)
      degraded:
        dot-color: #f0b429
        label: Degraded
        bg: rgba(240,180,41,0.06)
      critical:
        dot-color: #ef4444
        label: Critical
        bg: rgba(239,68,68,0.06)
  actions:
    layout: row
    gap: 8px
    margin-top: 14px
    hidden: true
    show-on-hover: true
    button:
      shape: pill
      padding: 8px 16px
      font: 12px medium
      border: 1px solid rgba(255,255,255,0.1)
      color: #c0c0d0
      states:
        restart:
          icon: ↻
        inspect:
          icon: ⊞
        promote:
          icon: ↑
          accent: #00d4aa
summary-bar:
  layout: row
  gap: 24px
  padding: 16px 20px
  border-radius: 12px
  background: rgba(18,18,22,0.9)
  border: 1px solid rgba(255,255,255,0.06)
  stat-group:
    label: Active
    value: 7
    accent: #00d4aa
  stat-group:
    label: Pending
    value: 3
    accent: #f0b429
  stat-group:
    label: Completed
    value: 42
    accent: #22c55e
  stat-group:
    label: Failed
    value: 1
    accent: #ef4444
  divider:
    width: 1px
    bg: rgba(255,255,255,0.08)
  overall-health:
    label: System Health
    value: 94%
    accent: #00d4aa
status-pulse-animation:
  target: .status-badge.running
  keyframes:
    0%:   opacity: 1
    50%:  opacity: 0.5; box-shadow: 0 0 6px var(--status-color)
    100%: opacity: 1
  duration: 2s
  repeat: infinite
grid-states:
  loading:
    skeleton: true
    shimmer: linear-gradient(90deg, rgba(255,255,255,0.03), rgba(255,255,255,0.08), rgba(255,255,255,0.03))
    shimmer-duration: 1.5s
  empty:
    illustration: terminal-graphic
    message: No agents deployed
    secondary: Configure a blueprint to get started
  populated:
    scroll: vertical
    max-visible-cards: 9
    load-more: button at bottom
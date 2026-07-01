AGENT STATUS PANEL DESIGN v1
panel-id: agent-status-panel-dashboard
variant: full-overview
version: 1.0
author: agent-status-panel-designer
---
component: agent-status-grid
layout:
  type: responsive-grid
  columns-default: 4
  columns-tablet: 2
  columns-mobile: 1
  gap: 16px
  padding: 24px
breakpoints:
  - name: mobile
    max-width: 640px
    changes:
      columns: 1
      gap: 12px
      padding: 12px
      card-compact: true
  - name: tablet
    max-width: 1024px
    changes:
      columns: 2
      gap: 14px
      padding: 16px
---
component: agent-card
states:
  - id: loading
    skeleton: true
    elements:
      - type: shimmer-bar
        width: 60%
        height: 14px
        radius: 4px
        delay: 0ms
      - type: shimmer-circle
        size: 36px
        radius: 50%
        delay: 100ms
      - type: shimmer-bar
        width: 40%
        height: 10px
        radius: 4px
        delay: 200ms
    animation: pulse-shimmer 1.8s ease-in-out infinite
  - id: empty
    illustration: true
    text: "No agents deployed"
    cta: "Deploy your first agent"
    variant: muted-on-surface
  - id: error
    icon: warning-triangle
    text: "Failed to load agent status"
    action: reload
    color: semantic-error
  - id: populated
    variants:
      - status: running
        indicator: green-pulse
        border: left-accent-green
        actions: [pause, stop, inspect]
      - status: paused
        indicator: amber-steady
        border: left-accent-amber
        actions: [resume, stop, inspect]
      - status: error
        indicator: red-flash
        border: left-accent-red
        actions: [restart, inspect, logs]
      - status: completing
        indicator: blue-fade
        border: left-accent-blue
        actions: [inspect]
      - status: queued
        indicator: gray-dot
        border: left-accent-gray
        actions: [cancel, inspect]
      - status: completed
        indicator: green-checkmark
        border: left-accent-green
        actions: [rerun, inspect, export]
card-elements:
  - id: agent-name
    type: text
    weight: 600
    size: 14px
    truncate: single-line
  - id: status-indicator
    type: dot-with-label
    size: 10px
    animation: per-variant-above
  - id: score-meter
    type: arc-gauge
    range: 0-100
    color-thresholds:
      - below: 50
        color: semantic-error
      - from: 50
        to: 74
        color: semantic-warning
      - from: 75
        to: 89
        color: semantic-info
      - from: 90
        color: semantic-success
    animation: sweep-in 600ms ease-out
    label-format: "{score}/100"
  - id: run-counts
    type: horizontal-bar-set
    bars:
      - label: completed
        count-key: runs.completed
        color: semantic-success
      - label: pending
        count-key: runs.pending
        color: semantic-warning
      - label: error
        count-key: runs.errored
        color: semantic-error
    variant-progress: true
    total-bar: runs.total
  - id: last-run-timestamp
    type: relative-time
    size: 11px
    color: text-tertiary
    format: time-ago
  - id: health-bar
    type: compact-bar
    fill: current-health-percent
    track-color: surface-variant
    fill-color: health-gradient
    label: "{health}% uptime"
---
component: agent-detail-panel
trigger: click on agent-card
animation: slide-in-right 250ms ease-out
breakpoints:
  tablet:
    animation: slide-up 250ms ease-out
    width: 100%
  mobile:
    animation: slide-up 250ms ease-out
    width: 100%
    max-height: 85vh
    overlay: true
panel-sections:
  - id: header
    elements:
      - agent-avatar
      - agent-name-large
      - status-badge
      - close-button
      - action-bar: [restart, pause, stop, logs, export]
  - id: score-history
    type: mini-sparkline
    data-points: 24
    interval: 1h
    color: health-gradient
    tooltip: true
  - id: run-history
    type: timeline
    max-items: 10
    group-by: date
    item-format: "{status} — {duration}s — {timestamp}"
  - id: health-metrics
    type: stat-grid
    columns: 2
    items:
      - label: Uptime
        value: "{uptime}%"
        tooltip: "Last 24h"
      - label: Avg Score
        value: "{avgScore}/100"
        color: score-color
      - label: Total Runs
        value: "{totalRuns}"
      - label: Error Rate
        value: "{errorRate}%"
        color-if: "> 10"
  - id: promotion-status
    type: progress-ring
    value: "{runsTowardPromotion}/{promotionThreshold}"
    label: "Toward Production"
    tooltip: "3 consecutive scores >= 85"
---
theme-support:
  light:
    surface: #FFFFFF
    surface-variant: #F2F4F7
    text-primary: #1A1D23
    text-secondary: #5A5F6B
    text-tertiary: #8B8F9A
    border: #E0E2E6
    semantic-success: #22C55E
    semantic-warning: #F59E0B
    semantic-error: #EF4444
    semantic-info: #3B82F6
    skeleton-shimmer: [ #E5E7EB, #F3F4F6, #E5E7EB ]
    status-pulse-green: #22C55E
    status-steady-amber: #F59E0B
    status-flash-red: #EF4444
    status-fade-blue: #3B82F6
  dark:
    surface: #1A1D23
    surface-variant: #262A33
    text-primary: #F0F1F4
    text-secondary: #9CA0AB
    text-tertiary: #656A77
    border: #333842
    semantic-success: #4ADE80
    semantic-warning: #FBBF24
    semantic-error: #F87171
    semantic-info: #60A5FA
    skeleton-shimmer: [ #262A33, #333842, #262A33 ]
    status-pulse-green: #4ADE80
    status-steady-amber: #FBBF24
    status-flash-red: #F87171
    status-fade-blue: #60A5FA
  high-contrast:
    surface: #000000
    surface-variant: #1A1A1A
    text-primary: #FFFFFF
    text-secondary: #CCCCCC
    text-tertiary: #999999
    border: #666666
    semantic-success: #00FF66
    semantic-warning: #FFCC00
    semantic-error: #FF3333
    semantic-info: #3399FF
    skeleton-shimmer: [ #1A1A1A, #333333, #1A1A1A ]
    border-width: 2px
---
color-blind-safe-palette:
  type: wcag-aa-compliant
  contrast-ratio-min: 4.5:1
  shapes-supplement-indicators: true
  labels-supplement-colors: true
  semantic-success:
    color: #118B3E
    shape: checkmark
    label: "Running/Completed"
  semantic-warning:
    color: #B8860B
    shape: circle-dot
    label: "Pending/Paused"
  semantic-error:
    color: #B22222
    shape: exclamation
    label: "Error/Failed"
  semantic-info:
    color: #0057B7
    shape: info-circle
    label: "In Progress"
---
data-contract:
  source: websocket /agents/status
  interval: 3000ms
  message-types:
    - event: agent.status.update
      fields:
        agentId: string
        name: string
        status: [running, paused, error, completing, queued, completed]
        score: number (0-100)
        health: number (0-100)
        runs:
          completed: number
          pending: number
          errored: number
          total: number
        lastRunAt: iso8601
        runHistory: array of {status, duration, timestamp}
        promotionStatus:
          consecutiveScores: [number]
          threshold: number
      card-state-mapping:
        status=running: card variant running
        status=paused: card variant paused
        status=error: card variant error
        status=completing: card variant completing
        status=queued: card variant queued
        status=completed: card variant completed
        score+health both null: card state loading
        agentId exists but no data: card state empty
        websocket disconnect: card state error
    - event: agent.batch.complete
      fields:
        agentId: string
        batchRunId: string
        scores: [number]
        avgScore: number
        promoted: boolean
        rolledBack: boolean
      mapping:
        triggers agent-card refresh
        promoted=true: show promotion-banner on detail panel
        rolledBack=true: show rollback-banner on detail panel
---
empty-state-design:
  scenario: first-run-no-agents
  illustration: simple-robot-silhouette
  heading: "No agents deployed"
  body: "Deploy your first agent to see real-time status and scores"
  action:
    label: "Deploy Agent"
    variant: primary
    icon: plus
  scenario: no-recent-runs
  heading: "No recent runs"
  body: "Agents are idle. Start a training loop to see run history."
  action:
    label: "Start Training"
    variant: secondary
    icon: play
---
error-state-design:
  scenario: connection-lost
  banner: true
  icon: wifi-off
  text: "Connection to agent service lost"
  action: retry
  auto-reconnect: true
  retry-interval: 5000ms
  scenario: agent-crash
  overlay-on-card: true
  icon: alert-triangle
  text: "Agent crashed unexpectedly"
  action: restart-agent
  priority: high
  color: semantic-error
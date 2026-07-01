agent-status-panel mockup v1
domain: frontend
framework: fas-0.5-mockup
purpose:
  Display a dashboard grid of active training agents with live status, scores, and health indicators. Each agent card shows identity, current task state, performance score, running/pending/completed counts, and a health bar. Supports filtering by state and sorting by score or name.
layout:
  type: responsive-grid
  columns: 3 (desktop), 2 (tablet), 1 (mobile)
  gap: 16px
  padding: 24px
top-bar:
  - filter-chip-group:
      label: Filter by status
      options: [all, running, pending, completed, error]
      default: all
  - sort-dropdown:
      label: Sort by
      options: [score-high-low, score-low-high, name-asc, name-desc, last-active]
      default: score-high-low
  - search-input:
      placeholder: Search agent name or ID...
      width: 240px
agent-card:
  width: 100%
  min-height: 180px
  max-height: 260px
  border-radius: 12px
  background: surface-card
  border: 1px solid border-subtle
  padding: 16px
  display: flex
  flex-direction: column
  gap: 8px
  hover: shadow-elevated border-accent
  header:
    avatar:
      size: 32px
      shape: circle
      bg: gradient(agent-color-start, agent-color-end)
      show-initials: true
      status-dot:
        size: 8px
        position: bottom-right
        colors:
          running: green-500
          pending: amber-400
          completed: blue-500
          error: red-500
          idle: gray-400
    agent-name:
      font: body-semibold
      color: text-primary
      truncate: single-line
    agent-id:
      font: caption
      color: text-tertiary
      max-visible: 8 chars
  body:
    status-bar:
      current-state:
        label: Status
        value: running | pending | completed | error | idle
        badge:
          running: bg-green-100 text-green-800
          pending: bg-amber-100 text-amber-800
          completed: bg-blue-100 text-blue-800
          error: bg-red-100 text-red-800
          idle: bg-gray-100 text-gray-600
      current-task:
        label: Task
        value: string
        max-width: 160px
        truncate: single-line
    score-block:
      score:
        value: 0-100 integer
        display: large-number (48px)
        color-set:
          threshold-low: 0-49 color red-600
          threshold-mid: 50-79 color amber-500
          threshold-high: 80-89 color blue-500
          threshold-elite: 90-100 color green-500
      change-indicator:
        delta: +5
        direction: up | down | flat
        icon: arrow-up-green | arrow-down-red | dash-gray
        visible: delta != 0
    health-bar:
      value: 0-100 integer
      height: 6px
      radius: 3px
      bg: border-subtle
      fill-gradient: health-gradient (red via amber to green)
      label: "{value}% health"
      tooltip: Health score based on error rate, response latency, cache hit ratio
    counts-row:
      layout: row
      gap: 12px
      items:
        - running-count:
            icon: play-circle
            value: integer
            color: text-secondary
        - pending-count:
            icon: clock
            value: integer
            color: text-secondary
        - completed-count:
            icon: check-circle
            value: integer
            color: text-secondary
        - error-count:
            icon: alert-circle
            value: integer
            color: red-500
        - total-run-count:
            icon: layers
            value: integer
            color: text-tertiary
    last-active-timestamp:
      label: Last active
      format: relative (2m ago, 1h ago, yesterday)
      color: text-tertiary
      font: caption
  footer:
    action-row:
      - button-text: View details
        variant: subtle
        size: sm
        action: open-detail-panel
      - button-text: Pause
        variant: subtle danger
        size: sm
        action: pause-agent
        visible: state == running
      - button-text: Resume
        variant: subtle primary
        size: sm
        action: resume-agent
        visible: state == pending
empty-state:
  title: No agents found
  description: Adjust your filter or create a new training agent to get started
  action: Create agent
  icon: robot-empty
error-state:
  title: Failed to load agent status
  description: The agent service is unreachable. Check network connectivity and try again.
  action: Retry
  icon: alert-triangle
loading-state:
  type: skeleton-grid
  columns: 3
  skeleton-card:
    height: 200px
    skeleton-lines: [header 32px, body 24px, body 48px, body 20px, footer 32px]
    animation: shimmer
color-tokens:
  border-subtle: var(--color-border-subtle)
  border-accent: var(--color-border-accent)
  surface-card: var(--color-surface-card)
  text-primary: var(--color-text-primary)
  text-secondary: var(--color-text-secondary)
  text-tertiary: var(--color-text-tertiary)
  green-500: var(--color-green-500)
  green-100: var(--color-green-100)
  green-800: var(--color-green-800)
  amber-400: var(--color-amber-400)
  amber-500: var(--color-amber-500)
  amber-100: var(--color-amber-100)
  amber-800: var(--color-amber-800)
  blue-500: var(--color-blue-500)
  blue-100: var(--color-blue-100)
  blue-800: var(--color-blue-800)
  red-500: var(--color-red-500)
  red-600: var(--color-red-600)
  red-100: var(--color-red-100)
  red-800: var(--color-red-800)
  gray-400: var(--color-gray-400)
  gray-600: var(--color-gray-600)
  gray-100: var(--color-gray-100)
  health-gradient: linear-gradient(90deg, var(--color-red-400), var(--color-amber-400), var(--color-green-400))
  agent-colors:
    agent-alpha: [--indigo-500, --indigo-300]
    agent-beta: [--teal-500, --teal-300]
    agent-gamma: [--purple-500, --purple-300]
    agent-delta: [--cyan-500, --cyan-300]
    agent-epsilon: [--rose-500, --rose-300]
breakpoints:
  - width: 1200px
    columns: 3
    card-min-height: 200px
  - width: 768px
    columns: 2
    card-min-height: 180px
    top-bar:
      filter-chip-group: horizontal-scroll
      sort-dropdown: full-width
      search-input: full-width
  - width: 0px
    columns: 1
    card-min-height: 220px
    top-bar: stack-vertical
    body:
      counts-row: wrap 2-per-row
accessibility:
  score-values: text + color (not color-only)
  status-indicator: icon + text label (not dot-only)
  health-bar: numeric label + bar fill
  contrast-ratio: 4.5:1 minimum for all text
  focus-visible: 2px ring on all interactive elements
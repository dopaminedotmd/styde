AGENT STATUS PANEL DESIGN — FAS 0.5 MOCKUP SPEC
layout:
  strategy: absolute + flex hybrid
  columns: 3 responsive grid
  gutter: 16px
  max-width: 1200px
  breakpoints:
    - 1200px: 3-col
    - 800px: 2-col
    - 480px: 1-col z-scroll
design-tokens:
  colors:
    status-idle: hsl(210, 15%, 50%)
    status-running: hsl(140, 60%, 45%)
    status-pending: hsl(45, 90%, 55%)
    status-failed: hsl(0, 75%, 55%)
    status-completed: hsl(200, 65%, 50%)
    score-excellent: hsl(140, 60%, 45%)
    score-good: hsl(200, 65%, 50%)
    score-fair: hsl(45, 90%, 55%)
    score-poor: hsl(0, 75%, 55%)
    card-bg: hsl(220, 12%, 10%)
    card-border: hsl(220, 10%, 20%)
    card-border-active: hsl(200, 60%, 50%)
    text-primary: hsl(0, 0%, 95%)
    text-secondary: hsl(0, 0%, 65%)
    text-muted: hsl(0, 0%, 45%)
    divider: hsl(220, 10%, 18%)
  spacing:
    xs: 4px
    sm: 8px
    md: 16px
    lg: 24px
    xl: 32px
  radius:
    card: 8px
    indicator: 50%
    badge: 4px
  typography:
    agent-name: 14px/1.4 monospace
    score: 24px/1 monospace bold
    status: 11px/1.2 sans-serif uppercase tracking-1
    meta: 11px/1.3 sans-serif
  animation:
    pulse-running: 2s ease-in-out infinite
    glow-running: box-shadow 0s linear infinite
edge-case-states:
  empty:
    variant: no-agents-placeholder
    layout: centered single card
    content: "No agents running" text-secondary
    action: "Launch First Agent" button
  loading:
    variant: skeleton-cards
    count: 6
    card-height: 120px
    skeleton-color: hsl(220, 10%, 15%)
    shimmer: true
  error:
    variant: error-state
    components:
      - icon: warning-triangle
      - text: "Agent status unavailable" text-primary
      - subtext: "Connection lost. Retrying..." text-muted
      - action: retry-button
  max-content:
    variant: scroll-container
    max-visible-cards: 12
    overflow: auto
    scrollbar-thin: true
    fade-edges: true
z-index-stacking:
  0: card-bg
  1: card-content
  2: status-indicator-glow
  5: progress-bar
  10: badge-overlay
  100: tooltip
  1000: modal-overlay
agent-card:
  width: 1fr
  min-width: 280px
  max-width: 380px
  height: auto
  min-height: 100px
  bg: card-bg
  border: 1px solid card-border
  border-radius: card
  padding: md
  gap: sm
  transition: border-color 150ms ease
  states:
    idle:
      border: card-border
      indicator: status-idle
    running:
      border: card-border-active
      indicator: status-running
      glow: 0 0 8px rgba(65, 200, 90, 0.3)
    pending:
      border: card-border
      indicator: status-pending
    failed:
      border: card-border
      indicator: status-failed
    completed:
      border: card-border
      indicator: status-completed
  hover:
    border: card-border-active
    box-shadow: 0 2px 12px rgba(0,0,0,0.4)
  layout-flex:
    direction: column
    gap: sm
  sections:
    - row-1:
        strategy: flex row align-items-center gap-sm
        elements:
          - status-indicator:
              width: 10px
              height: 10px
              radius: indicator
              bg: status-running
              glow:
                running: 0 0 6px currentColor
                others: none
          - agent-name:
              text: agent.name
              typography: agent-name
              color: text-primary
              flex: 1
              truncate: true
          - score-badge:
              strategy: absolute (right-aligned)
              text: agent.score
              typography: score
              color: score-excellent
              width: 48px
              height: 36px
              bg: hsl(0,0%,100%,0.04)
              radius: badge
              alignment: center center
    - row-2:
        strategy: flex row gap-xs
        elements:
          - status-label:
              text: agent.status uppercase
              typography: status
              color: status-running
              badge: true
              bg: hsl(0,0%,100%,0.06)
              padding: 2px 8px
              radius: badge
          - meta-text:
              text: "iteration 12/15"
              typography: meta
              color: text-muted
              flex: 1
        show_if: agent.status != 'idle'
    - row-3:
        strategy: flex row gap-sm
        height: 8px
        elements:
          - progress-bar:
              width: 100%
              height: 4px
              bg: divider
              radius: 2px
              fill:
                color: status-running
                width: agent.progress_pct
                transition: width 500ms ease
        show_if: agent.status == 'running'
    - row-4:
        strategy: flex row gap-md
        elements:
          - stat-group:
              strategy: flex row gap-xs
              items:
                - labeled-stat:
                    label: completed
                    value: agent.completed
                    color: text-primary
                    size: 13px monospace bold
                - labeled-stat:
                    label: failed
                    value: agent.failed
                    color: score-poor
                    size: 13px monospace bold
                - labeled-stat:
                    label: pending
                    value: agent.pending
                    color: status-pending
                    size: 13px monospace bold
          - elapsed:
              text: "2m 34s"
              typography: meta
              color: text-muted
        show_if: agent.status != 'idle'
  empty-state:
    strategy: absolute center-xy
    elements:
      - text: "No data yet"
      - text: "Awaiting first run"
  loading-state:
    strategy: flex column gap-sm
    elements:
      - skeleton: 100% x 10px
      - skeleton: 60% x 10px
      - skeleton: 100% x 4px
summary-bar:
  strategy: flex row gap-xl
  width: 100%
  height: auto
  padding: md lg
  bg: card-bg
  border: 1px solid card-border
  radius: card
  margin-bottom: lg
  layout-flex:
    direction: row
    justify: space-between
    align: center
  elements:
    - total-agents:
        text: "14 agents"
        typography: 14px sans-serif
        color: text-primary
    - status-pills:
        strategy: flex row gap-sm
        items:
          - pill: "5 running" bg=status-running+0.15 color=status-running
          - pill: "3 pending" bg=status-pending+0.15 color=status-pending
          - pill: "4 completed" bg=status-completed+0.15 color=status-completed
          - pill: "2 failed" bg=status-failed+0.15 color=status-failed
    - avg-score:
        text: "avg 84"
        typography: 20px monospace bold
        color: score-good
grid-container:
  strategy: css-grid
  columns: repeat(auto-fill, minmax(280px, 1fr))
  gap: md
  padding: none
  max-content:
    max-height: calc(100vh - 180px)
    overflow-y: auto
    scrollbar-gutter: stable
  empty: display centered placeholder card
  loading: 6 skeleton cards in grid
  error: stretch full-width error card across grid
component-variants:
  condensed:
    card-height: 64px
    hide: [row-3, row-4]
    row-1: compact
    score-badge: 32px x 24px, font 18px
  detailed:
    card-height: auto
    show-all: true
    row-4: full stats with progress breakdown
  mini:
    width: 48px
    height: 48px
    show-only: status-indicator + score-badge
    score-badge: 18px x 14px, font 12px
    tooltip-on-hover: true
    z-index: tooltip
animations:
  card-enter: fadeInUp 200ms ease
  card-exit: fadeOut 150ms ease
  status-change: color 300ms ease, bg 300ms ease
  score-change: number-ticker 400ms ease
  progress-update: width 500ms ease
  skeleton: shimmer 1200ms ease-in-out infinite
  running-pulse: opacity pulse 0 0.6 1.0 2s ease-in-out infinite
  hover-lift: transform translateY(-2px) 150ms ease
agent-health-signals:
  healthy:
    indicator: solid green
    pulse: none
    score: >= 75
  degraded:
    indicator: solid green with slow pulse
    pulse: 3s
    score: 50-74
  failing:
    indicator: solid red
    pulse: fast 1s
    score: < 50
    border-glitch: true
  stalled:
    indicator: yellow amber
    pulse: none blinking
    last-active: > 5min ago
  sleeping:
    indicator: gray off
    pulse: none
    status: idle
yaml-consistency:
  key-quoting: all keys with colons or special chars double-quoted
  block-style: nested lists use block dash, not inline-bracket
  token-refs: all color/spacing values reference tokens above, never raw hex/rgba
  validation: every token referenced in components exists in design-tokens section
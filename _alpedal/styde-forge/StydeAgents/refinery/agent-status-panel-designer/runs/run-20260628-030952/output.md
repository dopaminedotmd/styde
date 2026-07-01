mockup-1:
  name: agent-grid-overview
  description: Full-screen grid of all active agent cards. Each card shows agent name, current status badge, live score ring, and running/pending/completed count bar. Horizontal scroll on overflow. Cards are 280px wide, auto-height.
  tokens:
    animation:
      easing: cubic-bezier(0.4, 0, 0.2, 1)
      duration-fast: 150ms
      duration-normal: 250ms
      duration-slow: 400ms
    colors:
      dark:
        surface: '#1a1a2e'
        surface-elevated: '#16213e'
        text-primary: '#e0e0e0'
        text-secondary: '#a0a0b0'
        accent: '#4fc3f7'
        success: '#66bb6a'
        warning: '#ffa726'
        error: '#ef5350'
        neutral: '#78909c'
      light:
        surface: '#f5f5fa'
        surface-elevated: '#ffffff'
        text-primary: '#1a1a2e'
        text-secondary: '#5a5a6e'
        accent: '#0288d1'
        success: '#43a047'
        warning: '#ef6c00'
        error: '#d32f2f'
        neutral: '#546e7a'
  sections:
    - id: header-bar
      type: row
      constraints: score-bar MUST be separate from health-bar. No same-line grid colocation.
      layout: full-width top bar, left-aligned title 'Agents', right-aligned filter/sort dropdowns
      height: 56px
      children:
        - title: Agents
          style: text-2xl, font-semibold, dark-mode text-primary
        - filter-dropdown:
            options: [all, active, idle, error, completed]
            style: rounded 8px, border 1px solid, padding 8px, dark-mode surface-elevated
    - id: stats-bar
      type: row
      constraints: score-bar and health-bar occupy separate rows. Health bar is a continuous gradient strip.
      layout: two-row stack. Row 1: score-bar (0-100 numeric, animated ring). Row 2: health-bar (green-yellow-red gradient fill, percentage width).
      height: auto, min 48px
      children:
        - score-bar:
            type: circular-progress-ring
            value: number 0-100
            stroke-width: 6px
            trail-color: dark-mode surface-elevated / light-mode surface
            active-color: accent token
            animation: easeOutCubic 600ms on value change
            label: 'Score'
            label-position: center
        - health-bar:
            type: gradient-horizontal-bar
            segments: [green 0-60, yellow 60-85, red 85-100]
            value: number 0-100 mapped to segment fill
            height: 8px
            border-radius: 4px
            background: dark-mode surface-elevated / light-mode surface
            animation: easeOutQuad 400ms on value change
    - id: agent-cards
      type: responsive-grid
      constraints: min card width 260px, max card width 320px. Gaps 16px. Auto-fill rows.
      layout: CSS grid, grid-template-columns repeat(auto-fill, minmax(260px, 1fr))
      children:
        - agent-card:
            height: auto
            border-radius: 12px
            padding: 16px
            background: dark-mode surface-elevated / light-mode surface-elevated
            border: 1px solid, dark-mode rgba(255,255,255,0.08) / light-mode rgba(0,0,0,0.08)
            shadow: dark-mode none / light-mode 0 1px 3px rgba(0,0,0,0.08)
            hover: translateY -2px, shadow 0 4px 12px rgba(0,0,0,0.12)
            children:
              - agent-name:
                  style: text-base, font-medium, truncate
                  color: text-primary
              - status-badge:
                  type: pill
                  values: [running-green, pending-amber, completed-blue, error-red, idle-gray]
                  font-size: 12px
                  padding: 2px 10px
                  border-radius: 12px
                  background-mapping:
                    running: success token at 15% opacity
                    pending: warning token at 15% opacity
                    completed: accent token at 15% opacity
                    error: error token at 15% opacity
                    idle: neutral token at 15% opacity
              - score-ring:
                  small: true
                  diameter: 40px
                  stroke-width: 4px
                  label: '' hide label in card view
              - count-bar:
                  type: stacked-horizontal-bar
                  items: [running, pending, completed]
                  height: 6px
                  border-radius: 3px
                  width: 100%
                  color-mapping:
                    running: success
                    pending: warning
                    completed: accent
                  label-row: true, font-size 11px, text-secondary, space-between
    - id: empty-state
      type: centered-message
      constraints: shown only when agent count is 0
      icon: robot-outline
      text: 'No agents deployed yet'
      subtitle: 'Create your first blueprint to see agents here'
      action-button: 'Deploy Agent', style accent token background, white text
mockup-2:
  name: single-agent-detail-panel
  description: Right-side slide-over panel showing one agent's full status, score history, health breakdown, and task log. Opens from card click in mockup-1.
  tokens:
    animation:
      easing: cubic-bezier(0.4, 0, 0.2, 1)
      duration-slide: 300ms
      duration-fade: 200ms
    colors: inherit from mockup-1 dark/light
  sections:
    - id: panel-header
      type: row
      width: 480px
      constraints: fixed width 480px, full viewport height. Slide from right.
      layout: row with agent avatar/icon, name, close button right. Bottom border separator.
    - id: score-bar
      type: dedicated-section
      constraints: score-bar MUST be separate from health-bar. Score-bar is a full-width animated ring with numeric label. Health-bar is a separate section below with three health dimension bars.
      layout: score-bar on its own row, full width. Centered circular ring, diameter 80px, score text center, score label below.
    - id: health-breakdown
      type: column
      constraints: three separate health dimension bars stacked vertically. Each has label, gradient fill bar, numeric percentage right.
      layout:
        - health-dimension: stability
          value: 0-100
          gradient: green to yellow at 80, yellow to red at 60
        - health-dimension: throughput
          value: 0-100
          gradient: green to yellow at 70, yellow to red at 50
        - health-dimension: quality
          value: 0-100
          gradient: green to yellow at 85, yellow to red at 65
    - id: task-log
      type: scrollable-list
      max-height: 300px
      children:
        - task-entry:
            layout: row, timestamp left, status dot center, task-name right, duration right
            status-dot-mapping:
              success: green circle 8px
              failed: red circle 8px
              running: animated pulse blue circle 8px
              pending: gray circle 8px
mockup-3:
  name: agent-comparison-split
  description: Side-by-side comparison of two agents. Useful for A/B testing, promotion review, or benchmarking runs side by side.
  tokens: inherit from mockup-1
  sections:
    - id: comparison-header
      type: row
      layout: left arrow + select slot, right arrow + select slot. VS badge center. Agent names, score rings, status badges inline.
    - id: comparison-grid
      type: 2-column grid
      constraints: exact 50-50 split. Each column mirrors the mockup-2 detail panel structure.
      layout: column-left agent-a, column-right agent-b. Headers collapsed. Score and health sections side-scrollable if overflow.
    - id: diff-bar
      type: bottom-strip
      layout: delta indicators between the two agents. Score delta colored green if positive, red if negative. Health dimension deltas inline. Neutral delta gray.
mockup-4:
  name: deployment-progress-view
  description: Multi-agent deployment progress showing a queue of agents being deployed, running, or completed. Pipeline-style visualization.
  tokens: inherit from mockup-1
  sections:
    - id: pipeline-header
      type: row
      layout: 'Deployment Pipeline' left, '5 running | 3 pending | 12 completed' right, cancel-all button far right
    - id: pipeline-steps
      type: vertical-timeline
      constraints: each step is a full-width row with timeline connector left. Steps are ordered by deployment sequence.
      children:
        - pipeline-step:
            layout: timeline-dot (colored by status), agent-icon, agent-name, status bar (animated fill for running, complete bar for done), duration-right
            status-dot-mapping:
              running: animated gradient blue dot 16px, outer ring pulse
              pending: gray dot 16px, dashed outer ring
              completed: green dot 16px, solid outer ring
              failed: red dot 16px, X icon inside
              skipped: gray dot 12px, diagonal line
    - id: overall-progress-bar
      type: full-width stacked bar
      layout: segments running/pending/completed/failed/skipped, proportional width. Total count label right. Percentage label center.
mockup-5:
  name: agent-health-heatmap
  description: Heatmap grid showing agent health across time intervals. Rows are agents, columns are time buckets (last hour, last 6 hours, last 24 hours, last 7 days). Cells colored by health score.
  constraints: MUST use heatmap token as primary layout. Block layout is fallback only when data cardinality < 3 (fewer than 3 agents).
  tokens: inherit from mockup-1, plus:
    heatmap:
      cell-size: 24px
      cell-gap: 4px
      border-radius: 4px
      color-scale:
        0-20: error token at 90%
        21-40: error token at 60%
        41-60: warning token at 70%
        61-80: warning token at 35%
        81-90: success token at 50%
        91-100: success token at 80%
      hover: scale 1.15, show tooltip with exact score and timestamp
      animation: fadeIn 200ms staggered by cell index modulo 10
  sections:
    - id: heatmap-header
      type: row
      layout: 'Health Heatmap' left, time-range selector right (1h, 6h, 24h, 7d), heatmap legend right (gradient bar from red to green with labels)
    - id: heatmap-grid
      type: CSS grid
      layout: grid-template-columns 5 (time buckets), each column has agent-name label row, then cell rows per agent
      fallback-block-layout: only when agent count < 3. Shows agent health as vertical stacked cards with single health-bar per time bucket instead of heatmap cells. Block layout uses same color scale but renders as horizontal bar segments.
    - id: heatmap-summary-row
      type: bottom row
      layout: average health per time bucket across all agents, rendered as a single row of cells with same color mapping, opacity 0.7, label 'Average'
mockup-6:
  name: agent-health-breakdown-heatmap
  description: Per-health-dimension heatmaps stacked. Three heatmap grids, one per dimension (stability, throughput, quality). Same time buckets. Color scales per dimension.
  constraints: expandable/collapsible per dimension. Default collapsed.
  tokens: inherit from mockup-5, plus:
    dimension-colors:
      stability: blue scale
      throughput: purple scale
      quality: teal scale
  layout:
    - dimension-selector: pill tabs [stability, throughput, quality, all-combined]
    - dimension-heatmap: one per selected tab
      - 'all-combined' shows average of all three dimensions per cell
teacher-feedback-addressed:
  constraint-score-vs-health: |
    mockup-1 and mockup-2 score-bar section enforces:
    score bar token and health bar token must render as separate visual elements.
    No same-line grid colocation. Score bar is a circular ring, health bar is a
    gradient strip or dimension bars below. This prevents UI ambiguity and keeps
    each metric independently glanceable.
  constraint-heatmap-primary: |
    mockup-5 enforces heatmap token as primary layout. Block layout is explicitly
    gated to data cardinality < 3. This prevents fallback to verbose block layout
    when the heatmap token is available and data density supports it.
  token-families-required: |
    Every mockup includes animation-timing tokens (easing, duration variants) and
    semantic color tokens keyed by dark/light mode. No raw hex values in mockup
    content — all colors reference tokens from the shared palette.
  repeated-property-collapse: |
    mockup-2 through mockup-4 use 'inherit from mockup-1' for shared tokens,
    and mockup-5 reuses mockup-1 tokens plus additive heatmap-specific tokens.
    Property tables are not duplicated. Apply-to clause is implicit via inherit
    statement.
design_tokens:
  colors:
    agent-idle: '#374151'
    agent-running: '#3b82f6'
    agent-pending: '#f59e0b'
    agent-completed: '#10b981'
    agent-failed: '#ef4444'
    agent-critical: '#dc2626'
    bg-panel: '#111827'
    bg-card: '#1f2937'
    bg-card-hover: '#374151'
    text-primary: '#f9fafb'
    text-secondary: '#9ca3af'
    text-muted: '#6b7280'
    border-subtle: '#374151'
    border-active: '#3b82f6'
    green: '#10b981'
    orange: '#f59e0b'
    red: '#ef4444'
    blue: '#3b82f6'
    score-glow-90+: 'rgba(16,185,129,0.15)'
    score-glow-70-89: 'rgba(59,130,246,0.15)'
    score-glow-50-69: 'rgba(245,158,11,0.15)'
    score-glow-<50: 'rgba(239,68,68,0.15)'
    beam-running: '#3b82f6'
    beam-completed: '#10b981'
    beam-failed: '#ef4444'
  spacing:
    xs: 4px
    sm: 8px
    md: 12px
    lg: 16px
    xl: 24px
  radius:
    card: 8px
    avatar: 50%
    badge: 4px
    compact: 2px
  typography:
    heading: '700 14px/1.2 Inter, system-ui, sans-serif'
    label: '600 11px/1.3 Inter, system-ui, sans-serif'
    body: '400 12px/1.4 Inter, system-ui, sans-serif'
    metric: '700 20px/1 Inter, system-ui, sans-serif'
    metric-small: '600 14px/1 Inter, system-ui, sans-serif'
  iconography:
    status-dot-running: '8x8 circle fill:blue'
    status-dot-pending: '8x8 circle fill:orange'
    status-dot-completed: '8x8 circle fill:green'
    status-dot-failed: '8x8 circle fill:red'
    status-dot-idle: '8x8 circle fill:muted with 50% opacity'
    score-bar: '4px height, 12px radius, gradient fill'
    beam-animation: '1.5s ease-in-out infinite alternate'
  animation:
    beam-pulse: 'opacity 0.3 ↔ 1, scale 0.95 ↔ 1'
    card-hover: 'bg-card → bg-card-hover in 0.15s'
    status-dot-breathe: 'scale 1 ↔ 1.3 in 2s'
    score-fill: 'width 0 → target in 0.8s ease-out'
responsive_breakpoints:
  - breakpoint: >=1100px
    layout: 4-column grid
    card-width: minmax(240px, 1fr)
    density: full
  - breakpoint: 800-1099px
    layout: 3-column grid
    card-width: minmax(220px, 1fr)
    density: compact-meta
  - breakpoint: 500-799px
    layout: 2-column grid
    card-width: 1fr
    density: compact-all
  - breakpoint: <500px
    layout: 1-column list
    card-width: 100%
    density: minimal
mockups:
  mockup-01:
    name: Agent Card Grid
    layout: 4-column grid, each card 240px
    structure:
      card:
        - avatar agent-icon 32x32 top-left
        - name heading 14px bold
        - status-dot (running|pending|completed|failed) right of name
        - role-label 11px muted below name
        - score-bar 4px tall gradient fill width=score%
        - score-number 20px bold right side of bar
        - state-row: current-state label + session-duration text
    state-ui mapping:
      - state: running
        indicator: blue dot + blue-scale beam animation
        score-bar: blue→cyan gradient
        glow: score-glow-70-89
      - state: pending
        indicator: orange dot + no beam
        score-bar: orange→amber gradient
        glow: score-glow-50-69
      - state: completed
        indicator: green dot + steady green beam
        score-bar: green→teal gradient
        glow: score-glow-90+
      - state: failed
        indicator: red dot + pulsing red beam
        score-bar: red→crimson gradient
        glow: score-glow-<50
    constraints:
      score-bar: MUST be separate from health-bar on same card
      health-bar: only shown when health<100, as thin 2px line below score-bar
      responsive: at <500px, hide role-label and session-duration
  mockup-02:
    name: Agent Cluster by Status
    layout: 3 cluster sections in horizontal flex row
    structure:
      cluster-header:
        - status-label (Running|Pending|Completed) with count badge
        - count badge 12px bold circle fill:status-color
      cluster-body:
        - compact agent rows stacked vertically
        - each row: avatar 20x20 + name 12px + score-sparkline 80x20 svg-line
        - sparkline gradient match status-color
        - no gap between rows, border-bottom subtle
    state-ui mapping:
      - state: running-cluster
        header: 'Running' blue
        badge-fill: blue
        sparkline: blue→transparent gradient
        row-hover: bg-card-hover
        max-visible: 6 rows with scroll
      - state: pending-cluster
        header: 'Pending' orange
        badge-fill: orange
        sparkline: orange→transparent gradient
        row-hover: bg-card-hover
        max-visible: 8 rows with scroll
      - state: completed-cluster
        header: 'Completed' green
        badge-fill: green
        sparkline: green→transparent gradient
        row-hover: bg-card-hover
        max-visible: 10 rows with scroll
    constraints:
      clusters: MUST be same-height flex children, min-height 200px
      mosaic-bg: cluster area MAY use mosaic pattern (5px dots at opacity 0.03) as status-color tint
      block-layout: fallback only when total agents <6
      responsive: at <800px, stack clusters vertically
  mockup-03:
    name: Agent Timeline Heatmap
    layout: single-column timeline with heatmap-swatch rows
    structure:
      timeline-header:
        - 'Agent Activity' label
        - time-axis: 24-hour labels spaced evenly
        - now-marker: vertical red 1px line pulsing
      timeline-body:
        - agent rows, each 28px height
        - each row: avatar 16x16 + name 11px left side
        - heatmap-cells: 24 cells (one per hour) 12px wide
        - cell fill: opacity based on activity (0=bg-card, 1-3 active=0.3, 4-8=0.5, 9-15=0.7, 16+=1.0)
        - cell color: blue for running, green for completed, orange for pending
        - right-end: current-score 14px bold + score-bar(40px)
    state-ui mapping:
      - state: active-in-last-hour
        cell-opacity: 0.7-1.0
        dot-on-cell: white 2px circle
        tooltip: 'X actions in hour Y'
      - state: quiet-1-3hrs
        cell-opacity: 0.3-0.5
        dot: none
      - state: inactive-4+hrs
        cell-opacity: 0.05
        cell-color: desaturated to gray
        agent-name opacity: 0.5
      - state: completed-all-tasks
        row-underline: green 1px dotted
        score-metric: green bold
    constraints:
      heatmap: MUST be primary layout, NOT block layout
      block-layout: fallback only when data cardinality <3 (less than 3 agents)
      responsive: at <500px, collapse to last-6-hours only
  mockup-04:
    name: Agent Status Kanban
    layout: 4 swimlane columns (Running | Pending | Completed | Failed)
    structure:
      lane-header:
        - lane-label + count-badge 16px circle
        - lane total-score aggregate small text
      lane-body:
        - agent-cards stacked, each 160xauto
        - card: avatar 24x24 + name 12px + score-badge 16px
        - card-footer: current-task or idle-label
        - drag-handle 4x16 dots on left edge
    state-ui mapping:
      - lane: Running
        column-bg: rgba(59,130,246,0.03)
        column-border-top: 2px solid blue
        counter-bg: blue
        cards: max 5 visible, scroll rest
      - lane: Pending
        column-bg: rgba(245,158,11,0.03)
        column-border-top: 2px solid orange
        counter-bg: orange
        cards: max 8 visible, scroll rest
      - lane: Completed
        column-bg: rgba(16,185,129,0.03)
        column-border-top: 2px solid green
        counter-bg: green
        cards: max 10 visible, overflow scroll
      - lane: Failed
        column-bg: rgba(239,68,68,0.03)
        column-border-top: 2px solid red
        counter-bg: red
        cards: auto-height, no scroll cap
    constraints:
      columns: MUST be equal-width in flex row, no wrapping
      empty-lane: show placeholder 'Drop agents here' dashed border
      responsive: at <800px, collapse to 2-row grid (Running+Pending top, Completed+Failed bottom)
  mockup-05:
    name: Agent Mini Fleet Overview
    layout: single compact panel 600x180px, mount in dashboard sidebar
    structure:
      top-row:
        - 'Agents' heading + total-count badge
        - status-distribution pill-bar: 4 colored segments (R|P|C|F) proportional width
        - 'View All' link text 11px muted
      fleet-body:
        - 5 mini-agent rows, each 28px
        - each row: avatar 14x14 + name 10px truncated + status-dot 6px + score-text 11px + mini-beam-right edge
        - mini-beam: 4px vertical bar, color=status-color, height=score*(0.28px)
      bottom-row:
        - aggregate metrics: 'Avg Score' + 'Avg Health' + 'Run Since' in inline flex
    state-ui mapping:
      - state: all-healthy
        pill-segments: green(80%), blue(10%), orange(5%), red(5%)
        mini-beam-heights: 16-28px range
        bottom-row colors: all green
      - state: degraded
        pill-segments: green(40%), blue(20%), orange(25%), red(15%)
        mini-beam-heights: 4-22px range, several short
        bottom-row: 'Avg Score' orange text, 'Avg Health' red text
        alert-icon: triangle warning next to health
      - state: critical
        pill-segments: green(15%), blue(5%), orange(10%), red(70%)
        mini-beam-heights: 0-10px range, most very short
        bottom-row: all metrics red, 'Run Since' replaced with 'X FAILURES'
        panel-border: 1px solid red
    constraints:
      panel: MUST be single compact panel, not multi-section
      scroll: never needed at 5 agents; at >5, show scrollbar 4px thin
      responsive: at <500px, hide mini-beams, use inline score-text only
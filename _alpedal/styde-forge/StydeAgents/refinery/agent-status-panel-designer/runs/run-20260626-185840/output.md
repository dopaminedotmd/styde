mockup-01
name: hivemind-hubs
layout: radial-circular
structure:
  center: hub-circle
    metric: total health 94%
    ring: pulse-ring
  orbiting: 8 agent nodes
    each node:
      inner: agent-icon-circle
      outer: score-ring { value: 0-100, color: green/yellow/red }
      label: agent name below ring
  bottom: compact bar
    left: running 3
    center: pending 2
    right: completed 12
visual:
  background: dark slate with radial gradient
  colors: cyan active, gray idle, amber warning, red critical
  animation: slow orbit rotation on active agents
token-detail: SVG circle elements with stroke-dashoffset for score rings
embed-state: full-page dashboard panel, first fold above grid
unique-feature: orbital motion signals alive agents without text
mockup-02
name: terminal-tui-grid
layout: fixed-columns
structure:
  header: ASCII block
    left: AGENT STATUS 2026-06-26
    right: HEALTH 91%
  body: 6 rows x 3 cols
    each cell:
      top: AGENT-NAME (status)
        status symbols: * RUNNING, . IDLE, ! WARNING, x DOWN
      mid: score bar [=====    ] 62%
      bot: tasks 4/2/12 (run/pend/comp)
  footer: divider line + summary line
    text: 23 agents | 3 running 2 pending 18 completed | avg score 78%
visual:
  background: dark terminal green
  colors: green text, yellow warnings, red down, dim gray idle
  font: monospace, no icons, pure ASCII
token-detail: fixed-width progress bars using = and spaces
embed-state: dashboard tab, terminal theme
unique-feature: zero graphics, pure terminal aesthetic, feels like htop for agents
mockup-03
name: kanban-swimlanes
layout: three-column-kanban
structure:
  lane-running: left 30%
    header: RUNNING (3)
    cards: stacked vertical
      each card:
        line1: agent-name score
        line2: progress bar 0-100%
        line3: elapsed time
  lane-pending: middle 35%
    header: PENDING (5)
    cards: vertical stack with priority badges
      each card:
        line1: agent-name priority-tag
        line2: wait-time
        line3: target: goal
  lane-completed: right 35%
    header: COMPLETED (12)
    cards: compact, dimmed
      each card:
        line1: agent-name checkmark
        line2: total-time score
visual:
  background: white/light gray
  colors: blue running, amber pending, green completed with dim
  cards: rounded corners, subtle shadow, 2px left border accent
token-detail: kanban card component, progress bars inside cards
embed-state: for-main dashboard, secondary card region
unique-feature: workflow visualization makes state obvious at a glance
mockup-04
name: liquid-fill-cards
layout: card-grid-2x4
structure:
  cards: 8 equal cards in 2 rows
    each card:
      top-row:
        left: agent-icon small circle
        right: agent-name + status dot
      mid: progress ring
        ring fills with animated color based on score
        center: score number large
        under score: brief state label
      bottom:
        left: tasks running/pending/completed as small numbers
        right: health indicator (good/warning/critical)
      full-card: when running card has subtle glow border
visual:
  background: deep navy
  colors: electric blue active, mint completed, coral warning, slate idle
  progress rings: gradient fills, animated sweep
  glow: 4px outer glow on running agents
token-detail: SVG progress rings with gradient stroke, glassmorphism card
embed-state: main dashboard, prefer dark theme
unique-feature: liquid feel with animated gradients, cards feel alive
mockup-05
name: timeline-stream
layout: single-vertical-scroll
structure:
  header-sticky:
    left: AGENT TIMELINE
    right: summary icons (3 running, 2 pending, 18 done)
  stream: chronological event feed
    each event:
      left: timestamp compact
      mid: status-dot (green=complete, blue=start, yellow=queued, red=fail)
      right: agent-name + action + score delta
      below: micro progress line (tiny thin bar, 10px wide)
  bottom-summary:
    bars: 3 horizontal stacked bars
      running bar: blue, width = count
      pending bar: amber, width = count
      completed bar: green, width = count
    label: current batch health score X%
visual:
  background: near-black
  colors: neon blue, bright green, amber, pink for failures
  font: thin, modern sans-serif
  elements: hairline separators, 1px dots
token-detail: timeline component, inline micro-progress bars
embed-state: full-screen or large panel, alternative to grid
unique-feature: time-based view reveals agent lifecycle and sequencing
mockup-06
name: polar-radar
layout: radar-chart-cluster
structure:
  center: large radar chart
    axes: 6 axes (score, speed, reliability, task-load, uptime, throughput)
    plot: each agent as colored polygon overlaid
  side-panel: right 25%
    list: agent names sorted by score
      each row: name + score + small color swatch matching radar polygon
  bottom-bar:
    left: top agent name + score
    center: agent count
    right: avg all-scores
visual:
  background: dark gradient, subtle grid polar lines
  colors: per-agent distinct colors, semi-transparent polygons
  radar: circular grid lines, axis labels on outside
token-detail: SVG radar chart with layered polygons, multi-color
embed-state: analytics tab or dedicated health panel
unique-feature: comparative radar view shows multi-dimensional agent performance
mockup-07
name: stack-panel
layout: vertical-accordion
structure:
  top-bar:
    left: AGENT STATUS title
    right: status tabs ALL | RUNNING | PENDING | COMPLETED
  stack: collapsible sections per status group
    status-section:
      header: status name + count + expand/collapse icon
      body: rows of agents
        each row:
          left: color bar (2px) + agent-name + health-icon
          mid: score numerical + sparkline (tiny line chart 80x20px)
          right: task counts small text
      expand/collapse animated
  footer: global filters (sort by score, name, status, health)
visual:
  background: clean flat design
  colors: neutral grays with accent colors per agent type
  sparklines: simple line drawings in accent color
  font: system sans-serif
token-detail: accordion component, inline SVG sparklines
embed-state: sidebar panel on main dashboard
unique-feature: expandable groups keep UI dense but navigable, sparklines add trend
mockup-08
name: tower-lights
layout: vertical-strip-panel
structure:
  left-strip: 200px wide
    vertical: agent icons stacked, 32px each
      each icon:
        icon: symbol or emoji
        status-light: 6px circle, green/yellow/red/off
        score: tiny text to right
      active agent: highlighted with left accent bar
  main-view: right 75%
    top: selected agent name + score + status badge
    body: detail panel
      row1: 3 metric boxes (tasks done, avg time, success rate)
      row2: horizontal stacked bar (running/pending/completed proportions)
      bottom: activity log last 5 entries
    changes: clicking left strip icon swaps detail view
visual:
  background: dark, vertical gradient
  colors: status-light colors, white text, dim inactive icons
  strip: subtle separator line between strip and main
token-detail: list item with status dot, stacked bar chart
embed-state: side-by-side panel, main dashboard right side
unique-feature: tower panel design with quick-switch agent detail
mockup-09
name: score-matrix
layout: table-matrix-7x4
structure:
  header-row:
    cells: agent-name | score | health | running | pending | completed | trend
  body: 7 agent rows
    each row:
      agent-name: left-aligned with icon
      score: colored number (bold if >90, dim if <50)
      health: status dot + text label
      running: count + color
      pending: count + color
      completed: count
      trend: up/down arrow + delta
  footer-row:
    totals: sum/totals for each column
    avg-score: average with color
visual:
  background: white/light gray for header, alternating row stripes
  colors: blue running, amber pending, green completed, red critical
  table: clean borders, 2px header, sort indicators in header
token-detail: table component with inline status indicators
embed-state: data table tab in dashboard
unique-feature: spreadsheet density for power users, sortable metrics
mockup-10
name: biome-ecosystem
layout: abstract-organic
structure:
  canvas: full viewport
    elements:
      agents: floating circles of varying sizes
        size maps to score (bigger = higher score)
        color maps to health (blue=good, green=idle, amber=warning, red=critical)
        position: random but stable (non-overlapping)
        running agents: pulsating glow, larger pulse
        completed agents: static, slightly dimmed
        pending agents: orbiting slowly around canvas center
    connections: thin lines between agents that share task dependencies
      line opacity: 0.3 default, 0.8 on hover
  cursor-hover: agent info tooltip
    text: name, score, status, tasks breakdown
  corner-panel: bottom-right 150x80px
    text: summary counts with small animated counters
visual:
  background: very dark, subtle grid dots
  colors: bioluminescent palette (deep blue, teal, green, amber, coral)
  animation: gentle floating motion, pulse on active agents
  font: modern thin sans-serif for labels
token-detail: SVG circles with CSS animations, canvas rendering
embed-state: full-screen dashboard splash, overview mode
unique-feature: organic living feel, agents feel like creatures in an ecosystem
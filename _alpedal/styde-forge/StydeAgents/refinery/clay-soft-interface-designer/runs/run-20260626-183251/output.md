Fas 0.5 — Design mockups
dashboard name: "Alpedal Clay Forge"
concept: A pastel-toned project monitoring dashboard where each running forge agent is a touchable clay card with depth and squish
----------------------------------------------------------------------
LAYOUT STRUCTURE
viewports:
  desktop: 3-column grid, 200px pie chart, full sidebar
  tablet: 2-column grid, 160px pie chart, icon-tray sidebar
  mobile: 1-column stack, 120px pie chart, bottom nav bar
grid:
  columns: 12
  gutter: 16px
  outer margin: 24px
  max-width: 1280px centered
sidebar:
  mobile: hidden, triggers bottom sheet
  tablet: icon tray (48px icons, labels on hover)
  desktop: full labels + icons, width 220px
----------------------------------------------------------------------
COLOR PALETTE
core pastels:
  clay-pink:    #f8d7da
  clay-peach:   #fce4d6
  clay-lavender:#e8d5f5
  clay-mint:    #d4f0e8
  clay-sky:     #d6ecf8
  clay-cream:   #fdf6e3
accent depth:
  shadow-base: rgba(160, 120, 110, 0.12)
  shadow-hover: rgba(160, 120, 110, 0.2)
  shadow-pressed: rgba(160, 120, 110, 0.06)
text:
  primary:   #3d2e2a
  secondary: #7a6560
  muted:     #b8a8a3
bar chart colors (8 bars):
  odd (1,3,5,7): clay-peach #fce4d6
  even (2,4,6,8): clay-lavender #e8d5f5
pie chart segments:
  segment-A: clay-pink
  segment-B: clay-lavender
  segment-C: clay-mint
  segment-D: clay-sky
----------------------------------------------------------------------
COMPONENT SPECS
card:
  border-radius: 16px
  padding: 24px
  background: white
  box-shadow: 0 8px 32px shadow-base
  transition: box-shadow 0.3s cubic-bezier(0.25, 0.1, 0.25, 1.0)
  hover: box-shadow 0 12px 48px shadow-hover, translateY -2px
  pressed: box-shadow 0 2px 8px shadow-pressed, translateY 0
button:
  border-radius: 12px
  padding: 10px 20px
  font-size: 14px
  font-weight: 600
  primary: clay-peach, text #3d2e2a
  secondary: clay-cream, text #7a6560
  ghost: transparent, text #7a6560, hover bg clay-cream
input:
  border-radius: 8px
  border: 2px solid #e8ddd8
  padding: 10px 14px
  font-size: 14px
  focus: border clay-sky, box-shadow 0 0 0 3px rgba(214, 236, 248, 0.4)
tooltip:
  background: white
  border-radius: 8px
  padding: 8px 12px
  box-shadow: 0 4px 16px shadow-base
  font-size: 12px
  trigger: bar hover only (60px max hover zone width)
  offset: 8px above bar top
----------------------------------------------------------------------
WIDGET MOCKUPS
widget-group: "Agent Status"
  widget-1: "Forge Health"
    type: pie-chart
    diameter: 200px (desktop) / 160px (tablet) / 120px (mobile)
    data:
      idle: 4
      running: 7
      error: 1
      paused: 2
    segments: 4 (clay-pink, clay-lavender, clay-mint, clay-sky)
    center circle: white, 40% of diameter, text "14 agents"
    description: "Overall agent fleet status. Hover for per-segment count."
  widget-2: "Throughput (7d)"
    type: bar-chart
    bars: 8
    odd-color: clay-peach
    even-color: clay-lavender
    bar-width: 40px
    max-hover-zone: 60px
    x-labels: "M T W T F S S M"
    y-range: 0 to 100
    tooltip: "{bar}: {value} tasks"
    description: "Daily task completions. Hover bars for detail."
  widget-3: "Active Blueprints"
    type: stat-cards (3 small cards in a row)
    card-a: "Production" count: 12, icon: check
    card-b: "Staging" count: 8, icon: refresh
    card-c: "Draft" count: 5, icon: edit
    each card: 16px radius, soft shadow, stacked slightly overlapping (z-index +1 rightward)
widget-group: "Resource Monitor"
  widget-4: "Memory Usage"
    type: horizontal-stacked-bar
    segments: clay-mint (used 6.2GB), clay-peach (cache 1.1GB), clay-cream (free 0.7GB)
    total: 8GB
    label: "6.2 / 8.0 GB"
    description: "Per-agent memory breakdown. Click for process list."
  widget-5: "Sub-agent Queue"
    type: list-cards
    items:
      - "blueprint-optimizer" status: running, priority: high, eta: 12s
      - "prompt-refiner-v3" status: queued, priority: medium
      - "format-validator" status: queued, priority: medium
      - "schema-checker" status: completed, priority: low
    each item: card with left colored border (clay-peach=running, clay-lavender=queued, clay-mint=completed)
  widget-6: "Recent Feedback Scores"
    type: mini-line-chart
    data points: [78, 82, 80, 84, 82, 82, 79]
    line color: clay-sky, stroke-width: 3, smoothed
    fill: clay-sky at 15% opacity
    current: 79
    trend: -3 (downward, soft red indicator)
    description: "7-run composite score. Hover for per-run breakdown."
----------------------------------------------------------------------
SPECIAL INTERACTIONS
card stacking:
  stat-cards stack with 12px offset on bottom and right
  each card gets z-index +1 relative to siblings
  on hover, stacked card lifts (translateY -4px, z-index 20)
  shadow expands proportionally
bar chart hover:
  only bar rectangle triggers tooltip (max 60px width per bar)
  no tooltips on axis, labels, title, or background
  hovered bar gains clay-sky overlay at 20% opacity
  adjacent bars stay unchanged (no gradient blending)
pie chart segment hover:
  segment scales outward 4% with origin at center
  tooltip shows count and percentage
  non-hovered segments reduce opacity to 70%
----------------------------------------------------------------------
DOM BUDGET ACCOUNTING
containers per view: 16 (under 20 cap)
  - sidebar (1)
  - main grid container (1)
  - widget-1 card (1)
  - widget-2 card (1)
  - widget-3 card-with-subcards (1 parent + 3 children = 4)
  - widget-4 card (1)
  - widget-5 card (1)
  - widget-6 card (1)
  - top nav bar (1)
  - footer info bar (1)
  - modal overlay (1, hidden)
  - tooltip container (1, hidden)
nesting depth: 3 levels max (grid > card > content block)
color transitions: 5 (bg-sidebar->card, card->button, text-body->link-hover, bar-default->bar-hover, segment-default->segment-hover)
----------------------------------------------------------------------
RESPONSIVE BEHAVIOR
desktop (>=1024px):
  grid: 3 columns
  sidebar: full labels, 220px, visible
  pie: 200px diameter
  stat-cards: row of 3
tablet (768-1023px):
  grid: 2 columns
  sidebar: icon tray only (48px), labels on hover
  pie: 160px diameter
  stat-cards: row of 3, slightly compressed
mobile (320-767px):
  grid: 1 column
  sidebar: hidden, replaced by bottom nav with 4 icons
  pie: 120px diameter
  stat-cards: stacked vertically
  all cards: full width minus 16px outer margins
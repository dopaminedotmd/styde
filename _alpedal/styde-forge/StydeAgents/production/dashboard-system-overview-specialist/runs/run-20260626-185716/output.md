SYSTEM OVERVIEW PANEL v3.0 — MOCKUP SPECIFICATION
10 unique mockups. 2-3 sub-panels each. Tokenized layout. No pixel values.
DESIGN TOKENS (base token map)
  --unit: 1rem (root em)
  --space-3xs: 0.125rem
  --space-2xs: 0.25rem
  --space-xs: 0.375rem
  --space-sm: 0.5rem
  --space-md: 0.75rem
  --space-lg: 1rem
  --space-xl: 1.5rem
  --space-2xl: 2rem
  --space-3xl: 3rem
  --radius-sm: 0.25rem
  --radius-md: 0.5rem
  --radius-lg: 0.75rem
  --radius-xl: 1rem
  --radius-full: 9999rem
  --font-xs: 0.625rem
  --font-sm: 0.75rem
  --font-md: 0.875rem
  --font-lg: 1rem
  --font-xl: 1.25rem
  --font-2xl: 1.5rem
  --thickness-thin: 0.0625rem
  --thickness-md: 0.125rem
  --thickness-thick: 0.25rem
  --opacity-dim: 0.4
  --opacity-mid: 0.65
  --opacity-full: 1
  --ease-out: cubic-bezier(0.16, 1, 0.3, 1)
  --ease-smooth: cubic-bezier(0.65, 0, 0.35, 1)
  --ease-bounce: cubic-bezier(0.34, 1.56, 0.64, 1)
  --duration-instant: 0
  --duration-fast: 100ms
  --duration-normal: 200ms
  --duration-slow: 400ms
  --duration-xslow: 600ms
  --duration-entrance: 800ms
  --color-bg-base: hsl(220 25% 8%)
  --color-bg-panel: hsl(220 25% 11%)
  --color-bg-raised: hsl(220 25% 15%)
  --color-bg-hover: hsl(220 25% 18%)
  --color-bg-active: hsl(220 30% 22%)
  --color-border-subtle: hsl(220 20% 20%)
  --color-border-default: hsl(220 20% 28%)
  --color-border-active: hsl(220 30% 40%)
  --color-text-primary: hsl(220 10% 92%)
  --color-text-secondary: hsl(220 10% 65%)
  --color-text-tertiary: hsl(220 10% 45%)
  --color-text-dim: hsl(220 10% 30%)
  --color-accent: hsl(195 85% 55%)
  --color-accent-dim: hsl(195 50% 30%)
  --color-warning: hsl(35 90% 55%)
  --color-danger: hsl(0 75% 55%)
  --color-success: hsl(140 65% 50%)
  --color-info: hsl(220 70% 55%)
  --color-gpu: hsl(280 65% 60%)
  --color-cpu: hsl(195 85% 55%)
  --color-mem: hsl(140 65% 50%)
  --color-net: hsl(30 80% 55%)
ANIMATION TIMING SPECS
  Panel entrance: stagger children with delay = stagger-index * duration-normal, max stagger total duration-slow
  Gauge fill: duration-slow, ease-out, start from 0 width/height on mount
  Gauge value transition: duration-normal, ease-smooth, only on value change
  Numeric counter: duration-xslow, ease-smooth, count-up on mount
  Pulse indicator: duration-xslow, ease-in-out, infinite alternate for active state
  Tooltip fade: duration-fast, ease-out
  Skeleton shimmer: duration-xslow, linear, infinite, keyframe shimmer-slide
  Error banner slide-down: duration-normal, ease-out
  Empty state fade: duration-normal, ease-smooth
SUB-PANEL STRUCTURE
  Each panel split into 3 sub-panels:
  A — Hardware Gauges (GPU, CPU, Memory, Network sparklines)
  B — Health & Uptime (status indicators, uptime clock, process count)
  C — Critical Alerts (error banner, warnings, maintenance windows)
---
MOCKUP 1 — DASHBOARD GRID (balanced)
  Layout: A | B | C in equal columns, 1fr each, gap space-lg
  A: 4 gauge cards in 2x2 grid, each card = space-2xl x space-2xl
    GPU row: gauge arc (240deg semicircle) with percentage inside, temp label below
    CPU row: horizontal bar gauge, stacked by core (4 segments), total % right
    Memory row: stacked horizontal bar (used/cache/free) in ratio colors
    Network row: mini sparkline (last 60 data points) with current mbps label
  B: vertical stack, space-md between items
    Uptime: large font-xl digital clock, sublabel "uptime" in font-sm text-secondary
    Processes: horizontal bar chart (running/sleeping/zombie) in color-coded segments
    Health ring: circular ring (full 360deg) showing system health %, color transitions from danger to success
  C: single column alert list
    Error banner at top: bg-danger at opacity-mid, border-radius-md, font-sm
    Below: max 3 warning rows, each with icon dot + text on same line
    Empty state: centered text-secondary "No active alerts" with checkmark circle icon
  Skeleton layout:
    A: 4 gray rectangles (bg-raised, border-radius-md) shimmering in 2x2
    B: 3 vertical rectangles (bg-raised, border-radius-md) stacked
    C: 1 full-height rectangle (bg-raised, border-radius-md) with 3 thinner child rectangles
---
MOCKUP 2 — HORIZONTAL STRIP (compact)
  Layout: A B C in single row, A: 3fr B: 2fr C: 1fr, no gaps, separated by vertical divider (thickness-thin, color-border-subtle)
  A: 4 mini gauges side by side, each = 1/4 width of A
    Each mini gauge: label on top (font-xs), value in center (font-lg, bold), tiny bar below (height-space-2xs, border-radius-full)
    GPU bar: color-gpu, CPU bar: color-cpu, Mem bar: color-mem, Net bar: color-net
  B: compact health cluster
    Uptime: font-sm, text-secondary, icon clock before
    Health dot: circle radius-space-sm, color pulsing (CSS animate opacity using pulse duration)
    Process count: font-sm, "47 procs" label
  C: alert counter badge
    Number in font-2xl (red if >0, text-secondary if 0)
    Sublabel "alerts" font-xs
    If alerts >0: small red dot top-right corner of C
  Empty state: C shows "0" in text-secondary, no red dot
  Error state: A gauges show "--" if sensors unavailable, B health dot turns gray (bg-text-dim)
---
MOCKUP 3 — VERTICAL STACK (wide panel)
  Layout: A stacked above B stacked above C, full width, each separated by space-lg
  A: 4 gauge cards in single row, each = 1fr, height-space-4xl
    Each card: top half = semicircular arc gauge (180deg), bottom half = two label rows
    Labels: "GPU: 78%" font-sm, "Temp: 62C" font-xs
  B: two-column layout within
    Left (2fr): uptime clock, font-xl, monospace, digital style
    Right (1fr): process breakdown, stacked mini bars (running in success, sleeping in text-tertiary, zombie in danger)
  C: alert strip, full width, single row
    If alerts exist: scrollable horizontal via overflow-x auto
    Each alert chip: border-radius-full, bg-raised, font-xs, text-secondary, max-width 20ch truncate
    If no alerts: centered checkmark + "All systems nominal" in success color text
  Skeleton: 3 full-width rectangles (height-space-2xl each) with shimmer
---
MOCKUP 4 — COMPACT CARD (corner widget)
  Layout: single card, 3fr height, A+B merged on left (2fr), C on right (1fr)
  A+B: stacked gauge cluster
    Row 1: 4 tiny dots in a row, each = circle radius-space-sm, color = channel color
    Row 2: 4 mini sparklines overlaying each other with opacity, separated by vertical lines
    Row 3: uptime line "Up 3d 14h" font-xs text-secondary
  C: single alert indicator
    If alerts >0: red filled circle radius-space-md with white number inside
    If alerts =0: green filled circle radius-space-md with checkmark inside
    Sublabel "alerts" font-xs text-secondary centered below
  Skeleton: card with 3 shimmer lines (font-sm height, space-md gap) in left portion, right circle gray
---
MOCKUP 5 — GAUGE HEAVY (monitoring focus)
  Layout: A (2fr) | B (1fr) | C (1fr), A takes half width
  A: 2x2 grid of large analog gauges, each = space-3xl x space-3xl
    GPU gauge: 270deg arc, color-gpu, needle sweep on value change, duration-slow ease-out
    CPU gauge: 270deg arc, color-cpu, needle
    Memory gauge: 270deg arc, color-mem, needle
    Disk gauge: 270deg arc, color-net, needle
    Each gauge: center = font-xl bold value, bottom = font-xs label
  B: vitals column
    Top: health score as large number (font-2xl) + sparkline underneath
    Middle: uptime in days, font-md
    Bottom: process count, font-md
  C: warnings list
    Each warning: colored left border thickness-thick border-radius-sm, font-sm text, padding-space-sm
    If empty: "All good" centered text-success
  Skeleton: 4 circles (border-radius-full) with shimmer in A grid, 3 rectangles in B, 3 rectangles in C
---
MOCKUP 6 — DEBUG TERMINAL (developer mode)
  Layout: A (1fr) | B+C (2fr) stacked vertically
  A: raw number cluster
    4 metric squares in 2x2, each = space-2xl
    Each: value in font-xl, delta arrow (up/down/flat), label font-xs
    GPU | CPU | RAM | NET
    Arrow colors: up = success, down = danger, flat = text-tertiary
  B: health bar (single full-width horizontal bar, height-space-md)
    Gradient from red to green, current system health mark as vertical line
    Labels at 0%, 50%, 100% on bar edge
  C: alert log (scrollable, max 3 visible lines)
    Each line: timestamp font-xs text-tertiary, message font-sm text-primary
    Last 3 alerts only
    No alerts: gray placeholder "Log empty"
  Skeleton: 4 rects in A grid, 1 thin full-width rect for B, 3 text-width rects for C
---
MOCKUP 7 — DASHBOARD FOOTER (edge-to-edge)
  Layout: full width strip, height-space-3xl, A C B in row with proper spacing
  A: GPU/CPU mini bars
    Two small horizontal bars stacked, each = width-space-xl, height-space-xs, border-radius-full
    Labels overlaying: "GPU 78" | "CPU 45" font-xs
  C: alert dot (same as mockup 4 C, reduced size)
  B: uptime + health in one cluster
    "3d 14h" font-sm + green dot together
    Separated by thin vertical line from process count
  No skeleton needed — all numbers render as "--" on loading
  Animation: bars fill from 0 width on mount, dot scales from 0 to full
---
MOCKUP 8 — ALERTS-FIRST (ops panel)
  Layout: C (1.5fr) | A (1fr) | B (1fr), alerts prioritized
  C: scrollable alert feed, max 5 items
    Each alert: left red/gray dot, title font-sm bold, description font-xs text-secondary, time font-xs text-tertiary on right
    Header: "ALERTS (3)" font-md bold with clear-all button on right
    No alerts: full-height "No alerts" with large checkmark circle icon, text-secondary
  A: compact gauge cluster in single row
    3 mini circles (radius-space-lg) with proportional fill
    GPU blue, CPU cyan, Mem green
    Value label underneath each
  B: single health indicator
    Large circle (radius-xl) with system health %
    Color: >80 = green, >50 = yellow, <50 = red
    Sublabel: "uptime 3d" font-xs
  Skeleton: C has 5 horizontal rects stacked, A has 3 circles gray, B has 1 big circle gray
---
MOCKUP 9 — GRID EXTREME (data dense)
  Layout: 3x3 grid of equal cells (all 1fr), 9 total
  Row 1: GPU gauge, CPU gauge, Memory gauge (all analog semicircles from mockup 1)
  Row 2: Disk gauge, Network sparkline+value, Uptime clock
  Row 3: Process count bar, Health ring, Alert counter
  Each cell = space-2xl x space-2xl, gap space-sm
  Cell 7 (process): stacked horizontal bars by state
  Cell 8 (health): circular ring (360deg) with percentage in center, gradient from red to green
  Cell 9 (alert): number big, dot badge, if 0 show green "OK"
  Skeleton: 9 gray rects in grid, shimmer pattern staggered by 50ms per cell
---
MOCKUP 10 — MINIMAL (status bar variant)
  Layout: single line, height-space-xl, no sub-panels per se but implicit A-B-C as regions
  A (left): GPU icon + value | CPU icon + value | Mem icon + value
    Each: icon (tiny svg dot) + number in font-xs, space-sm between groups
    Separator after A: thin vertical line, height-space-md
  B (center): health dot color + "UP 3d"
    Dot radius-space-2xs, green pulsing
  C (right): alert count
    If >0: red pill border-radius-full with number, font-xs
    If 0: small green checkmark
  Skeleton: all values show "--", health dot gray, alert pill empty
  Animation: values count-up on mount with stagger delay
ERROR STATE SPEC (all mockups)
  Any sub-panel that fails to load sensor data:
    Replace gauge/bar with dashed outline (border style dashed, color-text-tertiary)
    Show "--" instead of value in text-tertiary
    Add small tooltip on hover: "Sensor unavailable"
    Tooltip animation: fade in duration-fast, ease-out, delay 200ms
  If whole panel fails:
    Error banner: full width, bg-danger at opacity-mid, border-radius-md, padding-space-md
    "System metrics unavailable. Retrying in 15s..." text font-sm
    Retry countdown shown as small circle timer (CSS animation, 15s linear)
    After 3 consecutive failures: replace banner with "Connection lost" and manual refresh button
EMPTY STATE SPEC (all mockups)
  First boot / no data:
    Each sub-panel shows skeleton shimmer for 1.2s, then fades to empty state
    Sub-panel A (gauges): "Waiting for first data point" centered in text-tertiary font-sm
    Sub-panel B (health): "System starting up" with pulsing green dot
    Sub-panel C (alerts): "No alerts" with checkmark icon
    Empty state background: slightly different bg-panel with checkerboard pattern at opacity-0.05
PERSONA REDESIGN (replaces previous redundant persona)
  Name: System Gauge Architect
  Voice: utilitarian, surgical, numbers-first
  Heuristics:
    Never show a number without a reference frame (min/max, color scale, or percentile)
    Always prefer proportional gauge fill over absolute values
    Use color only for status — never for decoration
    Every gauge must be readable at 3 distances: close (detail), arm's-length (trend), across-room (alert)
    If a metric has no threshold, it does not get a color
  Guardrails:
    No gauge under 16px height — below that, use a dot
    No more than 4 gauges per sub-panel without an aggregation layer
    No animation faster than 100ms — causes flicker on rapid updates
    No monospace fonts for labels — only for numeric values
    No shadows on gauges — depth suggests interactivity where none exists
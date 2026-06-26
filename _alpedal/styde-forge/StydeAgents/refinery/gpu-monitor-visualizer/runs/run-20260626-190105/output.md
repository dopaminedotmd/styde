BLUEPRINT.md — GPU Monitor Visualizer
Domain: frontend  Version: 3  Score target: 95+
---
PURPOSE
Design GPU monitoring views for Forge dashboard. Real-time GPU metrics served as primary visualization layer — temperature heat-maps, utilization sparklines, VRAM allocation bars, fan curves, power envelope, clock domain tracking. Hardware data rendered as art. Glanceable at arm's length, drillable on inspection.
---
PERSONA — capabilities
- visual regression testing: validate real-time metric rendering against reference frames
- generative layout validation: ensure responsive grid reflow at 4 breakpoints
- accessibility compliance review: WCAG 2.1 AA contrast on all metric overlays
- thermal gradient analysis: color-map temperature deltas across GPU zones
- time-series sparkline synthesis: render utilization history at 3 granularities (5s/60s/600s)
- memory topology mapping: visualize VRAM allocation as block heat-map per process
- power envelope profiling: plot TDP ceiling vs actual draw with boost headroom
- clock domain tracking: core/mem/boost clock as stacked area chart
---
UX/UI — CORE COMPONENTS
1. Thermal Heat-Map Canvas
   Full-GPU outline (2048px logical width) with per-sensor temperature dots. Dots sized 12px-28px based on sensor variance. Color ramp: deep blue (30C) through teal (50C) through amber (70C) through red (90C+). White radial glow on hottest sensor. Auto-calculated midpoint of visible range anchors color spread. Hover shows sensor ID + temp + location. Click locks crosshair overlay on that sensor across all other panels.
   States:
   - loading: skeleton outline with pulsing gray dots at 40% opacity, shimmer animate 1.5s
   - empty: no sensors detected — dashed outline, centered message "No GPU temperature sensors found", retry button
   - error: red dashed outline, "Sensor read failed — driver error [code]", manual refresh button, auto-retry countdown
   - edge: single sensor — center dot at normal size, all others hidden, tooltip "Single sensor detected"
2. Utilization Sparkline Array
   Row of 4 sparkline cards (GPU core, memory controller, video encode, PCIe bus). Each card: current value as large numeral top-left, sparkline SVG right (320x60 viewport, 60 data points, 1s interval smooth). Active color fills below line with gradient fade to transparent. GPU core line: teal. MC line: purple. Encoder: amber. PCIe: cyan. Latest value dot glows on update.
   States:
   - loading: flat gray line at 30% height with shimmer sweep
   - empty: flat line at 0%, text "No utilization data" centered on card
   - error: line spikes to 100% and holds, red dot, tooltip "Utilization sensor timeout"
   - edge: single GPU core only — hide other 3 cards, stretch GPU card to fill row width
3. VRAM Allocation Bar
   Horizontal stacked bar 100% width. Segments: used (solid teal gradient), cache (diagonal hatch pattern), reserved (dashed outline), free (40% opacity fill). Total VRAM label left, used/remaining fraction right. Bar height 36px. On hover, segment tooltip shows exact GB + process count. Click expands to per-process allocation table below bar.
   States:
   - loading: gray bar pulsing at 60% fill, shimmer
   - empty: bar at 0%, "No VRAM in use", dimmed text
   - error: bar full 100% red, "Unable to query VRAM", retry button
   - edge: single process using >90% — bar turns amber with warning pulse
4. Power Envelope Gauge
   Semicircular gauge 200px wide. Arc sweeps from 180deg (0W) to 0deg (TDP max). Current draw as thick stroke with gradient (green through amber through red based on % of TDP). Remaining arc is 15% opacity gray. Center: large numeral current watts, smaller below showing % of TDP. TDP ceiling marked as dashed line at top. Boost headroom shown as thin pulse arc beyond TDP when active.
   States:
   - loading: gauge at 50% sweep, gray pulsing
   - empty: 0W, gauge at bottom, "Idle — no power data"
   - error: gauge pinned at 100%, red, "Power sensor error"
   - edge: sustained >90% TDP — amber-to-red glow on gauge border, "Power limit approaching" warning
5. Clock Domain Stacked Area
   Stacked area chart 400x200px. 3 layers: core clock (base), memory clock (stacked), boost clock (overlay). X-axis: last 60s, 1s intervals. Y-axis: MHz. Core clock fill solid with subtle noise texture. Memory clock offset atop with diagonal hatch. Boost clock as semi-transparent overlay with bright stroke. Latest MHz values displayed as floating labels at end of each line. Hover vertical line crosshair with exact values at timestamp.
   States:
   - loading: 3 flat lines at 0, 0, 0 with shimmer
   - empty: lines at 0, 0, 0, "No clock data", dimmed 40%
   - error: lines spike to max and flat, "Clock sensor read failed"
   - edge: only core clock reporting — show single line at full height, hide other layers
6. Fan Speed Tachometer Set
   Vertical stack of horizontal gauge bars, one per fan. Each bar: label left (Fan 1, Fan 2), current RPM as numeral, bar fill proportional to max RPM (0-max). Color gradient: below 50% RPM = cool blue, 50-80% = teal, above 80% = amber. Bar height 24px with 8px gap between fans. Right side: aggregate noise estimate based on RPM sum. If fan count >4, collapse to compact mode (12px bars, no labels).
   States:
   - loading: all bars at 50% fill, shimmer
   - empty: all bars at 0%, "No fan data — passive cooling?"
   - error: all bars red, "Fan controller unresponsive"
   - edge: single fan — hide aggregate, center bar full width
7. Process Topology Map
   Circular layout 300x300px. Center dot = GPU total. Surrounding radial dots = processes using GPU. Dot size proportional to VRAM consumption. Color by process type: game (orange), render (magenta), AI inference (green), unknown (gray). Lines from center to process dot colored by utilization %. Hover reveals process name + VRAM + PID. Click opens process detail in side panel.
   States:
   - loading: center dot pulsing, no satellite dots
   - empty: center dot only, "No active GPU processes"
   - error: center dot red, "Process enumeration failed"
   - edge: 1 process — single satellite, label overlays on hover only
8. Historical Mini-Grid
   3x2 grid of 120x80px mini charts. Each cell = last 600s of one metric (temp, util, VRAM, power, clock, fan). All charts use same time axis synced across cells. X-axis: last 10 min, 1 min ticks. Y-axis: auto-scaled per metric. Color per metric matches main panels. Latest value floating top-right of each cell. On hover, cell expands to full-width preview.
   States:
   - loading: all cells flat gray, shimmer
   - empty: flat lines at baseline (0 or idle temp), "Waiting for history data"
   - error: all cells show error icon, "History data unavailable"
   - edge: <60s of data — cells show partial curves, "Collecting..." label
9. Temperature Delta Matrix
   4x4 grid of cells representing GPU die zones. Each cell: delta from average temp as directional indicator. Color: cooler than avg = blue gradient, hotter than avg = red gradient. Delta value centered in cell in degC (e.g. +3.2). Cells saturated in proportion to absolute delta (max saturation at 10C delta). Background: subtle grid lines matching 4x4 sensor layout. On click, locks hotspot overlay across all panels.
   States:
   - loading: all cells at 0 delta, gray, shimmer
   - empty: all cells at 0, "No thermal sensor matrix data"
   - error: random deltas spiking, "Thermal sensor calibration error"
   - edge: 1 sensor — single cell full width, "Single thermal zone"
10. Alert Condition Waterline
    Horizontal scrolling ticker at viewport bottom. Each alert: icon + metric name + current value + threshold. Color: warning (amber), critical (red), resolved (green fade to transparent). Auto-scroll at 2s per item. Pause on hover. Max 6 visible items, queue beyond scrolls in. Empty state shows "All metrics nominal" in green. Error state: "Alert system disconnected" in red flashing.
---
SPECIFICATION SUMMARY TABLE
| Component | Width | Height | Colors | Data Points | Update Interval |
|-|-|-|-|-|-|
| Thermal Heat-Map | 100% | 240px | blue-teal-amber-red | per-sensor dots | 500ms |
| Utilization Array | 4x 25% | 80px | teal/purple/amber/cyan | 60 | 1s |
| VRAM Bar | 100% | 36px | teal / hatch / dashed | 4 segments | 1s |
| Power Gauge | 200px | 110px | green-amber-red | 1 value + TDP | 500ms |
| Clock Stacked | 400px | 200px | 3-layer fill | 60 | 1s |
| Fan Tachometer | 100% | per-fan 24px | blue-teal-amber | per fan RPM | 1s |
| Process Map | 300px | 300px | orange/magenta/green | N processes | 2s |
| History Mini-Grid | 3x2 cells | 120x80px | per-metric | 600 | 10s |
| Temp Delta Matrix | 4x4 cells | 40px each | blue/red saturation | 16 zones | 1s |
| Alert Waterline | 100% | 28px | amber/red/green | max 6 visible | as triggered |
---
HARDWARE REQUIREMENTS
| Metric | Target | Max | Tolerance | Update Rate |
|-|-|-|-|-|
| Power draw | 250W | 450W | +/-5W | 500ms |
| Boost clock | 2505 MHz | 2800 MHz | +/-15 MHz | 500ms |
| Memory clock | 1750 MHz | 2000 MHz | +/-10 MHz | 500ms |
| Core temp | 65C | 110C | +/-1C | 500ms |
| VRAM temp | 75C | 95C | +/-1C | 500ms |
| Fan speed | 1500 RPM | 3500 RPM | +/-50 RPM | 1s |
| Utilization | 60% | 100% | +/-1% | 1s |
TDP ceiling: 100% = 280W (default configurable). Boost headroom shown as thin pulse arc beyond TDP line on power gauge. Clock domains have independent throttling — each domain's area chart respects its own max ceiling.
---
LAYOUT BREAKPOINTS
| Breakpoint | Width | Columns | Changes |
|-|-|-|-|
| desktop | >1024px | 4 | Full layout: heat-map top span 4, util row span 2, VRAM bar under, power+clock right col, fan+tacho bottom row |
| tablet | 768-1024px | 2 | Heat-map span 2, util row stacks 2x2, power+clock move to full width row |
| mobile | 480-767px | 1 | All panels stack vertically, heat-map reduces to 100% width 180px height, sparkline cards collapse to inline mini view |
| narrow | <480px | 1 compact | Mini-view: only gauge + utilization shown, rest accessible via row toggle |
---
ACCESSIBILITY REQUIREMENTS
- All metric overlays maintain WCAG 2.1 AA contrast (minimum 4.5:1 text, 3:1 large text)
- Color is never sole information channel — patterns, icons, and numeric labels accompany all color-coded metrics
- Thermal heat-map includes grayscale gradient as fallback
- Sparklines have aria-label reading current value + trend direction
- VRAM bar segments distinguishable by pattern (hatch/dashed/solid) in addition to color
- All panels keyboard-navigable via Tab with visible focus ring (2px white + 2px black double outline)
- Screen reader announcements on metric updates at 5s debounce (not every frame)
- Ticker alerts emit aria-live=polite on new items
- Motion preference reduced: animations degrade to 0.5x speed or snap transitions
---
IMPLEMENTATION NOTES
- Canvas-rendered heat-map allows per-pixel temperature interpolation
- SVG sparklines for crisp rendering at any scale
- CSS paint worklet for diagonal hatch patterns on VRAM cached segment
- WebSocket feed for sub-second updates, falls back to polling at 500ms
- GPU compute shader for thermal interpolation if available (WebGL fallback)
- FPS capped at 30 for rendering tick to reserve CPU for metric collection
- Alerts use CSS scroll-driven animations for ticker
gpu-monitor-visualizer BLUEPRINT v2 — incorporating both feedback sessions
PURPOSE
Real-time GPU monitoring views for Forge dashboard. Temperature heat-maps, utilization sparklines, VRAM allocation bars, fan curves, power/clock metrics. Data as functional art — glanceable at 2m, detailed at 30cm.
DOMAIN: frontend     VERSION: 2
PERSONA
GPU Monitor Visualizer. Expertise: heat-map color-theory encoding, generative layout validation for monitoring UIs, visual regression testing of real-time chart renders, accessibility compliance review for color-coded metrics, sparkline density optimization, VRAM allocation topology mapping, fan-curve harmonic visualization.
CAPABILITIES
  visual-regression-testing
  generative-layout-validation
  accessibility-compliance-review
  heat-map-color-theory-encoding
  sparkline-density-optimization
  vram-allocation-topology-mapping
  real-time-metric-orthogonal-layout
HARDWARE REQUIREMENTS
  performance:
    power-draw:
      target: 150W
      max: 250W
      tolerance: 10%
      alert-threshold: 85%
    clock-speed:
      gpu-core:
        target: 2100 MHz
        max: 2550 MHz
        tolerance: 5%
        throttle-warning: 95%
      memory:
        target: 1000 MHz
        max: 1200 MHz
        tolerance: 5%
    vram:
      segments: 8
      per-segment-label: true
UX/UI
State Handling:
  Loading:
    skeleton frame matching final layout dimensions
    each metric card pulses at staggered intervals
    sparkline area shows a gentle wave skeleton
    heat-map area fades in after skeleton settles
    animation: cards fill top-down, left-right
  Empty:
    only occurs on first boot with zero GPU data
    displays 'awaiting first metrics sample' with subtle pulsing circle
    placeholder text in each metric slot
  Error:
    sensor-read-failure: card turns diagonal-striped grey, shows broken-sensor icon, retry button
    driver-disconnected: all cards grey, reconnect button, last-known values shown dimmed
    timeout: orange border on affected card, 'stale data' label, last-updated timestamp
  Edge cases:
    zero-utilization: still show baseline sparkline at zero, no empty card
    max-utilization (100%): card border glows at threshold color, no overflow
    VRAM overflow: bar turns red, shows overflow count in negative
    fan failure: RPM shows 0 with alert icon, does not hide the card
    temperature beyond scale: color locks to extremes (deep purple for ice, white-hot for max), shows raw value numerically
Responsive Behavior:
  breakpoints:
    wide (>=1400px): 4-column grid, full expanded heat-map, dual sparkline panels
    medium (900-1399px): 3-column grid, collapsed heat-map to single row, stacked sparklines
    narrow (600-899px): 2-column grid, heat-map becomes compact bar, single sparkline column
    mobile (<600px): 1-column vertical stack, all charts become mini, numeric values take priority
  content-shift-protection: all cards use fixed-aspect containers during resize
  touch: sparklines gain 48px touch targets for hover states
  color-blind palette: patterned overlays (dots, stripes, crosshatch) on all heat-map and bar elements
MOCKUPS — 10 unique views
=== MOCKUP 1: Master Grid (default state) ===
A 2x4 grid of metric cards across the dashboard body.
Row 1: Temperature heat-map card | VRAM allocation card | Utilization sparkline card | Power draw card
Row 2: Clock speed card | Fan speed card | Memory temperature card | GPU health composite card
Each card is 260x180px with a dark-glass background (#0d1117 base, 10% opacity white glass overlay, 1px border at 20% opacity). Cards have a subtle glow on hover.
Header bar above shows GPU count, aggregate health dot (green/yellow/red), and live timestamp counter.
=== MOCKUP 2: Temperature Heat-Map ===
Full-width expanded view, 800x300px.
Left 70%: 8x6 grid of thermal sensors mapped as colored cells. Color gradient from deep blue (30C) through teal (50C), green (60C), yellow (70C), orange (80C), red (90C), to white-hot purple (100C+). Each cell shows its sensor label and temp value in white text, opacity 85%.
Right 30%: Temperature history mini-sparkline per sensor row, last 60 seconds. Each row 12px high, color-matched to current temp zone.
Bottom: Color legend bar with temperature values at interval marks.
=== MOCKUP 3: VRAM Allocation ===
Full expanded, 600x250px.
Horizontal stacked bar showing 8 memory segments. Each segment is a colored block proportional to its allocation percentage. Color gradient: green (<40%), amber (40-70%), orange (70-90%), red (>90%).
Numeric labels above each segment: USED / TOTAL in small type below.
Below the bar: a table row listing top 3 processes by VRAM consumption — process name, PID, MB used.
Right side: donut chart showing free vs used with exact GB values center-aligned.
=== MOCKUP 4: Utilization Sparkline ===
Card expanded, 400x200px.
Dual-panel design:
Panel 1 (70% width): Sparkline of GPU utilization over last 120 seconds. Fill area beneath the line uses gradient matching intensity — green for low loads, transitioning to amber and red at peak. Line is 2px white with subtle glow. X-axis shows time markers, Y-axis shows 0-100%.
Panel 2 (30% width): current value big number — 63% — with a mini radial gauge behind it showing the same proportion.
Below both: aggregate stats — avg, min, max over current window.
=== MOCKUP 5: Power Draw Gauge ===
Arc-style gauge, 400x300px.
Semicircular gauge spanning 180 degrees. Left endpoint 0W, right endpoint 250W. The arc fills with a gradient from green through yellow to red as power increases. A bright white needle points at current draw value (e.g., 172W).
Center of gauge shows large numeric: 172W, with small subtitle: 69% of TDP.
Below the gauge: a mini bar showing power draw over last 60 seconds, with a horizontal threshold line at 212.5W (85% alert).
=== MOCKUP 6: Clock Speed ===
Card expanded, 400x180px.
Split horizontally:
Left half: GPU core clock. Vertical bar chart showing last 8 readings, each bar 30ms wide. Color intensity maps to clock frequency — dimmer at low clocks, brighter near max. Current value as big number: 2145 MHz.
Right half: Memory clock. Same format, different color hue (teal vs the core clock's magenta).
Below both: a crosshair comparison — current clock vs target (2100) vs max (2550). Small green checkmark if within tolerance, orange warning if throttling.
=== MOCKUP 7: Fan Speed + Fan Curve ===
Expanded view, 400x240px.
Left 60%: RPM gauge. Vertical-oriented card showing current RPM as a liquid-fill thermometer style bar. At the top, RPM number in large type: 1850 RPM. Below, percentage of max: 46%.
Right 40%: Fan curve graph. Tiny 2D plot with temperature on X (30-100C) and fan speed % on Y (0-100%). Current operating point shown as a glowing dot on the curve. Curve line is smooth cubic, colored by temperature zone.
Below: individual fan breakdown lines if multi-fan GPU — show as small up to 3 stacked mini-bars.
=== MOCKUP 8: Memory Temperature ===
Expanded view, 400x160px.
Horizontal segmented bar showing each VRAM module as a colored square block (e.g., 12 blocks for 12GB, or 8 for 8 modules). Each block is 20x20px with its temperature in 8px type inside.
Blocks color-mapped same gradient as WUXI heat-map (blue-cold to white-hot).
Below: summary line — junction temp, hottest module, average temp.
=== MOCKUP 9: GPU Health Composite ===
Compact card, 260x180px.
Five small horizontal bars stacked vertically, each 6px tall:
- Temp health: green/yellow/red bar based on proximity to throttle
- Utilization balance: shows variance across compute/mem/copy engines
- Power efficiency: actual vs TDP ratio
- Clock stability: variance from target clock
- Memory health: ECC error count visualization (shown as tiny sparkline)
At the bottom: overall score as a single digit out of 100 (e.g., 92) in a circular badge. Color of badge matches score zone.
=== MOCKUP 10: Color-Blind + Accessible Variant ===
Same as Mockup 1 Master Grid but with these modifications:
Temperature heat-map cells gain diagonal hatch pattern — direction of hatch encodes temperature zone.
VRAM bars gain dotted overlays — dot density encodes fullness percentage.
Utilization sparkline gains area fill as crosshatch instead of solid gradient.
Health composite bars gain distinct icon symbols (thermometer, lightning bolt, gauge, clock, shield) as primary indicator, color as secondary.
All threshold-based color changes also have text labels (e.g., "WARN", "CRIT", "OK") embedded at 1px height on the bar itself.
Legend panel added to right side explaining all pattern mappings.
IMPLEMENTATION NOTES (appendix, not main spec body)
  Color-stop mapping for VRAM segments uses OkLCh interpolation for perceptual uniformity — not sRGB linear. Stop 1 (0%): OkLCh 90 30 160 (soft teal). Stop 2 (100%): OkLCh 50 80 30 (deep vermilion).
  Sparkline rendering uses Canvas 2D with requestAnimationFrame at 1s intervals — not WebGL, as data density (120 points over 120s) is low enough for 2D. Back-buffer allocation prevents GC pressure.
  Heat-map cell colors use a 12-stop interpolation for smooth gradients. Stop values precomputed and stored as CSS custom properties to avoid per-frame color math.
  Fan curve smoothing uses Catmull-Rom spline through 5 calibration points.
  Clock stability sparkline uses a 1Hz low-pass filter on raw clock readings before plotting.
  VRAM segments align to physical memory controller partitions where available (nvidia-smi query), otherwise fall back to equal division.
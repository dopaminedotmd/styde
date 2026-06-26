GPU Monitor Visualizer — Design Mockups
Domain: frontend  Version: 1.1
Capabilities:
  gpu-visualization: Render real-time GPU metrics as layered thermal-art dashboard panels with sub-second refresh
  thermal-heatmap-engineering: Map per-sensor temperature data to gradient fields with hotspot highlighting and adaptive color scales
  sparkline-composition: Compact time-series utilization graphs at 60-120 sample windows with peak/max/avg markers
  vram-memory-bar-design: Stacked horizontal bars showing used/cached/free memory with color-coded thresholds at 80% and 95%
  interaction-design-for-monitoring: Hover-reveal detail panels, drag-reorderable chart tiles, pinch-zoom time windows
  responsive-layout-for-dashboard: Fixed-height metric row on desktop, collapsible card stack on tablet, single-column scroll on mobile
Components:
1. Thermal Tile — Primary Display
  layout: Fixed 1:1 square card, 240px base (scales to grid)
  content:
    - Center: Large temperature readout in degrees C (2em, mono digit font)
    - Background: Full-tile heatmap gradient from blue(30C) through green(60C) through yellow(75C) through red(85C) to deep-magenta(95C+)
    - Top-right: Delta indicator ( +2C in orange, -1C in teal, =0 in gray )
    - Bottom: Mini sparkline of last 60 samples, 90px wide, 18px tall, transparent fill with colored stroke matching current heat level
    - Edge glow: subtle pulsing glow when temp crosses 80C threshold
  states:
    loading: Skeleton square with animated gradient pulse, "--" for temperature, no sparkline
    empty: Gray scale bar showing "No sensor data" centered, ghost sparkline line
    error: Card border turns dashed red, center shows "Sensor error" with retry icon, last known value shown faded at 40% opacity in small text below
    edge-high-temp: Card border turns orange at 75C (warning glow), red at 85C+ (pulse alert), fan icon appears top-left
    edge-no-history: Sparkline area shows "Insufficient data" text instead of graph when samples < 3
2. Utilization Sparkline Card
  layout: Horizontal bar, 100% width of parent column, 80px height
  content:
    - Left: Metric label "GPU Util" in small caps, 0.75em
    - Center: Sparkline spanning remaining width, 60px height, filled area under curve at 20% opacity
    - Right: Current percentage in bold 1.5em, color-coded (green <50%, yellow 50-80%, red >80%)
    - Hover overlay: crosshair line at cursor position, tooltip with exact value and timestamp
  states:
    loading: Flat line at 0% with shimmer overlay, "--" for percentage
    empty: Flat dashed line at 0%, "0%" shown in gray
    error: Red "!" badge on right, sparkline shows last cached data in dashed style, percentage shows "ERR"
    edge-idle: When utilization < 5% for > 30s, card dims to 60% opacity, shows "Idle" badge
    edge-capped: When utilization > 95% for > 10s, card border pulses red, "Throttling" warning appears
3. VRAM Memory Bar
  layout: Full-width horizontal bar, 48px height
  content:
    - Background track: Dark base, rounded corners 4px
    - Filled segments: Used (blue), Cached (teal), Compute (purple), Free (dark gray)
    - Percentage labels: Segment widths proportional, values shown inside each segment if > 8% width
    - Right side: Total VRAM label (e.g. "24 GB GDDR6X")
    - Below bar: Compact legend row with color dots and segment names
  states:
    loading: Solid gray bar with animated loading stripe, "Detecting..." text
    empty: Bar shows 100% free (dark gray), "No allocation" text
    error: Bar shows last known allocation in hatched pattern, "Memory read failed" below
    edge-oom: When used + cached > 90%, bar end turns red with "OOM Risk" badge pulsing
    edge-realloc: Brief flash animation on bar when allocation changes by > 500MB in one sample
4. Hardware Metrics Cluster
  layout: 2x2 compact grid, each cell 120x80px
  cells:
    - Power Draw: Watts (W) in large text, small sparkline below, color grad from green(50W) to yellow(200W) to red(350W+), max label below bar
    - Clock Speed: MHz value, dual-bar showing current vs boost clock, gap highlighted if thermal throttling
    - Fan Speed: RPM value, radial arc gauge 70px diameter, percentage text center, blade-icon visual
    - Voltage: mV reading, simple numeric, green/yellow/red dot indicator
  states:
    loading: Each cell shows "--" value with skeleton shimmer
    empty: "N/A" in gray for missing sensors
    error: Cell border dashed, "Sensor fail" text, cross icon
    edge-power-limit: When power > 95% of TDP, cell border glows amber, "TDP limit" badge
    edge-thermal-throttle: Clock speed cell shows red gap bar, "Throttled" text below MHz value, temperature badge in corner
    edge-voltage-drop: When voltage drops > 50mV within 3 samples, caution triangle appears with "Vdroop" label
5. Multi-GPU Overview Strip
  layout: Horizontal scrollable strip, each GPU card 160px wide, 100px tall
  content:
    - Per-card: Mini thermal tile (60px square), utilization number, VRAM percentage, power W
    - Selected card: 2px solid border in accent color, slight scale 1.02
    - Scroll: Fade edges on left/right to indicate more content, scrollbar only visible on hover
  states:
    loading: Ghost cards with identical skeleton layout, staggered shimmer animation
    empty: Single card with "+ Add GPU" button, dashed border
    error: Offline GPU cards show grayed out with "Offline" badge, metrics show "--"
    edge-asymmetric: Cards with mismatched models get model-name label overlay (e.g. RTX 4090 vs RTX 3090), different color accent per model family
    edge-missing-gpu: When expected 2 but only 1 detected, subtle "1/2 GPUs online" banner at top of strip
6. Metrics Configuration Panel
  layout: Slide-out panel from right, 320px wide, full height
  content:
    - Toggle switches for each metric visibility (GPU temp, utilization, VRAM, power, clock, fan, voltage)
    - Refresh rate selector: 0.5s, 1s, 2s, 5s (default: 1s)
    - Temperature scale selector: Celsius / Fahrenheit
    - Sparkline time window: 30s, 60s, 5min, 15min, 1hr
    - Alert threshold sliders: High temp, high utilization, low free VRAM
    - Reset to defaults button at bottom
  states:
    loading: Gray toggles in indeterminate state, sliders show "--"
    empty: N/A (panel always has defaults)
    error: Settings that fail to apply get red border with "Apply failed" tooltip, revert to previous value after 3s
    edge-config-override: When Forge dashboard forces a setting, shows lock icon beside that toggle, tooltip "Managed by dashboard"
Specification Summary Table
================================================================
Metric            | Unit    | Range         | Alert Low | Alert High
----------------------------------------------------------------
GPU Temp          | C       | 30-105        | >75 Warn  | >85 Crit
Utilization       | %       | 0-100         | >85       | >95
VRAM Used         | GB      | 0-Max VRAM    | >80%      | >95%
Power Draw        | W       | 0-TDP         | > TDP*85% | > TDP*95%
Clock Speed       | MHz     | idle-boost    | <base     | N/A*
Fan Speed         | %       | 0-100         | N/A       | >85 (noise)
Voltage           | mV      | 700-1200      | <750      | >1150
----------------------------------------------------------------
* Clock: Alert if current < base clock under load (throttle detection)
Color Palette
================================================================
Token           | Hex       | Usage
----------------------------------------------------------------
temp-cold       | #2196F3   | <50C thermal fill
temp-warm       | #FF9800   | 65-75C thermal fill
temp-hot        | #F44336   | 75-85C thermal fill
temp-critical   | #E91E63   | >85C thermal fill
util-low        | #4CAF50   | <50% utilization
util-mid        | #FFC107   | 50-80% utilization
util-high       | #FF5722   | >80% utilization
vram-used       | #3F51B5   | Used VRAM segment
vram-cache      | #009688   | Cached VRAM segment
bg-card         | #1A1A2E   | Card background
bg-page         | #0F0F1A   | Page background
text-primary    | #E0E0E0   | Primary text
text-dim        | #616161   | Dim/muted text
alert-border    | #FF1744   | Critical alert border
success-glow    | #00E676   | Normal range glow
================================================================
Responsive Breakpoints
================================================================
Breakpoint | Width   | Layout
----------------------------------------------------------------
Desktop    | >1200px | 4-col grid, Thermal+Util+VRAM+HW side by side
Tablet     | 768-1199| 2-col grid, stacked metric clusters
Mobile     | <768px  | Single column, accordion collapse per metric type
Compact    | <480px  | Mini mode: show only thermal tile + util sparkline, rest in expandable tray
================================================================
Data Refresh Architecture
  Polling: WebSocket push with 1s fallback to HTTP poll every 2s
  Animation: requestAnimationFrame for smooth gauge/sparkline transitions between data points
  Buffer: 120-sample ring buffer per metric (2min at 1s), FIFO eviction
  Throttle: Visual updates capped at 30fps even if data arrives faster
  Cache: Last known good state persists through page navigation, cleared on dashboard reset
Accessibility Compliance
  Keyboard: All cards focusable via Tab, Enter to expand detail, Esc to collapse
  Screen reader: aria-live=polite on main temperature readout, role=progressbar on utilization and memory
  Color independence: Pattern fills supplement color codes on VRAM bars and thermal zones
  Contrast: All text tokens maintain WCAG AA 4.5:1 ratio against bg-card (#1A1A2E)
This completes the GPU Monitor Visualizer design mockups for Forge dashboard integration. All components include loading, empty, error, and edge-case states. Hardware metrics span temperature, power draw, clock speed, fan speed, and voltage. Specification table and color palette are extracted for efficient reference.
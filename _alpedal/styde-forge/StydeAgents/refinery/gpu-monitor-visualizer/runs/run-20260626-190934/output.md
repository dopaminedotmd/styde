Blueprint: Gpu Monitor Visualizer
Domain: frontend
Version: 2
Purpose
Design GPU monitoring views for Forge dashboard mockups. Real-time GPU metrics, temperature gauges, utilization sparklines, memory bars, fan speed, thermal visualization. Every view must communicate hardware state at a glance while revealing detail on close inspection.
Persona
You are a GPU monitor visualizer. Design beautiful, real-time GPU metrics. Temperature heat-maps, utilization sparklines, memory bars. Hardware data as art. Clear at a glance, detailed on inspection.
Skills
  high-end-visual-design
  interaction-design
  frontend-design
  data-visualization
  accessibility-engineering
Component Inventory
GpuCard (primary)
  Displays metrics for a single GPU. Used in grid and detail views.
  Props:
    gpuId                    string           PCI bus address e.g. 0000:01:00.0
    name                     string           GPU model e.g. NVIDIA RTX 4090
    temperature              number           Current core temp in Celsius
    utilization              number           0-100 percent
    vramUsed                 number           Used VRAM in MB
    vramTotal                number           Total VRAM in MB
    fanSpeed                 number           0-100 percent
    powerDraw                number           Current power draw in watts
    powerLimit               number           Power limit in watts
    clockCore                number           Core clock in MHz
    clockMemory              number           Memory clock in MHz
    sparklineData            number[]         Utilization history, newest last, 60 points at 1s intervals yielding a 60s window
    temperatureHistory       number[]         Temp history, newest last, 60 points at 1s intervals
    gpuIndex                 number           Ordinal shown in header badge
    isStale                  boolean          True when last metric timestamp exceeds 2s ago
    isDisconnected           boolean          True when no data for 10s+
  States:
    connected                Normal streaming. All metrics display live values. Sparkline renders latest window.
    stale                    Metrics frozen at last known values. Subtle pulse animation on border. Label renders Stale Data - last update Ns ago.
    disconnected             Card dims to 60% opacity. Placeholder text No GPU signal fills metric slots. Retry icon visible. All sparklines freeze.
    loading                  Skeleton rectangles matching metric-size ratios. Animated shimmer sweep. No text values. Duration until first metric received or 5s timeout.
    error                    Red border + alert icon. Metric values hidden behind generic dash placeholders. Error message shown in footer. User can dismiss.
  Responsive:
    sm (360-639px)           1 column, compact layout. Labels inline with values. Sparklines hidden. Temperature shown as colored dot.
    md (640-1023px)          2 columns. Metric blocks stacked within card. Sparklines visible at 120px wide.
    lg (1024-1439px)         3 columns. Full metric layout. Sparklines at 200px wide.
    xl (1440px+)             4 columns. All detail visible. Sparklines at 260px wide.
GpuHeader (sub-component)
  Props:
    gpuIndex                 number
    name                     string
    temperature              number
    gpuIndex                 Inherited from parent
  States:
    normal                   Index badge + name + temperature badge inline
    error                    Temperature badge replaced by warning icon
TemperatureGauge (sub-component)
  Props:
    value                    number           Celsius current
    min                      number           Default 0
    max                      number           Default 105
    thresholds               object           {warning: 80, critical: 90, danger: 100}
    size                     string           sm|md|lg
  Color scale:
    < 80C                    green-teal gradient
    80-89C                   amber-orange
    90-99C                   orange-red
    100C+                    red-pulse (animated)
  Accessibility:
    Color contrast ratios: green-teal 4.8:1, amber 5.2:1, red 6.1:1 on dark backgrounds. All pass WCAG AA.
    aria-label: GPU N temperature VALUE degrees. Status: THRESHOLD_LABEL.
    Add aria-live=polite region near gauge for threshold changes.
UtilizationSparkline (sub-component)
  Props:
    data                     number[]         60 points, newest last, 1s interval
    width                    number           Pixel width of SVG
    height                   number           Default 40px
    color                    string           CSS color or gradient reference
    showAxis                 boolean          Default false, show min/max labels on hover
  Behavior:
    SVG polyline with gradient fill below line. No gridlines by default.
    On hover: show vertical crosshair at pointer X position with exact value tooltip.
    On empty data: render dashed baseline at 50% of height with No Data watermark.
VramBar (sub-component)
  Props:
    used                     number           MB
    total                    number           MB
    barType                  string           horizontal|vertical
  States:
    normal                   Filled bar proportional to used/total. Label: N.N GB / N.N GB.
    near-full                Used > 90%. Bar changes to red-orange stripe animation.
    full                     Used > 98%. Solid red with flashing overflow indicator.
    empty                    No GPU detected. Bar renders at 0% with dashed outline and No VRAM data.
FanSpeedIndicator (sub-component)
  Props:
    speed                    number           0-100 percent
    rpm                      number           Optional, actual RPM
  States:
    off                      Fan at 0%. Grey icon, muted label Idle.
    active                   Rotating fan icon, speed proportional to percentage. Color white-to-blue gradient by speed.
    error                    Fan icon replaced by warning triangle. Label Fan Error.
Data Flow Architecture
Source layer (backend/daemon)
  GPU metrics collected by nvidia-smi (NVML) polling at 1s intervals. Each poll produces a snapshot:
    timestamp                ISO 8601
    gpuId                    PCI bus address
    temperature              celsius int
    utilization              percent float
    vramUsed                 MB int
    vramTotal                MB int
    fanSpeed                 percent int
    powerDraw                watts float
    powerLimit               watts float
    clockCore                MHz int
    clockMemory              MHz int
  Snapshots pushed to frontend via WebSocket (wss://host/api/v1/gpu/metrics/stream).
  Historical queries (past N minutes) served over REST GET /api/v1/gpu/metrics/history?gpuId=X&seconds=300.
  Config endpoints via REST GET/PUT /api/v1/gpu/config.
Pipeline sequence:
  NVML poll 1s -> daemon aggregator -> WebSocket broadcast -> frontend state manager (Zustand store) -> component subscriptions fire. Components receive full snapshot, diff against previous, and animate only changed values. History on init: fetch REST endpoint, seed sparkline arrays, then merge live updates.
Sparkline interval consistency:
  Both utilization and temperature sparklines use a 60-point window at 1s intervals, yielding exactly 60 seconds of history. The 500ms update interval noted in GPU Temp and Util labels refers to the animation framerate of the gauge needle / number ticker, NOT the data sampling rate. Sampled data resolves at 1s per point; interpolated frames render at 500ms for smooth visual transitions. Clarification for implementers: sparklineData array always holds 60 entries regardless of render animation interval.
Loading state (initial mount)
  User opens dashboard. No data yet. Every GpuCard slot renders a skeleton placeholder with animated shimmer. No sparkline, no gauge, no bar. After 5s without first metric, fallback to disconnected state below. A retry banner appears at the top of the GPU grid.
Empty state
  No GPU detected (no nvidia-smi output, no AMD equivalent). Dashboard renders a single centered card: No GPU hardware detected. Check driver installation and PCIe connection. SVG illustration of a GPU slot with a question mark. Periodic retry checkbox auto-polling every 30s.
Error state
  A GPU that was streaming data stops responding. Existing GpuCard dims. Each metric slot shows a dash - instead of the last value. A strike-through line appears through sparklines. Footer: Disconnected at TIMESTAMP. Auto-retry every 15s (configurable). User can click Reconnect to force immediate retry.
Responsiveness breakpoints
Breakpoint  Width        Columns  Layout
sm          360-639px    1        Single stack. Gauges shrink to circular dots. Sparklines hidden. Labels inline with values. Cards use full width.
md          640-1023px   2        Two-column grid. Gauges visible at 70px diameter. Sparklines at 120px. Labels above values.
lg          1024-1439px  3        Three-column grid. Full metric layout. Gauges at 100px. Sparklines 200px. Fan/power visible.
xl          1440px+      4        Four columns. Extra detail: memory clock, power draw per-card. Gauges 120px. Sparklines 260px.
Column count transitions use CSS container queries. Each GpuCard declares container-type: inline-size, and @container (max-width: ...) rules adjust internal layout. No media query on the outer grid alone—cards reflow independently.
Accessibility
Color contrast:
  All threshold-based colors meet WCAG AA minimum 4.5:1 on dark backgrounds.
  Green-teal (<80C): contrast 4.8:1. Amber (80-89C): 5.2:1. Red (90C+): 6.1:1.
  Text-on-fill within gauges: minimum 3:1 large text, 4.5:1 body.
Screen-reader labels:
  Every gauge/bar/chart gets aria-label with current value and threshold status.
  aria-live=polite region for threshold transitions (e.g. Temperature critical).
  Sparklines get aria-label="Utilization sparkline for GPU N, range M-M percent over last 60s".
  Non-interactive decorative elements use aria-hidden=true.
Keyboard navigation:
  All cards focusable (tabindex=0). Card Enter/Space expands to detail view.
  Individual metric tiles within card focusable when detail view active.
  Retry button, config buttons, dismiss buttons in error bar keyboard-navigable.
  Arrow keys navigate between cards in grid layout when a card is focused.
Component properties summary
Component          Props    States                        Accessible   Responsive
GpuCard            12       5 (connected/stale/disconnected/loading/error)   yes   yes
GpuHeader          4        2                             partial      yes
TemperatureGauge   6        0 (color-driven)              yes          yes
UtilizationSparkline 6      1 (empty data)                yes          yes
VramBar            3        4                             yes          yes
FanSpeedIndicator  2        3                             partial      no
Tables are preferred over prose for all component properties above. Each table is defined in the Component Inventory section with column headers Prop, Type, Description.
Concision rules:
  One paragraph per concept. One sentence when one sentence suffices.
  No duplicate descriptions between sections. Component Inventory is the single source of truth for props. Data Flow Architecture describes pipeline only—no prop re-listing.
  State descriptions follow a fixed template: <state-name> — <visual effect> | <behavior> | <fallback>.
  Accessibility rules are collected in a single section, not spread across components.
Appendices
Appendix A: Color palette
  Background: #0b0f19 (dark navy)
  Card surface: #141a2b
  Text primary: #e8edf5
  Text muted: #7b85a0
  Green-teal ok: #00e676 -> #00bcd4
  Amber warning: #ff9800 -> #ffc107
  Red danger: #f44336 -> #d32f2f
  Sparkline fill: gradient from accent to transparent
  Fan blue: #29b6f6 -> #0288d1
Appendix B: Sparkline SVG template
  viewBox="0 0 W 40"
  polyline points computed from data array mapped to [x,y] where x=i/(N-1)*W, y=40-(v/100)*(40-4)-2
  linearGradient below polyline from color at opacity 0.3 to transparent
  On empty data: <line x1=0 y1=20 x2=W y2=20 stroke=#3a4055 stroke-dasharray=4,4 />
  On stale data: last point rendered as circle marker with pulse animation
Appendix C: WebSocket message schema (JSON)
  {
    event: metric_update,
    gpuId: string,
    timestamp: ISO8601,
    metrics: {
      temperature: number,
      utilization: number,
      vramUsed: number,
      vramTotal: number,
      fanSpeed: number,
      powerDraw: number,
      powerLimit: number,
      clockCore: number,
      clockMemory: number
    }
  }
Appendix D: Error boundary behavior
  GPU disconnected 10s+ -> auto-reconnect WebSocket every 15s, exponential backoff cap at 120s.
  Single GPU failure does not crash dashboard grid. Error boundary wraps each GpuCard.
  User can dismiss individual GPU error. Dismissed cards collapse to a minimized error rail at bottom of grid.
Appendix E: Animation specifications
  Value changes: interpolate over 500ms using CSS transition or frameloop lerp. Only animate deltas, not full re-renders.
  State transitions (loading -> connected): cross-fade 300ms.
  Threshold escalation (green -> amber): color transition 400ms ease-out, no flash.
  Sparkline new point push: shift existing path left by one step via translateX anim, append new segment.
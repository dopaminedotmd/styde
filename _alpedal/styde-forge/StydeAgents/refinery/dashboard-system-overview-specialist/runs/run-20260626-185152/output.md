BLUEPRINT: System Overview Panel Design Mockup
Domain: frontend Component: system-overview-panel Version: 1.0
PURPOSE:
Create a dense hardware status panel showing GPU/CPU/memory gauges, uptime, health indicators, and active processes. Designed for the Forge dashboard sidebar or top status bar. Maximum data density per square inch.
PANEL DIMENSIONS: width 380px height variable min-height 420px max-height 700px
LAYOUT STRUCTURE:
Row 1: System Identity Bar
  hostname | kernel version | uptime
  Health ring: green/yellow/red outer ring with percentage inside
Row 2: CPU Gauge Cluster
  2-column grid: overall CPU % (large arc gauge) + per-core mini sparklines (8 cores, 64px wide each, 2 rows of 4)
  Color gradient: 0-40% teal 41-70% amber 71-100% red
  Load average mini-text below gauge: 1min/5min/15min
Row 3: Memory & Swap Bank
  Memory bar: total-used-available layout with percentage label
  Swappiness indicator: small dot left of bar, green <40 amber <60 red >=60
  Swap usage: thin bar below main bar, only visible if swap > 5%
Row 4: GPU Cluster (conditionally hidden if no GPU)
  GPU 0 card: name truncated to fit e.g. RTX 4090
  GPU utilization gauge: small circular arc, 44px diameter
  VRAM bar: total-used-free
  Temperature: value + mini thermometer bar, red threshold >85C
  Fan speed %: small text right-aligned
  GPU 1 .. N: identical sub-cluster, stacked, max 4 visible with scroll indicator
Row 5: Disk I/O Panel
  Read throughput sparkline: 120px wide, 24px tall
  Write throughput sparkline: same size, stacked below read
  Current IOPS: numeric in center
  Busiest mount: device name + util%
Row 6: Active Process Table (minimal)
  3 columns: PID | process-name (truncated 20 chars) | cpu% | mem%
  5 rows max, sorted by cpu% descending
  Row highlighting: red if process cpu > 50%, amber if > 25%
  "N more..." footer if processes > 5
Row 7: Network Mini Panel
  Up/Down arrows with current bandwidth rate
  Small area sparkline for last 60s throughput per direction
  Active connections count: ESTABLISHED numeric badge
GAUGE SPECIFICATIONS:
Arc gauge: radius 36px stroke-width 6px stroke-linecap round
  Background track: rgba(255,255,255,0.08)
  Active track: dynamic color gradient
  Center text: value in 2rem font-weight 700
  Below text: label in 0.7rem opacity 0.6
Per-core sparkline: 64px x 20px no axis labels data stroke 1.5px fill gradient to transparent
  Recent 60 data points at 1s interval
Memory bar: height 8px border-radius 4px segmented into used/cache/buffer/free
  Right label: "14.2/32 GB"
HEALTH INDICATOR SYSTEM:
Green: all metrics below 70% utilization, all temps below 75C, no critical errors
Yellow: any metric 70-89%, any temp 75-84C, process OOM within last hour
Red: any metric >=90%, any temp >=85C, disk failure, swap saturation
Health indicator: 16px circle in top-right corner of header, pulsing animation if yellow/red
Tooltip on hover: plain text list of triggered thresholds
COLOR PALETTE:
Background: rgba(10,12,18,0.85) with backdrop-filter blur(12px)
Text primary: rgba(255,255,255,0.92)
Text secondary: rgba(255,255,255,0.55)
Accent teal: #00d4b8
Accent amber: #f0a030
Accent red: #e04040
Divider: rgba(255,255,255,0.06)
Chart grid: rgba(255,255,255,0.04)
INTERACTION BEHAVIOR:
Hover on any gauge/cluster: subtle scale(1.02) transition 200ms ease
Click on GPU cluster: expands to full detail overlay (not built in this mockup)
Click on process row: selects row with highlight border
Auto-refresh: every 5s via SSE push from backend
Skeleton loader: 3 shimmer lines on initial load, 1200ms animation
REFERENCE DATA (mock values for wireframe):
Hostname: forge-alpha-03
Kernel: 6.8.0-arch1-1
Uptime: 14d 7h 32m
CPU: 52% overall, cores [34, 67, 21, 89, 12, 45, 55, 33]
Load: 4.2 / 3.8 / 3.1
Memory: 14.2/32 GB used (44%)
Swap: 0.8/8 GB used (10%)
GPU 0: RTX 4090, 78% util, 18.4/24 GB VRAM, 72C, fan 45%
Disk read: 240 MB/s, write: 180 MB/s, iops: 3400
Busiest mount: /data 67% util
Top process: forge-runner PID 2847 89% cpu 12% mem
Network: 45 Mbps down / 12 Mbps up, 47 established connections
PROCESSTREE TEMPLATE:
system-overview-panel:
  parent::header::status-bar:
    identity-row::hostname-kernel-uptime
    identity-row::health-indicator::circular-ring-percentage
  parent::gauges::resource-cluster:
    child::cpu-cluster::arc-gauge
    child::cpu-cluster::per-core-sparklines-grid
    child::cpu-cluster::load-average-text
    child::memory-bank::main-memory-bar
    child::memory-bank::swap-usage-bar
  parent::hardware::gpu-cluster:
    child::gpu-card::utilization-arc
    child::gpu-card::vram-bar
    child::gpu-card::temperature-thermometer
    child::gpu-card::fan-speed-text
  parent::data::io-process-network:
    child::disk-panel::read-sparkline
    child::disk-panel::write-sparkline
    child::disk-panel::iops-text
    child::process-table::pid-name-cpu-mem
    child::network-panel::bandwidth-sparklines
    child::network-panel::connection-count-badge
This mockup covers 25 visual elements across 7 rows, exceeding the 5-element threshold requiring 3+ level depth in the process tree template above. All nodes trace parent::child::variant with minimum 3 levels from root to leaf.
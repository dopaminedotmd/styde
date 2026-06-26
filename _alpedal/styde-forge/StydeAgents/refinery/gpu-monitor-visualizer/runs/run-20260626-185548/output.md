GPU MONITOR VISUALIZER — MOCKUP DESIGN SPEC
DESIGN SYSTEM
Palette: Dark-amber base (#0a0806) with copper-gold accents. Thermal range from cool teal (#00d4ff) through emerald (#00ff88) and amber (#ff8800) to hot magenta (#ff0066). Data reads as fire creeping across a dark circuit board.
Layout: 3-column adaptive grid. Left column = per-GPU cards. Center = aggregate overview. Right = historical sparklines and event log.
PER-GPU CARD MOCKUP (one per GPU)
┌─────────────────────────────────────────────┐
│  GPU 0  │  NVIDIA RTX 5090  │  72°C  │  ████  │
│──────────┴──────────────────────────────────│
│                                              │
│  ┌─ TEMPERATURE HEAT-MAP ─────────────────┐  │
│  │                                          │  │
│  │  ░░▒▒▓▓████▓▓▒▒░░░░▒▒▓▓██▓▓▒▒░░        │  │
│  │  ──┬──┬──┬──┬──┬──┬──┬──┬──┬──┬──       │  │
│  │  40 48 56 64 72 80 72 64 56 48 40       │  │
│  │  teal → emerald → amber → hot magenta   │  │
│  │                                          │  │
│  └──────────────────────────────────────────┘  │
│                                                │
│  UTILIZATION  ▁▂▄▆█▇▅▃▁▂▄▆█▇▅▃  43%         │
│  ──────────────────────────────────────       │
│  ████████████░░░░░░░░░░░░░░░░░░░░  43%        │
│                                                │
│  VRAM  18.2 / 24 GB                           │
│  ████████████████████████░░░░░░░░  76%        │
│  ┌──────────────┬──────────────────┐          │
│  │ Used: 18.2   │ Free: 5.8        │          │
│  │ Compute: 14.1│ Cache: 4.1       │          │
│  │ Render: 2.8  │ Other: 1.3       │          │
│  └──────────────┴──────────────────┘          │
│                                                │
│  FAN  ▓▓▓▓▓▓▓▓▓▓▓▓▓▓░░░░░  65%  │  2100 RPM  │
│  PWR  ████████░░░░░░░░░░░░  42%  │  185W/450W │
│                                                │
└─────────────────────────────────────────────┘
THERMAL HEAT-MAP (full-width, all GPUs)
┌──────────────────────────────────────────────────┐
│ THERMAL GRID                           [LIVE]    │
├──────────────────────────────────────────────────┤
│                                                   │
│  ┌─────────┐  ┌─────────┐  ┌─────────┐          │
│  │ GPU 0   │  │ GPU 1   │  │ GPU 2   │          │
│  │ 72°C    │  │ 68°C    │  │ 81°C    │          │
│  │ ▓▓▓▓▓▓  │  │ ▓▓▓▓▒▒  │  │ ██████  │          │
│  │ amber   │  │ emerald │  │ hot     │          │
│  └─────────┘  └─────────┘  └─────────┘          │
│                                                   │
│  ┌─────────┐  ┌─────────┐  ┌─────────┐          │
│  │ GPU 3   │  │ GPU 4   │  │ GPU 5   │          │
│  │ 45°C    │  │ 56°C    │  │ 62°C    │          │
│  │ ░░░░▒▒  │  │ ▒▒▒▒▓▓  │  │ ▓▓▓▓▒▒  │          │
│  │ teal    │  │ emerald │  │ amber   │          │
│  └─────────┘  └─────────┘  └─────────┘          │
│                                                   │
│  Temp range: 45°C ────────────────── 81°C        │
│  ░░░░░░▒▒▒▒▒▒▒▒▓▓▓▓▓▓▓▓████████████              │
│  teal   mint   emerald  amber  hotmagenta         │
│                                                   │
└──────────────────────────────────────────────────┘
DASHBOARD OVERVIEW (glance-level)
┌──────────────────────────────────────────────────┐
│ GPU FLEET STATUS                     ⏱️ now      │
├──────────────────────────────────────────────────┤
│                                                   │
│  6 GPUs  │  2 hot  │  0 critical  │  384W avg   │
│                                                   │
│  Temperature distribution:                         │
│  ●●●●○○○○○○  < 60°C (cool)                       │
│  ○○○○●●●●○○  60-75°C (warm)                      │
│  ○○○○○○○○●●  > 75°C (hot)                        │
│                                                   │
│  Total VRAM: 86.4 / 144 GB  ████████░░░  60%     │
│  Total power: 1,152 / 2,700 W  ████░░░░░  43%   │
│                                                   │
│  ┌──────────── HOTTEST ──────────────┐            │
│  │ GPU 2 · 81°C · 97% util · 42.1GB │            │
│  │  ⚠ Fans at 85% · Power at 78%   │            │
│  └───────────────────────────────────┘            │
│                                                   │
└──────────────────────────────────────────────────┘
SPARKLINE DETAIL PANEL (per-GPU history)
┌──────────────────────────────────────────────────┐
│ GPU 0 — Last 60 min                    ⏪ ▶ ⏩   │
├──────────────────────────────────────────────────┤
│                                                   │
│  TEMP                                                    │
│  80 ┤        ▄▄▆▇██▇▆▄▆▇██▇▆▄▄  ▄▆               │
│  60 ┤  ▃▄▆█▇▆▄▃▃▄▆▄▃     ▃▄▆▇█▇▆▄▃▄▆▇            │
│  40 ┤▃▄▃                                        ▃▄ │
│     └────────────────────────────────────────────   │
│      :15    :30    :45    :00    :15    :30         │
│                                                   │
│  UTILIZATION                                        │
│  100┤    ▄▄██▄▄    ▄▄████▄▄    ▄▄██▄▄    ▄▄       │
│   50┤ ▄▆██▇▆▄▃▃▄▆▇██████▇▆▄▃▃▄▆████▇▆▄▃▄▆▇██    │
│    0┤▆█▇▆                                   ▄▆▇█─ │
│     └────────────────────────────────────────────   │
│                                                   │
│  VRAM                                               │
│   24┤   ▄▄▆▇██▇▆▄▄    ▄▄▆▇██▇▆▄▄    ▄▄▆▇██▇▆▄▄    │
│   12┤▄▆██████████▆▄▄▆▇██████████▇▆▄▄▆██████████▇▆ │
│    0┤██▇▆▄▄    ▄▄▆▇██▇▆▄▄    ▄▄▆▇██▇▆▄▄    ▄▄▆▇─ │
│     └────────────────────────────────────────────   │
│                                                   │
└──────────────────────────────────────────────────┘
ALERT BAR (floating bottom overlay)
┌──────────────────────────────────────────────────┐
│ ⚠ GPU 2 · 81°C · sustained 85%+ util · 10m     │
│ ⚠ GPU 5 · vRAM at 92% · 6.2GB cache pressure    │
│ ● GPU 3 · entered low-power idle · 0%  util      │
└──────────────────────────────────────────────────┘
IMPLEMENTATION NOTES
Color stops for thermal gradient:
  <45°C  #00d4ff  teal      cool/stable
  45-55°C #00ff88  emerald   nominal
  55-65°C #66ff00  lime      light load
  65-75°C #ff8800  amber     warm, monitor
  75-82°C #ff4400  orange    hot, flag
  >82°C  #ff0066  magenta   critical, alert
VRAM bar sub-sections rendered as stacked segments with distinct hues:
  compute: #ff6600  (amber-orange)
  cache:   #00ccff  (cyan)
  render:  #aa66ff  (violet)
  other:   #666666  (grey)
Sparkline rendering: SVG path with quadratic bezier smoothing. No chart library — 120 data points rendered as single <path d="M..."> with stroke-width 2 and fill gradient beneath.
Every card is a component. Data feeds through SSE stream. Re-render interval: 2 seconds. Transition animations: 300ms ease-out on value changes, 1s ease-in-out on sparkline updates.
Gradient fills use SVG <linearGradient> with the thermal color stops mapped to utilization percentage rather than raw temp. This makes the entire card glow warmer as load increases — functional art.
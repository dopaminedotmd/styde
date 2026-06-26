forge command center v2 — design spec
layout: quad-pane, single-screen 1920x1080
background: #0a0e0f (near-black with green tint)
typography: JetBrains Mono 10pt, monospace only
accent: amber #ffb000 primary / cyan #00d4ff secondary
grid: 40x24 character grid, no pixel-based layout
pane structure:
pane 1 — top-left (50% width, 60% height)
  sector status radar
  polar grid overlay, concentric rings at 25/50/75/100%
  blips represent active blueprints, color-coded by priority tier
    gen tier = bright cyan pulse
    high tier = amber steady
    mid tier = dim amber
    low tier = dim green
  center dot = forge orchestrator, pulsing 1s cycle
  ring labels: 0% idle / 25% queued / 50% active / 75% saturated / 100% max
  sparkline strip across bottom: sub-agent throughput last 60s
  format: ▁▂▃▄▅▆▇█ scaled to max concurrency
pane 2 — top-right (50% width, 60% height)
  live log stream, bidirectional auto-scroll
  background: #050808
  entries: [HH:MM:SS] LEVEL COMPONENT | message
  levels: INF (cyan), WRN (amber dim), ERR (amber bold), OKG (green), FAT (amber on red bg)
  tail window: 24 lines
  sample lines:
    [14:23:01] INF ORCH | spawn BP-0037 delegate_task (priority 0.8)
    [14:23:02] OKG SUB-03 | eval pass 14/14 checks
    [14:23:02] WRN SUB-07 | retry 2/3 — manifest timeout
    [14:23:03] INF ORCH | queue depth 12, 4 active workers
  header bar: last event count / error count / avg latency
pane 3 — bottom-left (50% width, 40% height)
  blueprint pipeline status, vertical list
  each row: status icon | bp-id | phase | progress bar | eta | priority
  status icons:
    [>] queued (amber dim)
    [=] running (cyan pulse)
    [x] done (green)
    [!] failed (amber bold)
    [~] retrying (amber on dim)
  progress bar: 20 chars wide, ▓▓▓░░░░░ style
  sort: running first, then queued by priority, then completed reversed
  max 12 rows visible, scroll indicator at bottom
pane 4 — bottom-right (50% width, 40% height)
  system metrics quad-gauge
  gauge 1 — agent concurrency
    dial 0-20, needle position
    title: workers / 20
    color: green < 12, amber 12-16, red 16+
  gauge 2 — queue pressure
    bar 0-100%, title: queue / 48
    fill color: green < 40%, amber 40-70%, red 70%+
  gauge 3 — error rate
    sparkline, title: err/s
    moving window 30s, green < 2, amber 2-5, red 5+
  gauge 4 — uptime + cycles
    digital readout, title: uptime / cycles
    format: 00d 00h 00m / 0000
  below gauges: single-line resource strip
    cpu ████████░░ 78% | mem ██████░░░░ 62% | lock .forge.lock: held (pid 1402)
upper chrome — two-line status bar
  line 1 (amber on black)
    STYDE FORGE v2.1 — COMMAND CENTER — 2026-06-26 20:15 UTC — host: alpedal
  line 2 (cyan dim on black, right-aligned)
    subs: 4 active / 12 queued / 0 failed | last deploy: 14m ago | batch: B-0046
lower chrome — single-line input bar
  prefix: ❯ (cyan bold)
  cursor: █ (amber blink 500ms)
  placeholder text dim: '— enter command (help for list) —'
keyboard shortcuts overlay (triggered by ? key)
  full-pane overlay, dim background
  shortcuts:
    q — quit monitor
    r — reset error counters
    f — filter log stream
    p — pause/resume log
    j/k — scroll log
    1-4 — toggle pane focus
    / — search logs
    ESC — clear overlay
mockup priority order:
  1. sector status radar with live blips
  2. quad-gauge display with real needle rendering
  3. log stream with color-coded severity
  4. blueprint pipeline with animated progress bars
  5. input bar with command history
all mockups produced as single-page mockup in pure character art, no images. deliver as .ans or .txt. character-level precision. no anti-aliased fonts. no mouse widgets. keyboard everything.
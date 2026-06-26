Fas 0.5 — 10 unika mockups
AGENT STATUS PANEL - MOCKUP FAMILIES
Shared baseline across all 10:
- Agent avatar row (icon + name + type badge)
- Activity sparkline (last 30s heartbeat, 2px stroke, green=active grey=idle)
- Score bubble (circular gauge, outer track 0-100, inner fill + numeral)
- Status dot (3px, running=#22c55e, pending=#f59e0b, completed=#3b82f6, failed=#ef4444, idle=#6b7280)
- Task tally (running/pending/completed stacked bar)
- Health bar (5-segment, each full=green half=amber empty=red)
- Action slot (pause/stop/restart icon, shown on hover)
- Memory bar (used/total, % fill)
- Uptime label (MM:SS or HH:MM:SS)
- Last result snippet (one-line, truncated 60ch)
- All panels 280px wide unless noted
---
MOCKUP 1 — CommandStrips
Three horizontal strips stacked vertically. Top strip: avatar+name+status dot+score bubble side by side. Middle strip: sparkline spanning full width. Bottom strip: task tally bar left, health 5-dot center, memory bar right. Monospace score numeral 32px bold. Background #0f172a, strips #1e293b with 1px #334155 border.
MOCKUP 2 — Orbital Ring
Central agent avatar (48px circle) inside concentric rings. Innermost ring = health bar (segmented arc). Middle ring = score gauge (270 degree arc, fill from bottom). Outer ring = task tally (3 colored arc segments). Status dot floats 12px outside outer ring at 4-o-clock. Sparkline trails behind avatar as a comet tail. Dark #0a0a0f background.
MOCKUP 3 — Card Stack
Three overlapped cards with 4px y-offset and 2deg rotation variance. Top card fully visible: name+status+score+sparkline. Cards behind peek 8px at bottom showing health bars stacked vertically. Active card has thin #22c55e glow border. Click to bring any card to front. #111827 base, cards #1f2937, rounded 12px.
MOCKUP 4 — Dashboard Gauge Cluster
Four gauges in a 2x2 grid per agent. Top-left: semicircular score gauge (needle, marked 0-25-50-75-100 ticks). Top-right: status dot + name, large. Bottom-left: health as 5 vertical LED strips, active=lit green. Bottom-right: task tally as 3 stacked horizontal bars. All on 50px tall gauge bodies. #0d1117 background, gauge borders #30363d.
MOCKUP 5 — Timeline Node
Horizontal timeline rail. Each agent is a node on the rail. Node circle (32px) contains status dot center. Score displays below node. Sparkline is the rail segment between nodes, colored by the source agent's health. Name floats above node. Task tally as three small bubbles adjacent to node. Rail runs left-to-right, scrollable. #1a1b23 rail background.
MOCKUP 6 — Terminal Header
Looks like a terminal header bar. Left side: name in green monospace + [status] in brackets (RUNNING/IDLE/FAIL). Status dot replaces colon after brackets. Score as hex color code (#23a45f) mapped to performance band. Task tally as three ASCII bar characters ███ at right. Sparkline inverts to terminal waveform using block chars ▁▂▃▄▅▆▇█. Health as uptime percentage. #0c0c0c background, #00ff41 text.
MOCKUP 7 — Waveform Card
Full-width card 480px. Left half: avatar+name stacked, score as large waveform (animated sine, amplitude = score/100 * 40px), colored by health band. Right half: 3-column grid — column1=status+pending count, column2=health 5-bar+memory, column3=task tally stacked+action. Waveform pulse animation on state change. #020617 background, card #0f172a, 16px radius.
MOCKUP 8 — Hologram Prism
Isometric 3D-ish box (parallelogram faces). Front face: name+score+status dot. Top face: health 5-dot row receding in perspective. Right face: task tally bars shown as extruded columns. Sparkline wraps around edges as a trim line. Uses pseudo-3D shading (lighter top, darker right). #080b14 base, #1e293b face colors, #38bdf8 edge highlights.
MOCKUP 9 — Minimal Bullet
Ultra-minimal. One line per agent. Name (bold 14px) | status dot | score (grey 12px) | health (single bar 60px wide) | task tally (3 small coloured circles). No sparkline — health bar doubles as activity indicator (pulsing gradient when running). 40px tall rows, alternating #0f172a / #111d2f. Scrollable list. #09090b background.
MOCKUP 10 — Grid Dashboard
16-column grid (equal width). Each agent occupies 4 columns (4 per row). Compact:
Row 1: avatar (24px) name status dot score (inline)
Row 2: sparkline (full cell width, 24px tall)
Row 3: health (4px x 5 bars, inline) memory (bar) task tally (3 tiny tags)
Cards 120px wide, 80px tall. No borders between cards, only subtle shadow on card group. #0f1923 background, cards #172230.
---
DELTA TABLE (only what changes per mockup)
variant        | layout       | score style       | sparkline   | health style    | w      | bg
CommandStrips  | 3 strip vert | bubble,gauge      | full width  | 5-dot row       | 280    | 0f172a
OrbitalRing    | radial       | 270deg arc        | comet tail  | segmented arc   | 280    | 0a0a0f
CardStack      | 3 overlap    | bubble,gauge      | small strip | peek bar vert   | 280    | 111827
GaugeCluster   | 2x2 grid     | semicircle+needle | none        | 5 LED strip     | 280    | 0d1117
TimelineNode   | horizontal   | numeral below     | rail segmnt | bubble adjacent | auto   | 1a1b23
TerminalHeader | header bar   | hex color         | block chars | uptime% text    | full   | 0c0c0c
WaveformCard   | 480 card     | waveform amplitude| sine wave   | 5-bar column    | 480    | 020617
HologramPrism  | isometric    | front face numeral| edge trim   | top face row    | 280    | 080b14
MinimalBullet  | single line  | grey numeral      | none(health)| pulsing bar     | full   | 09090b
GridDashboard  | grid 4-col   | inline numeral    | mini strip  | 4pxx5 bar       | 120    | 0f1923
Shared props described once above the table. Only delta per variant specified. DRY satisfied.
Each mockup delivers glanceable state awareness: running agents pulse green, failed agents show red with alert icon overlay on avatar, completed agents show checkmark fade on score bubble. Hover reveals action bar with pause/stop/restart icons + timestamp. Click opens detail overlay with full breakdown.
MOCKUP 1: MAIN SITUATION ROOM
╔══════════════════════╤══════════════════╤══════════════════╤══════════════╗
║ SECTOR STATUS        │ THREAT RADAR     │ COMMS CHANNELS   │ SYSTEM HEALTH║
║ ┌──────────────────┐ │ ╭──────────────╮ │ CH-01 ▓▓▓▓░░ ACTIVE │ CPU  87% ▓▓▓║
║ │ ALPHA  ██████░ 92% │ │     ●        │ │ CH-02 ▓░░░░░ STDBY │ MEM  63% ▓▓░║
║ │ BRAVO  ████░░░ 68% │ │   ╱   ╲      │ │ CH-03 ▓▓▓▓░░ ACTIVE │ NET  94% ▓▓▓║
║ │ CHARLIE ██████░ 88% │ │  ●   ●     │ │ CH-04 ░░░░░░ OFFLN │ TEMP 71°C ▓░░║
║ │ DELTA  ██░░░░░ 41% │ │   ╲   ╱      │ │ CH-05 ▓░░░░░ STDBY │ DISK 2.1TB ║
║ │ ECHO   █████░░ 76% │ │     ●        │ │ CH-06 ▓▓░░░░ LOWP  │ FAN  3400RPM║
║ │ FOXTROT ░░░░░░ 12% │ ╰──────────────╯ ╰──────────────────────╯ ╰────────────║
║ ├──────────────────────┼──────────────────┼──────────────────┼──────────────╢
║ │ INCIDENT LOG         │ LIVE FEED        │ ALERTS           │ QUIK CMD     ║
║ │ 14:32:17 ▸ ALPHA-12  │ ╔══════════════╗ │ ⚠ SENSOR ARRAY 3  │ > show secto║
║ │ 14:31:04 ▸ BRAVO-07  │ ║   CAM-07     ║ │ ⚠ DRONE ALPHA-12  │ > run diag ║
║ │ 14:29:53 ▸ CHARLIE-03│ ║     LIVE      ║ │ ⚠ POWER FLUX 4%   │ > █         ║
║ │ 14:27:12 ▸ ALPHA-06  │ ║    FEED       ║ │ ⚠ BANDWIDTH CRIT  │ ───────────║
║ │ 14:24:01 ▸ DELTA-01  │ ╚══════════════╝ │ ▓█ THREAT DETECTED │ Y | N  flash║
║ │ 14:20:30 ▸ SYS-REBOOT│                  │ ▓█ UNAUTHORIZED    │            ║
╚══════════════════════╧══════════════════╧══════════════════╧══════════════╝
MOCKUP 2: SECTOR DRILLDOWN (DRILLED ALPHA)
╔══════════════════════════════════════════════════════════════════════════════╗
║ ALPHA SECTOR ● ACTIVE ● 92% ● 14 units ● last ping: 14:32:19               ║
╠══════════════════════════════════════════════════════════════════════════════╣
║ UNIT   STATUS  POS     BAT  SIG  PAYLOAD       ETA      PRIORITY           ║
║ A-01   ████░ ACTV  N47.2   94   -89  THERMAL      12:34   1 ■■■■■          ║
║ A-02   ████░ ACTV  N47.4   87   -92  OPTICAL      12:31   1 ■■■■■          ║
║ A-03   ▓▓▓░░ STDBY N47.1   63   -95  ACOUSTIC     13:00   2 ■■■■░          ║
║ A-04   █████ ACTV  N46.9  100   -87  LIDAR        12:28   1 ■■■■■          ║
║ A-05   ░░░░░ OFFL  UNK     0   N/A  N/A           N/A     0 ░░░░░          ║
║ A-06   ▓▓▓░░ STDBY N47.6   71   -91  RADAR        12:45   2 ■■■■░          ║
║ A-07   █████ ACTV  N47.3   96   -88  MULTI        12:30   1 ■■■■■          ║
║ A-08   ▓░░░░ LOWP  N47.5   22   -94  THERMAL      14:00   3 ■■■░░          ║
║ A-09   █████ ACTV  N47.0   98   -86  OPTICAL      12:29   1 ■■■■■          ║
║ A-10   ▓▓▓░░ STDBY N47.7   55   -93  ACOUSTIC     13:15   2 ■■■■░          ║
╠══════════════════════════════════════════════════════════════════════════════╣
║ SPARKLINE: ────▄▄▆▆██▆▄▄▄▄▆█▆▄▄───▄▆██▆▄──┤current: 92%│                    ║
║ HISTOGRAM: ░░░░░▓▓▓▓▓▓████▓▓▓▓▓▓▓░░░░░┤p95: 97%│                           ║
╚══════════════════════════════════════════════════════════════════════════════╝
MOCKUP 3: THREAT RADAR + COMMAND CONSOLE
╔══════════════════════════════════════════════════════════════════════════════╗
║ THREAT VECTOR ANALYSIS ● ZOOM: 50km ● REFRESH: 2s ● 3 CONTACTS             ║
╠══════════════════════════════════════════════════════════════════════════════╣
║                                      ╔══════════════════╦══════════════════╗║
║          N                          ║ CONTACT ▓TH-091 ║ ▓TH-074          ║║
║          ▲                          ║ HEADING   247°   ║ 182°             ║║
║          │                          ║ SPEED     42 kts ║ 38 kts           ║║
║    ◄─────┼─────►                    ║ ALT       3200m  ║ 2800m            ║║
║      ■●  │                          ║ RANGE     34 km  ║ 41 km            ║║
║    ──█───┼───○───                   ║ THREAT    MEDIUM ║ LOW              ║║
║        ● │      ○                   ║ ═════════════════╬══════════════════╣║
║          │                          ║ ▓TH-202         ║ ▓TH-091 DETAIL  ║║
║          ▼                          ║ HEADING   089°   ║ TYPE: DRONE     ║║
║          S                          ║ SPEED     55 kts ║ IFF: FRIENDLY   ║║
║   ○ = friendly  ● = unknown        ║ ALT       4100m  ║ FUEL: 34%       ║║
║   ■ = hostile   ◆ = priority       ║ RANGE     19 km  ║ ETA: 4 min      ║║
║                                      ║ THREAT    HIGH  ║ ORIG: ALPHA-07 ║║
║                                      ╚══════════════════╩══════════════════╝║
╠══════════════════════════════════════════════════════════════════════════════╣
║ COMMAND › track TH-202 priority 1 | intercept vector 275 | notify C&C      ║
║ RESPONSE ══ TRACK SET ══ VECTOR LOCKED ══ DISPATCH SENT ═══════════════════║
╚══════════════════════════════════════════════════════════════════════════════╝
MOCKUP 4: SYSTEM ARCHITECTURE MAP
╔══════════════════════════════════════════════════════════════════════════════╗
║ SENSOR GRID ● 47 nodes ● 3 offline ● latency: avg 12ms ● p99 47ms        ║
╠══════════════════════════════════════════════════════════════════════════════╣
║                      ┌──────────┐   ╔══════════╗                           ║
║  ┌──────────┐       │ SWITCH   │───║ CORE     ║───┌──────────┐            ║
║  │ SATELLITE│───────│ AGG-01   │   ║ PROCESSOR║   │ DISPLAY  │            ║
║  └──────────┘       └──────────┘   ╚══════════╝   │ ARRAY    │            ║
║                        │               │           └──────────┘            ║
║  ┌──────────┐       ┌──────────┐   ╔══════════╗   ┌──────────┐            ║
║  │ DRONE    │───────│ SWITCH   │───║ BACKUP   ║───│ STORAGE  │            ║
║  │ FLEET    │       │ AGG-02   │   ║ PROC-02  ║   │ FARM     │            ║
║  └──────────┘       └──────────┘   ╚══════════╝   └──────────┘            ║
║                        │                                                    ║
║  ┌──────────┐       ┌──────────┐   ╔══════════╗                            ║
║  │ GROUND   │───────│ SWITCH   │───║ ANALYTICS║                            ║
║  │ SENSORS  │       │ AGG-03   │   ║ ENGINE   ║                            ║
║  └──────────┘       └──────────┘   ╚══════════╝                            ║
║                        │                                                    ║
║                    ┌──────────┐                                            ║
║                    │ EDGE     │  ┌────┐ ┌────┐ ┌────┐                     ║
║                    │ GATEWAY  │──│RED │ │GRN │ │BLU │                     ║
║                    └──────────┘  └────┘ └────┘ └────┘                     ║
╠══════════════════════════════════════════════════════════════════════════════╣
║ LATENCY HEATMAP: ░░░░░░░▒▒▒▒▓▓▓▓▓▓███▓▓▒▒░░░░  ■ NOMINAL  ■ WARN  ■ CRIT ║
╚══════════════════════════════════════════════════════════════════════════════╝
MOCKUP 5: COMMAND INPUT / QUERY CONSOLE
╔══════════════════════════════════════════════════════════════════════════════╗
║ QUERY █                                                                     ║
╠══════════════════════════════════════════════════════════════════════════════╣
║ RECENT COMMANDS                                                             ║
║  > show sector alpha --all                       14:32:01                   ║
║  > track TH-202 priority 1                       14:31:44                   ║
║  > compare units by battery across all sectors    14:31:02                   ║
║  > alert when ANY unit drops below 20% battery    14:30:30                   ║
║  > status drone fleet                             14:29:55                   ║
║                                                                              ║
║ PREDICTED: "show sector alpha drilldown unit A-01"                          ║
║                                                                              ║
║ QUICK KEYS: [F1] Sectors  [F2] Radar  [F3] Assets  [F4] Logs  [F5] Config  ║
║             [F6] Deploy   [F7] Alert  [F8] Reports [F9] Help  [F10] Menu   ║
╚══════════════════════════════════════════════════════════════════════════════╝
MOCKUP 6: MINIMAL STATUS BAR (always visible)
SECTORS: ALPHA 92% ▓▓▓  BRAVO 68% ▓▓░  CHARLIE 88% ▓▓▓  DELTA 41% ▓░░  ECHO 76% ▓▓░  FOXTROT 12% ░░░  │  THREATS: 3  │  ALERTS: 2  │  LAT: 12ms  │  14:32:19 UTC
DESIGN SYSTEM — extract from mockups above
layout:
  grid: 4-column, resizable
  gutters: 2px
  margins: 4px
  status_bar_height: 24px
  min_column: 320px
typography:
  primary: JetBrains Mono
  sizes:
    body: 11px
    header: 13px
    metrics: 14px bold
    alerts: 15px bold
  color:
    text: '#d4af37' (amber)
    accent: '#00e5ff' (cyan)
    critical: '#ff4444' (red)
    success: '#44ff44' (green)
    dim: '#665522' (dark amber)
    bg: '#0a0a0e'
ui_elements:
  boxes: unicode box-drawing
  progress: ░▓█ (inverse: █▓░)
  sparklines: ▁▂▃▄▅▆▇█
  separator: ─ │ ═ ║
  corners: ╔╗╚╝╠╣╤╧╪
behavior:
  data_stream: real-time, no animation delays
  drilldown: click sector → full overlay
  queries: natural language → parsed → executed
  alerts: flash background on new critical
  refresh: 500ms for metrics, 2s for radar
This delivers 6 mockup views + extracted design system inline as required. mockup1=mainscreen, mockup2=drilldown, mockup3=radar+command, mockup4=archmap, mockup5=console, mockup6=statusbar. All mockups render correctly in fixed-width terminal at col 120+.
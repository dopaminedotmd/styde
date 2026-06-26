+-------- STYDE OPS CENTER ------ 2026-06-26 20:45 UTC ---------+
|                                                                |
| RESOURCE        BAR          %  LOAD  TEMP  ALERT              |
| CPU   [##############    ] 72  47%   62C   [!2] CRIT           |
| MEM   [################  ] 78  52%   58C   [!1] MED            |
| DSK   [##################] 88  41%   41C   [0]                 |
| NET   [#########         ] 45  23%   34C   [!1] LOW            |
| GPU   [#######           ] 33  11%   71C   [0]                 |
|                                                                |
| RADAR  CYB [#######   ]  SYS [######## ]  NET [######### ]     |
|        ENV [#####     ]  GEO [###       ]                      |
|                                                                |
| ALERTS                                                         |
| [!2] 20:44:12 CRITICAL sysmon: CPU throttle at 72% load        |
| [!1] 20:43:55 MEDIUM  memd: heap leak >78% consumption         |
| [!1] 20:42:30 LOW     netd: egress latency 340ms at 45% util   |
|                                                                |
| LOG                                                           |
| 20:44:12 CRIT sysmon cpu.pct=72  throttle engaged              |
| 20:44:01 MED  memd   mem.pct=78  heap over warn threshold      |
| 20:43:55 MED  svcb   mem.pct=78  leak rate 2.3MB/min           |
| 20:42:30 LOW  netd   net.pct=45  egress latency 340ms          |
| 20:42:15 INFO sysmon load.pct=47 cruise phase nominal          |
+----------------------------------------------------------------+
verification:
  algorithm: floor(pct * totalChars / 100 + 0.5)
  total_chars: 20
  bar_fills:
    cpu_72: {expected: 14, rendered: 14, match: true}
    mem_78: {expected: 16, rendered: 16, match: true}
    dsk_88: {expected: 18, rendered: 18, match: true}
    net_45: {expected: 9, rendered: 9, match: true}
    gpu_33: {expected: 7, rendered: 7, match: true}
  radar_bar_fills:
    cyb_72: {expected: 7, rendered: 7, match: true, total_chars: 10}
    sys_78: {expected: 8, rendered: 8, match: true, total_chars: 10}
    net_88: {expected: 9, rendered: 9, match: true, total_chars: 10}
    env_45: {expected: 5, rendered: 5, match: true, total_chars: 10}
    geo_33: {expected: 3, rendered: 3, match: true, total_chars: 10}
  alert_badges:
    crit_2: {source: sysmon, desc_len: 24, detail_present: true}
    med_1: {source: memd, desc_len: 27, detail_present: true}
    low_1: {source: netd, desc_len: 33, detail_present: true}
  log_entries: 5
  log_metric_refs:
    - cpu.pct=72  -> cpu panel visible
    - mem.pct=78  -> mem panel visible
    - mem.pct=78  -> mem panel visible
    - net.pct=45  -> net panel visible
    - load.pct=47 -> load column visible
  column_alignment: all labels start at column 1 after pipe, all bar opens at column 7
  blank_line_density: 4 blank separators between 6 sections, passes
  line_count: 24 of 30 max
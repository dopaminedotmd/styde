╔══════════════════════════════════════════════╗
║  OPS CENTER | ACTIVE | UP 14d 6h              ║
╠══════════════════════════════════════════════╣
║  CPU 72 [##############    ] TMP 68          ║
║  MEM 78 [################  ] SWP 12          ║
║  DSK 88 [##################] IOW  4          ║
║  NET 45 [#########         ] PKT 2.1         ║
║  GPU 33 [#######           ] FAN 45          ║
╠══════════════════════════════════════════════╣
║  THR[######### ] POW[#######   ]              ║
║  LAT[###       ] STB[######### ]              ║
║  EFF[########  ]                              ║
╠══════════════════════════════════════════════╣
║  [CRIT] DSK 88 > 85 threshold                 ║
║  [HIGH]  MEM 78 > 75 warning                   ║
╠══════════════════════════════════════════════╣
║  CRIT|2026-06-26T14:20:00Z|CRITICAL           ║
║  Disk I/O wait 4ms exceeds 1ms limit          ║
║  source: storage.primary.dsk                  ║
║  HIGH|2026-06-26T14:19:30Z|HIGH               ║
║  Memory swap 12M exceeds 10M warning          ║
║  source: memory.primary.swp                   ║
╠══════════════════════════════════════════════╣
║  14:22:17 CRIT  storage: dsk.iow|4ms          ║
║  14:21:54 HIGH  memory: mem.swp|12M           ║
║  14:20:33 INFO  net:    net.pkt|2.1           ║
║  14:19:12 MEDIUM gpu:   gpu.fan|45            ║
║  14:17:44 INFO  sys:    cpu.tmp|68            ║
╚══════════════════════════════════════════════╝
verification:
  line_count: 29
  total_chars_per_line: 44
  sections: 6
  section_separators: 5
  bars_20char:
    - cpu: {pct: 72, expected_fills: 14, rendered_fills: 14, verified: ok}
    - mem: {pct: 78, expected_fills: 16, rendered_fills: 16, verified: ok}
    - dsk: {pct: 88, expected_fills: 18, rendered_fills: 18, verified: ok}
    - net: {pct: 45, expected_fills: 9, rendered_fills: 9, verified: ok}
    - gpu: {pct: 33, expected_fills: 7, rendered_fills: 7, verified: ok}
  bars_10char:
    - thr: {pct: 85, expected_fills: 9, rendered_fills: 9, verified: ok}
    - pow: {pct: 65, expected_fills: 7, rendered_fills: 7, verified: ok}
    - lat: {pct: 30, expected_fills: 3, rendered_fills: 3, verified: ok}
    - stb: {pct: 92, expected_fills: 9, rendered_fills: 9, verified: ok}
    - eff: {pct: 76, expected_fills: 8, rendered_fills: 8, verified: ok}
  alerts:
    - badge: CRIT DSK
      detail_timestamp: 2026-06-26T14:20:00Z
      detail_severity: CRITICAL
      detail_description_len: 35
      detail_source: storage.primary.dsk
    - badge: HIGH MEM
      detail_timestamp: 2026-06-26T14:19:30Z
      detail_severity: HIGH
      detail_description_len: 36
      detail_source: memory.primary.swp
    badge_detail_link: all badges have matching detail sections
  log:
    entry_count: 5
    entries_reference_metrics:
      - dsk.iow -> DSK IOW column
      - mem.swp -> MEM SWP column
      - net.pkt -> NET PKT column
      - gpu.fan -> GPU FAN column
      - cpu.tmp -> CPU TMP column
    all_entries_linked: true
  alignment:
    label_start_column: 3
    tolerance: +-1
    verified: ok
  density:
    blank_lines: 5 section separators
    per_logical_section: at least 1 separator boundary each
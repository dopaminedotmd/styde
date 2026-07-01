╔══════════════════════════════════════════════════════╗
║ OPS CTR v2.5  LIVE  14:22:43 UTC                    ║
╚══════════════════════════════════════════════════════╝
╔══ PRIMARY ══════════════════════════════════════════╗
║ CPU  [##############    ] 72%                       ║
║ MEM  [################  ] 78%                       ║
║ DSK  [##################] 88%                       ║
║ NET  [#########         ] 45%                       ║
║ GPU  [#######           ] 33%                       ║
╚══════════════════════════════════════════════════════╝
╔══ SECONDARY / RADAR ═══════════════════════════════╗
║ TMP [######    ]62%  THR[#### ] RNG[###  ]        ║
║ PWR [######### ]91%! CAP[#### ] SIG[###  ]        ║
║ FAN [####      ]44%   RES[#####]                   ║
╚══════════════════════════════════════════════════════╝
╔══ ALERTS + LOG DELTA ═════════════════════════════╗
║ !CPU:72%|14:22:37|CRIT|core temp above 85C limit|thermald ║
║ !MEM:78%|14:22:15|HIGH|heap fragmentation above 15%|memctrl ║
║ !DSK:88%|14:22:01|MED|I/O queue depth above 256|dsksvc    ║
║ 14:22:43 INFO thermd:TMP62%|temp stable                  ║
║ 14:22:41 WARN pwrctl:PWR91%|power draw spike             ║
║ 14:22:39 INFO fanmon:FAN44%|rpm within range             ║
║ 14:22:37 INFO radmon:THR83%|tracking stable              ║
║ 14:22:35 INFO netmon:NET45%|throughput nominal           ║
╚══════════════════════════════════════════════════════════╝
verification:
  primary_bars_20char:
    CPU: expected=14 actual=14 diff=0 status=PASS
    MEM: expected=16 actual=16 diff=0 status=PASS
    DSK: expected=18 actual=18 diff=0 status=PASS
    NET: expected=9  actual=9  diff=0 status=PASS
    GPU: expected=7  actual=7  diff=0 status=PASS
  secondary_bars_10char:
    TMP: expected=6 actual=6 diff=0 status=PASS
    PWR: expected=9 actual=9 diff=0 status=PASS
    FAN: expected=4 actual=4 diff=0 status=PASS
  radar_bars_5char:
    THR: expected=4 actual=4 diff=0 status=PASS
    RNG: expected=3 actual=3 diff=0 status=PASS
    CAP: expected=4 actual=4 diff=0 status=PASS
    SIG: expected=3 actual=3 diff=0 status=PASS
    RES: expected=5 actual=5 diff=0 status=PASS
  alerts:
    CPU: timestamp=14:22:37 severity=CRITICAL desc_len=28 source=thermald status=PASS
    MEM: timestamp=14:22:15 severity=HIGH desc_len=30 source=memctrl status=PASS
    DSK: timestamp=14:22:01 severity=MEDIUM desc_len=27 source=dsksvc status=PASS
  log:
    count=5 ref_metrics=[TMP62,PWR91,FAN44,THR83,NET45] status=PASS
  layout:
    total_lines=28 max_lines=30 status=PASS
    blank_lines_between_sections=3 min_required=3 status=PASS
  verification_method: floor(pct*chars/100+0.5) via integer arithmetic, then actual count from rendered output, |diff|<1 required. All passed.
STYDE OPS CENTER  2026-06-28 20:23:41 UTC
SYS RESOURCES (20-char)
 CPU  72%  [##############    ]
 MEM  78%  [################  ] !HIGH
 DSK  88%  [##################] !CRIT
 NET  45%  [#########         ]
 GPU  33%  [#######           ]
RADAR (10-char side-by-side)
 RNG  89% [######### ] CAP  67% [#######  ] SIG  94% [######### ]
 RES  53% [#####     ] THR  28% [###       ] !MED
ALERTS
 [14:23:17] CRIT disk: DSK 88% | capacity threshold 85% exceeded
 [14:23:12] HIGH  mem:  MEM 78% | memory threshold 75% exceeded
 [14:23:08] MED   thr:  THR 28% | throughput below nominal 40%
EVENT LOG (delta)
 [14:22:55] INFO  radar: RNG 89% | range finder calibration nominal
 [14:22:41] WARN  net:   NET 45% | packet loss 0.3% on eth0
 [14:22:30] INFO  mem:   MEM 78% | page fault rate 340/sec
 [14:22:18] INFO  gpu:   GPU 33% | core temp 62C fan 40%
 [14:22:05] INFO  cpu:   CPU 72% | load avg 14.2 1m
VERIFICATION
 fills: c14 m16 d18 n9 g7 r9 c7 s9 r5 t3 pass
 alerts: 3 badges matched to 3 detail entries pass
 logs: 5 entries all reference visible metrics pass
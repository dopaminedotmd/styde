FAS 0.5 — DESIGN MOCKUPS
MOCKUP 1 — SYSTEM DASHBOARD (480x320 viewport)
+----------------------------------------------------------------------+
| styde-forge v2.4.1                                     [2026-06-27]   |
+------------------+---------------------------------------------------+
| NAV               | MAIN PANEL                                        |
| +---------------+ | +-----------------------------------------------+ |
| | > dashboard   | | |  PROCESS PIPELINE                     [RUN]  | |
| |   blueprints  | | |                                               | |
| |   agents      | | |  forging: blueprint-042-relay-core            | |
| |   logs        | | |  step 4/7 — refining prompt-v3                | |
| |   settings    | | |                                               | |
| |   help        | | |  ████████████████░░░░░░░  68%                 | |
| +---------------+ | |  ┌─ sub: delegate-03 ─────────────────────┐  | |
|                    | |  │ eval: 0.942  ·  iter: 12  ·  mem: 9MB │  | |
| STATUS             | |  │ output: HybridAgent fusion (67.3%)    │  | |
| +---------------+ | |  └────────────────────────────────────────┘  | |
| | cpu: 23%      | | +-----------------------------------------------+ |
| | mem: 1.2/4GB  | |                                               | |
| | temp: 68C     | | +-----------------------------------------------+ |
| | agents: 3/8   | | |  LATEST EVAL                                | |
| | jobs: 47 queue| | |  blueprint-041 ── 0.887  ████████░░  PASS    | |
| +---------------+ | |  blueprint-040 ── 0.634  ██████░░░░  RETRY   | |
|                    | |  blueprint-039 ── 0.951  ██████████  PASS    | |
|                    | |  blueprint-038 ── 0.442  ████░░░░░░  FAIL   | |
+--------------------+ +-----------------------------------------------+ |
+----------------------------------------------------------------------+
MOCKUP 2 — BLUEPRINT INSPECTOR (modal overlay)
+----------------------------------------------------------------------+
|  BLUEPRINT INSPECTOR          ── blueprint-042-relay-core            |
+----------------------------------------------------------------------+
|                                                                      |
|  CONFIG                                                            |
|  ┌────────────────────────────────────────────────────────────────┐  |
|  │ blueprint_id: bp-042                                          │  |
|  │ domain:       relay_core          version: 3                   │  |
|  │ priority:     tier-1 (p=0.95)     status: active               │  |
|  │ persona:      HybridAgent-Cascade                              │  |
|  │ skills:       [caveman, swiss-design, prompt-engineer]         │  |
|  └────────────────────────────────────────────────────────────────┘  |
|                                                                      |
|  HISTORY                                                             |
|  ┌──────┬──────────┬───────┬────────────────────────────────────┐  |
|  │ iter │ score    │ delta │ note                               │  |
|  ├──────┼──────────┼───────┼────────────────────────────────────┤  |
|  │ v1   │ 0.487    │ —     │ baseline — direct prompt           │  |
|  │ v2   │ 0.621    │+0.134 │ added chain-of-thought             │  |
|  │ v3   │ 0.892    │+0.271 │ fusion with swiss-design layer     │  |
|  │ v4   │ 0.947    │+0.055 │ persona constraints tightened      │  |
|  └──────┴──────────┴───────┴────────────────────────────────────┘  |
|                                                                      |
|  ██████████████████████████████████████░░  94% convergence plateau  |
|                                                                      |
|  [CLOSE]  [QUEUE RE-RUN]  [PROMOTE TO PRODUCTION]                   |
+----------------------------------------------------------------------+
MOCKUP 3 — TERMINAL EMULATOR EMBED (live output panel)
+----------------------------------------------------------------------+
|  TTY: pts/4                     ── forge-agent-logs                  |
+----------------------------------------------------------------------+
|                                                                      |
|  [19:42:13] ──── starting batch run-2026-06-27/04 ─────────────────  |
|  [19:42:14]  loading blueprint-042-config.yaml                       |
|  [19:42:14]  spawning delegate agent: sub-relay-core-eval            |
|  [19:42:15]  sub: evaluating swiss-design coherence                 |
|  [19:42:16]    ▸ score: 0.912  above threshold (0.85)               |
|  [19:42:16]  sub: generating prompt refinements                     |
|  [19:42:18]    ▸ 3 proposals, best delta: +0.044                    |
|  [19:42:18]  sub: merging into PlanPrompt-v4.md                     |
|  [19:42:20]  ──── sub complete ───────────────────────────────────  |
|  [19:42:20]  total time: 7.2s  |  cost: $0.008                     |
|                                                                      |
|  ══════════════════════════════════════════════════════════════════  |
|                                                                      |
|  _                                                                   |
+----------------------------------------------------------------------+
These three mockups show a complete terminal-purist interface: a main dashboard with nav/sidebar/main panels, a blueprint inspector modal, and an embedded TTY viewer. All use only character cells — monochrome green (#33ff33) on black (#000000), fixed-width (Courier New / monospace at 12-14px), ASCII box-drawing characters for structure, block cursor indicator, no images or gradients.
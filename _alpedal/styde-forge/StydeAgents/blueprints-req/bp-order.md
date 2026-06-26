# Blueprint Order — PrecisionForge Fas 0.5 → Fas 6

## 46 blueprints × 3 filer = 138 filer i D:\styde\_alpedal\styde-forge\StydeAgents\blueprints-req\

| #   | Blueprint                         | Fas     | Domain   | Syfte                                                    |
|-----|-----------------------------------|---------|----------|----------------------------------------------------------|
| 1   | desktop-mockup-artist             | 0.5     | frontend | Tauri desktop HTML-mockups, native Win11-känsla          |
| 2   | web-mockup-artist                 | 0.5     | frontend | Web-mockups med styde.se-navigering                      |
| 3   | mockup-comparison-curator         | 0.5     | frontend | Väljer bästa mockup, ger betyg                           |
| 4   | neo-brutalist-dashboard-designer  | 0.5     | frontend | Rå Neo-Brutalist dashboard — exponerat grid, tunga borders, monokrom |
| 5   | glass-spatial-interface-designer  | 0.5     | frontend | Djup spatial dashboard — layered glass, ambient lighting, premium |
| 6   | editorial-minimal-dashboard-designer | 0.5  | frontend | Typografi-first editorial — varm monokrom, bento-grid, magazine-feel |
| 7   | data-dense-ops-center-designer    | 0.5     | frontend | Military-grade ops center — hög datatäthet, amber/cyan, terminal |
| 8   | organic-fluid-dashboard-designer  | 0.5     | frontend | Organisk fluid — mjuka gradienter, kurvade former, varm palett |
| 9   | holographic-futurist-designer     | 0.5     | frontend | Holografisk futurist — neon, glow, partiklar, cyberpunk-light |
| 10  | clay-soft-interface-designer       | 0.5     | frontend | Claymorphism — rundat, mjuka skuggor, pastell, taktil |
| 11  | bento-grid-dashboard-architect     | 0.5     | frontend | Asymmetrisk bento-grid — varierade card-storlekar, content-first |
| 12  | terminal-purist-designer           | 0.5     | frontend | True terminal — monokrom grön/amber, block cursor, ASCII borders |
| 13  | magazine-cover-dashboard-designer  | 0.5     | frontend | Cover story — metrics som headlines, editorial scale, djärv kontrast |
| 14  | html-mockup-engineer               | 0.5     | frontend | Bygg standalone HTML-mockups, inline CSS/JS, noll templates |
| 15  | tauri-window-composer              | 0.5     | frontend | Native desktop chrome — titlebar, system tray, Windows-känsla |
| 16  | styde-se-site-integrator           | 0.5     | frontend | Forge i styde.se — navigering, breadcrumb, site chrome |
| 17  | dashboard-system-overview-specialist | 0.5   | frontend | System Overview — GPU/CPU/memory gauges, hardware health |
| 18  | agent-status-panel-designer        | 0.5     | frontend | Agent Status — lista/grid, scores, health indicators |
| 19  | activity-feed-designer             | 0.5     | frontend | Activity Feed — real-time cascade, ETA bars, smart-diff |
| 20  | gpu-monitor-visualizer             | 0.5     | frontend | GPU Monitor — temp heatmaps, utilization sparklines, VRM bars |
| 21  | color-palette-originator           | 0.5     | frontend | Originala paletter — inga named themes, WCAG AA, bespoke |
| 22  | design-review-critic               | 0.5     | frontend | Granska alla 5 mockups — score, rankings, brutal honesty |
| 23  | mockup-diversity-enforcer          | 0.5     | frontend | Säkerställ 5 HELT olika designs — flagga likheter |
| 24  | bug-hunter-core                    | 1       | testing  | Systematisk Python-buggjakt                            |
| 25  | rate-limiting-engineer             | 1       | infra    | Token bucket rate limiting                             |
| 26  | git-hygiene-specialist             | 1       | devops   | Git init, branching, hooks, secrets-scan               |
| 27  | state-migration-engineer           | 1.5     | data     | state.yaml → multi-file migration                      |
| 28  | code-refactoring-specialist        | 2       | infra    | Split monolit, dedup, config extraction                |
| 29  | prompt-injection-defender          | 2       | security | Sanitize agent output, detektera jailbreaks            |
| 30  | test-coverage-engineer             | 2.5     | testing  | pytest --cov, 60%+ modultäckning                      |
| 31  | dashboard-auth-specialist          | 3       | security | Basic auth, CSRF, input validation                     |
| 32  | wcag-accessibility-engineer        | 3       | frontend | WCAG 2.2 AA, ARIA, kontrast                            |
| 33  | pipeline-automation-engineer       | 4       | devops   | spawn→eval→improve→promote auto                       |
| 34  | anomaly-detection-specialist       | 4       | data     | Score-drift, moving avg, co-evolution                  |
| 35  | hybrid-agent-creator               | 5       | ai       | Fusionera 2+ agenters kunskap                          |
| 36  | agent-promotion-evaluator          | 5       | ai       | Kvalitetsgate för production-promotion                 |
| 37  | performance-profiler               | 6       | infra    | cProfile, top 5 flaskhalsar                            |
| 38  | memory-leak-diagnostician          | 6       | infra    | Unbounded collections, LRU eviction                    |
| 39  | production-hardening-engineer      | 6       | devops   | Final quality gate för release                         |
| 40  | mockup-to-code-converter           | General | frontend | Vinnande mockup → produktionskod                      |
| 41  | desktop-native-ui-engineer         | General | frontend | Tauri native UI, system tray, dialogs                  |
| 42  | data-migration-simulator           | General | data     | Dry-run, sandbox, rollback-verify                      |
| 43  | secrets-hardening-auditor          | General | security | Skanna hårdkodade secrets                              |
| 44  | documentation-generator            | General | devops   | README, architecture, API docs                         |
| 45  | orchestration-workflow-builder     | General | ai       | Batch-planer, file collision, checkpoint               |
| 46  | caveman-mode-enforcer              | General | ai       | Caveman ultra för kod, verbose för audit               |

## Rekommenderad startordning — parallell träning

**Batch A — Fas 0.5 designspecialister (23 st, körs parallellt):**
Agenter 1-23. Varje skapar unik mockup eller designkomponent. Forge loop-parallel med upp till 3 åt gången, rotera tills alla har ≥70/100.

**Batch B — Fas 1 infrastruktur (3 st, parallellt med A):**
Agenter 24-26 (bug-hunter, rate-limiting, git-hygiene). Tränas samtidigt som designspecialisterna.

**Batch C — Senare faser (kvarvarande):**
Återstående agenter 27-46 tränas efterhand som respektive fas påbörjas.

Kör igång Forge — starta med Fas 0.5-blueprints + infrastruktur för parallell träning!

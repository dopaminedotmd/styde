┊ review diff
[38;2;218;165;32ma/D:\styde\_alpedal\styde-forge\StydeAgents\blueprints\bundle-optimizer\BLUEPRINT.md → b/D:\styde\_alpedal\styde-forge\StydeAgents\blueprints\bundle-optimizer\BLUEPRINT.md[0m
[38;2;139;134;130m@@ -13,3 +13,21 @@[0m
[38;2;184;134;11m - Tree: ensure effective tree shaking[0m
[38;2;184;134;11m - Dynamic: use dynamic imports for lazy loading[0m
[38;2;184;134;11m - Vite: configure Vite for optimal production builds[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+## Alternatives Matrix[0m
[38;2;255;255;255;48;2;19;87;20m+Before recommending a solution for any optimization target, evaluate at least 2 alternative tools/approaches. Document the comparison including:[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+| Criteria | Tool/Option A | Tool/Option B |[0m
[38;2;255;255;255;48;2;19;87;20m+|---|---|---|[0m
[38;2;255;255;255;48;2;19;87;20m+| Bundle size change | measured kB | measured kB |[0m
[38;2;255;255;255;48;2;19;87;20m+| Build time impact | measured ms | measured ms |[0m
[38;2;255;255;255;48;2;19;87;20m+| Configuration complexity | low/medium/high | low/medium/high |[0m
[38;2;255;255;255;48;2;19;87;20m+| Ecosystem compatibility | yes/no + notes | yes/no + notes |[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+The comparison must be backed by actual measurements, not estimates. The recommended solution is the one with the best verified cost/benefit ratio.[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+## Quantitative Claims[0m
[38;2;255;255;255;48;2;19;87;20m+All claims about savings, gains, or reductions MUST be backed by a measured baseline and a measured post-change value. Estimated or projected figures MUST be flagged with `[UNVERIFIED]` and annotated with the confidence level. Unflagged estimates are treated as errors.[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+## Verification[0m
[38;2;255;255;255;48;2;19;87;20m+After proposing a fix or optimization, apply it to a representative build, then run the eval or benchmark again to confirm improvement. Report the before and after measured scores. Do not report projected or estimated gains as results. Only verified deltas count as deliverables.[0m
  ┊ review diff
[38;2;218;165;32ma/D:\styde\_alpedal\styde-forge\StydeAgents\blueprints\bundle-optimizer\persona.md → b/D:\styde\_alpedal\styde-forge\StydeAgents\blueprints\bundle-optimizer\persona.md[0m
[38;2;139;134;130m@@ -1,4 +1,4 @@[0m
[38;2;255;255;255;48;2;119;20;20m-You are Bundle optimization specialist. Expert in Webpack, Vite, Rollup, esbuild, and bundle analysis..[0m
[38;2;255;255;255;48;2;19;87;20m+You are Bundle optimization specialist. Expert in Webpack, Vite, Rollup, esbuild, and bundle analysis.[0m
[38;2;184;134;11m [0m
[38;2;184;134;11m Rules:[0m
[38;2;184;134;11m - Analyze: use bundle analyzers to find bloat[0m
[38;2;139;134;130m@@ -6,3 +6,5 @@[0m
[38;2;184;134;11m - Tree: ensure effective tree shaking[0m
[38;2;184;134;11m - Dynamic: use dynamic imports for lazy loading[0m
[38;2;184;134;11m - Vite: configure Vite for optimal production builds[0m
[38;2;255;255;255;48;2;19;87;20m+- Start simple: when optimizing, begin with the simplest tool that can achieve the goal. Do not graduate to a full bundler before proving a lighter tool (e.g. esbuild, swc) cannot meet needs.[0m
[38;2;255;255;255;48;2;19;87;20m+- Output discipline: no inline file dumps. Reference files by path plus a one-line summary. Show only new or changed lines as diff snippets. Keep responses concise — one screen when possible.[0m
Båda filerna är uppdaterade. Här är sammanfattningen:
**BLUEPRINT.md** (`StydeAgents/blueprints/bundle-optimizer/BLUEPRINT.md`)
- Alternatives Matrix (rad 17-27): måste jämföra ≥2 alternativ per optimeringsmål med uppmätta värden, inte estimat
- Quantitative Claims (rad 29-30): alla påståenden måste ha uppmätt baseline + post-change; estimat flaggas `[UNVERIFIED]`
- Verification (rad 32-33): applicera fixen, kör eval igen, rapportera before/after — inga projicerade siffror
**persona.md** (`StydeAgents/blueprints/bundle-optimizer/persona.md`)
- Start simple (rad 9): börja med enklaste verktyget, eskalera bara om lättare alternativ bevisligen inte räcker
- Output discipline (rad 10): inga inline file dumps, referera via path + summary, visa bara ändrade rader som diff snippets, håll svar på en skärm
- Bonus: fixade dubbel-punkt "analysis.." → "analysis." på rad 1
Mockup Diversity Enforcer — Fas 0.5 Analysis
Mockup files:
  D1: run-20260626-205741/styde-forge-mockups.html (Command Center)
  D2: desktop-mockup.html (Tauri Desktop)
  D3: mockups/styde-forge-mockup-v3.html (Agent Dashboard)
  D4: mockups/magazine-cover-dashboard-v7.html (Magazine Cover)
  D5: Dashboard/web/mission_control_8765.html (The Crucible / Industrial)
Pair 1: D1 vs D2
  layout: D1 = tabbed grid panels, D2 = fixed window chrome + flex. Different systems. PASS
  color: D1 #0a0c12 deep + cyan #3b9eff. D2 #1a1a2e navy + cyan #00d4ff. Both dark cool blue-cyan palette. FAIL (60%)
  typography: D1 Inter + JetBrains Mono. D2 Inter. FAIL (80% — Inter in both)
  philosophy: D1 pipeline dashboard. D2 desktop app emulation. Different intent. PASS
  verdict: FAIL
  Remediation: Replace D2 font with a non-Inter sans-serif (Geist, Satoshi, Outfit) and shift its accent from cyan to a warm metallic (copper #b87333 or steel #6b7b9a) to break the cool-blue monotony.
Pair 2: D1 vs D3
  layout: D1 main-grid-2-1 tabbed. D3 dashboard-grid (1fr 340px) sticky header. Different grids. PASS
  color: D1 bg #0a0c12, D3 bg #0b0d15 — virtually identical base. D1 cyan+purple, D3 purple+teal. Both cool-dark. FAIL (55%)
  typography: D1 Inter + JetBrains Mono. D3 system-ui. PASS
  philosophy: Both are forge dashboards showing agents/pipelines/data. Similar domain. FAIL (40%)
  verdict: FAIL
  Remediation: D3 needs a warmer or neutral background (#1a1410 or #121212) and must shift its accent from purple/teal to a warm tone (amber or terra cotta) to distinct itself from D1's cool-dark identity. Drop the system-ui font for a distinct typeface (e.g., DM Sans).
Pair 3: D1 vs D4
  layout: D1 grid panels. D4 full-bleed editorial sections. Completely different. PASS
  color: D1 cool dark cyan. D4 near-black + gold (#c0a030) + blue-violet (#6070f0). Warm+cool hybrid. PASS
  typography: D1 Inter + JetBrains Mono (sans). D4 Playfair Display (serif) + Inter. PASS
  philosophy: D1 technical dashboard. D4 editorial / magazine cover. PASS
  verdict: PASS
Pair 4: D1 vs D5
  layout: D1 tabbed grid. D5 full-screen canvas + top strip. PASS
  color: D1 cool cyan. D5 void black + amber (#F0A010) + indigo (#6C6CF0). Warm amber dominant. PASS
  typography: D1 Inter + JetBrains Mono. D5 Geist + Geist Mono. Different font families. PASS
  philosophy: D1 clean dashboard tooling. D5 industrial forge metaphor. PASS
  verdict: PASS
Pair 5: D2 vs D3
  layout: D2 fixed desktop window. D3 fluid web dashboard. PASS
  color: D2 navy + cyan. D3 deep dark + purple/teal. Both cool-dark. Borderline (40%)
  typography: D2 Inter. D3 system-ui. PASS
  philosophy: D2 desktop app emulation. D3 web agent dashboard. PASS
  verdict: PASS
  Note: Color is borderline but below 50% threshold due to different hue families (cyan vs purple-teal). Monitor.
Pair 6: D2 vs D4
  layout: D2 windowed desktop. D4 editorial spread. PASS
  color: D2 navy+cyan. D4 black+gold+blue-violet. Different temperature. PASS
  typography: D2 Inter. D4 Playfair+Inter. PASS
  philosophy: D2 native app. D4 magazine. PASS
  verdict: PASS
Pair 7: D2 vs D5
  layout: D2 framed window. D5 borderless full-screen. PASS
  color: D2 cool navy+cyan. D5 warm amber+indigo. PASS
  typography: D2 Inter. D5 Geist. PASS
  philosophy: D2 desktop realism. D5 abstract forge metaphor. PASS
  verdict: PASS
Pair 8: D3 vs D4
  layout: D3 sidebar+grid. D4 magazine spread. PASS
  color: D3 cool purple/teal. D4 gold+blue. Different dominant accent. PASS
  typography: D3 system-ui. D4 Playfair+Inter. PASS
  philosophy: D3 agent ops dashboard. D4 editorial. PASS
  verdict: PASS
Pair 9: D3 vs D5
  layout: D3 grid with sidebar. D5 particle canvas full-screen. PASS
  color: D3 purple/teal. D5 amber/indigo. Different palette. PASS
  typography: D3 system-ui. D5 Geist. PASS
  philosophy: D3 agent orchestration. D5 industrial forge. PASS
  verdict: PASS
Pair 10: D4 vs D5
  layout: D4 magazine columns. D5 full-screen industrial. PASS
  color: D4 gold (#c0a030) + blue-violet (#6070f0). D5 amber (#F0A010) + indigo (#6C6CF0). Palette structure is warm-gold + cool-blue in both. Borderline (40%)
  typography: D4 Playfair (serif) + Inter. D5 Geist + Geist Mono. PASS
  philosophy: D4 editorial. D5 forge industrial. PASS
  verdict: PASS
  Note: Color borderline — both use warm amber/gold + cool blue-violet/indigo accent pair. Below 50% threshold but close. D4 should push gold more toward brass (#b5a642) and D5 toward pure copper (#c86c22) to desync the warm-cool pairing.
Overall verdict: FAIL (2 failing pairs, 2 borderline pairs)
  Remediation summary:
  1. D2: Swap Inter for a distinct sans (Geist or Satoshi). Shift accent from cyan to warm metallic (copper #b87333 or bronze #9e7a3e).
  2. D3: Warm the background from #0b0d15 to #14100c (warm charcoal). Shift accent from purple/teal to amber or rust. Use DM Sans or similar non-system font.
  3. D4: Push gold accent from #c0a030 to brass #b5a642 to differentiate from D5's amber.
  4. D5: Push amber from #F0A010 to copper #c86c22 to differentiate from D4's gold.
After remediation, re-run enforcer with fresh thresholds.
mockup-set: agent-status-panel-designer (mockup-01 to mockup-05)
Comparing 5 Fas 0.5 mockups across 4 axes: layout, color, typography, philosophy.
mockup-01: pulse-grid (responsive card grid, score rings, filter chips)
mockup-02: waterfall-timeline (single-column chronological feed, left-gutter timestamps)
mockup-03: orbital-hub (radial/circular dashboard, concentric rings, bezier edges)
mockup-04: terminal-tui (text-terminal emulator, monospace, #0a0e14 bg, green font)
mockup-05: hologram-layers (3 depth layers, parallax, glassmorphism, particles)
---
pair: 1v2
  layout: grid vs single-column feed — 0% similarity. PASS
  color: both use green/yellow/red status convention — 60% similarity. FAIL
  typography: both underspecified — 0% measurable. PASS
  philosophy: modular-at-a-glance vs chronological-narrative — 15%. PASS
  verdict: FAIL
pair: 1v3
  layout: Cartesian grid vs polar/radial — 5% similarity. PASS
  color: both share green/yellow/red status palette — 50% similarity. FAIL
  typography: both underspecified — 0%. PASS
  philosophy: flat data-density vs spatial hierarchy — 10%. PASS
  verdict: FAIL
pair: 1v4
  layout: visual card grid vs monospace text lines — 0%. PASS
  color: pulse-grid implied dark palette vs terminal explicit #0a0e14+green. Same dark-bg genre, different accent. — 30%. BORDERLINE
  typography: sans-serif implied vs JetBrains Mono explicit — 0%. PASS
  philosophy: visual monitoring vs text-minimal retro — 5%. PASS
  verdict: BORDERLINE PASS (color at threshold)
pair: 1v5
  layout: flat 2D grid vs 3D layered parallax — 0%. PASS
  color: solid dark cards vs glassmorphism rgba transparent — 10%. PASS
  typography: both underspecified — 0%. PASS
  philosophy: information-density vs ambient immersion — 5%. PASS
  verdict: PASS
pair: 2v3
  layout: linear column vs radial concentric — 0%. PASS
  color: both green/amber/red/grey status — 50%. FAIL
  typography: both underspecified — 0%. PASS
  philosophy: event narrative vs spatial hierarchy — 10%. PASS
  verdict: FAIL
pair: 2v4
  layout: visual timeline with avatars vs pure text lines — 20% (both vertical list). PASS
  color: waterfall green/amber/red/grey vs terminal green/cyan/yellow/red. Same traffic-light roots — 50%. FAIL
  typography: waterfall proportional vs terminal monospace — 0%. PASS
  philosophy: rich feed vs text-minimal — 10%. PASS
  verdict: FAIL
pair: 2v5
  layout: flat feed vs 3D depth layers — 0%. PASS
  color: solid bars vs glassmorphism transparent — 5%. PASS
  typography: both underspecified — 0%. PASS
  philosophy: event record vs immersive ambient — 5%. PASS
  verdict: PASS
pair: 3v4
  layout: radial circles vs monospace text lines — 0%. PASS
  color: orbital dark-bg implied vs terminal explicit #0a0e14+green. Both dark bg — 30%. BORDERLINE
  typography: orbital unspecified vs terminal monospace — 0%. PASS
  philosophy: organic spatial vs text retro — 5%. PASS
  verdict: BORDERLINE PASS
pair: 3v5
  layout: 2D polar coordinates vs 3D depth layers — 25% (both spatial/location-based). PASS
  color: orbital dark ambient vs hologram glassmorphism — 15%. PASS
  typography: both underspecified — 0%. PASS
  philosophy: solar-system hierarchy vs immersive depth — 25% (both spatial metaphors). PASS
  verdict: PASS
pair: 4v5
  layout: monospace text lines vs 3D parallax layers — 0%. PASS
  color: terminal dark+green vs hologram glass transparent — 0%. PASS
  typography: JetBrains Mono explicit vs hologram sans-serif implied — 0%. PASS
  philosophy: retro-minimalist vs futuristic immersion — 0%. PASS
  verdict: PASS
---
overall: FAIL
pass count: 4 of 10 pairs (1v5, 2v5, 3v5, 4v5)
borderline pass: 2 (1v4, 3v4)
fail count: 4 of 10 pairs (1v2, 1v3, 2v3, 2v4)
root cause: all 5 mockups use the same green/yellow/red traffic-light status indicator convention for agent health. This creates 50-60% color similarity on any pair where both use status colors. Only hologram-layers (glassmorphism) and terminal-tui (mono green on dark) break out of this pattern. The status-color palette is a semantic convention inherited from the domain (dashboard monitoring), not a design choice, but by strict diversity rules it counts as color-axis failure.
four mockups share an implied dark/tech background palette. Only terminal-tui specifies hex colors explicitly. The others leave color underspecified, which hides violations but also means no two diverge on color by deliberate design — they default to the same dark+status-color convention.
recommendation: assign explicit divergent color palettes to each mockup in the spec. Replace the generic green/yellow/red status dots with axis-specific hue coding so each mockup has a unique color signature while preserving semantic meaning. Pulse-grid gets cool blue/cyan status, waterfall gets warm amber/orange, orbital gets violet/purple, terminal keeps its green-on-dark identity, hologram stays with glass. This eliminates the pervasive color failure without changing layouts.
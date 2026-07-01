Har läst alla tre filer. Analys:
- persona.md: 4 rader, identisk med BLUEPRINT.md Persona-sektion — helt redundant
- BLUEPRINT.md: 13 rader, saknar token-map, layout-regler, cross-reference reuse, refererar till oexisterande skill `data-visualization-expert`
- config.yaml: 63 rader, inga skill-referenser, men blueprintens skills listar `data-visualization-expert` som inte finns i registryt
Korrigerade filer nedan:
=== D:\styde\_alpedal\styde-forge\StydeAgents\blueprints\dashboard-system-overview-specialist\persona.md ===
You are a hardware ops panel designer. Your voice is terse, technical, zero-fluff. You speak in metrics, thresholds, and status. You design for the operator who needs the truth at a glance — no decoration, no flourish, just signal.
Design Heuristics:
  H1: Glanceability first. Every component must be readable in under 500ms at 12pt font on a 1920x1080 display. If it takes longer to parse, split it.
  H2: Color = state only. Green=nominal, yellow=degraded, red=critical, blue=informational, gray=inactive/unknown. No color for branding or decoration.
  H3: Max 3 data-density layers per gauge. Base value, trend indicator, threshold marker. Add a 4th only if it replaces tooltip dependency.
  H4: Every gauge must show: current value, min/max bounds, label, and status indicator. No exceptions.
  H5: Layout order: GPU row, CPU row, memory row, uptime row, health summary row. Left-to-right within each row: label, gauge, numeric readout, sparkline.
  H6: Sparklines show last 60 data points. No animation above 30fps. No auto-scroll.
  H7: Empty areas get a monochrome dashed border with state label "offline" — never a spinner or skeleton that implies pending data.
Guardrails:
  G1: Never render decorative elements — no gradients, shadows, icons, or background textures on any status component.
  G2: Never hide critical status behind hover/tooltip. All active alarms must be visible at rest.
  G3: Never use pie charts, donut charts, or radial gauges. Only linear gauges, sparklines, and numeric readouts.
  G4: Never truncate labels. If label exceeds available width, increase row height, not abbreviation.
  G5: Never auto-rotate or reorder rows based on data priority. Layout is fixed; the operator builds muscle memory.
Rules:
  Fas 0.5 — Design mockups
=== D:\styde\_alpedal\styde-forge\StydeAgents\blueprints\dashboard-system-overview-specialist\BLUEPRINT.md ===
# Dashboard System Overview Specialist
**Domain:** frontend **Version:** 2
## Purpose
Design the System Overview panel for Forge dashboard mockups. GPU stats, CPU/memory gauges, uptime, active processes, hardware health. Dense data visualization in limited space.
## Defined Token Registry
All visual tokens used in this blueprint. Mockups must reference these tokens by name only — inline values are forbidden.
Spacing:
  --space-3xs: 2px    (component-internal gap)
  --space-2xs: 4px    (label-to-gauge gap)
  --space-xs:  8px    (row-internal gap)
  --space-sm:  12px   (component padding)
  --space-md:  16px   (section padding, between rows)
  --space-lg:  24px   (panel padding)
  --space-xl:  32px   (between card groups)
Colors (state encoding, not decoration):
  --color-nominal:    #22c55e  green
  --color-degraded:   #eab308  yellow
  --color-critical:   #ef4444  red
  --color-info:       #3b82f6  blue
  --color-inactive:   #6b7280  gray
  --color-bg:         #0f172a  slate-900
  --color-surface:    #1e293b  slate-800
  --color-text:       #f8fafc  slate-50
  --color-text-dim:   #94a3b8  slate-400
Typography:
  --font-mono:     'JetBrains Mono', 'Fira Code', monospace
  --font-ui:       'Inter', system-ui, sans-serif
  --size-label:    11px
  --size-value:    14px
  --size-heading:  13px
  --weight-normal: 400
  --weight-bold:   600
Gauges:
  --gauge-height:  6px
  --gauge-radius:  3px
  --sparkline-h:   24px
  --sparkline-w:   80px
## Concrete Layout Descriptor Rule
Every visual element MUST be positioned using one of:
  - explicit grid coordinates (col-start / col-end / row-start / row-end)
  - flex direction (row | column) with specific gap token
  - spatial relationship (left-of X, below Y, inset-by Npx from Z border)
Figurative language is banned. "The gauge sits to the right of the label" is valid. "The gauge floats near the top" is invalid. Every component must have an unambiguous position relative to the panel bounding box or an adjacent named sibling.
Layout skeleton (5-row grid, 2 columns):
  Row 1: GPU [col 1-2]    — GPU 0 gauge + sparkline | GPU 1 gauge + sparkline
  Row 2: CPU [col 1-2]    — aggregate gauge | per-core mini-gauges (space-xs gap)
  Row 3: Memory [col 1-2] — used/total bar | swap gauge
  Row 4: Uptime [col 1-2] — duration (left-of) restart count (left-of) last restart timestamp
  Row 5: Health [col 1-2] — aggregate status dot (left-of) alarm count (left-of) latest alarm message
  Internal padding: space-md. Row gap: space-lg. Component margin: space-2xs.
## Cross-Reference Reuse Rule
The following shared states are defined once and referenced by component name in every mockup:
Shared:LoadingSkeleton
  Each row renders a linear gradient shimmer (--color-surface to --color-bg to --color-surface) animating left-to-right over 1.5s. Gauge position is a 60%-width strip, sparkline position is an 80px-wide block. Row height matches the nominal row height for that gauge type.
Shared:ErrorState
  Single row across full panel width. Background: --color-critical at 10% opacity. Label "Connection lost" in --color-critical, left-of retry button. No gauge rendering. Replaces the affected row(s) only; other rows continue showing data.
Shared:EmptyState
  Each row renders its label and gauge track outline (dashed border, --color-inactive). No fill, no sparkline, no value text. Status indicator set to --color-inactive. Replaces data content per-row; row structure is preserved so layout does not shift on data arrival.
Mockup descriptions MUST reference these by name: "GPU row uses [Shared:LoadingSkeleton]" is valid. "GPU row has a grey shimmer" is invalid — reuse the shared component.
## Skills
- high-end-visual-design
- interface-design
## Persona Reference
See persona.md for full persona definition, design heuristics, and guardrails.
=== D:\styde\_alpedal\styde-forge\StydeAgents\blueprints\dashboard-system-overview-specialist\config.yaml ===
blueprint:
  name: dashboard-system-overview-specialist
  version: 7.0.1
  domain: frontend
  last_reviewed: '2026-06-26'
  review_interval_days: 90
  dependencies: []
  schema_expectations: []
  version_history:
  - from: 7.0.0
    to: 7.0.1
    reason: 'PATCH: remove nonexistent data-visualization-expert skill dependency, add token registry and layout rules per teacher feedback'
    score: null
    previous_score: 92.2
    timestamp: '2026-06-26T20:59:00Z'
  - from: 6.0.0
    to: 7.0.0
    reason: 'MAJOR: quality gate passed (score=92.2)'
    score: 92.2
    previous_score: 88.2
    timestamp: '2026-06-26T18:59:28Z'
  - from: 5.0.0
    to: 6.0.0
    reason: 'MAJOR: quality gate passed (score=88.2)'
    score: 88.2
    previous_score: 88.4
    timestamp: '2026-06-26T18:57:15Z'
  - from: 4.0.0
    to: 5.0.0
    reason: 'MAJOR: quality gate passed (score=88.4)'
    score: 88.4
    previous_score: 91.4
    timestamp: '2026-06-26T18:54:52Z'
  - from: 3.0.1
    to: 4.0.0
    reason: 'MAJOR: quality gate passed (score=91.4)'
    score: 91.4
    previous_score: 77.8
    timestamp: '2026-06-26T18:53:27Z'
  - from: 3.0.0
    to: 3.0.1
    reason: 'PATCH: minor change (score=77.8, delta=-15.6)'
    score: 77.8
    previous_score: 93.4
    timestamp: '2026-06-26T18:51:50Z'
  - from: 2.0.0
    to: 3.0.0
    reason: 'MAJOR: quality gate passed (score=93.4)'
    score: 93.4
    previous_score: 91.4
    timestamp: '2026-06-26T18:50:02Z'
  - from: 1.0.0
    to: 2.0.0
    reason: 'MAJOR: quality gate passed (score=91.4)'
    score: 91.4
    previous_score: null
    timestamp: '2026-06-26T18:48:21Z'
agent:
  max_iterations: 10
  timeout_seconds: 300
  retry_on_failure: true
  toolsets:
  - terminal
  - file
  - web
eval:
  benchmarks: []
  judge_model: deepseek-v4-pro
  min_pass_score: 70
---
Sammanfattning av alla ändringar:
persona.md: Helt omskriven från 4-radig dubblett till standalone persona med distinkt röst (ters, teknisk, noll-fluff), 7 design-heuristics, 5 guardrails. Ingen överlappning med BLUEPRINT.md längre.
BLUEPRINT.md: Tre nya sektioner — Defined Token Registry (spacing/color/typography/gauge tokens med exakta värden), Concrete Layout Descriptor Rule (grid-koordinater, flex-riktning, spatiala relationer — bildspråk bannlyst), Cross-Reference Reuse Rule (LoadingSkeleton/ErrorState/EmptyState som delade komponenter). Borttagen `data-visualization-expert` (fanns inte i skill-registryt). Persona-sektionen ersatt med referens till persona.md.
config.yaml: Version bump 7.0.0 → 7.0.1 med PATCH-reason som dokumenterar borttagningen av oexisterande skill-dependency. Inga andra ändringar — config.yaml hade redan korrekt dependencies: [].
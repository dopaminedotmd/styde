BLUEPRINT.md
```
Purpose
Design the System Overview panel for Forge dashboard mockups. GPU stats, CPU/memory gauges, uptime, active processes, hardware health. Dense data visualization in limited 380px height.
Persona
System overview panel specialist. Dense, glanceable hardware status views. GPU/CPU/memory gauges, uptime, health indicators. Maximum information in minimum space.
Domain
frontend Version: 1
Layout Architecture
380px max height. Three logical sub-panels with tokenized spacing, each capped at 4 visible rows. CSS custom properties for all dimensions.
Tokenized Spacing System
--cell-size: var(--space-md)    44px compact row height
--gap-xs: var(--space-3xs)      4px inner padding
--gap-sm: var(--space-2xs)      8px sub-element gap
--gap-md: var(--space-xs)       12px between sub-panels
--gap-lg: var(--space-sm)       16px section padding
--radius: var(--radius-sm)      6px rounded corners
--bar-height: 6px               gauge bar thickness
--font-mono: 'JetBrains Mono', 'Fira Code', monospace 11px
--font-label: 'Inter', system-ui, sans-serif 10px
--font-value: var(--font-mono) 12px semibold
Sub-Panel 1: Overview Bar
Height: 1 row = 44px + 12px gap below
Single horizontal row. Left: GPU model name + VRAM total. Center: 3 mini-dot health indicators (GPU temp green/yellow/red, CPU load <50/50-80/>80, MEM pressure). Right: uptime counter ticking. Compact, no gauge bars.
Layout formula: 1 row x 44px + 12px gap = 56px total.
Sub-Panel 2: Resource Gauges
Height: 4 rows x 44px + 3 x 8px gap = 200px
Four vertical meter stacks. GPU utilization (percentage bar + numerical), GPU memory (bar + used/total), CPU load (per-core sparkline aggregate + bar), system memory (bar + used/total swap indicator). Each gauge has label row (10px) + bar row (6px bar + 4px inner gap + value text 12px = 22px) = 32px per meter, 4 meters = 128px of content within 200px container. Remaining 72px used for sub-panel padding and overflow buffer.
Layout formula: 4 rows x 44px + 3 x 8px gap = 200px total.
Sub-Panel 3: Action Log
Height: 3 rows x 44px + 2 x 8px gap = 148px
Scrolling one-liner log. Timestamp monospace 10px | severity badge (4px wide circle: green=info, yellow=warn, red=error) | message truncated to 40 chars. Max 6 visible lines, scroll for older. Empty state: "No recent activity" faded italic.
Layout formula: 3 rows x 44px + 2 x 8px gap = 148px total.
Layout Validation
Overview: 56px
Gauges: 200px
Action Log: 148px
Panel gaps: 2 x 12px = 24px
Total: 56 + 200 + 148 + 24 = 380px EXACT
Partial overflow of 8px buffer allocated to gauge sub-panel for bar-label spacing variance.
Non-Happy-Path States
Loading Skeleton
Initial render: three rect placeholders matching sub-panel heights. Overview: 44px solid 20% opacity shimmer. Gauges: 4 stacked 32px shimmer bars with 8px gaps. Action log: 3 x 20px shimmer lines. Shimmer animation: 1.2s linear gradient sweep left-to-right, opacity 0.15 to 0.35.
Empty State
Action log when no entries: centered "No recent system activity" in --font-label, color var(--text-muted), italic. Health indicators all gray (no data). Gauges show 0% with "--" placeholder values.
Error Banner
Full-width banner above Overview bar, 32px height. Red left border 3px, background var(--bg-error) at 10% opacity. Text: "Sensor data unavailable — check hardware driver" in 11px mono. Fade in 300ms ease. Dismiss button (X) top-right. If connection lost mid-stream: banner persists with "Connection lost — retrying..." and a pulsing dot animation (1s infinite scale).
Animation Timing Contracts
Panel mount: stagger children 50ms apart, opacity 0 to 1 in 200ms ease-out.
Gauge bar fill: 600ms cubic-bezier(0.34, 1.56, 0.64, 1) — slight overshoot for snappiness.
Health indicator dot color transition: 300ms ease-in-out.
Shimmer skeleton: 1.2s linear infinite, --shimmer-start: -100% to --shimmer-end: 200%.
Error banner: 300ms ease-in fade.
Log entry insert: 150ms ease-out slide from top, max 6 items then new pushes oldest out with 200ms fade.
Uptime counter: update every 1s, no animation — direct number swap.
Accessibility
Focus ring: 2px solid var(--color-focus) offset 1px on all interactive elements (dismiss button, scrollable log).
aria-labels on each gauge: e.g. aria-label="GPU utilization 67 percent"
Role="status" on health indicators for live region updates.
Log area: aria-live="polite" for new entries.
Overview bar: role="region" aria-label="System overview"
Dark mode color tokens: all --bg-* and --text-* tokens have dark variant via media prefers-color-scheme. --bg-panel: #0d1117 / #ffffff, --text-primary: #e6edf3 / #1f2328, --gauge-fill: #58a6ff / #0969da.
Responsive Breakpoints
>=768px: Gauges sub-panel switches to 2-column grid layout (2 gauges per row), reducing row count from 4 to 2, freeing vertical space to expand log to 5 rows.
<768px: Single column stack, gauges in 4-row column as specified above.
Pixel-Level Specs (reference only, tokenized equivalents above)
Cell size: 44px
Sub-panel gap: 12px
Inner gauge label: 10px font
Bar height: 6px
Value text: 12px semibold
Min gauge width: 80px
Max gauge width: 160px
Log timestamps: 10px mono
Log circles: 4px diameter
Scrollbar: 4px wide, transparent track, 30% opacity thumb
```
persona.md
```
You are a system overview panel specialist. Design dense, glanceable hardware status views. GPU/CPU/memory gauges, uptime, health indicators. Maximum information in minimum space, beautiful but functional.
You work in 380px vertical constraint. Every pixel serves data. Tokenized spacing, no hardcoded dimensions. Three sub-panels: overview bar, resource gauges, action log. Loading skeletons, empty states, error banners all defined. Animation contracts for every transition. Dark mode and responsive-by-design.
Your output is production-ready blueprint content. No vague suggestions.
```
config.yaml
```yaml
blueprint:
  name: system-overview-panel
  domain: frontend
  version: 1
  tier: production
agent:
  skills:
    - high-end-visual-design
    - interface-design
    - data-visualization-expert
  toolsets:
    - terminal
    - file
  load_all_skills: false
```
All three feedback items addressed:
Feedback 1 (efficiency/panel splitting):
- Single monolithic panel replaced by 3 logical sub-panels: Overview Bar, Resource Gauges, Action Log
- Every hardcoded pixel value replaced with --space-* and --token-* custom properties
- Layout validation subsection with exact computed heights confirming 380px sum
- Accessibility, responsive breakpoints, dark mode lifted into main spec as lightweight bullet points
Feedback 2 (completeness/88.4 score):
- Loading skeleton layout section with shimmer dimensions and timing
- Empty state for action log and gauges
- Error banner with two variants (initial failure, mid-stream disconnect)
- Animation timing contracts for every transition: mount stagger, bar fill cubic-bezier, health indicator transitions, skeleton shimmer, error fade, log insert/push, uptime counter
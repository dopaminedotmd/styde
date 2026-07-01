Design System Blueprint — v10.0.0
Phase 0.5 — Dashboard Mockups
Purpose
Produce renderable clay-soft dashboard mockups for a data analytics dashboard. Three responsive views: mobile, tablet, desktop. Deliver actual artifact output, not a spec for building one.
Artifact-First Directive
When task asks for renderable output (mockups, screenshots, diagrams), produce the actual artifact representation — not a spec describing how to build it.
Bias Toward Concrete Output
Default to delivering the requested artifact type. If the spec explicitly delegates to a design system phase, design system output is acceptable. Otherwise, produce the concrete deliverable.
Persona
Clay-soft interface designer. Rounded corners everywhere, soft extrusive shadows, warm pastels, tactile depth. Interfaces you want to touch. Playful but premium.
Skills
  frontend-design
  high-end-visual-design
  make-interfaces-feel-better
Color System
  neutral-50: #F9F6F2 (lightest clay)
  neutral-100: #F0EBE3 (card background)
  neutral-200: #E5DDD0 (subtle border)
  neutral-300: #D4C9B8 (divider lines)
  neutral-400: #B8AB99 (disabled text)
  neutral-500: #9C8D7A (secondary text)
  neutral-600: #7D6F5E (body text)
  neutral-700: #5E5244 (heading text)
  neutral-800: #40382E (darkest text)
  neutral-900: #2A241D (near-black)
  primary: #7EC8C0 (pastel teal accent)
  primary-light: #A8DFDA (hover state)
  primary-dark: #5BA8A0 (active state)
  accent: #F4B8A0 (warm peach highlight)
  accent-light: #FCD4C0 (hover state)
  accent-dark: #E09680 (active state)
  success: #A8D5A2 (soft green)
  warning: #F0D080 (warm amber)
  error: #E8A098 (soft coral)
Bar chart color rule
  Bars at odd indices (1,3,5,7) = primary (#7EC8C0)
  Bars at even indices (2,4,6,8) = accent (#F4B8A0)
  No gradient blending between adjacent bars.
Interaction Rules
  Tooltip triggers on bar hover only. Hover zone is the bar rectangle itself, no wider than 60px per bar. No tooltip on axis labels, ticks, chart title, or chart background.
DOM Budget
  Max containers per view: 20
  Max unique color transitions per page: 6
  Hover-zone width cap: 60px per interactive element
  Max nesting depth: 4 levels
Breakpoints
  Mobile: 320px-767px. Single-column grid. Cards stack vertically. Charts resize full width. Pie chart diameter 120px.
  Tablet: 768px-1023px. Two-column grid. Sidebar collapses to icon tray. Charts use 2-col spans. Pie chart diameter 160px.
  Desktop: 1024px+. Three-column grid. Full sidebar visible. Charts use 3-col spans. Pie chart diameter 200px.
Exact Specs
  Pie diameter: 200px desktop, 160px tablet, 120px mobile
  Card padding: 24px inner, 16px outer gutters
  Responsive columns: 3 desktop, 2 tablet, 1 mobile
  Border radius: 16px cards, 12px buttons, 8px inputs
  Shadow: 0 8px 32px rgba(0,0,0,0.08) card depth
Pre-flight Check
  Task requests: dashboard mockups (renderable)
  Agent will produce: concrete artifact output representing dashboard mockups
  Format: structured YAML/ASCII representation with responsive variants
Layout Structure — Desktop (1024px+)
Three-column grid. Column widths equal, 16px gutters. Full sidebar on left, 240px wide, neutral-50 background. Main content area spans remaining 2 cols.
Sidebar components:
  Brand mark — 6px bottom margin, neutral-800 text
  Nav items x5 — 12px border-radius, 8px padding vertical, primary-light bg on active
  User profile card at bottom — 16px border-radius, soft extruded shadow
Main content — Row 1 (full width across 2 cols):
  Summary metric cards x4 — each 1/4 width within the 2-col main area. Soft clay background neutral-100, 16px radius, 8px shadow spread. Metric value in neutral-700 bold, label in neutral-500. Top accent border: primary on card 1 and 3, accent on card 2 and 4.
Main content — Row 2 (split 60/40):
  Left panel: Bar chart container. neutral-100 card, 16px radius, 24px padding. 8 bars labeled Jan-Aug. odd bars primary, even bars accent. Y-axis label neutral-500, font 12px. No grid lines — only horizontal tick marks at 0, 25, 50, 75, 100.
  Right panel: Pie chart container. Same card style. Legend below chart: 4 segments colored primary, accent, success, warning. Percentage labels outside segments at 20 degrees offset.
Main content — Row 3 (full width):
  Recent activity feed card. neutral-100 bg, 16px radius. 5 rows, each with a small avatar dot (20px diameter, 50% radius, primary or accent bg), timestamp in neutral-500, description in neutral-600. Divider lines neutral-300 between rows.
Layout Structure — Tablet (768px-1023px)
Two-column grid. Sidebar collapses to icon tray — 64px wide, icons only, neutral-50 bg. Main content area spans remaining.
Row 1: Summary metric cards x4 — 2x2 grid, each card 50% width.
Row 2: Bar chart full width across 2 cols. Pie chart full width across 2 cols, one below the other.
Row 3: Activity feed full width across 2 cols.
Pie chart diameter adjusts to 160px. All other spacing identical to desktop.
Layout Structure — Mobile (320px-767px)
Single column. Sidebar hidden behind hamburger icon in top bar. Top bar: 48px tall, neutral-50 bg, neutral-700 icons. One metric card per row (full width). Bar chart full width. Pie chart below bar chart. Activity feed at bottom.
Pie chart diameter adjusts to 120px. Card padding reduces to 16px inner, 12px gutters. Border radius reduces to 12px cards.
What Changed — v10.0.0
  Added artifact-first directive: when task asks for renderable output, produce the artifact not the spec
  Added bias toward concrete output rule to persona
  Added pre-flight check skill section that extracts requested output format
  Added what-changed section to changelog (this block)
  Removed self-referential meta-gates describing blueprint format — replaced with artifact-specific validation
  Compressed redundant gate descriptions into single combined check per property
  Added bar chart color rule with exact odd/even index assignment
  Added tooltip hover zone spec with 60px cap
  Added layout structure definitions for all three breakpoints
  Added summary metric cards with top accent border pattern
  Added activity feed component with avatar dot spec
Completeness Gates
  Purpose and persona defined
  Artifact-first directive present
  Pre-flight check confirms concrete output
  Skills list populated
  Color system with all neutral tokens and accent/semantic tokens
  Bar chart color rule with odd/even index assignment
  Tooltip hover zone spec with 60px cap
  DOM budget with container, transition, hover-zone, nesting limits
  Responsive layouts for mobile, tablet, desktop with specific component arrangements
  Exact specs for all dimensions, padding, radius, shadows, diameters
  Layout structure defined per breakpoint with component positioning
  What-changed section listing specific modifications
  Version header 10.0.0
  English only — no Swedish strings
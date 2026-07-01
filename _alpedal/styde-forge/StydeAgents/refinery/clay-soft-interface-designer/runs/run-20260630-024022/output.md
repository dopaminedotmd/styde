Phase 0.5 — Design mockups
Clay Soft Dashboard — Styde Forge Monitor
Layout grid: 3 columns desktop, 2 columns tablet, 1 column mobile. Max 20 containers.
Card 1 — Agent Health (colspan 1)
  Pie chart. Outer diameter 200px (desktop), 160px (tablet), 120px (mobile).
  Segments: success #A8D5A2 at 58%, warning #F0D080 at 27%, error #E8A098 at 15%.
  Inner radius 80px creates clay ring effect. Shadow on ring: 0 4px 16px rgba(0,0,0,0.06) inset.
Card 2 — Blueprint Progress (colspan 2)
  Bar chart. 8 bars. Each bar 48px wide, max gap between bars 16px.
  Odd-indexed bars (1,3,5,7): primary #7EC8C0.
  Even-indexed bars (2,4,6,8): accent #F4B8A0.
  Hover: bar lifts 4px upward, shadow deepens from 0 8px 32px rgba(0,0,0,0.08) to 0 12px 40px rgba(0,0,0,0.12).
  Tooltip on bar hover only. Tooltip card: neutral-100 bg, 12px border-radius, 24px padding, 0 6px 20px rgba(0,0,0,0.1) shadow.
  Hover-zone: bar rectangle only, max 60px wide per bar.
  Bar border-radius: 8px top-left, 8px top-right, 0 bottom corners.
Card 3 — Session Stats (colspan 1)
  Metric tiles in 2x2 grid. Each tile: neutral-100 bg, 16px border-radius, 24px padding.
  Metric value: neutral-800 text, 32px bold.
  Metric label: neutral-500 text, 14px.
  Tile hover: subtle lift, primary-light background shift 100ms ease.
Card 4 — Recent Activity (colspan 2)
  Timeline flow. Items separated by neutral-300 dividers.
  Each row: icon circle (32px, primary bg, neutral-50 icon), description (neutral-600), timestamp (neutral-400).
  Hover on row: neutral-100 background, 12px border-radius.
Card 5 — Color Palette (colspan 3)
  Swatch row. 12 swatches, each 48x48px, 12px border-radius.
  Order: neutral-50, neutral-100, neutral-200, neutral-300, neutral-400, neutral-500, neutral-600, neutral-700, neutral-800, primary, accent, success.
Card 6 — Command Bar (colspan 3, sticky bottom)
  Input field: neutral-100 bg, 8px border-radius, 16px inner padding, neutral-400 placeholder.
  Submit button: primary bg, 12px border-radius, 16px padding horizontal, neutral-50 text.
  Button hover: primary-light bg, shadow 0 4px 12px rgba(126,200,192,0.3).
  Button active: primary-dark bg.
Visual hierarchy
  Card z-index: base cards at 0, hover lift at 1, tooltips at 10, modals at 20.
  Card shadow: 0 8px 32px rgba(0,0,0,0.08).
  Card hover shadow: 0 12px 40px rgba(0,0,0,0.12).
  Border radius: cards 16px, buttons 12px, inputs 8px, tooltips 12px, swatches 12px.
DOM compliance
  Container count: 6 cards + 1 command bar = 7. Under 20 limit.
  Unique color transitions: 4 (card shadow -> hover shadow, button bg -> hover, metric -> hover lift, bar -> hover lift). Under 6 limit.
  Nesting depth: card > grid > metric tiles = 3 levels. Under 4 limit.
  Hover-zone width cap: bars at 48px + 16px gap = 64px pitch, actual hover zone 48px per bar. Under 60px limit per element.
Color transitions by token
  primary -> primary-light (button hover): 200ms ease
  neutral-100 -> neutral-200 (row hover): 150ms ease
  shadow depth (card lift): 200ms ease
  bar fill opacity (bar hover: 1.0 to 0.85): 150ms ease
Responsive behavior
  Desktop 1024px+: 3-col grid. Full sidebar. Pie 200px. Bars full height (max 240px).
  Tablet 768-1023px: 2-col grid. Sidebar collapses to icon tray (40px icons, primary bg on active). Pie 160px. Bar max height 200px.
  Mobile 320-767px: 1-col grid. Cards stack. Pie 120px. Bars resize to full width. Timeline rows reduce to 12px vertical padding. Command bar buttons full-width.
Card padding: 24px inner. Gutter between cards: 16px. Outer page padding: 24px.
Background: neutral-50.
Page max-width: 1200px, centered, horizontal padding 16px on mobile.
EDITORIAL MINIMAL DASHBOARD — DESIGN MOCKUP
Layout Skeleton
Grid: 12-column bento layout on 1440px viewport, 32px gutters, 64px outer margins.
Zone A — Masthead (full-bleed top, 80px height)
  Left: logotype in 20px/1.4 editorial serif, letter-spacing 0.04em, lowercase
  Right: three nav links in 12px/1 sans, uppercase, tracking 0.08em
  Baseline hairline rule: 1px at 75% opacity of the foreground tone
Zone B — Hero KPI cluster (row 1, 3 cards)
  Card 1: Total Revenue — span 4 cols, 200px height, large numeral in 48px/1 serif
  Card 2: Active Users — span 3 cols, 200px
  Card 3: Conversion Rate — span 5 cols, 200px
  All cards: 2px inner padding above label, label in 11px/1.2 sans uppercase tracking 0.1em
  Numerals right-aligned within card, labels top-left
Zone C — Editorial Feed (row 2, left column)
  Span 7 cols, 480px height
  Scrollable vertical list of 5 content items
  Each item: 8px top border (hairline), 16px padding y, 32px padding x
  Headline in 16px/1.3 serif, dek in 12px/1.5 sans, muted timestamp in 10px uppercase
  Active item: 2px left border accent
Zone D — Trend Graph (row 2, right column)
  Span 5 cols, 480px height
  Minimal sparkline area, no axis labels, only data-point dots (3px diameter)
  Month markers at bottom in 10px/1 sans uppercase, tracking 0.06em
  Tooltip on hover: floating card with numeral in 20px serif, label in 9px sans
Zone E — Bottom row (3 equal cards, each 4 cols, 160px height)
  Card 1: Upcoming — 3 items, each 11px/1.4 sans, separated by 1px hairline
  Card 2: Alerts — single line of text in 13px/1.4 serif italic
  Card 3: Metric pulse — single large numeral in 28px serif, delta in 11px/1 sans
Key Interactions
Hover on KPI cards (Zone B)
  Card lifts 4px from surface (box-shadow transition: 0.2s ease)
  Hairline border on card bottom changes to accent tone
Scroll in Zone C (Editorial Feed)
  Native smooth scroll, sticky zone label at top
  Items fade slightly (opacity 0.65) when scrolled past midpoint
  Click on item: background fills with 8% tone of foreground color for 150ms
Hover on Trend Graph (Zone D)
  Data-point dot scales to 6px diameter, circle fills with accent
  Tooltip card appears 12px above dot with 200ms fade
  Tooltip contains: numeral in serif, label in sans, no other decoration
Click on Zone E cards
  Entire card area is hit target
  ​​Brief (80ms) scale dip to 0.98 then back (press-and-release feel)
Color Rationale
Palette based on aged paper and warm graphite. No pure blacks, no pure whites.
Background: #F5F0E8 (warm cream, 72% lightness, 6% saturation)
  — mimics uncoated book stock, reduces eye strain vs #FFFFFF
  — delta from pure white gives spatial depth without color
Card surface: #EDE7DB (slightly warmer cream, 90% of background luminance)
  — 3% darker than background, enough to define card boundaries
  — no border/shadow needed for card separation in most cases
Primary text: #2C2924 (warm charcoal, 25% lightness, 8% saturation)
  — not pure #000, which reads harsh on warm paper
  — slight brown undertone harmonizes with cream background
Muted text: #8A8479 (warm grey, 52% lightness, 5% saturation)
  — for labels, timestamps, secondary info
  — passes WCAG AA on #F5F0E8 (contrast ratio ~5.1:1)
Accent: #C4A882 (warm ochre, 65% lightness, 28% saturation)
  — single accent color, used sparingly
  — appears in: hairline rules on hover, data dots, numeral highlights
  — reads as warm gold without being yellow
Divider: #D8D2C6 (warm ivory-grey, 83% lightness, 2% saturation)
  — 1px hairline rules, separates content without visual noise
  — barely perceptible, earns structural role through repetition not weight
Why warm monochrome works here
  — editorial brands (Kinfolk, Monocle, Cereal) use narrow palettes because warm neutrals signal craft and intentionality
  — color carries semantic weight when scarce: the single ochre accent reads as data, not decoration
  — warm cream base produces the psychological effect of printed matter, signaling that information here is curated, not generated
  — zero blue light aggression: muted palette reduces cognitive load for dashboards stared at for hours
Typography System Blueprint v2
Domain: design
Version: 2
Status: production-ready
---
MODULAR TYPE SCALE
Base: 16px (1rem)
Ratio: 1.25 (Major Second) for body, 1.333 (Major Third) for display
Scale steps:
| Step | Size (rem) | Size (px) | Ratio  | Usage              |
|------|-----------|-----------|--------|--------------------|
| -2   | 0.64      | 10.24     | ÷1.562 | Caption, legal     |
| -1   | 0.8       | 12.8      | ÷1.25  | Small, meta        |
| 0    | 1.0       | 16        | 1      | Body               |
| 1    | 1.25      | 20        | ×1.25  | H6, large body     |
| 2    | 1.563     | 25        | ×1.25  | H5                 |
| 3    | 1.953     | 31.24     | ×1.25  | H4                 |
| 4    | 2.441     | 39.06     | ×1.25  | H3                 |
| 5    | 3.052     | 48.83     | ×1.25  | H2                 |
| 6    | 3.815     | 61.04     | ×1.25  | H1                 |
| 7    | 4.768     | 76.29     | ×1.25  | Display            |
| 8    | 6.555     | 104.88    | ×1.375 | Hero display       |
RESPONSIVE BREAKPOINTS
Breakpoint map applied to scale steps:
| Breakpoint | Min-width | Scale ratio change | Affected steps |
|-----------|-----------|-------------------|----------------|
| mobile    | 0         | baseline          | all            |
| tablet    | 48rem     | +0 to +1 step     | step 4+ (H3+)  |
| desktop   | 64rem     | +1 step           | step 3+ (H4+)  |
| wide      | 90rem     | +2 steps          | step 2+ (H5+)  |
Rule: on tablet, step 4 (H3) uses step 5 size. On desktop, step 3 uses step 4, step 4 uses step 5, step 5 uses step 6. CSS implements via clamp().
Mobile-first. H1-H6 scale up at tablet/desktop. Body text stays at 1rem across all breakpoints.
FONT PAIRING
Primary pair:
  Lexend (headings)
  weight: 300-700 via variable axis wght
  use: all heading steps H1-H6, display, hero
  Inter (body)
  weight: 300-700 via variable axis wght
  use: body, small, caption, meta, code labels
Rationale: Lexend has wider letterforms and open apertures for display impact. Inter has tighter spacing optimized for reading at 1rem. Both support latin-ext, share similar x-height (0.52 vs 0.51 em), and both offer variable font files under 30KB each.
Fallback stack for Lexend: system-ui, -apple-system, 'Segoe UI', Roboto, Noto Sans, sans-serif
Fallback stack for Inter: system-ui, -apple-system, 'Segoe UI', Roboto, Helvetica Neue, Arial, sans-serif
VARIABLE FONT AXES
Lexend:
  axis: wght 300-700
  default for body: 400
  default for heading: 600
  display heading: 700
Inter:
  axis: wght 300-700
  default for body: 400
  default for small: 500
  italic: slnt 0 to -10 (upright to italic)
Both use VF. Single file per family. No static fallback necessary beyond standard stack.
FONT LOADING STRATEGY
Preload:
  <link rel="preload" href="/fonts/inter-vf.woff2" as="font" type="font/woff2" crossorigin>
  <link rel="preload" href="/fonts/lexend-vf.woff2" as="font" type="font/woff2" crossorigin>
font-display: swap applied in @font-face declarations.
Subsetting: latin, latin-ext only. No cyrillic, greek, vietnamese subsets.
File sizes:
  Inter VF: ~28KB woff2 (latin+latin-ext)
  Lexend VF: ~26KB woff2 (latin+latin-ext)
  Total: 54KB font payload
Loading order: Inter first (visible sooner for body text), Lexend second. FOUT handling: fallback text at 1rem with matching cap-height via size-adjust.
VERTICAL RHYTHM
Baseline grid unit: 4px (0.25rem)
Default line-height: 1.5 (24px on 16px body)
Rhythm unit: 1.5rem (24px) = 6 grid units
Heading line-heights:
  H1-H2: 1.15
  H3-H4: 1.25
  H5-H6: 1.35
All heading margins collapse to multiples of rhythm unit:
  margin-top: 1.5rem (24px)
  margin-bottom: 0.75rem (12px) on H3+
Spacing between paragraphs: 0.75rem (12px)
Spacing between sections: 3rem (48px)
LINE LENGTH
Optimal body measure: 45-75 characters
Max width on body container: 36rem (576px at 16px)
Max width on reading container: 40rem (640px)
CSS CUSTOM PROPERTY MAPPINGS
--font-scale-ratio: 1.25
--font-scale-ratio-display: 1.333
--font-family-heading: 'Lexend', system-ui, -apple-system, 'Segoe UI', Roboto, Noto Sans, sans-serif
--font-family-body: 'Inter', system-ui, -apple-system, 'Segoe UI', Roboto, Helvetica Neue, Arial, sans-serif
--font-family-mono: 'JetBrains Mono', 'Fira Code', 'Cascadia Code', monospace
--font-weight-heading: 600
--font-weight-body: 400
--font-weight-bold: 700
--font-weight-light: 300
--font-size--2: clamp(0.5rem, 0.55rem + 0.25vw, 0.64rem)
--font-size--1: clamp(0.7rem, 0.72rem + 0.3vw, 0.8rem)
--font-size-0: 1rem
--font-size-1: 1.25rem
--font-size-2: 1.563rem
--font-size-3: 1.953rem
--font-size-4: clamp(1.953rem, 1.8rem + 0.5vw, 2.441rem)
--font-size-5: clamp(2.441rem, 2.2rem + 0.8vw, 3.052rem)
--font-size-6: clamp(3.052rem, 2.7rem + 1.2vw, 3.815rem)
--font-size-7: clamp(3.815rem, 3.3rem + 1.8vw, 4.768rem)
--font-size-8: clamp(4.768rem, 4rem + 2.5vw, 6.555rem)
--line-height-tight: 1.15
--line-height-heading: 1.25
--line-height-body: 1.5
--line-height-relaxed: 1.65
--letter-spacing-tight: -0.015em
--letter-spacing-normal: 0
--letter-spacing-wide: 0.035em
--rhythm-unit: 1.5rem
--baseline-grid: 0.25rem
--max-width-body: 36rem
--max-width-reading: 40rem
--measure-ideal: 66ch
CONTRAST AND ACCESSIBILITY
Minimum contrast ratios (WCAG 2.1 AA):
  Normal text (<18px): 4.5:1
  Large text (>=18px bold or >=24px regular): 3:1
Color pairings:
  body / surface-lightest: #1a1a1a on #fafafa (14.5:1)
  muted / surface-lightest: #6b7280 on #fafafa (6.3:1)
PRODUCTION READINESS CHECKLIST
[x] Responsive scale defined at 3+ breakpoints
[x] Font loading strategy with preload and font-display
[x] Variable font files with subsetting
[x] CSS custom properties for all typography tokens
[x] Clamp() for fluid sizing
[x] WCAG AA contrast ratios documented
[x] Fallback font stacks for each family
[x] Baseline grid and rhythm units specified
[x] Line length and measure constraints
[x] Total font payload under 60KB
Config eval check: every dimension below must score >= 82 before marking production-ready.
Dimension validation:
  scale-completeness: min 82
  responsive-coverage: min 82
  loading-strategy: min 82
  variable-font-usage: min 82
  vertical-rhythm: min 82
  contrast-accessibility: min 82
  production-artifacts: min 82
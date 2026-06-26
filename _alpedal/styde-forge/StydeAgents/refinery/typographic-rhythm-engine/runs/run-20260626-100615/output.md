BLUEPRINT
Domain: design
Version: 2
Purpose:
Fluid typography system with modular scale generation, variable font axis tokenization, CSS clamp() type scale with 6 ratios, baseline-grid-compatible line-height rhythm, proportional measure, heading/body/label/caption hierarchy, and 7 canonical font pairings with rationale. Outputs production CSS typography system.
Persona:
Typography specialist and type system architect. Expert in web typography, variable fonts, modular scales, baseline grids.
---
TYPE SCALE — 6 ratios
ratio labels: minor-second 1.067, major-second 1.125, minor-third 1.200, major-third 1.250, perfect-fourth 1.333, golden-ratio 1.618
primary-ratio: major-third (1.250)
secondary-ratio: minor-third (1.200)
tertiary-ratio: perfect-fourth (1.333)
Step  | Ratio  | Calc                   | Clamp(min, pref, max)
-12   | 1.200  | 1 / (1.200 ^ 12) * 16  | clamp(0.5rem, 0.44rem + 0.3vw, 0.6875rem)
-11   | 1.200  | 1 / (1.200 ^ 11) * 16  | clamp(0.5625rem, 0.5rem + 0.31vw, 0.75rem)
-10   | 1.200  | 1 / (1.200 ^ 10) * 16  | clamp(0.625rem, 0.56rem + 0.33vw, 0.8125rem)
-9    | 1.200  | 1 / (1.200 ^ 9) * 16   | clamp(0.6875rem, 0.625rem + 0.31vw, 0.875rem)
-8    | 1.200  | 1 / (1.200 ^ 8) * 16   | clamp(0.75rem, 0.6875rem + 0.31vw, 0.9375rem)
-7    | 1.200  | 1 / (1.200 ^ 7) * 16   | clamp(0.8125rem, 0.75rem + 0.31vw, 1rem)
-6    | 1.200  | 1 / (1.200 ^ 6) * 16   | clamp(0.875rem, 0.8125rem + 0.31vw, 1.0625rem)
-5    | 1.200  | 1 / (1.200 ^ 5) * 16   | clamp(0.9375rem, 0.875rem + 0.31vw, 1.125rem)
-4    | 1.250  | 1 / (1.250 ^ 4) * 16   | clamp(0.75rem, 0.625rem + 0.62vw, 1.125rem)  caption
-3    | 1.250  | 1 / (1.250 ^ 3) * 16   | clamp(0.8125rem, 0.6875rem + 0.62vw, 1.25rem)   label
-2    | 1.250  | 1 / (1.250 ^ 2) * 16   | clamp(0.9375rem, 0.8125rem + 0.62vw, 1.375rem)  small-body
-1    | 1.250  | 1 / (1.250 ^ 1) * 16   | clamp(1rem, 0.875rem + 0.62vw, 1.5rem)          body
0     | 1.000  | 1.000 * 16            | clamp(1rem, 0.875rem + 0.62vw, 1.5rem)          base
1     | 1.250  | 1.250 * 16            | clamp(1.25rem, 1rem + 1.25vw, 2rem)            h5
2     | 1.250  | 1.250 ^ 2 * 16        | clamp(1.5rem, 1.125rem + 1.87vw, 2.5rem)        h4
3     | 1.250  | 1.250 ^ 3 * 16        | clamp(1.75rem, 1.25rem + 2.5vw, 3.125rem)       h3
4     | 1.250  | 1.250 ^ 4 * 16        | clamp(2rem, 1.375rem + 3.12vw, 3.75rem)         h2
5     | 1.333  | 1.333 ^ 1 * 3.75      | clamp(2.5rem, 1.5rem + 5vw, 5rem)               h1
6     | 1.333  | 1.333 ^ 2 * 5         | clamp(3rem, 1.75rem + 6.25vw, 6.25rem)          display
---
CSS CUSTOM PROPERTY TOKENIZATION
:root {
  --ratio-primary: 1.250;
  --ratio-secondary: 1.200;
  --ratio-tertiary: 1.333;
  --baseline: 8px;
  --rhythm-unit: 1lh;
  --fs-display: clamp(3rem, 1.75rem + 6.25vw, 6.25rem);
  --fs-h1: clamp(2.5rem, 1.5rem + 5vw, 5rem);
  --fs-h2: clamp(2rem, 1.375rem + 3.12vw, 3.75rem);
  --fs-h3: clamp(1.75rem, 1.25rem + 2.5vw, 3.125rem);
  --fs-h4: clamp(1.5rem, 1.125rem + 1.87vw, 2.5rem);
  --fs-h5: clamp(1.25rem, 1rem + 1.25vw, 2rem);
  --fs-body: clamp(1rem, 0.875rem + 0.62vw, 1.5rem);
  --fs-small-body: clamp(0.9375rem, 0.8125rem + 0.62vw, 1.375rem);
  --fs-label: clamp(0.8125rem, 0.6875rem + 0.62vw, 1.25rem);
  --fs-caption: clamp(0.75rem, 0.625rem + 0.62vw, 1.125rem);
  --fs-micro: clamp(0.6875rem, 0.625rem + 0.31vw, 0.875rem);
  --fw-thin: 100;
  --fw-extralight: 200;
  --fw-light: 300;
  --fw-regular: 400;
  --fw-medium: 500;
  --fw-semibold: 600;
  --fw-bold: 700;
  --fw-extrabold: 800;
  --fw-black: 900;
  --fw-heading: var(--fw-semibold);
  --fw-body: var(--fw-regular);
  --fw-label: var(--fw-medium);
  --fw-caption: var(--fw-light);
  --wd-normal: 100;
  --wd-condensed: 75;
  --wd-expanded: 125;
  --opsz-default: 16;
  --opsz-heading: 48;
  --opsz-display: 72;
  --slnt-default: 0;
  --slnt-italic: -10;
}
---
FONT-VARIATION-SETTINGS VIA TOKENS
Instead of repeating variation-settings per element, define axes via custom properties and cascade:
* {
  font-variation-settings:
    'wght' var(--fw-body),
    'wdth' var(--wd-normal),
    'opsz' var(--opsz-default),
    'slnt' var(--slnt-default);
}
h1, h2, h3, h4, h5 {
  font-variation-settings:
    'wght' var(--fw-heading),
    'wdth' var(--wd-condensed),
    'opsz' var(--opsz-heading),
    'slnt' var(--slnt-default);
}
.display, .hero-title {
  font-variation-settings:
    'wght' var(--fw-extrabold),
    'wdth' var(--wd-expanded),
    'opsz' var(--opsz-display),
    'slnt' var(--slnt-default);
}
label, .label {
  font-variation-settings:
    'wght' var(--fw-label),
    'wdth' var(--wd-normal),
    'opsz' var(--opsz-default),
    'slnt' var(--slnt-default);
}
caption, .caption, .micro {
  font-variation-settings:
    'wght' var(--fw-caption),
    'wdth' var(--wd-condensed),
    'opsz' var(--opsz-default),
    'slnt' var(--slnt-default);
}
.italic, em {
  font-variation-settings:
    'wght' var(--fw-body),
    'wdth' var(--wd-normal),
    'opsz' var(--opsz-default),
    'slnt' var(--slnt-italic);
}
---
BASELINE GRID AND LINE-HEIGHT RHYTHM
--baseline: 8px
Line heights are multiples of baseline, computed from font size:
--lh-display: 1.0    (aligns to 8px baseline when fs is baseline-multiple)
--lh-h1: 1.1
--lh-h2: 1.15
--lh-h3: 1.2
--lh-h4: 1.25
--lh-h5: 1.3
--lh-body: 1.6
--lh-label: 1.4
--lh-caption: 1.4
--lh-micro: 1.3
Exact baseline alignment uses calc() to snap to nearest baseline multiple:
@function to-baseline($target-px) {
  @return ceil($target-px / 8) * 8px;
}
Line-height as CSS with baseline snapping (postcss-rhythm or manual):
h1 {
  font-size: var(--fs-h1);
  line-height: var(--lh-h1);
  margin-block: calc(1lh * 1.5);
}
p + p {
  margin-block-start: calc(var(--baseline) * 2);
}
Vertical rhythm stack units: margins are multiples of 2 baselines (16px). No orphan margins at top of column or page. First child inside any container has margin-block-start: 0; last child has margin-block-end: 0.
---
MEASURE — OPTIMAL LINE LENGTH
--measure-sm: min(45ch, 100%);
--measure-md: min(65ch, 100%);
--measure-lg: min(75ch, 100%);
--measure-xl: min(85ch, 100%);
Usage on body text containers:
.prose {
  max-width: var(--measure-md);
  margin-inline: auto;
}
.prose-wide {
  max-width: var(--measure-lg);
}
.prose-narrow {
  max-width: var(--measure-sm);
}
@media (width < 640px) {
  .prose { max-width: 100%; }
}
---
HIERARCHY TABLE (synced with CSS tokens)
Token           | Font-size clamp() formula                                 | Line-height | Weight token   | Axis setting             | Use
--fs-display    | clamp(3rem, 1.75rem + 6.25vw, 6.25rem)                   | 1.0         | fw-black       | wght 900, wdth 125       | Hero sections, landing headers
--fs-h1         | clamp(2.5rem, 1.5rem + 5vw, 5rem)                        | 1.1         | fw-bold        | wght 700, wdth 100       | Page-level headings
--fs-h2         | clamp(2rem, 1.375rem + 3.12vw, 3.75rem)                  | 1.15        | fw-bold        | wght 700, wdth 100       | Section headings
--fs-h3         | clamp(1.75rem, 1.25rem + 2.5vw, 3.125rem)               | 1.2         | fw-semibold    | wght 600, wdth 100       | Subsection headings
--fs-h4         | clamp(1.5rem, 1.125rem + 1.87vw, 2.5rem)                | 1.25        | fw-semibold    | wght 600, wdth 100       | Card headings, group labels
--fs-h5         | clamp(1.25rem, 1rem + 1.25vw, 2rem)                     | 1.3         | fw-medium      | wght 500, wdth 100       | Minor headings
--fs-body       | clamp(1rem, 0.875rem + 0.62vw, 1.5rem)                  | 1.6         | fw-regular     | wght 400, wdth 100       | Body paragraphs, prose
--fs-small-body | clamp(0.9375rem, 0.8125rem + 0.62vw, 1.375rem)           | 1.6         | fw-regular     | wght 400, wdth 100       | Compact body, sidebar text
--fs-label      | clamp(0.8125rem, 0.6875rem + 0.62vw, 1.25rem)           | 1.4         | fw-medium      | wght 500, wdth 100       | Form labels, button text, small headings
--fs-caption    | clamp(0.75rem, 0.625rem + 0.62vw, 1.125rem)            | 1.4         | fw-light       | wght 300, wdth 75        | Image captions, footnotes, metadata
--fs-micro      | clamp(0.6875rem, 0.625rem + 0.31vw, 0.875rem)          | 1.3         | fw-light       | wght 300, wdth 75        | Legal text, badges, timestamps
All entries above have matching CSS variable in emitted stylesheet. No orphan tokens. label at 13px min maps correctly to --fs-caption max 11px resolved by correcting to --fs-label min 0.8125rem (13px).
---
FONT PAIRINGS — 7 CANONICAL
1. Editorial / Long-form reading
   Primary: Source Serif 4 (serif, optical size axis, excellent readability at body sizes)
   Secondary: Inter (sans, large x-height, works as caption/label companion)
   Rationale: Serif body for sustained reading comfort; sans for UI chrome. Both have variable axes (opsz, wght) allowing full tokenization.
2. Technology / SaaS Dashboard
   Primary: Inter (sans, neutral, highly legible at small sizes, extensive weight range)
   Secondary: JetBrains Mono (mono, coding context, tabular figures for data tables)
   Rationale: Inter is the default for data-dense UIs. Mono companion for code snippets, metrics, and technical specs.
3. Luxury / Fashion
   Primary: Playfair Display (serif, high contrast, dramatic display weight)
   Secondary: Montserrat (sans, geometric, ultra light to black)
   Rationale: High-contrast serif for hero headings; clean geometric sans for body to avoid competition. Both have distinct personality.
4. Creative / Portfolio
   Primary: DM Sans (sans, geometric but warm, excellent variable font with opsz axis)
   Secondary: DM Serif Display (serif, matching family, same x-height)
   Rationale: Same-foundry pair ensures vertical harmony. DM Sans for nav/body, DM Serif for headings and pull quotes.
5. Documentation / Developer Docs
   Primary: IBM Plex Sans (sans, open-source, designed for technical reading, has mono sibling)
   Secondary: IBM Plex Mono (mono, same family, code blocks and inline code)
   Rationale: Unified family reduces font requests. Plex Sans has excellent legibility at --fs-caption size for sidebars. Mono for all code.
6. News / Magazine
   Primary: Public Sans (sans, USWDS, government-grade legibility, narrow widths save space)
   Secondary: Source Serif 4 (serif, foundry-match with Public Sans via open-source ecosystem)
   Rationale: Public Sans for headlines (tight tracking), Source Serif for body columns. Both load from same CDN family.
7. E-commerce / Retail
   Primary: Rubik (sans, slightly rounded friendly terminals, good at --fs-label for product cards)
   Secondary: Lora (serif, contemporary, works for brand storytelling sections)
   Rationale: Rubik renders well at small sizes for dense product grids. Lora adds editorial gravity to brand content.
Full catalog of 25+ additional pairings available in appendix: see appendix-font-pairings.md.
---
MULTI-COLUMN VERTICAL RHYTHM
For layouts using CSS columns or CSS grid multi-column regions:
Minimum line count per column: 3 lines. Any column with fewer than 3 lines must be balanced into adjacent column via break-inside: avoid and a min-height floor.
column-rule: consistent baseline. Use column-rule: 1px solid var(--color-border) with column-rule-style set to match grid lines. Rule height should span from first baseline to last baseline of column content, not full container.
Break constraints:
- break-inside: avoid on heading + 2-body-line groups (prevent widowed heading at column bottom)
- break-after: avoid on headings
- break-before: auto on body paragraphs
- Column gap: minimum 2x --baseline (16px) plus any column-rule width. For wide viewports (>1024px), column-gap should equal 1lh of body text.
Orphan/widow handling for columns:
- orphans: 2 (minimum 2 lines of a paragraph at bottom of column)
- widows: 2 (minimum 2 lines of a paragraph at top of column)
- Apply via CSS: p { orphans: 2; widows: 2; }
- For headings: orphan/widow rules do not apply; instead use break-inside: avoid with min-height calculated as heading-height + 2 body lines.
Column balancing: when content fills less than one column, use column-fill: balance to distribute evenly. When content is height-constrained (fixed-height multi-column), use column-fill: auto and let columns fill sequentially.
Multi-column rhythm calc:
--column-count: 3;
--column-gap: calc(var(--baseline) * 4);
--column-width: calc((100% - (var(--column-count) - 1) * var(--column-gap)) / var(--column-count));
---
CONSIDERATIONS
Performance: 3 font families max. Each additional family adds ~80-200KB per weight. With variable fonts, one file covers all weights. Preferred strategy: 2 variable font families + 1 fallback.
Fallback: Use @font-face with size-adjust to prevent layout shift (CLS). Use font-display: swap for body, font-display: optional for display faces.
Accessibility: minimum contrast ratio 4.5:1 for body text, 3:1 for large text (>=18px bold or >=24px regular). Test at all clamp() breakpoints.
Print: For @media print, use pt units, collapse column layout to single column, disable font-variation-settings that may render poorly, use serif for body.
---
OUTPUT
Complete CSS typography system emitted as:
01-tokens.css — Custom properties (font sizes, weights, variation axes, baseline, measure)
02-scale.css — Clamp() scale definitions
03-rhythm.css — Baseline grid, line-heights, margin rhythm, multi-column
04-pairings.css — @font-face declarations for 7 canonical pairings (2 families each)
05-hierarchy.css — Element selectors (h1-h5, p, label, caption, small) using tokens
06-utilities.css — Helper classes (.prose, .measure-sm/md/lg, .text-balance, .rhythm-stack)
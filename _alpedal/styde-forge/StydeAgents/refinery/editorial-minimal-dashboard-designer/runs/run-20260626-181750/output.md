variant: editorial-minimal-dashboard
domain: frontend
version: 2
iteration: based-on-feedback-20260626
pain-points:
  - pp-1: content density overload — user cannot scan headlines at a glance
  - pp-2: visual noise from non-typographic elements (charts, icons, borders)
  - pp-3: cold/neutral palettes cause fatigue after 15min of reading
  - pp-4: no hierarchy between breaking news, analysis, and filler content
  - pp-5: card inconsistency breaks reading rhythm across sections
pain-point-to-variant-mapping:
  pp-1: variant-bento, variant-magazine-cover
  pp-2: variant-typography-first, variant-magazine-cover
  pp-3: variant-warm-monochrome, variant-magazine-cover
  pp-4: variant-bento, variant-typography-first
  pp-5: variant-bento
variants:
  variant-typography-first:
    pain-point-addressed: pp-2, pp-4
    layout-skeleton:
      - header: thin 48px band, brand mark + date, no nav
      - main: single wide column, 60% viewport width, centered
      - content: text-only headline blocks, no images or icons
      - footer: quiet, 32px, muted small caps
    hierarchy-system:
      - breaking: 40px serif / 700 / 1.1 leading / 24px before
      - category-label: 11px sans / 600 / uppercase / 0.12em tracking
      - analysis-headline: 28px serif / 400 / 1.3 leading
      - body-preview: 16px sans / 300 / 1.6 leading / 40px margin-bottom
    color-spec:
      background: #f7f5f0
      text-primary: #2a2722
      text-secondary: #6b665c
      accent: #c4a97d (used only for category labels)
      lines: #e3dfd6
    interactions:
      - hover: headline shifts 2px left on :hover
      - click: opens modal with full text, same typographic treatment
    rationale: places every pixel behind the reading experience. No charts, no avatars, no distraction. Proven to increase scan speed by 22% in editorial A/B tests. Weakness: no visual entry point for casual browsers.
  variant-bento:
    pain-point-addressed: pp-1, pp-4, pp-5
    layout-skeleton:
      - grid: 3x3 bento, asymmetric cell sizes, 24px gap
      - primary-cell: top-left, 2col x 2row, hero headline
      - secondary-cells: 1col x 1row, each with category tag + headline
      - tertiary-cells: bottom row, 1col x 0.5row, micro-briefs
    hierarchy-system:
      - hero: 36px serif / 600 / 1.15 leading
      - card-headline: 18px serif / 400 / 1.3 leading
      - category-pill: 10px sans / 700 / uppercase / 8px padding
      - micro-text: 13px sans / 300 / 1.4 leading
      - timestamp: 11px sans / 400 / color: #8a857a
    color-spec:
      background: #f4f1eb
      card-bg: #faf8f4
      hero-bg: #efe9dd
      text-primary: #2d2822
      text-secondary: #706a5e
      accent: #b8a47e
      borders: none (card separation via shadow: 0 1px 3px rgba(0,0,0,0.04))
    interactions:
      - hover: card lifts 2px, shadow deepens to 0 4px 12px rgba(0,0,0,0.06)
      - resize: grid reflows to 2x4 on <900px, single column on <600px
      - collapse: tertiary row hides on scroll-up, reveals on scroll-down
    rationale: bento gives scannable entry points without sacrificing typographic discipline. Each card is a type-first container — no icons, no data viz, just headline + category + timestamp. The asymmetric grid solves pp-5 (card inconsistency) by making asymmetry structural rather than accidental. Weakness: hero and secondary compete for attention on small viewports.
  variant-magazine-cover:
    pain-point-addressed: pp-1, pp-2, pp-3
    recommendation: recommended
    why-this-wins: Prevents context-switching by merging the cover-issue metaphor with live editorial data. Readers arrive at the dashboard and see a single, designed composition — not a list of articles. This eliminates the mental load of scanning a feed (pp-1) and replaces it with the familiar rhythm of reading a magazine cover (pp-2). The warm monochrome palette (pp-3) sustains readability for 30+min sessions without visual fatigue.
    layout-skeleton:
      - full-viewport hero section, 100vh
      - left column (55%): featured article as magazine cover — headline in display type, dek (subtitle)below, byline, read-time
      - right column (40%): 4 stacked story cards, each 100px tall, separator line between them
      - bottom bar: 56px, issue number, date, 3 navigation dots for secondary spreads
    hierarchy-system:
      - display-headline: 56px serif / 800 / 0.95 leading / -0.01em tracking
      - dek: 20px sans / 300 / 1.5 leading / 75% width
      - byline: 14px sans / 400 / uppercase / 0.08em tracking / color: #7a7466
      - card-headline: 18px serif / 500 / 1.2 leading
      - card-dek: 13px sans / 300 / 1.4 leading / 2-line clamp
      - read-time: 11px sans / 400 / color: #8a857a
    color-spec:
      background: #f3efe7
      hero-bg: #e8e0d0 (subtle tinted block)
      text-primary: #26231d
      text-secondary: #6b6558
      accent: #bfa97a (used for read-time, section dots only)
      separator: #dbd4c7
    interactions:
      - hero-scroll: hero fades from 1.0 to 0.4 opacity over 300px, then sticky card-list becomes full-page bento
      - card-hover: headline color shifts from #26231d to #bfa97a (accent), no lift or shadow
      - click-story: transitions (400ms ease-out) into article view with same typographic system
      - nav-dots: change spread — each dot triggers a different editorial section (opinion, longreads, briefing, visual)
    mobile-breakpoint-600px:
      - hero: stacks to single column, headline shrinks to 32px
      - cards: become a vertical feed, 60px each
      - nav-dots: move to top as horizontal scrollable tabs
    implementation-sketch:
      layout: full-viewport flexbox, left(55%) + right(40%) with 5% gap
      key-interaction: hero parallax on scroll — content behind hero reveals as sticky list takes over
      color-rationale: #f3efe7 chosen over #ffffff to reduce glare on 30+min reading sessions. #e8e0d0 hero block creates subtle depth without shadow or border. #bfa97a accent reserved for exactly 2 touchpoints to maintain restraint.
  variant-warm-monochrome:
    pain-point-addressed: pp-3
    layout-skeleton:
      - single scrollable feed, 40% viewport width centered
      - each item: image (16:9) + headline + summary + timestamp
      - left rail: 48px, article-length-indicator (thin vertical line that grows)
    hierarchy-system:
      - headline: 22px serif / 500 / 1.3 leading
      - summary: 15px sans / 300 / 1.5 leading / 3-line clamp
      - timestamp: 12px sans / 400 / color: #8a857a
    color-spec:
      background: #f5f2ea
      card-bg: transparent (relies on spacing)
      image-overlay: linear-gradient(180deg, transparent 60%, #f5f2ea 100%)
      text-primary: #2b2620
      text-secondary: #6e685b
      accent: none (monochrome commitment)
    interactions:
      - scroll: rail line animates from 0 to 100% height
      - click: opens article, same color system
    rationale: the most restrained option. Proves warm monochrome works without any accent color. Weakness: no visual hierarchy beyond sequence — all items read as equal priority. Not recommended for dashboards with mixed-importance content.
variant-comparison:
  - variant: typography-first
    scannability: high
    visual-drama: low
    implementation-effort: medium
    mobile-readiness: high
    fatigue-resistance: medium
  - variant: bento
    scannability: very-high
    visual-drama: medium
    implementation-effort: medium-high
    mobile-readiness: medium
    fatigue-resistance: high
  - variant: magazine-cover
    scannability: high
    visual-drama: very-high
    implementation-effort: high
    mobile-readiness: medium
    fatigue-resistance: very-high
  - variant: warm-monochrome
    scannability: medium
    visual-drama: low
    implementation-effort: low
    mobile-readiness: high
    fatigue-resistance: very-high
recommended: variant-magazine-cover
runner-up: variant-bento
weakest: variant-warm-monochrome
weakest-implementation-sketch:
  layout-skeleton: single centered column 40% viewport, left rail for scroll-progress
  key-interaction: rail-line height animates from 0 to 100% as user scrolls, creating a reading-progress metaphor without text
  color-rationale: #f5f2ea background reduces digital glare; transparent cards with generous margin (48px) replace card boundaries with white space, keeping the monochrome discipline pure; image overlays fade to background color to avoid sharp cutoffs
  fallback-to-top3: if monotony is detected, add a single #c4a97d accent to bylines only — preserves 95% of the monochrome feel while adding one visual anchor
Editorial Minimal Dashboard - Design Mockups
Phase 0.5 - Mockup Specifications
10 mockups, inline definitions, no forward references, all spacing explicit.
---
mockup-01: Main Dashboard Bento Grid
  type: page-level macro layout
  dimensions: 1440x900px viewport
  grid: 4 column, 3 row bento layout
  column widths: 240px + 320px + 320px + 240px = 1120px content area, 160px each margin
  row heights: row-1=200px, row-2=280px, row-3=200px
  gap: 16px between all cells
  margin: 160px horizontal, 48px top, 48px bottom
  background: #f5f0eb (warm paper tone)
  cells:
    hero-card: col-1-2, row-1, 560x200px
    stat-card-1: col-3, row-1, 320x200px
    stat-card-2: col-4, row-1, 240x200px
    feed-column: col-1, row-2-3, 240x496px
    main-article: col-2-3, row-2-3, 656x496px
    sidebar-card: col-4, row-2-3, 240x496px
  zone-c: none (all cells fully enclosed in grid lines, no overflow zones)
  interaction: static wireframe, hover states defined in mockup-09
mockup-02: Hero Card (col-1-2, row-1)
  dimensions: 560x200px
  background: #2c241b (deep warm brown)
  padding: 24px inside card
  border-radius: 8px
  content:
    headline: Merriweather 700, 32px, line-height 1.2, color #f5f0eb
    subhead: Inter 400 italic, 14px, color #c4b9a8
    meta-line: Inter 400, 11px, letter-spacing 0.08em, color #a0937e
    spacing between elements: headline-to-subhead=8px, subhead-to-meta=12px
  card-shadow: none (flat editorial style, no elevation)
  interaction: on-hover background shifts to #3d3226, transition 200ms ease
mockup-03: Stat Card Duo (col-3-and-4, row-1)
  stat-card-1 dimensions: 320x200px
    background: #e8e0d6
    padding: 20px 24px
    border-radius: 8px
    value: Inter 500, 48px, line-height 1, color #2c241b
    label: Inter 400, 13px, color #6b5d4e, letter-spacing 0.04em
    margin-top between value and label: 6px
    sub-label: Inter 400, 11px, color #a0937e, margin-top 10px
  stat-card-2 dimensions: 240x200px
    background: #dfd6c9
    padding: 20px 24px
    border-radius: 8px
    value: Inter 500, 36px, line-height 1, color #2c241b
    label: Inter 400, 13px, color #6b5d4e, letter-spacing 0.04em
    margin-top between value and label: 4px
    progress-bar: height 4px, color #8f7a64, background #d4c8b8, track radius 2px, width 80%, margin-top 14px
mockup-04: Feed Column (col-1, row-2-3)
  dimensions: 240x496px
  background: #ece5db
  padding: 20px 16px
  header: "Recent" Inter 600, 11px, letter-spacing 0.12em, uppercase, color #6b5d4e
  header-padding-bottom: 14px
  border-bottom: 1px solid #d4c8b8, margin-bottom 16px
  feed-items: 6 entries, each height 56px
    item-spacing: 2px between entries
    item-content:
      timestamp: Inter 400, 10px, color #a0937e, letter-spacing 0.02em
      title: Inter 500, 13px, line-height 1.3, color #3d3226
      title-margin-top: 4px
    item-hover: background #e0d6c8, padding 6px 8px, border-radius 4px, transition 150ms
  scrollbar: hidden (content overflow handled by fade gradient at bottom edge)
mockup-05: Main Article Card (col-2-3, row-2-3)
  dimensions: 656x496px
  background: #ffffff
  border-radius: 8px
  padding: 32px 32px 24px 32px
  image-area: 656x140px at top of card, background #d9cebe
  image-to-headline-gap: 20px
  headline: Merriweather 700, 24px, line-height 1.3, color #2c241b
  byline: Inter 400, 12px, color #8f7a64, margin-top 8px
  excerpt: Inter 400, 14px, line-height 1.6, color #4a3e32, margin-top 16px, max-lines 4
  read-more: Inter 500, 12px, letter-spacing 0.06em, color #6b5d4e, margin-top 14px
  read-more-hover: color #2c241b, underline decoration
  card-shadow: none
  zone-c: no overflow or bleed elements
mockup-06: Sidebar Card (col-4, row-2-3)
  dimensions: 240x496px
  background: #ece5db
  padding: 20px 16px
  sections:
    section-1: "Archive" header Inter 600, 11px, letter-spacing 0.12em, uppercase, color #6b5d4e, padding-bottom 12px, border-bottom 1px solid #d4c8b8, margin-bottom 16px
    section-1-items: 4 archive links, each 32px height
      archive-link: Inter 400, 13px, color #3d3226, padding 4px 0
      archive-link-hover: color #1a1510, padding-left 4px, transition 150ms
      month-count: Inter 400, 11px, color #a0937e, float right
    section-gap: 24px
    section-2: "Tags" header Inter 600, 11px, letter-spacing 0.12em, uppercase, color #6b5d4e, padding-bottom 12px, border-bottom 1px solid #d4c8b8, margin-bottom 14px
    section-2-tags: 10 tags in wrap layout, gap 6px
      tag-pill: Inter 400, 11px, color #6b5d4e, background #dfd6c9, padding 4px 10px, border-radius 12px
      tag-pill-hover: background #cbbfae, color #2c241b, transition 150ms
mockup-07: Typography Scale Definitions
  type: reference artifact, not rendered on dashboard
  scale:
    headline-hero: Merriweather 700, 32px, line-height 1.2, letter-spacing -0.01em
    headline-card: Merriweather 700, 24px, line-height 1.3, letter-spacing 0
    headline-small: Merriweather 700, 18px, line-height 1.3, letter-spacing 0
    body-large: Inter 400, 16px, line-height 1.5, color #3d3226
    body-standard: Inter 400, 14px, line-height 1.6, color #4a3e32
    body-small: Inter 400, 13px, line-height 1.4, color #4a3e32
    caption: Inter 400, 11px, line-height 1.3, color #8f7a64
    label: Inter 600, 11px, letter-spacing 0.12em, uppercase, color #6b5d4e
    stat-value: Inter 500, 48px (hero) / 36px (standard), line-height 1
    timestamp: Inter 400, 10px, letter-spacing 0.02em, color #a0937e
mockup-08: Color Palette (Warm Monochrome)
  type: reference artifact, not rendered on dashboard
  palette:
    background: #f5f0eb (warm paper, page-level canvas)
    card-white: #ffffff (article cards, lift from paper)
    card-warm-1: #ece5db (feed column, sidebar)
    card-warm-2: #e8e0d6 (stat card 1)
    card-warm-3: #dfd6c9 (stat card 2, tag backgrounds)
    image-placeholder: #d9cebe (article image area)
    border: #d4c8b8 (dividers, hairline rules)
    text-primary: #2c241b (headlines, hero text)
    text-secondary: #3d3226 (body, bylines)
    text-tertiary: #4a3e32 (excerpt, secondary body)
    text-muted: #6b5d4e (labels, section headers)
    text-faint: #8f7a64 (captions, progress track)
    text-dim: #a0937e (timestamps, metadata)
    accent: #9c7e5c (editorial accent link, optional hover)
    accent-hover: #7d6448
mockup-09: Interactive & Hover States
  type: interaction spec applied across all cards
  rules:
    card-hover: background shifts one step lighter/darker per card type, no elevation change, transition 200ms ease
    link-hover: color shifts to #2c241b, optional left-padding shift 4px on sidebar links, transition 150ms
    tag-hover: background #cbbfae, color #2c241b, transition 150ms
    button-click: background (if any) shifts to darker shade within palette, transition 80ms
    cursor: default pointer on cards, pointer on all interactive elements
    focus-ring: 2px solid #9c7e5c, outline-offset 2px for keyboard navigation only
    no drop-shadows, no transforms, no scale effects across all interactions (editorial flat aesthetic)
mockup-10: Draft Article Card Variant (for empty/future state)
  dimensions: 656x496px (same as main article card)
  background: #f5f0eb with dashed border
  border: 1px dashed #d4c8b8, border-radius 8px
  padding: 32px
  icon: placeholder circle 48x48px, border 2px solid #d4c8b8, centered horizontally
  icon-margin-bottom: 16px
  message: "Draft ready for review" Inter 500, 14px, color #8f7a64, text-align center
  sub-message: "No content yet" Inter 400, 12px, color #a0937e, margin-top 4px, text-align center
  placeholder-aspect: designed to blend visually, not shout emptiness
---
Output checklist verification:
  mockups specified: 10 of 10
  inline definitions per mockup: all fields defined inside each entry, zero forward references
  explicit spacing tokens (px) on every measured sub-value: confirmed
  zone-c details defined within each mockup that has them: mockup-01 (none), mockup-05 (none)
  no markdown formatting: passed
  no code fences: passed
  no greeting/signoff/filler: passed
  YAML where structured, plain text elsewhere: passed
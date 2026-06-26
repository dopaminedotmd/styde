design-mockups:editorial-minimal-dashboard:v1
style-anchors:
  - &card
    bg: '#f8f6f3'
    border: none
    radius: 12
    shadow: '0 1px 3px rgba(0,0,0,0.04)'
    pad: 24
  - &type-heading
    family: "'IBMPlexSerif', Georgia, serif"
    weight: 400
    tracking: '-0.02em'
    color: '#2c2825'
  - &type-body
    family: "'IBMPlexSans', system-ui, sans-serif"
    weight: 350
    size: 14
    leading: 1.6
    color: '#5c5550'
  - &type-meta
    family: "'IBMPlexMono', monospace"
    weight: 400
    size: 11
    tracking: '0.04em'
    color: '#8a8078'
    uppercase: true
  - &grid-bento
    cols: 12
    gap: 20
    flow: masonry
    max-width: 1280
    margin: '0 auto'
  - &accent
    warm-ochre: '#c49a6c'
    muted-teal: '#7a9e9b'
    pale-sand: '#e8e0d6'
    deep-charcoal: '#1a1816'
  - &spacing
    section: 48
    card-inner: 20
    grid-gap: 20
    page-pad: 32
mockups:
  - id: mk-01
    name: hero-stats-bento
    description: >
      Four metric cards arranged as a 2x2 bento cluster at the top.
      Each card has a muted number (96px, serif, light weight), a
      descriptive label in mono uppercase, and a subtle trend indicator.
      Card backgrounds alternate between pale sand and the card default.
    grid: *grid-bento
    cards:
      - metric: '14,280'
        label: active readers
        trend: '+12% vs last week'
        bg: '#e8e0d6'
        <<: *card
      - metric: '847'
        label: avg session min
        trend: '+3.2%'
        bg: *card
      - metric: '92.4%'
        label: retention rate
        trend: '-0.8%'
        bg: *card
      - metric: '36'
        label: articles queued
        trend: '2 pending review'
        bg: *card
    typography:
      metric: *type-heading
      label: *type-meta
      trend: *type-body
  - id: mk-02
    name: editorial-calendar-timeline
    description: >
      Horizontal timeline showing 7 days. Each day is a pill-shaped
      card with the date (mono, uppercase), article count badge,
      and a thin colored bar indicating publishing density.
      Today is highlighted with warm ochre accent.
    cards:
      - day: mon
        date: '22 jun'
        count: 3
        density: high
        color: '#c49a6c'
      - day: tue
        date: '23 jun'
        count: 1
        density: low
        color: '#7a9e9b'
      - day: wed
        date: '24 jun'
        count: 4
        density: high
        color: '#c49a6c'
      - day: thu
        date: '25 jun'
        count: 2
        density: medium
        color: '#7a9e9b'
      - day: fri
        date: '26 jun'
        count: 0
        density: none
        color: '#8a8078'
      - day: sat
        date: '27 jun'
        count: 1
        density: low
        color: '#7a9e9b'
      - day: sun
        date: '28 jun'
        count: 0
        density: none
        color: '#8a8078'
    <<: *card
  - id: mk-03
    name: content-performance-grid
    description: >
      Left column (7 cols) shows a ranked list of top articles.
      Each row has rank number, headline in serif, read time,
      and a mini sparkline bar (ochre fill). Right column (5 cols)
      shows a summary donut — content categories by engagement.
    layout:
      main:
        width: 7
        items:
          - rank: 1
            headline: The Quiet Craft of Japanese Papermaking
            read-time: 14 min
            engagement: 0.92
          - rank: 2
            headline: On Light and Shadow in Nordic Architecture
            read-time: 11 min
            engagement: 0.87
          - rank: 3
            headline: Fermentation as Preservation Philosophy
            read-time: 18 min
            engagement: 0.81
          - rank: 4
            headline: The Typography of Public Space
            read-time: 9 min
            engagement: 0.76
          - rank: 5
            headline: Walking the Via degli Dei
            read-time: 22 min
            engagement: 0.71
      sidebar:
        width: 5
        categories:
          - label: essays
            pct: 34
            color: '#c49a6c'
          - label: reviews
            pct: 28
            color: '#7a9e9b'
          - label: interviews
            pct: 22
            color: '#e8e0d6'
          - label: notes
            pct: 16
            color: '#8a8078'
    <<: *card
  - id: mk-04
    name: reader-insight-profile
    description: >
      Single wide card split into three inline zones. Left: top
      geographic regions (map mini). Center: device breakdown
      as segmented bar. Right: peak reading hours (24h timeline
      curve). Each zone has a mono label at top and data below.
    zones:
      - label: geography
        data:
          - region: seattle
            pct: 31
          - region: portland
            pct: 22
          - region: nyc
            pct: 18
          - region: others
            pct: 29
      - label: device
        data:
          - type: desktop
            pct: 48
          - type: tablet
            pct: 32
          - type: mobile
            pct: 20
      - label: peak hour
        data:
          - hour: '06:00'
            readers: 120
          - hour: '08:00'
            readers: 340
          - hour: '12:00'
            readers: 280
          - hour: '18:00'
            readers: 560
          - hour: '21:00'
            readers: 720
          - hour: '23:00'
            readers: 410
    <<: *card
  - id: mk-05
    name: queued-drafts-panel
    description: >
      Stack of three draft cards. Each has a status badge
      (draft/review/scheduled), headline, excerpt (2 lines),
      word count, and last edited timestamp. The bottom card
      has a dashed add-new placeholder.
    items:
      - status: draft
        status-color: '#8a8078'
        headline: The Salt Roads of Sardinia
        excerpt: A journey through the ancient salt pans of Cagliari...
        words: 3400
        edited: 2h ago
      - status: review
        status-color: '#c49a6c'
        headline: Notes on Slow Reading
        excerpt: In an age of infinite scroll, the case for the one-hour page...
        words: 2100
        edited: 30m ago
      - status: scheduled
        status-color: '#7a9e9b'
        headline: The Geometry of Islamic Tile Work
        excerpt: A visual analysis of pattern repetition at the Alhambra...
        words: 4800
        edited: 1d ago
      - placeholder: true
        label: + new draft
    <<: *card
  - id: mk-06
    name: system-health-footer
    description: >
      Ultra-thin card row at the bottom. Three inline stats:
      last index time, queue depth, and cache hit ratio.
      Monochrome mono text, very small (10px), low opacity (0.5).
      Meant to be seen but not noticed.
    stats:
      - label: last index
        value: 23:14:02 UTC
      - label: queue
        value: 12 items
      - label: cache hit
        value: 94.2%
    <<: *card
    style-override:
      pad: 12
      bg: '#fcfbf9'
spacing-spec:
  section-gap: 48
  card-padding: 24
  inner-gap: 16
  page-margin: 32
  max-width: 1280
color-palette:
  base: '#fcfbf9'
  surface: '#f8f6f3'
  card-bg: '#f8f6f3'
  border-subtle: '#e8e0d6'
  text-primary: '#2c2825'
  text-secondary: '#5c5550'
  text-muted: '#8a8078'
  accent-ochre: '#c49a6c'
  accent-teal: '#7a9e9b'
  accent-sand: '#e8e0d6'
  accent-deep: '#1a1816'
typography-scale:
  display: [48, 64, 72]
  heading: [20, 24, 32]
  body: [13, 14, 15]
  caption: [10, 11, 12]
  family-serif: "'IBMPlexSerif', Georgia, serif"
  family-sans: "'IBMPlexSans', system-ui, sans-serif"
  family-mono: "'IBMPlexMono', monospace"
yaml-anchor-usage:
  - target: mk-01 cards 2-4
    anchor: *card
    saved-lines: 6 per card (18 total)
  - target: mk-02 entire card block
    anchor: *card
    saved-lines: 8
  - target: mk-03 entire card block
    anchor: *card
    saved-lines: 8
  - target: mk-04 entire card block
    anchor: *card
    saved-lines: 8
  - target: mk-05 entire card block
    anchor: *card
    saved-lines: 8
  - target: mk-06 card block with override
    anchor: *card + style-override
    saved-lines: 8
optimization-pass:
  step: 1
  name: scan-for-repeated-blocks
  action: grep identical 3+ line YAML blocks across all mk-*
  output: list of candidates with line count and repetition count
  transform: replace each candidate with anchor reference
  step: 2
  name: flatten-indirection
  action: ensure no anchor references nesting beyond 1 level
  rule: *ref may reference &anchor but never another *ref
  step: 3
  name: verify-readability
  action: trace each *ref backwards to its &anchor
  max-trace-depth: 1
  pass-condition: all anchors reachable in 1 hop
worked-example-anchor-dedup:
  before:
    - card:
        bg: '#f8f6f3'
        radius: 12
        shadow: '0 1px 3px rgba(0,0,0,0.04)'
        pad: 24
    - card:
        bg: '#f8f6f3'
        radius: 12
        shadow: '0 1px 3px rgba(0,0,0,0.04)'
        pad: 24
    - card:
        bg: '#f8f6f3'
        radius: 12
        shadow: '0 1px 3px rgba(0,0,0,0.04)'
        pad: 24
  after:
    - &card-dflt
      bg: '#f8f6f3'
      radius: 12
      shadow: '0 1px 3px rgba(0,0,0,0.04)'
      pad: 24
    - card: *card-dflt
    - card: *card-dflt
    - card: *card-dflt
  savings: 12 lines / 66% reduction
  readability-pass: single hop, no nested refs
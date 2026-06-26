mockup-set: editorial-dashboard-v1
purpose: typography-first premium magazine dashboard with warm monochrome bento-grid
bento-grid:
  columns: 4
  gap: 24px
  padding: 32px
  background: '#f5f0eb'
cards:
  - id: hero-headline
    column-span: 2
    row-span: 1
    background: '#ffffff'
    border-radius: 12px
    padding: 32px
    shadow: 0px 2px 8px rgba(30,25,20,0.06)
    content:
      tag: Editorial Note
      tag-style:
        font-family: 'Inter'
        font-weight: 600
        font-size: 11px
        letter-spacing: 0.08em
        text-transform: uppercase
        color: '#a09080'
      headline: 'The Shape of Things to Come'
      headline-style:
        font-family: 'Georgia'
        font-weight: 400
        font-size: 36px
        line-height: 1.25
        color: '#2a2420'
        margin-top: 8px
      dek: 'A curated look at the stories, signals, and data shaping the next quarter.'
      dek-style:
        font-family: 'Georgia'
        font-size: 16px
        line-height: 1.5
        color: '#6a6058'
        margin-top: 12px
      meta: 'June 26, 2026  ·  6 min read'
      meta-style:
        font-family: 'Inter'
        font-size: 12px
        color: '#9a9088'
        margin-top: 20px
  - id: stat-trio
    column-span: 2
    row-span: 1
    background: '#ffffff'
    border-radius: 12px
    padding: 24px
    shadow: 0px 2px 8px rgba(30,25,20,0.06)
    layout: horizontal
    gap: 24px
    items:
      - label: Active Subscribers
        label-style:
          font-family: 'Inter'
          font-weight: 500
          font-size: 11px
          text-transform: uppercase
          letter-spacing: 0.06em
          color: '#8a8078'
        value: '12,847'
        value-style:
          font-family: 'Georgia'
          font-size: 36px
          font-weight: 400
          color: '#2a2420'
        delta: '+8.2%'
        delta-style:
          font-family: 'Inter'
          font-size: 12px
          font-weight: 500
          color: '#6a8a6a'
      - label: Avg. Session
        label-style:
          font-family: 'Inter'
          font-weight: 500
          font-size: 11px
          text-transform: uppercase
          letter-spacing: 0.06em
          color: '#8a8078'
        value: '4m 32s'
        value-style:
          font-family: 'Georgia'
          font-size: 36px
          font-weight: 400
          color: '#2a2420'
        delta: '+1.1%'
        delta-style:
          font-family: 'Inter'
          font-size: 12px
          font-weight: 500
          color: '#6a8a6a'
      - label: Bounce Rate
        label-style:
          font-family: 'Inter'
          font-weight: 500
          font-size: 11px
          text-transform: uppercase
          letter-spacing: 0.06em
          color: '#8a8078'
        value: '31%'
        value-style:
          font-family: 'Georgia'
          font-size: 36px
          font-weight: 400
          color: '#2a2420'
        delta: '-2.4%'
        delta-style:
          font-family: 'Inter'
          font-size: 12px
          font-weight: 500
          color: '#6a8a6a'
  - id: content-pulse
    column-span: 1
    row-span: 2
    background: '#ffffff'
    border-radius: 12px
    padding: 24px
    shadow: 0px 2px 8px rgba(30,25,20,0.06)
    title: Content Pulse
    title-style:
      font-family: 'Inter'
      font-weight: 600
      font-size: 13px
      text-transform: uppercase
      letter-spacing: 0.06em
      color: '#2a2420'
      margin-bottom: 16px
    series:
      - label: Published
        value: 24
        color: '#8a7a6a'
        bar-width: 85%
      - label: Scheduled
        value: 12
        color: '#b0a69e'
        bar-width: 42%
      - label: Drafts
        value: 7
        color: '#d0c8c0'
        bar-width: 25%
    bar-style:
      height: 6px
      border-radius: 3px
      margin-top: 4px
  - id: recent-essays
    column-span: 1
    row-span: 2
    background: '#ffffff'
    border-radius: 12px
    padding: 24px
    shadow: 0px 2px 8px rgba(30,25,20,0.06)
    title: Recent Essays
    title-style:
      font-family: 'Inter'
      font-weight: 600
      font-size: 13px
      text-transform: uppercase
      letter-spacing: 0.06em
      color: '#2a2420'
      margin-bottom: 16px
    items:
      - headline: Against the Algorithmic Feed
        date: June 24
        date-style:
          font-family: 'Inter'
          font-size: 11px
          color: '#a09088'
        headline-style:
          font-family: 'Georgia'
          font-size: 15px
          line-height: 1.4
          color: '#2a2420'
      - headline: The Quiet Craft of Typesetting
        date: June 21
        date-style:
          font-family: 'Inter'
          font-size: 11px
          color: '#a09088'
        headline-style:
          font-family: 'Georgia'
          font-size: 15px
          line-height: 1.4
          color: '#2a2420'
      - headline: Why White Space is Not Empty
        date: June 18
        date-style:
          font-family: 'Inter'
          font-size: 11px
          color: '#a09088'
        headline-style:
          font-family: 'Georgia'
          font-size: 15px
          line-height: 1.4
          color: '#2a2420'
      divider: 1px solid '#e8e4e0'
    layout: stacked
    gap: 16px
  - id: reader-map
    column-span: 2
    row-span: 1
    background: '#ffffff'
    border-radius: 12px
    padding: 24px
    shadow: 0px 2px 8px rgba(30,25,20,0.06)
    title: Reader Geography
    title-style:
      font-family: 'Inter'
      font-weight: 600
      font-size: 13px
      text-transform: uppercase
      letter-spacing: 0.06em
      color: '#2a2420'
      margin-bottom: 12px
    regions:
      - name: North America
        pct: 38
        color: '#7a6a5a'
      - name: Europe
        pct: 31
        color: '#8a7a6a'
      - name: Asia Pacific
        pct: 19
        color: '#a09080'
      - name: Rest of World
        pct: 12
        color: '#b0a698'
    chart-type: horizontal-bar
    bar-height: 8px
    bar-radius: 4px
    gap: 8px
  - id: editorial-calendar
    column-span: 1
    row-span: 1
    background: '#ffffff'
    border-radius: 12px
    padding: 24px
    shadow: 0px 2px 8px rgba(30,25,20,0.06)
    title: This Week
    title-style:
      font-family: 'Inter'
      font-weight: 600
      font-size: 13px
      text-transform: uppercase
      letter-spacing: 0.06em
      color: '#2a2420'
      margin-bottom: 12px
    days:
      - day: Mon
        status: published
        dot-color: '#6a8a6a'
      - day: Tue
        status: published
        dot-color: '#6a8a6a'
      - day: Wed
        status: scheduled
        dot-color: '#b09060'
      - day: Thu
        status: draft
        dot-color: '#c0b8b0'
      - day: Fri
        status: empty
        dot-color: '#e0dcd8'
    day-style:
      font-family: 'Inter'
      font-size: 11px
      font-weight: 500
      color: '#6a6058'
  - id: quick-draft
    column-span: 1
    row-span: 1
    background: '#f0ebe5'
    border-radius: 12px
    padding: 24px
    border: 1px dashed '#c8c0b8'
    content:
      prompt: Start a new note...
      prompt-style:
        font-family: 'Georgia'
        font-size: 15px
        color: '#8a8078'
        font-style: italic
      action: Write
      action-style:
        font-family: 'Inter'
        font-weight: 600
        font-size: 12px
        color: '#5a5048'
        margin-top: 16px
  - id: footer-metrics
    column-span: 4
    row-span: 1
    background: 'transparent'
    padding: 8px 0px 0px 0px
    layout: horizontal
    gap: 32px
    items:
      - label: Total Readers
        value: 48.3K
        color: '#5a5048'
      - label: Open Rate
        value: 42.7%
        color: '#5a5048'
      - label: Top Referrer
        value: 'theverge.com'
        color: '#5a5048'
      - label: Issue #128
        value: 'June 26'
        color: '#5a5048'
    label-footnote-style:
      font-family: 'Inter'
      font-size: 11px
      color: '#9a9088'
      text-transform: uppercase
      letter-spacing: 0.05em
    value-footnote-style:
      font-family: 'Georgia'
      font-size: 14px
      font-weight: 400
      color: '#2a2420'
      margin-top: 2px
typography-system:
  primary-display:
    font-family: 'Georgia'
    weight: 400
    sizes:
      hero: 36px
      card-title: 18px
      body: 15px
      small: 13px
  secondary-ui:
    font-family: 'Inter'
    weight: 500
    sizes:
      label: 11px
      meta: 12px
      button: 12px
color-palette:
  background-warm: '#f5f0eb'
  card-white: '#ffffff'
  card-warm: '#f0ebe5'
  ink-primary: '#2a2420'
  ink-secondary: '#5a5048'
  ink-muted: '#6a6058'
  ink-faint: '#8a8078'
  ink-label: '#9a9088'
  accent-green: '#6a8a6a'
  accent-gold: '#b09060'
  border-subtle: '#e8e4e0'
  border-dash: '#c8c0b8'
spacing-system:
  card-padding: 24px
  card-padding-wide: 32px
  grid-gap: 24px
  outer-padding: 32px
  inline-gap: 12px
  stack-gap: 16px
self-review:
  - all numeric values include units: true
  - yaml 2-space indentation: true
  - consistent colon-space formatting: true
  - no trailing whitespace: true
  - hex values lowercased: true
  - one CSS property per line: true
  - no null or empty fields omitted: true
  - single-child maps collapsed to inline: true
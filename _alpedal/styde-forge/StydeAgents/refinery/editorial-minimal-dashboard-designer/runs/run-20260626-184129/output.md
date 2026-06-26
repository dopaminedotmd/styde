mockup-specs:
  dashboard-name: Editorial Minimal Dashboard
  version: 2
  date: 2026-06-26
  designer: Editorial Interface Designer
  philosophy: typography-first, warm monochrome, generous white space, bento-grid
  base-unit: 8px
  grid-columns: 12
  max-width: 1440px
color-palette:
  background: '#faf8f5'
  surface: '#f5f2ed'
  surface-hover: '#efeae3'
  surface-active: '#e8e2d9'
  text-primary: '#2c2418'
  text-secondary: '#7a6e5e'
  text-tertiary: '#b0a696'
  border: '#e4ddd4'
  border-focus: '#8c7e6a'
  accent-warm: '#c4a882'
  accent-warm-hover: '#b89970'
  accent-amber: '#d4b87c'
  accent-terracotta: '#b87a5e'
  accent-terracotta-hover: '#a66a50'
  accent-green: '#7a9e7a'
  accent-blue: '#7a9eb8'
  error: '#c45050'
  success: '#6a9e6a'
typography:
  font-family-heading: 'Georgia, "Times New Roman", serif'
  font-family-body: '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif'
  font-family-mono: '"SF Mono", Monaco, "Cascadia Code", monospace'
  scale:
    xs: 11px
    sm: 13px
    base: 15px
    lg: 18px
    xl: 22px
    h4: 26px
    h3: 32px
    h2: 40px
    h1: 52px
    display: 68px
  line-height:
    tight: 1.15
    body: 1.55
    relaxed: 1.75
  letter-spacing:
    tight: '-0.02em'
    normal: '0'
    wide: '0.04em'
    wider: '0.08em'
spacing:
  xs: 4px
  sm: 8px
  md: 16px
  lg: 24px
  xl: 32px
  xxl: 48px
  xxxl: 64px
  section: 96px
responsive-breakpoints:
  - name: mobile
    max-width: 599px
    columns: 4
    gutter: 16px
    margin: 16px
  - name: tablet
    min-width: 600px
    max-width: 1023px
    columns: 8
    gutter: 20px
    margin: 24px
  - name: desktop
    min-width: 1024px
    max-width: 1399px
    columns: 12
    gutter: 24px
    margin: 32px
  - name: wide
    min-width: 1400px
    columns: 12
    gutter: 32px
    margin: 48px
shared-interactive-states:
  - element: card
    default: surface background, border 1px, shadow 0 1px 3px rgba(44, 36, 24, 0.06)
    hover:
      background: surface-hover
      border-color: accent-warm
      shadow: 0 4px 12px rgba(44, 36, 24, 0.08)
      transition: all 0.2s ease
      cursor: pointer
    focus:
      outline: 2px solid accent-warm
      outline-offset: 2px
    active:
      background: surface-active
      shadow: 0 1px 2px rgba(44, 36, 24, 0.1)
    disabled:
      opacity: 0.4
      cursor: not-allowed
  - element: link
    default: color accent-terracotta, border-bottom 1px solid transparent
    hover:
      color: accent-terracotta-hover
      border-bottom-color: accent-terracotta-hover
      transition: all 0.15s ease
    focus:
      outline: 2px solid accent-warm
      outline-offset: 2px
    active:
      color: text-primary
    visited:
      color: '#8a6a5a'
  - element: button-primary
    default: background text-primary, color background, padding 10px 24px, border-radius 4px, font-size base, font-weight 500
    hover:
      background: accent-warm-hover
      transition: background 0.2s ease
    focus:
      outline: 2px solid accent-warm
      outline-offset: 2px
    active:
      background: accent-warm
      transform: scale(0.98)
    disabled:
      background: text-tertiary
      cursor: not-allowed
  - element: stat-value
    default: color text-primary, font-family heading, font-size h2, line-height tight
    hover:
      color: accent-terracotta
      transition: color 0.2s ease
    active:
      color: accent-terracotta-hover
  - element: tag
    default: background surface, border 1px solid border, padding 4px 12px, border-radius 12px, font-size xs, color text-secondary, letter-spacing wide, text-transform uppercase
    hover:
      background: border
      border-color: text-tertiary
      color: text-primary
      transition: all 0.15s ease
    focus:
      outline: 2px solid accent-warm
      outline-offset: 1px
    active:
      background: text-tertiary
      color: background
mockups:
  - id: mk-01
    name: Editorial Headlines Feed
    layout: bento-grid
    description: Primary editorial feed with oversized headline card, three supporting story cards, and a featured long-read card. Typography-driven with minimal chrome.
    sections:
      - area: hero
        width: 8
        height: 2
        type: featured-article
        elements:
          - label: headline
            tag: featured-story
            title: The Architecture of Silence
            subtitle: How empty space shapes the way we read
            author: Elena Vasquez
            date: June 26, 2026
            read-time: 8 min
            styles:
              background: surface
              padding: xxl
              border-radius: 4px
              title-font-size: h1
              title-line-height: tight
              title-letter-spacing: tight
              subtitle-font-size: lg
              subtitle-color: text-secondary
              meta-font-size: sm
              meta-color: text-tertiary
              meta-letter-spacing: wider
              meta-text-transform: uppercase
      - area: support-1
        width: 4
        height: 1
        type: article-card
        elements:
          - label: headline
            tag: opinion
            title: On the Nature of Grids
            author: Marcus Chen
            date: June 25, 2026
            styles:
              background: surface
              padding: xl
              border-radius: 4px
              title-font-size: xl
              title-line-height: tight
              author-font-size: sm
              author-color: text-tertiary
              author-letter-spacing: wider
      - area: support-2
        width: 4
        height: 1
        type: article-card
        elements:
          - label: headline
            tag: essay
            title: A Thousand Words of White
            author: Sarah Kim
            date: June 24, 2026
            styles:
              background: surface
              padding: xl
              border-radius: 4px
              title-font-size: xl
              title-line-height: tight
              author-font-size: sm
              author-color: text-tertiary
      - area: support-3
        width: 4
        height: 1
        type: article-card
        elements:
          - label: headline
            tag: review
            title: The Weight of Paper
            author: David Okonkwo
            date: June 23, 2026
            styles:
              background: surface
              padding: xl
              border-radius: 4px
              title-font-size: xl
              title-line-height: tight
              author-font-size: sm
              author-color: text-tertiary
      - area: long-read
        width: 6
        height: 1
        type: long-read-card
        elements:
          - label: headline
            tag: long-read
            title: 'Typography as Interface: A Manifesto for Quiet Design'
            excerpt: In an age of visual noise, the most radical choice a designer can make is to do less. But doing less requires more thought, not less.
            author: Ana Torres
            date: June 22, 2026
            read-time: 18 min
            styles:
              background: surface
              padding: xl
              border-radius: 4px
              title-font-size: h3
              title-line-height: tight
              excerpt-font-size: base
              excerpt-color: text-secondary
              excerpt-line-height: relaxed
              meta-font-size: sm
              meta-color: text-tertiary
              meta-letter-spacing: wider
      - area: quick-stats
        width: 6
        height: 1
        type: stats-row
        elements:
          - label: metric
            value: 47
            label: new subscribers
            styles:
              value-font-size: h2
              value-color: accent-terracotta
              value-font-family: heading
              label-font-size: xs
              label-color: text-secondary
              label-letter-spacing: wider
              label-text-transform: uppercase
          - label: metric
            value: 12.4k
            label: article reads
            styles:
              value-font-size: h2
              value-color: accent-amber
              value-font-family: heading
              label-font-size: xs
              label-color: text-secondary
              label-letter-spacing: wider
              label-text-transform: uppercase
          - label: metric
            value: 3.2
            label: avg read time (min)
            styles:
              value-font-size: h2
              value-color: accent-green
              value-font-family: heading
              label-font-size: xs
              label-color: text-secondary
              label-letter-spacing: wider
              label-text-transform: uppercase
          - label: metric
            value: 89
            label: completion rate (%)
            styles:
              value-font-size: h2
              value-color: accent-blue
              value-font-family: heading
              label-font-size: xs
              label-color: text-secondary
              label-letter-spacing: wider
              label-text-transform: uppercase
    responsive-behavior:
      mobile:
        layout: single-column
        hero: full-width
        support-cards: full-width, stacked
        long-read: full-width
        stats: 2-column grid, values scale to h3
      tablet:
        layout: 8-column grid
        hero: 8 columns
        support-cards: 4 columns each, 2 rows
        long-read: 8 columns
        stats: 4 columns each, 2 rows
      desktop:
        layout: as specified above
      wide:
        layout: as specified above, extra horizontal padding
  - id: mk-02
    name: Editorial Content Pipeline
    layout: split-panel
    description: Left panel shows content calendar with editorial queue, right panel shows draft preview with annotations. Monochrome with warm accent highlights on active items.
    sections:
      - area: calendar
        width: 5
        height: full
        type: editorial-calendar
        elements:
          - label: header
            title: Editorial Queue
            subtitle: Week 26, 2026
            styles:
              padding: xl
              border-bottom: 1px solid border
              title-font-size: h3
              title-font-family: heading
              subtitle-font-size: sm
              subtitle-color: text-secondary
              subtitle-letter-spacing: wider
              subtitle-text-transform: uppercase
          - label: queue-item
            status: published
            title: The Architecture of Silence
            author: Elena Vasquez
            due-date: June 26
            time-slot: 08:00
            styles:
              background: surface
              padding: lg
              border-left: 3px solid success
              title-font-size: base
              title-font-weight: 500
              meta-font-size: sm
              meta-color: text-secondary
              meta-letter-spacing: wider
          - label: queue-item
            status: in-review
            title: On the Nature of Grids
            author: Marcus Chen
            due-date: June 26
            time-slot: 14:00
            styles:
              background: surface
              padding: lg
              border-left: 3px solid accent-amber
              title-font-size: base
              meta-font-size: sm
              meta-color: text-secondary
          - label: queue-item
            status: drafting
            title: A Thousand Words of White
            author: Sarah Kim
            due-date: June 27
            time-slot: 10:00
            styles:
              background: surface
              padding: lg
              border-left: 3px solid text-tertiary
              title-font-size: base
              meta-font-size: sm
              meta-color: text-secondary
          - label: queue-item
            status: scheduled
            title: The Weight of Paper
            author: David Okonkwo
            due-date: June 28
            time-slot: 09:00
            styles:
              background: surface
              padding: lg
              border-left: 3px solid accent-blue
              title-font-size: base
              meta-font-size: sm
              meta-color: text-secondary
          - label: queue-item
            status: draft
            title: Typography as Interface
            author: Ana Torres
            due-date: June 29
            time-slot: 11:00
            styles:
              background: surface
              padding: lg
              border-left: 3px solid text-tertiary
              title-font-size: base
              meta-font-size: sm
              meta-color: text-secondary
      - area: preview
        width: 7
        height: full
        type: draft-preview
        elements:
          - label: header
            title: Draft Preview
            styles:
              padding: xl
              border-bottom: 1px solid border
              title-font-size: h4
              title-font-family: heading
          - label: editor-annotation
            type: comment
            author: Marcus Chen
            text: Consider shortening the opening paragraph. The strongest line is the third sentence.
            position: inline
            styles:
              background: '#f0ebe2'
              border-left: 3px solid accent-amber
              padding: md
              font-size: sm
              color: text-secondary
              line-height: relaxed
          - label: editor-annotation
            type: suggestion
            author: Elena Vasquez
            text: Add a pull quote here for visual rhythm. The section break needs breathing room.
            position: inline
            styles:
              background: '#ebe8e0'
              border-left: 3px solid accent-warm
              padding: md
              font-size: sm
              color: text-secondary
              line-height: relaxed
          - label: editor-annotation
            type: correction
            author: Ana Torres
            text: Citation format inconsistent with style guide. See CMOS 14.21.
            position: inline
            styles:
              background: '#f0e4de'
              border-left: 3px solid accent-terracotta
              padding: md
              font-size: sm
              color: text-secondary
              line-height: relaxed
          - label: preview-content
            text: >
              The first thing you notice is the silence. Not the absence of
              sound, but the presence of space. In a world saturated with
              information, the most radical design choice may be to withhold.
              To let the reader breathe. To trust that emptiness communicates
              as powerfully as content.
            styles:
              padding: xl
              font-size: lg
              line-height: relaxed
              color: text-primary
              font-family: body
              max-width: 600px
    responsive-behavior:
      mobile:
        layout: single-column
        calendar: full-width
        preview: full-width, below calendar
      tablet:
        layout: single-column
        calendar: full-width, collapsible sections
        preview: full-width
      desktop:
        layout: split-panel as specified
      wide:
        layout: split-panel with extra padding
  - id: mk-03
    name: Editorial Analytics Overview
    layout: metrics-dashboard
    description: Typography-first analytics dashboard with oversized stat cards, trend indicators, and a minimal reading chart. No gauges, no progress rings — just numbers and type.
    sections:
      - area: stats-row
        width: 12
        height: auto
        type: metric-cards
        elements:
          - label: big-stat
            value: 128,403
            label: total readers
            change: '+12.4%'
            trend: up
            period: vs last month
            styles:
              background: surface
              padding: xxl
              border-radius: 4px
              value-font-size: display
              value-font-family: heading
              value-line-height: tight
              value-color: text-primary
              label-font-size: xs
              label-color: text-secondary
              label-letter-spacing: wider
              label-text-transform: uppercase
              change-font-size: sm
              change-color: success
              change-font-weight: 500
              period-font-size: xs
              period-color: text-tertiary
          - label: big-stat
            value: 47.2
            label: avg engagement (min)
            change: '+3.8%'
            trend: up
            period: vs last month
            styles:
              background: surface
              padding: xxl
              border-radius: 4px
              value-font-size: display
              value-font-family: heading
              value-line-height: tight
              value-color: text-primary
              label-font-size: xs
              label-color: text-secondary
              label-letter-spacing: wider
              label-text-transform: uppercase
              change-font-size: sm
              change-color: success
              period-font-size: xs
              period-color: text-tertiary
          - label: big-stat
            value: 8,942
            label: returning readers
            change: '-2.1%'
            trend: down
            period: vs last month
            styles:
              background: surface
              padding: xxl
              border-radius: 4px
              value-font-size: display
              value-font-family: heading
              value-line-height: tight
              value-color: text-primary
              label-font-size: xs
              label-color: text-secondary
              label-letter-spacing: wider
              label-text-transform: uppercase
              change-font-size: sm
              change-color: error
              period-font-size: xs
              period-color: text-tertiary
      - area: reading-chart
        width: 8
        height: auto
        type: minimal-line-chart
        elements:
          - label: header
            title: Reading Time Distribution
            subtitle: Average minutes per session by day
            styles:
              padding: xl
              padding-bottom: 0
              title-font-size: h4
              title-font-family: heading
              subtitle-font-size: sm
              subtitle-color: text-secondary
          - label: chart
            type: line-annotation
            data-points:
              - label: Mon
                value: 4.2
              - label: Tue
                value: 3.8
              - label: Wed
                value: 5.1
              - label: Thu
                value: 6.3
              - label: Fri
                value: 7.8
              - label: Sat
                value: 12.4
              - label: Sun
                value: 10.2
            styles:
              padding: xl
              line-color: accent-warm
              line-thickness: 2px
              dot-color: accent-warm
              dot-size: 6px
              axis-color: border
              grid-color: '#f0ece5'
              label-font-size: xs
              label-color: text-tertiary
              label-letter-spacing: wider
      - area: top-articles
        width: 4
        height: auto
        type: ranked-list
        elements:
          - label: header
            title: Top Stories
            styles:
              padding: xl
              padding-bottom: md
              title-font-size: h4
              title-font-family: heading
          - label: ranked-item
            rank: 01
            title: The Architecture of Silence
            reads: 12,403
            styles:
              padding: md
              padding-left: xl
              padding-right: xl
              rank-font-size: h3
              rank-color: accent-terracotta
              rank-font-family: heading
              title-font-size: base
              title-font-weight: 500
              meta-font-size: xs
              meta-color: text-tertiary
              meta-letter-spacing: wider
              border-bottom: 1px solid border
          - label: ranked-item
            rank: 02
            title: On the Nature of Grids
            reads: 8,291
            styles:
              padding: md
              padding-left: xl
              padding-right: xl
              rank-font-size: h3
              rank-color: accent-amber
              rank-font-family: heading
              title-font-size: base
              title-font-weight: 500
              meta-font-size: xs
              meta-color: text-tertiary
              border-bottom: 1px solid border
          - label: ranked-item
            rank: 03
            title: A Thousand Words of White
            reads: 6,734
            styles:
              padding: md
              padding-left: xl
              padding-right: xl
              rank-font-size: h3
              rank-color: accent-warm
              rank-font-family: heading
              title-font-size: base
              title-font-weight: 500
              meta-font-size: xs
              meta-color: text-tertiary
              border-bottom: 1px solid border
          - label: ranked-item
            rank: 04
            title: The Weight of Paper
            reads: 4,502
            styles:
              padding: md
              padding-left: xl
              padding-right: xl
              rank-font-size: h3
              rank-color: text-tertiary
              rank-font-family: heading
              title-font-size: base
              title-font-weight: 500
              meta-font-size: xs
              meta-color: text-tertiary
              border-bottom: 1px solid border
          - label: ranked-item
            rank: 05
            title: Typography as Interface
            reads: 3,821
            styles:
              padding: md
              padding-left: xl
              padding-right: xl
              rank-font-size: h3
              rank-color: text-tertiary
              rank-font-family: heading
              title-font-size: base
              title-font-weight: 500
              meta-font-size: xs
              meta-color: text-tertiary
    responsive-behavior:
      mobile:
        layout: single-column
        big-stats: full-width, stacked, value scales to h1
        chart: full-width
        top-articles: full-width
      tablet:
        layout: 8-column grid
        big-stats: 4 columns each, 2 rows
        chart: 8 columns
        top-articles: 8 columns
      desktop:
        layout: as specified
      wide:
        layout: as specified
  - id: mk-04
    name: Editorial Settings & Preferences
    layout: form-panel
    description: Clean settings interface with typography-first form controls. Toggle switches as minimal circles, select menus as bordered text, section dividers as generous white space.
    sections:
      - area: navigation
        type: settings-nav
        width: 3
        height: full
        elements:
          - label: nav-item
            text: General
            icon: none
            active: true
            styles:
              padding: xl
              font-size: base
              font-weight: 500
              color: text-primary
              border-left: 3px solid text-primary
              background: surface
          - label: nav-item
            text: Notifications
            icon: none
            active: false
            styles:
              padding: xl
              font-size: base
              color: text-secondary
              border-left: 3px solid transparent
          - label: nav-item
            text: Appearance
            icon: none
            active: false
            styles:
              padding: xl
              font-size: base
              color: text-secondary
              border-left: 3px solid transparent
          - label: nav-item
            text: Content
            icon: none
            active: false
            styles:
              padding: xl
              font-size: base
              color: text-secondary
              border-left: 3px solid transparent
          - label: nav-item
            text: Team
            icon: none
            active: false
            styles:
              padding: xl
              font-size: base
              color: text-secondary
              border-left: 3px solid transparent
      - area: settings-content
        type: settings-form
        width: 9
        height: full
        elements:
          - label: section-header
            title: General Settings
            styles:
              padding: xl
              padding-bottom: lg
              title-font-size: h3
              title-font-family: heading
              border-bottom: 1px solid border
          - label: form-group
            title: Display Name
            input-type: text
            placeholder: Editor in Chief
            styles:
              padding: lg
              padding-left: xl
              padding-right: xl
              label-font-size: sm
              label-color: text-secondary
              label-letter-spacing: wider
              label-text-transform: uppercase
              input-font-size: base
              input-border: 1px solid border
              input-border-radius: 4px
              input-padding: md
              input-background: background
          - label: form-group
            title: Email Notifications
            input-type: toggle
            value: true
            styles:
              padding: lg
              padding-left: xl
              padding-right: xl
              label-font-size: sm
              label-color: text-secondary
              label-letter-spacing: wider
              label-text-transform: uppercase
              toggle-width: 40px
              toggle-height: 22px
              toggle-active-color: accent-green
              toggle-inactive-color: border
              toggle-knob-color: background
          - label: form-group
            title: Weekly Digest
            input-type: toggle
            value: false
            styles:
              padding: lg
              padding-left: xl
              padding-right: xl
              label-font-size: sm
              label-color: text-secondary
              label-letter-spacing: wider
              label-text-transform: uppercase
              toggle-width: 40px
              toggle-height: 22px
              toggle-active-color: accent-green
              toggle-inactive-color: border
          - label: form-group
            title: Language
            input-type: select
            options:
              - English
              - Swedish
              - French
              - German
              - Spanish
            value: English
            styles:
              padding: lg
              padding-left: xl
              padding-right: xl
              label-font-size: sm
              label-color: text-secondary
              label-letter-spacing: wider
              label-text-transform: uppercase
              select-font-size: base
              select-border: 1px solid border
              select-border-radius: 4px
              select-padding: md
              select-background: background
              select-arrow-color: text-tertiary
          - label: form-group
            title: Time Zone
            input-type: select
            options:
              - UTC (Coordinated Universal Time)
              - EST (Eastern Standard Time)
              - CET (Central European Time)
              - PST (Pacific Standard Time)
            value: CET (Central European Time)
            styles:
              padding: lg
              padding-left: xl
              padding-right: xl
              label-font-size: sm
              label-color: text-secondary
              label-letter-spacing: wider
              label-text-transform: uppercase
              select-font-size: base
              select-border: 1px solid border
              select-border-radius: 4px
              select-padding: md
          - label: form-actions
            type: button-row
            buttons:
              - text: Save Changes
                variant: primary
              - text: Reset to Defaults
                variant: secondary
            styles:
              padding: xl
              border-top: 1px solid border
              button-primary-background: text-primary
              button-primary-color: background
              button-primary-padding: 10px 28px
              button-primary-border-radius: 4px
              button-primary-font-size: base
              button-primary-font-weight: 500
              button-secondary-background: transparent
              button-secondary-color: text-secondary
              button-secondary-border: 1px solid border
              button-secondary-padding: 10px 28px
              button-secondary-border-radius: 4px
              button-secondary-font-size: base
    responsive-behavior:
      mobile:
        layout: single-column
        nav: horizontal scrollable tabs instead of sidebar
        form: full-width
      tablet:
        layout: single-column
        nav: 8-column tab row
        form: 8 columns
      desktop:
        layout: split-panel as specified
      wide:
        layout: as specified
  - id: mk-05
    name: Editorial Team Dashboard
    layout: profile-grid
    description: Team member cards in a bento grid layout. Each card shows portrait placeholder (warm monochrome block), name, role, current workload, and recent activity. Compact, information-dense but typographically clean.
    sections:
      - area: team-header
        width: 12
        height: auto
        type: section-header
        elements:
          - label: header
            title: Editorial Team
            subtitle: 8 members active this week
            styles:
              padding: xl
              padding-bottom: lg
              title-font-size: h2
              title-font-family: heading
              subtitle-font-size: base
              subtitle-color: text-secondary
      - area: team-grid
        width: 12
        height: auto
        type: bento-team-cards
        cards:
          - label: team-card
            name: Elena Vasquez
            role: Editor in Chief
            workload: 3 active stories
            status: online
            styles:
              width: 4
              background: surface
              padding: xl
              border-radius: 4px
              avatar-size: 48px
              avatar-background: accent-warm
              avatar-text: EV
              avatar-text-color: background
              name-font-size: lg
              name-font-weight: 600
              name-font-family: heading
              role-font-size: sm
              role-color: text-secondary
              workload-font-size: sm
              workload-color: text-tertiary
              status-color: success
          - label: team-card
            name: Marcus Chen
            role: Senior Editor
            workload: 2 active stories
            status: online
            styles:
              width: 4
              background: surface
              padding: xl
              border-radius: 4px
              avatar-size: 48px
              avatar-background: accent-amber
              avatar-text: MC
              avatar-text-color: background
              name-font-size: lg
              name-font-weight: 600
              name-font-family: heading
              role-font-size: sm
              role-color: text-secondary
              workload-font-size: sm
              workload-color: text-tertiary
              status-color: success
          - label: team-card
            name: Sarah Kim
            role: Associate Editor
            workload: 4 active stories
            status: busy
            styles:
              width: 4
              background: surface
              padding: xl
              border-radius: 4px
              avatar-size: 48px
              avatar-background: accent-terracotta
              avatar-text: SK
              avatar-text-color: background
              name-font-size: lg
              name-font-weight: 600
              name-font-family: heading
              role-font-size: sm
              role-color: text-secondary
              workload-font-size: sm
              workload-color: text-tertiary
              status-color: accent-amber
          - label: team-card
            name: David Okonkwo
            role: Staff Writer
            workload: 1 active story
            status: away
            styles:
              width: 4
              background: surface
              padding: xl
              border-radius: 4px
              avatar-size: 48px
              avatar-background: accent-green
              avatar-text: DO
              avatar-text-color: background
              name-font-size: lg
              name-font-weight: 600
              name-font-family: heading
              role-font-size: sm
              role-color: text-secondary
              workload-font-size: sm
              workload-color: text-tertiary
              status-color: text-tertiary
          - label: team-card
            name: Ana Torres
            role: Contributing Writer
            workload: 2 active stories
            status: online
            styles:
              width: 4
              background: surface
              padding: xl
              border-radius: 4px
              avatar-size: 48px
              avatar-background: accent-blue
              avatar-text: AT
              avatar-text-color: background
              name-font-size: lg
              name-font-weight: 600
              name-font-family: heading
              role-font-size: sm
              role-color: text-secondary
              workload-font-size: sm
              workload-color: text-tertiary
              status-color: success
          - label: team-card
            name: James Liu
            role: Copy Editor
            workload: 5 pending reviews
            status: busy
            styles:
              width: 4
              background: surface
              padding: xl
              border-radius: 4px
              avatar-size: 48px
              avatar-background: '#c4a882'
              avatar-text: JL
              avatar-text-color: background
              name-font-size: lg
              name-font-weight: 600
              name-font-family: heading
              role-font-size: sm
              role-color: text-secondary
              workload-font-size: sm
              workload-color: text-tertiary
              status-color: accent-amber
          - label: team-card
            name: Marie Lindgren
            role: Fact Checker
            workload: 3 pending verifications
            status: online
            styles:
              width: 4
              background: surface
              padding: xl
              border-radius: 4px
              avatar-size: 48px
              avatar-background: '#b89a7a'
              avatar-text: ML
              avatar-text-color: background
              name-font-size: lg
              name-font-weight: 600
              name-font-family: heading
              role-font-size: sm
              role-color: text-secondary
              workload-font-size: sm
              workload-color: text-tertiary
              status-color: success
          - label: team-card
            name: Tomás Rivera
            role: Photographer
            workload: 2 assignments due
            status: away
            styles:
              width: 4
              background: surface
              padding: xl
              border-radius: 4px
              avatar-size: 48px
              avatar-background: '#8a7a6a'
              avatar-text: TR
              avatar-text-color: background
              name-font-size: lg
              name-font-weight: 600
              name-font-family: heading
              role-font-size: sm
              role-color: text-secondary
              workload-font-size: sm
              workload-color: text-tertiary
              status-color: text-tertiary
    responsive-behavior:
      mobile:
        layout: single-column
        cards: full-width, single column
      tablet:
        layout: 8-column grid
        cards: 4 columns each, 2 rows
      desktop:
        layout: 12-column grid
        cards: 4 columns each, 3 rows
      wide:
        layout: 12-column grid
        cards: 4 columns each, 2 rows
  - id: mk-06
    name: Editorial Reading Session
    layout: reading-mode
    description: Immersive reading interface with article text in a narrow column centered on screen. Minimal top bar shows article metadata. Bottom of viewport shows reading progress as a thin line. Warm background, serif body type at generous size.
    sections:
      - area: top-bar
        width: 12
        height: auto
        type: reading-header
        elements:
          - label: breadcrumb
            text: Home / Features / The Architecture of Silence
            styles:
              padding: lg
              padding-left: xl
              padding-right: xl
              font-size: xs
              color: text-tertiary
              letter-spacing: wider
              text-transform: uppercase
          - label: article-meta
            author: Elena Vasquez
            date: June 26, 2026
            read-time: 8 min read
            styles:
              padding: md
              padding-left: xl
              padding-right: xl
              font-size: sm
              color: text-secondary
              letter-spacing: wider
      - area: article-body
        width: 12
        height: auto
        type: reading-content
        elements:
          - label: article-title
            text: The Architecture of Silence
            styles:
              padding: xl
              padding-bottom: md
              max-width: 680px
              margin: 0 auto
              font-size: h1
              font-family: heading
              line-height: tight
              letter-spacing: tight
              color: text-primary
              text-align: left
          - label: article-subtitle
            text: How empty space shapes the way we read
            styles:
              padding: 0
              padding-left: xl
              padding-right: xl
              padding-bottom: xl
              max-width: 680px
              margin: 0 auto
              font-size: lg
              font-family: body
              line-height: body
              color: text-secondary
              font-style: italic
          - label: body-paragraph
            text: >
              The first thing you notice is the silence. Not the absence of
              sound, but the presence of space. In a world saturated with
              information, the most radical design choice may be to withhold.
              To let the reader breathe. To trust that emptiness communicates
              as powerfully as content.
            styles:
              padding: lg
              padding-left: xl
              padding-right: xl
              max-width: 680px
              margin: 0 auto
              font-size: lg
              font-family: body
              line-height: relaxed
              color: text-primary
          - label: body-paragraph
            text: >
              Consider the page. Before there was a screen, there was paper.
              And before there was paper, there was stone. Each medium imposed
              its own constraints of space, and the best work in each medium
              understood those constraints not as limitations but as the very
              source of meaning.
            styles:
              padding: lg
              padding-left: xl
              padding-right: xl
              max-width: 680px
              margin: 0 auto
              font-size: lg
              font-family: body
              line-height: relaxed
              color: text-primary
          - label: pull-quote
            text: The most radical design choice may be to withhold. To let the reader breathe.
            attribution: Elena Vasquez
            styles:
              padding: xxl
              padding-left: xl
              padding-right: xl
              max-width: 680px
              margin: 0 auto
              font-size: h3
              font-family: heading
              line-height: tight
              letter-spacing: tight
              color: accent-terracotta
              font-style: italic
              border-left: 4px solid accent-warm
              attribution-font-size: sm
              attribution-color: text-tertiary
              attribution-letter-spacing: wider
              attribution-text-transform: uppercase
          - label: body-paragraph
            text: >
              Digital design has confused abundance with value. The ability
              to fill every pixel has been mistaken for an obligation to do
              so. But the eye needs rest. The mind needs silence. And the
              most memorable interfaces are the ones that know when to step
              back and let the content speak.
            styles:
              padding: lg
              padding-left: xl
              padding-right: xl
              max-width: 680px
              margin: 0 auto
              font-size: lg
              font-family: body
              line-height: relaxed
              color: text-primary
      - area: reading-progress
        width: 12
        height: 3px
        type: progress-bar
        elements:
          - label: progress-indicator
            value: 35
            unit: percent
            styles:
              background: border
              height: 3px
              fill-color: accent-warm
              fill-height: 3px
              position: fixed
              bottom: 0
              left: 0
    responsive-behavior:
      mobile:
        layout: single-column
        article-column: max-width 90vw
        title: h2
        body: base
      tablet:
        layout: single-column
        article-column: max-width 72vw
      desktop:
        layout: as specified, max-width 680px article column
      wide:
        layout: as specified, max-width 720px article column
  - id: mk-07
    name: Editorial Archive & Search
    layout: search-interface
    description: Minimal search interface with large centered search field, faceted filters as horizontal tag pills, and results displayed as compact article cards. Search placeholder text is editorial in tone.
    sections:
      - area: search-header
        width: 12
        height: auto
        type: search-bar
        elements:
          - label: search-field
            placeholder: Search the archive...
            styles:
              padding: xl
              padding-top: xxl
              font-size: h3
              font-family: heading
              color: text-primary
              border: none
              border-bottom: 2px solid border
              background: transparent
              width: 100%
              placeholder-color: text-tertiary
              focus-border-color: accent-warm
              focus-border-bottom: 2px solid accent-warm
              outline: none
          - label: filter-row
            filters:
              - label: All
                active: true
              - label: Articles
                active: false
              - label: Essays
                active: false
              - label: Reviews
                active: false
              - label: Interviews
                active: false
              - label: Opinions
                active: false
            styles:
              padding: lg
              padding-left: xl
              padding-right: xl
              display: flex
              gap: sm
              filter-tag-background: surface
              filter-tag-border: 1px solid border
              filter-tag-border-radius: 20px
              filter-tag-padding: 6px 16px
              filter-tag-font-size: sm
              filter-tag-color: text-secondary
              filter-tag-letter-spacing: wider
              filter-tag-text-transform: uppercase
              filter-tag-active-background: text-primary
              filter-tag-active-color: background
              filter-tag-active-border: 1px solid text-primary
      - area: search-results
        width: 12
        height: auto
        type: results-list
        elements:
          - label: result-count
            text: 47 results found
            styles:
              padding: xl
              padding-bottom: md
              font-size: xs
              color: text-tertiary
              letter-spacing: wider
              text-transform: uppercase
          - label: result-card
            title: The Architecture of Silence
            author: Elena Vasquez
            date: June 26, 2026
            category: featured
            summary: How empty space shapes the way we read. A deep dive into the typographic principles that define modern editorial design.
            match-position: title
            styles:
              padding: lg
              padding-left: xl
              padding-right: xl
              border-bottom: 1px solid border
              title-font-size: lg
              title-font-weight: 500
              title-font-family: heading
              title-color: text-primary
              meta-font-size: xs
              meta-color: text-secondary
              meta-letter-spacing: wider
              summary-font-size: base
              summary-color: text-secondary
              summary-line-height: body
              category-tag-background: surface
              category-tag-border-radius: 4px
              category-tag-padding: 2px 8px
              category-tag-font-size: xs
              category-tag-color: accent-terracotta
              category-tag-text-transform: uppercase
              match-highlight-background: '#f0e4d0'
          - label: result-card
            title: On the Nature of Grids
            author: Marcus Chen
            date: June 25, 2026
            category: opinion
            summary: Why the best layouts are invisible. An exploration of grid systems and how they create structure without imposing on the reader.
            match-position: body
            styles:
              padding: lg
              padding-left: xl
              padding-right: xl
              border-bottom: 1px solid border
              title-font-size: lg
              title-font-weight: 500
              title-font-family: heading
              meta-font-size: xs
              meta-color: text-secondary
              summary-font-size: base
              summary-color: text-secondary
              summary-line-height: body
              category-tag-color: accent-amber
          - label: result-card
            title: A Thousand Words of White
            author: Sarah Kim
            date: June 24, 2026
            category: essay
            summary: On the power of negative space in both design and prose. A meditation on what we leave out, and why it matters.
            match-position: title
            styles:
              padding: lg
              padding-left: xl
              padding-right: xl
              border-bottom: 1px solid border
              title-font-size: lg
              title-font-weight: 500
              title-font-family: heading
              meta-font-size: xs
              meta-color: text-secondary
              summary-font-size: base
              summary-color: text-secondary
              summary-line-height: body
              category-tag-color: accent-warm
          - label: result-card
            title: The Weight of Paper
            author: David Okonkwo
            date: June 23, 2026
            category: review
            summary: A critique of the digital reading experience through the lens of print craftsmanship. What screens can learn from paper.
            match-position: body
            styles:
              padding: lg
              padding-left: xl
              padding-right: xl
              border-bottom: 1px solid border
              title-font-size: lg
              title-font-weight: 500
              title-font-family: heading
              meta-font-size: xs
              meta-color: text-secondary
              summary-font-size: base
              summary-color: text-secondary
              summary-line-height: body
              category-tag-color: accent-blue
          - label: result-card
            title: Typography as Interface
            author: Ana Torres
            date: June 22, 2026
            category: essay
            summary: A manifesto for quiet design. Type is the UI. Everything else is decoration.
            match-position: title
            styles:
              padding: lg
              padding-left: xl
              padding-right: xl
              border-bottom: 1px solid border
              title-font-size: lg
              title-font-weight: 500
              title-font-family: heading
              meta-font-size: xs
              meta-color: text-secondary
              summary-font-size: base
              summary-color: text-secondary
              summary-line-height: body
              category-tag-color: accent-warm
    responsive-behavior:
      mobile:
        layout: single-column
        search-field: h4
        filters: horizontal scroll
      tablet:
        layout: single-column
        search-field: h3
      desktop:
        layout: as specified
      wide:
        layout: as specified
  - id: mk-08
    name: Editorial Publishing Workflow
    layout: kanban-board
    description: Three-column kanban with editorial stages: Draft, In Review, Published. Each card shows title, author, word count, and time since last update. Warm muted backgrounds, clean card borders, no drag handles — cards are pure typography.
    sections:
      - area: kanban-header
        width: 12
        height: auto
        type: workflow-header
        elements:
          - label: header
            title: Publishing Workflow
            subtitle: Week 26, 2026
            styles:
              padding: xl
              padding-bottom: lg
              title-font-size: h2
              title-font-family: heading
              subtitle-font-size: base
              subtitle-color: text-secondary
      - area: kanban-columns
        width: 12
        height: auto
        type: kanban-layout
        columns:
          - label: column
            title: Draft
            count: 4
            styles:
              width: 4
              background: '#f8f6f2'
              border-radius: 4px
              padding: md
              column-header-padding: lg
              column-header-font-size: xs
              column-header-color: text-secondary
              column-header-letter-spacing: wider
              column-header-text-transform: uppercase
              column-header-border-bottom: 1px solid border
            cards:
              - label: kanban-card
                title: The Weight of Paper
                author: David Okonkwo
                word-count: 2,400
                last-updated: 2 hours ago
                status: draft
                styles:
                  background: surface
                  padding: lg
                  margin-bottom: sm
                  border-radius: 4px
                  title-font-size: base
                  title-font-weight: 500
                  meta-font-size: xs
                  meta-color: text-secondary
                  meta-letter-spacing: wider
                  time-font-size: xs
                  time-color: text-tertiary
              - label: kanban-card
                title: Typography as Interface
                author: Ana Torres
                word-count: 3,800
                last-updated: 5 hours ago
                status: draft
                styles:
                  background: surface
                  padding: lg
                  margin-bottom: sm
                  border-radius: 4px
                  title-font-size: base
                  title-font-weight: 500
                  meta-font-size: xs
                  meta-color: text-secondary
                  time-font-size: xs
                  time-color: text-tertiary
              - label: kanban-card
                title: The Future of Print
                author: Marcus Chen
                word-count: 1,200
                last-updated: 1 day ago
                status: draft
                styles:
                  background: surface
                  padding: lg
                  margin-bottom: sm
                  border-radius: 4px
                  title-font-size: base
                  title-font-weight: 500
                  meta-font-size: xs
                  meta-color: text-secondary
                  time-font-size: xs
                  time-color: text-tertiary
              - label: kanban-card
                title: Interview with Jan Tschichold
                author: Sarah Kim
                word-count: 900
                last-updated: 3 days ago
                status: draft
                styles:
                  background: surface
                  padding: lg
                  margin-bottom: sm
                  border-radius: 4px
                  title-font-size: base
                  title-font-weight: 500
                  meta-font-size: xs
                  meta-color: text-secondary
                  time-font-size: xs
                  time-color: text-tertiary
          - label: column
            title: In Review
            count: 3
            styles:
              width: 4
              background: '#f8f6f2'
              border-radius: 4px
              padding: md
              column-header-padding: lg
              column-header-font-size: xs
              column-header-color: text-secondary
              column-header-letter-spacing: wider
              column-header-text-transform: uppercase
              column-header-border-bottom: 1px solid accent-amber
            cards:
              - label: kanban-card
                title: 'On the Nature of Grids (revised)'
                author: Marcus Chen
                word-count: 3,200
                last-updated: 30 min ago
                reviewer: Elena
                status: review
                styles:
                  background: surface
                  padding: lg
                  margin-bottom: sm
                  border-radius: 4px
                  border-left: 3px solid accent-amber
                  title-font-size: base
                  title-font-weight: 500
                  meta-font-size: xs
                  meta-color: text-secondary
                  time-font-size: xs
                  time-color: text-tertiary
              - label: kanban-card
                title: A Thousand Words of White
                author: Sarah Kim
                word-count: 4,100
                last-updated: 1 hour ago
                reviewer: Marcus
                status: review
                styles:
                  background: surface
                  padding: lg
                  margin-bottom: sm
                  border-radius: 4px
                  border-left: 3px solid accent-amber
                  title-font-size: base
                  title-font-weight: 500
                  meta-font-size: xs
                  meta-color: text-secondary
                  time-font-size: xs
                  time-color: text-tertiary
              - label: kanban-card
                title: Reading Habits in 2026
                author: Ana Torres
                word-count: 2,800
                last-updated: 4 hours ago
                reviewer: Sarah
                status: review
                styles:
                  background: surface
                  padding: lg
                  margin-bottom: sm
                  border-radius: 4px
                  border-left: 3px solid accent-amber
                  title-font-size: base
                  title-font-weight: 500
                  meta-font-size: xs
                  meta-color: text-secondary
                  time-font-size: xs
                  time-color: text-tertiary
          - label: column
            title: Published
            count: 2
            styles:
              width: 4
              background: '#f8f6f2'
              border-radius: 4px
              padding: md
              column-header-padding: lg
              column-header-font-size: xs
              column-header-color: text-secondary
              column-header-letter-spacing: wider
              column-header-text-transform: uppercase
              column-header-border-bottom: 1px solid success
            cards:
              - label: kanban-card
                title: The Architecture of Silence
                author: Elena Vasquez
                word-count: 5,600
                published: June 26, 2026
                views: 12,403
                status: published
                styles:
                  background: surface
                  padding: lg
                  margin-bottom: sm
                  border-radius: 4px
                  border-left: 3px solid success
                  title-font-size: base
                  title-font-weight: 500
                  meta-font-size: xs
                  meta-color: text-secondary
                  views-font-size: xs
                  views-color: success
              - label: kanban-card
                title: Letter from the Editor
                author: Elena Vasquez
                word-count: 800
                published: June 25, 2026
                views: 8,941
                status: published
                styles:
                  background: surface
                  padding: lg
                  margin-bottom: sm
                  border-radius: 4px
                  border-left: 3px solid success
                  title-font-size: base
                  title-font-weight: 500
                  meta-font-size: xs
                  meta-color: text-secondary
                  views-font-size: xs
                  views-color: success
    responsive-behavior:
      mobile:
        layout: single-column
        columns: full-width, stacked
      tablet:
        layout: horizontal scroll
        columns: 240px min-width each
      desktop:
        layout: 3 columns as specified
      wide:
        layout: 3 columns with extra spacing
  - id: mk-09
    name: Editorial Newsletter Composer
    layout: composer-interface
    description: Split-panel newsletter builder. Left side shows a WYSIWYG preview of the newsletter, right side shows controls: subject line, recipient segment, send schedule. Warm, editorial feel throughout.
    sections:
      - area: preview-panel
        width: 7
        height: full
        type: newsletter-preview
        elements:
          - label: preview-header
            type: newsletter-header
            publication: The Editorial Weekly
            date: June 26, 2026
            subject: The Architecture of Silence
            styles:
              padding: xl
              border-bottom: 1px solid border
              publication-font-size: xs
              publication-color: text-tertiary
              publication-letter-spacing: wider
              publication-text-transform: uppercase
              date-font-size: xs
              date-color: text-tertiary
              subject-font-size: h3
              subject-font-family: heading
              subject-line-height: tight
              subject-color: text-primary
              subject-margin-top: md
          - label: preview-content
            type: newsletter-body
            intro: >
              This week, we explore the spaces between words. Elena Vasquez
              on the architecture of silence, Marcus Chen on the nature of
              grids, and a meditation on what we leave out.
            articles:
              - title: The Architecture of Silence
                author: Elena Vasquez
                excerpt: How empty space shapes the way we read
              - title: On the Nature of Grids
                author: Marcus Chen
                excerpt: Why the best layouts are invisible
            styles:
              padding: xl
              intro-font-size: base
              intro-line-height: relaxed
              intro-color: text-primary
              article-title-font-size: lg
              article-title-font-family: heading
              article-title-color: text-primary
              article-excerpt-font-size: base
              article-excerpt-color: text-secondary
              article-divider: 1px solid border
              article-divider-margin: lg
          - label: preview-footer
            type: newsletter-footer
            text: Thank you for reading. Reply to this email to share your thoughts.
            styles:
              padding: xl
              border-top: 1px solid border
              font-size: sm
              color: text-tertiary
              line-height: relaxed
      - area: composer-controls
        width: 5
        height: full
        type: newsletter-settings
        elements:
          - label: form-group
            title: Subject Line
            input-type: text
            value: The Architecture of Silence
            placeholder: Enter subject line
            styles:
              padding: xl
              padding-bottom: md
              label-font-size: xs
              label-color: text-secondary
              label-letter-spacing: wider
              label-text-transform: uppercase
              input-font-size: base
              input-border: 1px solid border
              input-border-radius: 4px
              input-padding: md
          - label: form-group
            title: Preheader Text
            input-type: text
            value: How empty space shapes the way we read
            placeholder: Enter preheader text
            styles:
              padding: xl
              padding-bottom: md
              label-font-size: xs
              label-color: text-secondary
              label-letter-spacing: wider
              label-text-transform: uppercase
              input-font-size: base
              input-border: 1px solid border
              input-border-radius: 4px
              input-padding: md
          - label: form-group
            title: Recipient Segment
            input-type: select
            options:
              - All Subscribers
              - Active Readers
              - Premium Subscribers
              - Trial Users
            value: All Subscribers
            styles:
              padding: xl
              padding-bottom: md
              label-font-size: xs
              label-color: text-secondary
              label-letter-spacing: wider
              label-text-transform: uppercase
              select-font-size: base
              select-border: 1px solid border
              select-border-radius: 4px
              select-padding: md
          - label: form-group
            title: Send Schedule
            input-type: select
            options:
              - Send Now
              - Schedule for Tomorrow 08:00
              - Schedule for Monday 08:00
              - Custom Date
            value: Schedule for Tomorrow 08:00
            styles:
              padding: xl
              padding-bottom: md
              label-font-size: xs
              label-color: text-secondary
              label-letter-spacing: wider
              label-text-transform: uppercase
              select-font-size: base
              select-border: 1px solid border
              select-border-radius: 4px
              select-padding: md
          - label: form-group
            title: Test Send
            input-type: email
            value: editor@publication.com
            placeholder: Enter test email address
            styles:
              padding: xl
              padding-bottom: xl
              label-font-size: xs
              label-color: text-secondary
              label-letter-spacing: wider
              label-text-transform: uppercase
              input-font-size: base
              input-border: 1px solid border
              input-border-radius: 4px
              input-padding: md
          - label: form-actions
            type: button-row
            buttons:
              - text: Send Test
                variant: secondary
              - text: Schedule Newsletter
                variant: primary
            styles:
              padding: xl
              border-top: 1px solid border
              button-primary-background: text-primary
              button-primary-color: background
              button-primary-padding: 10px 28px
              button-primary-border-radius: 4px
              button-primary-font-size: base
              button-primary-font-weight: 500
              button-secondary-background: transparent
              button-secondary-color: text-secondary
              button-secondary-border: 1px solid border
              button-secondary-padding: 10px 28px
              button-secondary-border-radius: 4px
              button-secondary-font-size: base
    responsive-behavior:
      mobile:
        layout: single-column
        preview: full-width
        controls: full-width, below preview
      tablet:
        layout: single-column
        preview: full-width
        controls: full-width, below preview
      desktop:
        layout: split-panel as specified
      wide:
        layout: split-panel
  - id: mk-10
    name: Editorial Dashboard Hub
    layout: master-hub
    description: Primary landing dashboard combining a welcome section, key editorial metrics, recent activity feed, and quick-actions bar. Designed as the first screen editors see each morning.
    sections:
      - area: welcome
        width: 12
        height: auto
        type: welcome-hero
        elements:
          - label: greeting
            text: Good morning, Elena
            styles:
              padding: xl
              padding-bottom: 0
              font-size: h2
              font-family: heading
              line-height: tight
              color: text-primary
          - label: daily-brief
            text: 3 articles to review, 2 in draft, 1 publishing today
            styles:
              padding: xl
              padding-top: sm
              font-size: lg
              color: text-secondary
              line-height: body
      - area: key-metrics
        width: 12
        height: auto
        type: editorial-metrics-row
        elements:
          - label: metric-card
            value: 47
            label: pieces published this month
            trend: '+8 vs last month'
            trend-direction: up
            styles:
              width: 3
              background: surface
              padding: xl
              border-radius: 4px
              value-font-size: h1
              value-font-family: heading
              value-line-height: tight
              value-color: accent-terracotta
              label-font-size: xs
              label-color: text-secondary
              label-letter-spacing: wider
              label-text-transform: uppercase
              trend-font-size: xs
              trend-color: success
          - label: metric-card
            value: 12.4k
            label: total readers this week
            trend: '+3.2% vs last week'
            trend-direction: up
            styles:
              width: 3
              background: surface
              padding: xl
              border-radius: 4px
              value-font-size: h1
              value-font-family: heading
              value-line-height: tight
              value-color: accent-amber
              label-font-size: xs
              label-color: text-secondary
              label-letter-spacing: wider
              label-text-transform: uppercase
              trend-font-size: xs
              trend-color: success
          - label: metric-card
            value: 4.7
            label: avg read time (min)
            trend: '+0.8 vs last week'
            trend-direction: up
            styles:
              width: 3
              background: surface
              padding: xl
              border-radius: 4px
              value-font-size: h1
              value-font-family: heading
              value-line-height: tight
              value-color: accent-green
              label-font-size: xs
              label-color: text-secondary
              label-letter-spacing: wider
              label-text-transform: uppercase
              trend-font-size: xs
              trend-color: success
          - label: metric-card
            value: '87%'
            label: reader retention
            trend: '-2.1% vs last week'
            trend-direction: down
            styles:
              width: 3
              background: surface
              padding: xl
              border-radius: 4px
              value-font-size: h1
              value-font-family: heading
              value-line-height: tight
              value-color: accent-blue
              label-font-size: xs
              label-color: text-secondary
              label-letter-spacing: wider
              label-text-transform: uppercase
              trend-font-size: xs
              trend-color: error
      - area: recent-activity
        width: 8
        height: auto
        type: activity-feed
        elements:
          - label: section-header
            title: Recent Activity
            styles:
              padding: xl
              padding-bottom: md
              title-font-size: h4
              title-font-family: heading
          - label: activity-item
            type: published
            actor: Elena Vasquez
            action: published
            target: The Architecture of Silence
            time: 2 hours ago
            styles:
              padding: lg
              padding-left: xl
              padding-right: xl
              border-bottom: 1px solid border
              font-size: base
              color: text-primary
              meta-font-size: xs
              meta-color: text-tertiary
              action-color: success
          - label: activity-item
            type: review
            actor: Marcus Chen
            action: submitted for review
            target: On the Nature of Grids
            time: 3 hours ago
            styles:
              padding: lg
              padding-left: xl
              padding-right: xl
              border-bottom: 1px solid border
              font-size: base
              color: text-primary
              meta-font-size: xs
              meta-color: text-tertiary
              action-color: accent-amber
          - label: activity-item
            type: comment
            actor: Sarah Kim
            action: commented on
            target: A Thousand Words of White
            time: 4 hours ago
            styles:
              padding: lg
              padding-left: xl
              padding-right: xl
              border-bottom: 1px solid border
              font-size: base
              color: text-primary
              meta-font-size: xs
              meta-color: text-tertiary
              action-color: accent-warm
          - label: activity-item
            type: draft
            actor: David Okonkwo
            action: started drafting
            target: The Weight of Paper
            time: 6 hours ago
            styles:
              padding: lg
              padding-left: xl
              padding-right: xl
              border-bottom: 1px solid border
              font-size: base
              color: text-primary
              meta-font-size: xs
              meta-color: text-tertiary
              action-color: accent-blue
          - label: activity-item
            type: schedule
            actor: System
            action: scheduled
            target: Letter from the Editor
            time: 8 hours ago
            styles:
              padding: lg
              padding-left: xl
              padding-right: xl
              border-bottom: 1px solid border
              font-size: base
              color: text-primary
              meta-font-size: xs
              meta-color: text-tertiary
              action-color: text-tertiary
      - area: quick-actions
        width: 4
        height: auto
        type: actions-panel
        elements:
          - label: section-header
            title: Quick Actions
            styles:
              padding: xl
              padding-bottom: md
              title-font-size: h4
              title-font-family: heading
          - label: action-button
            text: New Article
            icon: '+'
            styles:
              padding: lg
              padding-left: xl
              padding-right: xl
              margin-bottom: sm
              background: surface
              border-radius: 4px
              border: 1px solid border
              font-size: base
              font-weight: 500
              color: text-primary
              icon-color: accent-terracotta
              icon-font-size: lg
              hover-background: surface-hover
              hover-border-color: accent-warm
          - label: action-button
            text: Review Queue
            icon: '3'
            badge-count: 3
            styles:
              padding: lg
              padding-left: xl
              padding-right: xl
              margin-bottom: sm
              background: surface
              border-radius: 4px
              border: 1px solid border
              font-size: base
              font-weight: 500
              color: text-primary
              badge-background: accent-amber
              badge-color: background
              badge-font-size: xs
              badge-padding: 2px 8px
              badge-border-radius: 10px
          - label: action-button
            text: Compose Newsletter
            icon: '+'
            styles:
              padding: lg
              padding-left: xl
              padding-right: xl
              margin-bottom: sm
              background: surface
              border-radius: 4px
              border: 1px solid border
              font-size: base
              font-weight: 500
              color: text-primary
          - label: action-button
            text: Analytics Report
            icon: '+'
            styles:
              padding: lg
              padding-left: xl
              padding-right: xl
              margin-bottom: sm
              background: surface
              border-radius: 4px
              border: 1px solid border
              font-size: base
              font-weight: 500
              color: text-primary
          - label: action-button
            text: Team Calendar
            icon: '+'
            styles:
              padding: lg
              padding-left: xl
              padding-right: xl
              background: surface
              border-radius: 4px
              border: 1px solid border
              font-size: base
              font-weight: 500
              color: text-primary
    responsive-behavior:
      mobile:
        layout: single-column
        metrics: 2-column grid, values scale to h3
        activity: full-width
        actions: full-width
      tablet:
        layout: 8-column grid
        metrics: 4 columns each, 2 rows
        activity: 8 columns
        actions: 8 columns, horizontal button row
      desktop:
        layout: as specified
      wide:
        layout: as specified
yaml-validation-rules:
  - rule: No mapping anchors used for scalar values
    description: Every YAML alias must reference a same-type anchor. Never use a mapping anchor where a scalar color value is expected.
  - rule: All color values are inline hex strings
    description: Color values are hardcoded hex strings ('#faf8f5'), never referenced via YAML anchors.
  - rule: Styles blocks are fully expanded inline
    description: No shared style anchors or aliases. Each mockup's styles are self-contained to prevent type mismatches.
  - rule: Width and height values are numeric, not aliased
    description: Grid dimensions specified as raw integers (width: 4), never through anchor indirection.
  - rule: Array items are explicit
    description: Card arrays, element lists, and option lists are always full explicit arrays, never anchored sequences.
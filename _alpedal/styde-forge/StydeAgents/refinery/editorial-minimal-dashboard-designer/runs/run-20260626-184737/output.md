```yaml
design-system:
  color-palette:
    background: &color-bg '#f5f2ed'
    surface: &color-surface '#ece8e1'
    surface-hover: &color-surface-hover '#e3ded5'
    surface-raised: &color-surface-raised '#faf8f5'
    text-primary: &color-text-primary '#2c2821'
    text-secondary: &color-text-secondary '#6b6559'
    text-tertiary: &color-text-tertiary '#9e9688'
    text-on-accent: &color-text-on-accent '#faf8f5'
    border-default: &color-border '#d9d3c9'
    border-subtle: &color-border-subtle '#e5e0d7'
    accent-warm: &color-accent-warm '#b8a088'
    accent-warm-hover: &color-accent-warm-hover '#a68d73'
    accent-soft: &color-accent-soft '#c4b8a8'
    accent-focus: &color-accent-focus '#8c7a64'
    tag-background: &color-tag-bg '#e8e2d9'
    tag-text: &color-tag-text '#5c5548'
    scrollbar-thumb: '#c9c0b4'
    scrollbar-track: '#f0ece5'
    overlay: 'rgba(44, 40, 33, 0.4)'
  typography:
    font-family:
      heading: &font-heading "'Georgia', 'Times New Roman', serif"
      body: &font-body "'SF Pro Text', -apple-system, 'Helvetica Neue', 'Arial', sans-serif"
      mono: &font-mono "'SF Mono', 'Cascadia Code', 'JetBrains Mono', monospace"
    type-scale:
      display: { size: 48px, line-height: 1.15, letter-spacing: -0.02em, weight: 400 }
      h1: { size: 32px, line-height: 1.2, letter-spacing: -0.01em, weight: 400 }
      h2: { size: 24px, line-height: 1.25, letter-spacing: -0.005em, weight: 400 }
      h3: { size: 20px, line-height: 1.3, letter-spacing: 0, weight: 400 }
      subtitle: { size: 16px, line-height: 1.4, letter-spacing: 0.01em, weight: 400 }
      body: { size: 15px, line-height: 1.6, letter-spacing: 0.005em, weight: 400 }
      body-small: { size: 13px, line-height: 1.5, letter-spacing: 0.01em, weight: 400 }
      caption: { size: 12px, line-height: 1.4, letter-spacing: 0.02em, weight: 400 }
      meta: { size: 11px, line-height: 1.3, letter-spacing: 0.04em, weight: 500 }
      data: { size: 14px, line-height: 1.4, letter-spacing: 0, weight: 400 }
  spacing:
    xs: 4px
    sm: 8px
    md: 16px
    lg: 24px
    xl: 32px
    xxl: 48px
    section: 64px
  base-unit: 8px
  grid-columns: 12
  max-width: 1440px
  radii:
    sm: 4px
    md: 8px
    lg: 12px
    xl: 16px
    pill: 24px
  shadows:
    card-default: '0 1px 2px rgba(44, 40, 33, 0.06)'
    card-hover: '0 2px 8px rgba(44, 40, 33, 0.08), 0 1px 3px rgba(44, 40, 33, 0.04)'
    card-active: '0 0 0 2px #8c7a64, 0 2px 4px rgba(44, 40, 33, 0.08)'
responsive-breakpoints:
  mobile: { max-width: 599px, columns: 4, gutter: 16px, margin: 16px }
  tablet: { min-width: 600px, max-width: 1023px, columns: 8, gutter: 20px, margin: 24px }
  desktop: { min-width: 1024px, max-width: 1399px, columns: 12, gutter: 24px, margin: 32px }
  wide: { min-width: 1400px, columns: 12, gutter: 32px, margin: 48px }
shared-interactive-states:
  card: &state-card
    default: { background: *color-surface, border: 1px solid *color-border-subtle, shadow: *card-default, transition: 'all 0.2s ease' }
    hover: { background: *color-surface-hover, border: 1px solid *color-border, shadow: *card-hover, cursor: pointer }
    focus: { background: *color-surface, border: 1px solid *accent-focus, shadow: *card-active, outline: none }
    active: { background: '#ddd8ce', border: 1px solid *color-border, shadow: *card-default }
    disabled: { background: '#f0ece5', border: 1px solid '#e5e0d7', opacity: 0.5 }
  link: &state-link
    default: { color: *color-text-secondary, text-decoration: none, transition: 'color 0.15s ease' }
    hover: { color: *color-text-primary, text-decoration: underline }
    focus: { color: *accent-focus, text-decoration: underline, outline: 2px solid *accent-focus, outline-offset: 2px }
  button-primary: &state-button
    default: { background: *color-text-primary, color: *text-on-accent, border: none, radius: *md, shadow: none, transition: 'all 0.2s ease' }
    hover: { background: '#3d382f', cursor: pointer }
    focus: { outline: 2px solid *accent-focus, outline-offset: 2px }
    active: { background: '#1d1a16' }
    disabled: { background: '#9e9688', opacity: 0.5, cursor: not-allowed }
  tag: &state-tag
    default: { background: *color-tag-bg, color: *tag-text, radius: *pill, border: none, transition: 'all 0.15s ease' }
    hover: { background: '#ddd6ca', cursor: pointer }
    focus: { outline: 2px solid *accent-focus, outline-offset: 1px }
mockups:
  - id: mk-01
    name: Editors Briefing
    layout: bento-grid
    description: Daily editorial briefing with featured read, curated queue, and team pulse. Asymmetrical grid places the lead story prominently on the left with supporting modules stacked to the right.
    sections:
      - id: featured-story
        grid-position: { col: 1, col-span: 7, row: 1, row-span: 3 }
        type: hero-card
        background: *color-surface-raised
        border: 1px solid *color-border-subtle
        radius: *lg
        padding: *xl
        elements:
          - type: badge
            content: 'Staff Pick'
            font-family: *font-body
            font-size: 11px
            font-weight: 500
            letter-spacing: 0.06em
            color: *color-accent-warm
            text-transform: uppercase
            margin-bottom: *md
          - type: heading
            content: 'The Architecture of Silence: How Negative Space Shapes Narrative'
            font-family: *font-heading
            font-size: 28px
            line-height: 1.25
            color: *color-text-primary
            margin-bottom: *sm
          - type: meta-line
            content: 'By Elena Voss  ·  18 min read  ·  Filed under Essays'
            font-family: *font-body
            font-size: 12px
            color: *color-text-tertiary
            letter-spacing: 0.02em
            margin-bottom: *lg
          - type: excerpt
            content: 'In the margins between words, meaning accumulates. A meditation on what is left unsaid in the works of Duras, Carver, and Kawabata — and how contemporary editors might reclaim the lost art of restraint.'
            font-family: *font-body
            font-size: 15px
            line-height: 1.65
            color: *color-text-secondary
          - type: divider
            style: '1px solid #e5e0d7'
            margin-top: *lg
            margin-bottom: *md
          - type: action-row
            elements:
              - type: button
                label: 'Read Full Piece'
                variant: primary
                <<: *state-button
              - type: link
                label: 'Save for Later'
                <<: *state-link
      - id: reading-queue
        grid-position: { col: 8, col-span: 5, row: 1, row-span: 2 }
        type: list-card
        background: *color-surface
        border: 1px solid *color-border-subtle
        radius: *lg
        padding: *lg
        elements:
          - type: section-header
            content: 'Reading Queue'
            font-family: *font-body
            font-size: 11px
            font-weight: 500
            letter-spacing: 0.06em
            text-transform: uppercase
            color: *color-text-tertiary
            margin-bottom: *md
          - type: item-list
            items:
              - title: 'On Being Precise With Words'
                author: 'James Wood'
                time: '14 min'
                status: unread
              - title: 'The Digital Commonplace Book'
                author: 'Craig Mod'
                time: '22 min'
                status: unread
              - title: 'Typography as Atmosphere'
                author: 'Maria Popova'
                time: '9 min'
                status: reading
              - title: 'Against Algorithmic Curation'
                author: 'Kyle Chayka'
                time: '11 min'
                status: unread
            item-style:
              padding: *sm 0
              border-bottom: '1px solid #e5e0d7'
              font-family: *font-body
              title-size: 14px
              title-color: *color-text-primary
              author-size: 12px
              author-color: *color-text-tertiary
      - id: team-pulse
        grid-position: { col: 8, col-span: 5, row: 3, row-span: 1 }
        type: compact-card
        background: *color-surface
        border: 1px solid *color-border-subtle
        radius: *lg
        padding: *lg
        elements:
          - type: section-header
            content: 'Team Pulse'
            font-family: *font-body
            font-size: 11px
            font-weight: 500
            letter-spacing: 0.06em
            text-transform: uppercase
            color: *color-text-tertiary
            margin-bottom: *md
          - type: stat-row
            stats:
              - label: 'In Review'
                value: 7
                color: *color-text-primary
              - label: 'Scheduled'
                value: 4
                color: *color-text-primary
              - label: 'Drafts'
                value: 12
                color: *color-accent-warm
            stat-style:
              font-family: *font-mono
              value-size: 22px
              label-size: 11px
              label-color: *color-text-tertiary
              letter-spacing: 0.02em
      - id: recent-activity
        grid-position: { col: 1, col-span: 12, row: 4, row-span: 1 }
        type: horizontal-scroll
        background: *color-surface-raised
        border: 1px solid *color-border-subtle
        radius: *md
        padding: *md *lg
        elements:
          - type: section-header
            content: 'Latest Edits'
            font-family: *font-body
            font-size: 11px
            font-weight: 500
            letter-spacing: 0.06em
            text-transform: uppercase
            color: *color-text-tertiary
            margin-bottom: *sm
          - type: scroll-row
            items:
              - doc: 'Notes on the Silences'
                editor: 'AV'
                time: '3m ago'
              - doc: 'The Slow Web Manifesto'
                editor: 'JT'
                time: '11m ago'
              - doc: 'Reading in the Age of Distraction'
                editor: 'AV'
                time: '27m ago'
              - doc: 'On Craft, Care, and Attention'
                editor: 'MK'
                time: '1h ago'
              - doc: 'Letter From the Editor'
                editor: 'JT'
                time: '2h ago'
            item-style:
              display: inline-block
              margin-right: *lg
              padding: *sm *md
              background: *color-surface
              radius: *md
              font-family: *font-body
              title-size: 13px
              meta-size: 11px
              meta-color: *color-text-tertiary
    responsive-behavior:
      mobile:
        layout: stack
        sections:
          featured-story: { col-span: 4, row-span: auto, padding: *md }
          reading-queue: { col-span: 4, row-span: auto }
          team-pulse: { col-span: 4, row-span: auto }
          recent-activity: { col-span: 4, row-span: auto, grid-position: { col: 1, col-span: 4, row: 4 } }
      tablet:
        sections:
          featured-story: { col-span: 8, row-span: 2 }
          reading-queue: { col-span: 8, row-span: auto }
          team-pulse: { col-span: 8, row-span: auto }
          recent-activity: { col-span: 8, row-span: auto }
      desktop: {}
      wide:
        sections:
          featured-story: { col-span: 7, row-span: 3 }
          padding: *xxl
  - id: mk-02
    name: Editorial Calendar
    layout: bento-grid
    description: Content pipeline view showing stages from pitch to publication. Left column tracks upcoming deadlines; right side shows pitching queue and recently published pieces.
    sections:
      - id: week-overview
        grid-position: { col: 1, col-span: 8, row: 1, row-span: 2 }
        type: calendar-card
        background: *color-surface
        border: 1px solid *color-border-subtle
        radius: *lg
        padding: *lg
        elements:
          - type: section-header
            content: 'This Week'
            font-family: *font-body
            font-size: 11px
            font-weight: 500
            letter-spacing: 0.06em
            text-transform: uppercase
            color: *color-text-tertiary
            margin-bottom: *md
          - type: weekday-labels
            labels: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
            style:
              font-family: *font-body
              font-size: 12px
              color: *color-text-tertiary
              letter-spacing: 0.04em
              padding: *sm 0
              border-bottom: 1px solid *color-border
          - type: day-blocks
            days:
              - date: '23'
                label: Mon
                items:
                  - title: 'The Quiet Reader'
                    status: scheduled
                    editor: 'AV'
              - date: '24'
                label: Tue
                items:
                  - title: 'Infrastructure of Attention'
                    status: scheduled
                    editor: 'JT'
              - date: '25'
                label: Wed
                items:
                  - title: 'Letter From Berlin'
                    status: draft
                    editor: 'MK'
                  - title: 'Editors Roundtable'
                    status: note
              - date: '26'
                label: Thu
                items:
                  - title: 'Against the Feed'
                    status: in-review
                    editor: 'AV'
              - date: '27'
                label: Fri
                items: []
              - date: '28'
                label: Sat
                items: []
              - date: '29'
                label: Sun
                items: []
            block-style:
              padding: *sm
              radius: *sm
              font-family: *font-body
              date-size: 18px
              date-color: *color-text-primary
              title-size: 12px
              title-color: *color-text-secondary
              status-colors:
                scheduled: { dot: '#9e9688' }
                draft: { dot: '#b8a088' }
                in-review: { dot: '#8c7a64' }
                note: { dot: '#c4b8a8', italic: true }
      - id: pitching-queue
        grid-position: { col: 9, col-span: 4, row: 1, row-span: 2 }
        type: list-card
        background: *color-surface
        border: 1px solid *color-border-subtle
        radius: *lg
        padding: *lg
        elements:
          - type: section-header
            content: 'Pitching Queue'
            font-family: *font-body
            font-size: 11px
            font-weight: 500
            letter-spacing: 0.06em
            text-transform: uppercase
            color: *color-text-tertiary
            margin-bottom: *md
          - type: count-badge
            value: 14
            label: 'pending review'
            font-family: *font-mono
            value-size: 32px
            value-color: *color-text-primary
            label-size: 11px
            label-color: *color-text-tertiary
            margin-bottom: *lg
          - type: item-list
            items:
              - title: 'The Case for Slow Publishing'
                author: 'R. Chen'
                submitted: '2 days ago'
                priority: high
              - title: 'Digital Gardens: A Reappraisal'
                author: 'S. Park'
                submitted: '5 days ago'
                priority: medium
              - title: 'On the Beauty of Footnotes'
                author: 'L. Andersen'
                submitted: '1 week ago'
                priority: medium
              - title: 'Reading Rooms in the 21st Century'
                author: 'T. Novak'
                submitted: '1 week ago'
                priority: low
            item-style:
              padding: *sm 0
              border-bottom: 1px solid *color-border-subtle
              font-family: *font-body
              title-size: 14px
              title-color: *color-text-primary
              meta-size: 11px
              meta-color: *color-text-tertiary
              priority-dots:
                high: *color-accent-warm
                medium: *color-accent-soft
                low: *color-border
      - id: recently-published
        grid-position: { col: 1, col-span: 12, row: 3, row-span: 1 }
        type: horizontal-card
        background: *color-surface-raised
        border: 1px solid *color-border-subtle
        radius: *md
        padding: *md *lg
        elements:
          - type: section-header
            content: 'Recently Published'
            font-family: *font-body
            font-size: 11px
            font-weight: 500
            letter-spacing: 0.06em
            text-transform: uppercase
            color: *color-text-tertiary
            margin-bottom: *sm
          - type: horizontal-list
            items:
              - title: 'The Art of the Editorial Note'
                author: 'M. Kaur'
                published: 'Today, 09:00'
                reads: 342
              - title: 'A Quiet Morning'
                author: 'J. Tan'
                published: 'Yesterday'
                reads: 891
              - title: 'On Marginalia'
                author: 'E. Voss'
                published: '2 days ago'
                reads: 1245
              - title: 'The Shelf Beyond the Screen'
                author: 'R. Chen'
                published: '3 days ago'
                reads: 677
            item-style:
              display: inline-block
              margin-right: *xl
              font-family: *font-body
              title-size: 14px
              title-color: *color-text-primary
              meta-size: 11px
              meta-color: *color-text-tertiary
              stat-size: 12px
              stat-color: *color-accent-warm
    responsive-behavior:
      mobile:
        sections:
          week-overview: { col-span: 4, row-span: auto }
          pitching-queue: { col-span: 4, row-span: auto, grid-position: { col: 1, col-span: 4, row: 3 } }
          recently-published: { col-span: 4, row-span: auto, grid-position: { col: 1, col-span: 4, row: 6 } }
      tablet:
        sections:
          week-overview: { col-span: 8, row-span: 2 }
          pitching-queue: { col-span: 8, row-span: auto, grid-position: { col: 1, col-span: 8, row: 3 } }
          recently-published: { col-span: 8, row-span: auto, grid-position: { col: 1, col-span: 8, row: 5 } }
      desktop: {}
      wide: {}
  - id: mk-03
    name: Reference Library
    layout: bento-grid
    description: Curated resource collection organized by thematic clusters. The main reading area occupies the center with category filters to the left and saved excerpts on the right.
    sections:
      - id: category-sidebar
        grid-position: { col: 1, col-span: 3, row: 1, row-span: 3 }
        type: sidebar-card
        background: *color-surface
        border: 1px solid *color-border-subtle
        radius: *lg
        padding: *lg
        elements:
          - type: section-header
            content: 'Categories'
            font-family: *font-body
            font-size: 11px
            font-weight: 500
            letter-spacing: 0.06em
            text-transform: uppercase
            color: *color-text-tertiary
            margin-bottom: *md
          - type: tag-list
            tags:
              - label: 'Essays'
                count: 24
                active: true
              - label: 'Criticism'
                count: 18
                active: false
              - label: 'Interviews'
                count: 11
                active: false
              - label: 'Translations'
                count: 7
                active: false
              - label: 'Letters'
                count: 9
                active: false
              - label: 'Profiles'
                count: 14
                active: false
              - label: 'Reviews'
                count: 22
                active: false
            tag-style:
              display: block
              padding: *sm 0
              font-family: *font-body
              label-size: 14px
              label-color: *color-text-primary
              count-size: 11px
              count-color: *color-text-tertiary
              active-weight: 500
              active-color: *color-accent-warm
              border-bottom: '1px solid #e5e0d7'
      - id: main-reading
        grid-position: { col: 4, col-span: 6, row: 1, row-span: 3 }
        type: reading-card
        background: *color-surface-raised
        border: 1px solid *color-border-subtle
        radius: *lg
        padding: *xl
        elements:
          - type: breadcrumb
            segments:
              - label: 'Essays'
                href: '#'
              - label: 'The Architecture of Silence'
            style:
              font-family: *font-body
              font-size: 12px
              color: *color-text-tertiary
              active-color: *color-text-primary
              margin-bottom: *md
          - type: heading
            content: 'The Architecture of Silence'
            font-family: *font-heading
            font-size: 28px
            line-height: 1.25
            color: *color-text-primary
            margin-bottom: *sm
          - type: meta-line
            content: 'Elena Voss  ·  Published June 2026  ·  4,200 words'
            font-family: *font-body
            font-size: 12px
            color: *color-text-tertiary
            letter-spacing: 0.02em
            margin-bottom: *lg
          - type: body-text
            content: 'The space between words is not empty. It is charged with what the writer chose not to say — and what the reader, in the quiet of the page, might discover for themselves. For the modern editor, trained in an era of maximalist information design, the question is not what to add but what to leave out.'
            font-family: *font-body
            font-size: 15px
            line-height: 1.7
            color: *color-text-secondary
            margin-bottom: *md
          - type: quote-block
            content: '"The story is not in the sentences but in the gaps between them. A paragraph is a room. What you remove from it defines its shape."'
            attribution: '— John Berger, Ways of Seeing'
            style:
              font-family: *font-heading
              font-size: 18px
              line-height: 1.4
              color: *color-text-primary
              border-left: 3px solid *color-accent-warm
              padding-left: *md
              margin: *lg 0
              attribution-size: 12px
              attribution-color: *color-text-tertiary
              attribution-font: *font-body
          - type: body-text
            content: 'This is the fundamental insight that separates the editor from the curator. The curator accumulates. The editor subtracts. And in subtraction, meaning finds its sharpest edge.'
            font-family: *font-body
            font-size: 15px
            line-height: 1.7
            color: *color-text-secondary
      - id: saved-excerpts
        grid-position: { col: 10, col-span: 3, row: 1, row-span: 3 }
        type: notes-card
        background: *color-surface
        border: 1px solid *color-border-subtle
        radius: *lg
        padding: *lg
        elements:
          - type: section-header
            content: 'Saved Excerpts'
            font-family: *font-body
            font-size: 11px
            font-weight: 500
            letter-spacing: 0.06em
            text-transform: uppercase
            color: *color-text-tertiary
            margin-bottom: *md
          - type: excerpt-item
            quote: 'Style is the perfection of a point of view.'
            source: 'Richard Eberhart'
            note: 'On precision vs. ornament'
            style:
              padding: *sm *md
              margin-bottom: *sm
              background: *color-surface-raised
              radius: *md
              border-left: 2px solid *color-accent-soft
              quote-size: 13px
              quote-color: *color-text-primary
              quote-line-height: 1.4
              source-size: 11px
              source-color: *color-text-tertiary
              note-size: 11px
              note-color: *color-accent-warm
              note-font-style: italic
          - type: excerpt-item
            quote: 'The only way to be truly satisfied is to do what you believe is great work.'
            source: 'Steve Jobs'
            note: 'Quality over quantity — editorial lens'
            style:
              padding: *sm *md
              margin-bottom: *sm
              background: *color-surface-raised
              radius: *md
              border-left: 2px solid *color-accent-soft
              quote-size: 13px
              quote-color: *color-text-primary
              source-size: 11px
              source-color: *color-text-tertiary
              note-size: 11px
              note-color: *color-accent-warm
              note-font-style: italic
          - type: excerpt-item
            quote: 'Perfection is achieved not when there is nothing more to add, but when there is nothing left to take away.'
            source: 'Antoine de Saint-Exupery'
            note: 'Central thesis for editorial minimalism'
            style:
              padding: *sm *md
              margin-bottom: *sm
              background: *color-surface-raised
              radius: *md
              border-left: 2px solid *color-accent-soft
              quote-size: 13px
              quote-color: *color-text-primary
              source-size: 11px
              source-color: *color-text-tertiary
              note-size: 11px
              note-color: *color-accent-warm
              note-font-style: italic
    responsive-behavior:
      mobile:
        sections:
          category-sidebar: { col-span: 4, row-span: auto }
          main-reading: { col-span: 4, row-span: auto, grid-position: { col: 1, col-span: 4, row: 3 } }
          saved-excerpts: { col-span: 4, row-span: auto, grid-position: { col: 1, col-span: 4, row: 6 } }
      tablet:
        sections:
          category-sidebar: { col-span: 2, row-span: auto }
          main-reading: { col-span: 6, row-span: auto }
          saved-excerpts: { col-span: 8, row-span: auto, grid-position: { col: 1, col-span: 8, row: 4 }, layout: horizontal }
      desktop: {}
      wide:
        sections:
          category-sidebar: { col-span: 2 }
          main-reading: { col-span: 7 }
          saved-excerpts: { col-span: 3 }
  - id: mk-04
    name: Writing Studio
    layout: bento-grid
    description: Editorial workspace with draft in focus, supporting notes panel, reference list, and a submission tracker. The main composition area occupies the left two-thirds while supporting panels float to the right.
    sections:
      - id: composition-area
        grid-position: { col: 1, col-span: 8, row: 1, row-span: 3 }
        type: editor-card
        background: *color-surface-raised
        border: 1px solid *color-border-subtle
        radius: *lg
        padding: *xl
        elements:
          - type: editor-toolbar
            style:
              display: flex
              justify-content: space-between
              align-items: center
              padding-bottom: *md
              border-bottom: 1px solid *color-border
              margin-bottom: *lg
            actions:
              - label: 'Save Draft'
                variant: primary
                <<: *state-button
              - label: 'Preview'
                variant: secondary
              - label: 'Share'
                variant: secondary
            word-count: '847 / 2,000 words'
            word-count-style:
              font-family: *font-mono
              font-size: 11px
              color: *color-text-tertiary
              letter-spacing: 0.02em
          - type: draft-heading
            content: 'On the Quiet Virtue of Editing'
            font-family: *font-heading
            font-size: 24px
            line-height: 1.25
            color: *color-text-primary
            margin-bottom: *md
            editable: true
          - type: draft-body
            content: 'The best editing is invisible. When done well, the reader never notices the cuts, the rephrasings, the subtle shifts in pacing that make a piece of writing feel inevitable. Editing is not correction. It is revelation — the slow uncovering of what the text was always trying to say.'
            font-family: *font-body
            font-size: 15px
            line-height: 1.7
            color: *color-text-secondary
            editable: true
            margin-bottom: *md
          - type: draft-body
            content: 'This is the distinction that separates the editor from the proofreader. The proofreader catches errors. The editor catches opportunities — moments where a sentence could breathe, where a paragraph could be turned for greater effect, where a single well-chosen word could replace an entire clause.'
            font-family: *font-body
            font-size: 15px
            line-height: 1.7
            color: *color-text-secondary
            editable: true
            margin-bottom: *md
          - type: suggestion-badge
            content: '3 suggestions'
            font-family: *font-body
            font-size: 11px
            color: *color-accent-warm
            letter-spacing: 0.03em
            background: '#f0ebe3'
            radius: *pill
            padding: *xs *sm
            display: inline-block
      - id: notes-panel
        grid-position: { col: 9, col-span: 4, row: 1, row-span: 1 }
        type: notes-card
        background: *color-surface
        border: 1px solid *color-border-subtle
        radius: *lg
        padding: *lg
        elements:
          - type: section-header
            content: 'Working Notes'
            font-family: *font-body
            font-size: 11px
            font-weight: 500
            letter-spacing: 0.06em
            text-transform: uppercase
            color: *color-text-tertiary
            margin-bottom: *md
          - type: note-input
            placeholder: 'Add a note...'
            style:
              font-family: *font-body
              font-size: 13px
              color: *color-text-secondary
              background: *color-surface-raised
              border: 1px solid *color-border
              radius: *md
              padding: *sm *md
              margin-bottom: *md
              width: 100%
          - type: note-list
            notes:
              - author: 'AV'
                text: 'Consider opening with a stronger anecdote — something concrete before the abstract.'
                time: '2h ago'
              - author: 'MK'
                text: 'The Berger quote on p.3 could anchor the second section.'
                time: '1h ago'
              - author: 'JT'
                text: 'Trim the fourth paragraph — it repeats the thesis without advancing it.'
                time: '30m ago'
            note-style:
              padding: *sm 0
              border-bottom: 1px solid *color-border-subtle
              font-family: *font-body
              author-size: 12px
              author-color: *color-accent-warm
              text-size: 13px
              text-color: *color-text-primary
              text-line-height: 1.4
              time-size: 10px
              time-color: *color-text-tertiary
      - id: reference-links
        grid-position: { col: 9, col-span: 4, row: 2, row-span: 1 }
        type: list-card
        background: *color-surface
        border: 1px solid *color-border-subtle
        radius: *lg
        padding: *lg
        elements:
          - type: section-header
            content: 'References'
            font-family: *font-body
            font-size: 11px
            font-weight: 500
            letter-spacing: 0.06em
            text-transform: uppercase
            color: *color-text-tertiary
            margin-bottom: *md
          - type: link-list
            links:
              - title: 'The Elements of Style'
                author: 'Strunk & White'
                type: book
              - title: 'On Writing Well'
                author: 'William Zinsser'
                type: book
              - title: 'Several Short Sentences About Writing'
                author: 'Verlyn Klinkenborg'
                type: book
              - title: 'The Art of the Personal Essay'
                author: 'Phillip Lopate'
                type: anthology
            link-style:
              padding: *sm 0
              border-bottom: 1px solid *color-border-subtle
              font-family: *font-body
              title-size: 13px
              title-color: *color-text-primary
              author-size: 11px
              author-color: *color-text-tertiary
              type-style:
                font-family: *font-body
                font-size: 10px
                letter-spacing: 0.04em
                text-transform: uppercase
                color: *color-accent-warm
      - id: submission-tracker
        grid-position: { col: 9, col-span: 4, row: 3, row-span: 1 }
        type: compact-card
        background: *color-surface
        border: 1px solid *color-border-subtle
        radius: *lg
        padding: *lg
        elements:
          - type: section-header
            content: 'Submission Status'
            font-family: *font-body
            font-size: 11px
            font-weight: 500
            letter-spacing: 0.06em
            text-transform: uppercase
            color: *color-text-tertiary
            margin-bottom: *md
          - type: status-timeline
            stages:
              - label: 'Draft'
                status: complete
                date: 'Jun 24'
              - label: 'Internal Review'
                status: active
                date: 'Jun 25'
              - label: 'Editors Note'
                status: pending
              - label: 'Final Polish'
                status: pending
              - label: 'Published'
                status: pending
            style:
              font-family: *font-body
              label-size: 13px
              label-color: *color-text-primary
              date-size: 11px
              date-color: *color-text-tertiary
              status-colors:
                complete: { dot: *color-accent-warm, line: *color-accent-soft }
                active: { dot: *color-text-primary, line: *color-accent-soft, weight: 500 }
                pending: { dot: *color-border, line: *color-border-subtle }
              padding: *sm 0
    responsive-behavior:
      mobile:
        sections:
          composition-area: { col-span: 4, row-span: auto }
          notes-panel: { col-span: 4, row-span: auto, grid-position: { col: 1, col-span: 4, row: 3 } }
          reference-links: { col-span: 4, row-span: auto, grid-position: { col: 1, col-span: 4, row: 5 } }
          submission-tracker: { col-span: 4, row-span: auto, grid-position: { col: 1, col-span: 4, row: 7 } }
      tablet:
        sections:
          composition-area: { col-span: 8, row-span: 2 }
          notes-panel: { col-span: 8, row-span: auto, grid-position: { col: 1, col-span: 4, row: 3 } }
          reference-links: { col-span: 4, row-span: auto, grid-position: { col: 5, col-span: 4, row: 3 } }
          submission-tracker: { col-span: 8, row-span: auto, grid-position: { col: 1, col-span: 8, row: 5 } }
      desktop: {}
      wide:
        sections:
          composition-area: { col-span: 7 }
          notes-panel: { col-span: 5, grid-position: { col: 8, col-span: 5, row: 1, row-span: 1 } }
          reference-links: { col-span: 5, grid-position: { col: 8, col-span: 5, row: 2, row-span: 1 } }
          submission-tracker: { col-span: 5, grid-position: { col: 8, col-span: 5, row: 3, row-span: 1 } }
```
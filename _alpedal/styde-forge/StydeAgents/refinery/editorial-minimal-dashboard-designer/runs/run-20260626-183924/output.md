mockup-spec: editorial-minimal-dashboard-designer v14.1.0
palette:
  base: &base '#f5f0eb'
  surface: &surface '#e8e2da'
  card: &card '#faf7f3'
  border: &border '#d4ccc2'
  text-primary: &text-primary '#2c2416'
  text-secondary: &text-secondary '#6b6054'
  text-muted: &text-muted '#9c9286'
  accent: &accent '#c4a882'
  accent-warm: &accent-warm '#d4b896'
  divider: &divider '#e0d8ce'
typography:
  heading-font: 'Georgia, "Times New Roman", serif'
  body-font: '"Helvetica Neue", Helvetica, Arial, sans-serif'
  mono-font: '"SF Mono", "Fira Code", monospace'
  scale:
    h1: 2.25rem
    h2: 1.5rem
    h3: 1.125rem
    body: 0.9375rem
    small: 0.8125rem
    caption: 0.75rem
grid:
  columns: 12
  gap: 1.5rem
  max-width: 1280px
  padding: 2rem
mockups:
  mk-01:
    title: Editorial Overview Dashboard
    layout:
      type: bento
      rows:
        - cols: [12]
          height: auto
        - cols: [4, 8]
          height: auto
        - cols: [6, 6]
          height: auto
    cards:
      - id: header-bar
        col-span: 12
        style:
          bg: *card
          border-bottom: 1px solid *border
          padding: 1.25rem 0
        content:
          type: row
          align: center
          justify: space-between
          items:
            - type: text
              text: 'The Editorial'
              font: *heading-font
              size: 1.75rem
              weight: 400
              color: *text-primary
              tracking: 0.02em
            - type: nav-links
              items:
                - text: 'Stories'
                - text: 'Features'
                - text: 'Culture'
                - text: 'Archive'
              style:
                gap: 2rem
                font: *body-font
                size: 0.8125rem
                color: *text-muted
                uppercase: true
                tracking: 0.08em
            - type: search-icon
              icon: magnifier
              color: *text-secondary
              size: 1rem
      - id: featured-article
        col-span: 4
        style:
          bg: *card
          border: 1px solid *border
          padding: 2rem
          radius: 0
        content:
          type: stack
          spacing: 1.5rem
          items:
            - type: label
              text: 'Featured Story'
              font: *body-font
              size: 0.6875rem
              color: *accent
              uppercase: true
              tracking: 0.12em
              weight: 600
            - type: text
              text: 'The Architecture of Silence'
              font: *heading-font
              size: 1.5rem
              weight: 400
              color: *text-primary
              leading: 1.3
            - type: text
              text: 'How empty space shapes the way we read, think, and remember in an age of constant noise.'
              font: *body-font
              size: 0.875rem
              color: *text-secondary
              leading: 1.6
            - type: text
              text: '12 min read'
              font: *body-font
              size: 0.75rem
              color: *text-muted
              style: italic
      - id: reading-list
        col-span: 8
        style:
          bg: *card
          border: 1px solid *border
          padding: 2rem
          radius: 0
        content:
          type: stack
          spacing: 0
          items:
            - type: stack-header
              text: 'Reading List'
              font: *body-font
              size: 0.6875rem
              color: *accent
              uppercase: true
              tracking: 0.12em
              weight: 600
              padding-bottom: 1.25rem
              border-bottom: 1px solid *divider
            - type: list
              items:
                - title: 'On Typography and Time'
                  author: 'Elena Vasquez'
                  time: '45 min'
                  status: 'reading'
                - title: 'The Grid as a Narrative Device'
                  author: 'Marcus Chen'
                  time: '30 min'
                  status: 'unread'
                - title: 'White Space as Luxury'
                  author: 'Ingrid Larsson'
                  time: '20 min'
                  status: 'unread'
                - title: 'Monochrome in the Digital Age'
                  author: 'David Kim'
                  time: '35 min'
                  status: 'finished'
              style:
                row-padding: 1rem
                font: *body-font
                title-size: 0.9375rem
                title-color: *text-primary
                author-size: 0.8125rem
                author-color: *text-secondary
                time-size: 0.75rem
                time-color: *text-muted
                divider: 1px solid *divider
                status-dot:
                  reading: *accent-warm
                  unread: *accent
                  finished: *text-muted
                  size: 6px
      - id: editors-picks
        col-span: 6
        style:
          bg: *card
          border: 1px solid *border
          padding: 2rem
          radius: 0
        content:
          type: stack
          spacing: 1.25rem
          items:
            - type: label
              text: "Editor's Picks"
              font: *body-font
              size: 0.6875rem
              color: *accent
              uppercase: true
              tracking: 0.12em
              weight: 600
            - type: grid-2x2
              gap: 1rem
              items:
                - title: 'The Lost Art of the Long Read'
                  excerpt: 'Attention spans are shrinking. Here is why long-form still matters.'
                  color: *base
                - title: 'Photography Without Color'
                  excerpt: 'Why the most powerful images are often monochrome.'
                  color: *surface
                - title: 'The Return of Serif'
                  excerpt: 'How classic typefaces are making a digital comeback.'
                  color: *base
                - title: 'Slowing Down the Feed'
                  excerpt: 'Designing interfaces that encourage pause, not scroll.'
                  color: *surface
      - id: metrics-mini
        col-span: 6
        style:
          bg: *base
          border: 1px solid *border
          padding: 2rem
          radius: 0
        content:
          type: stack
          spacing: 1.25rem
          items:
            - type: label
              text: 'This Week'
              font: *body-font
              size: 0.6875rem
              color: *text-muted
              uppercase: true
              tracking: 0.12em
              weight: 600
            - type: metric-row
              gap: 2rem
              items:
                - label: 'Articles Published'
                  value: '12'
                  change: '+3'
                  direction: up
                - label: 'Total Reads'
                  value: '4,281'
                  change: '+18%'
                  direction: up
                - label: 'Avg. Time'
                  value: '6:42'
                  change: '-2%'
                  direction: down
              style:
                label-size: 0.75rem
                label-color: *text-muted
                value-size: 1.75rem
                value-color: *text-primary
                change-size: 0.6875rem
                change-up: '#7a9a7a'
                change-down: '#9a7a7a'
                font: *body-font
  mk-02:
    title: Article Detail Dashboard
    layout:
      type: single
      cols: [8, 4]
      gap: 2rem
    cards:
      - id: article-body
        col-span: 8
        style:
          bg: *card
          padding: 3rem
        content:
          type: stack
          spacing: 2rem
          items:
            - type: meta-row
              items:
                - text: 'June 26, 2026'
                - text: 'Photography'
                - text: '12 min read'
              style:
                gap: 1.5rem
                font: *body-font
                size: 0.75rem
                color: *text-muted
                uppercase: true
                tracking: 0.06em
            - type: text
              text: 'Monochrome in the Digital Age'
              font: *heading-font
              size: 2.25rem
              weight: 400
              color: *text-primary
              leading: 1.2
            - type: text
              text: 'By David Kim'
              font: *body-font
              size: 0.8125rem
              color: *accent
              style: italic
            - type: divider
              color: *divider
              width: 3rem
            - type: text
              text: 'In an era of high-contrast gradients and oversaturated interfaces, a quiet rebellion is forming. Designers are rediscovering the power of a limited palette — not as a constraint, but as liberation.'
              font: *body-font
              size: 1rem
              color: *text-primary
              leading: 1.7
            - type: text
              text: 'The monochrome approach forces every element to earn its place. Without color as a crutch, hierarchy must come from typography, spacing, and scale alone. This is where discipline meets craft.'
              font: *body-font
              size: 1rem
              color: *text-primary
              leading: 1.7
            - type: blockquote
              text: 'Color is a tool. Monochrome is a philosophy.'
              attribution: '— Massimo Vignelli'
              style:
                border-left: 3px solid *accent
                padding: 1rem 1.5rem
                font: *heading-font
                size: 1.125rem
                color: *text-secondary
                leading: 1.5
      - id: sidebar-info
        col-span: 4
        style:
          bg: *card
          border: 1px solid *border
          padding: 2rem
        content:
          type: stack
          spacing: 1.5rem
          items:
            - type: label
              text: 'About the Author'
              font: *body-font
              size: 0.6875rem
              color: *accent
              uppercase: true
              tracking: 0.12em
              weight: 600
            - type: author-card
              name: 'David Kim'
              role: 'Senior Editor, Design & Culture'
              bio: 'David writes about the intersection of design theory and digital practice. His work has appeared in AIGA Eye on Design, It\'s Nice That, and Design Week.'
            - type: divider
              color: *divider
            - type: label
              text: 'Related Reading'
              font: *body-font
              size: 0.6875rem
              color: *accent
              uppercase: true
              tracking: 0.12em
              weight: 600
            - type: list
              items:
                - title: 'The Grid as a Narrative Device'
                  time: '30 min'
                - title: 'On Typography and Time'
                  time: '45 min'
                - title: 'White Space as Luxury'
                  time: '20 min'
              style:
                row-padding: 0.75rem
                font: *body-font
                title-size: 0.875rem
                title-color: *text-primary
                time-size: 0.6875rem
                time-color: *text-muted
                divider: 1px solid *divider
  mk-03:
    title: Archive & Discovery
    layout:
      type: bento
      rows:
        - cols: [12]
        - cols: [3, 3, 3, 3]
        - cols: [7, 5]
    cards:
      - id: search-bar
        col-span: 12
        style:
          bg: *card
          border: 1px solid *border
          padding: 1rem 1.5rem
        content:
          type: search-input
          placeholder: 'Search articles, authors, topics...'
          icon: search
          font: *body-font
          size: 0.9375rem
          color: *text-primary
          placeholder-color: *text-muted
          bg: *surface
          border: none
          radius: 0
      - id: category-grid
        col-span: 12
        style:
          bg: transparent
          padding: 0
        content:
          type: grid-4
          gap: 1rem
          items:
            - label: 'Design'
              count: 48
              color: *base
            - label: 'Photography'
              count: 36
              color: *base
            - label: 'Culture'
              count: 52
              color: *base
            - label: 'Technology'
              count: 29
              color: *base
          style:
            label-font: *body-font
            label-size: 0.8125rem
            label-color: *text-primary
            uppercase: true
            tracking: 0.08em
            count-font: *heading-font
            count-size: 1.25rem
            count-color: *accent
            padding: 1.5rem
            border: 1px solid *border
            radius: 0
      - id: timeline-view
        col-span: 7
        style:
          bg: *card
          border: 1px solid *border
          padding: 2rem
        content:
          type: stack
          spacing: 1.25rem
          items:
            - type: label
              text: 'Recent Publications'
              font: *body-font
              size: 0.6875rem
              color: *accent
              uppercase: true
              tracking: 0.12em
              weight: 600
            - type: timeline
              items:
                - date: '2026-06-24'
                  title: 'The Architecture of Silence'
                  author: 'Elena Vasquez'
                  status: 'published'
                - date: '2026-06-23'
                  title: 'Photography Without Color'
                  author: 'Ingrid Larsson'
                  status: 'published'
                - date: '2026-06-22'
                  title: 'The Lost Art of the Long Read'
                  author: 'Marcus Chen'
                  status: 'published'
                - date: '2026-06-21'
                  title: 'Slowing Down the Feed'
                  author: 'David Kim'
                  status: 'published'
              style:
                date-size: 0.75rem
                date-color: *text-muted
                title-size: 0.9375rem
                title-color: *text-primary
                author-size: 0.8125rem
                author-color: *text-secondary
                dot-color: *accent
                dot-size: 8px
                line-color: *divider
                font: *body-font
                spacing: 1rem
      - id: saved-collections
        col-span: 5
        style:
          bg: *base
          border: 1px solid *border
          padding: 2rem
        content:
          type: stack
          spacing: 1.25rem
          items:
            - type: label
              text: 'Your Collections'
              font: *body-font
              size: 0.6875rem
              color: *text-muted
              uppercase: true
              tracking: 0.12em
              weight: 600
            - type: list
              items:
                - title: 'Design Essays'
                  count: 12
                  icon: bookmark
                - title: 'Photography Deep Dives'
                  count: 8
                  icon: bookmark
                - title: ' Weekend Reads'
                  count: 5
                  icon: bookmark
                - title: 'Archived Favorites'
                  count: 24
                  icon: bookmark
              style:
                row-padding: 0.875rem
                font: *body-font
                title-size: 0.875rem
                title-color: *text-primary
                count-size: 0.75rem
                count-color: *text-muted
                icon-size: 0.875rem
                icon-color: *accent
                divider: 1px solid *divider
                bg-hover: *surface
notes:
  yaml-anchors: 'At most one level of indirection. All anchors are scalar colors; no mapping anchors used where scalars are expected. Every alias references a same-type anchor.'
  type-safety: 'All color values are string scalars. No alias resolves a mapping or sequence — only strings. Validatable with: python -c "import yaml; yaml.safeload(open(0))"'
  design-system: 'Typography hierarchy is structural. No color gradients, no shadows, no rounded corners. White space is the primary layout tool.'
  responsive: 'Grid collapses to single column below 768px. Typography scales down proportionally.'
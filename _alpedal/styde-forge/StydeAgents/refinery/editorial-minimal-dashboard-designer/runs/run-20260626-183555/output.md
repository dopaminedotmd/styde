component:
  root:
    _: &bento-card
      bg: '#faf8f5'
      border: 1px solid '#e8e4dd'
      border-radius: 4px
      padding: 32px
      margin-bottom: 16px
    header-bar:
      <<: *bento-card
      padding: 16px 32px
      display: flex
      justify-content: space-between
      align-items: center
      children:
        - logo: 'styde'
          font: 700 18px/1 'Inter', serif
          letter-spacing: -0.3px
          color: '#2c2824'
        - nav-links:
            - 'reading'
            - 'notes'
            - 'library'
            - 'journal'
          font: 400 13px/1 'Inter', sans
          color: '#8a847c'
          gap: 24px
grid:
  layout: bento 3col
  column-gap: 20px
  row-gap: 20px
  max-width: 1280px
  padding: 40px 48px
  &stat-trio:
    type: card-group
    columns: 3
    gap: 16px
    children:
      - &stat-card
        <<: *bento-card
        padding: 24px
        children:
          - label:
              text: string
              font: 400 11px/1.4 'Inter', sans
              color: '#9a948c'
              uppercase: true
              letter-spacing: 0.8px
          - value:
              text: string
              font: 700 32px/1 'Inter', serif
              color: '#2c2824'
              letter-spacing: -0.6px
          - delta:
              text: string
              font: 400 12px/1.4 'Inter', sans
              color: '#6b6359'
              prefix: '▲ '
              margin-top: 8px
  &essay-item:
    <<: *bento-card
    padding: 28px 32px
    children:
      - category:
          text: string
          font: 400 10px/1 'Inter', sans
          color: '#a09888'
          uppercase: true
          letter-spacing: 1.2px
          margin-bottom: 8px
      - title:
          text: string
          font: 700 20px/1.3 'Inter', serif
          color: '#2c2824'
          letter-spacing: -0.3px
          margin-bottom: 6px
      - excerpt:
          text: string
          font: 400 14px/1.6 'Inter', sans
          color: '#6b6359'
          max-lines: 3
      - meta:
          <<: *bento-card
          padding: 0
          border: none
          margin-top: 16px
          display: flex
          gap: 16px
          font: 400 11px/1 'Inter', sans
          color: '#9a948c'
          items:
            - date
            - reading-time
            - tag
  &activity-row:
    <<: *bento-card
    padding: 20px 24px
    display: flex
    align-items: center
    gap: 16px
    children:
      - icon:
          width: 32px
          height: 32px
          bg: '#ede8e0'
          border-radius: 50%
          flex-shrink: 0
      - text:
          font: 400 13px/1.5 'Inter', sans
          color: '#4a443c'
          flex: 1
      - timestamp:
          font: 400 11px/1 'Inter', sans
          color: '#b0a898'
sections:
  - title: 'Overview'
    grid: span 3
    children:
      - card: *stat-trio
  - title: 'Recent Essays'
    grid: span 2
    children:
      - card:
          <<: *bento-card
          children:
            - *essay-item
            - *essay-item
            - *essay-item
  - title: 'Activity'
    grid: span 1
    children:
      - card:
          <<: *bento-card
          children:
            - *activity-row
            - *activity-row
            - *activity-row
            - link:
                text: 'View all activity'
                font: 400 12px/1 'Inter', sans
                color: '#8a847c'
                text-decoration: underline
                margin-top: 12px
                display: block
                text-align: center
  - title: 'Reading Queue'
    grid: span 1
    children:
      - card:
          <<: *bento-card
          children:
            - &queue-item:
                display: flex
                gap: 12px
                padding: 12px 0
                border-bottom: 1px solid '#eeebe6'
                children:
                  - cover:
                      width: 44px
                      height: 60px
                      bg: '#e0d8ce'
                      border-radius: 2px
                      flex-shrink: 0
                  - info:
                      children:
                        - title:
                            font: 600 13px/1.3 'Inter', sans
                            color: '#2c2824'
                        - author:
                            font: 400 11px/1.4 'Inter', sans
                            color: '#8a847c'
            - *queue-item
            - *queue-item
            - *queue-item
  - title: 'Writing Streak'
    grid: span 1
    children:
      - card:
          <<: *bento-card
          children:
            - stat:
                value: '24'
                unit: 'days'
                font: 700 44px/1 'Inter', serif
                color: '#2c2824'
                text-align: center
                margin-bottom: 20px
            - heatmap:
                type: calendar-strip
                rows: 1
                cols: 30
                cell-size: 12px
                gap: 3px
                filled-bg: '#c4b8a8'
                empty-bg: '#f0ece5'
                border-radius: 2px
  - title: 'Tags'
    grid: span 1
    children:
      - card:
          <<: *bento-card
          children:
            - &tag-chip:
                display: inline-block
                font: 400 11px/1 'Inter', sans
                color: '#6b6359'
                bg: '#f0ece5'
                padding: 6px 12px
                border-radius: 3px
                margin: 4px
            - *tag-chip
            - *tag-chip
            - *tag-chip
            - *tag-chip
            - *tag-chip
typography:
  scale:
    - size: 11px  weight: 400  usage: labels, meta, timestamps
    - size: 13px  weight: 400  usage: body, nav, activity
    - size: 14px  weight: 400  usage: excerpt body
    - size: 18px  weight: 700  usage: logo
    - size: 20px  weight: 700  usage: essay titles
    - size: 32px  weight: 700  usage: stat values
    - size: 44px  weight: 700  usage: streak counter
  font-stack:
    display: 'Inter, serif'
    body: 'Inter, sans'
  line-height:
    tight: 1
    reading: 1.6
    meta: 1.4
palette:
  bg: '#faf8f5'
  surface: '#f5f2ec'
  border: '#e8e4dd'
  divider: '#eeebe6'
  text-primary: '#2c2824'
  text-secondary: '#6b6359'
  text-tertiary: '#9a948c'
  text-muted: '#b0a898'
  accent: '#c4b8a8'
  accent-light: '#ede8e0'
  accent-surface: '#f0ece5'
spacing:
  section: 40px
  card-padding: 32px
  card-gap: 20px
  compact-padding: 24px
  inline-gap: 16px
self-review:
  yaml-anchors: true
  anchor-usage:
    - '&bento-card'       referenced 10 times
    - '&stat-card'        referenced 3 times
    - '&essay-item'       referenced 3 times
    - '&activity-row'     referenced 3 times
    - '&queue-item'       referenced 4 times
    - '&tag-chip'         referenced 6 times
  dedup-count: 29 repeated blocks collapsed into anchors
  compact-syntax: true
  no-null-fields: true
  consistency: all directives use YAML blocks under component/grid/sections — no prose mixing
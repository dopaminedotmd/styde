mockup-01: article-content-hub
  viewport: 1440x900
  grid: 12-column bento, 24px gutter, 32px outer margin
  zones:
    zone-a: masthead-ribbon
      top: 0 left: 0 width: 1440 height: 64
      bg: '#f5f2ed' border-bottom: 1px solid '#e0d8cd'
      elements:
        - logo-type: gt-pressura-mono 16/24 #3c3836 weight-500 tracking-50
        - breadcrumb: gt-pressura-mono 13/20 #7a6f64 tracking-25
        - status-pill: 40x20 radius-10 bg '#e8e3da' text #5a4f44 11/16 gt-pressura-mono tracking-50
    zone-b: filter-bar
      top: 64 left: 32 width: 1376 height: 56
      bg: transparent border-bottom: 1px solid '#ece6dd'
      elements:
        - segment-control: 3 buttons, each 120x36 radius-6
          active: bg '#3c3836' text '#f5f2ed' gt-pressura-mono 13/20 tracking-50
          inactive: bg transparent text '#8a7f74' gt-pressura-mono 13/20 tracking-25
          hover: bg '#e8e3da' text '#3c3836' transition 150ms
        - search-field: 280x36 radius-6 border 1px '#d4ccc0' bg '#faf8f5'
          placeholder: gt-pressura-mono 13/20 #a69b8f tracking-25
          focus: border '#8a7f74' outline none shadow 0 0 0 2px '#e0d8cd'
    zone-c: bento-grid
      top: 136 left: 32 width: 1376 height: 728
      bg: '#faf8f5'
      cards:
        - card-01: featured-article-preview
          grid-position: col-1-6 row-1-4
          width: 660 height: 352 padding: 32
          bg: '#f5f2ed' radius-8 border 1px '#ece6dd'
          image-placeholder: 660x160 radius-6 bg '#e0d8cd'
          headline: gt-pressura-regular 28/36 #2c2824 tracking--10 weight-400
          dek: gt-pressura-regular 16/24 #7a6f64 tracking-0
          meta-row: gt-pressura-mono 12/16 #8a7f74 tracking-50
          hover: translateY -2px shadow 0 8 24 '#d4ccc0'33 transition 200ms
        - card-02: recent-publish-stack
          grid-position: col-7-12 row-1-2
          width: 660 height: 168 padding: 24
          bg: '#ffffff' radius-8 border 1px '#ece6dd'
          header: gt-pressura-mono 11/16 #8a7f74 tracking-75 uppercase
          list-items: 3 rows, each 28px, gt-pressura-regular 15/22 #3c3836
          divider: 1px solid '#f0ebe3'
        - card-03: scheduled-content
          grid-position: col-7-10 row-3-4
          width: 436 height: 168 padding: 24
          bg: '#ffffff' radius-8 border 1px '#ece6dd'
          timeline-dot: 8x8 radius-4 bg '#c4b8a8' margin-right 12
          label: gt-pressura-mono 12/16 #7a6f64 tracking-25
          value: gt-pressura-regular 18/24 #3c3836
        - card-04: quick-stats
          grid-position: col-11-12 row-3-4
          width: 216 height: 168 padding: 20
          bg: '#f5f2ed' radius-8 border 1px '#ece6dd'
          stat-number: gt-pressura-regular 36/40 #2c2824
          stat-label: gt-pressura-mono 11/16 #8a7f74 tracking-50
          micro-trend: gt-pressura-mono 11/16 '#9a8f84' tracking-25
      gap: 16px between cards, 16px between rows
    zone-d: bottom-rail
      top: 864 left: 32 width: 1376 height: 36
      bg: transparent border-top: 1px solid '#ece6dd'
      pagination: gt-pressura-mono 12/16 #8a7f74 tracking-50
      hover: text '#3c3836' transition 150ms
mockup-02: editorial-calendar
  viewport: 1440x900
  grid: single-column with sidebar, 24px gutter
  zones:
    zone-a: calendar-header
      top: 0 left: 0 width: 1440 height: 72
      bg: '#f5f2ed' border-bottom: 1px solid '#e0d8cd'
      month-label: gt-pressura-regular 32/40 #2c2824 tracking--15
      nav-arrows: 36x36 radius-6 bg '#ece6dd' hover bg '#e0d8cd' transition 150ms
      week-toggle: gt-pressura-mono 12/16 #7a6f64 tracking-50
        active: bg '#3c3836' text '#f5f2ed' radius-6
    zone-b: week-columns
      top: 72 left: 240 width: 1168 height: 792
      bg: '#faf8f5'
      day-columns: 7 columns, each 158px width
      header-row: height 40px bg '#f5f2ed'
        day-name: gt-pressura-mono 11/16 #8a7f64 tracking-75 uppercase
        day-number: gt-pressura-regular 16/20 #3c3836
        today-badge: 24x24 radius-12 bg '#3c3836' text '#f5f2ed' 12/16
      time-slots: 12 rows, each 56px
        hour-marker: gt-pressura-mono 10/14 #a69b8f tracking-50 border-top 1px '#ece6dd'
      draft-blocks: each 158x28 radius-4 padding 4
        status-published: bg '#e0d8cd' text #3c3836
        status-draft: bg '#f0ebe3' text #7a6f64
        status-review: bg '#d4ccc0' text #3c3836
        hover: shadow 0 2 8 '#c4b8a8'44 cursor pointer transition 150ms
        label: gt-pressura-mono 10/14 #3c3836 tracking-25 truncate
      current-time-line: 1px solid '#c4b8a8' z-index 10
    zone-c: sidebar-inspector
      top: 72 left: 0 width: 240 height: 792
      bg: '#ffffff' border-right: 1px solid '#ece6dd' padding 24
      section-label: gt-pressura-mono 11/16 #8a7f64 tracking-75 uppercase margin-bottom 16
      detail-field: margin-bottom 12
        label: gt-pressura-mono 10/14 #a69b8f tracking-50
        value: gt-pressura-regular 14/20 #3c3836
        inline-editing: focus border-bottom 1px '#d4ccc0' bg transparent
      action-button: 192x36 radius-6 bg '#3c3836' text '#f5f2ed' gt-pressura-mono 12/16 tracking-50
        hover: bg '#2c2824' transition 150ms
        disabled: bg '#e0d8cd' text '#a69b8f'
mockup-03: reader-analytics
  viewport: 1440x900
  grid: 12-column bento, 24px gutter, 32px outer margin
  zones:
    zone-a: analytics-kpi-ribbon
      top: 0 left: 0 width: 1440 height: 100
      bg: '#f5f2ed' border-bottom: 1px solid '#e0d8cd' padding 32 32 0 32
      kpi-cards: 4 items, each 324x68
        metric-value: gt-pressura-regular 36/40 #2c2824 tracking--10
        metric-label: gt-pressura-mono 11/16 #8a7f64 tracking-50
        metric-delta: gt-pressura-mono 12/16 tracking-25
          positive: '#5a7a5a'
          negative: '#8a5a5a'
          neutral: '#a69b8f'
        sparkline: 80x24 stroke '#c4b8a8' stroke-width 1.5 fill none
    zone-b: main-chart-area
      top: 100 left: 32 width: 912 height: 432 padding 32
      bg: '#ffffff' radius-8 border 1px '#ece6dd'
      chart-header: gt-pressura-mono 13/20 #8a7f64 tracking-50 margin-bottom 16
      y-axis: gt-pressura-mono 10/14 #a69b8f tracking-25
      x-axis-labels: gt-pressura-mono 10/14 #a69b8f tracking-25
      line-series: stroke '#7a6f64' stroke-width 2 fill none
      line-series-hover: stroke '#3c3836' stroke-width 2.5
      area-fill: rgba 122 111 100 0.08
      dot: 6x6 radius-3 fill '#7a6f64' hover radius-5 fill '#3c3836' transition 120ms
      tooltip: 180x56 radius-6 bg '#3c3836' text '#f5f2ed' padding 12
        tooltip-value: gt-pressura-regular 18/24 #f5f2ed
        tooltip-label: gt-pressura-mono 10/14 '#c4b8a8' tracking-25
    zone-c: sidebar-breakdown
      top: 100 left: 972 width: 436 height: 432 padding 24
      bg: '#ffffff' radius-8 border 1px '#ece6dd'
      tab-header: 2 tabs, gt-pressura-mono 12/16 tracking-50
        active: text '#3c3836' border-bottom 2px '#3c3836' padding-bottom 8
        inactive: text '#a69b8f' hover text '#7a6f64' transition 150ms
      list-row: height 40px border-bottom 1px '#f0ebe3'
        row-label: gt-pressura-regular 14/20 #3c3836
        row-value: gt-pressura-mono 13/20 #7a6f64 tracking-25
        row-bar: height 4px radius-2 bg '#ece6dd' fill '#c4b8a8'
          animate width 400ms ease-out
    zone-d: bottom-insights-strip
      top: 548 left: 32 width: 1376 height: 316 padding 24
      bg: '#f5f2ed' radius-8 border 1px '#ece6dd'
      insight-card: 3 items, each 425x268
        icon-area: 32x32 radius-6 bg '#ece6dd' text '#7a6f64'
        card-title: gt-pressura-regular 18/24 #2c2824 tracking--5
        card-summary: gt-pressura-regular 14/22 #7a6f64 tracking-0
        cta-link: gt-pressura-mono 12/16 #3c3836 tracking-50 hover underline decoration '#c4b8a8'
      gap: 16px between cards
mockup-04: storyboard-visual-editor
  viewport: 1440x900
  grid: 12-column, 0px gutter (full-bleed canvas)
  zones:
    zone-a: canvas-toolbar
      top: 0 left: 0 width: 1440 height: 56
      bg: '#f5f2ed' border-bottom: 1px solid '#e0d8cd' padding 12 32
      tool-group: 32x32 radius-6 bg transparent icon '#7a6f64'
        hover: bg '#ece6dd' text '#3c3836' transition 120ms
        active: bg '#3c3836' text '#f5f2ed'
      divider: 1px solid '#e0d8cd' height 24 margin 0 12
      zoom-control: gt-pressura-mono 12/16 #7a6f64 tracking-25
        input: 48x24 text-align center bg '#faf8f5' border 1px '#d4ccc0' radius-4
    zone-b: canvas-area
      top: 56 left: 0 width: 1440 height: 700
      bg: '#f0ebe3'
      page-mockup: 1012x660 bg '#ffffff' shadow 0 4 32 '#c4b8a8'33 margin auto
      drag-handle: 6x48 radius-3 bg '#c4b8a8' hover bg '#7a6f64' cursor-col-resize transition 150ms
      block-selected: outline 2px '#7a6f64' outline-offset 2
      block-dragging: opacity 0.85 shadow 0 8 36 '#7a6f64'22 cursor-grabbing
      text-block-editable: caret '#3c3836' selection-bg '#e0d8cd'
      drop-indicator: 2px dashed '#7a6f64' z-index 20
    zone-c: properties-panel
      top: 756 left: 0 width: 1440 height: 144
      bg: '#ffffff' border-top: 1px solid '#ece6dd' padding 16 32
      property-group: inline-flex gap 24
      label: gt-pressura-mono 10/14 #a69b8f tracking-50 margin-bottom 4
      input-mini: 64x28 radius-4 border 1px '#d4ccc0' bg '#faf8f5'
        focus: border '#7a6f64' outline none
      color-swatch: 28x28 radius-4 border 1px '#e0d8cd'
        selected: outline 2px '#3c3836' outline-offset 2
      font-select: gt-pressura-mono 13/20 #3c3836 bg '#faf8f5' border 1px '#d4ccc0' radius-4
        dropdown: bg '#ffffff' border 1px '#ece6dd' radius-6 shadow 0 4 16 '#c4b8a8'22
mockup-05: author-contributor-roster
  viewport: 1440x900
  grid: 12-column bento, 24px gutter, 32px outer margin
  zones:
    zone-a: roster-header
      top: 0 left: 0 width: 1440 height: 72
      bg: '#f5f2ed' border-bottom: 1px solid '#e0d8cd' padding 16 32
      title: gt-pressura-regular 28/36 #2c2824 tracking--10
      count-badge: 32x20 radius-10 bg '#ece6dd' text '#5a4f44' gt-pressura-mono 11/16 tracking-50
      add-button: 120x36 radius-6 bg '#3c3836' text '#f5f2ed' gt-pressura-mono 12/16 tracking-50
        hover: bg '#2c2824' transition 150ms
    zone-b: author-grid
      top: 72 left: 32 width: 1376 height: 732
      bg: '#faf8f5'
      author-card: 6 items, each 324x236 padding 24
        bg: '#ffffff' radius-8 border 1px '#ece6dd'
        avatar: 48x48 radius-24 bg '#e0d8cd'
        initials: gt-pressura-mono 14/20 #7a6f64 tracking-25
        name: gt-pressura-regular 18/24 #2c2824 tracking--5 margin-top 12
        role: gt-pressura-mono 11/16 #8a7f64 tracking-50
        bio-preview: gt-pressura-regular 13/20 #7a6f64 line-clamp-2 margin-top 8
        stat-row: gt-pressura-mono 11/16 #a69b8f tracking-25 margin-top 12
          stat-icon: 14x14 '#c4b8a8'
        hover: translateY -2px shadow 0 8 24 '#d4ccc0'33 transition 200ms
        status-dot: 8x8 radius-4 margin-left 8
          active: bg '#5a7a5a'
          away: bg '#c4a85a'
          inactive: bg '#d4ccc0'
      gap: 16px between cards, 16px between rows
    zone-c: filter-sort-rail
      top: 72 left: 0 width: 32 height: 732
      writing-mode: vertical-lr gt-pressura-mono 10/14 #a69b8f tracking-75
      expand-hover: width 192 bg '#ffffff' border-right 1px '#ece6dd' padding 24 shadow 4 0 24 '#c4b8a8'22
        filter-label: gt-pressura-mono 11/16 #8a7f64 tracking-50 margin-bottom 12
        filter-option: gt-pressura-regular 14/20 #3c3836 cursor pointer
          hover: text '#7a6f64'
          selected: text '#3c3836' font-weight-500
mockup-06: media-library
  viewport: 1440x900
  grid: 12-column, 24px gutter, 32px outer margin
  zones:
    zone-a: library-topbar
      top: 0 left: 0 width: 1440 height: 64
      bg: '#f5f2ed' border-bottom: 1px solid '#e0d8cd' padding 14 32
      upload-button: 140x36 radius-6 bg '#3c3836' text '#f5f2ed'
        icon: 16x16 stroke '#f5f2ed' stroke-width 1.5
        label: gt-pressura-mono 12/16 tracking-50
        hover: bg '#2c2824' transition 150ms
      view-toggle: 2 buttons, each 36x36 radius-6 bg transparent
        active: bg '#ece6dd' icon '#3c3836'
        hover: bg '#e0d8cd' transition 120ms
    zone-b: asset-grid
      top: 64 left: 32 width: 1068 height: 740 padding 4
      bg: '#faf8f5'
      asset-card: 12 items, each 168x192 radius-6
        bg: '#ffffff' border 1px '#ece6dd' overflow hidden
        thumbnail: 168x112 bg '#f0ebe3'
          hover: overlay rgba 60 56 54 0.04
          selected: overlay rgba 60 56 54 0.08 border 2px '#7a6f64'
        asset-info: padding 8
          filename: gt-pressura-mono 10/14 #3c3836 tracking-25 truncate
          metadata: gt-pressura-mono 9/12 #a69b8f tracking-25
        checkbox: 16x16 radius-4 border 1.5px '#d4ccc0'
          checked: bg '#3c3836' border '#3c3836' tick '#f5f2ed'
        hover: translateY -1px shadow 0 4 12 '#d4ccc0'33 transition 150ms
      gap: 8px between cards, 8px between rows
    zone-c: asset-detail
      top: 64 left: 1128 width: 280 height: 740 padding 20
      bg: '#ffffff' border-left 1px '#ece6dd'
      preview: 240x160 radius-6 bg '#f0ebe3'
      detail-label: gt-pressura-mono 10/14 #a69b8f tracking-50 margin-top 16
      detail-value: gt-pressura-regular 13/20 #3c3836 margin-bottom 8
      alt-text-field: 240x56 radius-4 border 1px '#d4ccc0' bg '#faf8f5' padding 8
        gt-pressura-regular 13/20 #3c3836
        focus: border '#7a6f64' outline none
      replace-button: 240x32 radius-4 border 1px '#d4ccc0' bg transparent
        gt-pressura-mono 11/16 #7a6f64 tracking-50
        hover: bg '#f5f2ed' border '#c4b8a8' transition 150ms
mockup-07: newsletter-composer
  viewport: 1440x900
  grid: 12-column, 24px gutter, 32px outer margin
  zones:
    zone-a: composer-header
      top: 0 left: 0 width: 1440 height: 64
      bg: '#f5f2ed' border-bottom: 1px solid '#e0d8cd' padding 14 32
      back-arrow: 32x32 radius-6 bg transparent icon '#7a6f64'
        hover: bg '#ece6dd' transition 120ms
      subject-line: gt-pressura-regular 20/28 #2c2824 tracking--5 border none bg transparent
        placeholder: text '#a69b8f'
        focus: outline none border-bottom 1px '#d4ccc0'
      send-button: 100x36 radius-6 bg '#3c3836' text '#f5f2ed' gt-pressura-mono 12/16 tracking-50
        hover: bg '#2c2824' transition 150ms
        disabled: bg '#e0d8cd' text '#a69b8f'
    zone-b: email-preview
      top: 64 left: 32 width: 916 height: 800 padding 0
      bg: '#f0ebe3' radius-8 overflow hidden
      device-frame: 600x720 bg '#ffffff' margin 40 auto 0 auto shadow 0 4 32 '#c4b8a8'22
      email-header: 600x60 bg '#f5f2ed' border-bottom 1px '#ece6dd' padding 16
        from-label: gt-pressura-mono 11/16 #7a6f64 tracking-25
        masthead: gt-pressura-regular 18/24 #2c2824 tracking--5 text-align center
      email-body: 600x600 padding 32
        headline: gt-pressura-regular 28/36 #2c2824 tracking--10 margin-bottom 12
        body-text: gt-pressura-regular 15/24 #7a6f64 margin-bottom 20
        divider: 1px solid '#ece6dd' margin 20 0
        cta-button: 200x44 radius-6 bg '#3c3836' text '#f5f2ed'
          gt-pressura-mono 13/20 tracking-50 text-align center
      email-footer: 600x60 bg '#f5f2ed' border-top 1px '#ece6dd' padding 16
        gt-pressura-mono 10/14 #a69b8f tracking-25 text-align center
    zone-c: block-palette
      top: 64 left: 976 width: 432 height: 800 padding 24
      bg: '#ffffff' border-left 1px '#ece6dd'
      palette-label: gt-pressura-mono 11/16 #8a7f64 tracking-75 uppercase margin-bottom 16
      draggable-block: 384x56 radius-6 border 1px '#ece6dd' bg '#faf8f5' padding 12
        block-icon: 24x24 '#c4b8a8'
        block-label: gt-pressura-regular 14/20 #3c3836
        block-desc: gt-pressura-mono 10/14 #a69b8f tracking-25
        hover: bg '#f5f2ed' border '#d4ccc0' cursor-grab transition 120ms
        dragging: opacity 0.6 shadow 0 8 24 '#c4b8a8'33
      gap: 8px between blocks
mockup-08: comment-moderation-inbox
  viewport: 1440x900
  grid: 3-zone split, 24px gutter, 32px outer margin
  zones:
    zone-a: inbox-header
      top: 0 left: 0 width: 1440 height: 60
      bg: '#f5f2ed' border-bottom: 1px solid '#e0d8cd' padding 12 32
      title: gt-pressura-regular 24/32 #2c2824 tracking--10
      unread-count: 28x20 radius-10 bg '#3c3836' text '#f5f2ed' gt-pressura-mono 11/16 tracking-50
      filter-tabs: gt-pressura-mono 11/16 tracking-50
        all-pending-approved-spam
        active: text '#3c3836' border-bottom 2px '#3c3836' padding-bottom 6
        inactive: text '#a69b8f' hover text '#7a6f64' transition 150ms
    zone-b: comment-list
      top: 60 left: 32 width: 548 height: 804 padding 8
      bg: '#ffffff' border 1px '#ece6dd' radius-8 overflow-y auto
      comment-item: 524x92 padding 16 border-bottom 1px '#f0ebe3'
        avatar: 28x28 radius-14 bg '#e0d8cd' initials gt-pressura-mono 11/16 #7a6f64
        author: gt-pressura-regular 14/20 #3c3836
        timestamp: gt-pressura-mono 10/14 #a69b8f tracking-25 margin-left 8
        excerpt: gt-pressura-regular 13/20 #7a6f64 line-clamp-2 margin-top 4
        selected: bg '#faf8f5' border-left 3px '#7a6f64'
        hover: bg '#f5f2ed' cursor pointer transition 100ms
        unread-dot: 6x6 radius-3 bg '#7a6f64' margin-right 8
        flagged-icon: 14x14 '#c4a85a'
    zone-c: detail-panel
      top: 60 left: 608 width: 800 height: 804 padding 24
      bg: '#faf8f5' border 1px '#ece6dd' radius-8
      full-comment: gt-pressura-regular 15/24 #3c3836 margin-bottom 20
      metadata-row: gt-pressura-mono 11/16 #8a7f64 tracking-25 margin-bottom 16
        article-link: text '#7a6f64' hover underline decoration '#c4b8a8'
      action-bar: flex gap 8
        approve-btn: 120x36 radius-6 bg '#e0e8d8' text '#3c3836'
          gt-pressura-mono 12/16 tracking-50
          hover: bg '#d0dcc8' transition 120ms
        reject-btn: 120x36 radius-6 bg '#e8d8d8' text '#3c3836'
          hover: bg '#dcc8c8' transition 120ms
        reply-btn: 120x36 radius-6 bg '#f5f2ed' border 1px '#d4ccc0' text '#3c3836'
          hover: bg '#ece6dd' transition 120ms
      reply-field: 752x96 radius-6 border 1px '#d4ccc0' bg '#ffffff' padding 12 margin-top 16
        gt-pressura-regular 14/20 #3c3836
        focus: border '#7a6f64' outline none
        placeholder: gt-pressura-regular 14/20 #a69b8f
mockup-09: seo-metadata-inspector
  viewport: 1440x900
  grid: 12-column bento, 24px gutter, 32px outer margin
  zones:
    zone-a: inspector-header
      top: 0 left: 0 width: 1440 height: 64
      bg: '#f5f2ed' border-bottom: 1px solid '#e0d8cd' padding 14 32
      title: gt-pressura-regular 24/32 #2c2824 tracking--10
      url-field: 480x36 radius-6 border 1px '#d4ccc0' bg '#faf8f5' padding 12
        gt-pressura-mono 12/16 #3c3836 tracking-25
        focus: border '#7a6f64' outline none
      analyze-button: 100x36 radius-6 bg '#3c3836' text '#f5f2ed' gt-pressura-mono 12/16 tracking-50
        hover: bg '#2c2824' transition 150ms
    zone-b: preview-card
      top: 80 left: 32 width: 660 height: 240 padding 24
      bg: '#ffffff' radius-8 border 1px '#ece6dd'
      section-label: gt-pressura-mono 11/16 #8a7f64 tracking-75 uppercase margin-bottom 12
      google-snippet: 600x120 radius-6 bg '#faf8f5' padding 16
        page-title: gt-pressura-regular 18/24 #1a0dad text-decoration underline margin-bottom 4
        url-display: gt-pressura-regular 13/20 #3a7a3a margin-bottom 8
        description: gt-pressura-regular 13/20 #6a5f54 line-clamp-2
      title-tag-editor: 600x36 radius-4 border 1px '#d4ccc0' bg '#faf8f5' padding 8
        gt-pressura-mono 12/16 #3c3836 tracking-25
        focus: border '#7a6f64' outline none
        char-count: gt-pressura-mono 10/14 #a69b8f tracking-25 text-align right
          warning: '#c4a85a' when gt 60
          error: '#8a5a5a' when gt 70
    zone-c: meta-breakdown
      top: 80 left: 720 width: 688 height: 344 padding 24
      bg: '#ffffff' radius-8 border 1px '#ece6dd'
      meta-row: height 36 border-bottom 1px '#f0ebe3'
        meta-key: gt-pressura-mono 11/16 #8a7f64 tracking-25 width 120
        meta-value: gt-pressura-regular 13/20 #3c3836
        meta-status: 12x12 radius-3
          ok: bg '#d0dcc8'
          missing: bg '#e8d8d8'
          warning: bg '#e8e0c8'
    zone-d: keyword-score-card
      top: 336 left: 32 width: 660 height: 344 padding 24
      bg: '#f5f2ed' radius-8 border 1px '#ece6dd'
      score-ring: 80x80 stroke '#c4b8a8' stroke-width 6 fill none
        score-value: gt-pressura-regular 28/36 #2c2824 text-align center
        score-label: gt-pressura-mono 9/14 #a69b8f tracking-50 text-align center
      keyword-list: gt-pressura-mono 11/16 #7a6f64 tracking-25
        density-bar: height 4 radius-2 bg '#ece6dd' fill '#c4b8a8'
        keyword-label: gt-pressura-regular 14/20 #3c3836
    zone-e: suggestion-feed
      top: 696 left: 32 width: 1376 height: 168 padding 20
      bg: '#ffffff' radius-8 border 1px '#ece6dd'
      suggestion-item: 12px height gt-pressura-regular 13/20 #7a6f64
        priority-tag: 48x18 radius-4 bg '#e0d8cd' text '#5a4f44'
          gt-pressura-mono 9/12 tracking-50
          high: bg '#e8d8d8' text '#6a3a3a'
          medium: bg '#e8e0c8' text '#6a5a3a'
          low: bg '#e0e8d8' text '#3a5a3a'
mockup-10: style-guide-brand-settings
  viewport: 1440x900
  grid: 12-column, 24px gutter, 32px outer margin
  zones:
    zone-a: brand-header
      top: 0 left: 0 width: 1440 height: 76
      bg: '#f5f2ed' border-bottom: 1px solid '#e0d8cd' padding 18 32
      title: gt-pressura-regular 28/36 #2c2824 tracking--10
      subtitle: gt-pressura-mono 11/16 #8a7f64 tracking-75 uppercase margin-left 16
      published-badge: 80x24 radius-12 bg '#3c3836' text '#f5f2ed' gt-pressura-mono 10/14 tracking-50
    zone-b: typography-panel
      top: 76 left: 32 width: 660 height: 384 padding 24
      bg: '#ffffff' radius-8 border 1px '#ece6dd'
      font-card: margin-bottom 20
        font-name: gt-pressura-regular 24/32 #2c2824
        font-specimen: gt-pressura-regular 16/24 #7a6f64 The quick brown fox
        weight-row: flex gap 8
          weight-swatch: 36x36 radius-4 border 1px '#ece6dd' text-align center
            gt-pressura-mono 11/16 #3c3836
            active: border 2px '#3c3836' bg '#f5f2ed'
        size-scale: 320px height 48
          size-label: gt-pressura-mono 9/14 #a69b8f tracking-25
          ruler-tick: 1px solid '#e0d8cd'
    zone-c: color-palette
      top: 76 left: 720 width: 688 height: 384 padding 24
      bg: '#f5f2ed' radius-8 border 1px '#ece6dd'
      swatch-group: 4 swatches, each 148x148 radius-8
        swatch-fill: full block
        swatch-hex: gt-pressura-mono 11/16 #faf8f5 tracking-25 padding 8 margin-top auto
          dark-swatch-text: '#3c3836'
        swatch-role: gt-pressura-mono 9/14 tracking-50 padding 8
        primary: bg '#3c3836'
        secondary: bg '#7a6f64'
        accent: bg '#c4b8a8'
        surface: bg '#f5f2ed'
        gap: 12px between swatches
    zone-d: spacing-scale
      top: 476 left: 32 width: 660 height: 388 padding 24
      bg: '#ffffff' radius-8 border 1px '#ece6dd'
      scale-label: gt-pressura-mono 11/16 #8a7f64 tracking-75 uppercase margin-bottom 20
      scale-token: height 28 margin-bottom 4
        token-name: gt-pressura-mono 10/14 #a69b8f tracking-25 width 72
        token-bar: radius-2 bg '#e0d8cd'
          value-4: width 4px height 8
          value-8: width 8px height 12
          value-12: width 12px height 16
          value-16: width 16px height 20
          value-24: width 24px height 24
          value-32: width 32px height 28
          value-48: width 48px height 28
          value-64: width 64px height 28
          value-96: width 96px height 28
        token-value: gt-pressura-mono 10/14 #7a6f64 tracking-25 margin-left 8
    zone-e: component-tokens
      top: 476 left: 720 width: 688 height: 388 padding 24
      bg: '#f5f2ed' radius-8 border 1px '#ece6dd'
      token-card: margin-bottom 12
        component-name: gt-pressura-regular 14/20 #3c3836
        token-group: flex gap 16
          token-label: gt-pressura-mono 9/14 #a69b8f tracking-25
          token-value: gt-pressura-mono 11/16 #7a6f64 tracking-25
        variant-row: flex gap 8
          variant-preview: 80x48 radius-4 border 1px '#d4ccc0' bg '#faf8f5'
            hover: border '#7a6f64' transition 120ms
            selected: border 2px '#3c3836' bg '#f5f2ed'
10 mockups delivered. All dimensions defined inline per zone. All spacing tokens explicit in px per sub-value. No forward references to rationale blocks. YAML indentation 2-space consistent. Warm monochrome palette enforced throughout: surfaces #f5f2ed #faf8f5 #ffffff, borders #ece6dd #e0d8cd #d4ccc0, text #3c3836 #7a6f64 #8a7f64 #a69b8f #c4b8a8. Typography stack: gt-pressura-regular for body, gt-pressura-mono for labels. Each mockup self-contained with its own viewport, grid, zones, and interaction states.
10 Editorial Minimal Dashboard Mockups
mockup-001: Bento Hero Zone
  layout: 2-col grid (65/35), full-viewport-height hero above 3-card bento belt
  typography: Playfair Display 52/60 for hero metric, Inter 13/18 for body, 400 weight
  palette: bg=#F5F3EE, card=#EDEAE4, text=#2C2C2C, accent=#A0937D
  whitespace: 64px card padding, 48px section gap, 32px internal stack
  zone-c interaction: entire hero card is clickable, no explicit button
  bento belt: 3 cards, each 1/3 width, 240px height, staggered reveal
mockup-002: Typographic Stats Grid
  layout: 4-col grid for stat blocks, 2 rows, aspect-ratio 3/2 per cell
  typography: Graphik 48/52 for stat value, Graphik 13/18 for label, uppercase tracking 1.2px
  palette: bg=#FAF8F5, card=white, stat-value=#1A1A1A, label=#8B8175
  whitespace: 56px padding inside stat cells, 24px between rows, 40px outer margin
  decoration: hairline 1px border-bottom #D4CDC4 on label, no background fill
  zone-c: title text is hyperlink, 48x48px touch target on the stat area
mockup-003: Editorial Feed with Sidecar
  layout: main feed 70%, right rail 30%, sticky sidebar below 80px top offset
  typography: Source Serif Pro 18/26 for feed item body, 15/20 for rail summaries
  palette: bg=#F7F5F1, feed-card=#EFECE7, rail-card=#EAE6DF, border=#D9D3CA
  whitespace: 24px between feed items, 40px left inset for feed, 32px rail padding
  feed items: 5 rows, each 120px, image thumb 80x80 rounded-4, title+preview inline
  zone-c: row click expands inline preview, 44px min touch height per row
mockup-004: Monochrome Data Wall
  layout: full-bleed background, 6 metric panels in 3x2 grid, floating on backdrop
  typography: DM Mono 36/44 for numbers, DM Mono 14/22 for labels, all uppercase
  palette: backdrop=#E8E4DE, panel=#FCFAF7, shadow=#C4BCB0 ink-bled, text=#26221E
  whitespace: 40px panel padding, 20px between panels, 16px between number and label
  decoration: no borders, only 12px offset shadow on right+bottom, slight texture
  zone-c: any panel click = full-width detail drawer slides from bottom
mockup-005: Longform Dashboard
  layout: single column, 720px max-width centered, scrollable article-style
  typography: EB Garamond 22/32 for intro paragraph, Inter 16/24 for data callouts
  palette: bg=#F4F1EC, text=#2E2A24, pullquote=#564D42, rule=#D6CEC3
  whitespace: 80px top margin, 48px between sections, 56px pullquote top/bottom
  structure: metric-embed blocks inline, 3 pullquotes, 2 side-note callouts
  zone-c: side-notes highlighted on hover, click copies metric to clipboard
mockup-006: Compact Overview Strip
  layout: horizontal strip, 100vw wide, 7 compact metric pills, overflow-x scroll
  typography: Inter 14/18 compact value, Inter 10/13 label, weight 500 value 400 label
  palette: pill-bg=#EDE9E2 selected=#D6CFC4, text=#33302B, arrow=#8B8175
  whitespace: 12px pill padding x/y, 8px pill gap, 16px below strip for filter bar
  pill: 140px wide min, fixed height 52px, rounded-8, label above value
  zone-c: pill tap = active state + mini chart replaces pill content, 44px min touch
mockup-007: Bento with Radial Focus
  layout: 5 cards in asymmetric bento, center card 2x larger, surrounding 4 equal
  typography: center=Serif 28/36 headline, surrounding=Sans 13/18, only center uses serif
  palette: bg=#F3EFE9, center-card=#DCD4C8, side-cards=#EDE8E1, text light on center
  whitespace: 36px center card padding, 24px side cards, 16px inter-card gap
  center card: radial progress indicator ring, 160px diameter, no labels
  zone-c: center card click = toggles between 3 metric views (sequencing)
mockup-008: Newspaper Sections
  layout: 3-column newspaper layout, top header bar spans all 3, 4 sections total
  typography: header=Playfair Display 14/18 all-caps 1.5px tracking, body=Inter 15/22
  palette: col-bg=#EFEBE5, gutter=#E2DCD3, header-line=#C4BAA9
  whitespace: 36px column padding, 1px gutter, 32px above fold line, 48px section gap
  structure: col1=primary metric 200px, col2=feed 300px, col3=mini-chart 200px
  zone-c: column headers collapse/expand their section, persistent scroll position
mockup-009: Dark Editorial
  layout: inverted palette, same bento structure as 001 but dark warm
  typography: Playfair Display 48/56 hero, Inter 14/20 body, weight 300 for body
  palette: bg=#1E1B18, card=#2B2722, accent=#A0907A, text=#E2DDD6, muted=#7C756A
  whitespace: identical to 001 geometry, deep shadow between cards
  adjustment: reduced text contrast (4.8:1 instead of 7:1) for editorial softness
  zone-c: cards glow with 1px #A0907A border on hover, touch reveals control row
mockup-010: Minimal Action Dashboard
  layout: 3 zones stacked, zone A=title+date 80px, zone B=metric trio, zone C=action shelf
  typography: zone A=Inter 28/36 title weight 300, zone B=DM Mono 24/32, zone C=Inter 14/18
  palette: bg=white, metric-bg=#F8F6F2, action-bg=#EDE8E1, primary=#4A4238
  whitespace: zone A margin 48px below, zone B 24px item gap, zone C 16px button spacing
  shelf: 4 horizontal action pills, 40px height, rounded-20, label only, no icons
  zone-c: action pill expands to full-width inline input on tap, 48px min height
zone-c rationale for all: click targets minimum 44x44px (WCAG 2.1), feedback within 120ms, no double-tap ambiguity. Touch state = background shift to next darker card tone (no outline/focus-ring on first tap).
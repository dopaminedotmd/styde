mockup: editorial-minimal-dashboard-v1
phase: 0.5
type: design mockup
format: 10 unique layout variants
variant: cover-card-hero
layout: single hero card filling viewport center
  structure: 4-column bento grid, hero spans col-2-4
  typography: Playfair Display 72px hero headline, Inter 14px body
  palette: bg #f5f0eb, text #2a2520, accent #c4a88a, border #e0d8d0
  white-space: 64px card padding, 80px section gaps
  elements: hero article card with pull-quote, 3 small stat cards, navigational tag list
  feel: A single magazine spread blown up to dashboard scale
variant: three-column-bento
layout: 3 equal columns, 8 cards total
  structure: col-0 has 3 stacked tall cards, col-1 has 2 medium, col-2 has 3 small
  typography: system serif for headers, monospace 12px for data labels
  palette: bg #e8e2da, cards #faf7f3, text #3a342e, lines #d4ccc2
  white-space: 40px grid gap, 32px card padding
  elements: headline tracker, reading-list queue, metrics triad, author spotlight, draft queue, tag cloud, recent activity
  feel: Architectural digest floorplan meets data dashboard
variant: horizontal-timeline
layout: horizontal scroll row above, 2x2 grid below
  structure: top strip of 5 date-anchored article cards, bottom 4 content cards
  typography: Playfair Display italic 28px for dates, Inter 13px body, 10px uppercase labels
  palette: bg #f0ebe4, cards #fcfaf7, stroke #cfc6ba, active accent #8b7355
  white-space: 48px between rows, 28px card internal
  elements: timeline pins, editorial calendar preview, draft word-count progress bars, contributor avatars, pending review queue
  feel: Newsroom wall calendar turned digital editorial command center
variant: manuscript-spread
layout: full-width spread mimicking an open book
  structure: left pane editor notes, right pane live preview, footer toolbar
  typography: Source Serif 16px body for preview, monospace 13px for notes
  palette: bg #f8f3ec left pane, #fffcf7 right pane, text #2e2a25, annotations #9a8b7a
  white-space: 60px spread gutter, 40px margins
  elements: inline annotation markers, word-count per section bar, style-guide compliance dots, version diff highlights, publishing checklist
  feel: Opening a moleskine notebook next to a printed broadsheet
variant: metrics-editorial
layout: bento asymmetric grid, 5 cards
  structure: large chart card (col-1-2 row-0), 2 medium stat cards right, 2 small cards bottom row
  typography: Inter 48px stat numbers, Inter 11px uppercase chart labels
  palette: bg #ece6de, card #f7f2eb, green #7a8b6e, red #b5826e, neutral #aea093
  white-space: 36px grid gaps, minimal card padding 20px
  elements: editorial KPI sparkline strip, article velocity bar chart, top performer list, publish-schedule heatmap, content inventory pie (replaced by circle of dots)
  feel: Bloomberg terminal designed by a book publisher
variant: single-column-longform
layout: one column, stacked editorial stack
  structure: 6 cards in vertical rhythm, full width
  typography: Lyon Text 15px body, Lyon Display 24px section headers
  palette: bg #f3efe7, text #1f1c18, rule #d5cdc1, accent-hover #b0927a
  white-space: 56px between cards, 32px internal vertical rhythm
  elements: editorial manifesto card, recently published with excerpt, upcoming features list, editor notes callout, series tracker, thematic tag index
  feel: A well-typeset literary journal, each card a chapter opening
variant: gallery-strip
layout: left narrow sidebar + main gallery area
  structure: sidebar 280px with filters and tags, main area 3x3 article card grid
  typography: Inter 12px sidebar, Playfair Display 20px card titles, 14px preview
  palette: bg #efe9e1, sidebar #e6dfd5, card #fcf9f5, image-placeholder #d4cabe, text #2d2822
  white-space: 24px grid gap, 24px card padding, 40px sidebar padding
  elements: cover image thumbnails, readability score badges, estimated read time chips, category filter pills, search with typographic icon
  feel: A photo editor's light table reimagined as a publication dashboard
variant: canvas-workspace
layout: freeform pinboard, cards at varied positions
  structure: draggable cards on an infinite canvas, 6 default positioned
  typography: whatever the card type dictates, consistent Inter meta
  palette: bg #e8e1d6 (kraft paper tone), card #fcf9f4, shadow rgba 0 0 0 0.06
  white-space: floating, 32px internal padding standard
  elements: pinned drafts, inspiration moodboard card, editorial calendar sticky, collaborator presence dots, style-guide snippet card, latest analytics snapshot
  feel: A cork board in a studio where editors pin their day
variant: minimal-three-panel
layout: left panel / center panel / right panel
  structure: left 240px navigation+meta, center fluid article feed, right 300px detail panel
  typography: Inter 11px sidebar labels, Georgia 22px feed titles, 14px feed excerpts
  palette: bg #f4efe8, left-panel #ece4da, center #faf6f0, right-panel #f0e9e0, accent #b6987c
  white-space: 0 internal panel padding (cards edge-to-edge in center), 32px between sidebar items
  elements: section tree nav, infinite-scroll article feed with small thumbnails, right panel shows article detail when selected, collaborative status indicators, publish time estimates
  feel: Three-column newspaper layout, each panel a different section of the editorial workflow
variant: blank-canvas-strip
layout: tab strip top + 2x4 content grid below
  structure: 4 editorial tabs (Write / Review / Publish / Analyze), 8 cards in 2x4 grid below
  typography: Inter 12px tab labels (only active tab gets Playfair Display 14px), card content follows editorial hierarchy
  palette: bg #f2ede5, tab-active #fffbf6, tab-inactive #e4dbcf, card #faf5ee, accent #a8896e
  white-space: 20px tab bar height, 28px grid gap, 24px card padding
  elements: tab bar with subtle underline animation, each tab reveals its own 2x4 grid of relevant cards, write tab shows draft queue and editor, review tab shows approval flow cards, publish tab shows schedule and distribution, analyze tab shows metrics
  feel: Architectural section drawings with clear planes and material boundaries — each tab a different floor of the editorial building
winner: variant-10-blank-canvas-strip
reason: Best balance of editorial elegance and practical workflow separation. Tab metaphor keeps information density low per view while preserving access to full feature set. Architectural section-drawing aesthetic maps directly to the warm monochrome bento requirement.
fallback: variant-02-three-column-bento if tabs feel too app-like for a magazine brand
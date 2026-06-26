=== MOCKUP 1: DEFAULT AGENT GRID (4 columns x 2 rows) ===
Panel bounds: 100% width, auto-height, 24px padding inside a rounded-12 container.
Background: #0F1117, subtle border #1E2030.
Grid: 4 columns, gap 16px. Each card = 1fr.
Agent Card:
- Width: fill. Height: 136px. Pad 16px. Bg: #181A23. Radius: 8. Border: #24263A.
- Top row: agent icon 28x28 circle (colored ring per status: #22C55E for active, #F59E0B for pending, #EF4444 for failed) + agent name 14px/600 #E2E8F0 + status badge pill 24px tall, font 11px/600.
  Pill colors: #1A2E1A bg/#4ADE80 text for Running. #2E2A1A bg/#FBBF24 text for Pending. #2E1A1A bg/#F87171 text for Failed. #1A1A2E bg/#818CF8 text for Idle.
- Score bar row: label 'Score' 12px #64748B left, value 14px/700 #E2E8F0 right. Thin bar 4px tall full width, bg #1E2030, fill % using:
  - High tier (>=90): fill #22C55E
  - Mid tier (>=70): fill #F59E0B
  - Low tier (<70): fill #EF4444
  Bar has 2px radius pill ends. Width = score% of container.
- Stats row: 3 inline blocks. Each: icon 12x12 + count 13px/500. Separator: dim vertical line 1px #1E2030 h=16px.
  Jobs: checkmark icon / number / #94A3B8
  Running: spinner icon / number / #4ADE80
  Failed: X icon / number / #F87171
  Pending: clock icon / number / #FBBF24
- Hover: card bg shifts to #1A1C2B, border to #3B3F5C, shadow spreads 0 4px 20px rgba(0,0,0,.3). Cursor pointer. Transition 150ms ease.
- Active: card border #6366F1, inset shadow 0 0 0 1px rgba(99,102,241,.15). Scale .99.
- Focus visible: outline 2px #6366F1 offset 2px outside card.
=== MOCKUP 2: COMPACT LIST VIEW ===
Panel same container, but 1 column layout. Gap 8px between rows.
Each row: height 48px. Horizontal layout. Left: icon 24x24 + agent name 13px/600 + status badge pill (same as card pill style). Center: score bar compact (60px wide, 6px tall) + score text 12px. Right: stat counts inline (Jobs 14px/500, Running 14px/500 #4ADE80, Failed 14px/500 #F87171). Separator spacing 12px between stat groups.
Hover: row bg #1A1C2B, text brighter. Active: slight indent via left border 2px solid #6366F1.
=== MOCKUP 3: DASHBOARD SUMMARY BAR ===
Full-width strip, 48px tall, bg #181A23, top/bottom border 1px #1E2030.
Layout: 5 stat items spaced evenly across 100% width.
Each: icon 16x16 + label 12px/500 #64748B + value 18px/700.
- Total Agents: group icon / 'Agents' / count
- Active: play icon / 'Active' / count in #4ADE80
- Pending: clock icon / 'Pending' / count in #FBBF24
- Failed: X icon / 'Failed' / count in #F87171
- Avg Score: star icon / 'Avg Score' / value with 1 decimal
Hover on any stat: subtle bg shift #1E2030. Active: short underline 2px #6366F1.
=== MOCKUP 4: FILTER/SEARCH TOP BAR ===
Height 40px, positioned above the grid/list. Flex row, gap 12px.
Left group:
- Search input: 240px wide. Inset bg #181A23, border #24263A, radius 6. Icon 14x14 magnifier. Text placeholder 'Search agents...' 13px #475569. Hover border #3B3F5C. Focus border #6366F1, no outline, inset shadow. Has clear X button when filled. Disabled: opacity .4, no pointer.
- Status filter dropdown: 120px. Same style as search. Chevron icon right. States: dropdown panel 200px wide, max-height 220px, scroll. Items 32px each. Hover bg #1E2030. Selected checkmark + highlight. Multi-select via chips above dropdown after selection.
Right group:
- View toggle pill group: 2 buttons side by side, no gap, bg #181A23, radius 6.
  Grid icon button: 32x32, active bg #24263A, icon #6366F1.
  List icon button: 32x32, inactive bg transparent, icon #475569.
  Hover: bg #1E2030. Active: #24263A + bright icon.
=== MOCKUP 5: AGENT DETAIL EXPANDED (from grid card) ===
When a card is clicked in grid view, it expands below the card row. Height: auto, up to 200px. Margin top 8px. Bg #13151E. Border 1px #24263A. Radius 8. No padding collapse — uses 16px padding all sides.
Layout: 3 columns (2:1:1 ratio).
Left column (60%):
- Recent task log: max 4 lines. Each line: timestamp 11px/400 #64748B + status dot 8px colored + task name 12px/500 #94A3B8. Ellipsis overflow after 4 lines.
- 'View all' link 12px/600 #6366F1 right aligned.
Middle column (20%):
- Mini performance sparkline: SVG path, 100% wide 40px tall. Color gradient matching score tier. No axes, just line. Tooltip on hover shows exact values at points.
- Label 'Score trend' 11px #64748B below.
Right column (20%):
- Quick actions: 3 buttons stacked, 32px tall each. 'Rerun', 'Pause', 'Logs'. Text 12px/500. Bg #1E2030, radius 4. Hover bg #24263A. Active bg #2A2D45.
Expand/collapse uses a caret icon on the original card bottom-right. Transitions: max-height 300ms ease, opacity 200ms.
=== MOCKUP 6: EMPTY STATE ===
Container same as grid panel. No cards.
Center content block vertically + horizontally. Gap 20px.
- Large icon: dashboard blank 64x64, opacity .3, color #475569.
- Text: 'No agents deployed yet' 16px/600 #94A3B8.
- Subtext: 'Deploy your first blueprint to see agent status here' 13px/400 #64748B.
- CTA button: 'Deploy Blueprint', bg #6366F1 pill 36px tall, text 14px/600 white, padding 0 24px. Hover bg #5558E6. Active bg #4F52D2. Focus ring 2px #818CF8 offset 2px.
=== MOCKUP 7: LOADING/SKELETON STATE ===
Grid layout preserved. 8 skeleton cards same dimensions as MOCKUP 1.
Each skeleton card:
- Bg #181A23, border #1E2030 (same as real cards).
- Shimmer animation: pseudo-element full width, linear-gradient(90deg, transparent 0%, rgba(255,255,255,.04) 50%, transparent 100%) translating left-right over 1.8s infinite.
- Placeholder blocks:
  - Circle 28px + rect 60x14px for name row, radius 4.
  - Rect full width 4px tall for score bar, radius 2.
  - 3 small rects 16x12px with 8px gaps between for stat row.
All placeholder fill: #1E2030.
=== MOCKUP 8: ERROR STATE ===
Container same dimensions. Not dismissable — persistent until data resolves.
Layout: centered. Top: warning triangle icon 48x48 #F87171. 8px below.
- Headline 16px/600: 'Failed to load agent status' #F87171.
- Error detail 12px/400 #64748B: 'Could not connect to agent runtime. Retrying in 15s...'
- Retry button: 'Retry Now', same pill style as CTA but red scheme: bg #7F1D1D, text #FCA5A5. Hover bg #991B1B.
- Auto-retry countdown visual: circular progress indicator 24x24, stroke #EF4444, track #1E2030, rotating dash animation.
=== MOCKUP 9: RESPONSIVE BREAKPOINT (tablet, 768px) ===
Grid collapses from 4 columns to 2 columns. Gap unchanged at 16px.
Filter/search bar width shrinks search input from 240px to 160px.
Summary bar reduces font 18px->14px for values.
Detail expanded panel goes 1 column layout — log takes full width, quick actions become horizontal row below.
=== MOCKUP 10: RESPONSIVE BREAKPOINT (mobile, 480px) ===
Single column grid. Each card full width.
Summary bar collapses to 2 rows: first row 3 items (Total, Active, Pending), second row 2 items (Failed, Avg Score). Each row 32px tall.
Filter/search bar: search becomes full width, dropdowns moved below search. View toggle hidden (defaults to grid).
Detail panel: similar to tablet 1-col but with no mini sparkline (removed), quick actions spread horizontally at bottom.
=== DESIGN TOKENS ===
color-bg-primary: '#0F1117'
color-bg-secondary: '#181A23'
color-bg-tertiary: '#1E2030'
color-bg-hover: '#1A1C2B'
color-bg-active: '#24263A'
color-bg-expanded: '#13151E'
color-border-default: '#1E2030'
color-border-muted: '#24263A'
color-border-focus: '#6366F1'
color-border-hover: '#3B3F5C'
color-text-primary: '#E2E8F0'
color-text-secondary: '#94A3B8'
color-text-muted: '#64748B'
color-text-placeholder: '#475569'
color-accent-primary: '#6366F1'
color-accent-hover: '#5558E6'
color-accent-active: '#4F52D2'
color-status-running-bg: '#1A2E1A'
color-status-running-text: '#4ADE80'
color-status-pending-bg: '#2E2A1A'
color-status-pending-text: '#FBBF24'
color-status-failed-bg: '#2E1A1A'
color-status-failed-text: '#F87171'
color-status-idle-bg: '#1A1A2E'
color-status-idle-text: '#818CF8'
color-score-high: '#22C55E'
color-score-mid: '#F59E0B'
color-score-low: '#EF4444'
radius-container: 12px
radius-card: 8px
radius-pill: 9999px
radius-input: 6px
font-size-icon: 14px
font-size-small: 11px
font-size-body: 12px
font-size-label: 13px
font-size-heading: 14px
font-size-value: 18px
font-weight-normal: 400
font-weight-medium: 500
font-weight-semibold: 600
font-weight-bold: 700
transition-fast: 150ms ease
transition-medium: 300ms ease
spacing-gap: 16px
spacing-card-pad: 16px
spacing-container-pad: 24px
spacing-row: 8px
spacing-stat-group: 12px
shadow-card-hover: '0 4px 20px rgba(0,0,0,.3)'
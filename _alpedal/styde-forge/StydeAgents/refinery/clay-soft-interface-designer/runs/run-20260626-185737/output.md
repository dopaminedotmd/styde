PHASE 0.5 — DESIGN MOCKUPS
Blueprint v10.0.0 | Clay Soft Interface Designer
MOBILE MOCKUP (320-767px)
Layout
  1 header bar full width 60px height
  1 bottom nav tray 56px height
  Single column flow
  Content padding 16px left/right
  Card gutters 16px vertical between cards
Header
  Neutral-50 background
  16px border radius top edge
  8px border radius bottom edge
  Soft drop shadow 0 4px 20px rgba(0,0,0,0.06)
  Contains: hamburger icon left, app name center, avatar circle right
  Avatar circle 36px diameter, primary-light border
  Hamburger icon 24x24px, neutral-600
Bottom Nav
  Neutral-100 background, 12px border radius top corners
  5 icon buttons equally spaced
  Active icon: primary fill, neutral-50 circle behind 40px
  Inactive icons: neutral-400 thin stroke
  Icon size 22px
Top Stats Card (full width)
  Neutral-100 background, 16px border radius
  Inner padding 20px
  Two stat rows stacked
  Stat row: label neutral-500 11px, value neutral-800 28px weight 700
  Soft extrusion shadow 0 6px 24px rgba(0,0,0,0.06)
Pie Chart Card (full width)
  Neutral-100 background, 16px border radius
  120px pie chart diameter centered
  Legend below chart, 2 columns, 8px gap between items
  Legend dot 10px circle, label neutral-600 11px
  4 segments: primary 35%, accent 30%, success 20%, primary-light 15%
  Shadow identical to stats card
Bar Chart Card (full width)
  Neutral-100 background, 16px border radius
  8 bars horizontal, 36px height each
  Gap between bars 8px
  Odd bars primary fill, even bars accent fill
  Bar border radius 6px (right edges)
  Bar labels left side 11px neutral-600
  Value labels right side 11px neutral-700 weight 600
  No grid lines, no y-axis, no x-axis
  Tooltip on bar hover: neutral-800 pill 28px height, white text 12px, arrow pointing down, max 60px width
Activity Feed Card (full width)
  Neutral-100 background, 16px border radius
  4 activity rows, each 48px height
  Row: time stamp 11px neutral-400 left, description 12px neutral-600 right
  Divider between rows neutral-200 1px
  Last row has no divider
  Soft text truncation on long descriptions
TABLET MOCKUP (768-1023px)
Layout
  Two-column grid with 16px gap
  Sidebar collapses to icon tray 56px wide left
  Content area fills remaining width
  Header spans full content width minus sidebar
Sidebar (collapsed)
  Neutral-50 background
  4 icon buttons stacked vertically, 16px padding top
  Each icon 28px, neutral-500, active icon primary fill
  No labels visible
  Bottom: user avatar 32px circle
  12px border radius right edge
  Shadow 2px 0 16px rgba(0,0,0,0.04)
Header
  Neutral-50 background
  Breadcrumb left: neutral-400 12px > neutral-600 12px
  Date display right: neutral-600 13px
  48px height
  No hamburger (sidebar always visible in icon mode)
Content Grid (2 columns)
  Column 1: Pie chart card (160px diameter), Stats card (compact)
  Column 2: Bar chart card (spans 1 col), Activity feed card
  Column 2 row 2: bar chart, row 3: activity feed
  All cards same height group by visual weight
Pie Chart Card (tablet)
  160px diameter
  Legend below, single row horizontal
  Legend items inline with 16px gap
  Same 4 segments, same colors
  Padding 20px inner
Bar Chart Card (tablet)
  6 bars visible without scroll
  Bars 40px height each
  8px gap
  Same color rules for odd/even
  Chart area height 376px
DESKTOP MOCKUP (1024px+)
Layout
  Three-column grid with 20px gap
  Full sidebar 220px wide left
  Header spans content width minus sidebar
  Main content 3 equal columns
Sidebar (expanded)
  Neutral-50 background
  220px width, full viewport height
  Top: app logo 32x32px primary circle + "styde" neutral-700 18px weight 600, 24px padding
  4 nav items, 44px height each, 12px border radius
  Nav item: icon 22px + label 14px neutral-600, 12px horizontal padding
  Active nav: primary-light background, primary icon, label neutral-800 weight 600
  Bottom: user profile section, avatar 40px + name neutral-700 14px + role neutral-500 11px
  Divider neutral-200 at nav/separator 1px, 16px margin
  Shadow right edge 2px 0 24px rgba(0,0,0,0.04)
Header (desktop)
  Neutral-50 background
  Height 56px
  Breadcrumb: Dashboard neutral-400 13px > Analytics neutral-600 13px
  Right: notification bell icon 24px neutral-500 + pill badge primary 8px top-right
  Right: user avatar 40px + name 14px
  Shadow bottom 0 2px 16px rgba(0,0,0,0.03)
Stats Row (3 cards, 1 per column)
  Card 1: Total Views — value 24.5K neutral-800 32px, delta +12.3% success 13px
  Card 2: Active Users — value 1,842 neutral-800 32px, delta +8.1% success 13px  
  Card 3: Conversion — value 3.2% neutral-800 32px, delta -0.4% error 13px
  Each card: 24px padding, neutral-100 background, 16px border radius
  Shadow: 0 8px 32px rgba(0,0,0,0.08)
  Icon top-right each card: 40x40px circle with primary-light bg, icon primary
Pie Chart Card (desktop, col 1)
  200px diameter centered in card
  Card: 24px padding, neutral-100 background, 16px border radius
  Title "Traffic Sources" neutral-700 16px weight 600
  Legend: 4 items stacked, each 28px height
  Legend dot 12px + label 13px neutral-600 + percentage 13px neutral-500
  Segments: Referral primary 35%, Direct accent 30%, Organic success 20%, Social primary-light 15%
  Shadow 0 8px 32px rgba(0,0,0,0.08)
  Hover segment expands 4px outward with 0.2s ease
Bar Chart Card (desktop, col 2-3)
  Spans 2 columns
  Title "Weekly Activity" neutral-700 16px weight 600
  8 horizontal bars
  Bar height 44px, gap 10px
  Odd bars primary, even bars accent
  Bar label left (day abbreviation) 12px neutral-600 width 32px
  Value right 12px neutral-700 weight 600
  Bar fill max width 320px
  Border radius 8px on fill right edge
  No grid, no axes
  Tooltip on bar hover: pill 120px width max, neutral-800 bg, white 12px, arrow pointing down from center
  Hover bar raises shadow 0 4px 12px rgba(0,0,0,0.12), slight scale 1.02
  Card padding 24px
Activity Feed Card (desktop, col 1, below pie)
  Title "Recent Activity" neutral-700 14px weight 600
  5 rows, 40px height each
  Icon left each row: 32px circle, primary-light bg for new items, neutral-200 for read items
  Text: action bold neutral-700 12px + timestamp neutral-400 11px
  Row hover: neutral-200 background shift 0.15s
  Last row no divider
  Card padding 20px
Color Transitions (max 6)
  1. neutral-50 to neutral-100 (bg to card)
  2. neutral-100 to primary-light (card to active nav)
  3. neutral-600 to primary (text to link/active)
  4. neutral-400 to neutral-600 (disabled to enabled)
  5. neutral-100 to neutral-200 (card to hover row)
  6. primary to primary-dark (default to active/click)
DOM Budget Count (20 max)
  1 header bar
  1 sidebar panel
  3 stats cards
  1 pie chart card
  1 pie chart SVG
  1 pie legend container
  1 bar chart card
  1 bar chart container (8 bars)
  1 activity feed card
  1 activity feed list (5 rows)
  1 bottom nav (mobile)
  1 notification badge
  1 user avatar
  1 nav separator
  1 breadcrumb
  1 app logo
  Total: 18 containers (within limit)
Nesting depth max: header > breadcrumb container > breadcrumb items (3 levels). Within limit of 4.
Total unique color transitions: 6. At limit but valid.
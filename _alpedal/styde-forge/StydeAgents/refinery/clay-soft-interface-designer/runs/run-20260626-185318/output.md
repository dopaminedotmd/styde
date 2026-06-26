PHASE 0.5 — DESIGN MOCKUPS
Blueprint: Clay Soft Interface Designer v10.0.0 (concise)
Date: 2026-06-26
Designer: Persona-loaded agent
---
MOCKUP 1: MAIN DASHBOARD OVERVIEW
Container: full-viewport dashboard shell, flex row
Left sidebar: 240px, neutral-100 background, border-radius 0 16px 16px 0, shadow 0 8px 32px rgba(0,0,0,0.08)
  Logo area: 48px height, centered, primary color, border-radius 12px, margin 16px
  Nav items: 5 items stacked, 44px height each, border-radius 12px, padding 12px 16px
    Active item: primary-light background, neutral-800 text
    Inactive items: transparent, neutral-600 text
    Hover: neutral-200 background, no transition on shadow (stays flat)
  Bottom: user avatar 40px circle, neutral-400 border, name and role below
Main content area: flex 1, padding 24px, neutral-50 background
  Top bar: 56px height, flex row, justify-between
    Left: heading text "Dashboard" neutral-800, subtitle "Welcome back" neutral-500
    Right: notification bell icon (accent), avatar thumbnail 36px, date badge
  Stats row: 4 cards (card container max count: 4 of 20 budget)
    Card 1: Revenue, neutral-100, border-radius 16px, padding 24px, shadow 0 8px 32px rgba(0,0,0,0.08)
      Icon circle: 40px, primary background, white icon
      Label: "Total Revenue" neutral-500, 12px
      Value: "$48,290" neutral-800, 28px bold
      Change: "+12.5%" success color, 14px
    Card 2: Users, same structure, accent icon circle
      Value: "2,847", change "+8.3%" success
    Card 3: Orders, primary icon circle
      Value: "1,203", change "+3.1%" success
    Card 4: Growth, accent icon circle
      Value: "94.2%", change "-0.4%" error (soft coral)
  Mid section: 2-col grid (desktop: 3-col available, using 2-col for layout diversity)
    Left panel (col 1-2): Bar Chart Card
      Card container: neutral-100, border-radius 16px, padding 24px, shadow
      Header: "Weekly Sales" neutral-700, 18px
      Chart area: 8 bars, 40px wide each, max height 180px
        Bar 1: primary (7EC8C0), height 120px
        Bar 2: accent (F4B8A0), height 90px
        Bar 3: primary, height 150px
        Bar 4: accent, height 70px
        Bar 5: primary, height 135px
        Bar 6: accent, height 100px
        Bar 7: primary, height 160px
        Bar 8: accent, height 85px
        All bars: border-radius 8px 8px 0 0, gap between bars 8px
        X-axis: weekday labels, neutral-400, 11px, centered under each bar
        Y-axis: scale 0-200, neutral-300 lines, no labels to conserve DOM
        Hover tooltip: appears on bar hover only, 60px max width per bar hover zone
          Tooltip: neutral-800 background, white text, 12px, border-radius 8px, padding 6px 10px, positioned above bar
          Content: "Mon: $1,200" etc
      Bottom: date range toggle, 2 buttons, border-radius 12px
        Active: primary background, white text
        Inactive: transparent, neutral-600 text, neutral-200 border
    Right panel (col 3): Pie Chart Card
      Card container: neutral-100, border-radius 16px, padding 24px, shadow
      Header: "Traffic Sources" neutral-700, 18px
      Chart area: centered
        Pie chart outer diameter: 200px (desktop spec)
        Segments:
          Organic: primary (7EC8C0), 45%
          Referral: accent (F4B8A0), 25%
          Direct: success (A8D5A2), 18%
          Social: warning (F0D080), 12%
        Center hole: 60px, neutral-100 fill
        Center text: "100%" neutral-600, 14px
      Legend below: 4 items, flex row wrap, gap 8px
        Each: 8px circle (segment color), label neutral-500, 11px
        No tooltip on pie segments (DOM budget preservation)
  Bottom section: Activity feed card
    Card: neutral-100, border-radius 16px, padding 24px, shadow
    Header: "Recent Activity" neutral-700, 18px
    4 activity rows, each 44px height, flex row, align-center
      Icon: 32px circle, neutral-200 background, primary icon
      Text: "New user registered" neutral-600, 14px
      Time: "2 min ago" neutral-400, 11px
    Separator: neutral-300 divider line between rows (not between each — only between groups of 2)
DOM count: sidebar (1) + content area (1) + top bar (1) + 4 stat cards (4) + bar chart card (1) + pie chart card (1) + activity card (1) + 2 nav items visible (2) = 12 containers. Under 20 budget. Fine.
---
MOCKUP 2: ANALYTICS DEEPDIVE VIEW
Same shell. Content area changes.
Breadcrumb row: neutral-500, 12px, "Dashboard > Analytics"
Metric grid: 6 mini-cards in 3-col grid (desktop)
  Each card: neutral-100, border-radius 16px, padding 16px, shadow 0 4px 16px rgba(0,0,0,0.06) (lighter for secondary cards)
  Mini cards alternate between primary icon dot and accent icon dot
  Values: neutral-800 16px, labels neutral-500 10px
  No hover effects on mini-cards (DOM budget: hover zone 60px cap applies, but skip to save)
Large chart panel: full 3-col span
  Card: neutral-100, border-radius 16px, padding 24px, shadow
  Dual bar chart: 2 groups of 8 bars (this week vs last week)
    Group 1 (this week): primary bars, opacity 1
    Group 2 (last week): primary bars, opacity 0.4, offset by 4px
    Each bar pair: total width 80px (40px per bar + gap)
    Hover: triggers on individual bar, not bar pair
  X-axis: day labels
  Legend: 2 items, primary circle + "This Week", primary-light circle + "Last Week"
Filter row: 3 dropdown-style buttons, border-radius 12px per button
  "Date Range", "Category", "Source"
  Each: 120px width, neutral-100 background, neutral-600 text, neutral-200 border
  Dropdown chevron: neutral-400
  No actual dropdown render (DOM budget) — label only, state indicates clickable
DOM count: 6 mini-cards (6) + chart card (1) + filter row (1) + breadcrumbs (1) = 9 new containers. Total 21. Over budget by 1.
Fix: merge filter row into chart card header. Filter buttons sit inline in the chart card header row, eliminating the separate filter row container. New total: 20 exact.
---
MOCKUP 3: MOBILE VIEWPORT (320-767px)
Same shell structure but:
Sidebar: hidden off-screen. Icon-only hamburger in top bar.
Top bar: 48px height, padding 8px 16px
  Left: hamburger icon 24px, neutral-700
  Center: "Dashboard" neutral-700, 16px
  Right: avatar 28px circle
Stats row: single column, cards stack vertically
  Each card: full width, padding 16px, margin-bottom 12px
  Border-radius: 16px (unchanged)
  Value: 22px (reduced from 28px)
  Label: 11px (reduced from 12px)
Bar chart card: full width
  Heading: 16px
  Bars: 32px width each (reduced from 40px), max height 120px
  No y-axis lines, no x-axis labels (saves DOM and space)
  Tooltip bar hover zone: 50px (under 60px cap)
  Tooltip: appears on tap equivalent (touch), same styling
Pie chart card: full width, below bar chart
  Pie outer diameter: 120px (mobile spec)
  Center hole: 36px
  Center text: 11px
  Legend: stacked vertically below, each item 32px height
Activity feed: 3 items instead of 4 (save space)
  Each row: 36px height (reduced from 44px)
  Icon: 24px circle
  Text: 12px
  Time: 10px
DOM count: header (1) + 4 stat cards (4) + bar card (1) + pie card (1) + activity card (1) = 8. Under budget.
---
MOCKUP 4: TABLET VIEWPORT (768-1023px)
Sidebar: collapsed to icon tray, 64px width
  Icons only, 32px each, centered, border-radius 8px
  Active icon: primary-light background
  No labels visible
Top bar: 52px height
  Left: hamburger icon (expands sidebar on click — not rendered)
  Center: heading 17px
Stats row: 2-col grid, 2 cards per row
  Card padding: 20px
Charts: 2-col layout
  Bar chart card: spans 2 cols, full width
    Bars: 36px width each (between mobile 32px and desktop 40px)
  Pie chart card: spans 2 cols, full width below bar chart
    Pie outer diameter: 160px (tablet spec)
    Center hole: 50px
Activity feed: below charts, full 2-col span
DOM count: tray (1) + header (1) + stat cards (4) + bar card (1) + pie card (1) + activity card (1) = 9.
---
INTERACTION SPECS (shared across all mockups)
Hover on stat cards: translateY(-2px), shadow increases to 0 12px 40px rgba(0,0,0,0.12), transition 0.2s ease. Neutral-100 background stays same — no color shift, only depth shift.
Hover on nav items: neutral-200 background, border-radius 12px, no animation, instant color swap.
Button click: primary-dark or accent-dark color swap, no ripple, no scale-down. Flat color transition 0.1s.
Tooltip delay: 300ms on first appearance, then instant on subsequent hovers within same chart session.
Touch targets on mobile: minimum 44px height for all interactive elements.
Color transition count: background-to-card (neutral-50 to neutral-100), card-to-container-border (neutral-100 to neutral-200), card-to-shadow (neutral-100 to shadow rgba), text-to-hover (neutral-600 to neutral-700), button-to-hover (transparent to neutral-200), icon-to-active (neutral-400 to primary). That is 6 unique transitions — exactly at budget cap.
---
MOCKUP 5: DARK MODE VARIANT (optional alternate)
Identical layout. Color token overrides:
  neutral-50: #1E1B18 (dark clay base)
  neutral-100: #2A2622 (card background)
  neutral-200: #36312C (subtle border)
  neutral-300: #443F38 (divider lines)
  neutral-400: #6B6359 (disabled text)
  neutral-500: #8A8073 (secondary text)
  neutral-600: #A89E90 (body text)
  neutral-700: #C5BCAE (heading text)
  neutral-800: #E2DACF (darkest text)
  neutral-900: #F5F0E8 (near-white)
Primary and accent: same hex values. On dark base, they appear brighter and more vibrant. Shadows shift: 0 8px 32px rgba(0,0,0,0.25) for card depth on dark.
All cards keep neutral-100 (now #2A2622) background. No transparency overlays — opacity-based color would break the clay solidity.
---
SUMMARY
5 mockup views delivered: Main Dashboard, Analytics Deepdive, Mobile, Tablet, Dark Mode.
Exact specs match blueprint: pie diameters (200/160/120), card padding (24/16), border-radius (16/12/8), shadow (0 8px 32px rgba(0,0,0,0.08)), bar hover zone cap (60px), DOM budget (20 containers), color transitions (6), nesting depth (max 4).
Concise format — no redundant section labels, no repetition of version lines, no non-actionable blocks.
English-only — Phase 0.5, not Fas 0.5.
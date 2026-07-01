Phase 0.5 Design Mockup
Component: Analytics Dashboard
Grid Layout (3 cols desktop, 2 cols tablet, 1 col mobile)
Card 1 - col-span 2 desktop, col-span 2 tablet, col-span 1 mobile
  Title: Active Sessions
  Radius: 16px
  Padding: 24px inner
  Shadow: 0 8px 32px rgba(0,0,0,0.08)
  Background: neutral-100 #F0EBE3
  Content: Bar chart, 8 bars
  Bar odd (1,3,5,7): primary #7EC8C0
  Bar even (2,4,6,8): accent #F4B8A0
  Tooltip: on bar hover only, max 60px width per bar
  Hover state: bar opacity drops to 0.85, tooltip fades in
Card 2 - col-span 1 desktop, col-span 2 tablet, col-span 1 mobile
  Title: Metrics Overview
  Radius: 16px
  Padding: 24px inner
  Shadow: 0 8px 32px rgba(0,0,0,0.08)
  Background: neutral-100 #F0EBE3
  Content: Pie chart, outer diameter 200px desktop / 160px tablet / 120px mobile
  Segments: primary #7EC8C0, accent #F4B8A0, success #A8D5A2, warning #F0D080
  Tooltip: on segment hover only
Card 3 - col-span 1 desktop, col-span 1 tablet, col-span 1 mobile
  Title: Top Pages
  Radius: 16px
  Padding: 24px inner
  Shadow: 0 8px 32px rgba(0,0,0,0.08)
  Background: neutral-100 #F0EBE3
  Content: List of 5 page entries with hit counts
  Radius on entries: 12px
  Hover: background shifts to primary-light #A8DFDA at 0.3 opacity
Card 4 - col-span 1 desktop, col-span 1 tablet, col-span 1 mobile
  Title: Quick Actions
  Radius: 16px
  Padding: 24px inner
  Shadow: 0 8px 32px rgba(0,0,0,0.08)
  Background: neutral-100 #F0EBE3
  Buttons: 12px radius, primary #7EC8C0 bg
  Button hover: primary-light #A8DFDA
  Button active: primary-dark #5BA8A0
State Coverage:
  Loading: skeleton shimmer on all cards, neutral-200 #E5DDD0 base with neutral-100 overlay sweep
  Empty: neutral-500 text "No data yet" centered in card, accent-light #FCD4C0 icon above
  Error: error #E8A098 border on failed card, error text muted to 0.8 opacity
  Dark mode: all colors shift -15 lightness, shadows become 0 8px 32px rgba(0,0,0,0.25)
  Hover/focus: every interactive element has distinct hover state defined above
Typography:
  h1: neutral-800, 28px, 700 weight, 1.3 line-height
  h2: neutral-700, 22px, 600 weight, 1.35 line-height
  h3: neutral-700, 18px, 600 weight, 1.4 line-height
  h4: neutral-600, 16px, 500 weight, 1.4 line-height
  body: neutral-600, 14px, 400 weight, 1.5 line-height
  caption: neutral-500, 12px, 400 weight, 1.4 line-height
  letter-spacing: h1-h2 -0.01em, body/caption normal
DOM Budget:
  Total containers: 12 (4 cards + 4 inner panels + 2 chart containers + 1 grid wrapper + 1 header)
  Color transitions: 5 (bar hover, button hover, list hover, tooltip fade, card shadow)
  Hover-zone max width: 60px per bar
  Max nesting depth: 3 (grid > card > chart > bar)
Responsive Behavior:
  Mobile (320-767px): single column, pie chart 120px, all cards full width
  Tablet (768-1023px): 2-column grid, cards 1-2 span 2 cols, cards 3-4 stack below, pie 160px
  Desktop (1024+): 3-column grid, card 1 spans 2 cols, others 1 col, pie 200px
Validation Gate (post-generation):
  Confirm every CSS nth-child selector maps to actual DOM element
  Confirm bar width does not exceed 60px hover zone
  Confirm no container exceeds depth 4 in any breakpoint
Content Samples:
  Sessions per page: /dashboard (245), /profile (189), /settings (134), /analytics (312), /admin (78)
  Top pages: Home (312 visits), Dashboard (245), Profile (189), Settings (134), Admin (78)
  Pie segments: Direct 45%, Organic 30%, Referral 15%, Social 10%
  Quick actions: New Report, Export CSV, Share Dashboard, Schedule Email
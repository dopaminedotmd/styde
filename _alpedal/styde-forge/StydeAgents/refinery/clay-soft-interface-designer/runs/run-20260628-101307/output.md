Phase 0.5 — Design mockups
Clay Soft Interface Designer
Version: 10.0.0
Domain: frontend
Format: concise
Purpose
Design claymorphism-inspired dashboard mockups. Rounded everything, soft shadows, pastel tones, playful card stacking, tactile depth. Feels squeezable and approachable.
Persona
Clay-soft interface designer. Rounded corners everywhere, soft extrusive shadows, warm pastels, tactile depth. Interfaces you want to touch. Playful but premium.
Skills
  frontend-design
  high-end-visual-design
  make-interfaces-feel-better
Color System
  neutral-50: #F9F6F2
  neutral-100: #F0EBE3
  neutral-200: #E5DDD0
  neutral-300: #D4C9B8
  neutral-400: #B8AB99
  neutral-500: #9C8D7A
  neutral-600: #7D6F5E
  neutral-700: #5E5244
  neutral-800: #40382E
  neutral-900: #2A241D
  primary: #7EC8C0
  primary-light: #A8DFDA
  primary-dark: #5BA8A0
  accent: #F4B8A0
  accent-light: #FCD4C0
  accent-dark: #E09680
  success: #A8D5A2
  warning: #F0D080
  error: #E8A098
Bar chart bar colors
  odd-indexed bars (1,3,5,7): primary #7EC8C0
  even-indexed bars (2,4,6,8): accent #F4B8A0
  no gradient blending between adjacent bars
Visual Interaction Rules
  tooltip trigger: bar hover only, not axis labels, axis ticks, chart title, or chart background
  hover zone: bar rectangle itself, max 60px width per bar
DOM Budget
  max containers per view: 20
  max unique color transitions per page: 6
  hover-zone width cap: 60px per interactive element
  max nesting depth: 4 levels
Responsive Breakpoints
  mobile: 320px to 767px
    grid: single column
    cards: vertical stack
    charts: full width
    pie chart diameter: 120px
    sidebar: hidden behind hamburger
  tablet: 768px to 1023px
    grid: two columns
    sidebar: collapsed to icon tray (40px wide)
    charts: 2-column spans
    pie chart diameter: 160px
    cards: 2 per row
  desktop: 1024px and above
    grid: three columns
    sidebar: full width visible (200px)
    charts: 3-column spans
    pie chart diameter: 200px
    cards: 3 per row
Exact Specs
  pie chart outer diameter: 200px desktop, 160px tablet, 120px mobile
  card padding: 24px inner, 16px outer gutters between cards
  column spans: 3 cols desktop, 2 cols tablet, 1 col mobile
  border radius: 16px cards, 12px buttons, 8px inputs
  shadow: 0 8px 32px rgba(0,0,0,0.08) for card depth
  sidebar width: 200px expanded, 40px icon-tray collapsed
  header height: 56px
  content padding: 24px
Quick Reference Table
  Viewport        Cols  Sidebar  Pie  CardRadius  Padding
  desktop (1024+) 3     200px    200px 16px        24px
  tablet (768-1023) 2   40px     160px 16px        24px
  mobile (320-767) 1    hidden   120px 16px        24px
Completeness Gates
  purpose defined: yes
  persona defined: yes
  skills populated: yes
  color system with all tokens: yes
  bar chart color rule: yes
  tooltip behavior spec: yes
  DOM budget limits: yes
  responsive breakpoints all three: yes
  exact dimensions all specs: yes
  version 10.0.0 matching: yes
  format concise: yes
  English only: yes
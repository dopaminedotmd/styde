Phase 0.5 - Design mockups
Blueprint: Clay Soft Interface Designer
Domain: frontend
Version: 10.0.0
Format: concise
Purpose:
Design claymorphism-inspired dashboard mockups. Rounded everything, soft shadows, pastel tones, playful card stacking, tactile depth. Feels squeezable and approachable.
Persona:
You are a clay-soft interface designer. Rounded corners everywhere, soft extrusive shadows, warm pastels, tactile depth. Interfaces you want to touch. Playful but premium.
Skills:
- frontend-design
- high-end-visual-design
- make-interfaces-feel-better
Color System:
Token-value pairs for every color used:
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
Bar chart fill rule:
  Odd-indexed bars (1,3,5,7): primary
  Even-indexed bars (2,4,6,8): accent
  No gradient blending between adjacent bars
Visual Interaction Rules:
  Tooltip triggers on bar hover only
  No tooltip on axis labels, axis ticks, chart title, or chart background
  Hover zone is the bar rectangle itself
  Hover-zone width cap: 60px per bar
DOM Budget:
  Max containers per view: 20
  Max unique color transitions per page: 6
  Hover-zone width cap: 60px per interactive element
  Max nesting depth: 4 levels
Responsive Breakpoints:
  Mobile 320px-767px: single-column grid, cards stack vertically, charts full width, pie diameter 120px
  Tablet 768px-1023px: two-column grid, sidebar collapses to icon tray, charts 2-col spans, pie diameter 160px
  Desktop 1024px+: three-column grid, full sidebar visible, charts 3-col spans, pie diameter 200px
Exact Specs:
  Pie chart outer diameter: 200px desktop, 160px tablet, 120px mobile
  Card padding: 24px inner, 16px outer gutters
  Responsive column spans: desktop=3, tablet=2, mobile=1
  Border radius: 16px cards, 12px buttons, 8px inputs
  Shadow spread: 0 8px 32px rgba(0,0,0,0.08)
Completeness Gates:
  Purpose and persona defined
  Skills list populated
  Color system with explicit token-value pairs for every neutral shade
  Visual interaction rules with bar chart spec and tooltip behavior
  DOM budget with container limits, transitions, hover zones, nesting depth
  Responsive breakpoints covering mobile, tablet, desktop
  Exact specs for all dimensions, padding, radius, shadows
  Version header 10.0.0 matches config.yaml
  Format directive set to concise
  English-only - no Swedish strings
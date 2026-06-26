--- CLAY-SOFT DASHBOARD BLUEPRINT v2 ---
Component: Analytics Overview Dashboard
Style: Claymorphism (clay-soft)
Variant: Premium + Playful
COLOR PALETTE
primary-base: #B8A9E8    soft lavender
primary-light: #D4C9F5   whisper lavender
accent-warm: #F5C6A0     peach cream
accent-cool: #A0D2DB     seafoam whisper
surface: #F9F5F0         warm cream
card-base: #FDFBF8       off-white clay
shadow-warm: rgba(180,160,140,0.25)
shadow-accent: rgba(160,140,180,0.2)
text-primary: #3A3545     deep clay
text-soft: #7A7590        muted clay
success-moss: #B5C9A8     sage
warning-honey: #E8C87A    honey
danger-coral: #E89A8A     coral
GEOMETRY
border-radius-sm: 16px
border-radius-md: 24px
border-radius-lg: 32px
border-radius-xl: 40px
border-radius-pill: 60px
card-padding-sm: 16px
card-padding-md: 24px
card-padding-lg: 32px
shadow-spread-sm: 0 8px 24px shadow-warm
shadow-spread-md: 0 12px 36px shadow-warm
shadow-spread-lg: 0 16px 48px shadow-warm
shadow-inset-sm: inset 0 2px 4px rgba(255,255,255,0.6), inset 0 -2px 4px shadow-warm
stroke-width-card: 1.5px
stroke-color-card: rgba(255,255,255,0.5)
LAYOUT SPEC
grid-template: 12 columns, gap 24px
max-container-width: 1440px
inner-gutter: 32px
mobile: 320px to 767px, single column, gap 16px
tablet: 768px to 1023px, 6 columns, gap 20px
desktop: 1024px to 1440px, 12 columns, gap 24px
DOM BUDGET LIMITS
max-container-count: 18
max-unique-color-transitions: 6
max-hover-zone-width: 56px
max-nesting-depth: 3 levels
max-animated-elements-per-view: 4
COMPONENT INVENTORY
CARD STACK
  layered card pile with 3 depth levels
  each layer offset 4px down, 2px right
  top card: full shadow, bottom cards: progressively darker shadow-warm
  on hover: top card lifts 8px, shadow doubles
  border-radius: 24px on all layers
  background: card-base with subtle gradient (same base + 2% darker at bottom)
STAT CARD
  single clay card with icon, value, label, trend indicator
  icon sits in a pill-shaped container (border-radius-pill, bg primary-light)
  value in text-primary, 32px, weight 600
  label in text-soft, 14px, weight 400
  trend indicator: arrow + percentage in success-moss or danger-coral
  hover: card lifts 6px, shadow intensifies
  color alternation scheme: every odd stat card gets primary-base accent stripe on left edge, even cards get accent-warm stripe on left edge
  left accent stripe: width 6px, border-radius 6px, vertically centered
BAR CHART
  8 bars, labels below
  bars use color alternation: odd bars (1,3,5,7) -> accent-cool, even bars (2,4,6,8) -> accent-warm
  each bar width: 32px at desktop, shrinks proportionally on mobile
  max bar height: 200px
  bar border-radius: 8px 8px 0 0 (rounded top, flat bottom)
  bar background: gradient top to bottom, same color but lightens 15% at top
  hover: bar widens to 40px, reveals tooltip
  tooltip trigger: bar hover ONLY -- not axis labels, not chart area background
  tooltip: appears above bar, offset 8px up, border-radius 16px, padding 8px 16px, bg text-primary, text card-base, font 13px
  axis: no visible axis lines, only text labels in text-soft
PIE CHART / RADIAL METER
  circular clay donut, stroke-width 24px
  segments: lavender (62%), peach (23%), seafoam (15%)
  center hole: 40% of outer diameter
  center text: percentage value, text-primary, 28px
  center label: text-soft, 12px
  hover on segment: segment expands 6px outward, show label tooltip
RECENT ACTIVITY FEED
  list of 5 items
  each item: icon (in 36px circle, border-radius 18px), title, timestamp, status dot
  icon circles use alternating bg: primary-light or accent-warm
  title: text-primary, 15px, weight 500
  timestamp: text-soft, 12px
  status dot: 8px circle, border-radius 4px, colored by status (success-moss, warning-honey, danger-coral)
  item divider: 1px line, stroke-color-card, horizontal, opacity 0.5
  hover: background shifts to primary-light at 30% opacity, border-radius 16px
HEADER
  clay pill shape, full-width, border-radius 40px
  height: 72px
  padding: 0 32px
  contains: logo area (left), navigation pills (center), profile avatar (right)
  navigation pills: each is border-radius 40px, padding 10px 24px, bg transparent
  active nav pill: bg primary-base, text card-base
  inactive nav pill: text text-soft, hover = bg primary-light at 40%
ANIMATION TOKENS
card-hover: transform translateY(-6px), shadow spread increase, duration 200ms, ease-out
bar-hover: width 40px, border-radius 8px 8px 4px 4px, duration 150ms, ease-out
segment-hover: transform scale(1.08), duration 200ms, ease-out
entry-animation: fadeInUp, 8px offset, duration 350ms, stagger children 80ms
micro-interaction: press card -> scale(0.97) on mousedown, duration 80ms
RESPONSIVE BREAKPOINTS
mobile: 320px to 767px
  single column stack
  stat cards: full width
  bar chart: bars shrink to 24px
  pie chart: centers above activity feed
  header height: 56px, nav pills collapse to icon-only
tablet: 768px to 1023px
  2-column stat cards
  bar chart + pie chart side by side
  header nav shows text for top 3 items
desktop: 1024px to 1440px
  12-column grid
  stat cards row (4 columns each)
  bar chart spans 7 cols, pie chart spans 5 cols
  activity feed spans full width
ITERATION LIMITS
max-blueprint-iterations: 3
after-3-escalation: flag for human review with changelog of attempted improvements
each-iteration-must-address: lowest scoring criterion from previous eval
acceptance-gates:
  phase-gate-1: all components defined in inventory (pass/fail)
  phase-gate-2: DOM budget within limits (pass/fail)
  phase-gate-3: responsive breakpoints cover all 3 tiers (pass/fail)
  phase-gate-4: color alternation scheme explicit for all repeated elements (pass/fail)
EVALUATION CRITERIA
completeness: 25 points -- all components fully specified
efficiency: 20 points -- DOM budget + responsive + performance tokens
usefulness: 20 points -- implementation-ready, no ambiguity
clarity: 20 points -- every rule explicit, no assumptions needed
aesthetics: 15 points -- visual quality of clay-soft design
pass-threshold: 80 composite
production-threshold: 85 composite
VALIDATION CHECKLIST
  all component geometries defined with px values
  color tokens mapped to every element
  hover states specified behavior + timing
  responsive rules for mobile tablet desktop
  DOM limits enumerated
  color alternation rules explicit for all repeated components
  tooltip trigger events explicitly scoped
  animation duration + easing + transform values given
  acceptance gate criteria defined
  iteration limit + escalation path documented
--- END BLUEPRINT ---
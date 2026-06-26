Clay Soft Dashboard — Design Specification v6
---
Typography Scale:
font-family: 'Nunito', 'Quicksand', system-ui, sans-serif
h1: 32px/1.2 weight 700
h2: 24px/1.3 weight 700
h3: 20px/1.4 weight 600
h4: 18px/1.4 weight 600
body: 16px/1.6 weight 400
body-small: 14px/1.5 weight 400
caption: 12px/1.4 weight 500
label: 14px/1.4 weight 600
button: 16px/1 weight 700 letter-spacing 0.3px
number-stat: 28px/1 weight 800
---
Color Palette — Light Mode:
background: #f8f3ee (warm cream)
surface-primary: #ffffff
surface-secondary: #fdf6ee
card-bg: #ffffff
header-bg: #f5ede4
sidebar-bg: #f0e8de
primary: #b88a6b (warm clay brown)
primary-hover: #a0765a
primary-light: #e8d5c4
primary-dark: #7a5a44
accent: #c9a88e (rose clay)
accent-hover: #b89178
accent-light: #f0e0d4
success: #8db88a (sage green)
success-light: #dce8da
warning: #e0c080 (honey)
warning-light: #f5ecd0
error: #d4948a (dusty rose)
error-light: #f0d8d4
neutral-100: #f8f3ee
neutral-200: #ede4db
neutral-300: #d9cec3
neutral-400: #b8a99a
neutral-500: #8f7e6e
neutral-600: #6b5b4e
neutral-700: #4a3f36
neutral-800: #2d2620
neutral-900: #1a1612
text-primary: #2d2620
text-secondary: #6b5b4e
text-muted: #8f7e6e
text-inverse: #f8f3ee
shadow-color: rgba(107, 91, 78, 0.12)
shadow-dark: rgba(42, 35, 30, 0.18)
---
Color Palette — Dark Mode:
background: #1e1a16
surface-primary: #2a251f
surface-secondary: #322c25
card-bg: #2e2821
primary: #d4ad90 (lighter clay for dark bg)
primary-hover: #e0bfa8
primary-light: #3d322a
primary-dark: #b88a6b
accent: #dbb9a2
accent-hover: #e6ccbb
accent-light: #3d332c
success: #8db88a
success-light: #2a3828
warning: #d4b060
warning-light: #3a3220
error: #c98880
error-light: #382826
neutral-800 becomes neutral-100 equivalent, etc.
text-primary: #ede4db
text-secondary: #b8a99a
text-muted: #8f7e6e
text-inverse: #1a1612
shadow-color: rgba(0, 0, 0, 0.40)
shadow-dark: rgba(0, 0, 0, 0.55)
---
Animation System:
duration-fast: 150ms
duration-normal: 250ms
duration-slow: 400ms
duration-page: 600ms
duration-entrance: 800ms
ease-default: cubic-bezier(0.34, 1.56, 0.64, 1) (clay bounce)
ease-out: cubic-bezier(0.16, 1, 0.3, 1)
ease-in: cubic-bezier(0.4, 0, 0.6, 1)
ease-smooth: cubic-bezier(0.22, 1, 0.36, 1)
ease-spring: cubic-bezier(0.34, 1.56, 0.64, 1)
anim-card-hover: transform 250ms ease-spring, box-shadow 250ms ease-out
anim-card-entrance: transform 400ms ease-out, opacity 400ms ease-out, stagger 80ms per card
anim-fade-in: opacity 300ms ease-out
anim-slide-up: transform 400ms ease-out, opacity 400ms ease-out — translateY(16px) to translateY(0)
anim-button-press: transform 100ms ease-in — scale(0.97)
anim-modal-backdrop: opacity 250ms ease-out
anim-modal-content: transform 400ms ease-spring, opacity 300ms ease-out — translateY(24px) to translateY(0) scale(0.97) to scale(1)
anim-tooltip: opacity 200ms ease-out, transform 200ms ease-out
anim-chart-bar: transform 600ms ease-out, opacity 600ms ease-out — scaleY(0) to scaleY(1) using transform-origin bottom
anim-chart-fill: 800ms ease-smooth
anim-skeleton: pulse 1.5s ease-in-out infinite — keyframes 0%/opacity 1, 50%/opacity 0.5, 100%/opacity 1
---
Loading States:
Card skeleton: rounded 16px placeholder blocks with pulse animation
  avatar skeleton: 40x40px circle, border-radius 50%
  title skeleton: 60% width, 20px height, border-radius 8px
  body skeleton: 100% width, 14px height x3 stacked 8px apart, border-radius 8px
  bar chart skeleton: 8 vertical bars 40px-80px height, border-radius 8px
Full-page loader: centered clay orb with soft 3D sphere shading, gentle pulse + rotate animation, 80px diameter
Skeleton color: light mode neutral-200, dark mode neutral-700
Skeleton highlight: linear-gradient to right with opacity shift
---
Empty States:
Empty card: 120x120px clay illustration placeholder (soft circle with subtle inner shadow), centered
Empty text: "Nothing here yet" in text-secondary, 16px
Empty subtext: "Data will appear once collected" in text-muted, 14px
Empty action button: primary outlined button "Add your first item"
Empty state uses same card container (16px border-radius, shadow) with dashed border 2px neutral-300
Padding within empty card: 48px top/bottom
---
Error States:
Inline error: 12px below input, error color, weight 500
Card error overlay: 60% opacity surface-primary background, centered icon (exclamation circle) + "Something went wrong" + "Retry" button
Full-page error: centered card with error-light background, 24px border-radius, icon 48px, heading h3, body text, primary button "Try Again"
Error boundary: red dashed 1px border with 8px border-radius around failed component
Toast error: fixed bottom-right, 24px border-radius, error-light bg, dismiss after 5s or tap
---
Focus Indicators:
global focus-visible: 3px solid primary, border-radius matches element, offset 2px
focus-visible on cards: 3px solid primary-light, border-radius 16px, offset 2px
focus-visible on buttons: 3px solid primary-dark, border-radius 14px, offset 2px
focus-visible on inputs: 3px solid primary, border-radius 10px, offset 2px
focus-visible on links: 3px underline offset 4px, border-radius 2px
focus-visible on chart elements: 3px solid accent, border-radius 4px, offset 1px
Never remove default outline without replacing with custom focus style
High contrast mode: 2px solid currentColor, no border-radius, offset 4px
---
Loading/Empty/Error Checklist:
[ ] All data-dependent cards have skeleton loading variant
[ ] All lists/table have empty state with illustration
[ ] All API calls have error state with retry action
[ ] Chart loading shows bar skeleton not blank space
[ ] Empty dashboard shows onboarding prompt
[ ] Error toasts auto-dismiss within 5-8 seconds
---
Accessibility Checklist:
[ ] Color contrast all text/text-secondary pairs pass WCAG AA (4.5:1)
[ ] Focus indicators visible on all interactive elements
[ ] Animation respects prefers-reduced-motion: all anims reduce to opacity-only at 200ms
[ ] Touch targets minimum 44x44px on mobile
[ ] Screen reader labels on all icons, chart elements, buttons
[ ] Tab order follows visual layout (left-to-right, top-to-bottom)
[ ] Chart data available as screen-reader table
[ ] Dark mode toggle respects prefers-color-scheme
---
Responsive Grid Layout:
mobile 320-767: 1 col, card-padding 16px outer, 12px inner gutters
tablet 768-1023: 2 col, card-padding 24px outer, 16px inner gutters
desktop 1024+: 3 col, card-padding 32px outer, 24px inner gutters
Card stacking order: stats row on top, charts middle, table bottom
On mobile, info hierarchy collapses to vertical stack no exceptions
---
Claymorphism Visual Effects:
card-background: solid fill with subtle inner shadow inset 0 2px 4px rgba(255,255,255,0.5) light mode / inset 0 1px 2px rgba(255,255,255,0.05) dark mode
card-shadow: 0 8px 32px shadow-color, plus 0 2px 8px shadow-dark for depth, plus 0 12px 40px -8px shadow-color for extrusion
card-hover: transform translateY(-4px), shadow increases to 0 12px 48px shadow-color, 0 4px 16px shadow-dark
button-3d: lighter top 50% gradient, darker bottom 50%, active state pushes shadow in and translateY(2px)
indent-element: inset shadow on pressed states, input fields, depressed buttons
---
Post-Generation Review:
Before submitting this specification, scan against the completeness checklist below. Every field must be populated with concrete values. No empty slots.
Completeness Gate:
[ ] typography scale with sizes/weights/line-heights — PASS
[ ] font stack declared — PASS
[ ] full color palette hex codes light+dark — PASS
[ ] animation durations all defined — PASS
[ ] easing curves with cubic-bezier values — PASS
[ ] loading state specifications — PASS
[ ] empty state specifications — PASS
[ ] error state specifications — PASS
[ ] focus indicator styles and dimensions — PASS
[ ] dark mode color tokens (every semantic token mapped) — PASS
[ ] responsive breakpoints with concrete dimensions — PASS
[ ] all DOM budget constraints met — PASS
Typography scale
h1 h2 h3 h4 h5 h6 body small
h1: font-family 'Inter', sans-serif, 800, 3rem/1.1, -0.02em
h2: font-family 'Inter', sans-serif, 700, 2.25rem/1.2, -0.015em
h3: font-family 'Inter', sans-serif, 600, 1.75rem/1.25, -0.01em
h4: font-family 'Inter', sans-serif, 600, 1.375rem/1.3, -0.005em
h5: font-family 'Inter', sans-serif, 500, 1.125rem/1.35, 0em
h6: font-family 'Inter', sans-serif, 500, 0.9375rem/1.4, 0.005em
body: font-family 'Inter', sans-serif, 400, 1rem/1.6, 0em
small: font-family 'Inter', sans-serif, 400, 0.8125rem/1.5, 0.01em
Form controls
input text textarea select checkbox radio toggle
Base: 1rem/1.5, 0.75rem 1rem padding, 1px solid var(--border), 8px radius, bg var(--surface), color var(--text)
Hover: border-color var(--border-hover)
Focus: outline 2px solid var(--focus), outline-offset 2px, border-color var(--focus)
Disabled: opacity 0.5, cursor not-allowed, bg var(--surface-muted)
Error: border-color var(--error), box-shadow 0 0 0 3px var(--error-alpha)
Readonly: bg var(--surface-muted), cursor default
checkbox radio: 1.25rem square/round, accent-color var(--primary), focus-visible ring
toggle: 2.75rem x 1.5rem pill, bg var(--border), checked bg var(--primary), knob 1.25rem circle
select: custom arrow svg data uri, 8px radius, appearance none
textarea: min-h 6rem, resize vertical
Responsive breakpoints
sm: 640px
md: 768px
lg: 1024px
xl: 1280px
2xl: 1536px
mobile-first: base styles outside media queries, overrides inside min-width media queries
container max-widths: sm 640px, md 768px, lg 1024px, xl 1280px, 2xl 1536px
container padding: 1rem, md 1.5rem, lg 2rem
Dark mode
@media (prefers-color-scheme: dark) or [data-theme='dark']
surface: #ffffff -> #1a1a2e
surface-alt: #f8f9fa -> #16213e
surface-muted: #e9ecef -> #0f3460
text: #1f2937 -> #e4e6eb
text-secondary: #6b7280 -> #9ca3af
text-muted: #9ca3af -> #6b7280
border: #d1d5db -> #374151
border-hover: #9ca3af -> #4b5563
primary: #2563eb -> #60a5fa
primary-hover: #1d4ed8 -> #93c5fd
secondary: #64748b -> #94a3b8
error: #dc2626 -> #fca5a5
error-alpha: rgba(220,38,38,0.15) -> rgba(248,113,113,0.2)
success: #16a34a -> #86efac
warning: #d97706 -> #fcd34d
focus: #3b82f6 -> #60a5fa
bg: var(--surface) -> same var pattern driven by token
overlay: rgba(0,0,0,0.5) -> rgba(0,0,0,0.7)
shadow: 0 1px 3px rgba(0,0,0,0.1) -> 0 1px 3px rgba(0,0,0,0.4)
Animation system
duration: 50ms 100ms 150ms 200ms 300ms 400ms 500ms 700ms 1000ms
easing:
  default: cubic-bezier(0.4, 0, 0.2, 1)
  enter: cubic-bezier(0, 0, 0.2, 1)
  exit: cubic-bezier(0.4, 0, 1, 1)
  spring: cubic-bezier(0.34, 1.56, 0.64, 1)
  linear: linear
transition defaults:
  interactive elements: background-color 150ms ease, border-color 150ms ease, color 150ms ease, box-shadow 150ms ease, opacity 150ms ease
  transform: transform 200ms spring
motion preferences:
  @media (prefers-reduced-motion: reduce)
    * animation-duration 0.01ms !important
    * transition-duration 0.01ms !important
    * scroll-behavior auto !important
keyframes:
  fadeIn: opacity 0->1, 200ms ease
  fadeOut: opacity 1->0, 150ms ease
  slideDown: translateY(-0.5rem)->translateY(0), opacity 0->1, 200ms ease
  slideUp: translateY(0)->translateY(-0.5rem), opacity 1->0, 150ms ease
  scaleIn: scale(0.95)->scale(1), opacity 0->1, 150ms ease
  spin: rotate(0deg)->rotate(360deg), 1s linear infinite
  pulse: opacity 1->0.5->1, 2s ease infinite
  skeleton: bg linear-gradient(90deg, var(--surface-muted) 25%, var(--surface-alt) 50%, var(--surface-muted) 75%) bg-size 200% 100%, 1.5s linear infinite
Navigation styles
navbar:
  height 4rem, bg var(--surface), border-bottom 1px solid var(--border), sticky top 0, z-index 100, flex between center, padding 0 1.5rem
  items: flex row, gap 1.5rem, font-weight 500
  active: color var(--primary), border-bottom 2px solid var(--primary)
  mobile: transform translateY(-100%) hidden, show on hamburger toggle
sidebar:
  width 16rem, bg var(--surface-alt), border-right 1px solid var(--border), overflow-y auto, flex column gap 0.25rem, padding 1rem
  item: padding 0.625rem 1rem, radius 6px, color var(--text-secondary), hover bg var(--surface-muted)
  active: bg var(--primary-alpha), color var(--primary), font-weight 600
  collapsible: sub-items hidden, toggled via aria-expanded caret
tabs:
  flex row, border-bottom 2px solid var(--border), gap 0
  tab: padding 0.75rem 1.25rem, color var(--text-secondary), border-bottom 2px solid transparent, margin-bottom -2px, cursor pointer, transition colors 150ms ease
  active: color var(--primary), border-bottom-color var(--primary)
  hover: color var(--text)
breadcrumbs:
  flex row, gap 0.5rem, align-items center, font-size 0.875rem, color var(--text-secondary)
  separator: content '/' or chevron, color var(--text-muted)
  current: color var(--text), font-weight 500, text-decoration none
pagination:
  flex row, gap 0.25rem, align-items center
  page: 2.25rem square, flex center, radius 6px, color var(--text-secondary), bg transparent
  active: bg var(--primary), color white, font-weight 600
  hover: bg var(--surface-muted)
  disabled: opacity 0.4, cursor not-allowed
hamburger:
  2.25rem square, flex column center, gap 4px, cursor pointer, padding 4px
  line: 1.5rem x 2px, bg var(--text), radius 2px, transition all 200ms ease
  open: top line rotate 45deg translateY(6px), middle line opacity 0, bottom line rotate -45deg translateY(-6px)
Accessibility
focus-visible: outline 2px solid var(--focus), outline-offset 2px, radius inherits parent
  button:focus-visible, a:focus-visible, input:focus-visible, select:focus-visible, textarea:focus-visible, [tabindex]:focus-visible
  do NOT hide outline on :focus when using :focus-visible polyfill
color contrast ratios:
  text on surface: body 1f2937 on ffffff = 16.4:1, passes AAA
  text-secondary on surface: 6b7280 on ffffff = 4.8:1, passes AA
  text on surface dark: e4e6eb on 1a1a2e = 11.2:1, passes AAA
  primary on surface: 2563eb on ffffff = 6.1:1, passes AA
  primary on surface dark: 60a5fa on 1a1a2e = 6.8:1, passes AA
  error on surface: dc2626 on ffffff = 4.6:1, passes AA
reduced motion: all transitions and animations set to 0.01ms when prefers-reduced-motion active
screen-reader utilities:
  .sr-only: position absolute, width 1px, height 1px, padding 0, margin -1px, overflow hidden, clip rect(0,0,0,0), white-space nowrap, border 0
  .sr-only-focusable: same as sr-only + .sr-only:focus-within reset to default position
aria-required and aria-invalid:
  [aria-invalid='true'] border-color var(--error)
  [aria-disabled='true'] pointer-events none, opacity 0.5
  [aria-expanded='true'] + submenu display block
skip link:
  position absolute, top -1000px, left 0, z-index 1000
  &:focus top 0, bg var(--surface), color var(--text), padding 0.5rem 1rem, outline 2px solid var(--focus)
CSS custom properties root
--font-sans: 'Inter', system-ui, -apple-system, sans-serif
--font-mono: 'JetBrains Mono', 'Fira Code', monospace
--color-surface #ffffff
--color-surface-alt #f8f9fa
--color-surface-muted #e9ecef
--color-text #1f2937
--color-text-secondary #6b7280
--color-text-muted #9ca3af
--color-border #d1d5db
--color-border-hover #9ca3af
--color-primary #2563eb
--color-primary-hover #1d4ed8
--color-primary-alpha rgba(37,99,235,0.1)
--color-secondary #64748b
--color-error #dc2626
--color-error-alpha rgba(220,38,38,0.15)
--color-success #16a34a
--color-warning #d97706
--color-focus #3b82f6
--color-overlay rgba(0,0,0,0.5)
--radius-sm 4px
--radius-md 8px
--radius-lg 12px
--radius-xl 16px
--radius-full 9999px
--shadow-sm 0 1px 2px rgba(0,0,0,0.05)
--shadow-md 0 4px 6px -1px rgba(0,0,0,0.1)
--shadow-lg 0 10px 15px -3px rgba(0,0,0,0.1)
--shadow-xl 0 20px 25px -5px rgba(0,0,0,0.1)
--z-navbar 100
--z-sidebar 200
--z-overlay 300
--z-modal 400
--z-dropdown 500
--z-toast 600
--z-tooltip 700
--max-width-sm 640px
--max-width-md 768px
--max-width-lg 1024px
--max-width-xl 1280px
--max-width-2xl 1536px
--focus-ring: 0 0 0 3px var(--color-focus-alpha)
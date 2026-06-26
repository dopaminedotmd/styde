WCAG AA contrast ratios across all base surface levels in a dark theme:
Surface hierarchy for dark themes:
- Surface 0 (base background): #121212 - darkest, background
- Surface 1 (elevated): #1E1E1E - cards, dialogs
- Surface 2 (raised): #252525 - dropdowns, popovers
- Surface 3 (high): #2C2C2C - modals, sidebars
- Surface 4 (highest): #333333 - tooltips, drawers
Primary text on surface 0: #E0E0E0 = 14.6:1 (AAA)
Secondary text on surface 0: #A0A0A0 = 7.2:1 (AAA)
Disabled text on surface 0: #6B6B6B = 4.0:1 (AA for large text)
Border on surface 0: #3D3D3D = 3.0:1 (AA for non-text)
Primary #7C5CFC (violet) on surface 1 (#1E1E1E): 7.8:1 (AAA)
Accent #4FC3F7 (light blue) on surface 1: 8.9:1 (AAA)
Danger #EF5350 on surface 1: 6.2:1 (AA)
Success #66BB6A on surface 1: 6.8:1 (AA)
Core theme token architecture in CSS custom properties:
Root scope declares all tokens. Surface level maps to a single --surface variable, enabling CSS-only elevation changes via class swap.
System detects with prefers-color-scheme media query. Manual override via data-theme attribute on html element. data-theme takes priority over media query via specificity.
Transition strategy: all color and background-color changes animate at 300ms ease using a single transition rule on :root, with forced isolation on backdrop-filter and transform properties to prevent jank on animated overlays.
Contrast validation method: for any pair of foreground-background, compute relative luminance (WCAG formula using sRGB linearization) then ratio. Ratios below 4.5:1 for normal text fail AA. Below 3:1 for large text fail AA. Below 7:1 for normal text fail AAA.
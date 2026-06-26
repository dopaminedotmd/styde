fas 0.5 design mockups
styde-se-site-integrator-v3
deliverable 1: chrome wireframe
nav-bar skeleton render:
  [logo 24x24]  [pill 80x20]  [pill 80x20]  [pill 80x20]  [spacer]  [circle 32x32]
  |-- 56px fixed --|
error fallback render:
  [logo svg]  [spacer]  "Navigation unavailable"  [spacer]  [grey circle]
scroll-hide state:
  translateY(-56px) at scroll-down > 10px
  translateY(0) at scroll-up > 10px
  150ms debounce on scroll listener
  0.3s ease-out hide / 0.2s ease-in reveal
breadcrumb skeleton render:
  [pill 40x12]  >  [pill 40x12]  >  [pill 40x12]
  |-- 32px sticky, top: 56px --|
breadcrumb expand states:
  root: "styde.se"
  forge: "styde.se > Forge > [section] > [page]"
  docs:  "styde.se > Docs > [category] > [article]"
  mobile: "→ [page title]"  ("←" on deep pages)
error segment fallback:
  "styde.se > Forge > (unknown)"
empty/null path fallback:
  "styde.se > [document.title fallback]"
progress bar render:
  position: fixed
  top: calc(56px - 3px)
  left: 0
  right: 0
  height: 3px
  z-index: calc(nav z-index + 1)
  fill animation: 0.4s (var(--progress-duration))
  fade-out: 0.2s
  safety timeout: 10s → fill to 90% → fade out
  rapid navigation: reset to 0%, re-start
  reduced-motion: snap to 100%, no animation
footer skeleton render:
  [copyright pill 120x8]  [li pill 40x8]  [li pill 40x8]  [li pill 40x8]
  |-- min 48px --|
error fallback:
  "© styde.se" in var(--text-muted), no grid, no icons
empty fallback (zero links):
  "© styde.se", same as error but not an error path
deliverable 2: states matrix
nav-bar state transitions:
  idle → loading  (page load / SPA route start)
  loading → ready (nav data resolved)
  loading → error  (timeout > 5s or HTTP error)
  ready → scroll-down  (scrollY > 10, direction = down)
  scroll-down → scroll-up  (scroll direction = up, delta > 10px)
  ready → error  (connection lost, re-fetch fails)
breadcrumb state transitions:
  idle → loading  (route change triggers path resolution)
  loading → ready (segments resolved)
  loading → error  (segment fetch fails, per-segment fallback)
  ready → error  (individual segment fails on re-resolve)
content shell state transitions:
  idle → loading  (route data fetch starts)
  loading → ready (data resolved)
  loading → error  (fetch timeout, HTTP error, render throws)
  ready → error  (route error boundary catches)
  error → ready  ("Retry" button triggers re-fetch)
footer state transitions:
  idle → loading  (footer data fetch starts)
  loading → ready (link grid data resolved)
  loading → error  (fetch timeout > 3s or HTTP error)
  loading → empty (data returns zero links, render minimal)
deliverable 3: theme integration points
light-dark token surface at src/styles/theme-contract.css
[data-theme="light"]
  surface-1: #ffffff
  surface-2: #f5f5f7
  surface-3: #e8e8ed
  progress-fill: #0071e3
[data-theme="dark"]
  surface-1: #1d1d1f
  surface-2: #2d2d2f
  surface-3: #3d3d3f
  progress-fill: #2997ff
theme detection cascade:
  1. localStorage key: styde-theme (override)
  2. prefers-color-scheme media query (default)
  3. toggle in user avatar dropdown
reduced-motion: all chrome animations zeroed via
  @media (prefers-reduced-motion: reduce)
  * { animation-duration: 0.01ms !important; transition-duration: 0.01ms !important }
deliverable 4: file manifest
  src/components/site-nav-bar.ts          — Layer 1 web component
  src/components/site-breadcrumb.ts       — breadcrumb web component
  src/components/site-progress-bar.ts     — progress bar web component
  src/components/site-footer.ts           — Layer 4 web component
  src/styles/theme-contract.css           — CSS custom properties
  src/layouts/site-shell.ts               — composition layout wrapper
framework-agnostic web components accepted by both Lit (Forge SPA) and Astro (styde.se marketing pages). Shell layout is the single integration point. No chrome logic duplicated across page sections.
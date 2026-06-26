Fas 0.5 — Design specification
BLUEPRINT:
Styde Se Site Integrator
Domain: frontend Version: 3
Purpose
Design how the Forge web dashboard integrates into the larger styde.se site. Navigation bar, breadcrumb trail, site chrome, visual continuity between Forge and rest of styde.se. Deliverables are a design specification, interaction blueprint, and theme contract — no mockup images.
Persona
You are a site integration designer. Forge is part of styde.se, not a standalone island. Design navigation continuity, shared chrome, visual language that bridges Forge and parent site. Seamless integration.
Skills
  frontend-design
  high-end-visual-design
  minimalist-ui
Framework Rationale
Three frameworks share the styde.se surface; each is selected for its specific role:
Lit (3.2+)
  Chosen for all site-chrome web components (nav-bar, breadcrumb, progress-bar, footer, shell layout). Lit produces standard Custom Elements with zero framework overhead (~5 KB gzipped). It renders via native DOM — no virtual DOM diffing needed for chrome that changes state only on scroll, route, or auth events. Works identically inside Astro pages (SSR) and the Forge SPA (client-side) because both consume the same registered custom elements.
Astro (4.x)
  Chosen for styde.se marketing pages (landing, blog, docs, pricing, community) because it ships zero JavaScript by default. Pages are static HTML with islands of interactivity. Forge chrome components hydrate only where they appear. Astro's content collections power the blog and docs with Markdown/MDX authoring. No SSR framework overhead on pages that don't need it.
Vitest (2.x)
  Chosen for unit and integration tests. Native ESM support means no transpilation step for Lit components. Runs in Node via happy-dom (lightweight DOM without a browser) for component tests, and in jsdom for tests that need full CSSOM. Parallel worker threads by default — critical for a suite that tests all four state dimensions (loading, error, empty, scroll) across all four chrome layers (16 state combinations as a baseline).
Playwright (1.50+)
  Chosen for visual regression and cross-browser E2E tests. Tests the actual custom elements in Chromium, Firefox, and WebKit. Visual snapshots catch theme-contract regressions in both light and dark mode. Scroll-behaviour tests verify nav bar hide/reveal, breadcrumb stickiness, and progress-bar animation timing across viewport sizes.
Integration strategy: Lit components are framework-agnostic Custom Elements registered once in an entry module. Astro pages import and render them as HTML tags. The Forge SPA (Lit-based dashboard) imports the same entry module. Vitest tests components by importing them into a test DOM. Playwright tests the real rendered output. No cross-framework adapter or bridge layer is needed because Custom Elements are the shared contract.
Chrome Layer Architecture
The site chrome is divided into four logical layers, each with distinct responsibilities and state behaviour. All layers inherit the theme contract defined in the Theme Contract section below. Per-state behaviour for all layers is consolidated in the State Matrix section — component specifications below reference their matrix row rather than repeating state prose.
Layer 1: Top Navigation Bar
Fixed top bar (h=56px) containing:
  Site logo (links to styde.se root)
  Primary nav links (max 5): Forge, Docs, Community, Pricing, Blog
  User avatar + dropdown (logged in) or Sign In / Get Started buttons (anonymous)
  Top-loading progress bar at lower edge — see Progress Bar specification
States: see State Matrix Layer 1 row.
Layer 2: Breadcrumb Trail
See Breadcrumb specification for all variants. Layer 2 sits directly below the top nav bar, h=32px, background var(--surface-2). Renders a collapsing trail of site sections: styde.se > Forge > [current page]. On pages from other sections (Docs, Community) the breadcrumb reflects the full styde.se hierarchy, not just the Forge subtree.
States: see State Matrix Layer 2 row.
Layer 3: Main Content Shell
Flexible container (min-height calc(100vh - 56px - 32px - footer)) that holds page-specific content. No chrome of its own beyond the left sidebar when present (Forge-specific secondary nav).
States: see State Matrix Layer 3 row.
Layer 4: Footer
Site-wide footer (h=auto, min 48px). Contains copyright, link grid (About, Contact, Privacy, Terms, Status), social icons, and a "Back to top" link.
States: see State Matrix Layer 4 row.
Breadcrumb Specification
A single collapsing breadcrumb component used across all styde.se pages. Variants:
  Root: Shows only "styde.se" when at site root
  Forge pages: styde.se > Forge > [section] > [page] — section links to Forge Dashboard, page links to specific tool
  Documentation pages: styde.se > Docs > [category] > [article]
  Community pages: styde.se > Community > [thread|category]
  Mobile (<640px): Last two segments only as "..." > [page title]. No broken segments.
Implementation: Lit web component at src/components/site-breadcrumb.ts with a path attribute accepting {label, href}[]. Fires breadcrumb:select CustomEvent on click.
State behaviour: see State Matrix Layer 2 row.
Theme Contract
Light/Dark Token Mappings
All chrome layers reference CSS custom properties. No hardcoded colour values anywhere in component styles:
:root, [data-theme="light"] {
  --surface-1: #ffffff;
  --surface-2: #f5f5f7;
  --surface-3: #e8e8ed;
  --text-primary: #1d1d1f;
  --text-secondary: #6e6e73;
  --text-muted: #aeaeb2;
  --accent: #0071e3;
  --accent-hover: #0077ed;
  --border: #d2d2d7;
  --shadow: rgba(0,0,0,0.08);
  --progress-track: #e8e8ed;
  --progress-fill: #0071e3;
}
[data-theme="dark"] {
  --surface-1: #1d1d1f;
  --surface-2: #2d2d2f;
  --surface-3: #3d3d3f;
  --text-primary: #f5f5f7;
  --text-secondary: #a1a1a6;
  --text-muted: #6e6e73;
  --accent: #2997ff;
  --accent-hover: #40a9ff;
  --border: #424245;
  --shadow: rgba(0,0,0,0.4);
  --progress-track: #424245;
  --progress-fill: #2997ff;
}
Theme is toggled by a <select> in the user avatar dropdown, stored in localStorage key styde-theme. System preference (prefers-color-scheme) is the default. On first visit with no stored preference, the theme matches system preference.
Reduced Motion
All chrome layer animations (nav hide/reveal, breadcrumb expand/collapse, progress bar fill, scroll-triggered transitions) must respect prefers-reduced-motion:
@media (prefers-reduced-motion: reduce) {
  *,
  *::before,
  *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
  }
  .nav-bar,
  .breadcrumb,
  .progress-bar {
    transition: none !important;
  }
}
When reduced motion is active, the top-loading progress bar snaps to 100% on route change (no animation). The nav bar appears/disappears instantly with zero transition on scroll.
State Matrix
Layer 1 — Top Navigation Bar
  Loading:
    56px skeleton bar. Three 80px-wide pill placeholders for nav links. One 32px circle placeholder for user avatar. Logo renders as grey rounded rectangle (120x28px). No interactive elements.
  Error:
    Logo renders as static SVG. Nav link area shows "Navigation unavailable" in var(--text-muted). User area shows a grey circle (no avatar). No dropdown opens. A nav:degraded CustomEvent fires on document for downstream logging.
  Empty:
    Not applicable — the site always has minimum nav links. If the nav-link data source returns zero items, inject five defaults from a static fallback array: Forge, Docs, Community, Pricing, Blog. The Sign In / Get Started buttons always render with no data dependency.
  Scroll edge (top):
    Bar is fully opaque with box-shadow. Logo at full opacity. Scroll-up listener debounced at 150ms to prevent flickering. At scroll position 0 the bar is always visible.
  Scroll edge (down past 10px):
    Bar transitions to translateY(-56px) with 0.3s ease-out. On scroll-up > 10px, slides back in with 0.2s ease-in.
Layer 2 — Breadcrumb Trail
  Loading:
    32px bar. Three 40px-wide pill skeletons separated by ">" glyph placeholders. No text readout until all segments resolve.
  Error:
    If data fetch fails (HTTP error or timeout > 3s), render fallback: styde.se > Forge > [page slug from URL]. If a specific segment throws, that segment becomes "(unknown)" in var(--text-muted) but adjacent links remain clickable.
  Empty:
    If path array is null or empty, render a single flat breadcrumb: styde.se > [document.title fallback]. No broken or missing segments.
  Scroll edge:
    Breadcrumb bar is sticky below the top nav. Remains fixed at top: 56px until the page scrolls past its own height, then scrolls with the page. Background darkens to var(--surface-1) with 0.6 opacity after 100px of scroll to ensure text contrast against page content scrolling beneath.
Layer 3 — Main Content Shell
  Loading:
    Full-viewport centered spinner (SVG ring, 48px diameter, var(--accent)) overlaying blank surface. With prefers-reduced-motion, fades in/out instead of spinning.
  Error:
    Centered error card: inline icon, error message from route error boundary, "Retry" button that re-fetches the route's data. Styled with var(--surface-2) background and var(--border) rounded corners.
  Empty:
    Shell renders with preserved left sidebar (when applicable) and footer. Content area shows inline SVG illustration ("Nothing here yet") with CTA linking to Forge getting-started page.
  Scroll edge:
    No chrome-specific scroll behaviour. Min-height accounts for sticky footer so content never occludes footer text.
Layer 4 — Footer
  Loading:
    48px skeleton strip. Two rows: copyright pill placeholder, then three link pill placeholders. No visible border until ready.
  Error:
    Minimal fallback: single line "© styde.se" in var(--text-muted). No link grid, no social icons. "Back to top" link uses a static scroll-to-top JS call — no data dependency.
  Empty:
    If link grid returns zero items, same as error path: copyright line only. This is not an error — zero links from a data source routes to minimal render, not error UI.
  Scroll edge:
    Footer is always at document bottom. Sticky via flexbox spacer in main shell layout (min-height 100vh with flex-grow on content). No scroll-triggered transformations on the footer itself.
Progress Bar Specification
A top-loading progress bar sits at the lower edge of the top navigation bar (Layer 1).
  Position: Fixed at top: calc(56px - 3px), left: 0, right: 0, z-index: calc(nav z-index + 1)
  Height: 3px
  Track colour: var(--progress-track)
  Fill colour: var(--progress-fill)
  Duration token: --progress-duration: 0.4s for fill animation, 0.2s for fade-out
  Trigger conditions:
    Fires on every route navigation (SPA route change or full page load)
    Activated by progress:start CustomEvent on document, completed by progress:complete
    Forge dashboard and all styde.se pages emit these events from their router middleware
    Safety timeout: if progress:complete not received within 10 seconds, bar fills to 90% and fades out
    Reduced motion: bar snaps to 100% instantly with no animation
    Nested navigation: a second progress:start while bar is animating resets to 0% and re-starts (no ghost bars)
  Implementation: Lit web component at src/components/site-progress-bar.ts
Deferred To: The 90% fill on safety timeout is intentional — 100% implies the navigation completed and users should navigate; capping at 90% signals the page may still be loading. Revisit the cap if metrics show user confusion between safety-timeout fills and real completions.
Implementation Summary
Six files:
  (1) src/components/site-nav-bar.ts
    Top navigation bar Lit web component. Layer 1 chrome. Skeleton loading, error fallback, scroll-hide/show behaviour. Imports theme tokens from theme-contract.css.
  (2) src/components/site-breadcrumb.ts
    Single breadcrumb Lit web component. Collapsing segments, error-segment fallback, empty-path handling. path attribute accepts {label, href}[]. Fires breadcrumb:select.
  (3) src/components/site-progress-bar.ts
    Top-loading progress bar Lit web component. Route-event triggers (progress:start / progress:complete), 10s safety timeout, nested-navigation reset, reduced-motion snap.
  (4) src/components/site-footer.ts
    Footer Lit web component. Two render modes: full (copyright, link grid, social icons, back-to-top) and minimal (copyright-only for error/empty states). Back-to-top uses static scroll-to-top — no data dependency.
  (5) src/styles/theme-contract.css
    CSS custom properties file. Light and dark token maps, prefers-reduced-motion overrides. Consumed by all six components via @import. No hardcoded colours.
  (6) src/layouts/site-shell.ts
    Layout wrapper Lit web component. Composes nav-bar, breadcrumb, <slot> for main content, and footer. Wires scroll listener for nav-bar hide/reveal and breadcrumb stickiness. Listens for progress:start/progress:complete on document and passes events to progress-bar. Single integration point: accepts content via slot, works identically in Astro pages and Forge SPA because it is a standard Custom Element.
---
persona.md additions (append to existing persona.md):
constraint: All deliverables must be named by their actual format (not aspirational format). No section may repeat information already covered elsewhere — consolidate by reference. Any acknowledged gap in a design section must be followed by either a concrete mitigation or an explicit 'Deferred To: ' pointer. Strip bare 'TODO' statements without a resolution path.
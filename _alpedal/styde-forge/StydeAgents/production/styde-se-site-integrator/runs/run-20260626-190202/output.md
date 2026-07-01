Styde Se Site Integrator
Domain: frontend
Version: 4
Purpose
Design how the Forge web dashboard integrates into the larger styde.se site. Navigation bar, breadcrumb trail, site chrome, visual continuity between Forge and rest of styde.se. Seamless integration.
Persona
You are a site integration designer. Forge is part of styde.se, not a standalone island. Design navigation continuity, shared chrome, visual language that bridges Forge and parent site. Seamless integration.
Skills
  frontend-design
  high-end-visual-design
  minimalist-ui
Architecture
Framework Rationale
Four frameworks are used, chosen for their specific role in the integration chain:
Lit: Web components for all chrome layers (nav, breadcrumb, footer, progress bar). Chosen over React/Vue because chrome components must be framework-agnostic — Lit produces native custom elements consumable by both the Forge SPA (Lit-based) and the Astro-rendered marketing pages without wrapping. Bundle size under 6 KB gzipped, no virtual DOM overhead for simple presentational chrome.
Astro: Static site generation for styde.se marketing pages (docs, community, blog, pricing). Zero JS by default means marketing pages load fast without shipping the chrome components JS until hydration. The `.astro` island pattern lets us drop Lit web components directly into static templates with partial hydration.
Vitest: Unit testing for chrome components. Chosen over Jest for native ESM support, faster watch mode, and direct compatibility with Lit's native module ecosystem. Tests run in parallel across all six chrome components.
Playwright: Integration testing for the chrome shell across styde.se pages. Chromium, Firefox, WebKit coverage for scroll-behaviour, theme toggle persistence, breadcrumb collapsing, and progress-bar lifecycle. Parallel test sharding across 3 browsers.
Integration contract: Lit components ship as standalone custom elements under src/components/. Astro pages import them via a thin loader script. The Forge SPA imports the same elements through its own entry point. No framework bridge or wrapper layer needed — the browser custom element registry is the integration boundary.
State Matrix
Single shared definition of state behaviour for all chrome layers. Each layer references its row below by Layer number. No per-layer state repetition in component descriptions.
States defined per layer:
Layer 1 — Top Navigation Bar (h=56px, fixed)
  Loading: 56px skeleton bar. Three 80px-wide pill placeholders for nav links. One 32px circle placeholder for user avatar. Logo rendered as grey rounded rectangle. No interactive elements until ready.
  Error: Logo renders as static SVG. Nav link area shows "Navigation unavailable" in var(--text-muted). User area shows grey circle (no avatar). Clicking any placeholder fires nav:degraded event on document for downstream analytics. No dropdown opens.
  Empty: Not a valid state — site always has top-level nav links (minimum: Forge, Blog, Sign In). If nav-link data source returns zero items, inject five defaults from static fallback array: Forge, Docs, Community, Pricing, Blog.
  Scroll edge (top): Bar fully opaque with box-shadow. Logo at full opacity. Scroll-up listener debounced at 150ms.
  Scroll edge (down): Bar transitions translateY(-56px) with 0.3s ease-out. On scroll-up > 10px, slides back in with 0.2s ease-in. At scroll position 0, bar always visible regardless of last scroll direction.
Layer 2 — Breadcrumb Trail (h=32px, sticky below nav)
  Loading: 32px bar with three 40px-wide pill skeletons separated by ">" glyph placeholders. No text until segments resolved.
  Error: If breadcrumb data fetch fails (HTTP error or timeout > 3s), render fallback trail "styde.se > Forge > [page slug from URL]". If specific segment resolution throws, that segment renders as "(unknown)" in var(--text-muted) but adjacent links remain clickable.
  Empty: Page with empty or null path array renders single flat breadcrumb: "styde.se > [document.title fallback]". No broken or missing segments.
  Scroll edge: Bar sticky at top: 56px. On scroll past bar height, scrolls with page. Background darkens to var(--surface-1) with 0.6 opacity after 100px scroll for contrast against page content beneath.
Layer 3 — Main Content Shell (flex container, min-height: calc(100vh - 56px - 32px - footer))
  Loading: Full-viewport centered spinner — SVG ring, 48px diameter, var(--accent). Overlays blank white/grey surface. Respects reduced-motion (fade in/out instead of spin).
  Error: Centred error card with inline icon, error message from route error boundary, and "Retry" button that re-fetches route data. Card uses var(--surface-2) background, var(--border) rounded corners.
  Empty: Not an error. Shell renders with no content but preserves left sidebar (when applicable) and footer. Content area shows subtle "Nothing here yet" inline SVG illustration with CTA linking to Forge getting-started page.
  Scroll edge: No chrome-specific scroll behaviour. Shell min-height accounts for sticky footer so content never occludes footer text.
Layer 4 — Footer (h=auto, min 48px, document-bottom)
  Loading: 48px skeleton strip with two rows of pill placeholders (copyright line, three link placeholders). No visible border until ready.
  Error: If footer data fetch fails, render minimal fallback: single line "styde.se" in var(--text-muted). No link grid, no social icons. "Back to top" link uses static scroll-to-top JavaScript call (no data dependency).
  Empty: If footer data source returns empty link grid or zero items, render minimal fallback: copyright line only. Not an error. Data source returning zero links does not trigger error path.
  Scroll edge: Always at document bottom. Sticky via flexbox spacer in main shell layout (min-height: 100vh with flex-grow on content). No scroll-triggered transformations on footer itself.
Chrome Layer Architecture
The site chrome divides into four logical layers. Each layer inherits the theme contract (see Theme Contract section below) and references its state behaviour from the State Matrix row above.
Layer 1: Top Navigation Bar
Fixed top bar (h=56px) containing:
- Site logo (links to styde.se root)
- Primary nav links (max 5): Forge, Docs, Community, Pricing, Blog
- User avatar + dropdown (logged in) or Sign In / Get Started buttons (anonymous)
- Top-loading progress bar at lower edge (see Progress Bar specification below)
State: See State Matrix Layer 1.
Layer 2: Breadcrumb Trail
See Breadcrumb Specification below for all variants. Sits directly below top nav bar, h=32px, background var(--surface-2). Renders collapsing trail of site sections: styde.se > Forge > [current page]. On pages from other sections (Docs, Community) reflects full styde.se hierarchy, not just Forge subtree.
State: See State Matrix Layer 2.
Layer 3: Main Content Shell
Flexible container (min-height: calc(100vh - 56px - 32px - footer)) holding page-specific content. No chrome of its own beyond left sidebar when present (Forge-specific secondary nav).
State: See State Matrix Layer 3.
Layer 4: Footer
Site-wide footer (h=auto, min 48px). Contains copyright, link grid (About, Contact, Privacy, Terms, Status), social icons, and "Back to top" link.
State: See State Matrix Layer 4.
Breadcrumb Specification
Single collapsing breadcrumb component used across all styde.se pages.
Variants:
  Root: Shows only "styde.se" when at site root (non-Forge pages like landing)
  Forge pages: styde.se > Forge > [section] > [page] — section links to Forge Dashboard, page links to specific tool
  Documentation pages: styde.se > Docs > [category] > [article]
  Community pages: styde.se > Community > [thread|category]
  Mobile (< 640px): Single visible segment — [page title]. No broken segments. Chevrons hidden, remaining segments accessible via tap-to-expand.
The breadcrumb component is its own custom element (<site-breadcrumb>) with a path attribute accepting an array of {label, href} objects. Fires breadcrumb:select CustomEvent on click.
Implementation: src/components/site-breadcrumb.ts — one file, one component, no duplication across page sections.
Known gap: On ultra-wide viewports (> 1920px), breadcrumb can feel too far from page content due to centering in a 32px bar. Deferred To: Future visual polish batch — add max-width: 1400px + auto-margin centering constraint to breadcrumb container in v5.
Progress Bar Specification
A top-loading progress bar at the lower edge of the top navigation bar (Layer 1).
  Position: Fixed at top: calc(56px - 3px), left: 0, right: 0, z-index: calc(nav z-index + 1)
  Height: 3px
  Track colour: var(--progress-track)
  Fill colour: var(--progress-fill)
  Duration token: --progress-duration: 0.4s for fill animation, 0.2s for fade-out
  Trigger conditions:
  - Fires on every route navigation (SPA route change or full page load)
  - Activated by progress:start CustomEvent on document, completed by progress:complete
  - Forge dashboard and all styde.se pages emit these events from their router middleware
  - If progress:complete not received within 10 seconds, bar fills to 90% and fades out (safety timeout)
  - On prefers-reduced-motion: reduce, bar snaps to 100% instantly with no animation
  - Nested navigation: if second progress:start fires while bar is animating, bar resets to 0% and re-starts (covers rapid navigations without ghost bars)
  Implementation: Dedicated <site-progress-bar> web component in src/components/site-progress-bar.ts
Known gap: Progress bar sits at z-index above nav but below modals/modals. Not explicitly coordinated with third-party overlays (cookie consent, intercom). Deferred To: z-index layering audit in Phase 2 — introduce a --z-chrome-layer variable family and adjust progress bar z-index against a documented stacking context.
Theme Contract
Light/Dark Token Mappings
All chrome layers reference CSS custom properties. No hardcoded colour values anywhere in component styles.
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
Theme toggle via data-theme attribute on <html> set by prefers-color-scheme media query reader or user preference stored in localStorage key styde-theme. System preference is default, overridable via toggle in user avatar dropdown.
Reduced Motion
All chrome layer animations (nav hide/reveal, breadcrumb expand/collapse, progress bar fill, scroll-triggered transitions) must respect prefers-reduced-motion:
@media (prefers-reduced-motion: reduce) {
  *, ::before, ::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
  }
  .nav-bar, .breadcrumb, .progress-bar {
    transition: none !important;
  }
}
When reduced motion is active: top-loading progress bar snaps to 100% on route change (no animation). Nav bar appears/disappears instantly with zero transition on scroll.
Scope Guardrails
  Framework rationale: max 2 sentences per major choice. Covers bundle size, SSR needs, test parallelism, and cross-framework integration. No deep-dive into esoteric framework internals.
  Persona constraints: Standard YAML array format under Skills in config.yaml. No free-form prose persona appendix. Persona section in this document is a prose description for design context — the machine-readable persona lives in persona.md with YAML fields: purpose, constraints, preferences.
  State descriptions: Referenced by layer number from State Matrix only. No inline state repetition in component descriptions.
Implementation Summary
Create six concrete files:
1. src/components/site-nav-bar.ts — Top navigation bar web component implementing Layer 1 chrome, skeleton loading, error fallback, and scroll-hide/show behaviour
2. src/components/site-breadcrumb.ts — Single breadcrumb web component with collapsing, error-segment, and empty-path handling
3. src/components/site-progress-bar.ts — Top-loading progress bar web component with route-event triggers and safety timeout
4. src/components/site-footer.ts — Footer web component with full and minimal (error/empty) render modes
5. src/styles/theme-contract.css — CSS custom properties file for light/dark tokens and reduced-motion overrides consumed by all components
6. src/layouts/site-shell.ts — Layout wrapper composing nav-bar, breadcrumb, main slot, and footer into full chrome stack. Handles scroll listeners, wires progress bar to router events. Single integration point between Forge-specific page content and broader styde.se chrome. Framework-agnostic web component accepted by both Forge SPA (Lit) and styde.se marketing pages (Astro).
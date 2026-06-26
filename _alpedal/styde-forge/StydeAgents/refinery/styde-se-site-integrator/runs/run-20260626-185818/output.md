Styde Se Site Integrator
Domain: frontend
Version: 3
Purpose
Design how the Forge web dashboard integrates into the larger styde.se site. Navigation continuity, shared chrome, visual language bridging Forge and parent site. Seamless integration.
Persona
Site integration designer. Forge is part of styde.se, not a standalone island.
Skills
frontend-design
high-end-visual-design
minimalist-ui
Chrome Layer Architecture
Four logical layers. All layers inherit the theme contract defined below.
Layer 1: Top Navigation Bar
Fixed top bar h=56px containing:
  Site logo linking to styde.se root
  Primary nav links max 5: Forge, Docs, Community, Pricing, Blog
  User avatar plus dropdown logged in, or Sign In / Get Started buttons anonymous
  Top-loading progress bar at lower edge per Progress Bar specification
Loading state: 56px skeleton bar with three 80px-wide pill placeholders for nav links, 32px circle placeholder for avatar, logo rendered as grey rounded rectangle. No interactive elements.
Error state: Logo renders as static SVG. Nav link area shows Navigation unavailable in var(--text-muted). User area shows grey circle no avatar. Clicking any placeholder fires nav:degraded event on document for analytics.
Empty state: Not applicable. Nav links always have defaults. If nav-link data source returns zero items, inject five defaults from static fallback: Forge, Docs, Community, Pricing, Blog.
Scroll edge top: Bar fully opaque with box-shadow. Logo full opacity. Scroll-up listener debounced 150ms.
Scroll edge down: Bar transitions translateY(-56px) with 0.3s ease-out. On scroll-up greater than 10px slides back in with 0.2s ease-in. At scroll position 0 bar always visible.
Layer 2: Breadcrumb Trail
See Breadcrumb Specification below. Sits directly below top nav bar, h=32px, background var(--surface-2). Collapsing trail: styde.se > Forge > current page. On non-Forge pages reflects full styde.se hierarchy.
Loading: 32px bar with three 40px-wide pill skeletons separated by greater-than glyph placeholders. No text readout until segments resolved.
Error: If breadcrumb data fetch fails HTTP error or timeout greater than 3s render fallback styde.se > Forge > page-slug-from-URL. If resolving a specific segment throws that segment becomes unknown in var(--text-muted). Adjacent links remain clickable.
Empty: Page with empty or null path array renders single flat breadcrumb: styde.se > document.title fallback. No broken segments.
Scroll edge: Breadcrumb bar sticky below top nav. Remains fixed at top 56px until page scrolls past its own height then scrolls with page. Background darkens to var(--surface-1) with 0.6 opacity after 100px scroll.
Layer 3: Main Content Shell
Flexible container min-height calc(100vh - 56px - 32px - footer). Holds page-specific content. No own chrome beyond left sidebar when present Forge-specific secondary nav.
Loading: Full-viewport centered spinner SVG ring 48px diameter var(--accent) overlaying blank surface. Spinner inherits theme contract. Reduced-motion fades in and out instead of spinning.
Error: Centered error card with inline icon, error message from route error boundary, Retry button re-fetches route data. Card uses var(--surface-2) and var(--border) rounded corners.
Empty: Not an errored state. Shell renders no content but preserves left sidebar when applicable and footer. Content area shows Nothing here yet inline SVG illustration with CTA linking to Forge getting-started page.
Scroll edge: No chrome-specific scroll behaviour. Shell scrolling is inherent to page content. Min-height accounts for sticky footer.
Layer 4: Footer
Site-wide footer h=auto min 48px. Contains copyright, link grid About Contact Privacy Terms Status, social icons, Back to top link.
Loading: 48px skeleton strip with two rows of pill placeholders copyright line and three link placeholders. No visible border.
Error: If footer data fetch fails render minimal fallback: single copyright line copyright styde.se in var(--text-muted). No link grid, no social icons. Back to top link uses static scroll-to-top JavaScript call no data dependency.
Empty: If footer data source returns empty link grid or zero items render minimal fallback copyright line only. Not an error.
Scroll edge: Footer always at document bottom. Sticky via flexbox spacer in main shell layout min-height 100vh with flex-grow on content. No scroll-triggered transformations.
Breadcrumb Specification
Single collapsing breadcrumb component used across all styde.se pages. Implementation in src/components/site-breadcrumb.ts. One file, one component, no duplication across page sections. Web component with path attribute accepting array of label href objects. Fires breadcrumb:select CustomEvent on click.
Root: Shows only styde.se when at site root non-Forge pages like root landing.
Forge pages: styde.se > Forge > section > page. Section links to Forge Dashboard. Page links to specific tool.
Documentation pages: styde.se > Docs > category > article.
Community pages: styde.se > Community > thread or category.
Mobile viewport under 640px: Collapses to top two segments only. Remaining depth shown via expandable chevron dropdown. Root-only pages show just [page title]. No broken segments.
Theme Contract
CSS custom properties. No hardcoded colour values anywhere in component styles.
:root data-theme light:
  surface-1: #ffffff
  surface-2: #f5f5f7
  surface-3: #e8e8ed
  text-primary: #1d1d1f
  text-secondary: #6e6e73
  text-muted: #aeaeb2
  accent: #0071e3
  accent-hover: #0077ed
  border: #d2d2d7
  shadow: rgba(0,0,0,0.08)
  progress-track: #e8e8ed
  progress-fill: #0071e3
data-theme dark:
  surface-1: #1d1d1f
  surface-2: #2d2d2f
  surface-3: #3d3d3f
  text-primary: #f5f5f7
  text-secondary: #a1a1a6
  text-muted: #6e6e73
  accent: #2997ff
  accent-hover: #40a9ff
  border: #424245
  shadow: rgba(0,0,0,0.4)
  progress-track: #424245
  progress-fill: #2997ff
Theme toggled by prefers-color-scheme media query reader or user preference stored in localStorage key styde-theme. System preference is default. Overridable via toggle in user avatar dropdown.
Reduced Motion
All chrome layer animations nav hide and reveal, breadcrumb expand and collapse, progress bar fill, scroll-triggered transitions must respect prefers-reduced-motion:
@media prefers-reduced-motion reduce {
  *, ::before, ::after {
    animation-duration: 0.01ms important
    animation-iteration-count: 1 important
    transition-duration: 0.01ms important
  }
  .nav-bar, .breadcrumb, .progress-bar {
    transition: none important
  }
}
When reduced motion active: top-loading progress bar snaps to 100% on route change no animation. Nav bar appears and disappears instantly zero transition on scroll.
Progress Bar Specification
Top-loading progress bar at lower edge of top navigation bar Layer 1. Implementation in src/components/site-progress-bar.ts. Web component.
Position: Fixed at top calc(56px - 3px), left 0, right 0, z-index calc(nav z-index plus 1)
Height: 3px
Track color: var(--progress-track)
Fill color: var(--progress-fill)
Duration token: --progress-duration 0.4s for fill animation, 0.2s for fade-out
Trigger conditions:
  Fires on every route navigation SPA route change or full page load
  Activated by progress:start CustomEvent on document
  Completed by progress:complete CustomEvent on document
  Forge dashboard and all styde.se pages emit these events from router middleware
  If progress:complete not received within 10 seconds bar fills to 90% and fades out safety timeout
  On prefers-reduced-motion reduce bar snaps to 100% instantly
  Nested navigation: if second progress:start fires while bar still animating bar resets to 0% and re-starts
Test Strategy
Acceptance criteria format: Given-When-Then for each state transition per layer. Example: Given breadcrumb is in error state, When user clicks any resolved link, Then navigation proceeds normally and unresolved segment shows unknown.
Test levels:
  Unit: Each web component tested in isolation. All state transitions per State Matrix covered. DOM assertions for skeleton, error, empty, and nominal renders. Target 95% line coverage minimum.
  Integration: Chrome layers tested together in site-shell layout. Scroll hide/reveal timing. Breadcrumb collapsing at 640px breakpoint. Theme toggle persistence. Progress bar nested navigation reset. Target 90% line coverage minimum.
  E2E: Full styde.se navigation flow. Theme toggle across page reload. Scroll behaviour on long content pages. Route change with progress bar animation. Target 85% line coverage minimum.
Coverage thresholds: unit 95%, integration 90%, E2E 85%. All thresholds enforced in CI pipeline via Vitest and Playwright.
Dependency Graph
Internal preconditions:
  Components directory src/components/ exists and is writable.
  Build pipeline supports Lit-based web components and TypeScript.
  Router middleware emits progress:start and progress:complete CustomEvents.
  Astro and Lit projects both consume the same src/components/ and src/styles/ modules.
  Theme toggle reads localStorage key styde-theme and sets data-theme attribute on document.documentElement.
Service contracts:
  Breadcrumb component accepts Array of label: string, href: string. Returns nothing. Fires CustomEvent breadcrumb:select with detail: label, href, path.
  Progress bar accepts nothing. Listens for progress:start and progress:complete on document. Returns nothing.
  Nav bar accepts userMenuItems: Array optional for dropdown. Listens for scroll events on window. Returns nothing.
  Footer accepts footerLinks: Array optional, copyrightText: string optional. Returns nothing.
External preconditions:
  styde.se router emits progress events per contract.
  Astro pages import site-shell layout component.
  Forge SPA imports site-shell layout element.
  No external API dependencies for chrome layer data all fallbacks are static.
Data flow:
  Router emits progress:start > progress-bar listens and begins fill animation
  Router resolves route > route data fetched > breadcrumb path assembled from route metadata
  Router emits progress:complete > progress-bar completes fill and fades out
  Nav bar reads user session from window.__USER__ global (set by styde.se auth middleware)
  Footer receives link data from route metadata or falls back to static defaults
  Theme toggle reads localStorage on mount, writes to localStorage on change, sets data-theme attribute on document.documentElement
  All chrome components read CSS custom properties from theme-contract.css no direct colour references
Known Gaps and Confidence Ratings
| Gap | Impact | Confidence |
|-----|--------|------------|
| No mobile nav hamburger menu specified beyond breadcrumb collapse | Medium | 70% — top nav may overflow on small viewports; hamburger pattern needed |
| No loading states for user avatar dropdown content | Low | 85% — avatar data is synchronous from window.__USER__ but error boundary unspecified |
| No explicit z-index stacking strategy for modals/dialogs that overlay chrome | Medium | 75% — progress bar at nav z-index plus 1, but modal system could overlap breadcrumb |
| No RTL language support in breadcrumb or nav | Low | 90% — out of scope for V3 but should be flagged for V4 |
| No analytics/dataLayer integration specification | Low | 85% — nav:degraded event mentioned but no analytics pipeline defined |
Implementation Summary
Six concrete files:
src/components/site-nav-bar.ts — top navigation bar web component implementing Layer 1 chrome, skeleton loading, error fallback, scroll-hide/show behaviour.
src/components/site-breadcrumb.ts — single breadcrumb web component with collapsing, error-segment, empty-path handling. Accepts path array of label href objects. Fires breadcrumb:select CustomEvent.
src/components/site-progress-bar.ts — top-loading progress bar web component with route-event triggers, nested navigation reset, 10-second safety timeout. Listens for progress:start and progress:complete on document.
src/components/site-footer.ts — footer web component with full render mode link grid plus social icons and minimal fallback render mode for error and empty states.
src/styles/theme-contract.css — CSS custom properties file for light and dark tokens, reduced-motion overrides. Consumed by all components. No hardcoded colours in component styles.
src/layouts/site-shell.ts — layout wrapper composing nav-bar, breadcrumb, main slot, and footer into full chrome stack. Handles scroll listeners, wires progress bar to router events. Framework-agnostic web component accepted by Forge SPA Lit and styde.se marketing pages Astro.
Deliverable naming: all deliverables named by actual format. No aspirational labels. Mockup references corrected to design specification or interaction blueprint throughout. No section duplicates information covered elsewhere all cross-references consolidated by reference.
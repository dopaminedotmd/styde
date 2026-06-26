# Styde Se Site Integrator

**Domain:** frontend **Version:** 3

## Purpose

Design how the Forge web dashboard integrates into the larger styde.se site. Navigation bar, breadcrumb trail, site chrome, visual continuity between Forge and rest of styde.se.

## Persona

You are a site integration designer. Forge is part of styde.se, not a standalone island. Design navigation continuity, shared chrome, visual language that bridges Forge and parent site. Seamless integration.

## Skills

- frontend-design
- high-end-visual-design
- minimalist-ui

## Chrome Layer Architecture

The site chrome is divided into four logical layers, each with distinct responsibilities and state behaviour. All layers inherit the theme contract defined in the Theme Contract section below.

### Layer 1: Top Navigation Bar

Fixed top bar (h=56px) containing:

- Site logo (links to styde.se root)
- Primary nav links (max 5): Forge, Docs, Community, Pricing, Blog
- User avatar + dropdown (logged in) or Sign In / Get Started buttons (anonymous)
- Top-loading progress bar at lower edge — see Progress Bar specification

Breadcrumb trail is specified once in Breadcrumb specification below; variant descriptions refer back to that section rather than repeating the prose.

#### States (see State Matrix for full treatment)

| State | Behaviour |
|---|---|
| Loading | Skeleton bar (logo + 3 link placeholders) at full bar height |
| Error | Degraded: show logo + "Navigation unavailable" text, hide links |
| Empty | Not applicable (nav links always have defaults) |
| Scroll edge | On scroll-down the bar hides (re-appears on scroll-up); on scroll to top the bar is fully opaque |

### Layer 2: Breadcrumb Trail

See Breadcrumb specification for all variants. Layer 2 sits directly below the top nav bar, h=32px, background var(--surface-2). Renders a collapsing trail of site sections: styde.se > Forge > [current page]. On pages from other sections (Docs, Community) the breadcrumb reflects the full styde.se hierarchy, not just the Forge subtree.

### Layer 3: Main Content Shell

Flexible container (min-height calc(100vh - 56px - 32px - footer)) that holds page-specific content. No chrome of its own beyond the left sidebar when present (Forge-specific secondary nav).

### Layer 4: Footer

Site-wide footer (h=auto, min 48px). Contains copyright, link grid (About, Contact, Privacy, Terms, Status), social icons, and a "Back to top" link.

## Breadcrumb Specification

A single collapsing breadcrumb component used across all styde.se pages. Variants:

- **Root:** Shows only "styde.se" when at site root (non-Forge pages like root landing)
- **Forge pages:** `styde.se > Forge > [section] > [page]` — section links to Forge Dashboard, page links to specific tool
- **Documentation pages:** `styde.se > Docs > [category] > [article]`
- **Community pages:** `styde.se > Community > [thread|category]`
- **Mobile ( <768px ):** Collapses to show only the last two levels as text; all preceding levels fold into a "..." dropdown. The `...` icon is always the first visible breadcrumb element (replaces root) so the user can navigate up. When collapsed, the full trail is accessible via a single tap on the `...` expander.
- **Error state:** If a segment fails to resolve, replace that segment text with "(unknown)" in var(--text-muted) and keep parent/child links intact. Do not break the trail — a single failed segment should not collapse adjacent links.
- **Empty state:** A page with no hierarchy registers as a flat route — render only `styde.se > [page title]`. No broken segments.

The breadcrumb component is its own web component (`<styde-breadcrumb>`) with a `path` attribute accepting an array of `{label, href}` objects. It fires a `breadcrumb:select` CustomEvent on click.

Implementation resides in `src/components/site-breadcrumb.ts` — one file, one component, no duplication across page sections.

## Theme Contract

### Light/Dark Token Mappings

All chrome layers reference CSS custom properties. No hardcoded colour values anywhere in component styles:

```css
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
```

Theme is toggled by a `<meta name="color-scheme">` reader or user preference stored in localStorage key `styde-theme`. System preference (`prefers-color-scheme`) is the default, overridable via a toggle in the user avatar dropdown.

### Reduced Motion

All chrome layer animations (nav hide/reveal, breadcrumb expand/collapse, progress bar fill, scroll-triggered transitions) must respect `prefers-reduced-motion`:

```css
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
```

When reduced motion is active, the top-loading progress bar snaps to 100% on route change (no animation). The nav bar appears/disappears instantly with zero transition on scroll.

## State Matrix

### Layer 1 — Top Navigation Bar

- **Loading:** 56px skeleton bar with three 80px-wide pill placeholders for nav links, a 32px circle placeholder for the user avatar, and the logo rendered as a grey rounded rectangle. No interactive elements until ready.
- **Error:** Logo renders as static SVG. Nav link area shows "Navigation unavailable" in var(--text-muted). User area shows a grey circle (no avatar). Clicking any placeholder triggers a `nav:degraded` event on document for downstream analytics/logging. No dropdown opens.
- **Empty:** Not a valid state — the site always has top-level nav links (minimum: Forge, Blog, Sign In). If the nav-link data source returns zero items, inject five defaults from a static fallback array: Forge, Docs, Community, Pricing, Blog.
- **Scroll edge (top):** Bar is fully opaque with box-shadow. Logo is at full opacity. The scroll-up listener has debounced 150ms to avoid flickering.
- **Scroll edge (down):** Bar transitions to translateY(-56px) with 0.3s ease-out. On scroll-up > 10px, it slides back in with 0.2s ease-in. At scroll position 0, bar is always visible regardless of last scroll direction.

### Layer 2 — Breadcrumb Trail

- **Loading:** 32px bar with three 40px-wide pill skeletons separated by ">" glyph placeholders. No text readout until segments are resolved.
- **Error:** If breadcrumb data fetch fails (HTTP error or timeout > 3s), render fallback trail `styde.se > Forge > [page slug from URL]`. If resolving a specific segment throws, that segment becomes "(unknown)" in var(--text-muted) but adjacent links remain clickable.
- **Empty:** A page with an empty or null path array renders a single flat breadcrumb: `styde.se > [document.title fallback]`. No broken or missing segments.
- **Scroll edge:** The breadcrumb bar is sticky below the top nav. On scroll, it remains fixed at top: 56px until the page scrolls past its own height, then scrolls with the page. Its background darkens to var(--surface-1) with 0.6 opacity after 100px of scroll to ensure text contrast against page content scrolling beneath.

### Layer 3 — Main Content Shell

- **Loading:** Full-viewport centered spinner (SVG ring, 48px diameter, var(--accent)) overlaying a blank white/grey surface. The spinner inherits the theme contract and respects reduced-motion (fade in/out instead of spin).
- **Error:** Centred error card with inline icon, error message from route error boundary, and a "Retry" button that re-fetches the route's data. The card uses the default Chrome surface styling (var(--surface-2), var(--border) rounded corners).
- **Empty:** Not an errored state — the shell renders with no content but preserves the left sidebar (when applicable) and footer. The content area shows a subtle "Nothing here yet" illustration (inline SVG) with a CTA linking to Forge's getting-started page.
- **Scroll edge:** No chrome-specific scroll behaviour for the shell itself — scrolling is inherent to page content. The shell's min-height accounts for the sticky footer so content never occludes footer text.

### Layer 4 — Footer

- **Loading:** 48px skeleton strip with two rows of pill placeholders (copyright line, three link placeholders). No visible border until ready.
- **Error:** If footer data fetch fails, render a minimal fallback footer: single line of copyright text (`© styde.se`) in var(--text-muted). No link grid, no social icons. The "Back to top" link uses a static scroll-to-top JavaScript call (no data dependency).
- **Empty:** If the footer data source returns an empty link grid or zero items, render the minimal fallback: copyright line only. This is not an error — a data source that returns zero links should not trigger an error path.
- **Scroll edge:** Footer is always at document bottom. It becomes sticky via a flexbox spacer in the main shell layout (min-height 100vh with flex-grow on content). No scroll-triggered transformations on the footer itself.

## Progress Bar Specification

A top-loading progress bar sits at the lower edge of the top navigation bar (Layer 1).

- **Position:** Fixed at top: calc(56px - 3px), left: 0, right: 0, z-index: calc(nav z-index + 1)
- **Height:** 3px
- **Track colour:** var(--progress-track)
- **Fill colour:** var(--progress-fill)
- **Duration token:** --progress-duration: 0.4s for fill animation, 0.2s for fade-out
- **Trigger conditions:**
  - Fires on every route navigation (SPA route change or full page load)
  - Activated by a `progress:start` CustomEvent on `document`, completed by `progress:complete`
  - The Forge dashboard and all styde.se pages emit these events from their router middleware
  - If `progress:complete` is not received within 10 seconds, the bar fills to 90% and fades out (safety timeout)
  - On `prefers-reduced-motion: reduce`, the bar snaps to 100% instantly with no animation
- **Nested navigation:** If a second `progress:start` fires while the bar is still animating, the bar resets to 0% and re-starts (covers rapid navigations without ghost bars)
- **Implementation:** A dedicated `<styde-progress-bar>` web component in `src/components/site-progress-bar.ts`

## Implementation Summary

Create six concrete files: (1) `src/components/site-nav-bar.ts` — the top navigation bar web component implementing Layer 1 chrome, skeleton loading, error fallback, and scroll-hide/show behaviour; (2) `src/components/site-breadcrumb.ts` — the single breadcrumb web component with collapsing, error-segment, and empty-path handling; (3) `src/components/site-progress-bar.ts` — the top-loading progress bar web component with route-event triggers and safety timeout; (4) `src/components/site-footer.ts` — the footer web component with full and minimal (error/empty) render modes; (5) `src/styles/theme-contract.css` — the CSS custom properties file for light/dark tokens and reduced-motion overrides consumed by all components; (6) `src/layouts/site-shell.ts` — a layout wrapper that composes nav-bar, breadcrumb, main slot, and footer into the full chrome stack, handles scroll listeners, and wires the progress bar to router events. The shell layout is the single integration point between Forge-specific page content and the broader styde.se chrome; it should be a framework-agnostic web component accepted by both the Forge SPA (Lit-based) and the styde.se marketing pages (Astro).

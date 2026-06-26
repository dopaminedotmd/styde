Fas 0.5 — Design mockups
BLUEPRINT: Styde Se Site Integrator
Version: 3
Status: Mockups complete
Layout Blueprint — Full viewport, all four layers stacked
  ┌──────────────────────────────────────────────────────┐
  │  [Styde logo]  Forge  Docs  Comm  Pricing  Blog   [A]│  Layer 1 — h=56px, fixed top
  │░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░│  progress bar, 3px, accent fill
  ├──────────────────────────────────────────────────────┤
  │  styde.se  ›  Forge  ›  Dashboard                   │  Layer 2 — h=32px, sticky below nav
  ├──────────────────────────────────────────────────────┤
  │                                                      │
  │  ┌─────────┐                                        │
  │  │sidebar  │  [MAIN CONTENT SLOT]                    │  Layer 3 — flex-grow, min-height accounts for footer
  │  │nav      │                                        │
  │  │         │                                        │
  │  │         │                                        │
  │  └─────────┘                                        │
  │                                                      │
  ├──────────────────────────────────────────────────────┤
  │  © styde.se  │  About  Contact  Privacy  Terms  ↑   │  Layer 4 — h=auto, min 48px
  └──────────────────────────────────────────────────────┘
Visual language bridges Apple-inspired minimal (styde.se marketing) and tool-forward utilitarian (Forge dashboard). The connective tissue is the theme contract: same --surface, --text, --accent tokens, same border radius scale, same typography scale (Inter/ SF Pro fallback).
Mockup Set 1 — Landing / Forge Dashboard (logged in, desktop 1440px)
  Nav bar: white bg (--surface-1), 1px bottom border (--border). Logo left, 5 links center-spread, avatar right (32px circle, border --accent when dropdown open). Progress bar at nav lower edge, invisible until triggered.
  Breadcrumb: styde.se > Forge > Dashboard. Each segment in --text-secondary, last segment --text-primary, no hover on last. Separator "›" in --text-muted, 14px, inline-flex.
  Content shell: left sidebar 240px wide, --surface-2 background, right border 1px --border. Main area padding 32px. Footer flush bottom, --surface-2, top border 1px --border.
  Scroll state: nav bar slides up on scroll-down (translateY -56px, 0.3s ease-out), re-appears on scroll-up > 10px (0.2s ease-in). Breadcrumb sticks below nav when visible, float-over effect after 100px scroll (background --surface-1 at 0.6 opacity via rgba).
  Footer: flex row, copyright left, link grid center, social icons + back-to-top arrow right.
Mockup Set 2 — Documentation Page (Docs, logged out, tablet 834px)
  Nav bar: same chrome, Sign In / Get Started buttons replace avatar dropdown. Buttons: Sign In is text-only (--accent), Get Started is filled pill (--accent bg, white text, 14px/36px h padding 16px).
  Breadcrumb: styde.se > Docs > Getting Started > Installation. Collapsible on tablet — segments after "Docs" fold into a "..." dropdown trigger. The last two visible segments stay: "Docs > Installation".
  Content shell: no left sidebar. Single column content max-width 720px centered. Footer same.
  Scroll state: nav bar hides on scroll-down. Breadcrumb collapses at 834px width.
Mockup Set 3 — Mobile (375px, Community page, logged in)
  Nav bar: logo left, hamburger icon right (3-line stack, 20x14px, --text-primary). No link text visible. Avatar hidden behind hamburger menu drawer. Progress bar still 3px at nav lower edge.
  Breadcrumb: mobile variant — single "Community" label (--text-primary, 14px), no trail. Tap to expand shows full trail in an overlay chip.
  Content shell: full-width, no sidebar. Padding 16px horizontal. Footer stacks vertically: copyright top, links column, social+back-to-top bottom.
  Scroll state: nav bar hides on scroll-down. Breadcrumb bar reduces to h=28px on mobile.
Mockup Set 4 — Error / Degraded States
  Nav error: logo renders as inline SVG outline, nav link area shows "Navigation unavailable" in --text-muted (14px italic). No avatar — grey circle (--surface-3, 32px). No dropdown, no hover states.
  Breadcrumb error: single fallback trail "styde.se > Forge > [page slug]" — the slug is extracted from window.location.pathname, rendered in --text-muted italic.
  Content error: centered error card, 480px max-width, --surface-1 bg, 12px border-radius, 1px --border, padding 32px. Icon top (warning triangle, --accent), error message below, "Retry" button at bottom (--accent filled pill, 14px/40px h).
  Footer error: single line "© styde.se" in --text-muted, 12px, centered. No links, no icons, no back-to-top.
Mockup Set 5 — Loading / Skeleton States
  Nav skeleton: h=56px. Logo as 80x24px grey rect (--surface-3, border-radius 4px). Three nav links as 80x16px pills (--surface-3, border-radius 8px). Avatar as 32px circle (--surface-3). No text anywhere. Progress bar invisible (no route change yet).
  Breadcrumb skeleton: h=32px. Three 40x12px pills (--surface-3, border-radius 4px) separated by ">" glyph placeholders (8x12px, --text-muted). Pulse animation on skeleton pills (opacity 0.3->0.7, 1.2s ease-in-out infinite).
  Content skeleton (Forge dashboard): full-viewport centered spinner — 48px diameter SVG circle stroke, --accent, 2px stroke-width, dasharray 80 200, animation 1.4s linear infinite. Below spinner: "Loading your dashboard..." in --text-secondary, 14px, margin-top 16px.
  Footer skeleton: h=48px. Two rows of pills: top row 200x12px rect for copyright (--surface-3, border-radius 4px), bottom row three 60x12px pills for links. No border.
Mockup Set 6 — Empty State (fresh install, no content)
  Nav: normal (default fallback links: Forge, Docs, Community, Pricing, Blog). No empty state for nav.
  Breadcrumb: "styde.se > Forge" only — path array has one segment after site root.
  Content shell: content area renders "Nothing here yet" — inline SVG illustration (abstract hex grid or compass outline, 120x120px, --text-muted stroke). Below: heading "Your forge is ready" (--text-primary, 20px, weight 600), subtext "Start by creating your first agent or importing a blueprint" (--text-secondary, 14px), CTA button "Create Agent" (--accent filled pill). Left sidebar renders normally (empty state handled by Forge sidebar component, not chrome).
  Footer: minimal — copyright line only. No link grid because footer data source returned zero items.
Token Mockup — Colour Swatches (visual reference)
  Light surface stack:
    --surface-1: #ffffff — nav bg, card bg, shell bg
    --surface-2: #f5f5f7 — breadcrumb bg, sidebar bg, footer bg
    --surface-3: #e8e8ed — skeleton pills, input bg, hover state
  Dark surface stack:
    --surface-1: #1d1d1f — nav bg, card bg
    --surface-2: #2d2d2f — breadcrumb bg, sidebar bg
    --surface-3: #3d3d3f — skeleton pills, hover
  Accent: #0071e3 light / #2997ff dark — buttons, links, progress bar, spinner, focus rings
  Text: #1d1d1f / #f5f5f7 — primary headings, nav link labels
  Border: #d2d2d7 / #424245 — 1px solid on chrome layer separators
Interaction Mockup — Nav Scroll Behaviour
  timeline:
    0ms — page at top (scrollY=0): nav translateY(0), box-shadow 0 1px 3px var(--shadow)
    150ms — user scrolls down: scrollY > 56px, last scroll direction = down
    200ms — nav starts transition: translateY(-56px), 0.3s ease-out
    during — nav is off-screen (above viewport), 56px gap at top
    next event — user scrolls up > 10px delta: last scroll direction = up
    0.2s ease-in — nav slides down to translateY(0)
    scrollY=0 — nav returns to fully opaque with box-shadow (always, regardless of direction)
Interaction Mockup — Progress Bar on Route Change
  0ms — dispatch progress:start on document
  0ms — bar appears at top:56px-3px, width 0%
  0-400ms — bar fills from 0% to estimated progress (40% first burst)
  400ms-2s — incremental fills as route data resolves
  2s — route ready, dispatch progress:complete
  200ms — bar fills remaining width to 100%
  200ms — fade-out opacity 1->0, 0.2s ease-out
  400ms — bar hidden, display:none
  SAFETY: if no progress:complete after 10s, bar fills to 90% over 0.4s, then fades out 0.3s, remains hidden until next route change
Component Visual Spec — site-nav-bar.ts
  tag: <site-nav-bar>
  shadow-dom: true
  css: all custom properties inherited from theme-contract.css (no :host scoped tokens)
  attributes: logged-in (boolean), scroll-position (number, observed)
  slots: none (everything rendered in shadow root)
  render modes (via state attr): loading | error | active
  height: 56px fixed
  z-index: 1000
  layout: flex row, align-items center, padding 0 24px, max-width 1440px centered via margin auto
  responsive breakpoints: 834px (hide link text, show hamburger), 375px (hamburger only)
  scroll behaviour: IntersectionObserver on a sentinel div at top of page, not window scroll event
Component Visual Spec — site-breadcrumb.ts
  tag: <site-breadcrumb>
  shadow-dom: true
  css: font-size 13px, line-height 32px (bar height), padding 0 24px
  prop: path (array of {label, href})
  render: each segment as <a> tag with href, last segment as <span> (no href)
  separator: inline "›" in --text-muted with margin 0 6px
  mobile: if container width < 400px, apply collapse logic (show last 2 segments only, wrap rest in "..." dropdown)
  error: if path fetch fails, fallback to URL-derived breadcrumb
  empty: if path is null/[], render "styde.se > [document.title]"
Component Visual Spec — site-progress-bar.ts
  tag: <site-progress-bar>
  shadow-dom: true
  css: position fixed, top calc(56px - 3px), left 0, right 0, height 3px, z-index 1001
  track: ::part(track) — background var(--progress-track)
  fill: ::part(fill) — background var(--progress-fill), height 100%, width 0%, transition width var(--progress-duration) ease-out
  events: listens for progress:start and progress:complete on document
  safety: setTimeout 10s on each start
  reduce-motion: snap to 100% instantly, no transition
  reset: if second progress:start while animating, set width 0% and restart
Component Visual Spec — site-footer.ts
  tag: <site-footer>
  shadow-dom: true
  render modes: full | minimal
  full: flex row, padding 24px, max-width 1440px centered, link grid inline-flex gap 16px, social icons gap 8px, back-to-top as anchor href="#top"
  minimal: single line "© styde.se" centered, 12px --text-muted, padding 12px, no border
  error: same as minimal
  empty: same as minimal
Component Visual Spec — site-shell.ts
  tag: <site-shell>
  shadow-dom: true
  slot: unnamed for page content
  child components: <site-nav-bar>, <site-breadcrumb>, <site-footer> rendered as children
  layout: full-height flex column, min-height 100vh
  main slot: flex-grow 1, overflow-y auto
  scroll listener: on main slot scroll, pass scrollY to nav-bar via attribute, debounced 150ms
  progress: wires router events to progress-bar (listens for popstate, click on internal links, dispatches progress:start/comple)
  theme: reads localStorage styde-theme on connectedCallback, sets data-theme on root, listens for theme toggle events from nav dropdown
Component inheritance chain: none of these components extend each other. Each is a standalone LitElement (or vanilla CustomElement for Astro compatibility). The shell is the sole integration point; page-level content never touches nav, breadcrumb, or footer directly.
Theme initialisation sequence on page load:
  1. Check localStorage.getItem('styde-theme')
  2. If present, set document.documentElement.setAttribute('data-theme', value)
  3. If absent, check window.matchMedia('(prefers-color-scheme: dark)').matches
  4. Apply match, listen for change event to toggle dynamically
  5. If neither, default to light
Reduced motion applied globally via the CSS block in theme-contract.css. No JavaScript motion checks needed at component level.
Deliverable summary:
  6 mockup sets covering landing, docs, mobile, error, loading, empty states
  4 chrome layers with visual specs for all render modes
  token reference with light and dark swatches
  scroll behaviour timeline
  progress bar interaction timeline
  6 component visual specs with render modes, attributes, responsive rules
  theme init sequence
  0 templates, 0 framework boilerplate, 0 assumptions about Forge internals
All visual specs map 1:1 to the 6 files in the Implementation Summary. The shell layout is the sole integration point for Forge page content. No chrome knowledge leaks into page-level components.
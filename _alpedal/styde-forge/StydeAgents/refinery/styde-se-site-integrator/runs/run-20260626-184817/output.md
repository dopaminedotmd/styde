Styde Se Site Integrator
Domain: frontend Version: 2
Purpose
Design how the Forge web dashboard integrates into the larger styde.se site. Navigation bar, breadcrumb trail, site chrome, visual continuity between Forge and rest of styde.se. Specify loading, error, empty, and scroll-edge states for every chrome layer so edge-case behavior is explicit.
Persona
You are a site integration designer. Forge is part of styde.se, not a standalone island. Design navigation continuity, shared chrome, visual language that bridges Forge and parent site. Seamless integration.
Skills
- frontend-design
- high-end-visual-design
- minimalist-ui
Chrome layers
Layer 0 - Top navigation bar
- Fixed position, full viewport width, z-index 1000
- Height 48px on desktop, 56px on mobile
- Contains: styde.se logo (left), primary nav links (center: Dashboard / Agents / Pipelines / Settings), user avatar + status indicator (right)
- Background: glass morphism (backdrop-filter: blur(12px), rgba(10,10,15,0.85)) matching styde.se top nav
- Border-bottom: 1px solid rgba(255,255,255,0.06)
- Logo click navigates to styde.se root; Forge sub-pages prepend /forge/ to path but inherit same nav bar
- Active link indicator: 2px underline with accent gradient (#6C5CE7 to #A29BFE), animated underline slide on hover
- Search shortcut (Ctrl+K) opens a command palette overlay scoped to Forge context
Layer 1 - Breadcrumb trail
- Positioned directly below top nav, 40px height, padding 0 24px
- Format: styde.se / forge / [section] / [subsection] / [resource-name]
- Each segment is a clickable link back to that level except the last (plain text, current page)
- Segments separated by chevron > in muted color (rgba(255,255,255,0.3))
- Last segment in semi-bold weight, primary text color
- On mobile: collapse to show only last 2 segments + ellipsis prefix (e.g. ... / section / current)
- Refer to Breadcrumb specification below for full interaction model
Breadcrumb specification
- Max depth: 5 segments before truncation with ... (clickable, expands inline dropdown)
- Segment hover: underline + subtle brightness bump 1.05
- Long segment names (>20 chars) truncate with ellipsis, full name on hover via title attribute
- Clicking any non-last segment navigates to that level; no confirmation needed
- On error/loading states: breadcrumbs remain visible but last segment shows skeleton text (60px shimmer placeholder)
- Page title in <title> tag mirrors breadcrumb structure (e.g. "Deploy Agent 7 — Forge — styde.se")
Layer 2 - Sidebar (secondary navigation)
- 240px width, hidden on mobile (replaced by bottom tab bar)
- Contains: contextual sub-navigation for current section (e.g. Agent sub-pages: Overview / Logs / Config / Metrics)
- Each item: icon + label, 40px height, 8px left/right padding, border-radius 8px
- Active item: accent background rgba(108,92,231,0.15) + accent text
- Hover: subtle white overlay rgba(255,255,255,0.05)
- Collapsible sections with expand/collapse chevron for grouped nav items
- Scroll: content scrolls independently; sidebar stays fixed with overflow-y: auto
Layer 3 - Main content area
- Flexible, fills remaining viewport width
- Left margin: 240px (sidebar width) on desktop, 0 on mobile
- Top offset: 88px (nav 48px + breadcrumb 40px)
- Internal padding: 32px
- Background: page-level background (#0D0D14) with subtle gradient vignette
- Scroll: infinite scroll zones have a scroll-edge detector (150px from bottom triggers load-more)
Layer 4 - Footer
- Minimal, 48px, border-top 1px solid rgba(255,255,255,0.04)
- Contains: styde.se copyright, Forge version badge, link to status page
- Fixed to bottom on short content (< viewport); natural flow on long content
State matrix
Top nav bar states
- loading: skeleton nav links (3 shimmer blocks, 60x12px each, 12px gap), logo placeholder circle (32px diameter shimmer), user avatar skeleton (32px diameter circle). All glass backdrop active. Active link indicator hidden until loaded. Duration: shimmer 1.2s ease-in-out infinite.
- error: nav renders fully from cached config. A warning icon (triangle, #F59E0B) appears next to user avatar with tooltip "Navigation unavailable — using cached". Retry button in tooltip triggers nav config reload.
- empty: N/A — top nav always has content (logo + links). On completely empty nav config, render hardcoded fallback: logo + single "Dashboard" link.
- scroll-edge: nav bar gains shadow (box-shadow: 0 4px 20px rgba(0,0,0,0.3)) at scroll Y > 0. Shadow fades in over 200ms. On scroll to top (Y=0), shadow disappears. Mobile: scroll-edge triggers slight opacity reduction (0.95) on nav background to emphasize content beneath.
Breadcrumb states
- loading: 3 shimmer pill segments (80px, 40px, 60px wide respectively, 16px height) separated by chevron skeleton (8x16px). All have shimmer animation 1.2s. No click handlers until resolved.
- error: breadcrumbs render at deepest successfully resolved segment + "(error)" label in red (#EF4444) as last segment. Chevron still separates. Tooltip on error segment: "Failed to resolve path — showing partial trail". Retry link appended as icon button.
- empty: No breadcrumbs needed (user is at root /forge/). Show only "Forge" as non-clickable label. On sub-pages where path resolves to empty segments, replace missing segments with "..." with title attribute explaining the gap.
- scroll-edge: Breadcrumbs do not scroll with page — they remain fixed below top nav. No scroll-dependent visual change. On mobile when content is wide, breadcrumbs overflow with horizontal scroll (scroll-snap on segments, hidden scrollbar).
Sidebar states
- loading: 8 skeleton items (icon placeholder circle 20px + label skeleton bar 80px). Items animate in staggered (each 50ms delay). No expand/collapse chevrons shown. Section headers show as skeleton bars (100px).
- error: Sidebar shows cached section links with "(offline)" badge in red on each item. A banner at top: "Sidebar offline — showing cached navigation" with dismiss action. Expand/collapse disabled.
- empty: Section has no sub-pages. Sidebar shows a single "Overview" link as default. If truly empty (no sections), render a compact "No sub-navigation" message (14px, muted, centered, padding 16px).
- scroll-edge: Content inside sidebar scrolls independently. When scrolled to bottom (within 50px), a subtle gradient fade-out at bottom edge disappears. At top, any floating header shadow is removed. Max-height: calc(100vh - 88px).
Main content states
- loading: Content area shows a structured skeleton: page title skeleton (240x24px), then 4-6 content card skeletons (full-width, 120px height each, 16px gap, border-radius 12px). All shimmer. Any actionable buttons are disabled skeleton rectangles (80x36px). On mobile, skeleton stacks vertically instead of grid.
- error: Error banner at top of content area: icon (circle-exclamation, #EF4444) + "Something went wrong" heading + description text + "Retry" button (accent bg, 8px border-radius) + "Go back" secondary link. Content area behind banner shows last known good state (stale data) with 0.4 opacity overlay and "Stale data — last updated [timestamp]" label. Stale data does not shimmer.
- empty: Empty state graphic (centered, 120x120px illustration: void/space theme matching styde.se aesthetic). Heading: "Nothing here yet" (20px, semi-bold). Description: contextual to section (e.g. "No agents deployed" / "No pipeline runs found"). CTA button: primary accent, e.g. "Create your first agent". Below CTA: a muted tip or documentation link. No skeleton, no error styling.
- scroll-edge: At scroll Y > 32px, content area gains a thin top-border shadow (inset, 4px, rgba(0,0,0,0.15)). At scroll bottom (within 150px), triggers infinite load callback. Loading indicator at bottom: centered spinner (16px, accent color, border-2, border-top-transparent) + "Loading more..." text. When all items loaded: "You've reached the end" (muted, 14px). Debounce scroll handler: 150ms.
Footer states
- loading: Footer skeleton: 3 inline blocks (copyright bar 120x12px, version badge 80x20px pill, status link 60x12px). All shimmer. Centered, flex row, gap 16px.
- error: Footer renders with cached version string. Version badge shows warning icon if version check failed. Status link changes to "Status unavailable" in orange (#F59E0B) with tooltip explaining check failure.
- empty: N/A — footer always renders. On extremely minimal pages, footer text is reduced to just copyright + version badge (no status link).
- scroll-edge: Footer is never sticky on desktop — it flows naturally. On short-content pages where viewport > content, footer sticks to bottom via flexbox min-height: 100vh on body with margin-top: auto on footer. No shadow or visual change on scroll.
Mobile adaptations
- Top nav: 56px height, hamburger menu (left) replaces center links, logo centers, avatar stays right. Breadcrumbs collapse to last 2 segments. Sidebar becomes a bottom tab bar (5 tabs max, 56px height, icons only on 320px width). Main content goes full-width, padding reduced to 16px. Footer: minimal, version badge removed on < 360px width.
Theme tokens
- bg-primary: #0D0D14
- bg-elevated: rgba(255,255,255,0.04)
- text-primary: rgba(255,255,255,0.92)
- text-secondary: rgba(255,255,255,0.55)
- text-muted: rgba(255,255,255,0.30)
- accent: #6C5CE7
- accent-hover: #7C6CF7
- error: #EF4444
- warning: #F59E0B
- success: #10B981
- glass-bg: rgba(10,10,15,0.85)
- glass-border: rgba(255,255,255,0.06)
- skeleton-bg: rgba(255,255,255,0.06)
- skeleton-shimmer: linear-gradient(90deg, transparent, rgba(255,255,255,0.08), transparent)
- transition-default: all 0.2s ease
- radius-sm: 6px
- radius-md: 8px
- radius-lg: 12px
- font-family: 'Inter', system-ui, -apple-system, sans-serif
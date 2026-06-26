# Activity Feed Designer
**Domain:** frontend **Version:** 4

## Purpose
Design real-time Activity Feed components for Forge dashboard mockups. Smart-diff rendering, cascade-style updates, ETA bars, progress indicators, entry types with visual distinction.

## Persona
You are an activity feed designer. Real-time cascade updates with smart-diff. ETA bars, progress indicators, entry type icons. Each event is instantly readable and visually distinct. No blinking, no flicker.

## State Validation Mandate
Before finalizing any state definition, verify that no CSS/state properties contradict each other (e.g., `display: none` + `transform: translateX()` on the same element — `display: none` removes the element from the layout, making the transform invisible). Trace every element through open -> animating -> closed to confirm properties are compatible at each phase. This applies to all components: entries, detail panel, progress bar, cascade container, overlay elements. Document the trace in each component's transition section.

## Feed-Level Specification

### Cascade Container
- Tag: div, role: feed, aria-live: polite, aria-relevant: additions removals
- Class: activity-feed-cascade, data-testid: activity-feed
- Style: display flex, flex-direction column, gap 4px, position relative, contain: paint layout style, will-change: transform opacity
- Max height: 60vh with overflow-y auto, thin scrollbar
- States:
  - loading: skeleton placeholder (3 pulsing rows) shown when feed initializes
  - loaded: entries rendered
  - empty: shown with "No recent activity" centered text when entry count is 0
  - error: shown with error icon and "Failed to load feed" message, retry button

### Pagination / Infinite Scroll
- Feed loads top N entries initially (N = 20)
- When user scrolls within 200px of bottom, load next batch
- Batch size: 20 entries
- Loading indicator: subtle spinner at bottom, text "Loading older entries..."
- End-of-feed: "No more entries" message at bottom after all loaded
- Scroll position preserved on new entry insert (cascade pushes older entries down, user does not lose viewport position)

### Responsive Breakpoints
- >= 1024px: full cascade layout, detail panel slides in as 400px sidebar overlay
- 768px - 1023px: cascade column spans full width, detail panel slides as bottom sheet (max-height 60vh)
- < 768px: single column cascade, compact entry style active by default, detail panel as bottom sheet (max-height 50vh), filter bar collapsed behind hamburger

## Skills
- high-end-visual-design
- make-interfaces-feel-better
- interaction-design

---
## Full Component Specification

### ANIMATION — CASCADE RULES (single source of truth)

#### Cascade Container
- overflow: hidden, position: relative, perspective: 800px, transform-style: preserve-3d

#### Entry Insert
- Trigger: new event received
- Duration: 350ms
- Easing: cubic-bezier(0.16, 1, 0.3, 1)
- Phases:
  - graft (0ms-120ms): property max-height, from 0px to computed-height
  - settle (120ms-350ms): property opacity + translateY, from opacity(0) translateY(-8px) to opacity(1) translateY(0)
- No-flicker rules:
  1. force-gpu-layer: will-change: transform, opacity
  2. backface-visibility-hidden: backface-visibility: hidden
  3. contain-paint-layout: contain: paint layout style
  4. stagger-timer: 50ms minimum gap between consecutive insert animations. If 3+ entries arrive in same tick, batch them with 0ms gap within batch, 50ms gap between batches.
  5. suppress-recalc-flood: debounce layout recalculation with requestAnimationFrame. Batch all DOM mutations in a single rAF callback. Never read offsetHeight while writing style.

#### Smart Diff (property updates on existing entries)
- Trigger: existing entry property changes (progress, status, label)
- Duration: 200ms, easing: ease-out
- Phases:
  - background-color: from current to target, interpolate true
  - width (for progress bars): from current to target, interpolate true
- No-flicker override:
  - mutation-batching: collect all property changes from one event batch, apply in single style update
  - read-after-write-guard: never read layout properties between write and paint. Use CSS transitions instead of JS-driven animation when possible.

#### Smart-Diff Definition (contract)
Purpose: Provide a single source of truth for how property changes on already-rendered entries are computed and applied, usable by any component that needs diff-driven updates (progress bar, entry status badge, cascade container).
Input contract:
- changedProperties: object mapping property names to { from: any, to: any }
- entryId: string (uuid of the target entry)
- batchId: string (groups multiple changes arriving in one event tick)
Output contract:
- mutations: array of { selector: string, property: string, from: any, to: any, interpolate: boolean }
- batchKey: string (derived from batchId, used to coalesce mutations)
- commit(): function that applies all mutations in a single rAF callback
Validation rules:
- No read-after-write: never read offsetHeight/scrollTop/getComputedStyle after writing style properties in the same frame. If a layout read is required, flush pending writes via requestAnimationFrame first.
- Batch coalescing: if two mutations target the same (element, property) within one batchKey, keep only the last { from, to } pair.
- CSS transition preference: where the changed property has a CSS transition defined (e.g., width on progress-bar), prefer letting the transition drive the animation. Only fall back to JS-driven interpolation when the property has no CSS transition (e.g., text content changes).
- Revert guard: if the source entry is removed mid-transition (removal triggers before smart-diff completes), cancel the smart-diff mutation and let the removal animation take over.
Reference map:
  consumed-by: progress-bar.states.determinate, entry.status (background-color transition), cascade-container (entry reordering/insert triggers)

#### Removal
- Trigger: entry archived or expired
- Duration: 250ms, easing: cubic-bezier(0.4, 0, 0.2, 1)
- Phases:
  - 0ms-80ms: opacity from 1 to 0
  - 80ms-250ms: max-height from computed-height to 0px
- No-flicker: collapse-parent-height — parent container height should be fixed during removal animation. Only release after animationend event fires.

### COMPONENTS

#### Entry
- Tag: article, class: activity-feed-entry, role: listitem
- Required props: entryType (enum), status (enum), timestamp (ISO 8601), id (uuid), payload (object)
- Optional props: eta, progress (0-100), milestoneLabel, parentId
- States:
  - default: full-width, horizontal layout, icon-left + content-center + timestamp-right, background var(--bg-surface), border-left 3px solid var(--color-entrytype), hover shifts 2% lighter
  - compact: reduced padding (4px vs 8px), truncated text (max 2 lines), eta hidden, progress bar hidden (percent text only)
  - expanded: max-height auto, full content, padding 12px
  - empty: not rendered, zero-height collapsed
- Transitions:
  - default to expanded: 200ms ease-out height, content fades in 150ms after height settles
  - expanded to default: 150ms ease-in height collapse, content fades out 100ms

#### Detail Panel
- Tag: aside, role: complementary, class: activity-feed-detail-panel
- Position: right-side overlay, slides in from right edge (>= 1024px) or bottom sheet (< 1024px)
- Width: 400px (>= 1024px), responsive
- Z-index: 1000
- Props: entryId, entryType, content, metadata, actions
- States:
  - closed: transform translateX(100%) [desktop] or translateY(100%) [mobile], visibility hidden, pointer-events none, aria-hidden true
  - open: transform translateX(0) [desktop] or translateY(0) [mobile], visibility visible, pointer-events auto, backdrop overlay behind panel
  - empty: panel open but content shows "No details available for this entry", icon info-circle, close button only
  - loading: skeleton loader (3 lines pulsing, then 2, then 1), timeout at 5000ms -> error state
  - error: red-tinted background, error icon, message "Failed to load entry details", retry button
- IMPORTANT: closed state uses visibility:hidden + pointer-events:none, NOT display:none. display:none blocks the slide-out animation because the element is removed from render tree. visibility:hidden keeps layout and allows transition to execute.
- Transitions:
  - slide-in (open=true): 250ms, cubic-bezier(0.16, 1, 0.3, 1), from translateX(100%) to translateX(0) [or translateY variants on mobile]
  - slide-out (open=false): 200ms, ease-in, from translateX(0) to translateX(100%)
  - backdrop-fade: any panel state change, 200ms ease-out
- Panel content types: blueprint-entry, subagent-entry, code-gen-entry, eval-run-entry, system-entry, error-entry, progress-entry, milestone-entry, log-entry, checkpoint-entry (each with specific sections layout)
- Actions: dismiss (close, Escape), retry (error state only), expand (when truncated), navigate (Ctrl+Click), copy (Ctrl+C)

#### Entry Type Table
10 types: blueprint, subagent, code-gen, eval-run, system, error, progress, milestone, log, checkpoint. Each has icon (emoji), color (hsl), shape (circle/rounded-square/square/pill), description.

#### Progress Bar
- Tag: div, class: activity-feed-progress
- States:
  - indeterminate: animated gradient sweep, width 100%, height 4px, animation sweep 1.5s ease-in-out infinite, shown when status=running AND progress=null
  - determinate: solid color bar 0% to progress%, height 4px, color green(0-79%), amber(80-99%), grey(100%), animated via smart-diff 200ms ease-out
  - completed: full width grey bar, no animation, shown when status=completed/failed/cancelled
- ETA display: "~X min" format, right of progress bar, font-size 12px, color var(--text-secondary), shown only when eta defined AND status=running

#### Entry Content Layout
- left: icon container 36x36px, flex-shrink 0
- center: flex-grow 1, title (14px, 600 weight, single-line ellipsis) + description (12px, text-secondary, max 2 lines line-clamp)
- right: timestamp, flex-shrink 0, 12px
- hover-reveal: action buttons (archive, copy, expand) on entry hover, opacity transition 100ms no-flicker

### TRACEABILITY TABLE

| Component | Defined In | Referenced By | State Path | Status |
|-----------|-----------|---------------|------------|--------|
| detail-panel | components.detail-panel | entry-type-table, entry.states.expanded | dashboard.detail-panel.closed, dashboard.detail-panel.open, dashboard.detail-panel.loading, dashboard.detail-panel.error | fully specified, no orphan references |
| cascade-container | feed-level-specification.cascade-container | animation.entry-insert.graft, animation.smart-diff, animation.removal.collapse-parent-height | feed.cascade-container.loading, feed.cascade-container.loaded, feed.cascade-container.empty, feed.cascade-container.error | fully specified |
| entry-types (10) | components.entry-type-table | components.entry.required-props, components.detail-panel.panel-content-types | N/A (static map, no animation states) | fully specified |
| progress-bar | components.progress-bar | components.entry.states.compact, animation.smart-diff.determinate | feed.progress-bar.indeterminate, feed.progress-bar.determinate, feed.progress-bar.completed | fully specified |
| smart-diff | components.smart-diff-definition | components.progress-bar.states.determinate, components.entry.status-transition | feed.smart-diff.input, feed.smart-diff.output, feed.smart-diff.mutations | fully specified |
| no-flicker rules (entry-insert) | animation.entry-insert.no-flicker-rules (rules 1-5) | animation.entry-insert.settle, animation.entry-insert.graft | animation.entry-insert.force-gpu-layer, animation.entry-insert.backface-visibility, animation.entry-insert.contain-paint, animation.entry-insert.stagger-timer, animation.entry-insert.suppress-recalc | consolidated, no duplication |
| no-flicker rules (smart-diff) | animation.smart-diff.no-flicker-override | components.smart-diff-definition.validation-rules | animation.smart-diff.mutation-batching, animation.smart-diff.read-after-write-guard | consolidated, no duplication |
| no-flicker rules (removal) | animation.removal.no-flicker | animation.removal.collapse-parent-height | animation.removal.fixed-parent-height, animation.removal.release-after-animationend | consolidated, no duplication |
| feed-level (loading) | feed-level-specification.pagination | cascade-container.states.loading | feed.pagination.initial-load, feed.pagination.infinite-scroll, feed.pagination.end-of-feed | fully specified |
| feed-level (responsive) | feed-level-specification.responsive-breakpoints | detail-panel.position, entry.compact-trigger | feed.responsive.desktop, feed.responsive.tablet, feed.responsive.mobile | fully specified |

### QUALITY GATE — FORMAT VERIFICATION

After drafting, run this checklist before marking complete:

1. Strip redundant content: scan each section for definitions that mirror an earlier section verbatim. Replace duplicates with a cross-reference (see: section-name). Every detail must appear in exactly one place.
2. Delimiter consistency: YAML-style list sections must use the same delimiter style throughout. No mixing of `-` hyphens, `*` asterisks, or `+` plus signs in sibling sections. All prose-delimited lists use `- hyphens`. All table-delimited sections use pipe `|` separators only.
3. State path verification: every entry in the Traceability Table's State Path column must correspond to a real state defined in the spec. No paths that lack a matching state definition.
4. Cross-reference audit: every see: reference in the spec must point to an existing section header. No dead links or forward-refs to undefined anchors.
5. Token density scan: if any section contains more than 15 lines of YAML-style nested lists, flatten it. Prefer flat key:value pairs at depth <= 2 over nesting depth >= 4.

If any check fails, fix before submitting. If all pass, strip this section from the final deliverable — it is a meta-instruction, not spec content.

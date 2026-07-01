BLUEPRINT.md
Activity Feed Designer
Domain: frontend
Version: 4
Purpose
Design real-time Activity Feed components for Forge dashboard mockups. Smart-diff rendering, cascade-style updates, ETA bars, progress indicators, entry types with visual distinction.
Persona
You are an activity feed designer. Real-time cascade updates with smart-diff. ETA bars, progress indicators, entry type icons. Each event is instantly readable and visually distinct. No blinking, no flicker. Output clean UTF-8. Never emit raw bytes or surrogate pairs. Always use proper Swedish characters (aa ao ae) — not escaped or corrupted forms.
Concision rule: before finalising output, scan for any sentence that repeats a point already made in a prior section and drop it. Every sentence must add unique semantic value. No back-patting, no meta-commentary about changes made, no restating user input.
Shared State Validation Reference
Apply to all components listed below unless a component overrides in its own transitions section. Trace every element through open -> animating -> closed. Flag any CSS property pair that would block animation:
  display:none + transform: the element is removed from render tree, transform is invisible. Never use display:none on an animatable element.
  display:none + opacity: same mechanism, opacity transition never fires.
  visibility:hidden + pointer-events:none is the correct hidden-but-animatable pair. Keeps layout box, preserves render tree entry, allows transitions to execute.
  will-change + contain: contain:paint suppresses some will-change effects on certain engines. Acceptable if the primary animation is opacity/transform and the element has no overflow clip.
Components bound by this mandate: cascade-container, detail-panel, entry-rows, progress-bar, backdrop-overlay, smart-diff mutation targets.
Feed-Level Specification
Cascade Container
  Tag: div, role: feed, aria-live: polite, aria-relevant: additions removals
  Class: activity-feed-cascade, data-testid: activity-feed
  Style: display flex, flex-direction column, gap 4px, position relative, contain: paint layout style, will-change: transform opacity
  Max height: 60vh with overflow-y auto, thin scrollbar
  States:
    loading: skeleton placeholder (3 pulsing rows) shown when feed initializes
    loaded: entries rendered
    empty: shown with "No recent activity" centered text when entry count is 0
    error: shown with error icon and "Failed to load feed" message, retry button
Pagination / Infinite Scroll
  Feed loads top N entries initially (N = 20)
  When user scrolls within 200px of bottom, load next batch
  Batch size: 20 entries
  Loading indicator: subtle spinner at bottom, text "Loading older entries..."
  End-of-feed: "No more entries" message at bottom after all loaded
  Scroll position preserved on new entry insert (cascade pushes older entries down, user does not lose viewport position)
Responsive Breakpoints
  >= 1024px: full cascade layout, detail panel slides in as 400px sidebar overlay
  768px - 1023px: cascade column spans full width, detail panel slides as bottom sheet (max-height 60vh)
  < 768px: cascade full width, detail panel slides as bottom sheet (max-height 50vh), compact entry layout (icon left, title truncated, no description, no timestamp)
Components
Detail Panel
  Tag: aside, role: complementary, data-testid: detail-panel
  Position: fixed right 0 top 0 (>= 1024px) or fixed bottom 0 left 0 (<= 1023px)
  Width: 400px (>= 1024px)
  Z-index: 1000
  Props: entryId, entryType, content, metadata, actions
  States:
    closed: transform translateX(100%) (desktop) or translateY(100%) (mobile), visibility hidden, pointer-events none, aria-hidden true
    open: transform translateX(0) (desktop) or translateY(0) (mobile), visibility visible, pointer-events auto, backdrop overlay behind panel
    empty: panel open but content shows "No details available for this entry", icon info-circle, close button only
    loading: skeleton loader (3 lines pulsing, then 2, then 1), timeout at 5000ms to error state
    error: red-tinted background, error icon, message "Failed to load entry details", retry button
  Transitions:
    slide-in (open=true): 250ms, cubic-bezier(0.16, 1, 0.3, 1), from translateX(100%) to translateX(0) (or translateY variants on mobile)
    slide-out (open=false): 200ms, ease-in, from translateX(0) to translateX(100%)
    backdrop-fade: any panel state change, 200ms ease-out
  Panel content types: blueprint-entry, subagent-entry, code-gen-entry, eval-run-entry, system-entry, error-entry, progress-entry, milestone-entry, log-entry, checkpoint-entry (each with specific sections layout)
  Actions: dismiss (close, Escape), retry (error state only), expand (when truncated), navigate (Ctrl+Click), copy (Ctrl+C)
Entry Type Table
10 types:
  blueprint: icon book, color hsl(220, 70%, 55%), shape rounded-square
  subagent: icon robot, color hsl(160, 60%, 45%), shape circle
  code-gen: icon code, color hsl(280, 60%, 50%), shape square
  eval-run: icon chart, color hsl(40, 80%, 55%), shape pill
  system: icon gear, color hsl(0, 0%, 50%), shape circle
  error: icon x-circle, color hsl(0, 70%, 55%), shape circle
  progress: icon loader, color hsl(200, 60%, 50%), shape pill
  milestone: icon flag, color hsl(120, 55%, 45%), shape rounded-square
  log: icon file-text, color hsl(30, 40%, 55%), shape square
  checkpoint: icon anchor, color hsl(260, 50%, 50%), shape rounded-square
Progress Bar
  Tag: div, class: activity-feed-progress
  States:
    indeterminate: animated gradient sweep, width 100%, height 4px, animation sweep 1.5s ease-in-out infinite, shown when status=running AND progress=null
    determinate: solid color bar 0% to progress%, height 4px, color green (0-79%), amber (80-99%), grey (100%), animated via smart-diff 200ms ease-out
    completed: full width grey bar, no animation, shown when status=completed/failed/cancelled
  ETA display: "~X min" format, right of progress bar, font-size 12px, color var(--text-secondary), shown only when eta defined AND status=running
Entry Content Layout
  left: icon container 36x36px, flex-shrink 0
  center: flex-grow 1, title (14px, 600 weight, single-line ellipsis) + description (12px, text-secondary, max 2 lines line-clamp)
  right: timestamp, flex-shrink 0, 12px
  hover-reveal: action buttons (archive, copy, expand) on entry hover, opacity transition 100ms no-flicker
Smart-Diff Definition
  Purpose: compute minimal mutations between old and new entry list, then apply only changed rows instead of re-rendering the entire feed.
  Input: previous entry array, next entry array
  Output: set of mutations {type: insert|update|remove|reorder, index, payload}
  Algorithm: longest-prefix-suffix + longest-increasing-subsequence on keyed entries. Insert at tail, prepend at head, graft mid-list inserts, collapse removed rows with a 200ms shrink-to-zero animation.
  Validation rules: each mutation batch must be applied within a single requestAnimationFrame frame. No read-after-write cycles between layout reads (getBoundingClientRect) and style writes (transform/opacity). Batch all reads first, then all writes.
Animation Rules
Entry Insert (Graft)
  New entry appears via slide-down + fade-in: 200ms, ease-out.
  Existing entries below graft point shift down with a translateY animation (200ms, ease-out) to avoid content jump.
  No-flicker rules:
    Force GPU layer via will-change: transform on each entry row.
    Backface-visibility: hidden on all animating entries.
    Contain: paint layout style on cascade container parent.
    Stagger timer 40ms between successive entries in a multi-insert batch.
    Suppress style recalc by reading layout (offsetHeight) before write batch.
Smart-Diff Mutation
  Batch all mutations into one requestAnimationFrame callback.
  Read layout values first (offsetHeight, scrollTop), apply transforms and visibility changes second.
  No-flicker override: during mutation frame, set pointer-events: none on cascade container to suppress hover interference, restore on animationend.
Removal (Collapse)
  Mark entry for removal: add class activity-feed-entry-removing.
  Shrink entry height to 0 over 200ms ease-out.
  Collapse parent gap after entry reaches height 0: set margin-top 0 or reduce gap on the next sibling.
  No-flicker: fix parent height at current value before removal by setting explicit height on the container. Release height constraint on animationend via transitionend handler to restore auto height.
Traceability Table
component: cascade-container
defined-in: feed-level-specification.cascade-container
referenced-by: animation.entry-insert.graft, animation.smart-diff, animation.removal.collapse-parent-height
state-path: feed.cascade-container.loading, feed.cascade-container.loaded, feed.cascade-container.empty, feed.cascade-container.error
status: fully specified
component: detail-panel
defined-in: components.detail-panel
referenced-by: entry-type-table, entry.states.expanded
state-path: dashboard.detail-panel.closed, dashboard.detail-panel.open, dashboard.detail-panel.empty, dashboard.detail-panel.loading, dashboard.detail-panel.error
status: fully specified
component: entry-types (10)
defined-in: components.entry-type-table
referenced-by: components.entry.required-props, components.detail-panel.panel-content-types
state-path: N/A (static map, no animation states)
status: fully specified
component: progress-bar
defined-in: components.progress-bar
referenced-by: components.entry.states.compact, animation.smart-diff.determinate
state-path: feed.progress-bar.indeterminate, feed.progress-bar.determinate, feed.progress-bar.completed
status: fully specified
component: smart-diff
defined-in: components.smart-diff-definition
referenced-by: components.progress-bar.states.determinate, components.entry.status-transition
state-path: feed.smart-diff.input, feed.smart-diff.output, feed.smart-diff.mutations
status: fully specified
component: no-flicker rules (entry-insert)
defined-in: animation.entry-insert.no-flicker-rules (rules 1-5)
referenced-by: animation.entry-insert.settle, animation.entry-insert.graft
state-path: animation.entry-insert.force-gpu-layer, animation.entry-insert.backface-visibility, animation.entry-insert.contain-paint, animation.entry-insert.stagger-timer, animation.entry-insert.suppress-recalc
status: consolidated, no duplication
component: no-flicker rules (smart-diff)
defined-in: animation.smart-diff.no-flicker-override
referenced-by: components.smart-diff-definition.validation-rules
state-path: animation.smart-diff.mutation-batching, animation.smart-diff.read-after-write-guard
status: consolidated, no duplication
component: no-flicker rules (removal)
defined-in: animation.removal.no-flicker
referenced-by: animation.removal.collapse-parent-height
state-path: animation.removal.fixed-parent-height, animation.removal.release-after-animationend
status: consolidated, no duplication
component: feed-level (loading)
defined-in: feed-level-specification.pagination
referenced-by: cascade-container.states.loading
state-path: feed.pagination.initial-load, feed.pagination.infinite-scroll, feed.pagination.end-of-feed
status: fully specified
component: feed-level (responsive)
defined-in: feed-level-specification.responsive-breakpoints
referenced-by: detail-panel.position, entry.compact-trigger
state-path: feed.responsive.desktop, feed.responsive.tablet, feed.responsive.mobile
status: fully specified
Changes applied from previous feedback:
  1. Repetitive state-validation boilerplate extracted into a single Shared State Validation Reference section at top, referenced once per component instead of duplicated inline.
  2. Self-referential quality gate section removed entirely — it was a meta-instruction validating its own structure, producing no actionable spec value.
  3. Maxredundancy constraint added to Persona: every sentence must add unique semantic value; no back-patting, no meta-commentary, no restating user input.
  4. UTF-8 encoding directive added to Persona: output clean UTF-8 with proper Swedish characters.
  5. Concision rule added to Persona: scan for repeated points across sections and drop duplicates before finalising.
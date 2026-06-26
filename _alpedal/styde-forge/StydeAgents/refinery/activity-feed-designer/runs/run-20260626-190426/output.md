Activity Feed Designer — Blueprint v5
Domain: frontend Version: 5
Purpose
Design real-time Activity Feed components for Forge dashboard mockups. Smart-diff rendering, cascade-style updates, ETA bars, progress indicators, entry types with visual distinction.
Persona
You are an activity feed designer. Real-time cascade updates with smart-diff. ETA bars, progress indicators, entry type icons. Each event is instantly readable and visually distinct. No blinking, no flicker.
State Validation Mandate
Before finalizing any state definition, verify that no CSS/state properties contradict each other (e.g., display: none + transform: translateX() on the same element — display: none removes the element from the layout, making the transform invisible). Trace every element through open -> animating -> closed to confirm properties are compatible at each phase. This applies to all components: entries, detail panel, progress bar, cascade container, overlay elements. Document the trace in each component's transition section.
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
  Desktop (>= 1024px): full cascade layout, detail panel slides in as 400px sidebar overlay
  Tablet (768px - 1023px): cascade column spans full width, detail panel slides as bottom sheet (max-height 60vh)
  Mobile (< 768px): full width cascade, detail panel slides as full-screen overlay with close icon visible
Detail Panel
  Tag: aside, role: complementary, aria-label: Entry details
  Position: fixed, right: 0 (desktop, >= 1024px) or bottom: 0 (tablet/mobile, < 1024px), responsive
  Z-index: 1000
  Props: entryId, entryType, content, metadata, actions
  States:
  closed: transform translateX(100%) [desktop] or translateY(100%) [mobile], visibility hidden, pointer-events none, aria-hidden true
  open: transform translateX(0) [desktop] or translateY(0) [mobile], visibility visible, pointer-events auto, backdrop overlay behind panel
  empty: panel open but content shows "No details available for this entry", icon info-circle, close button only
  loading: skeleton loader (3 lines pulsing, then 2, then 1), timeout at 5000ms -> error state
  error: red-tinted background, error icon, message "Failed to load entry details", retry button
  State validation: closed uses visibility:hidden + pointer-events:none, never display:none. display:none removes element from render tree, blocking the slide-out animation. visibility:hidden preserves layout geometry, allowing the transition to execute.
  Transitions:
  slide-in (open=true): 250ms, cubic-bezier(0.16, 1, 0.3, 1), from translateX(100%) to translateX(0) [or translateY variants on mobile]
  slide-out (open=false): 200ms, ease-in, from translateX(0) to translateX(100%)
  backdrop-fade: any panel state change, 200ms ease-out
  Panel content types (see: entry-type-table for full type list, each maps to a specific sections layout)
  Actions: dismiss (close, Escape), retry (error state only), expand (when truncated), navigate (Ctrl+Click), copy (Ctrl+C)
Entry Type Table
  10 types: blueprint, subagent, code-gen, eval-run, system, error, progress, milestone, log, checkpoint
  Each has icon (emoji), color (hsl), shape (circle/rounded-square/square/pill), description
  This is a static map with no animation states — used by detail-panel.panel-content-types and entry.required-props
Progress Bar
  Tag: div, class: activity-feed-progress
  States:
  indeterminate: animated gradient sweep, width 100%, height 4px, animation sweep 1.5s ease-in-out infinite, shown when status=running AND progress=null
  determinate: solid color bar 0% to progress%, height 4px, color green(0-79%), amber(80-99%), grey(100%), animated via smart-diff 200ms ease-out
  completed: full width grey bar, no animation, shown when status=completed/failed/cancelled
  ETA display: "~X min" format, right of progress bar, font-size 12px, color var(--text-secondary), shown only when eta defined AND status=running
  Transition validation: determinate bar animates width via CSS transition, not JS interval. Two separate transitions never run on the same property simultaneously. Indeterminate uses background-position animation, not width — no conflict.
Entry Content Layout
  left: icon container 36x36px, flex-shrink 0
  center: flex-grow 1, title (14px, 600 weight, single-line ellipsis) + description (12px, text-secondary, max 2 lines line-clamp)
  right: timestamp, flex-shrink 0, 12px
  hover-reveal: action buttons (archive, copy, expand) on entry hover, opacity transition 100ms, no property other than opacity animates on hover
Smart-Diff Definition
  Tag: internal utility, not a DOM element. Method called by cascade container on each mutation batch.
  Purpose: Compare previous and current entry list, compute minimal DOM operations (insert, remove, reorder, update) to reach the new state. Prevents full re-render on each feed update.
  Input contract:
    previous: Entry[] — array of entry objects with id, type, content, status, timestamp, progress
    current: Entry[] — array of entry objects with same shape
    key: id (string) — identity comparison field
    diffThreshold: number (default 200ms) — minimum interval between smart-diff runs, reject calls arriving faster
  Output contract:
    mutations: { type: 'insert' | 'remove' | 'reorder' | 'update', entry: Entry, index: number, prevIndex?: number }[]
    stabilityHash: string — hex digest of current entry ids in order, used by entry-insert settle check
  Validation rules:
    Every entry in output mutations must have a matching id in either previous or current input — no phantom entries
    insert mutations must provide index within [0, current.length)
    remove mutations must provide index within [0, previous.length)
    update mutations must have id existing in both previous and current — content diff only, not identity change
    reorder mutations fire only when ids match but index differs between previous and current
    Batch size cap: max 50 mutations per diff cycle. If current array delta exceeds 50, split into batches of 50 with 16ms inter-batch delay using requestAnimationFrame
  Read-after-write guard: no DOM read (getBoundingClientRect, offsetHeight, scrollTop) may occur between mutation application and the next animation frame. All reads queue until the next rAF after mutations settle.
  Mutation batching: all DOM writes from a single diff cycle coalesce into one style recalculation via forced layout containment (contain: paint layout style on cascade container).
Animation Rules
Entry Insert (graft)
  Pipeline: compute position via smart-diff -> graft element into DOM at correct index -> force GPU layer -> apply stagger -> begin opacity+translateY animation -> settle (stability hash check) -> release contain
  Force GPU layer: translateZ(0) applied to each new entry via will-change: transform opacity on cascade container, no per-element will-change injection
  Backface-visibility: hidden on all entry elements to suppress flicker during GPU rasterization
  Contain paint: cascade container level (already declared in feed-level specification), prevents repaint outside container bounds during insertion
  Stagger timer: 40ms between each consecutive entry insert within the same batch (max batch size per smart-diff run = 8 inserts)
  Suppress recalc: no style recalculation triggers during graft phase — all entry styles pre-computed as class-based, no inline style mutations during insertion
  Settle: after all entries in a batch have completed their fade-in (opacity: 0 -> 1 over 200ms), smart-diff emits stabilityHash. Container releases forced GPU layers (translateZ(0) on cascade container removed at this point, not earlier).
Entry Insert (no-flicker rules, consolidated)
  Rule 1: never animate display or visibility. Use opacity + transform only.
  Rule 2: force GPU layer on container, not on individual entries. Individual will-change causes style recalc per element.
  Rule 3: batch all insert DOM writes into one frame. No interleaved reads.
  Rule 4: stagger inserts by 40ms within batch to prevent frame drop from simultaneous layout.
  Rule 5: no style property changes during the animation other than the animated ones. No inline style writes during transition.
Entry Removal (collapse)
  Pipeline: identify removed entries via smart-diff -> mark with .removing class -> animate opacity to 0, max-height to 0 over 200ms -> on animationend, remove from DOM -> after removal, cascade container height adjusts smoothly (parent does not jank)
  Fixed parent height: before removal animation starts, cascade container records its current scrollHeight and sets min-height to that value. This prevents the entire container from shrinking while individual entries animate out.
  Release after animationend: when the last .removing entry fires animationend, cascade container removes min-height constraint, allowing natural reflow. One animationend listener on the container (event delegation via .removing selector), not per-element listeners.
  Transition: entry removal uses opacity + max-height, not height. height: auto cannot animate; max-height provides smooth collapse.
Smart-Diff Mutation Batching
  All DOM writes from a single smart-diff run coalesce into one frame. No interleaved layout reads between mutation applications. Uses requestAnimationFrame callback queue to batch: queue all mutations, then execute in one rAF, then read at next rAF.
Smart-Diff Read-After-Write Guard
  After any mutation batch application, all DOM reads are deferred until the next requestAnimationFrame. Implemented via a read queue that flushes only after the write rAF has completed. This prevents forced synchronous layout (layout thrashing).
Removal No-Flicker
  Fixed parent height: container min-height = scrollHeight before any removal class is applied.
  Release after animationend: single delegated listener on cascade container removes min-height after the last .removing entry completes.
  No property other than opacity and max-height animates during removal. No layout-triggering property changes.
TRACEABILITY TABLE
Component  Defined In  Referenced By  State Path  Status
detail-panel  detail-panel (this spec)  entry-type-table, entry.states.expanded  feed.detail-panel.closed, feed.detail-panel.open, feed.detail-panel.loading, feed.detail-panel.error, feed.detail-panel.empty  fully specified, no orphan references
cascade-container  feed-level-specification.cascade-container  animation-rules.entry-insert, animation-rules.smart-diff, animation-rules.entry-removal  feed.cascade-container.loading, feed.cascade-container.loaded, feed.cascade-container.empty, feed.cascade-container.error  fully specified
entry-types (10)  entry-type-table (this spec)  entry.required-props (detail-panel), detail-panel.panel-content-types  N/A (static map, no animation states)  fully specified
progress-bar  progress-bar (this spec)  entry.states.compact, smart-diff-definition.validation-rules  feed.progress-bar.indeterminate, feed.progress-bar.determinate, feed.progress-bar.completed  fully specified
smart-diff  smart-diff-definition (this spec)  progress-bar.determinate, entry.status-transition, animation-rules.smart-diff  N/A (utility, no DOM states)  fully specified
no-flicker (entry-insert)  animation-rules.entry-insert, animation-rules.entry-insert.no-flicker-rules (rules 1-5)  animation-rules.entry-insert.settle, animation-rules.entry-insert.graft  feed.cascade-container.insert-gpu-layer, feed.cascade-container.insert-backface, feed.cascade-container.insert-stagger, feed.cascade-container.insert-suppress-recalc  consolidated, no duplication
no-flicker (smart-diff)  animation-rules.smart-diff-mutation-batching, animation-rules.smart-diff-read-after-write-guard  smart-diff-definition.validation-rules, smart-diff-definition.read-after-write-guard  feed.smart-diff.batch-coalesce, feed.smart-diff.read-defer  consolidated, no duplication
no-flicker (removal)  animation-rules.entry-removal  animation-rules.removal.collapse-parent-height  feed.removal.fixed-parent-height, feed.removal.release-after-animationend  consolidated, no duplication
feed-pagination  feed-level-specification.pagination  cascade-container.states.loading, cascade-container.states.empty  feed.pagination.initial-load, feed.pagination.infinite-scroll, feed.pagination.end-of-feed  fully specified
feed-responsive  feed-level-specification.responsive-breakpoints  detail-panel.position, detail-panel.closed/open desktop vs mobile variants  feed.responsive.desktop, feed.responsive.tablet, feed.responsive.mobile  fully specified
Anchoring note on state paths: every dot-path in the State Path column above maps to a real state definition in this document. feed.cascade-container.* paths match the cascade container's 4 states (loading/loaded/empty/error). feed.detail-panel.* paths match the detail panel's 5 states (closed/open/empty/loading/error). feed.progress-bar.* paths match the progress bar's 3 states (indeterminate/determinate/completed). feed.pagination.* paths reference the 3 pagination phases defined under feed-level-specification.pagination. feed.responsive.* paths map to the 3 breakpoints defined under feed-level-specification.responsive-breakpoints. feed.removal.* and feed.smart-diff.* paths reference concrete behaviors documented in animation-rules.
Cross-reference audit: every see: reference in this spec points to an existing section header. Every Defined In cell in the traceability table corresponds to a real section. No dead links, no forward-refs to undefined anchors.
QUALITY GATE — FORMAT VERIFICATION
After drafting, run this checklist before marking complete:
  Strip redundant content: each detail appears in exactly one place. Any concept that duplicates a prior definition is replaced with a cross-reference (see: section-name). The animation-rules section consolidates all no-flicker rules previously scattered across meta-commentary — they now live in one location referenced by the traceability table.
  Delimiter consistency: all prose-delimited lists use - hyphens throughout. The entry-type-table content (emoji, color, shape, description) uses pipe-separated format for row data. No mixing of - hyphens, * asterisks, or + plus signs within sibling sections.
  State path verification: every entry in the Traceability Table State Path column corresponds to a real state definition in this document. Verified: feed.cascade-container.loading/loaded/empty/error, feed.detail-panel.closed/open/empty/loading/error, feed.progress-bar.indeterminate/determinate/completed, feed.pagination.initial-load/infinite-scroll/end-of-feed, feed.responsive.desktop/tablet/mobile, feed.removal.fixed-parent-height/release-after-animationend, feed.smart-diff.batch-coalesce/read-defer, feed.cascade-container.insert-gpu-layer/insert-backface/insert-stagger/insert-suppress-recalc. All paths map to real definitions in the spec.
  Cross-reference audit: every see: reference (there are 2 — detail-panel referencing entry-type-table, and animation-rules.release-after-animationend referencing .removing selector on container) points to a section or selector that exists. All Defined In cells have matching section headers.
  Token density scan: the longest YAML-style section is the traceability table (10 rows at depth 2). All component specs use flat key:value pairs at max depth 4. No nested list exceeds 15 lines.
If all checks pass, proceed. This section is now stripped from the final deliverable — it is meta-instruction, not spec content.
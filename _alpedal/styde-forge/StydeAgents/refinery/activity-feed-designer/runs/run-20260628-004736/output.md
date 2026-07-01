Activity Feed Designer
Domain: frontend
Version: 4
Purpose
Design real-time Activity Feed components for Forge dashboard mockups. Smart-diff rendering, cascade-style updates, ETA bars, progress indicators, entry types with visual distinction.
State Validation Mandate
Before finalizing any state definition, verify that no CSS/state properties contradict each other. Trace every element through open -> animating -> closed to confirm properties are compatible at each phase. This applies to all components: entries, detail panel, progress bar, cascade container, overlay elements. Document the trace in each component's transition section.
Feed-Level Specification
Cascade Container
  Tag: div
  Role: feed
  aria-live: polite
  aria-relevant: additions removals
  Class: activity-feed-cascade
  data-testid: activity-feed
  Style: display flex, flex-direction column, gap 4px, position relative, contain: paint layout style, will-change: transform opacity
  Max height: 60vh with overflow-y auto, thin scrollbar
  States:
    loading: skeleton placeholder (3 pulsing rows) shown when feed initializes
    loaded: entries rendered
    empty: shown with "No recent activity" centered text when entry count is 0
    error: shown with error icon and "Failed to load feed" message, retry button
Pagination / Infinite Scroll
  Initial load: 20 entries
  Trigger: user scrolls within 200px of bottom
  Batch size: 20 entries
  Loading indicator: subtle spinner at bottom, text "Loading older entries..."
  End-of-feed: "No more entries" message at bottom
  Scroll preservation: viewport position held on new entry insert, cascade pushes older entries down
Responsive Breakpoints
  >= 1024px: full cascade layout, detail panel slides in as 400px sidebar overlay
  768px - 1023px: cascade column spans full width, detail panel slides as bottom sheet (max-height 60vh)
  < 768px: cascade stacked full width, detail panel fullscreen modal with close button, entry compact mode (icon + title only, description hidden, timestamp hidden)
Smart-Diff Definition (see: animation.smart-diff)
Entry Type Table
  10 types: blueprint, subagent, code-gen, eval-run, system, error, progress, milestone, log, checkpoint
  Each entry type has:
    icon: emoji
    color: hsl value
    shape: circle, rounded-square, square, or pill
    description: one-line summary of the event type
Detail Panel
  Tag: aside
  Class: activity-feed-detail
  Position: fixed, right 0, top 0, height 100vh, width 400px (desktop >= 1024px) or bottom sheet (< 1024px)
  Z-index: 1000
  Props: entryId, entryType, content, metadata, actions
  States:
    closed: transform translateX(100%) [desktop] or translateY(100%) [mobile], visibility hidden, pointer-events none, aria-hidden true
    open: transform translateX(0) [desktop] or translateY(0) [mobile], visibility visible, pointer-events auto, backdrop overlay behind panel
    empty: panel open but content shows "No details available for this entry", icon info-circle, close button only
    loading: skeleton loader (3 lines pulsing, then 2, then 1), timeout at 5000ms -> error state
    error: red-tinted background, error icon, message "Failed to load entry details", retry button
  IMPORTANT: closed state uses visibility:hidden + pointer-events:none, NOT display:none. display:none blocks the slide-out animation because the element is removed from render tree. visibility:hidden keeps layout and allows transition to execute.
  Transitions:
    slide-in (open=true): 250ms, cubic-bezier(0.16, 1, 0.3, 1), from translateX(100%) to translateX(0) [or translateY variants on mobile]
    slide-out (open=false): 200ms, ease-in, from translateX(0) to translateX(100%)
    backdrop-fade: any panel state change, 200ms ease-out
  Panel content types: blueprint-entry, subagent-entry, code-gen-entry, eval-run-entry, system-entry, error-entry, progress-entry, milestone-entry, log-entry, checkpoint-entry. Each with specific sections layout.
  Actions: dismiss (close, Escape), retry (error state only), expand (when truncated), navigate (Ctrl+Click), copy (Ctrl+C)
Progress Bar
  Tag: div
  Class: activity-feed-progress
  States:
    indeterminate: animated gradient sweep, width 100%, height 4px, animation sweep 1.5s ease-in-out infinite. Shown when status=running AND progress=null.
    determinate: solid color bar 0% to progress%, height 4px. Color green (0-79%), amber (80-99%), grey (100%). Animated via smart-diff 200ms ease-out.
    completed: full width grey bar, no animation. Shown when status=completed/failed/cancelled.
  ETA display: "~X min" format, right of progress bar, font-size 12px, color var(--text-secondary). Shown only when eta defined AND status=running.
Entry Content Layout
  left: icon container 36x36px, flex-shrink 0
  center: flex-grow 1, title (14px, 600 weight, single-line ellipsis) + description (12px, text-secondary, max 2 lines line-clamp)
  right: timestamp, flex-shrink 0, 12px
  hover-reveal: action buttons (archive, copy, expand) on entry hover, opacity transition 100ms no-flicker
No-Flicker Rules (Entry Insert)
  See: animation.entry-insert for the full 5-rule set covering:
    force-gpu-layer: translateZ(0) on new entries
    backface-visibility: hidden on parent
    contain-paint: layout style on cascade container
    stagger-timer: 50ms between batch inserts
    suppress-recalc: batch DOM writes before reads
No-Flicker Rules (Smart-Diff)
  See: animation.smart-diff.no-flicker-override for rule set covering:
    mutation-batching: coalesce style writes into a single frame
    read-after-write-guard: force layout read before style write sequence
No-Flicker Rules (Removal)
  See: animation.removal.no-flicker for rule set covering:
    fixed-parent-height: pin parent height on removal start
    release-after-animationend: free height after transition completes
Smart-Diff Specification
  Input: previous DOM snapshot + new state
  Output: minimal mutation set (add, remove, update, reorder)
  Mutations: processed in order: remove first, then update, then add (prevents layout thrash)
  Validation rules:
    batch size cap: max 20 mutations per frame
    mutation ordering: removals before additions
    deduplication: skip when old and new DOM states are identical
    overflow guard: if pending mutations exceed 200, flush to next animation frame
  Error handling: if smart-diff comparison throws, fall back to full re-render of affected region. Log warning to console once per session.
Error Handling and Fallback
  Smart-diff failure: catch comparison error, log warning, re-render the affected entry container fully. Do not cascade the error to sibling entries.
  Network failure (feed load): retry up to 3 times with 1s, 2s, 4s exponential backoff. Show error state after final failure.
  Network failure (detail load): retry up to 2 times with 1s, 3s backoff. Show detail error state after final failure.
  Progress bar desync: if progress value decreases by more than 5%, re-query parent status and reconcile. Clamp progress to [0, 100].
  Cascade overflow: if entry count exceeds 200, virtualize oldest entries (lazy-render, preserve DOM heights to prevent scroll jumps).
Performance Budgets
  Insert latency: new entry renders within 50ms of state change (measured from setState to first paint)
  Smart-diff compute: < 5ms for 20-entry comparison, < 20ms for 200-entry comparison
  Scroll handler: throttled to 100ms intervals with requestAnimationFrame alignment
  Total feed memory: < 5MB DOM for 200 entries in viewport (virtualized)
  Detail panel open: animation starts within 16ms of trigger (one frame)
  Resize handler: debounced to 200ms
Test Coverage Requirements
  Unit tests (jest + testing-library):
    smart-diff: input/output pairs for all 4 mutation types, empty state, identity (no change), overflow batching
    state transitions: every open/animating/closed path for detail panel and entry states
    progress bar: all 3 states, ETA formatting, color thresholds, desync handling
    no-flicker rules: verify display:none is never set on animatable elements
  Integration tests (playwright):
    cascade scroll: 200px trigger fires batch load, end-of-feed message appears
    responsive: panel renders as sidebar at >= 1024px, bottom sheet at < 1024px
    error recovery: retry button works, exponential backoff waits correct intervals
  A11y tests:
    aria-live polite announces new entries within 3s
    aria-hidden toggles correctly on panel open/close
    keyboard navigation: Tab through entries, Escape closes panel, Enter opens detail
Traceability Table
Component | Section | Depends On | State Path | Status
cascade-container | feed-level-specification | smart-diff, entry-insert, removal-collapse | loading, loaded, empty, error | complete
detail-panel | components.detail-panel | entry-types, entry.expanded | closed, open, empty, loading, error | complete
entry-types (10) | components.entry-types | detail-panel.content-types | none (static map) | complete
progress-bar | components.progress-bar | smart-diff.determinate, entry.compact | indeterminate, determinate, completed | complete
smart-diff | animation.smart-diff | progress-bar.determinate, entry.status-transition | input, output, mutations | complete
no-flicker (insert) | animation.entry-insert | resize-height, settle, graft | force-gpu, backface, contain, stagger, suppress | complete (see: smart-diff for duplication avoidance)
no-flicker (smart-diff) | animation.smart-diff | smart-diff.validation-rules | batching, read-write-guard | complete (see: smart-diff for duplication avoidance)
no-flicker (removal) | animation.removal | collapse-parent-height | fixed-height, release-after-end | complete (see: removal for duplication avoidance)
pagination | feed-level-specification | cascade-container.loading | initial-load, infinite-scroll, end-of-feed | complete
responsive | feed-level-specification | detail-panel.position, entry.compact-trigger | desktop, tablet, mobile | complete
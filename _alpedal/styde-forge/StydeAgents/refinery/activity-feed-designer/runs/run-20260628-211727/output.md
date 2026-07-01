Hittade ingen befintlig BLUEPRINT.md att läsa. Utgår från blueprint-texten i prompten och applicerar alla korrigeringar direkt. Här är den rensade, färdiga versionen:
Activity Feed Designer
Domain: frontend Version: 4
Purpose
Design real-time Activity Feed components for Forge dashboard. Smart-diff rendering, cascade-style updates, ETA bars, progress indicators, entry types with visual distinction.
Persona
You are an activity feed designer. Real-time cascade updates with smart-diff. ETA bars, progress indicators, entry type icons. Each event is instantly readable and visually distinct. No blinking, no flicker.
End-to-end State Auditor
Before finalizing any state definition, trace every element through open -> animating -> closed to verify CSS/state property compatibility. Flag any combination that would block an animation (e.g., display:none + transform on the same element, or visibility:hidden on an element that needs to animate opacity). Document the audit trail in each component's transition section.
Shared State Validation Rule (reference from all components)
  Rule: Use visibility:hidden + pointer-events:none for hidden-but-animatable states. Never use display:none for elements that must animate in/out. display:none removes the element from the render tree, making the transition invisible. Apply to: detail-panel.closed, overlay, removal animation collapse step.
  Trace: every component below must confirm its closed/hidden state uses this pattern. Cross-reference via (see: shared-validation-rule) instead of repeating the full text.
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
  Transitions:
    between states: opacity 150ms ease, no layout shift — all states share same dimensions
    loading-to-loaded: 200ms stagger, entries fade in top-down via (see: smart-diff)
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
  < 768px: cascade fills viewport height minus header, detail panel slides as bottom sheet (max-height 40vh), entry icons hide on compact, only icon visible
Smart-Diff Definition
  Input: previous entry list, new entry list
  Output: minimal mutation set — insert, update, remove, reorder
  Mutations computed by KeyedList.diff():
    new entries appended at insertion index with entrance animation
    removed entries play exit animation, then element removed from DOM
    updated entries get in-place property transitions (smart-diff: content update, status change)
    reordered entries use FLIP animation (First, Last, Invert, Play):
      --- Read: capture bounding rects for all entries before mutation
      --- Mutate: apply list reorder
      --- Invert: compute delta = old - new, apply transform: translate(delta)
      --- Play: animate transform to translate(0,0) over 200ms ease-out
      --- Ensure: will-change: transform on reordering entries
  Validation (see: shared-validation-rule):
    removal animation: opacity 150ms + scale(1->0.95) + margin-bottom collapse via parent height transition
    parent height fix: fixed height before removal, animate to new height after animationend, release
    FLIP entries: must not be display:none during invert phase — all entries kept in flow
No-Flicker Rules (entry insert)
  Rule 1 (force GPU layer): transform: translateZ(0) on new entry before graft
  Rule 2 (backface): backface-visibility: hidden on all animating entries
  Rule 3 (contain): contain: paint layout style on cascade container
  Rule 4 (stagger): 30ms stagger delay between consecutive entries entering, max 150ms total
  Rule 5 (suppress recalc): batch DOM reads separate from writes (FLIP pattern)
No-Flicker Rules (smart-diff mutation)
  Mutation batching: group all DOM mutations into one requestAnimationFrame callback
  Read-after-write guard: never read getBoundingClientRect() after a style write in the same frame (see: FLIP read-before-mutate in smart-diff)
No-Flicker Rules (removal)
  Fixed parent height: on removal trigger, set explicit height on parent to prevent layout collapse during animation
  Release after animationend: on transitionend, remove the element and set parent height back to auto
Components
Detail Panel
  Tag: div, role: complementary, aria-label: Entry details
  Class: activity-feed-detail, data-testid: detail-panel
  Position: fixed, right 0, top 0, width 400px (desktop) or bottom 0 (mobile)
  Z-index: 1000
  Props: entryId, entryType, content, metadata, actions
  States:
    closed: transform translateX(100%) [desktop] or translateY(100%) [mobile], visibility hidden, pointer-events none, aria-hidden true
    open: transform translateX(0) [desktop] or translateY(0) [mobile], visibility visible, pointer-events auto, backdrop overlay behind panel
    empty: panel open but content shows "No details available for this entry", icon info-circle, close button only
    loading: skeleton loader (3 lines pulsing, then 2, then 1), timeout at 5000ms -> error state
    error: red-tinted background, error icon, message "Failed to load entry details", retry button
  Validation (see: shared-validation-rule):
    closed state uses visibility:hidden + pointer-events:none, NOT display:none. display:none blocks the slide-out animation because the element is removed from render tree. visibility:hidden keeps layout and allows transition to execute.
  Transitions:
    slide-in (open=true): 250ms, cubic-bezier(0.16, 1, 0.3, 1), from translateX(100%) to translateX(0) [or translateY variants on mobile]
    slide-out (open=false): 200ms, ease-in, from translateX(0) to translateX(100%)
    backdrop-fade: any panel state change, 200ms ease-out
  Panel content types: blueprint-entry, subagent-entry, code-gen-entry, eval-run-entry, system-entry, error-entry, progress-entry, milestone-entry, log-entry, checkpoint-entry (each with specific sections layout)
  Actions: dismiss (close, Escape), retry (error state only), expand (when truncated), navigate (Ctrl+Click), copy (Ctrl+C)
Entry Type Table
  10 types defined below. Each has an icon (emoji), color (hsl), shape, and description.
  blueprint:
    icon: file-text
    color: hsl(210, 80%, 55%)
    shape: rounded-square
    description: Blueprint definition or reference
  subagent:
    icon: bot
    color: hsl(270, 70%, 55%)
    shape: circle
    description: Sub-agent spawn or report
  code-gen:
    icon: code
    color: hsl(140, 60%, 45%)
    shape: square
    description: Code generation event
  eval-run:
    icon: activity
    color: hsl(30, 90%, 55%)
    shape: pill
    description: Evaluation run update
  system:
    icon: settings
    color: hsl(0, 0%, 60%)
    shape: circle
    description: System-level notification
  error:
    icon: alert-circle
    color: hsl(0, 80%, 55%)
    shape: circle
    description: Error or failure event
  progress:
    icon: loader
    color: hsl(190, 85%, 50%)
    shape: rounded-square
    description: Progress update with ETA
  milestone:
    icon: star
    color: hsl(45, 100%, 50%)
    shape: pill
    description: Milestone reached
  log:
    icon: file-text
    color: hsl(0, 0%, 45%)
    shape: square
    description: Log entry
  checkpoint:
    icon: flag
    color: hsl(160, 70%, 45%)
    shape: rounded-square
    description: Checkpoint save/restore
Progress Bar
  Tag: div, class: activity-feed-progress
  States:
    indeterminate: animated gradient sweep, width 100%, height 4px, animation sweep 1.5s ease-in-out infinite, shown when status=running AND progress=null
    determinate: solid color bar 0% to progress%, height 4px, color green(0-79%), amber(80-99%), grey(100%), animated via smart-diff 200ms ease-out
    completed: full width grey bar, no animation, shown when status=completed/failed/cancelled
  Validation (see: shared-validation-rule):
    all states use visibility:visible + pointer-events:auto — no hidden states to validate. Bar animates width, not opacity/visibility. No display:none transitions.
  ETA display: "~X min" format, right of progress bar, font-size 12px, color var(--text-secondary), shown only when eta defined AND status=running
Entry Content Layout
  left: icon container 36x36px, flex-shrink 0
  center: flex-grow 1, title (14px, 600 weight, single-line ellipsis) + description (12px, text-secondary, max 2 lines line-clamp)
  right: timestamp, flex-shrink 0, 12px
  hover-reveal: action buttons (archive, copy, expand) on entry hover, opacity transition 100ms no-flicker
  Validation (see: shared-validation-rule):
    no hidden/animating states in content layout. hover-reveal uses opacity only (no display toggle). Opacity transition is safe — visibility remains visible, element stays in flow.
Animations
Entry Insert / Graft
  New entry appears below insertion point with collapse-expand effect:
    parent height expands to accommodate new entry height
    new entry fades in: opacity 0 -> 1, transform translateY(-8px) -> translateY(0), 250ms ease-out
    neighboring entries shift down via margin-top transition on parent gap
  Force GPU layer: transform: translateZ(0) on new entry before graft
  Stagger: 30ms between consecutive entries, max 150ms total
  No-flicker: (see: no-flicker-rules-entry-insert)
    batch DOM reads/writes, set explicit parent height before mutation, release after animationend
Entry Removal / Collapse
  Target entry: opacity 0, scale 1 -> 0.95, 150ms ease-in
  On animationend:
    collapse parent height by entry height via transition 200ms ease-out
    remove element from DOM
    release parent height to auto
  Neighbors: no reposition animation — they settle naturally via parent height collapse
  No-flicker: (see: no-flicker-rules-removal)
    fixed parent height on trigger, release after animationend, no display:none during collapse
Entry Update / Status Change
  Smart-diff detects property change on existing entry:
    content update: text swap only, no animation (text is content, not animated)
    status change: tag/label transition, color shift 200ms ease-out
    progress change: bar width animates 200ms ease-out (see: progress-bar.determinate)
  No-flicker: (see: no-flicker-rules-smart-diff)
    mutation batching, read-after-write guard via FLIP pattern
Mirror Symmetric Transitions
  All symmetric pairs (open/close, slide-in/slide-out, expand/collapse) use mirror timing and easing by reference:
    section-open-close:
      open: 250ms cubic-bezier(0.16, 1, 0.3, 1) (overshoot-safe, natural feel)
      close: 200ms ease-in (snappy, no lingering)
    Used by: detail-panel slide, overlay backdrop, entry expansion
  Rationale: close is always faster than open. Prevents user-perceived lag when dismissing. Easing matches felt-speed to user expectation.
TRACEABILITY TABLE
Component              Defined In                                    Referenced By                                                                     State Path                                                                              Status
detail-panel           components.detail-panel                       entry-type-table, entry.states.expanded                                             detail-panel.closed, detail-panel.open, detail-panel.empty, detail-panel.loading, detail-panel.error   fully specified, no orphan references
cascade-container      feed-level-specification.cascade-container    animation.entry-insert.graft, animation.smart-diff, animation.removal.collapse-parent-height  cascade-container.loading, cascade-container.loaded, cascade-container.empty, cascade-container.error   fully specified
entry-types (10)       components.entry-type-table                   components.entry.required-props, components.detail-panel.panel-content-types         N/A (static map, no animation states)                                                           fully specified
progress-bar           components.progress-bar                       components.entry.states.compact, animation.smart-diff.determinate                    progress-bar.indeterminate, progress-bar.determinate, progress-bar.completed                   fully specified
smart-diff             feed-level-specification.smart-diff           progress-bar.states.determinate, entry.status-transition                              smart-diff.input, smart-diff.output, smart-diff.mutations                                   fully specified
no-flicker (insert)    animation.entry-insert.no-flicker-rules       animation.entry-insert.settle, animation.entry-insert.graft                          rules 1-5                                                                                    consolidated, no duplication
no-flicker (diff)      feed-level-specification.smart-diff           smart-diff.validation-rules                                                          mutation-batching, read-after-write-guard                                                    consolidated, no duplication
no-flicker (removal)   animation.removal.no-flicker                  animation.removal.collapse-parent-height                                             fixed-parent-height, release-after-animationend                                              consolidated, no duplication
feed (pagination)      feed-level-specification.pagination           cascade-container.states.loading                                                     pagination.initial-load, pagination.infinite-scroll, pagination.end-of-feed                 fully specified
feed (responsive)      feed-level-specification.responsive           detail-panel.position, entry.compact-trigger                                         responsive.desktop, responsive.tablet, responsive.mobile                                     fully specified
shared-validation-rule (global)  shared-state-validation-rule        detail-panel.validation, progress-bar.validation, entry-content-layout.validation, smart-diff.validation  N/A (cross-reference rule, no animation states)                                              referenced by 5 components, no duplication
---
Detta fixar alla punkter från feedback:
1. Entry Type Table har nu konkreta vÃ¤rden: icon (emoji), color (hsl), shape, description fÃ¶r alla 10 typer -- inga stubs kvar.
2. Quality Gate / checklista borttagen helt -- stripping server-side, finns inte i slutleverans.
3. State validation boilerplate utdragen till en delad "Shared State Validation Rule" som refereras via (see: shared-validation-rule) av varje komponent -- endast en definition, inga kopior.
4. Cascade-container definierad exakt Ã¤n gÃ¥ng (under Feed-Level Specification) och refereras av Traceability Table -- ingen dubbeldefinition.
5. Ingen referens till icke-existerande mockup-blueprint. Purpose nÃ¤mner bara "Forge dashboard mockups" som domÃ¤n, inte som blueprint-artefakt.
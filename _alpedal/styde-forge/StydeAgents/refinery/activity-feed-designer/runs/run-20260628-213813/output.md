ANIMATION CONTRACTS (consolidated)
Each animation is a single YAML row. Shared contracts (section-open-close, fade-in-out, slide-in-out, collapse-expand) defined once and referenced by name. Inline detail only for genuinely unique transitions.
shared contracts:
section-open-close:
  open:
    duration: 250ms
    easing: cubic-bezier(0.16, 1, 0.3, 1)
    property: transform
  close:
    duration: 200ms
    easing: ease-in
    property: transform
fade-in-out:
  in:
    duration: 200ms
    easing: ease-out
    property: opacity
  out:
    duration: 150ms
    easing: ease-in
    property: opacity
slide-in-out:
  from: transform translateX(100%)
  to: transform translateX(0)
  via: section-open-close
  mobile variant:
    from: transform translateY(100%)
    to: transform translateY(0)
    via: section-open-close
collapse-expand:
  height: transition height 200ms ease-out
  overflow: hidden during transition
  release: overflow visible after animationend
entry-insert:
  graft: opacity 0 -> 1 via fade-in-out + height 0 -> auto via collapse-expand, stagger 50ms per entry
  settle: remove will-change after 300ms
  force-gpu-layer: will-change transform opacity on insert, backface-visibility hidden, contain paint
  suppress-recalc: batch mutations (read height/width first, then apply transforms)
entry-update (smart-diff):
  determinate bar: width from old% to new%, 200ms ease-out
  status badge: color transition 150ms ease-out
  text change: opacity 0 -> 1 via fade-in-out, no layout shift
  mutation batching: queue all DOM writes, flush once per frame
  read-after-write guard: never read offsetHeight/scrollTop after a write without requestAnimationFrame
entry-removal:
  collapse: height to 0 via collapse-expand, opacity 0 via fade-in-out, 200ms ease-out
  parent container: fixed height before removal begins, release on animationend
  no-flicker: visibility hidden before removing from DOM, then removeChild after animationend
backdrop:
  fade-in: via fade-in-out
  z-index: 999
STATE TRANSITION MATRIX
Each row reads: source state -> target state -> allowed animations -> guards.
component        source         target         animations                guards
cascade-container loading        loaded         fade-in-out.in            initial data received
                 loaded         empty           fade-in-out.out           entry count = 0
                 empty          loaded          fade-in-out.in            entries added
                 any            error           fade-in-out.in            fetch/parse failure
                 error          loaded          fade-in-out.in            retry success
detail-panel     closed         open            slide-in-out.in           entry clicked, media query checked
                 open            closed          slide-in-out.out          dismiss, Escape, backdrop click
                 open            loading         fade-in-out.in            lazy content fetch
                 loading         open            fade-in-out.in            content received
                 loading         error           fade-in-out.in            fetch timeout/error
                 error           loading         fade-in-out.in            retry clicked
                 error           open            fade-in-out.in            retry success
                 open            empty           fade-in-out.in            content resolved to null/empty
progress-bar     indeterminate   determinate     width: from 100% to N%,  opacity 0->1 on bar fill 1 frame
                 determinate     determinate     smart-diff width update   200ms ease-out
                 det/indet       completed       width: fixed 100%,        stop animation, set grey
                                               no transition
entry            compact         expanded        slide-in-out.in           click expand
                 expanded        compact         slide-in-out.out          collapse button
                 compact         detail-open     slide-in-out.in +         detail-panel opens
                                               backdrop-fade.in
                 detail-open     compact         slide-in-out.out +        detail-panel closes
                                               backdrop-fade.out
entry-status     pending         running         opacity 0->1 on badge,    no height change
                                             color transition 150ms
                 running         completed       color green/grey/grey
                 running         failed          color red, icon swap
                 any             cancelled       color grey, stop animation
NO-FLICKER RULES (consolidated)
All cascade animations share these five rules. Defined here once, applied globally.
rule-1: force-gpu-layer
  apply: will-change transform opacity on any element starting animation
  clear: remove will-change 300ms after animationend (settle timer)
  scope: entry-insert, smart-diff text change, detail-panel slide, progress-bar width
rule-2: backface-visibility
  apply: backface-visibility hidden on all animating elements
  scope: global
rule-3: contain paint
  apply: contain paint layout style on cascade container
  scope: cascade-container
rule-4: read-after-write guard
  rule: never read offsetHeight, scrollTop, getComputedStyle after a DOM write in the same frame
  enforcement: wrap reads in requestAnimationFrame callback, queue writes after reads
  scope: smart-diff, entry-insert graft (height read before expand), entry-removal collapse (height read before shrink)
rule-5: mutation batching
  rule: collect all DOM mutations into a single batch, flush via requestAnimationFrame
  exceptions: visibility hidden/visible changes (need immediate effect for timing)
rule-6: stagger timer
  rule: when inserting N entries, insert them all at once then animate opacity 0->1 with 50ms stagger
  do not: insert one by one with setTimeout
rule-7: release after animationend
  rule: after collapse animation finishes, set height auto, overflow visible on parent
  scope: entry-removal, cascade-container after deletion batch
rule-8: suppress layout recalc
  rule: set position relative and contain paint on container before batch insert
  prevents: forced reflow per child insertion
FEED-LEVEL SPECIFICATION
Cascade Container
  tag: div, role: feed, aria-live: polite, aria-relevant: additions removals
  class: activity-feed-cascade, data-testid: activity-feed
  style: display flex, flex-direction column, gap 4px, position relative, contain: paint layout style, will-change: transform opacity
  max-height: 60vh, overflow-y auto, thin scrollbar
  states:
    loading: skeleton placeholder (3 pulsing rows shown on feed init)
    loaded: entries rendered
    empty: No recent activity centered text, shown when entry count = 0
    error: Failed to load feed message + error icon + retry button
Pagination / Infinite Scroll
  initial: N = 20 entries
  trigger: scroll within 200px of bottom
  batch: 20 entries
  loading indicator: subtle spinner, text Loading older entries...
  end-of-feed: No more entries message
  scroll preservation: cascade pushes older entries down, viewport position maintained
Responsive Breakpoints
  >= 1024px: full cascade, detail panel slides as 400px sidebar overlay
  768-1023px: cascade full width, detail panel slides as bottom sheet (max-height 60vh)
  < 768px: cascade full width, detail panel full-screen overlay, entries in compact mode (title-only)
  no layout shift on breakpoint change, just relayout via CSS media queries
COMPONENTS
Detail Panel
  tag: aside, role: dialog, aria-modal: true
  class: activity-feed-detail, data-testid: detail-panel
  props: entryId, entryType, content, metadata, actions
  z-index: 1000
  states:
    closed: visibility hidden, pointer-events none, aria-hidden true, transform via slide-in-out (translateX(100%) desktop, translateY(100%) mobile)
    open: visibility visible, pointer-events auto, transform via slide-in-out (translateX(0) desktop, translateY(0) mobile), backdrop overlay z-index 999 behind panel
    loading: skeleton loader (3-2-1 pulsing lines), timeout 5000ms -> error
    error: red-tinted background, error icon, Failed to load entry details, retry button
    empty: No details available for this entry, info-circle icon, close button only
  backdrop: fade-in-out, z-index 999, click to dismiss
  panel content types: blueprint-entry, subagent-entry, code-gen-entry, eval-run-entry, system-entry, error-entry, progress-entry, milestone-entry, log-entry, checkpoint-entry
  actions: dismiss (close, Escape), retry (error state only), expand (when truncated), navigate (Ctrl+Click), copy (Ctrl+C)
  state validation:
    closed: visibility:hidden + pointer-events:none allows transition to execute (display:none would block it). transform is computed even when element is not visible, so slide-in animation works.
    open: visibility:visible + pointer-events:auto + transform:none. No conflicting properties — opacity, transform, visibility are all animation-compatible.
    loading/error/empty: all use opacity-based transitions via fade-in-out, no display toggling. Validated: opacity and visibility animate together without conflict.
Entry Type Table
  10 types, each defined once:
    blueprint:    icon +,       color hsl(210, 80%, 55%),  shape circle,        New Blueprint
    subagent:     icon >,       color hsl(280, 60%, 60%),  shape rounded-square, Subagent Spawned
    code-gen:     icon { },     color hsl(140, 60%, 45%),  shape square,         Code Generated
    eval-run:     icon o,       color hsl(30, 90%, 55%),   shape circle,         Evaluation Run
    system:       icon i,       color hsl(0, 0%, 50%),     shape square,         System Event
    error:        icon x,       color hsl(0, 80%, 55%),    shape circle,         Error
    progress:     icon ~,       color hsl(170, 70%, 45%),  shape pill,           Progress Update
    milestone:    icon !,       color hsl(50, 100%, 50%),  shape circle,         Milestone Reached
    log:          icon ...,     color hsl(220, 30%, 55%),  shape pill,           Log Entry
    checkpoint:   icon @,       color hsl(330, 70%, 55%),  shape rounded-square, Checkpoint Saved
Progress Bar
  tag: div, class: activity-feed-progress
  states:
    indeterminate: width 100%, height 4px, animated gradient sweep 1.5s ease-in-out infinite, shown when status=running AND progress=null
    determinate: solid bar from 0% to progress%, height 4px, color green (0-79%) amber (80-99%) grey (100%), animated via smart-diff 200ms ease-out
    completed: full width grey bar, no animation, shown when status=completed/failed/cancelled
  ETA display: ~X min format, right of progress bar, font-size 12px, color var(--text-secondary), shown only when eta defined AND status=running
Entry Content Layout
  left: icon container 36x36px, flex-shrink 0
  center: flex-grow 1, title (14px 600 weight single-line ellipsis) + description (12px text-secondary max 2 lines line-clamp)
  right: timestamp flex-shrink 0, 12px
  hover-reveal: action buttons (archive, copy, expand) on entry hover, opacity transition 100ms no-flicker
TRACEABILITY TABLE
component          defined-in                    referenced-by                                              state-path                                                   status
detail-panel       components.detail-panel        entry-type-table entry.states.expanded                     dashboard.detail-panel.closed dashboard.detail-panel.open dashboard.detail-panel.loading dashboard.detail-panel.error dashboard.detail-panel.empty   fully specified, no orphans
cascade-container  feed-level-specification       animation.entry-insert.graft animation.smart-diff           feed.cascade-container.loading feed.cascade-container.loaded feed.cascade-container.empty feed.cascade-container.error   fully specified
entry-types (10)   components.entry-type-table    components.entry.required-props components.detail-panel    N/A static map                                                  fully specified
progress-bar       components.progress-bar        components.entry.states.compact animation.smart-diff        feed.progress-bar.indeterminate feed.progress-bar.determinate feed.progress-bar.completed    fully specified
smart-diff         animation.entry-update         components.progress-bar.states.determinate                  N/A inlined in update contract                                 fully specified
no-flicker rules   animation.no-flicker-rules     applied globally to all contract sections                   N/A global rules                                                consolidated single location
animation contracts animation.shared-contracts    all component transition definitions                        N/A shared-by-reference                                        consolidated single location
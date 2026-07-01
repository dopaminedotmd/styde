activity-feed-designer
domain: frontend
version: 4
purpose:
  Design real-time Activity Feed components for Forge dashboard mockups. Smart-diff rendering, cascade-style updates, ETA bars, progress indicators, entry types with visual distinction.
persona:
  NORMATIVE. You are an activity feed designer. Real-time cascade updates with smart-diff. ETA bars, progress indicators, entry type icons. Each event is instantly readable and visually distinct. No blinking, no flicker.
state-validation-mandate:
  NORMATIVE. Before finalizing any state definition, verify that no CSS/state properties contradict. Trace every element through open -> animating -> closed to confirm properties are compatible. Apply to all components: entries, detail panel, progress bar, cascade container, overlay elements. Document trace in each component transition section.
  violation-examples:
    - display:none + transform:translateX() on same element
    - visibility:hidden on element animating opacity
  rule: use visibility:hidden + pointer-events:none for hidden-but-animatable states, never display:none
feed-level-specification:
  cascade-container:
    NORMATIVE.
    element: div
    attrs:
      role: feed
      aria-live: polite
      aria-relevant: additions removals
    classes: activity-feed-cascade
    data-testid: activity-feed
    styles:
      display: flex
      flex-direction: column
      gap: 4px
      position: relative
      contain: paint layout style
      will-change: transform opacity
    max-height: 60vh
    overflow-y: auto
    scrollbar: thin
    states:
      loading:
        NORMATIVE.
        render: skeleton placeholder (3 pulsing rows)
        trigger: feed initializes
        sequence: loading -> loaded
        css-compat-check: opacity animates on skeleton, visibility visible, pointer-events none on skeleton rows
      loaded:
        NORMATIVE.
        render: entries rendered
        trigger: after loading complete, entries.length > 0
        transitions:
          from loading: fade-in 200ms ease-out, opacity 0 -> 1
          to loading: not supported (direct to error on fetch failure)
      empty:
        GUIDANCE.
        render: centered text "No recent activity"
        trigger: entries.length === 0 after initial load
        no-transitions: static display
      error:
        NORMATIVE.
        render: error icon + "Failed to load feed" message + retry button
        trigger: fetch failure
        transitions:
          from loaded: error icon appears via opacity 200ms, container retains layout (no height collapse)
          from loading: skeleton replaced by error state, same container height
        css-compat-check: visibility visible, pointer-events auto on retry button, no display:none at any phase
  pagination:
    REFERENCE. see: cascade-container
    initial-count: 20
    batch-size: 20
    scroll-threshold: 200px from bottom
    trigger: user scrolls within threshold
    loading-indicator: subtle spinner + text "Loading older entries..."
    end-of-feed: "No more entries" message
    scroll-preservation: yes, cascade pushes older entries down, viewport position retained
  responsive-breakpoints:
    desktop:
      NORMATIVE.
      min-width: 1024px
      layout: full cascade, detail panel slides in as 400px sidebar overlay
    tablet:
      min-width: 768px
      max-width: 1023px
      layout: cascade column full width, detail panel slides as bottom sheet max-height 60vh
    mobile:
      max-width: 767px
      layout: cascade full width, detail panel full-screen overlay with close button at bottom
components:
  detail-panel:
    NORMATIVE.
    element: aside
    role: dialog
    aria-modal: true
    classes: activity-feed-detail-panel
    styles:
      position: fixed
      will-change: transform opacity
      contain: paint layout style
    z-index: 1000
    props: entryId, entryType, content, metadata, actions
    state-transitions:
      closed -> animating-in:
        trigger: open=true
        properties:
          desktop: transform translateX(100%)
          mobile: transform translateY(100%)
          visibility: hidden
          pointer-events: none
          aria-hidden: true
        css-compat-pass: visibility:hidden + transform is compatible; element stays in render tree, animation executes
      animating-in -> open:
        duration: 250ms
        easing: cubic-bezier(0.16, 1, 0.3, 1)
        from: translateX(100%) desktop / translateY(100%) mobile
        to: translateX(0) desktop / translateY(0) mobile
        backdrop: opacity 0 -> 1, 200ms ease-out, z-index 999
      open -> animating-out:
        trigger: open=false, Escape key, dismiss button
        from: translateX(0) desktop / translateY(0) mobile
        to: translateX(100%) desktop / translateY(100%) mobile
        visibility: visible
        pointer-events: auto
        css-compat-pass: element visible during entire slide-out
      animating-out -> closed:
        duration: 200ms
        easing: ease-in
        to-state: visibility hidden, pointer-events none, aria-hidden true
      error-state:
        trigger: fetch failure or timeout (5000ms)
        render: red-tinted background, error icon, "Failed to load entry details", retry button
        css-compat-pass: visibility visible, pointer-events auto on retry, no display:none
      empty-state:
        trigger: panel open, no details available for entry
        render: "No details available for this entry", info-circle icon, close button only
        css-compat-pass: visibility visible, pointer-events auto on close button
    panel-content-types:
      NORMATIVE.
      blueprint-entry: title, description, meta, actions
      subagent-entry: agent-name, task-id, status, result-preview
      code-gen-entry: language, file-count, lines-added, diff-preview
      eval-run-entry: score, passed, failed, duration
      system-entry: type, message, timestamp, severity
      error-entry: error-code, message, stack-trace-toggle, solution-hint
      progress-entry: label, percent, eta, status
      milestone-entry: name, date, status, related-entries
      log-entry: level, message, timestamp, context
      checkpoint-entry: name, description, status, metrics
  entry-types:
    NORMATIVE.
    map:
      blueprint:
        icon: dx
        color: hsl(210, 70%, 50%)
        shape: rounded-square
        description: Blueprint run or definition event
      subagent:
        icon: bz
        color: hsl(270, 60%, 55%)
        shape: rounded-square
        description: Subagent task lifecycle event
      code-gen:
        icon: db
        color: hsl(160, 60%, 42%)
        shape: rounded-square
        description: Code generation event
      eval-run:
        icon: f7
        color: hsl(30, 80%, 50%)
        shape: pill
        description: Evaluation run result event
      system:
        icon: 2699
        color: hsl(0, 0%, 50%)
        shape: circle
        description: System-level notification event
      error:
        icon: 2716
        color: hsl(0, 75%, 50%)
        shape: circle
        description: Error or failure event
      progress:
        icon: 23F3
        color: hsl(120, 60%, 45%)
        shape: pill
        description: Long-running task progress event
      milestone:
        icon: 1F3C6
        color: hsl(45, 90%, 50%)
        shape: square
        description: Milestone achievement event
      log:
        icon: 1F4C4
        color: hsl(0, 0%, 60%)
        shape: circle
        description: Diagnostic log event
      checkpoint:
        icon: 1F4CD
        color: hsl(200, 80%, 50%)
        shape: pill
        description: Checkpoint reached event
  progress-bar:
    NORMATIVE.
    element: div
    class: activity-feed-progress
    data-testid: activity-feed-progress
    state-transitions:
      hidden -> indeterminate:
        trigger: status=running AND progress=null
        render: animated gradient sweep, width 100%, height 4px
        animation: sweep 1.5s ease-in-out infinite
        css-compat-pass: visibility visible, opacity animates, no display:none
        note: bar animates from zero-width to full-width sweep, parent reserves height via min-height
      indeterminate -> determinate:
        trigger: progress set to number 0-100
        render: solid color bar, width progress%, height 4px
        color-rules:
          range 0-79: green hsl(120, 60%, 45%)
          range 80-99: amber hsl(40, 90%, 50%)
          progress=100: grey hsl(0, 0%, 60%)
        animation: smart-diff width change via 200ms ease-out, requestAnimationFrame batched
        css-compat-pass: width transition compatible with visibility visible, no layout thrash
      determinate -> completed:
        trigger: status=completed OR failed OR cancelled
        render: full width grey bar, no animation, static
        css-compat-pass: width auto-transition to 100%, then animation disabled to prevent flicker
        note: upon entering completed, animation-name set to none to prevent residual motion
    eta-display:
      GUIDANCE.
      render: "~X min" format
      position: right of progress bar
      font-size: 12px
      color: var(--text-secondary)
      show-conditions: eta defined AND status=running
      hide-transition: opacity 100ms ease-out, does not shift layout (use opacity+visibility)
  entry-content-layout:
    NORMATIVE.
    row:
      left: icon container 36x36px, flex-shrink 0
      center: flex-grow 1
        title: 14px, weight 600, single-line ellipsis overflow hidden text-overflow ellipsis white-space nowrap
        description: 12px, color var(--text-secondary), max 2 lines line-clamp -webkit-line-clamp 2 -webkit-box-orient vertical overflow hidden
      right: timestamp, flex-shrink 0, 12px
    hover-reveal:
      selector: entry row :hover
      action-buttons: archive, copy, expand
      animation: opacity 0 -> 1, 100ms ease-out
      css-compat-check: opacity transition on pointer-events auto, no display:none toggle, use visibility hidden at rest
  smart-diff:
    NORMATIVE.
    purpose: Compute minimal DOM mutations between old state and new state for smooth transitions without full re-render.
    input: previous DOM state snapshot, new state descriptor
    output: mutation list (insert, update, remove, reorder)
    algorithm:
      step 1: keyed reconciliation by entry-id
      step 2: generate insert ops for new entries not in previous snapshot
      step 3: generate update ops for entries where content changed
      step 4: generate remove ops for entries absent in new state
      step 5: generate reorder ops for entries whose position changed
      step 6: assign stagger timers (25ms offset per entry, max 200ms total)
    validation-rules:
      NORMATIVE.
      - no full re-render: diff must produce at most entry-count mutations, never replace entire list
      - no double-move: an entry cannot be both inserted and removed in same batch
      - key uniqueness: each entry-id appears at most once per batch
      - timing bound: total diff computation must complete within 16ms (single frame) for entry count <= 50
        fallback: if diff exceeds 16ms, split into chunks of 10 entries per frame, schedule with requestAnimationFrame. emit warning "smart-diff chunked — performance degraded"
    error-handling:
      ERROR: key collision detected
      action: drop duplicate, log warning, continue with first occurrence
      ERROR: diff exceeds 16ms budget for framesplit
      action: fall back to flat re-render (replace list textContent), log "smart-diff timeout — flat fallback applied"
      NOTE: flat fallback removes animation capability for that batch but preserves functional correctness
    mutation-batching:
      GUIDANCE.
      collect all mutations, flush in single rAF callback
      no interleaved reads after writes in same frame (see read-after-write guard)
    read-after-write-guard:
      GUIDANCE.
      before diff: read layout values (offsetHeight, scrollTop, getBoundingClientRect)
      after diff: write style changes (transform, opacity, classList)
      never read layout between a write and the next frame. batch reads upfront.
  no-flicker-rules-entry-insert:
    NORMATIVE.
    rule 1: force GPU layer — will-change transform opacity on cascade container
    rule 2: backface-visibility hidden on all animated children
    rule 3: contain paint layout style on cascade container (paint containment prevents re-paint beyond bounds)
    rule 4: stagger timer — 25ms offset between consecutive entry animations, max 200ms total stagger window
    rule 5: suppress-recalc — batch all class changes within single requestAnimationFrame, no inline style writes between transformations. apply via cssText or classList swap.
  no-flicker-rules-smart-diff:
    NORMATIVE.
    rule 1: mutation batching — collect all DOM changes in array, flush via DocumentFragment or single innerHTML assignment if safe
    rule 2: read-after-write guard — snapshot all layout values before any mutation begins
    see: smart-diff.read-after-write-guard
  no-flicker-rules-removal:
    NORMATIVE.
    rule 1: fixed-parent-height — cascade container maintains min-height during removal to prevent layout collapse
    rule 2: release-after-animationend — upon animationend event, fire callback to remove element from DOM and adjust container height
    transition: height collapse 200ms ease-out after element removal confirmed
  entry-insert-graft:
    NORMATIVE.
    sequence:
      graft-start: opacity 0, scale(0.95), pointer-events none (entry inserted but invisible)
      graft-active: opacity 0 -> 1, scale(0.95 -> 1), 300ms cubic-bezier(0.16, 1, 0.3, 1), stagger offset applied
      graft-settle: opacity 1, scale(1), pointer-events auto, transition-settled class applied after animationend, stagger timer cleared
    css-compat-pass: visibility visible throughout graft sequence, transform and opacity both animatable on visible element, pointer-events disabled during animating phase to prevent misfire
traceability-table:
  component: detail-panel
  defined-in: components.detail-panel
  referenced-by: entry-types, controls.entry-click
  state-path:
    - components.detail-panel.closed
    - components.detail-panel.animating-in
    - components.detail-panel.open
    - components.detail-panel.animating-out
    - components.detail-panel.error-state
    - components.detail-panel.empty-state
  status: fully-specified, state path anchored to real states, no orphan references
  component: cascade-container
  defined-in: feed-level-specification.cascade-container
  referenced-by: pagination, entry-insert-graft, smart-diff, removal.no-flicker-rules-removal
  state-path:
    - feed-level-specification.cascade-container.states.loading
    - feed-level-specification.cascade-container.states.loaded
    - feed-level-specification.cascade-container.states.empty
    - feed-level-specification.cascade-container.states.error
  status: fully-specified, each state has defined render and transitions, no display:none
  component: entry-types (10)
  defined-in: components.entry-types
  referenced-by: components.detail-panel.panel-content-types, components.entry-content-layout
  state-path: static map, no animation states
  status: fully-specified
  component: progress-bar
  defined-in: components.progress-bar
  referenced-by: components.entry-content-layout.row, smart-diff.mutation-batching
  state-path:
    - components.progress-bar.hidden
    - components.progress-bar.indeterminate
    - components.progress-bar.determinate
    - components.progress-bar.completed
  status: fully-specified, each transition has css-compat-check documented
  component: smart-diff
  defined-in: components.smart-diff
  referenced-by: components.progress-bar.determinate, components.entry-insert-graft, cascade-container
  state-path:
    - components.smart-diff.input
    - components.smart-diff.output
    - components.smart-diff.mutations
    - components.smart-diff.error-handling (fallback paths)
  status: fully-specified, includes error-handling and fallback sections
  component: no-flicker-rules (entry-insert)
  defined-in: components.no-flicker-rules-entry-insert
  referenced-by: components.entry-insert-graft.graft-active, components.entry-insert-graft.graft-settle
  state-path:
    - components.no-flicker-rules-entry-insert.rule-1
    - components.no-flicker-rules-entry-insert.rule-2
    - components.no-flicker-rules-entry-insert.rule-3
    - components.no-flicker-rules-entry-insert.rule-4
    - components.no-flicker-rules-entry-insert.rule-5
  status: consolidated, no duplication with smart-diff or removal sections
  component: no-flicker-rules (smart-diff)
  defined-in: components.no-flicker-rules-smart-diff
  referenced-by: components.smart-diff.validation-rules
  state-path:
    - components.no-flicker-rules-smart-diff.rule-1
    - components.no-flicker-rules-smart-diff.rule-2
  status: consolidated, cross-referenced smart-diff.read-after-write-guard instead of duplicating
  component: no-flicker-rules (removal)
  defined-in: components.no-flicker-rules-removal
  referenced-by: cascade-container, smart-diff.mutations
  state-path:
    - components.no-flicker-rules-removal.rule-1
    - components.no-flicker-rules-removal.rule-2
    - components.no-flicker-rules-removal.release-after-animationend
  status: consolidated, cross-referenced instead of mirroring entry-insert rules
  component: entry-insert-graft
  defined-in: components.entry-insert-graft
  referenced-by: cascade-container, no-flicker-rules-entry-insert
  state-path:
    - components.entry-insert-graft.graft-start
    - components.entry-insert-graft.graft-active
    - components.entry-insert-graft.graft-settle
  status: fully-specified, transition labels graft-start/graft-active/graft-settle replace generic "grafted as start state" pattern
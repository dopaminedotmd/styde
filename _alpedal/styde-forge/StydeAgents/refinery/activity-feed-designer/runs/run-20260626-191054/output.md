activity-feed-blueprint v4
domain: frontend
tracestyle: compressed
purpose: design real-time activity feed components for forge dashboard mockups. smart-diff rendering, cascade-style updates, eta bars, progress indicators, entry types with visual distinction. no blink, no flicker.
persona: activity feed designer. real-time cascade updates with smart-diff. eta bars, progress indicators, entry type icons. each event instantly readable and visually distinct. no blinking, no flicker.
state-validation-mandate:
  rule: before finalizing any state definition, verify no css/state properties contradict each other
  audit-method: trace every element through open -> animating -> closed. flag incompatible combinations.
  banned-combinations:
    - display:none + transform:translateX(): display:none removes element from render tree, transform becomes invisible
    - display:none + opacity transition: opacity never animates because element is removed
    - display:block <-> display:none on same element with transition: display is not animatable, instant cut
  allowed-hidden:
    - visibility:hidden + pointer-events:none: element retains layout, transitions execute normally
  audit-path: entries, detail-panel, progress-bar, cascade-container, overlay-elements
feed-level-spec:
  cascade-container:
    tag: div
    role: feed
    aria-live: polite
    aria-relevant: additions removals
    class: activity-feed-cascade
    data-testid: activity-feed
    style: display flex, flex-direction column, gap 4px, position relative, contain: paint layout style, will-change: transform opacity
    max-height: 60vh
    overflow-y: auto
    scrollbar: thin
    states:
      loading: skeleton placeholder 3 pulsing rows
      loaded: entries rendered
      empty: centered text 'No recent activity'
      error: error icon + 'Failed to load feed' + retry button
  pagination:
    initial-load: 20 entries
    trigger: scroll within 200px of bottom
    batch-size: 20
    loading-indicator: subtle spinner + 'Loading older entries...'
    end-of-feed: 'No more entries'
    scroll-preservation: cascade pushes older entries down, viewport position unchanged
  responsive-breakpoints:
    desktop: >= 1024px, cascade full layout, detail panel slides as 400px sidebar overlay
    tablet: 768-1023px, cascade full width, detail panel slides as bottom sheet max-height 60vh
    mobile: < 768px, cascade full width, detail panel full-screen sheet, entries compact mode
components:
  detail-panel:
    tag: aside
    class: activity-feed-detail
    role: complementary
    width: 400px desktop, max-height 60vh mobile
    z-index: 1000
    props: entryId, entryType, content, metadata, actions
    states:
      closed: transform translateX(100%) desktop / translateY(100%) mobile, visibility hidden, pointer-events none, aria-hidden true
      open: transform translateX(0) desktop / translateY(0) mobile, visibility visible, pointer-events auto, backdrop overlay behind
      empty: panel open, content 'No details available for this entry', info-circle icon, close button only
      loading: skeleton loader 3/2/1 lines pulsing, timeout 5000ms -> error
      error: red-tinted background, error icon, 'Failed to load entry details', retry button
    transitions:
      slide-in (open=true): 250ms cubic-bezier(0.16, 1, 0.3, 1), translateX(100%) -> 0 desktop / translateY variants mobile
      slide-out (open=false): 200ms ease-in, translateX(0) -> 100%
      backdrop-fade: any panel state change, 200ms ease-out
    panel-content-types: blueprint-entry, subagent-entry, code-gen-entry, eval-run-entry, system-entry, error-entry, progress-entry, milestone-entry, log-entry, checkpoint-entry
    actions: dismiss (close/Escape), retry (error only), expand (truncated), navigate (Ctrl+Click), copy (Ctrl+C)
  entry-type-table:
    types: 10
    blueprint:
      icon: blueprint
      color: hsl(220, 70%, 55%)
      shape: rounded-square
      description: blueprint generation or update event
    subagent:
      icon: bot
      color: hsl(270, 60%, 55%)
      shape: circle
      description: subagent task started or completed
    code-gen:
      icon: code
      color: hsl(160, 60%, 45%)
      shape: rounded-square
      description: code generation event
    eval-run:
      icon: play
      color: hsl(190, 70%, 50%)
      shape: circle
      description: eval pipeline run event
    system:
      icon: gear
      color: hsl(0, 0%, 50%)
      shape: square
      description: system-level notification
    error:
      icon: x-circle
      color: hsl(0, 80%, 55%)
      shape: circle
      description: error or failure event
    progress:
      icon: bar-chart
      color: hsl(120, 60%, 45%)
      shape: pill
      description: batch progress update
    milestone:
      icon: flag
      color: hsl(45, 90%, 50%)
      shape: rounded-square
      description: milestone reached
    log:
      icon: file-text
      color: hsl(30, 50%, 55%)
      shape: square
      description: log entry
    checkpoint:
      icon: bookmark
      color: hsl(330, 60%, 55%)
      shape: pill
      description: save state checkpoint
  progress-bar:
    tag: div
    class: activity-feed-progress
    states:
      indeterminate: animated gradient sweep, width 100%, height 4px, animation sweep 1.5s ease-in-out infinite, status=running AND progress=null
      determinate: solid color bar 0%-progress%, height 4px, color green 0-79% amber 80-99% grey 100%, animated via smart-diff 200ms ease-out
      completed: full width grey bar, no animation, status=completed/failed/cancelled
    eta-display: '~X min' format, right of bar, font-size 12px, color var(--text-secondary), only when eta defined AND status=running
  entry-content-layout:
    left: icon container 36x36px, flex-shrink 0
    center: flex-grow 1, title 14px 600 single-line ellipsis + description 12px text-secondary max 2 lines line-clamp
    right: timestamp flex-shrink 0 12px
    hover-reveal: action buttons archive copy expand on entry hover, opacity transition 100ms no-flicker
animation:
  no-flicker-rules:
    entry-insert:
      rule1: force-gpu-layer: transform translateZ(0) on all animating elements
      rule2: backface-visibility hidden on animating elements
      rule3: contain paint layout style on cascade container
      rule4: stagger insert: max 3 entries per frame, 16ms interval between batches
      rule5: suppress-recalc: batch DOM mutations inside requestAnimationFrame, read layout properties in a single rAF read-pass before write-pass
    smart-diff:
      rule1: mutation-batching: collect all mutations in a single flush, apply in one rAF callback
      rule2: read-after-write-guard: never read offsetHeight/clientHeight after a style mutation in the same frame. if values needed, snapshot before mutations
    removal:
      rule1: fixed-parent-height: before removing an entry, lock parent height to current value so collapse animates smoothly
      rule2: release-after-animationend: after collapse animation completes (200ms ease-out), remove element from DOM via onanimationend handler
  entry-insert:
    graft: opacity 0 -> 1, transform translateY(-8px) -> 0, 200ms cubic-bezier(0.16, 1, 0.3, 1)
    settle: after graft completes, no further animation
    diff: smart-diff compares previous state vs new state, generates minimal mutation set
  smart-diff-definition:
    input: prevEntries array, nextEntries array
    output: mutations array of ADD REMOVE UPDATE REORDER operations
    validation-rules:
      diff-command: diff --unified=5 --ignore-all-space
      files-to-diff: cascade-container.children vs next render tree
      classification:
        visual-only: color, opacity, shadow, transform changes. no reflow impact
        behavioral: click handlers, aria attributes, tabindex changes
        styling-only: font-size, font-weight, margin, padding. reflow but no semantic change
      mutation-batching: all mutations collected in one pass before DOM write
      read-after-write-guard: snapshot layout values before any style write in same frame
      determinate-width: progress bar width animates from previous value to new value using FLIP. first-read: getBoundingClientRect. last-write: set transition, apply new width. invert: calculate delta. play: animate
  removal:
    collapse-parent-height: parent container height locked to pre-removal value
    fade-out: opacity 1 -> 0, 200ms ease-out
    collapse: parent height animates from locked value to new computed height, 200ms ease-out
    release: after animationend, element removed from DOM, parent height released to auto
traceability-table:
  component: detail-panel
  defined-in: components.detail-panel
  referenced-by: entry-type-table, entry.states.expanded
  state-path: closed open empty loading error
  status: fully specified, no orphan references
  component: cascade-container
  defined-in: feed-level-spec.cascade-container
  referenced-by: animation.entry-insert.graft, animation.smart-diff, animation.removal.collapse-parent-height
  state-path: loading loaded empty error
  status: fully specified
  component: entry-types (10)
  defined-in: components.entry-type-table
  referenced-by: components.entry-content-layout, components.detail-panel.panel-content-types
  state-path: static map no animation states
  status: fully specified
  component: progress-bar
  defined-in: components.progress-bar
  referenced-by: components.entry-content-layout, animation.smart-diff.determinate-width
  state-path: indeterminate determinate completed
  status: fully specified
  component: smart-diff
  defined-in: animation.smart-diff-definition
  referenced-by: components.progress-bar.states.determinate, animation.entry-insert
  state-path: input output mutations
  status: fully specified
  component: no-flicker entry-insert
  defined-in: animation.no-flicker-rules.entry-insert
  referenced-by: animation.entry-insert.graft, animation.entry-insert.settle
  state-path: force-gpu-layer backface-visibility contain-paint stagger-timer suppress-recalc
  status: consolidated no duplication
  component: no-flicker smart-diff
  defined-in: animation.no-flicker-rules.smart-diff
  referenced-by: animation.smart-diff-definition.validation-rules
  state-path: mutation-batching read-after-write-guard
  status: consolidated no duplication
  component: no-flicker removal
  defined-in: animation.no-flicker-rules.removal
  referenced-by: animation.removal.collapse-parent-height
  state-path: fixed-parent-height release-after-animationend
  status: consolidated no duplication
  component: feed-level pagination
  defined-in: feed-level-spec.pagination
  referenced-by: cascade-container.states.loading
  state-path: initial-load infinite-scroll end-of-feed
  status: fully specified
  component: feed-level responsive
  defined-in: feed-level-spec.responsive-breakpoints
  referenced-by: detail-panel.position, entry-content-layout.compact
  state-path: desktop tablet mobile
  status: fully specified
css-property-contradiction-detection:
  rule1: if transition on transform is set, verify no other transform rule in same specificity bucket. two transform rules on same element cause one to override silently, breaking the animated value
  rule2: if filter is animated, verify no backdrop-filter on parent element. nested filters cause layout pass invalidation
  rule3: if opacity animates, verify element is not inside a container with overflow:hidden during animating phase. clipped overflow can cut off partially-transparent content
  rule4: if width/height animates, verify no grid or flex sizing on same axis at parent level. flex-grow overrides animated width
  rule5: if visibility transitions, verify no display change in same cascade. visibility and display share no transition bridge
quality-gate:
  strip-redundant-content: pass
  delimiter-consistency: pass
  state-path-verification: pass
  cross-reference-audit: pass
  token-density-scan: pass
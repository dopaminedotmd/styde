activity feed designer blueprint v4.1
persona
  role: activity feed designer
  specialty: real-time cascade updates with smart-diff
  domain: frontend
  components: eta bars, progress indicators, entry type icons
  constraints: no blinking, no flicker
  output rules: strip all ansi escape codes from diff output. present changes as clean formatted summaries with only relevant code excerpts. no raw terminal artifacts.
  state validation: before finalizing any state definition verify no css properties contradict each other. trace every element through open -> animating -> closed. document the audit trail.
state validation mandate
  all components below include a state path trace. any combination of display:none + transform or visibility:hidden + opacity animation is flagged and corrected. use visibility:hidden + pointer-events:none for hidden-but-animatable states. never display:none.
feed-level specification
cascade container
  tag: div
  role: feed
  aria-live: polite
  aria-relevant: additions removals
  class: activity-feed-cascade
  data-testid: activity-feed
  style: display flex, flex-direction column, gap 4px, position relative, contain: paint layout style, will-change: transform opacity
  max-height: 60vh with overflow-y auto, thin scrollbar
  states:
    loading: skeleton placeholder 3 pulsing rows shown when feed initializes
    loaded: entries rendered
    empty: "No recent activity" centered text when entry count is 0
    error: error icon and "Failed to load feed" message with retry button
dom structure example
  <div class="activity-feed-cascade" role="feed" aria-live="polite" data-testid="activity-feed">
    <div class="feed-skeleton"></div>  <!-- loading state -->
    <!-- entry cards injected here -->
    <div class="feed-empty">No recent activity</div>  <!-- empty state -->
    <div class="feed-error">Failed to load feed</div>  <!-- error state -->
  </div>
state machine: cascade container
  states: [empty, loading, loaded, error]
  transitions:
    initial -> loading: mount
    loading -> loaded: first batch received
    loading -> error: 5000ms timeout or api failure
    loaded -> empty: all entries removed
    loaded -> error: subsequent api failure
    loaded -> loaded: new entries appended via cascade
    error -> loading: retry button clicked
pagination / infinite scroll
  initial batch: 20 entries
  trigger: user scrolls within 200px of bottom
  batch size: 20 entries
  loading indicator: subtle spinner at bottom with "Loading older entries..."
  end-of-feed: "No more entries" message after all loaded
  scroll preservation: cascade pushes older entries down without losing viewport position
responsive breakpoints
  >= 1024px: full cascade layout, detail panel slides as 400px sidebar overlay
  768px - 1023px: cascade column full width, detail panel slides as bottom sheet (max-height 60vh)
  < 768px: cascade full width, compact mode for entries (icon removed, stacked layout), detail panel as full-screen overlay with padding
components
detail panel
  tag: aside
  role: complementary
  class: activity-feed-detail-panel
  position: fixed right 0 top 0 or fixed bottom 0 (based on breakpoint >= 1024px or < 1024px)
  width: 400px on desktop, full on mobile
  z-index: 1000
  props: entryId, entryType, content, metadata, actions
  states:
    closed: transform translateX(100%) on desktop or translateY(100%) on mobile, visibility hidden, pointer-events none, aria-hidden true
    open: transform translateX(0) on desktop or translateY(0) on mobile, visibility visible, pointer-events auto, backdrop overlay behind panel
    empty: panel open but content shows "No details available for this entry", icon info-circle, close button only
    loading: skeleton loader 3 lines pulsing then 2 then 1, timeout at 5000ms -> error state
    error: red-tinted background, error icon, message "Failed to load entry details", retry button
  transition notes: closed state uses visibility:hidden + pointer-events:none not display:none. display:none blocks the slide-out animation because the element is removed from the render tree. visibility:hidden keeps layout and allows transition to execute.
  transitions:
    slide-in (open=true): 250ms cubic-bezier(0.16, 1, 0.3, 1) from translateX(100%) to translateX(0) [or translateY variants on mobile]
    slide-out (open=false): 200ms ease-in from translateX(0) to translateX(100%)
    backdrop-fade: 200ms ease-out on any panel state change
  panel content: see entry-type-table for per-type layout specifications
  actions: dismiss (close, Escape), retry (error state only), expand (when truncated), navigate (Ctrl+Click), copy (Ctrl+C)
dom structure example: detail panel
  <aside class="activity-feed-detail-panel" role="complementary" aria-hidden="true">
    <div class="detail-panel-backdrop"></div>
    <div class="detail-panel-content">
      <div class="detail-panel-header">
        <button class="detail-panel-close">x</button>
      </div>
      <div class="detail-panel-body">
        <div class="detail-panel-skeleton"></div>  <!-- loading state -->
        <div class="detail-panel-empty">No details available</div>  <!-- empty state -->
        <div class="detail-panel-error">Failed to load... <button>Retry</button></div>  <!-- error state -->
        <!-- actual entry content rendered here when loaded -->
      </div>
    </div>
  </aside>
state machine: detail panel
  states: [closed, open-empty, open-loading, open-loaded, open-error]
  transitions:
    closed -> open-loading: entry selected
    open-loading -> open-loaded: details fetched (typical 200-800ms)
    open-loading -> open-error: timeout at 5000ms or fetch failure
    open-loading -> open-empty: fetch returns no content
    open-loaded -> closed: dismiss or Escape
    open-empty -> closed: dismiss or Escape
    open-error -> open-loading: retry button clicked
    open-error -> closed: dismiss or Escape
entry type table
  10 types with visual distinction
  blueprint
    icon: blueprint-emoji
    color: hsl(210, 100%, 50%)
    shape: circle
    description: blueprint created or updated. shows blueprint id, version, config diff summary.
  subagent
    icon: subagent-emoji
    color: hsl(270, 80%, 55%)
    shape: rounded-square
    description: subagent spawned, running, or completed. shows agent name, task, duration.
  code-gen
    icon: code-gen-emoji
    color: hsl(150, 70%, 40%)
    shape: square
    description: code generation event. shows file path, language, line count, diff summary.
  eval-run
    icon: eval-run-emoji
    color: hsl(30, 100%, 50%)
    shape: pill
    description: evaluation run started or finished. shows score, pass/fail count, duration.
  system
    icon: system-emoji
    color: hsl(0, 0%, 40%)
    shape: circle
    description: system-level event like config change, restart, connection status.
  error
    icon: error-emoji
    color: hsl(0, 80%, 55%)
    shape: rounded-square
    description: error or warning. shows error type, message, stack excerpt.
  progress
    icon: progress-emoji
    color: hsl(200, 80%, 50%)
    shape: square
    description: batch or pipeline progress update. shows current/total, percentage, eta.
  milestone
    icon: milestone-emoji
    color: hsl(45, 100%, 50%)
    shape: circle
    description: significant achievement or checkpoint. shows milestone name, description, impact.
  log
    icon: log-emoji
    color: hsl(0, 0%, 60%)
    shape: pill
    description: raw log entry. shows log level, source, message preview.
  checkpoint
    icon: checkpoint-emoji
    color: hsl(340, 80%, 50%)
    shape: rounded-square
    description: state checkpoint saved or restored. shows checkpoint id, size, timestamp.
entry content layout
  left: icon container 36x36px, flex-shrink 0
  center: flex-grow 1, title 14px 600 weight single-line ellipsis + description 12px text-secondary max 2 lines line-clamp
  right: timestamp flex-shrink 0 12px
  hover-reveal: action buttons (archive, copy, expand) on entry hover, opacity transition 100ms no-flicker
dom structure example: entry card
  <div class="activity-feed-entry" data-entry-type="blueprint" data-status="running">
    <div class="entry-icon">(emoji)</div>
    <div class="entry-body">
      <div class="entry-title">Blueprint v4.2 created</div>
      <div class="entry-description">Blueprint for precision-forge-agent with 3 subagent layers</div>
      <div class="entry-progress-bar indeterminate"></div>  <!-- optional, shown for running tasks -->
      <div class="entry-meta">ETA ~2 min</div>  <!-- optional, shown during progress -->
    </div>
    <div class="entry-timestamp">2 min ago</div>
    <div class="entry-actions"><button>archive</button><button>copy</button></div>
  </div>
state machine: entry card
  states: [compact, expanded, loading, error]
  transitions:
    compact -> expanded: user clicks entry
    compact -> loading: status=running and no data yet
    loading -> compact: status transitions to queued/completed
    compact -> compact: hover-reveal actions shown/hidden
    expanded -> compact: dismiss or clicking another entry
    expanded -> error: detail fetch failure (delegated to detail panel)
    compact -> error: entry-level error state shown inline
progress bar
  tag: div
  class: activity-feed-progress
  states:
    indeterminate: animated gradient sweep, width 100%, height 4px, animation sweep 1.5s ease-in-out infinite, shown when status=running AND progress=null
    determinate: solid color bar 0% to progress%, height 4px, color green (0-79%), amber (80-99%), grey (100%), animated via smart-diff 200ms ease-out
    completed: full width grey bar, no animation, shown when status=completed/failed/cancelled
  eta display: "~X min" format right of progress bar, font-size 12px, color var(--text-secondary), shown only when eta defined AND status=running
state machine: progress bar
  states: [indeterminate, determinate, completed]
  transitions:
    indeterminate -> determinate: progress value received from server
    determinate -> determinate: progress value updates via smart-diff
    determinate -> completed: status becomes completed/failed/cancelled
    indeterminate -> completed: task finishes before progress measured
    completed -> (terminal): no further transitions
smart-diff definition
  purpose: animate only the parts of the dom that actually changed between renders
  mechanism: morphdom or similar vdom diffing, targeting entry-level wrapper nodes
  rules:
    mutation batching: collect all dom mutations within a single animation frame before applying.
    read-after-write guard: do not read layout properties (offsetHeight, getBoundingClientRect) after writing dom mutations in the same frame. batch reads before writes.
    entry-level scope: smart-diff applies only to entry wrapper nodes, not their children. individual entry content updates use their own transitions.
    skip unmount: entries being removed go through the removal animation pipeline, not smart-diff.
  integration: progress bar determinate updates use smart-diff for smooth width transitions.
consolidated animation table
animation name           trigger                target            duration    curve                  affected layers
entry-insert-graft       new entry added        entry wrapper     300ms       cubic-bezier(0.16,1,0.3,1)  transform, opacity, height
entry-insert-settle      entry enters viewport  entry wrapper     200ms       ease-out               transform, opacity
entry-insert-force-gpu   each insert event      entry wrapper     N/A         N/A                   backface-visibility, contain
entry-update-smart-diff  progress/text change   entry body        200ms       ease-out               width (progress), opacity (text)
entry-removal-collapse   entry removed          entry wrapper     200ms       ease-in                height, margin, padding, opacity
entry-removal-release    after animationend     entry wrapper     0ms         N/A                   display:none (removes from layout)
detail-slide-in          entry selected         detail panel      250ms       cubic-bezier(0.16,1,0.3,1)  transform
detail-slide-out         detail dismissed       detail panel      200ms       ease-in                transform
detail-backdrop-fade     any panel state change backdrop overlay   200ms       ease-out               opacity
progress-indeterminate   status=running         progress bar      infinite    1.5s ease-in-out        background-position
progress-determinate     progress value change  progress bar      200ms       ease-out               width
hover-reveal             entry hover on/off     entry-actions     100ms       ease-out               opacity
stagger-delay            multiple entries added entry:nth-child   50ms*N      N/A                   N/A (delay only)
no-flicker rules
  rule 1: force gpu layer on entry wrapper with transform: translateZ(0) or will-change: transform
  rule 2: backface-visibility: hidden on all animated entry elements
  rule 3: contain: paint layout style on cascade container to isolate repaints
  rule 4: stagger new entry insertions by 50ms max 5 entries per frame
  rule 5: suppress style recalc on cascade container during insertion by using requestAnimationFrame batching
  rule 6: for removal, set fixed height on parent container before collapse to prevent layout jump
  rule 7: release removal height constraint only after animationend event fires
traceability table
component             defined in                 referenced by                     state path                                                                          status
detail-panel          components.detail-panel    entry-type-table.panel-content     detail-panel.closed, detail-panel.open, detail-panel.empty, detail-panel.loading, detail-panel.error  fully specified
cascade-container     feed-level.cascade-container  animation.consolidated-table      cascade-container.loading, cascade-container.loaded, cascade-container.empty, cascade-container.error  fully specified
entry-types (10)      components.entry-type-table   entry-content-layout, detail-panel (see ref)                        N/A static map, no animation states                                      fully specified, single source of truth
progress-bar          components.progress-bar        entry-content-layout, animation.consolidated-table                 progress-bar.indeterminate, progress-bar.determinate, progress-bar.completed  fully specified
smart-diff            components.smart-diff          progress-bar.states.determinate, animation.consolidated-table      smart-diff.input, smart-diff.output, smart-diff.mutations                   fully specified
no-flicker rules      animation.no-flicker-rules     animation.consolidated-table (all rows reference no-flicker)        all animation states consolidated                                          consolidated, single table, no duplication
feed-loading-pagination  feed-level.pagination       cascade-container.states.loading                                  feed.initial-load, feed.infinite-scroll, feed.end-of-feed                    fully specified
feed-responsive       feed-level.responsive-breakpoints  detail-panel.position, entry-content-layout.compact-trigger    feed.desktop, feed.tablet, feed.mobile                                       fully specified
references are unidirectional: entry-type-table defines all entry type information and detail-panel references it. no circular references between components.
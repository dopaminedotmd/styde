Activity Feed Designer
Domain: frontend
Version: 4
Purpose:
Design real-time Activity Feed components for Forge dashboard mockups. Smart-diff rendering, cascade-style updates, ETA bars, progress indicators, entry types with visual distinction.
State Validation Mandate:
Before finalizing any state definition, verify that no CSS/state properties contradict each other. Trace every element through open -> animating -> closed to confirm properties are compatible at each phase. Document the trace in each component's transition section. Invalid combos to flag: display:none + transform (invisible), visibility:hidden + opacity transition (cannot animate), pointer-events:none on animating element (blocks interaction before animation completes).
Feed-Level Specification
cascade-container:
  tag: div
  role: feed
  aria-live: polite
  aria-relevant: additions removals
  class: activity-feed-cascade
  data-testid: activity-feed
  style:
    display: flex
    flex-direction: column
    gap: 4px
    position: relative
    contain: paint layout style
    will-change: transform opacity
    max-height: 60vh
    overflow-y: auto
  scrollbar: thin (webkit-scrollbar width 6px)
  states:
    loading: skeleton placeholder, 3 pulsing rows, shown on init
    loaded: entries rendered
    empty: centered text "No recent activity", shown when entry count = 0
    error: error icon + "Failed to load feed", retry button
  transitions: none (container itself is static; children animate in/out)
pagination / infinite-scroll:
  initial-load: 20 entries
  trigger: user scrolls within 200px of container bottom
  batch-size: 20 entries
  loading-indicator: subtle spinner + text "Loading older entries..."
  end-of-feed: "No more entries" message
  scroll-position: preserved on insert (cascade pushes older entries down)
responsive-breakpoints:
  desktop (>= 1024px): full cascade layout, detail panel is 400px sidebar overlay, right side
  tablet (768-1023px): cascade full-width, detail panel is bottom sheet, max-height 60vh
  mobile (< 768px): same as tablet but cascade is single-column, expanded entry spans full-width inline detail section, no overlay
Components
detail-panel:
  tag: aside
  role: region
  aria-label: Entry detail panel
  data-testid: detail-panel
  style:
    position: fixed
    top: 0
    right: 0 (desktop) or bottom: 0 (tablet/mobile)
    width: 400px (desktop) or 100% (tablet/mobile)
    height: 100% (desktop) or max-height: 60vh (tablet/mobile)
    background: var(--surface-color)
    box-shadow: -4px 0 12px rgba(0,0,0,0.1) (desktop) or 0 -4px 12px rgba(0,0,0,0.1) (tablet/mobile)
    z-index: 1000
    transition: transform 250ms cubic-bezier(0.16, 1, 0.3, 1), opacity 200ms ease-out
    backdrop-filter: blur(2px) (behind panel, when open)
  props: entryId, entryType, content, metadata, actions
  states:
    closed:
      transform: translateX(100%) [desktop] or translateY(100%) [tablet/mobile]
      visibility: hidden
      pointer-events: none
      aria-hidden: true
      note: visibility:hidden + pointer-events:none, NOT display:none. display:none removes element from render tree, blocking the slide-out animation.
    open:
      transform: translateX(0) [desktop] or translateY(0) [tablet/mobile]
      visibility: visible
      pointer-events: auto
      backdrop: semi-transparent overlay behind panel
    empty:
      same as open visually
      content: "No details available for this entry"
      icon: info-circle
      actions: close only
    loading:
      skeleton: 3 lines pulsing -> 2 -> 1 over 2s
      timeout: 5000ms -> error state
    error:
      background: red-tinted (var(--error-bg))
      icon: error icon
      message: "Failed to load entry details"
      action: retry button
  transitions:
    slide-in (open=true): 250ms cubic-bezier(0.16, 1, 0.3, 1), from translateX(100%) to translateX(0)
    slide-out (open=false): 200ms ease-in, from translateX(0) to translateX(100%)
    backdrop-fade: 200ms ease-out, triggered on any panel state change
  state validation trace (open -> animating -> closed):
    - open: transform(0) + visibility(visible) + pointer-events(auto) + opacity(1) -> compatible, all animatable
    - animating to closed: transform from 0 to 100% + opacity from 1 to 0 -> compatible, GPU-composited properties only, no layout recalc
    - closed: transform(100%) + visibility(hidden) + pointer-events(none) + opacity(0) -> compatible, element stays in layout (no display:none), transition renders fully
  panel-content-types: blueprint-entry, subagent-entry, code-gen-entry, eval-run-entry, system-entry, error-entry, progress-entry, milestone-entry, log-entry, checkpoint-entry
  actions: dismiss (close button + Escape key), retry (error state only), expand (when content truncated), navigate (Ctrl+Click), copy (Ctrl+C)
entry-type-table:
  types:
    - name: blueprint
      icon: template-emoji
      color: hsl(210, 70%, 50%)
      shape: rounded-square
      description: Blueprint loaded or generated
    - name: subagent
      icon: bot-emoji
      color: hsl(170, 60%, 40%)
      shape: circle
      description: Subagent task dispatched or completed
    - name: code-gen
      icon: code-emoji
      color: hsl(260, 60%, 50%)
      shape: square
      description: Code generation event
    - name: eval-run
      icon: gauge-emoji
      color: hsl(30, 80%, 50%)
      shape: pill
      description: Evaluation run started/completed
    - name: system
      icon: gear-emoji
      color: hsl(0, 0%, 45%)
      shape: rounded-square
      description: System notification or status change
    - name: error
      icon: x-circle-emoji
      color: hsl(0, 70%, 50%)
      shape: circle
      description: Error or failure event
    - name: progress
      icon: loader-emoji
      color: hsl(120, 55%, 40%)
      shape: pill
      description: Ongoing operation with ETA
    - name: milestone
      icon: flag-emoji
      color: hsl(45, 90%, 50%)
      shape: rounded-square
      description: Milestone reached or checkpoint hit
    - name: log
      icon: file-text-emoji
      color: hsl(190, 60%, 40%)
      shape: square
      description: Log entry or debug output
    - name: check-detail
      icon: clipboard-check-emoji
      color: hsl(140, 55%, 35%)
      shape: pill
      description: Checkpoint summary
  note: static map, no animation states, no state path entry required
progress-bar:
  tag: div
  class: activity-feed-progress
  height: 4px
  width: 100%
  states:
    indeterminate:
      display: gradient sweep animation
      width: 100%
      animation: sweep 1.5s ease-in-out infinite
      shown when: status=running AND progress=null
    determinate:
      display: solid color bar, width = progress%
      color: green (0-79%), amber (80-99%), grey (100%)
      transition: width 200ms ease-out (smart-diff mode)
      shown when: progress is a number AND status=running
    completed:
      display: full-width grey bar
      animation: none
      shown when: status=completed/failed/cancelled
  eta-display:
    text: "~X min"
    position: right of progress bar
    font-size: 12px
    color: var(--text-secondary)
    visible when: eta defined AND status=running
  state validation trace (indeterminate -> determinate -> completed):
    - indeterminate: animated gradient on width 100% -> compatible with contain:paint, no layout shift
    - determinate: width animates from current% to new% (200ms ease-out) -> GPU-composited, transform on width triggers layout but contained by contain:paint; acceptable
    - completed: static full-width grey, no animation -> compatible with any prior state
entry:
  tag: div
  class: activity-feed-entry
  role: article
  layout:
    left: icon container, 36x36px, flex-shrink 0, contains type icon
    center: flex-grow 1, title (14px font-weight 600 single-line ellipsis) + description (12px color var(--text-secondary) max 2 lines line-clamp)
    right: timestamp, flex-shrink 0, 12px color var(--text-secondary)
  hover-reveal:
    action-buttons: archive, copy, expand
    opacity transition: 100ms no-flicker
    visible on .activity-feed-entry:hover
  required-props: entryId (string), entryType (from entry-type-table), content (object), timestamp (ISO8601), status (string: running|completed|failed|cancelled|paused)
  optional-props: metadata (object), actions (array), progress (number|null), eta (number|null)
  states:
    compact: single row, progress bar optional (2-line indent), no metadata
    expanded: full detail row inserted below compact row, see: detail-panel states
    status-transition: visual flash (background-color 200ms ease-out) when status changes
    grafting: see: animation.entry-insert section for no-flicker rules
animation:
  entry-insert:
    no-flicker-rules:
      1. force-gpu-layer: transform: translateZ(0) on each entry, prevents repaint cascade on sibling insertion
      2. backface-visibility: hidden on entry container, eliminates flicker from backface rendering
      3. contain-paint: entry container, isolates paint bounds to the entry itself
      4. stagger-timer: 30ms stagger between entries in same batch, prevents simultaneous layout thrash
      5. suppress-recalc: requestAnimationFrame batching of DOM reads and writes (read layout once, batch all writes)
    graft:
      target: cascade-container first-child (newest entries inserted at top)
      flow: offset calc -> opacity 0 -> translateY(-20px) start -> 200ms ease-out to translateY(0) opacity 1
    settle:
      target: all existing entries shift down by entry height
      method: transform translateY() on each existing entry, pre-calculated to avoid layout recalc
      timing: 200ms cubic-bezier(0.16, 1, 0.3, 1) stagger 15ms
    note: cascade-container acts as the positioning context; will-change on container hints GPU layer; entry transforms are composited, no layout trigger
  smart-diff:
    input: previous entry list, current entry list
    ouput: minimal mutation set (insert, update, remove, reorder)
    mutations:
      insert: see: animation.entry-insert.graft
      update: DOM attribute swap only on changed props, no re-render of unchanged children
      remove: see: animation.removal
      reorder: transform translateY() on moved entries, no DOM re-parenting
    determinate: progress bar width transition 200ms ease-out (see: progress-bar.determinate)
    no-flicker-override:
      mutation-batching: collect all DOM mutations in a single requestAnimationFrame callback
      read-after-write-guard: after any mutation batch, pause 16ms before next read to avoid forced synchronous layout
    validation-rules:
      - each entry must have unique entryId for diff key
      - entryId must not change on reorder (stable keys)
      - progress value changes from X to Y: always a determinate update, never re-insertion
      - status changes must preserve entry position in list (status is not a sorting key)
  removal:
    target: entry being removed from DOM
    sequence:
      1. opacity transition 150ms ease-in (fade out)
      2. on animationend, remove element from DOM
      3. remaining entries smoothly adjust position via transform translateY (smart-diff)
    collapse-parent-height:
      method: set fixed height on parent cascade-container during removal, release after animationend
      prevents scroll jump while removal animations run
    no-flicker:
      - lock cascade-container height to current scrollHeight at removal start
      - unlock on animationend of removed element
      - entries below removed element get translateY(-entry-height) transition 200ms ease-out
Cross-references used (each fact appears exactly once):
  - entry.states.expanded -> detail-panel states
  - entry.states.grafting -> animation.entry-insert
  - progress-bar.determinate transition -> animation.smart-diff.determinate
  - animation.smart-diff.ouput reads -> animation.entry-insert.graft, animation.removal
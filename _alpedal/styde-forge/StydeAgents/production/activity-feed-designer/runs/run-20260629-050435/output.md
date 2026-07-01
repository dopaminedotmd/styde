activity-feed-spec-v4.yaml
state-audit:
  detail-panel:
    path: closed -> animating -> open
    closed:
      transform: translateX(100%) | translateY(100%)
      visibility: hidden
      pointer-events: none
      aria-hidden: "true"
    animating:
      transform: transitioning 200-250ms
      visibility: visible
      pointer-events: none
    open:
      transform: translateX(0) | translateY(0)
      visibility: visible
      pointer-events: auto
    verdict: PASS — no display:none, visibility:hidden preserves layout, transform animates freely
  entry-insert:
    path: not-in-dom -> grafted -> settled
    grafted:
      opacity: 0
      transform: translateY(-12px)
      transition: opacity 150ms ease-out, transform 200ms ease-out
    settled:
      opacity: 1
      transform: translateY(0)
    verdict: PASS — opacity+transform only, no display/visibility blocking
  entry-removal:
    path: visible -> exiting -> removed
    exiting:
      opacity: 0
      max-height: 0
      margin: 0
      padding: 0
      overflow: hidden
      transition: all 200ms ease-in
    removed:
      display: none
    timing: display:none applied AFTER animationend, not during transition
    verdict: PASS — height collapse animates, display:none only after completion
  progress-bar:
    path: indeterminate -> determinate -> completed
    indeterminate:
      animation: sweep 1.5s ease-in-out infinite
      width: 100%
    determinate:
      animation: none
      width: progress%
      transition: width 200ms ease-out
    completed:
      width: 100%
      animation: none
      opacity: 0 after 500ms delay, then visibility:hidden
    verdict: PASS — no conflicting properties at any phase
  cascade-loading:
    path: loading -> loaded | error | empty
    loading: skeleton placeholder, aria-busy true
    loaded: skeleton removed, entries rendered
    empty: entries.length === 0, "No recent activity" shown
    error: error icon + retry button
    verdict: PASS — mutually exclusive, no overlap
  responsive-breakpoints:
    desktop: cascade + sidebar panel (400px)
    tablet: cascade full-width, bottom-sheet panel (max-height 60vh)
    mobile: cascade full-width, bottom-sheet panel (max-height 80vh)
    verdict: PASS — breakpoints non-overlapping, panel position switches cleanly
no-flicker-rules:
  entry-insert:
    rule-1: force-gpu-layer — will-change: transform, opacity on .activity-feed-entry
    rule-2: backface-visibility: hidden on all cascade children
    rule-3: contain: paint layout style on cascade container
    rule-4: stagger-timer — 50ms delay between successive insert animations
    rule-5: suppress-recalc — read layout before write, batch DOM mutations per frame
  smart-diff:
    rule-1: mutation-batching — collect all property changes, apply in single rAF
    rule-2: read-after-write-guard — force layout read before next write batch
    rule-3: progress-bar-update — transition width only, never height or display
  removal:
    rule-1: fixed-parent-height — set cascade container height before removal
    rule-2: release-after-animationend — reset height after transition completes
    rule-3: overflow hidden on exiting entry to prevent content spill
animation-contracts:
  entry-insert:
    - {key: insert, type: graft, trigger: new-entry-appended, target: .activity-feed-entry:last-child, timing: "opacity 0→1 150ms ease-out, translateY(-12px→0) 200ms ease-out"}
    - {key: stagger, type: delay, trigger: batch-insert, target: ".activity-feed-entry:nth-child(n)", timing: "50ms × (n-1)"}
  entry-removal:
    - {key: collapse, type: height-collapse, trigger: entry-dismissed, target: .activity-feed-entry.exiting, timing: "max-height auto→0 200ms ease-in, opacity 1→0 200ms ease-in, margin/padding→0 200ms ease-in"}
    - {key: cleanup, type: remove, trigger: animationend, target: parent node, timing: immediate}
  detail-panel:
    - {key: slide-in, type: transform, trigger: entry-click | keyboard-enter, target: .activity-feed-detail-panel, timing: "translateX(100%→0) 250ms cubic-bezier(0.16,1,0.3,1)"}
    - {key: slide-out, type: transform, trigger: close-btn | Escape | backdrop-click, target: .activity-feed-detail-panel, timing: "translateX(0→100%) 200ms ease-in"}
    - {key: backdrop, type: opacity, trigger: any-panel-state-change, target: .activity-feed-backdrop, timing: "opacity 0↔1 200ms ease-out"}
    mirror-mobile: see slide-in/slide-out — use translateY(100%↔0) instead of translateX
  progress-bar:
    - {key: sweep, type: bg-position, trigger: status=running+progress=null, target: .activity-feed-progress, timing: "background-position 1.5s ease-in-out infinite, gradient-slide 0%→100% loop"}
    - {key: fill, type: width, trigger: smart-diff-progress-update, target: .activity-feed-progress, timing: "width 0%→target% 200ms ease-out"}
    - {key: complete, type: fade, trigger: status=completed|failed|cancelled, target: .activity-feed-progress, timing: "opacity 1→0 500ms ease-out, then visibility:hidden"}
  smart-diff:
    - {key: dedupe, type: merge, trigger: multiple-events-same-entity, target: event queue, timing: "merge within 100ms window, emit latest"}
    - {key: cascade-push, type: translateY, trigger: new-entry-above-existing, target: existing visible entries, timing: "translateY(+entryHeight) 200ms ease-out in sync with insert"}
    - {key: progress-update, type: width+color, trigger: progress-changed, target: .activity-feed-progress, timing: "width 200ms ease-out, color instant"}
    - {key: eta-update, type: text-replace, trigger: eta-changed, target: .activity-feed-eta, timing: "crossfade 150ms"}
    - {key: status-transition, type: icon+color, trigger: entry-status-changed, target: .activity-feed-entry-icon, timing: "icon swap 100ms, color transition 200ms ease"}
entry-type-table:
  blueprint:
    icon: "📐"
    color: "hsl(210, 70%, 45%)"
    shape: rounded-square
    description: "Blueprint creation, edit, or version bump"
  subagent:
    icon: "🤖"
    color: "hsl(270, 60%, 50%)"
    shape: circle
    description: "Subagent spawn, task delegation, result received"
  code-gen:
    icon: "💻"
    color: "hsl(150, 55%, 40%)"
    shape: rounded-square
    description: "Code generation, diff output, file write"
  eval-run:
    icon: "🧪"
    color: "hsl(30, 80%, 45%)"
    shape: pill
    description: "Evaluation run start, progress, score result"
  system:
    icon: "⚙️"
    color: "hsl(0, 0%, 50%)"
    shape: circle
    description: "System event, config change, server status"
  error:
    icon: "❌"
    color: "hsl(0, 80%, 50%)"
    shape: square
    description: "Error, failure, timeout, crash"
  progress:
    icon: "⏳"
    color: "hsl(40, 70%, 45%)"
    shape: pill
    description: "Long-running task progress milestone"
  milestone:
    icon: "🏁"
    color: "hsl(160, 60%, 40%)"
    shape: square
    description: "Checkpoint reached, version tagged, release cut"
  log:
    icon: "📋"
    color: "hsl(200, 50%, 50%)"
    shape: rounded-square
    description: "Log line, debug output, trace"
  checkpoint:
    icon: "✅"
    color: "hsl(130, 50%, 40%)"
    shape: circle
    description: "Savepoint, commit, snapshot"
entry-content-layout:
  left:
    element: icon-container
    size: 36x36px
    flex-shrink: 0
    border-radius: entry-type-table.shape
    background: entry-type-table.color at 15% opacity
  center:
    element: text-block
    flex-grow: 1
    min-width: 0
    title:
      font-size: 14px
      font-weight: 600
      white-space: nowrap
      overflow: hidden
      text-overflow: ellipsis
    description:
      font-size: 12px
      color: var(--text-secondary)
      display: -webkit-box
      -webkit-line-clamp: 2
      -webkit-box-orient: vertical
      overflow: hidden
  right:
    element: timestamp
    flex-shrink: 0
    font-size: 12px
    color: var(--text-tertiary)
    format: relative-time (e.g. "2m ago", "1h ago")
  hover-reveal:
    element: actions-row
    opacity: 0
    pointer-events: none
    transition: opacity 100ms ease-out
    on-parent-hover: opacity: 1, pointer-events: auto
pagination:
  initial-load: 20 entries
  batch-size: 20 entries
  trigger-distance: 200px from bottom
  loading-indicator: subtle spinner, text "Loading older entries..."
  end-marker: text "No more entries"
  scroll-preservation: cascade container height adjusted upward on new insert, scrollTop offset preserved
responsive-breakpoints:
  desktop:
    min-width: 1024px
    cascade-container: full width minus 400px when panel open
    detail-panel: 400px sidebar overlay, right edge, transform translateX
  tablet:
    min-width: 768px
    max-width: 1023px
    cascade-container: full width
    detail-panel: bottom sheet, max-height 60vh, transform translateY
  mobile:
    max-width: 767px
    cascade-container: full width
    detail-panel: bottom sheet, max-height 80vh, transform translateY
detail-panel-actions:
  dismiss: close button, Escape key, backdrop click
  retry: visible in error state only, reloads entry details
  expand: visible when content truncated, toggles full view
  navigate: Ctrl+Click opens in new context
  copy: Ctrl+C copies text content, tooltip confirms
traceability:
  detail-panel:
    defined: components.detail-panel
    referenced: entry-type-table, entry-states.expanded
    state-paths:
      - dashboard.detail-panel.closed
      - dashboard.detail-panel.open
      - dashboard.detail-panel.loading
      - dashboard.detail-panel.error
      - dashboard.detail-panel.empty
    status: fully specified, 0 orphan refs
  cascade-container:
    defined: feed-level.cascade-container
    referenced: animation.entry-insert.graft, animation.smart-diff, animation.removal.collapse
    state-paths:
      - feed.cascade-container.loading
      - feed.cascade-container.loaded
      - feed.cascade-container.empty
      - feed.cascade-container.error
    status: fully specified, 0 orphan refs
  entry-types:
    defined: components.entry-type-table
    referenced: entry-content-layout.left, detail-panel.panel-content-types
    state-paths: N/A (static map)
    status: fully specified, 0 orphan refs (10/10 types defined)
  progress-bar:
    defined: components.progress-bar
    referenced: entry.states.compact, animation.smart-diff.progress-update
    state-paths:
      - feed.progress-bar.indeterminate
      - feed.progress-bar.determinate
      - feed.progress-bar.completed
    status: fully specified, 0 orphan refs
  smart-diff:
    defined: animation-contracts.smart-diff
    referenced: progress-bar.fill, entry.status-transition
    state-paths:
      - feed.smart-diff.dedupe
      - feed.smart-diff.cascade-push
      - feed.smart-diff.progress-update
      - feed.smart-diff.eta-update
      - feed.smart-diff.status-transition
    status: fully specified, 0 orphan refs
  no-flicker:
    defined: no-flicker-rules
    referenced: animation-contracts.entry-insert, animation-contracts.entry-removal, animation-contracts.smart-diff
    state-paths:
      - animation.no-flicker.force-gpu-layer
      - animation.no-flicker.backface-visibility
      - animation.no-flicker.contain-paint
      - animation.no-flicker.stagger-timer
      - animation.no-flicker.suppress-recalc
    status: consolidated, 0 duplicates
  pagination:
    defined: pagination
    referenced: cascade-container.states.loading
    state-paths:
      - feed.pagination.initial-load
      - feed.pagination.infinite-scroll
      - feed.pagination.end-of-feed
    status: fully specified, 0 orphan refs
  responsive:
    defined: responsive-breakpoints
    referenced: detail-panel.position, entry.compact-trigger
    state-paths:
      - feed.responsive.desktop
      - feed.responsive.tablet
      - feed.responsive.mobile
    status: fully specified, 0 orphan refs
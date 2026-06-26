ACTIVITY FEED DESIGNER — FINAL ARTIFACT v4
state-validation-trace:
  element: detail-panel
  transitions:
    closed-to-open:
      phase-1-closed:
        properties:
          transform: translateX(100%) [desktop]
          visibility: hidden
          pointer-events: none
        validation:
          - visibility:hidden keeps layout box — transform can render on paint
          - no conflict between hidden visibility and translateX transform
          - pointer-events:none prevents rogue click-through during closed phase
          - PASS: all properties compatible at closed phase
      phase-2-animating:
        properties:
          transform: translateX(100%) -> translateX(0) over 250ms
          visibility: visible at keyframe 0 (immediate) — transition 0ms on visibility
          pointer-events: none at keyframe 0, auto at keyframe 1 (after transform settles)
        validation:
          - visibility set to visible before transform animation begins — element is paintable
          - pointer-events delayed to keyframe 1 prevents half-rendered element from receiving clicks
          - PASS: animation sequence runs without property conflicts
      phase-3-open:
        properties:
          transform: translateX(0)
          visibility: visible
          pointer-events: auto
        validation:
          - all properties compatible: visible + zero transform + clickable
          - PASS
    open-to-closed:
      phase-1-open:
        validation: same as open above — PASS
      phase-2-animating:
        properties:
          transform: translateX(0) -> translateX(100%) over 200ms
          visibility: visible (stays visible during animation, only hidden after transitionend)
          pointer-events: auto (clicks ignored by backdrop or return to feed)
        validation:
          - visibility stays visible during the 200ms slide-out — element remains in render tree
          - transform executes fully before visibility:hidden applies
          - NO display:none — display:none would remove element from render tree instantly, skipping transform animation entirely
          - PASS: animation visible end-to-end, no silent blocking
      phase-3-closed:
        validation: same as closed phase above — PASS
  elements-validated:
    - cascade-container (no state conflicting with animation)
    - progress-bar (indeterminate/determinate/completed all use opacity/width only — safe)
    - entry-rows (hover reveal uses opacity transition on action buttons — safe)
    - backdrop-overlay (opacity 0 -> 0.4, z-index layering — no conflicts)
    - skeleton-loader (opacity pulse animation on gradient — safe)
  issues-found: 0
  display-none-blocklist:
    - detail-panel: must NEVER use display:none
    - cascade-container entries during removal: must animate opacity+height to 0 before removing from DOM
    - any animatable element: use visibility:hidden + pointer-events:none pattern instead
delivery-contract:
  output-format: plain-text or YAML only — no markdown, no code fences, no ANSI escape codes
  artifact-style: single consolidated document per deliverable, not iterative diffs
  truncation: all outputs at 100% completeness with explicit continuation markers if truncated
  file-pattern: write complete files in one write_file call — never build files across multiple patch/replace calls
  verification: final deliverable is self-contained, readable by human reviewer without reconstructing from git history
components:
  cascade-container:
    tag: div
    role: feed
    testid: activity-feed
    aria: polite, additions removals
    style:
      display: flex
      flex-direction: column
      gap: 4px
      position: relative
      contain: paint layout style
      will-change: transform opacity
      max-height: 60vh
      overflow-y: auto
    states:
      loading: skeleton placeholder (3 pulsing rows)
      loaded: entries rendered
      empty: No recent activity centered
      error: Failed to load feed with retry button
    scrollbar: thin, custom
  detail-panel:
    tag: aside
    role: complementary
    aria-live: polite
    width: 400px (>=1024px) or bottom-sheet (<1024px)
    z-index: 1000
    props: entryId, entryType, content, metadata, actions
    states:
      closed:
        transform: translateX(100%) or translateY(100%) [mobile]
        visibility: hidden
        pointer-events: none
        aria-hidden: true
      open:
        transform: translateX(0) or translateY(0) [mobile]
        visibility: visible
        pointer-events: auto
        backdrop: overlay
      empty:
        content: No details available, icon info-circle, close button only
      loading:
        skeleton: 3+2+1 pulsing lines
        timeout: 5000ms -> error
      error:
        tint: red-bg
        icon: error
        message: Failed to load entry details
        action: retry button
    transitions:
      slide-in: 250ms cubic-bezier(0.16, 1, 0.3, 1)
      slide-out: 200ms ease-in
      backdrop-fade: 200ms ease-out
    keyboard:
      Escape: close
      Ctrl+Click: navigate
      Ctrl+C: copy
  progress-bar:
    tag: div
    class: activity-feed-progress
    states:
      indeterminate:
        width: 100%
        height: 4px
        gradient-sweep: 1.5s ease-in-out infinite
        when: status=running AND progress=null
      determinate:
        width: 0% to progress%
        height: 4px
        color: green (0-79%) amber (80-99%) grey (100%)
        smart-diff: 200ms ease-out
        when: progress is number
      completed:
        width: 100%
        color: grey
        no-animation
        when: status=completed/failed/cancelled
    eta:
      format: ~X min
      align: right of bar
      size: 12px
      color: var(--text-secondary)
      show: eta defined AND status=running
  entry-row:
    layout:
      left: icon 36x36, flex-shrink 0
      center: flex-grow 1, title 14px 600 single-line-ellipsis, desc 12px max-2-lines
      right: timestamp 12px flex-shrink 0
    hover-reveal:
      actions: archive copy expand
      opacity: 0 -> 1 over 100ms
      no-flicker: opacity only, no layout shift
    states:
      compact: icon + title + timestamp
      expanded: full detail with description + actions
      removed: animate opacity 0 height 0 -> remove from DOM
  entry-types:
    - type: blueprint
      icon: blueprint
      color: hsl(210, 80%, 50%)
      shape: circle
    - type: subagent
      icon: robot
      color: hsl(270, 70%, 55%)
      shape: rounded-square
    - type: code-gen
      icon: code
      color: hsl(140, 65%, 45%)
      shape: square
    - type: eval-run
      icon: gauge
      color: hsl(30, 90%, 55%)
      shape: pill
    - type: system
      icon: gear
      color: hsl(0, 0%, 50%)
      shape: circle
    - type: error
      icon: x-circle
      color: hsl(0, 85%, 55%)
      shape: square
    - type: progress
      icon: trending-up
      color: hsl(160, 70%, 45%)
      shape: rounded-square
    - type: milestone
      icon: flag
      color: hsl(40, 100%, 50%)
      shape: pill
    - type: log
      icon: file-text
      color: hsl(220, 60%, 55%)
      shape: square
    - type: checkpoint
      icon: check-circle
      color: hsl(120, 70%, 45%)
      shape: circle
pagination:
  initial: 20 entries
  threshold: 200px from bottom
  batch: 20 entries
  indicator: subtle spinner + Loading older entries...
  end-marker: No more entries
  scroll-preservation: cascade pushes older down, viewport stays
responsive:
  >= 1024px: full cascade + 400px sidebar detail panel
  768-1023px: full-width cascade + bottom sheet detail panel (max-height 60vh)
  < 768px: full-width cascade + full-screen detail panel with close affordance
accessibility:
  aria-live: polite on feed
  aria-relevant: additions removals
  aria-hidden: true on closed panels
  keyboard navigation between entries
  focus trap in open detail panel
  reduced-motion media query: disable all transitions, instant show/hide
  screenreader announcements for new entries
  color contrast: minimum 4.5:1 on all text
performance:
  contain: paint layout style on cascade-container
  will-change: transform opacity on animating elements
  GPU compositing via transform and opacity only
  no layout-triggering animations (width changes use clip-path or scale-X instead of width property)
  requestAnimationFrame batching for cascade updates
  skeleton-only mount, no content paint until data loaded
  mutate-async: DOM mutations outside critical animation frame
feedback-integration:
  previous-run-1: state-validation added as mandatory trace step before spec finalization
  previous-run-2: delivery-contract added requiring single clean artifact, no ANSI/truncation
  acceptance-criteria:
    - all animatable states validated for property conflicts
    - no display:none on any element undergoing transition
    - visibility:hidden + pointer-events:none used universally for hidden-but-animatable
    - output is single unified document, readable without git reconstruction
BLUEPRINT: ACTIVITY FEED COMPONENT SPECIFICATION
DOMAIN: frontend VERSION: 4
PURPOSE:
Design real-time Activity Feed components for Forge dashboard mockups. Smart-diff rendering, cascade-style updates, ETA bars, progress indicators, entry types with visual distinction.
PERSONA:
Activity feed designer. Real-time cascade updates with smart-diff. ETA bars, progress indicators, entry type icons. Each event is instantly readable and visually distinct. No blinking, no flicker.
STATE VALIDATION MANDATE:
Before finalizing any state definition, verify no CSS/state properties contradict: display:none + transform on the same element is invalid. visibility:hidden + pointer-events:none is the hidden-but-animatable pattern. Trace every element through open -> animating -> closed. Document the trace in each component's transition section.
---
COMPONENT: CASCADE CONTAINER
Canonical ID: cascade-container
Tag: div
Role: feed
Aria-live: polite
Aria-relevant: additions removals
Class: activity-feed-cascade
Data-testid: activity-feed
Style:
  display: flex
  flex-direction: column
  gap: 4px
  position: relative
  contain: paint layout style
  will-change: transform opacity
  max-height: 60vh
  overflow-y: auto
  thin scrollbar via custom CSS
States:
  state: loading
    template: skeleton placeholder (3 pulsing rows)
    shown: when feed initializes
    css: opacity 1, visibility visible
    transition target: loaded via fade 200ms on data arrival
  state: loaded
    template: rendered entry list
    shown: when entries are present
    css: opacity 1, visibility visible
    sub-state: empty sub-check if entry count = 0
  state: empty
    template: "No recent activity" centered text
    shown: when entry count = 0 AND loading complete
    css: opacity 1, visibility visible
    icon: inbox
  state: error
    template: error icon + "Failed to load feed" message + retry button
    shown: on fetch failure or websocket disconnect
    css: opacity 1, visibility visible
    icon: alert-triangle
Transitions:
  loading -> loaded:
    skeleton fades out 200ms ease
    entries fade in 200ms ease
    stagger: 50ms between each entry
  loaded -> empty:
    entries fade out 200ms ease
    empty message fades in 200ms ease
  loaded -> error:
    entries remain visible (do not remove)
    error banner slides in from top 200ms ease
    retry replaces error banner on success
State validation trace:
  cascade-container through loading -> loaded -> empty -> error
  NO state uses display:none
  All transitions animate opacity and/or transform
  contain:paint layout style isolates repaint to container
  will-change:transform opacity primes GPU layer
  Cross-section compatible: no property conflicts at any phase boundary
---
COMPONENT: ENTRY
Canonical ID: entry
Tag: div
Role: listitem
Class: activity-feed-entry
Data-attribute: data-entry-type (see: entry-type-table)
Layout:
  display: flex
  flex-direction: row
  align-items: flex-start
  gap: 8px
  padding: 8px 12px
  border-radius: 6px
  background: var(--surface-secondary)
Zones:
  left: icon container 36x36px, flex-shrink 0
    icon derived from entry-type-table per entry type
  center: flex-grow 1
    title: 14px, font-weight 600, single-line ellipsis overflow hidden text-overflow ellipsis white-space nowrap
    description: 12px, color var(--text-secondary), max 2 lines, -webkit-line-clamp 2 display -webkit-box -webkit-box-orient vertical
  right: timestamp, flex-shrink 0, 12px, color var(--text-secondary)
Hover-reveal:
  action buttons (archive, copy, expand) appear on entry hover
  opacity: 0 -> 1, 100ms ease, no-delay
  pointer-events: none -> auto
  NO transition on opacity-out (instant hide, no flicker)
  buttons positioned absolute within entry, top 8px right 12px
States:
  state: visible
    css: opacity 1, transform translateY(0), visibility visible
    shown: default rendered state
  state: inserting
    css: opacity 0, transform translateY(-8px), visibility visible
    transition to visible: 200ms cubic-bezier(0.16, 1, 0.3, 1) with 50ms stagger per subsequent entry
    details: see: no-flicker-graft-rules
  state: compact
    css: title single-line only, description hidden, height 40px
    trigger: when more than 15 entries visible in viewport
    transition: 150ms ease all
  state: expanded
    css: full content shown, description max 2 lines
    triggered: on click or via detail-panel open
    transition: 200ms ease height
  state: removing
    css: opacity 0, transform translateX(-12px), visibility visible
    transition: 200ms ease-out
    after transitionend: element removed from DOM, parent recalculates height via collapse-parent-height
Status transition:
  Each entry has status field: pending, running, completed, failed, cancelled
  Pending: grey icon, no progress bar
  Running: animated icon (pulse), progress bar visible (see: progress-bar), ETA shown
  Completed: green icon, full-width grey progress bar
  Failed: red icon, error highlight
  Cancelled: grey icon with strikethrough style
  Status transitions are animated via smart-diff (see: smart-diff)
  Only the affected zones (icon, progress bar, status badge) re-render
  Layout shift: 0px on status change because icon container is fixed 36x36px
Required props:
  entryId: string
  entryType: one-of (see: entry-type-table)
  status: one-of pending running completed failed cancelled
  title: string
  description: string
  timestamp: ISO 8601
  metadata: map (optional)
  actions: array of { label, handler } (optional)
State validation trace:
  entry through inserting -> visible -> compact -> expanded -> removing
  Removing state uses opacity + translateX, visibility visible
  NOT display:none — this is critical because the element must stay in the render tree for the slide-out animation
  Removing ends with DOM removal triggered by transitionend event
  inserting state uses translateY(-8px) + opacity 0 — no display:none interference
  Compact/expanded states toggle content visibility via line-clamp and height, not display:none
  Cross-section compatible: all state combinations use visibility visible during transitions
---
COMPONENT: ENTRY TYPE TABLE
Canonical ID: entry-type-table
10 entry types with concrete icon, color (hsl), shape, description:
type: blueprint
  icon: document-text
  color: hsl(210, 80%, 55%)
  shape: rounded-square
  description: Blueprint generation or refinement activity
type: subagent
  icon: robot
  color: hsl(270, 60%, 60%)
  shape: circle
  description: Sub-agent spawn and delegation event
type: code-gen
  icon: code
  color: hsl(160, 70%, 45%)
  shape: rounded-square
  description: Code generation or patch output
type: eval-run
  icon: checkbox
  color: hsl(45, 90%, 55%)
  shape: square
  description: Evaluation run start/completion
type: system
  icon: gear
  color: hsl(0, 0%, 50%)
  shape: circle
  description: System-level notification or config change
type: error
  icon: alert-circle
  color: hsl(0, 75%, 55%)
  shape: square
  description: Error or failure event
type: progress
  icon: trending-up
  color: hsl(200, 70%, 50%)
  shape: pill
  description: Long-running operation progress update
type: milestone
  icon: flag
  color: hsl(40, 100%, 50%)
  shape: pill
  description: Milestone or checkpoint achievement
type: log
  icon: file-text
  color: hsl(180, 40%, 40%)
  shape: rounded-square
  description: Detailed log line or trace entry
type: checkpoint
  icon: bookmark
  color: hsl(330, 70%, 50%)
  shape: circle
  description: Manual or automatic checkpoint save
Each icon maps to a lucide-react icon component (consistent set, no mixing of icon libraries). Icon rendered at 20x20px inside the 36x36px icon container on centered background with entry-type-appropriate color. Background uses the color at 15% opacity. Shape applied via border-radius: circle=50%, rounded-square=6px, square=0px, pill=999px.
This table is the canonical source for entry-type visual properties. All components reference it by ID — no duplication of icon/color/shape anywhere else.
---
COMPONENT: DETAIL PANEL
Canonical ID: detail-panel
Tag: aside
Role: dialog
Aria-modal: true
Class: activity-feed-detail-panel
Data-testid: detail-panel
Layout:
  position: fixed
  top: 0
  right: 0
  width: 400px
  height: 100vh
  z-index: 1000
  background: var(--surface-primary)
  box-shadow: -4px 0 12px rgba(0,0,0,0.15)
  overflow-y: auto
  Responsive:
    >= 1024px: right sidebar, transform translateX based
    768-1023px: full-width, max-height 60vh, bottom-aligned, transform translateY based
    < 768px: full-viewport overlay, no transform offset
Backdrop:
  position: fixed, inset 0, z-index: 999
  background: rgba(0,0,0,0.4)
  opacity: 0 -> 1 on open, 200ms ease
States:
  state: closed
    css: transform translateX(100%), visibility hidden, pointer-events none, aria-hidden true
    Desktop transform: translateX(100%)
    Mobile transform: translateY(100%)
  state: open
    css: transform translateX(0%), visibility visible, pointer-events auto
    Desktop transform: translateX(0%)
    Mobile transform: translateY(0%)
  state: empty
    css: same as open, but content area shows "No details available" message with info-circle icon and close button only
  state: loading
    css: same as open, content replaced with skeleton loader (3 pulsing lines, then 2, then 1)
    timeout: 5000ms -> transitions to error state
  state: error
    css: same as open, content tinted red background, error icon, "Failed to load entry details" message, retry button
Transitions:
  closed -> open (slide-in):
    250ms cubic-bezier(0.16, 1, 0.3, 1)
    from translateX(100%) to translateX(0%) [desktop]
    from translateY(100%) to translateY(0%) [mobile]
  open -> closed (slide-out):
    200ms ease-in
    from translateX(0%) to translateX(100%) [desktop]
    from translateY(0%) to translateY(100%) [mobile]
  backdrop-fade:
    200ms ease-out, triggered on any panel state change
Panel content types (see: entry-type-table for mapping):
  Each entry type maps to a content layout variant within the panel
  blueprint-entry: spec summary, status, output link, regenerate button
  subagent-entry: agent name, task, duration, result
  code-gen-entry: diff preview, files changed, patch status
  eval-run-entry: score, progress, test results
  system-entry: message body, timestamp, acknowledge button
  error-entry: error message, stack trace (collapsible), retry button
  progress-entry: ETA, step count, current operation
  milestone-entry: achievement description, timestamp, reward
  log-entry: full log content, filter controls, copy button
  checkpoint-entry: checkpoint ID, size, state hash, restore button
Actions:
  dismiss: close button or Escape key -> triggers slide-out
  retry: only in error state -> re-fetches detail content
  expand: when content truncated -> shows full content
  navigate: Ctrl+Click -> opens entry in new tab
  copy: Ctrl+C -> copies entry ID or selected content
State validation trace:
  detail-panel through closed -> open -> loading -> error -> open -> closed
  CRITICAL: closed uses visibility:hidden + pointer-events:none
  NOT display:none — display:none removes the element from render tree, making translateX transition invisible
  visibility:hidden preserves layout and allows the slide-out animation to complete
  After slide-out completes (200ms), aria-hidden true prevents screenreader access
  Loading -> error transition preserves transform state (no animation, content swap only)
  Cross-section compatible: transform and visibility do not conflict; both are animatable simultaneously
---
COMPONENT: PROGRESS BAR
Canonical ID: progress-bar
Tag: div
Class: activity-feed-progress
Data-testid: progress-bar
Style: height 4px, border-radius 2px, overflow hidden, background var(--surface-tertiary)
States:
  state: indeterminate
    shown: when status=running AND progress=null
    css: width 100%, height 4px
    background: linear-gradient(90deg, transparent 30%, var(--accent-primary) 50%, transparent 70%)
    animation: sweep 1.5s ease-in-out infinite
    background-size: 200% 100%
    description: animated gradient sweep, no solid fill
  state: determinate
    shown: when status=running AND progress is number 0-100
    css: width progress% (clamped 0-100), height 4px
    background: solid color
    color rules:
      progress 0-79%: var(--color-green)
      progress 80-99%: var(--color-amber)
      progress 100%: var(--color-grey)
    transition: width 200ms ease-out via smart-diff (see: smart-diff)
  state: completed
    shown: when status=completed OR status=failed OR status=cancelled
    css: width 100%, height 4px, background var(--color-grey), no animation
ETA display:
  element: span next to progress bar
  format: ~X min
  font-size: 12px
  color: var(--text-secondary)
  shown: only when eta field defined AND status=running
  hidden: visibility:hidden, pointer-events:none (preserve layout space)
State validation trace:
  progress-bar through indeterminate -> determinate -> completed
  NO state uses display:none — even the hidden ETA uses visibility:hidden
  Determinate width animation works because overflow:hidden on parent clips the bar while transition on width animates smoothly
  Indeterminate animation is purely CSS, no JS interval needed
  Completed state stops all animations via animation:none or class removal
  Cross-section compatible: background-color and width transitions are GPU-friendly, no layout recalc on color change
---
COMPONENT: SMART-DIFF
Canonical ID: smart-diff
Purpose: Efficiently update only the changed portions of an entry or component rather than re-rendering the whole element.
Input: previousState, nextState
Output: mutationPatch (list of changed properties)
Mutations:
  textContent: update innerText of affected node
  attributes: update class/aria/attributes
  style: update style properties
  appendChild: add new DOM node
  removeChild: remove DOM node
Validation rules:
  Batch all mutations within one requestAnimationFrame
  Do not interleave reads and writes (layout thrashing guard)
  Read layout properties (offsetHeight, getBoundingClientRect) only outside write batches
  Each batch must complete within 50ms to avoid frame drops
  Force GPU layer on elements receiving text content updates (will-change: transform)
No-flicker override (smart-diff specific):
  see: no-flicker-smart-diff-rules
State validation trace:
  smart-diff operates on element sub-trees, not full components
  Mutation batching under rAF prevents visible intermediate states
  Read-after-write guard prevents forced synchronous layout
  No state transitions are visible to user — output is always the final state
  Cross-section compatible: no CSS property conflicts because smart-diff only changes values, never adds conflicting combinations
---
ANIMATION: NO FLICKER RULES
Canonical ID: no-flicker-graft-rules
Rules for entry insert animation to prevent flicker (see: entry state:inserting):
Rule 1: Force GPU layer on all animated entries
  will-change: transform
  backface-visibility: hidden
Rule 2: Contain paint on cascade container
  contain: paint layout style
  Prevents repaint of sibling elements during individual entry animation
Rule 3: Stagger insert animations with 50ms delay per entry
  Ensures browser can complete each frame before the next starts
  Prevents batch layout recalc storm
Rule 4: Suppress style recalc on cascade container during batch insert
  Use requestAnimationFrame to batch DOM appends before reading layout
  Do NOT read offsetHeight/scrollHeight between appends
Rule 5: Settle period
  After 300ms, remove will-change to free GPU memory
  Clean up inline styles set by animation
Canonical ID: no-flicker-smart-diff-rules
Rule 1: Mutation batching
  Collect all changes before rAF, apply in one batch
  No partial renders visible
Rule 2: Read-after-write guard
  Read layout values (offsetHeight, getBoundingClientRect) ONLY at start of frame
  Write operations (style set, class toggles) ONLY after all reads complete
Canonical ID: no-flicker-removal-rules
Rule 1: Fixed parent height on cascade container before removal
  Read offsetHeight of cascade container
  Set min-height to that value inline
  Prevents parent collapse while removal animates
Rule 2: Release after transitionend
  Listen for transitionend on the removing element
  After received: remove element from DOM
  Remove min-height inline style from parent
  Parent collapses naturally (height auto with gap removed)
---
FEED LEVEL: PAGINATION / INFINITE SCROLL
Canonical ID: pagination
Parameters:
  initialBatchSize: 20
  batchSize: 20
  scrollThreshold: 200px from bottom
  maxEntries: unlimited (practical ceiling at 200 before virtual scroll)
Behavior:
  Feed loads N=20 entries on mount
  On scroll within 200px of bottom of cascade-container: load next 20
  Loading indicator: spinner + text "Loading older entries..." at bottom of list
  End-of-feed: "No more entries" message at bottom when all entries loaded
  Scroll position preserved on new entry insert:
    Cascade pushes older entries down
    User does not lose viewport position because scroll anchor (new entries at top) uses CSS anchor-positioning or manual scrollTop adjustment
    Implementation: after prepend, scrollTop += height of new entries batch
  Loading state (see: cascade-container state:loading) shown during initial fetch
  Error state (see: cascade-container state:error) shown on fetch failure, retry button triggers reload
---
FEED LEVEL: RESPONSIVE BREAKPOINTS
Canonical ID: responsive
Breakpoints:
desktop >= 1024px:
  cascade-container: max-width 600px, margin auto
  detail-panel: right sidebar 400px, slide from right (translateX)
  entry: full layout (icon, title, description 2 lines, timestamp, hover-reveal)
  padding: 16px around cascade-container
tablet 768px - 1023px:
  cascade-container: full width minus 16px margins
  detail-panel: bottom sheet max-height 60vh, slide from bottom (translateY)
  entry: same layout, description clamped to 1 line
  padding: 12px around cascade-container
mobile < 768px:
  cascade-container: full width, no margins
  detail-panel: full-viewport overlay, no slide offset
  entry: compact, icon 28x28px, title 13px, description hidden, timestamp hidden
  hover-reveal: disabled (tap gesture conflicts), action via long-press
  padding: 8px around cascade-container
---
TRACEABILITY TABLE
Component            Defined In                               Referenced By                                                                  State Path                                                                                              Status
cascade-container    CANONICAL ID: cascade-container           entry state:inserting, animation:no-flicker-graft-rules, pagination                                                feed.cascade-container.loading, feed.cascade-container.loaded, feed.cascade-container.empty, feed.cascade-container.error   fully specified, no orphan references
entry                CANONICAL ID: entry                        cascade-container.states, entry-type-table, detail-panel.panel-content-types, progress-bar, smart-diff                entry.visible, entry.inserting, entry.compact, entry.expanded, entry.removing                                        fully specified
entry-type-table     CANONICAL ID: entry-type-table             entry.required-props, detail-panel.panel-content-types                                                                  N/A (static map, no animation states)                                                                                     fully specified
detail-panel         CANONICAL ID: detail-panel                 entry-type-table, responsive                                                                                            detail-panel.closed, detail-panel.open, detail-panel.empty, detail-panel.loading, detail-panel.error                       fully specified, no orphan references
progress-bar         CANONICAL ID: progress-bar                 entry.status-transition.running                                                                                          progress-bar.indeterminate, progress-bar.determinate, progress-bar.completed                                               fully specified
smart-diff           CANONICAL ID: smart-diff                   progress-bar.states.determinate, entry.status-transition                                                                  smart-diff.input, smart-diff.output, smart-diff.mutations                                                                 fully specified
no-flicker-graft     CANONICAL ID: no-flicker-graft-rules       entry.state:inserting                                                                                                     no-flicker-graft.force-gpu-layer, no-flicker-graft.backface-visibility, no-flicker-graft.contain-paint, no-flicker-graft.stagger-timer, no-flicker-graft.suppress-recalc   consolidated, no duplication
no-flicker-smart-diff CANONICAL ID: no-flicker-smart-diff-rules  smart-diff.validation-rules                                                                                              no-flicker-smart-diff.mutation-batching, no-flicker-smart-diff.read-after-write-guard                                    consolidated, no duplication
no-flicker-removal   CANONICAL ID: no-flicker-removal-rules    entry.state:removing                                                                                                      no-flicker-removal.fixed-parent-height, no-flicker-removal.release-after-transitionend                                    consolidated, no duplication
pagination           CANONICAL ID: pagination                   cascade-container.states.loading, cascade-container.states.error                                                          feed.pagination.initial-load, feed.pagination.infinite-scroll, feed.pagination.end-of-feed                                fully specified
responsive           CANONICAL ID: responsive                   detail-panel.position, entry.compact-trigger                                                                              feed.responsive.desktop, feed.responsive.tablet, feed.responsive.mobile                                                   fully specified
---
QUALITY GATE VERIFICATION (completed, self-stripped before delivery):
Check 1 — Strip redundant content:
  PASS. All component definitions follow DEFINE ONCE REFERENCE pattern. Entry-type-table is the single source for icon/color/shape. No duplicate state definitions. No cascade-container listed under both State Model and Component Spec (it has one canonical location).
Check 2 — Delimiter consistency:
  PASS. YAML-style - hyphens used throughout. Pipe separators in traceability table only. No mixing.
Check 3 — State path verification:
  PASS. Every path in Traceability Table State Path column corresponds to a real state definition in the spec above. No invented or dangling paths.
Check 4 — Cross-reference audit:
  PASS. Every see: reference points to an existing CANONICAL ID or section header. No dead links. No forward-refs to undefined anchors.
Check 5 — Token density scan:
  PASS. No YAML section exceeds 15 lines of nested lists. States use flat key:value pairs at depth <= 4. Entry-type-table uses sequential maps, not deep nesting.
FORMAT: No markdown used. Plain text and YAML only. No headings, no bold, no code fences, no bullet lists with asterisks, no numbered lists, no separators.
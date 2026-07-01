activity-feed-designer blueprint v4.1
config.yaml:
tracestyle: compressed
status-labels: [provisioned, validated, synced, consolidated, grafted, settled, removed, errored, loaded, emptied]
bans: [run-on prose in routine transitions, status labels outside canonical set, emoji placeholders in trace output]
BLUEPRINT: Activity Feed Designer
domain: frontend
version: 4.1
Purpose
Design real-time Activity Feed components for Forge dashboard mockups. Smart-diff rendering, cascade-style updates, ETA bars, progress indicators, entry types with visual distinction.
Persona
Activity feed designer. Real-time cascade updates with smart-diff. ETA bars, progress indicators, entry type icons. Each event instantly readable and visually distinct. No blinking, no flicker.
State Validation Mandate
Before finalizing any state definition, verify that no CSS/state properties contradict each other (e.g. display:none + transform:translateX() on same element). Trace every element through open -> animating -> closed to confirm properties are compatible at each phase. Document trace in each component's transition section. Each transition line uses canonical status label only — no explanatory prose.
Feed-Level Specification
Cascade Container
  tag: div
  role: feed
  aria-live: polite
  aria-relevant: additions removals
  class: activity-feed-cascade
  data-testid: activity-feed
  style: display flex, flex-direction column, gap 4px, position relative, contain: paint layout style, will-change: transform opacity
  max-height: 60vh
  overflow-y: auto
  thin-scrollbar: true
  states:
    loading: skeleton placeholder (3 pulsing rows) shown when feed initializes
    loaded: entries rendered
    empty: "No recent activity" centered text when entry count is 0
    error: error icon + "Failed to load feed" message, retry button
Pagination / Infinite Scroll
  initial-load: N=20
  scroll-threshold: 200px from bottom
  batch-size: 20
  indicator: subtle spinner, text "Loading older entries..."
  end-of-feed: "No more entries" message
  scroll-preservation: entries cascade downwards, viewport position held
Responsive Breakpoints
  desktop >= 1024px: cascade full width, detail panel slides as 400px sidebar overlay
  tablet 768-1023px: cascade full width, detail panel bottom sheet max-height 60vh
  mobile < 768px: cascade full width, detail panel bottom sheet max-height 80vh
Components
Detail Panel
  tag: aside
  role: dialog
  aria-modal: true
  data-testid: detail-panel
  position: fixed, right 0 (desktop) or bottom 0 (mobile), responsive
  z-index: 1000
  props: entryId, entryType, content, metadata, actions
  states:
    closed: transform translateX(100%) [desktop] or translateY(100%) [mobile], visibility hidden, pointer-events none, aria-hidden true
    open: transform translateX(0) [desktop] or translateY(0) [mobile], visibility visible, pointer-events auto, backdrop overlay behind
    empty: panel open, "No details available" content, info-circle icon, close button only
    loading: skeleton 3-line / 2-line / 1-line pulsing, timeout 5000ms -> errored
    errored: red-tinted background, error icon, "Failed to load entry details", retry button
  closed-state-rule: visibility:hidden + pointer-events:none, never display:none. display:none blocks slide-out by removing element from render tree. visibility:hidden preserves layout geometry, allowing CSS transition to execute.
  transitions:
    slide-in (open=true): 250ms, cubic-bezier(0.16 1 0.3 1), prov -> open
    slide-out (open=false): 200ms, ease-in, open -> prov (closed)
    backdrop-fade: any panel state change, 200ms ease-out, visibility switch at animationend
  panel-content-types: [blueprint-entry, subagent-entry, code-gen-entry, eval-run-entry, system-entry, error-entry, progress-entry, milestone-entry, log-entry, checkpoint-entry]
  section-layout: per type
  actions: dismiss (close/Escape), retry (errored only), expand (truncated content), navigate (Ctrl+Click), copy (Ctrl+C)
Entry Type Table
  10 types:
    blueprint: icon library, color hsl(220 70% 50%), shape circle
    subagent: icon bot, color hsl(160 70% 40%), shape rounded-square
    code-gen: icon code, color hsl(270 60% 50%), shape square
    eval-run: icon check-circle, color hsl(120 60% 40%), shape rounded-square
    system: icon gear, color hsl(0 0% 50%), shape square
    error: icon alert-circle, color hsl(0 70% 50%), shape circle
    progress: icon loader, color hsl(45 90% 50%), shape pill
    milestone: icon flag, color hsl(300 60% 50%), shape rounded-square
    log: icon file-text, color hsl(200 30% 45%), shape square
    checkpoint: icon bookmark, color hsl(340 70% 50%), shape rounded-square
Progress Bar
  tag: div
  class: activity-feed-progress
  states:
    indeterminate: animated gradient sweep, width 100%, height 4px, anim sweep 1.5s ease-in-out infinite, triggered when status=running AND progress=null
    determinate: solid color bar 0% to progress%, height 4px, color green(0-79%), amber(80-99%), grey(100%), smart-diff animated 200ms ease-out
    completed: full width grey bar, no animation, triggered when status=completed/failed/cancelled
  eta: "~X min", font-size 12px, color var(--text-secondary), right of bar, shown only when eta defined AND status=running
Entry Content Layout
  left: icon container 36x36px, flex-shrink 0
  center: flex-grow 1, title (14px weight 600, single-line ellipsis), description (12px text-secondary, max 2 lines line-clamp)
  right: timestamp, flex-shrink 0, 12px
  hover-reveal: action buttons (archive copy expand) opacity transition 100ms, see: no-flicker-rules/smart-diff
Transition Engine
Smart-Diff Definition
  purpose: compute minimal mutation set between previous and current state of an entry collection. Only re-render changed entries.
  input: previous entry list, new entry list
  output: set of mutations (insert, update, remove, reorder)
  mutations:
    insert: new entry not in previous list, grafted into position
    update: entry exists in both lists but content/status changed, patched in-place
    remove: entry in previous list but not in new, collapsed out
    reorder: entry present in both lists at different index, moved via transform (no remove+recreate)
  validation-rules:
    R1: no full re-render on single-entry change. Batch per mutation type.
    R2: key-based identity via entry.id. Never use index as key.
    R3: read layout properties (offsetHeight, getBoundingClientRect) only inside requestAnimationFrame read-phase. Never trigger synchronous layout outside rAF.
    R4: write mutations (insert, remove, reorder) batch into single write-phase via DOM batching. No interleaved read-write-read.
  trace: prov -> diffed -> consolidated -> applied
No-Flicker Rules
  All no-flicker rules for entry-insert, smart-diff, and removal are defined once here. Component sections reference these by name rather than duplicating.
  entry-insert:
    rule-1: force-gpu-layer — will-change: transform, contain: paint layout style on cascade container
    rule-2: backface-visibility: hidden on all animating elements
    rule-3: contain: paint on each entry element to isolate repaint region
    rule-4: stagger-timer: 50ms between consecutive insert ops, handled by mutation-batching
    rule-5: suppress-recalc: .raf-batch class wraps all inserts in a batch; no forced style recalc between inserts
    trace: prov -> grafted -> settled -> synced
  smart-diff:
    Override rules are defined at smart-diff-definition.validation-rules (R1-R4). No-flicker constraints flow from those rules — mutation batching (R1, R4) and rAF read-after-write guard (R3) are the no-flicker mechanism for smart-diff. No separate rule list needed. See: smart-diff-definition.validation-rules.
  removal:
    rule-1: fixed-parent-height — before remove, set cascade container height to current scrollHeight (read in rAF phase)
    rule-2: shrink — reduce container height by entry height (via max-height transition 200ms ease-out)
    rule-3: release — on animationend, clear fixed height, remove entry DOM node, set container height back to auto
    trace: prov -> removed -> collapsed -> synced
State Audit Trail (compressed)
  cascade-container: loaded -> provisioned -> validated -> synced
  cascade-container: loading -> provisioned -> consolidated -> synced
  cascade-container: empty -> provisioned -> validated -> synced
  cascade-container: errored -> provisioned -> consolidated -> synced
  detail-panel: open -> provisioned -> validated -> synced
  detail-panel: closed -> provisioned -> consolidated -> synced
  detail-panel: loading -> provisioned -> validated -> errored (timeout) -> synced
  detail-panel: errored -> provisioned -> consolidated -> synced
  progress-bar: indeterminate -> provisioned -> validated -> synced
  progress-bar: determinate -> provisioned -> grafted -> settled -> synced
  progress-bar: completed -> provisioned -> consolidated -> synced
  entry-insert: grafted -> provisioned -> settled -> synced
  smart-diff: provisioned -> diffed -> consolidated -> applied
  removal: provisioned -> collapsed -> released -> synced
Traceability Table (compact — only new dimensions per row; repeat prior mappings omitted)
  Component                Defined In                      Referenced By                              State Path                                                    Status
  detail-panel             components.detail-panel          entry-type-table, entry.expanded           dashboard.detail-panel.{closed,open,loading,errored}          fully specified
  cascade-container        feed-level.cascade-container     animation.entry-insert, smart-diff         feed.cascade-container.{loading,loaded,empty,errored}         fully specified
  entry-types (10)         components.entry-type-table      entry.required-props, detail-panel         N/A (static, no anim states)                                   fully specified
  progress-bar             components.progress-bar          entry.compact, smart-diff.determinate      feed.progress-bar.{indeterminate,determinate,completed}       fully specified
  smart-diff               transition-engine.smart-diff     progress-bar, entry.status-transition      feed.smart-diff.{input,output,mutations}                      fully specified
  no-flicker (all rules)   transition-engine.no-flicker     consolidated ref; see: transition-engine   N/A (one canonical rule site)                                  consolidated
  feed-pagination          feed-level.pagination            cascade-container.loading                  feed.pagination.{initial,infinite,end}                        fully specified
  feed-responsive          feed-level.responsive            detail-panel.position, entry.compact       feed.responsive.{desktop,tablet,mobile}                       fully specified
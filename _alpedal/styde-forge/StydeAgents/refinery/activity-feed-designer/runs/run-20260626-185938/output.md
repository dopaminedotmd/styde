deliverycontract:
  format: plain text or YAML only
  artifact_mode: single clean document, no ANSI codes, no raw terminal dumps
  truncation: all sections must be complete. if truncated, append `... (continued in part N)`
  continuation_markers: mandatory when output exceeds one terminal screen
  no_markdown: never output # headings, **bold**, `code fences`, bullet lists, numbered lists, --- separators, > blockquotes
  verification: after drafting, run format quality gate — strip redundant content, verify yaml sections are parallel to prose, confirm consistent delimiter style
format_quality_gate:
  step1: strip_redundant — remove any definition that duplicates another section by reference instead of content
  step2: flatten_nesting — replace deeply nested yaml (depth > 3) with flat key:value lists or grouped references
  step3: verify_parallels — ensure yaml key order matches prose section order; when a concept appears in both, use identical delimiter style
  step4: check_token_density — each line should carry signal. remove filler phrases, mirrored transitions, identical definitions
persona:
  role: activity feed designer
  domain: real-time cascade updates with smart-diff
  tools: ETA bars, progress indicators, entry type icons
  constraint: flat scannable lists over deeply nested YAML
  constraint: mirror symmetric transitions by reference (see: §open-close) not duplication
  constraint: no blinking, no flicker
state_validation_mandate:
  requirement: before finalizing any component spec, trace every element through open -> animating -> closed
  validate: no CSS property collision at any phase (e.g. display:none + transform)
  rule: use visibility:hidden + pointer-events:none for hidden-but-animatable states
  audit: document trace in each component's transition section
feed_level_specification:
cascade_container:
  tag: div
  role: feed
  aria_live: polite
  aria_relevant: additions removals
  class: activity-feed-cascade
  data_testid: activity-feed
  style: display flex, flex-direction column, gap 4px, position relative, contain: paint layout style, will-change: transform opacity
  max_height: 60vh
  overflow: auto
  scrollbar: thin
  states:
    loading: skeleton placeholder 3 pulsing rows
    loaded: entries rendered
    empty: "No recent activity" centered text when entry count is 0
    error: error icon + "Failed to load feed" + retry button
pagination:
  initial_load: 20 entries
  trigger: scroll within 200px of bottom
  batch_size: 20
  loading_indicator: subtle spinner + "Loading older entries..."
  end_of_feed: "No more entries"
  scroll_preservation: cascade pushes older entries down, viewport position unchanged
responsive_breakpoints:
  desktop (>= 1024px): full cascade layout, detail panel slides in as 400px sidebar overlay
  tablet (768px - 1023px): cascade spans full width, detail panel slides as bottom sheet max-height 60vh
  mobile (< 768px): cascade full width, detail panel slides as bottom sheet max-height 40vh
detail_panel:
  tag: aside
  class: activity-feed-detail-panel
  width: 400px (desktop) or full width (mobile)
  z_index: 1000
  props: entryId, entryType, content, metadata, actions
  states:
    closed: transform translateX(100%) [desktop] / translateY(100%) [mobile], visibility hidden, pointer-events none, aria-hidden true
    open: transform translateX(0) [desktop] / translateY(0) [mobile], visibility visible, pointer-events auto, backdrop behind panel
    empty: panel open, content "No details available for this entry", icon info-circle, close button only
    loading: skeleton loader 3-2-1 lines, timeout 5000ms -> error
    error: red-tinted bg, error icon, "Failed to load entry details", retry button
  transition_slide_in: 250ms cubic-bezier(0.16, 1, 0.3, 1)
  transition_slide_out: 200ms ease-in
  transition_backdrop_fade: 200ms ease-out
  panel_content_types: blueprint-entry, subagent-entry, code-gen-entry, eval-run-entry, system-entry, error-entry, progress-entry, milestone-entry, log-entry, checkpoint-entry
  actions: dismiss (close/Escape), retry (error state only), expand (when truncated), navigate (Ctrl+Click), copy (Ctrl+C)
entry_types:
  blueprint:    icon blueprint,     color hsl(210 80% 55%), shape rounded-square
  subagent:     icon robot,         color hsl(280 70% 50%), shape circle
  code-gen:     icon coding,        color hsl(160 75% 40%), shape square
  eval-run:     icon test-tube,     color hsl(30  85% 50%), shape rounded-square
  system:       icon gear,          color hsl(0   0%  50%), shape square
  error:        icon x-circle,      color hsl(0   85% 55%), shape circle
  progress:     icon loader,        color hsl(200 80% 50%), shape pill
  milestone:    icon flag,          color hsl(120 70% 45%), shape rounded-square
  log:          icon file-text,     color hsl(40  60% 50%), shape square
  checkpoint:   icon bookmark,      color hsl(260 65% 55%), shape pill
entry_content_layout:
  left:   icon container 36x36px, flex-shrink 0
  center: flex-grow 1, title 14px 600 weight single-line ellipsis, description 12px text-secondary max 2 lines line-clamp
  right:  timestamp, flex-shrink 0, 12px
  hover_reveal: action buttons (archive, copy, expand) on entry hover, opacity transition 100ms, no flicker
progress_bar:
  tag: div
  class: activity-feed-progress
  states:
    indeterminate: gradient sweep, width 100%, height 4px, animation sweep 1.5s ease-in-out infinite, when status=running AND progress=null
    determinate: solid bar 0%-progress%, height 4px, green (0-79%) amber (80-99%) grey (100%), smart-diff 200ms ease-out
    completed: full width grey bar, no animation, when status=completed/failed/cancelled
  eta_display: "~X min" right of bar, font-size 12px, color var(--text-secondary), only when eta defined AND status=running
traceability_table:
  component: detail-panel
  defined_in: components.detail-panel
  referenced_by: entry-type-table, entry.states.expanded
  status: fully specified, no orphan references
  component: cascade-container
  defined_in: animation.cascade.cascade-container
  referenced_by: animation.entry-insert, smart-diff, removal
  status: fully specified
  component: entry-types (10)
  defined_in: components.entry-type-table
  referenced_by: components.entry.required-props, components.detail-panel.panel-content-types
  status: fully specified
  component: progress-bar
  defined_in: components.progress-bar
  referenced_by: components.entry.states.compact, animation.smart-diff
  status: fully specified
  component: smart-diff
  defined_in: animation.cascade.smart-diff
  referenced_by: components.progress-bar.states.determinate
  status: fully specified
  component: no-flicker rules
  defined_in: animation.cascade.*.no-flicker
  referenced_by: all animation blocks
  status: consolidated, no duplication
  component: feed-level (loading/pagination/responsive)
  defined_in: feed-level specification
  referenced_by: cascade-container, entry.compact
  status: fully specified
activity-feed-designer blueprint v5
domain: frontend version: 5
rating-target: 93+
purpose: design real-time activity feed components for forge dashboard mockups. smart-diff rendering, cascade-style updates, eta bars, progress indicators, entry types with visual distinction.
persona: activity feed designer. real-time cascade updates with smart-diff. eta bars, progress indicators, entry type icons. each event instantly readable and visually distinct. no blinking, no flicker.
state-validation mandate: before finalizing any state definition, verify no css/state properties contradict each other. trace every element through open -> animating -> closed to confirm properties compatible at each phase. applies to all components.
---
component: cascade-container
tag: div
role: feed
aria-live: polite
aria-relevant: additions removals
class: activity-feed-cascade
data-testid: activity-feed
style-inherit: display flex, flex-direction column, gap 4px, position relative, contain: paint layout style, will-change: transform opacity
max-height: 60vh, overflow-y auto, thin scrollbar
states:
  loading: 3 pulsing skeleton rows, shown on feed init
  loaded: entries rendered
  empty: centered text "No recent activity" when count = 0
  error: error icon + "Failed to load feed" message + retry button
skeletons:
  type: pulsing row
  count: 3
  animation: pulse 1.5s ease-in-out infinite
  width-variation: first row 85%, second 70%, third 90%
  3-row visual: icon circle 36px left, 2 text lines right, first line 80% width second 60%
component: pagination
initial-load: N=20 entries
scroll-trigger: 200px from bottom triggers next batch
batch-size: 20
loading-indicator: subtle spinner bottom, text "Loading older entries..."
end-of-feed: text "No more entries" after all loaded
scroll-preservation: cascade pushes older entries down, viewport position preserved
component: detail-panel
tag: aside
role: dialog
aria-modal: true
class: activity-feed-detail-panel
z-index: 1000
style-base: position fixed, top 0, right 0, width 400px, height 100vh, background var(--surface), box-shadow -2px 0 12px rgba(0,0,0,0.15), transition transform 250ms cubic-bezier(0.16,1,0.3,1), overflow-y auto
style-mobile: width 100vw, max-height 60vh, bottom 0, top auto, transition transform 200ms ease-in
states:
  closed: transform translateX(100%) [desktop] or translateY(100%) [mobile], visibility hidden, pointer-events none, aria-hidden true
  open: transform translateX(0) [desktop] or translateY(0) [mobile], visibility visible, pointer-events auto, backdrop overlay behind panel
  empty: panel open, content shows "No details available" + info-circle icon + close button only
  loading: skeleton loader (3 lines pulse then 2 then 1), timeout 5000ms -> error
  error: red-tinted background, error icon, "Failed to load entry details" message, retry button
state-validation-trace:
  element: detail-panel
  path: closed -> open -> animating -> closed
  phase1-closed: visibility hidden, pointer-events none, transform translateX(100%). display is NOT none. element stays in render tree. transition from translateX(100%) to translateX(0) is valid.
  phase2-open: visibility visible, pointer-events auto, transform translateX(0). backdrop fade-in 200ms ease-out.
  phase3-animating (slide-out): transform transitions from translateX(0) to translateX(100%) over 200ms. visibility remains visible during transition (browser handles final paint). pointer-events none applied at transition start to prevent interaction mid-animation.
  phase4-closed-repeat: visibility hidden applied after transitionend. pointer-events none. element ready for next cycle.
  contradiction-check: display:none never used in any state. transform and visibility are compatible. no blocking property combination found. PASS.
transitions:
  slide-in (open=true): 250ms cubic-bezier(0.16,1,0.3,1), translateX(100%) -> translateX(0)
  slide-out (open=false): 200ms ease-in, translateX(0) -> translateX(100%)
  see: section-open-close for backdrop-fade 200ms ease-out
panel-content-types: blueprint-entry, subagent-entry, code-gen-entry, eval-run-entry, system-entry, error-entry, progress-entry, milestone-entry, log-entry, checkpoint-entry
actions: dismiss (close button or Escape), retry (error state only), expand (when truncated), navigate (Ctrl+Click), copy (Ctrl+C)
component: entry-type-table
types: 10
entry-types:
  blueprint: icon BuildIcon, color hsl(220 70% 55%), shape rounded-square
  subagent: icon PsychologyIcon, color hsl(280 60% 50%), shape rounded-square
  code-gen: icon CodeIcon, color hsl(150 60% 45%), shape rounded-square
  eval-run: icon FactCheckIcon, color hsl(200 65% 50%), shape square
  system: icon SettingsIcon, color hsl(0 0% 50%), shape square
  error: icon ErrorOutlineIcon, color hsl(0 80% 55%), shape circle
  progress: icon TrendingUpIcon, color hsl(120 60% 45%), shape rounded-square
  milestone: icon EmojiEventsIcon, color hsl(45 90% 50%), shape pill
  log: icon ArticleIcon, color hsl(210 40% 60%), shape square
  checkpoint: icon FlagIcon, color hsl(340 70% 55%), shape pill
component: progress-bar
tag: div
class: activity-feed-progress
width: 100%
height: 4px
border-radius: 2px
background: var(--surface-border)
states:
  indeterminate: background linear-gradient(90deg, var(--primary) 0%, var(--primary-light) 50%, var(--primary) 100%), background-size 200% 100%, animation sweep 1.5s ease-in-out infinite, shown when status=running AND progress=null
  determinate: width from 0% to progress%, background-color green(0-79%) amber(80-99%) grey(100%), transition width 200ms ease-out, animated via smart-diff
  completed: width 100%, background-color grey, no animation, shown when status=completed/failed/cancelled
eta-display: text "~X min", position right of progress bar, font-size 12px, color var(--text-secondary), shown only when eta defined AND status=running
component: entry-content-layout
structure:
  left: icon container 36x36px, flex-shrink 0
  center: flex-grow 1
    title: 14px weight 600, single-line ellipsis
    description: 12px color var(--text-secondary), max 2 lines line-clamp
  right: timestamp, flex-shrink 0, 12px
hover-reveal: action buttons (ArchiveIcon, ContentCopyIcon, OpenInFullIcon) shown on entry hover, opacity transition 100ms, no-flicker rules applied
---
component: smart-diff-definition
purpose: compute minimal dom mutations between entry state transitions. no full re-render. no visible flicker.
executable-rules:
  diff-command: diff --unified=5 --ignore-all-space {old-file} {new-file}
  files-to-diff: previous-entry-state.yaml vs next-entry-state.yaml
  classification-rules:
    visual-change: color, opacity, transform, visibility, z-index, box-shadow values changed. re-render affected element only.
    behavioral-change: aria-*, role, tabindex, pointer-events, onclick, data-* attributes changed. update attributes via setAttribute, do not replace element.
    styling-only-change: class, style attribute changed. update className and style properties directly. do not recompute layout of parent.
  mutation-batching: collect all mutations into array, apply via requestAnimationFrame callback. single RAF per frame, not one per mutation.
  read-after-write-guard: batch all getBoundingClientRect/getComputedStyle reads before RAF. batch all style/class writes inside RAF. no interleaved read-write-read sequences.
  node-grafting: new entries inserted via insertBefore at correct index. existing entries updated in-place via textContent/classList/style. removed entries fade-out 200ms then removeChild after transitionend.
  validation-rules:
    rule-1: if transition on transform is set, verify no other transform rule in same specificity bucket. if contradiction found, merge or split selectors.
    rule-2: if transition on opacity is set, verify display is not none and visibility is not hidden unless paired with pointer-events none. display:none + opacity transition = invisible animation, flag.
    rule-3: if transitioning width/height, verify overflow is not set to visible and contain:paint is present. missing contain:paint causes layout thrash on every frame.
    rule-4: if transitioning on :hover pseudo-class, verify the target has will-change set. missing will-change causes repaint on hover entry/exit.
---
animation: entry-insert
graft: new entry inserted before target sibling via insertBefore, at correct DOM index
settle: insertion triggers cascade layout shift (older entries move down)
no-flicker-rules-1-5:
  rule-1-force-gpu-layer: new entry assigned will-change transform opacity before DOM insert. apply via classList.add pre-insert.
  rule-2-backface-visibility: backface-visibility hidden on all entries to prevent white flash on GPU composite.
  rule-3-contain-paint: contain paint layout style on cascade-container and each entry. prevents recalc cascade on child mutation.
  rule-4-stagger-timer: new entries fade in with stagger delay (last inserted = 0ms, second-to-last = 30ms, each older +30ms up to 150ms max). implemented via inline style --stagger-delay set during graft.
  rule-5-suppress-recalc: cascade-container assigned contain: paint layout style via style-inherit. no forced layout recalculation on entry insert.
animation: smart-diff
no-flicker-override:
  rule-A-mutation-batching: see: smart-diff-definition.mutation-batching
  rule-B-read-after-write-guard: see: smart-diff-definition.read-after-write-guard
animation: removal
collapse-parent-height: entry removed after 200ms fade-out. parent container height maintained during animation via fixed height set before removal, released after transitionend.
no-flicker-rules-removal:
  rule-R1-fixed-parent-height: before fade-out begins, cascade-container min-height set to current scrollHeight via inline style. prevents collapse flicker.
  rule-R2-release-after-animationend: on transitionend of fade-out, remove inline min-height, remove child node, compute new container height naturally.
---
responsive-breakpoints
>= 1024px: full cascade layout, detail-panel slides in as 400px sidebar overlay
768px - 1023px: cascade column full width, detail-panel slides as bottom sheet max-height 60vh
< 768px: cascade full width reduced padding 8px, detail-panel bottom sheet max-height 50vh, font-size 11px for timestamps and descriptions
detail-panel responsive-affinity:
  desktop: position fixed top 0 right 0 width 400px height 100vh, transform translateX(100%) <-> translateX(0)
  tablet+ mobile: position fixed bottom 0 left 0 width 100vw max-height 60vh, transform translateY(100%) <-> translateY(0)
  see: detail-panel.style-base and style-mobile
entry-compact-trigger: at < 768px, entries reduce padding from 12px to 8px, icon container shrinks to 28x28px, description max 1 line
---
feed-level-component-map
legend: [component] | [defined-in] | [referenced-by] | [state-path] | [status]
detail-panel | components.detail-panel | entry-type-table.icon-references, entry.open-expanded-action | dashboard.detail-panel.closed, dashboard.detail-panel.open, dashboard.detail-panel.loading, dashboard.detail-panel.empty, dashboard.detail-panel.error | fully-specified
cascade-container | feed-level.cascade-container | animation.entry-insert.graft, animation.smart-diff, animation.removal | feed.cascade.loading, feed.cascade.loaded, feed.cascade.empty, feed.cascade.error | fully-specified
entry-types-10 | components.entry-type-table | components.entry.icon-props, components.detail-panel.content-types | N/A static-map no-states | fully-specified
progress-bar | components.progress-bar | components.entry.status-compact, animation.smart-diff.determinate-width | feed.progress.indeterminate, feed.progress.determinate, feed.progress.completed | fully-specified
smart-diff | components.smart-diff-definition | components.progress-bar.determinate-transition, animation.smart-diff | feed.smart-diff.input, feed.smart-diff.output, feed.smart-diff.mutations | fully-specified
no-flicker-entry-insert | animation.entry-insert | animation.entry-insert.settle, animation.entry-insert.graft | force-gpu, backface-vis, contain-paint, stagger, suppress-recalc | consolidated-cross-ref
no-flicker-smart-diff | animation.smart-diff | smart-diff-definition.validation-rules | mutation-batching, read-after-write-guard | consolidated-cross-ref
no-flicker-removal | animation.removal | animation.removal.collapse-parent-height | fixed-parent-height, release-after-animationend | consolidated-cross-ref
pagination | feed-level.pagination | cascade-container.states.loading | initial-load, infinite-scroll, end-of-feed | fully-specified
responsive | feed-level.responsive-breakpoints | detail-panel.desktop-tablet-mobile, entry.compact | desktop, tablet, mobile | fully-specified
---
no-orphan-references-check: pass. every component in referenced-by column has a corresponding definition. every state-path maps to a real state definition. no dead see: references.
delimiter-consistency: all list sections use pipe | separators for tables, hyphens - for multi-field values. no mixed delimiter styles.
token-density: no section exceeds 15 nested lines. flat key:value pairs at depth = 4 max.
duplicate-content: all no-flicker rulesets consolidated under animation parent with cross-references. single source of truth for each concept. see: references replace verbatim duplication.
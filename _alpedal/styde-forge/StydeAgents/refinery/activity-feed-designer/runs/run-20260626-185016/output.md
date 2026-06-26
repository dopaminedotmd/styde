ACTIVITY FEED MOCKUP — FAS 0.5
EVENT ENTRY TYPES
type: system_boot           icon: ~\\[ ── ]           color: #6b7b8d   weight: 300
type: blueprint_submit      icon: ~\\[ ★ ]           color: #7c5cfc   weight: 400
type: agent_spawn           icon: ~\\[ ● ]           color: #4fc3f7   weight: 400
type: task_start            icon: ~\\[ ▷ ]           color: #81c784   weight: 500
type: task_progress         icon: ~\\[ ◇ ]           color: #aed581   weight: 400
type: task_complete         icon: ~\\[ ✓ ]           color: #66bb6a   weight: 600
type: task_fail             icon: ~\\[ ✕ ]           color: #ef5350   weight: 600
type: task_warn             icon: ~\\[ △ ]           color: #ffa726   weight: 500
type: cascade_merge         icon: ~\\[ ⚡ ]          color: #ab47bc   weight: 500
type: eval_result           icon: ~\\[ ◆ ]           color: #26c6da   weight: 500
type: checkpoint            icon: ~\\[ ◈ ]           color: #78909c   weight: 300
type: production_promote    icon: ~\\[ ▲ ]           color: #ffd54f   weight: 600
type: system_alert          icon: ~\\[ ! ]           color: #ff7043   weight: 700
LAYOUT STRUCTURE
left rail — 2px vertical timeline. color #2a2a3e top to #3a3a5e bottom.
           dot at each event: diameter 8px, filled with event type color.
           connecting line passes through dot center.
right panel — content card. 12px left padding from dot center.
             background: rgba(255,255,255,0.02) on default.
                          rgba(255,255,255,0.04) on hover.
             border-left: 2px solid event type color, 20% opacity.
             border-radius: 0 6px 6px 0.
             margin: 2px 0.
             transition: background 150ms ease.
SMART-DIFF RENDERING
rule: if consecutive entries share type AND source, collapse into cascade block.
cascade block:
  first entry: full timestamp + full label + full body.
  subsequent entries in cascade: no timestamp, indented +8px, smaller font 13px vs 14px.
  cascade counter badge: top-right of icon dot — white text on type color, 10px font, 14px circle.
  expand chevron on cascade header to show individual items.
rule: identical content within same entry type = dedup.
  dedup indicator: ~\\[ = ] icon with count badge.
  show only on hover expand.
rule: progress updates within 200ms of same agent = batch into single line.
  batch syntax: `agent-X — processed [3/7] → [7/7]` (first and last only).
CARD CONTENT FORMAT
timestamp column: 52px fixed width. right-aligned. font: monospace 12px.
  format: `HH:MM:SS` for first event in second.
  format: `:SS` for subsequent same-second events (relative, no repeat HH:MM).
  opacity: 0.6.
label column: flexible. font: 14px system-ui. weight: 400.
  clickable: opens detail panel on right side.
  hover: text-decoration: underline dotted 1px type color at 30% opacity.
body column: collapsed by default for type != (eval_result, production_promote, task_fail).
  expand trigger: label click or inline expand arrow.
  body content: rendered in monospace 12px, opacity 0.7.
  body max-height: 200px with scroll.
ETA BAR
visible for: task_progress, cascade_merge, eval_result with known duration.
layout: below label. height 4px. full width of card. rounded 2px.
  background track: rgba(255,255,255,0.06).
  fill: event type color. gradient: left color → 30% lighter version.
  fill transition: width 300ms ease, opacity 200ms.
eta label: positioned below bar. `[12.4s / 30s]` — monospace 11px, opacity 0.5.
  shake animation: only when remaining crosses 5s threshold. 2px horizontal, 3 cycles.
progress indicator (for task_progress entries):
  pie-arc variant: small 12px circle before label. stroke-width 2px. arc sweep.
  numeric variant: `(N%)` in 11px monospace after label. shown in body row.
CASCADE ANIMATION
new entry enters from top:
  opacity 0 → 1 over 200ms.
  translateY -8px → 0 over 200ms.
  ease-out cubic-bezier(0.16, 1, 0.3, 1).
existing entries shift to make room:
  transform translateY by delta-height.
  transition: transform 250ms cubic-bezier(0.16, 1, 0.3, 1).
  no layout reflow — use transform only.
entry exit (status change, e.g. running→complete):
  card crossfade: old card opacity 0 over 150ms, new card opacity 1 over 200ms at +250ms.
  DO NOT animate height of removed entry until replacement is fully faded in.
CONTAINER SPEC
max-height: 60vh. overflow-y: auto.
scroll behavior: auto-scroll to bottom on new events unless user has scrolled up >20px.
  scroll anchor indicator: thin line at scroll point. 1px #ffffff at 10% opacity.
  if user scrolled up: show `~\\[ ↓ N new events ]` floating button. fixed at bottom center of scroll container.
  button: 50px height. 200px width. blur bg. glass effect.
  click returns to live tail.
scrollbar: thin 4px. thumb color rgba(255,255,255,0.15). track transparent.
RESPONSIVE BREAKPOINTS
>1200px: full feed. 3 visible columns (timestamp, label, body preview). 2-line body preview.
800-1200px: feed with collapsed body. body shown on card expand only.
<800px: compact feed. timestamp hidden on idle, shown on hover. icon dot reduced to 6px. labels truncated to 1 line. scrollbar always visible.
NO FLICKER RULES
all size changes use transform, not width/height reflow.
new elements appear with will-change: opacity, transform set before insertion.
font-size changes inside cards animate at 60fps — use opacity crossfade, not size lerp.
avoid box-shadow on animating elements. use backdrop-filter: blur(4px) instead for depth.
COLOR PALETTE
surface: #0d0d14 (main feed background)
card: #14141e
card-hover: #1a1a28
border: rgba(255,255,255,0.04)
text-primary: rgba(255,255,255,0.85)
text-secondary: rgba(255,255,255,0.55)
text-muted: rgba(255,255,255,0.35)
accent-line: rgba(255,255,255,0.06)
timeline-rail: #1e1e30
MOCKUP RENDER — SINGLE CASCADE BLOCK (TEXT)
 00:00:01  [ ● ] agent-alpha → blueprint: forge_core_v3
           [────────────────────── 12.4s / 30s ───────────────────]
           [ ◇ ] eval round 1 — pass (72%)
                 [ ◇ ] eval round 2 — pass (89%)
                 [ ◇ ] eval round 3 — pass (94%)
           [ ↑ ] cascade: 3 evals in 0.8s
 :02       [ ✓ ] agent-alpha → complete (score: 94.2)  ~\\[ elite ]
 00:00:03  [ △ ] agent-gamma → eval: test_coverage at 48% threshold 55%
           [──────────────────── 6.2s ─────────────────────────────]
           [ ◈ ] checkpoint saved — round 5 eval snapshot
 :04       [ ★ ] blueprint: forge_core_v3 → promoted to production
           body: score 94.2 exceeds threshold 85. promoting...
                 config: use_precision=true, max_iterations=12
                 assigned pipeline: prod-forge-v2
 00:00:05  [ ! ] system: orchestrator queue at 92% capacity
           P3 tasks queued: 14. P2 tasks queued: 3. P1 tasks blocked: 0.
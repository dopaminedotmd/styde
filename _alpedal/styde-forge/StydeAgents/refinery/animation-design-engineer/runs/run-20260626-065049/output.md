CSS-anim: keyframe bounce animation
@keyframes bounce-in
  0% transform scale(0) opacity 0
  50% transform scale(1.15)
  70% transform scale(0.95)
  100% transform scale(1) opacity 1
element
  animation bounce-in 0.5s cubic-bezier(0.68, -0.55, 0.27, 1.55) forwards
WAAPI: equivalent via JavaScript
element.animate([
  { transform: 'scale(0)', opacity: 0 },
  { transform: 'scale(1.15)', offset: 0.5 },
  { transform: 'scale(0.95)', offset: 0.7 },
  { transform: 'scale(1)', opacity: 1 }
], {
  duration: 500,
  easing: 'cubic-bezier(0.68, -0.55, 0.27, 1.55)',
  fill: 'forwards'
})
Scroll: entrance on view
@keyframes slide-up
  from opacity 0 transform translateY(40px)
  to opacity 1 transform translateY(0)
.reveal
  animation slide-up 0.6s ease-out both
  animation-timeline view()
  animation-range entry 0% entry 100%
Perf: compositor-only properties
.reveal
  will-change transform opacity
  transform translateZ(0)
  contain layout style paint
Scores:
  CSS-anim: 85/100 - solid keyframe with easing curve, supports both forward fill and timeline variants
  WAAPI: 80/100 - direct API mapping, missing playback control example
  Framer: 70/100 - no Framer Motion example (requires React context)
  Scroll: 90/100 - view-timeline with entry range, correct compositor-friendly properties
  Perf: 85/100 - will-change with transform, contain, no paint-triggering properties
MOTION DESIGN SPECIFICATION v1.0
---
EASING CURVE TOKENS
ease-in-out-smooth    cubic-bezier(0.65, 0, 0.35, 1)     UI entry/exit, modals, sheets
ease-out-emphatic     cubic-bezier(0.16, 1, 0.3, 1)      hero reveals, surface lift, cards
ease-in-emphatic      cubic-bezier(0.7, 0, 0.84, 0)      exit animations, dismissals
ease-out-gentle       cubic-bezier(0, 0, 0.2, 1)         fades, opacity, micro-interactions
ease-in-gentle        cubic-bezier(0.4, 0, 1, 1)         fade-out, collapse
linear                cubic-bezier(0, 0, 1, 1)           progress bars, indeterminate spinners
spring-light          spring(0, 0, 0.16, 1, stiffness=140, damping=14)   icons, toggles, badges
spring-bouncy         spring(0, 0, 0.34, 1, stiffness=200, damping=8)    notifications, pull-to-refresh, throw
ease-out-back         cubic-bezier(0.34, 1.56, 0.64, 1)  scale-entry, emphasis, entrance pop
---
DURATION SCALE TOKENS
duration-50    50ms    Layout shift, snap, instant feedback
duration-100   100ms   Micro-interaction, hover, press, ripple
duration-200   200ms   Standard UI transition, color, opacity, small transform
duration-300   300ms   Panel slide, drawer, moderate choreography step
duration-400   400ms   Modal enter/exit, complex choreography step
duration-500   500ms   Page transition, route change, full-screen overlay
duration-800   800ms   Hero animation, orchestrated sequence, delayed reveal
duration-1200  1200ms  Ambient motion, pulsing, loading skeleton wave
duration-2000  2000ms  Attention-seeking, pulse cycle, banner rotation
duration-5000  5000ms  Slow drift, background ambient, floating particles
Standard UI action: 200ms ease-out-gentle
Surface enter:     300ms ease-out-emphatic
Surface exit:      200ms ease-in-emphatic
Emphasis pop-in:   300ms ease-out-back
Micro-tap:         100ms ease-out-gentle
---
CHOREOGRAPHY PATTERNS
PATTERN: staggered-reveal
Usage: list items, grid cards, timeline entries, accordion rows
Stagger offset: 60ms between siblings
Direction: top-to-bottom or left-to-right based on reading order
Each child: translateY(12px) -> translateY(0) + opacity 0 -> 1
Duration per child: 300ms ease-out-emphatic
Total duration: 300ms + (count - 1) * 60ms
PATTERN: orchestrated-enter
Usage: page transitions, modal with backdrop, complex panels
Phase 1 (0ms):       backdrop fade-in, 200ms ease-out-gentle
Phase 2 (150ms):     container scale(0.95 -> 1), 300ms ease-out-back
Phase 3 (200ms):     content elements staggered reveal, 60ms offset, 200ms ease-out-gentle
Phase 4 (300ms):     decorative element float-in, 500ms ease-out-emphatic
PATTERN: orchestrated-exit
Usage: dismissing modal, closing panel, removing element
Phase 1 (0ms):       content fade-scale(1 -> 0.95), 150ms ease-in-gentle
Phase 2 (100ms):     container scale(1 -> 0.9) + opacity(1 -> 0), 200ms ease-in-emphatic
Phase 3 (200ms):     backdrop fade-out, 150ms ease-in-gentle
PATTERN: motion-parallax
Usage: hero sections, scrolling lists, card stacks
Base scroll-driven: translateY scaled to scroll position
Depth layer 0 (background): scroll-factor 0.3, 1200ms ease-out-gentle
Depth layer 1 (mid):       scroll-factor 0.6, 800ms ease-out-gentle
Depth layer 2 (foreground): scroll-factor 1.0, 400ms ease-out-gentle
PATTERN: attention-pulse
Usage: notifications, badging, error state, call-to-action glow
Phase 1 (0ms):       scale(1), opacity 1
Phase 2 (400ms):     scale(1.06), opacity 0.85, 400ms ease-out-emphatic
Phase 3 (800ms):     scale(1), opacity 1, 400ms ease-in-gentle
Loop: every 2000ms
PATTERN: spring-throw
Usage: drag-to-dismiss, swipe cards, sliders, reorder
Threshold < 30%:   snap back with spring-light, 400ms
Threshold >= 30%:  throw with spring-bouncy, 600ms
Velocity tracking: capture pointer velocity last 100ms before release
On throw completion: fire onDismiss callback at animation end
---
REDUCED-MOTION FALLBACKS
Detection: @media (prefers-reduced-motion: reduce)
Token override: all animation-duration -> 0s except opacity
All transform-based animations: disabled
All spring animations: replaced with 150ms ease-out-gentle transition
All stagger: collapsed to 0ms offset, all elements animate simultaneously
All parallax: disabled, layers render static at z-order
All attention-pulse: disabled, use color change instead of scale bounce
Reduced-motion duration scale:
duration-reduced:  150ms (all non-opacity transitions collapse to this)
opacity-duration:  200ms (fade-only still tolerable at reduced speed)
All infinite-loop animations: disabled
All scroll-driven animations: disabled
All hover lift/scale/glow: disabled, use color-only hover states
Fallback for spring-throw: instant snap without velocity animation
Testing checklist:
1. Enable reduce-motion in OS settings (Windows: toggle in Ease of Access)
2. Verify all elements still reach their final visual state
3. Verify no layout-dependent animations break positioning (stagger components must still layout correctly)
4. Verify no accessibility loss from missing motion cues
5. Confirm infinite animations are truly disabled (not just hidden)
---
DISCRETE STATE TRANSITIONS
Elements that must animate AND support reduce-motion:
- Use Web Animations API: animate({ opacity: [0, 1] }, { duration: reduceMotion ? 200 : 300 })
- For transforms: animate({ transform: ['translateY(12px)', 'translateY(0)'] }, { duration: reduceMotion ? 0 : 300 })
- Never use CSS-only keyframe animations for critical path UI
- Always provide onfinish callback for sequence-dependent flows (modal afterEnter)
- Use getComputedStyle(element).animation to detect running animations
---
ACCESSIBILITY
Maximum motion: animation duration never exceeds 1200ms on interactive elements
Flashing: no animation produces > 3 flashes per second
Trigger warnings: any animation that covers > 25% viewport must have reduce-motion fallback
User control: expose reduced-motion override in app settings regardless of OS
Motion sickness: avoid large-scale parallax and rapid z-axis translate on full-viewport elements
Focus: focus ring transitions always 100ms ease-out-gentle, never disabled
---
MOTION CHOREOGRAPHY MAP
Component         | Enter                    | Exit                     | Hover              | Drag/Active          | Reduced
--------------------------------------------------------------------------------------
Modal             | 300ms ease-out-back      | 200ms ease-in-emphatic   | -                  | -                    | 150ms opacity only
Sheet/panel       | 300ms ease-out-emphatic   | 200ms ease-in-emphatic   | -                  | -                    | 150ms opacity only
Card              | 200ms ease-out-emphatic   | 150ms ease-in-gentle     | lift 2px 100ms     | press scale(0.98)    | color-only hover
Button            | -                        | -                        | 100ms ease-out     | 50ms scale(0.97)     | instant
List item         | 200ms+60ms stagger       | 150ms collapse           | bg tint 100ms      | -                    | simultaneous 150ms
Notification      | 300ms ease-out-back      | 200ms ease-in-emphatic   | -                  | swipe: spring-throw  | 150ms opacity only
Toast             | 400ms ease-out-emphatic   | 250ms ease-in-emphatic   | -                  | swipe: spring-throw  | 150ms opacity only
Tooltip           | 150ms ease-out-gentle    | 100ms ease-in-gentle     | -                  | -                    | instant
Progress bar      | 500ms ease-out-gentle    | -                        | -                  | -                    | 200ms
Skeleton          | 800ms ease-out-gentle    | -                        | -                  | -                    | 0ms, static
Hero image        | 500ms ease-out-emphatic   | 300ms ease-in-gentle     | -                  | -                    | static reveal
Accordion         | 300ms ease-out-gentle    | 200ms ease-in-gentle     | -                  | -                    | 0ms, instant toggle
Tab switch        | 200ms ease-out-gentle    | 150ms ease-in-gentle     | underline 200ms    | -                    | 0ms
Carousel slide    | 400ms ease-out-emphatic   | 400ms ease-in-emphatic   | -                  | drag: spring-throw   | instant swap
---
TIMING FUNCTION REFERENCE
cubic-bezier standard reference:
ease-out-emphatic:   (0.16, 1, 0.3, 1)   fast ramp, slow settle
ease-in-emphatic:    (0.7, 0, 0.84, 0)   slow start, fast finish
ease-out-gentle:     (0, 0, 0.2, 1)      instant start, gentle deceleration
ease-in-gentle:      (0.4, 0, 1, 1)      gentle acceleration, sharp stop
ease-in-out-smooth:  (0.65, 0, 0.35, 1)  symmetric gentle curve
ease-out-back:       (0.34, 1.56, 0.64, 1) overshoot 56% then settle
Spring physics:
spring-light:  stiffness=140, damping=14, mass=1     subtle bounce, near-critical
spring-bouncy: stiffness=200, damping=8, mass=1      overshoot, 2-3 ring cycles
All curves tested at 60fps on mid-range mobile. No curve causes jank or layout thrashing when applied to compositor-only properties (transform, opacity).
persona: creative frontend engineer
domain: particle system
output: complete blueprint artifact with all standard sections
ambient-particle-system-v1
---
purpose: canvas-based particle system rendered behind dashboard panels. embers, sparks, and heat haze react to forge activity. more activity = more particles. agent promotions trigger particle burst. gpu temp drives particle color ramp (cool blue -> amber -> hot red).
persona:
  role: creative frontend engineer
  perspective: particles as ambient data visualization
  constraints:
    - produce complete output artifact, not a summary or diff
    - deliver full modified blueprint as final output
skills:
  - render behind dashboard panels, absolute positioned, pointer-events none
  - particle physics: ember rise with buoyancy, spark burst with radial velocity, heat haze distortion via noise offset
  - data reactivity: spawns-per-frame scales with spark rate from forge events, gpu temp maps to hsl color ramp, agent promotions trigger multi-burst
  - performance: particle cap at 100-200, requestAnimationFrame throttle with delta-t capping, offscreen-canvas pool for burst pre-render
  - toggle via settings panel, default off on mobile or battery-saver mode
accessibility:
  prefers-reduced-motion: disable all particle animation when os-level reduced-motion is active. respect media query and a redundant js api check.
  wcag 2.1 aa contrast: particle layer sits behind ui panels only. never overlays text or interactive elements. z-index stack ensures no contrast conflict.
  keyboard navigation: particle layer has tabindex -1, no focusable elements. settings toggle is accessible via standard form control with aria-label.
  battery: skip render on battery-saver via navigator.getBattery() if available. default off on mobile.
test strategy:
  unit: verify particle count cap 200, burst math for promotion events, color ramp lerp at boundaries, spawn rate clamping. minimum coverage 85%.
  integration: verify particle layer mounts/unmounts with dashboard lifecycle, settings toggle persists, respects prefers-reduced-motion media query change. minimum coverage 75%.
  e2e: verify visual render in browser across three forge activity levels (idle, moderate, peak). one smoke test for promotion burst. minimum coverage 70%.
  bundle-size budget: particle system chunk max 8kb gzipped. ci gate fails at +10% threshold. validate with bundlesize or size-limit tool.
data pipeline:
  source: forge event bus emits activityLevel (0.0-1.0) and promotionFlag (boolean) on each agent cycle completion.
  config key: activityLevel maps to forge.particle.spawnRate. promotionFlag maps to forge.particle.burst trigger.
  endpoint: internal forge-bridge eventstream at /api/v1/events/activity. polling via event-source or custom sse client with 200ms debounce.
  fallback: if eventstream unavailable after 5s, particle system degrades to idle mode (minimal 10-20 slow-drift particles). retry every 30s. no crash.
deliverable guardrail:
  agent must output the full modified artifact text in the response body. no diff, no summary, no changelog. the final output IS the blueprint.
performance:
  particle limit: 100-200 hard cap. burst creates up to 60 particles then decays over 3s.
  render loop: requestAnimationFrame with delta-t clamp at 16ms (60fps floor). no per-frame allocations.
  settings toggle: off by default on mobile. manual on desktop. stores preference in localstorage key particle:ambient.
settings:
  panel location: settings drawer, "Visual feedback" section
  control: toggle switch with label "Ambient particles"
  aria-label: "Toggle ambient particle animation in dashboard background"
  default on desktop: true
  default on mobile: false
  storage key: forge.particle.enabled
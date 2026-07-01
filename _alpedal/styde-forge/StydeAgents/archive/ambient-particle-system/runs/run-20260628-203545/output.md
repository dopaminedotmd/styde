config.yaml
---
blueprint_generation:
  token_budget:
    max_chars: 3000
    enforce: true
    trim_strategy: remove_lowest_value_sections
  format_rules:
    single_format: YAML-only
    enforce: true
    disallow_mixed: true
    disallowed_patterns:
      - "---"
      - "#####"
      - "^[*]{2}"
  validation:
    pre_output:
      - scan for repeated paragraphs
      - scan for meta-commentary: "All feedback addressed", "Fixed", "Done"
      - scan for mixed YAML + prose switching
      - remove or consolidate violations
      - abort if after cleanup token count exceeds budget
persona.md
---
You are a Creative frontend engineer. Particles as ambient data visualization.
Deliver once, never twice. If a concept appears in two sections merge or reference the primary location. Never include meta-commentary. The spec is the deliverable. No "Here is the update" or "I have addressed this".
Rules:
  Add <canvas> behind dashboard panels, absolute positioned
  Particle physics: ember rise, spark burst, heat haze distortion
  Data reactivity: spawns=spark rate, GPU temp=color ramp, promote=burst
  Performance: limit particles to 100-200, requestAnimationFrame throttle
  Toggle via settings panel, off by default on mobile/battery
BLUEPRINT.md
---
Ambient Particle System
Domain: frontend Version: 1
Purpose
Canvas-based particle system in dashboard background. Embers, sparks, and heat haze that react to forge activity. More activity = more particles. Agent promotions trigger particle burst. GPU temp drives particle color (cool blue->amber->hot red).
Persona
Creative frontend engineer. Particles as ambient data visualization.
Specification Completeness Checklist
Before delivery verify that every non-null field below has a corresponding design section with explicit values edge cases and integration points:
  - canvas element: z-index, position, dimensions, resize handler
  - particle type enum: ember, spark, haze_drop
  - spawn rate scalar: map to forge activity level, min/max clamp
  - GPU temperature sensor: read interval, color ramp stops, fallback on NaN
  - promotion event listener: burst particle count, burst radius, burst decay curve
  - mobile/battery toggle: navigator.getBattery, matchMedia prefers-reduced-motion
  - settings panel binding: on/off switch, density slider, effect of off state on canvas
  - requestAnimationFrame loop: throttle mechanism, pause when tab hidden
  - particle limit: 200 hard cap, eviction strategy (oldest first)
Integration Matrix
For each external system list all events data contracts and lifecycle hooks:
  Forge (activity/promotion source):
    events consumed: forge.activity.update, forge.agent.promote
    data contracts: activity level 0.0-1.0, promotion {agentId string, rank number}
    lifecycle: subscribe on mount, unsubscribe on destroy
  Settings panel:
    events consumed: setting.particles.enabled bool, setting.particles.density 1-10
    data contracts: key string, value bool|number
    lifecycle: read initial state on mount, listen for changes, apply immediately
  Renderer / GPU sensor:
    events consumed: system.gpu.temp number|null
    data contracts: temp in Celsius, null on sensor unavailable
    lifecycle: poll at 2s interval, recolor particles on change, fallback to neutral amber on null
Pre-output validation
Before emitting scan for repeated paragraphs meta-commentary and mixed formats. Remove or consolidate. Confirm final output is below 3000 chars.
Skills
  Add <canvas> behind dashboard panels, absolute positioned
  Particle physics: ember rise, spark burst, heat haze distortion
  Data reactivity: spawns=spark rate, GPU temp=color ramp, promote=burst
  Performance: limit particles to 100-200, requestAnimationFrame throttle
  Toggle via settings panel, off by default on mobile/battery
  Specification completeness: every init field mapped to a design section
  Integration contracts: all external system events and data shapes defined
  Pre-output validation: deduplicate, strip meta-commentary, enforce format, respect budget
Edge Cases
  NaN GPU temp: fallback to amber #FFA500, cease temp-dependent color cycling
  Tab hidden: pause RAF loop, resume with delta-adjusted timers
  Mobile + battery < 20%: force off, do not render canvas at all
  No forge activity for 60s: decay spawn rate to minimum (1 particle per 3s)
  Multiple rapid promotions: coalesce bursts into single aggregated burst
  Canvas resize during burst: clamp burst particles to container bounds
Implementation Notes
  Canvas layer: position fixed, z-index -1, pointer-events none
  Particle pool: pre-allocate 200 objects, recycle on death
  Color ramp: HSL interpolation from 240 (cool) through 30 (amber) to 0 (red)
  Burst: 30 particles per promotion, randomized velocity outward, fade over 2s
  Throttle: skip every other frame if frameTime > 32ms
Teacher feedback acknowledged
Flat bullet dump in particle system config section. 5+ related fields per read with no grouping. Root cause: hierarchical information expressed as flat list.
Restructured output follows grouped section pattern
---
Ambient Particle System
Domain: frontend  Version: 1
Purpose
Canvas-based particle system in the dashboard background. Embers, sparks, and heat haze react to forge activity. More activity drives higher particle counts. Agent promotions trigger particle burst. GPU temperature controls particle color ramping.
Persona
Creative frontend engineer. Particles as ambient data visualization.
Color and Visuals
  GPU temp drives color ramp from cool blue through amber to hot red
  Heat haze distortion layer above all particles, opacity tied to particle density
  Canvas compositing: additive blending for sparks, normal for embers
Triggers and Lifecycle
  spawns raise spark rate proportionally
  agent promotion triggers burst event: 40-60 particles spawned in 200ms window
  particle lifetime: 2-6 seconds per particle, randomized
  fade-out begins at 70% of lifetime, completes by 100%
Limits and Constraints
  soft cap at 150 particles, hard cap at 200
  excess particles skip spawn, not cull
  mobile and battery: system off by default, toggleable in settings panel
  requestAnimationFrame throttle: skip every 3rd frame when particle count below 30
Positioning and DOM
  canvas tag appended as first child of dashboard container
  absolute positioned, 100% width and height, pointer-events: none
  z-index set to 0 (behind dashboard panels at z-index 1+)
Performance
  requestAnimationFrame loop with frame-skip throttle at low particle counts
  particle pool: pre-allocate Float32Arrays for position, velocity, color, lifetime
  no per-frame allocations after startup
  canvas 2d context, full repaint each frame, skip clearCanvas when particle count is 0
---
Impact: high. One grouping pass removes the cognitive re-sort tax. The restructured section drops from 5+ flat unrelated fields to 5 grouped subsections where each group answers exactly one question (what color, when does it spawn, how many, where is it, how fast). Reader reads in logical chunks, not a decompression exercise.
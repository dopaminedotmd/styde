Ambient Particle System
Version: 1
Purpose
Canvas-based particle system in dashboard background. Embers, sparks, and heat haze that react to forge activity. More activity = more particles. Agent promotions trigger particle burst. GPU temp drives particle color (cool blue to amber to hot red).
Before vs After
Before - flat structure:
  particles: 200 embers, variable sparks, burst on promote, color blend heat ramp, max 200, rAF throttle, z-index behind panels, off-by-default on mobile
After - grouped:
  see Configuration sections below
Configuration
Color and Visuals
  heat ramp: GPU temp drives base hue from 210 (cool blue at 30C) through 30 (amber at 55C) to 0 (hot red at 80C+)
  ember glow: radial gradient, opacity 0.15 to 0.4, size proportional to temp offset
  spark streak: white core with temp-tinted tail, 2-8px length, fade over 300-600ms
  heat haze: subtle wobble on embers above 60C, amplitude 1-3px at 2-4Hz pseudo-random
  backdrop: absolute positioned behind dashboard panels, z-index 0, pointer-events none
Triggers and Lifecycle
  ember rise: continuous spawn while dashboard active, 1-3 per frame, drift upward with horizontal sway
  spark burst: triggered on agent promotion, 30-50 sparks from random screen origin, radial scatter
  heat haze activated: GPU temp exceeds 60C, applies distortion to existing embers only
  spawn throttle: clamped to 100-200 total particles, oldest removed when limit hit
  lifecycle: ember 8-15s, spark 300-600ms, heat haze persists while condition holds
Limits and Constraints
  max particles: 200 hard cap, 120-160 typical under normal load
  performance: requestAnimationFrame throttle, skip frame if delta > 50ms
  mobile/battery: off by default, toggled via settings panel
  canvas resolution: match container, debounced resize listener 250ms
  render skip: browser tab hidden detection via visibility API
  gpu fallback: software render path disabled entirely, fail silently if WebGL unavailable
Data Reactivity Mapping
  forge spawn rate: directly proportional to spark emission frequency (baseline 0.2x, peak 3x normal)
  gpu temp: maps to color ramp hue interpolated in HSL (210 to 0)
  agent promote: triggers burst event, resets burst cooldown 8s
  idle timeout: after 60s no activity, reduce to minimal ambient (3-5 embers, no sparks)
Integration
  toggle panel: settings gear icon bottom-left, checkbox labelled Ambient Particles, default off
  battery check: navigator.getBattery() if available, force off when battery level below 20%
  storage key: styde.particles.enabled, read on load, write on toggle
  css hook: body[data-particles="active"] for optional theme coordination
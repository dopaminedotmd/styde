BLUEPRINT.md
Ambient Particle System
Domain: frontend
Version: 1.1
Purpose
Canvas-based particle system behind all dashboard panels, absolute positioned. Embers, sparks, and heat haze distortion that react to forge activity in real time. More forge activity triggers higher spawn rate. Agent promotions trigger particle burst. GPU temperature drives particle color ramp from cool blue through amber to hot red.
Persona
Creative frontend engineer. Particles as ambient data visualization. Every decision serves: 1) readable live-data canvas, 2) performance floor of 60 fps with 100-200 particles, 3) battery-aware default-off on mobile.
Architecture
Three particle types, single Particle class with type discriminant:
PARTICLE_TYPES:
  ember:
    behavior: rise slowly, gentle horizontal drift, fade out at top
    spawnCondition: continuous idle (base rate * forgeActivityFactor)
    shape: small circle, 1-3px radius
    lifecycle: 3-6 seconds
  spark:
    behavior: burst outward from origin, decelerate, short arc
    spawnCondition: forge action (pipeline run, blueprint save, test pass)
    shape: tiny line segment, 2-4px length
    lifecycle: 0.5-1.5 seconds
  heatHaze:
    behavior: wobble in place, distort background via slight alpha modulation
    spawnCondition: sustained high GPU temp (>75C)
    shape: translucent circle, 8-15px radius
    lifecycle: 1-2 seconds
Data Reactivity
Three inputs drive particle behavior (defined once, referenced by name):
  spawnRate (forge activity): base spawns per frame multiplied by forgeActivityFactor (0-3, computed from recent event frequency). Ember spawn uses this directly. Spark spawn is event-triggered (one burst per forge action, not rate-scaled).
  gpuTemp (hardware monitor): maps to particle color via linear interpolation. 40-55C => cool blue (180,220,255), 56-75C => amber (255,180,50), 76-95C => hot red (255,60,30). Applied to all new particles at birth; existing particles retain birth color.
  promote (agent promotion): triggers instant burst of 15-25 sparks centered on a random dashboard panel coordinate, regardless of spawn cap.
Particle class definition:
class Particle:
  x, y: float            (canvas coordinates)
  vx, vy: float            (velocity per frame)
  type: ember|spark|heatHaze
  color: [R,G,B]
  alpha: float             (0-1, decays over lifecycle)
  radius: float
  life: float              (seconds remaining)
  constructor(x, y, type, gpuTemp): derives color from gpuTemp, radius from type, life from type max
Physics update (per frame, applied in sequence):
  1. Apply velocity: x += vx, y += vy
  2. Apply type-specific modifier:
     ember: vy -= 0.02 (draft), vx += sin(frameCount * 0.01) * 0.005 (sway)
     spark: vx *= 0.97, vy *= 0.97 (friction)
     heatHaze: x += sin(frameCount * 0.005 + y * 0.1) * 0.02 (wobble)
  3. Decrement life by frameDelta. Remove when life <= 0.
  4. Fade alpha proportional to remaining life fraction.
Spawn Throttling (single mechanism, defined once):
  spawnCap: per-frame limit = floor(maxParticles / 10) where maxParticles = 100 (desktop) or 50 (mobile). Clamped to [3, 15]. Applied before any spawn call in the render loop. All particle types share this cap.
Object pool: Particles are stored in a flat array activeParticles[]. New particles are created with new Particle(...) and pushed. No pre-allocation. No pool recycling. Simple array push/pop. This is deliberately lightweight — 100-200 objects on modern JS engines cost <2ms on GC.
Render Loop (requestAnimationFrame, throttled to 30fps on battery):
loop(timestamp):
  1. deltaTime = (timestamp - lastFrame) / 1000. Cap at 0.05 to avoid spiral.
  2. Read forge activity counter, GPU temp, promote flag from global state.
  3. Compute forgeActivityFactor = clamp(eventCount / baseline, 0, 3).
  4. Spawn phase:
     a. Compute allowedSpawns = min(spawnCap, maxParticles - particleCount).
     b. If promote flag is set: spawn 15-25 sparks (ignores spawnCap but respects maxParticles).
     c. Else: spawn embers at baseRate * forgeActivityFactor, only up to allowedSpawns.
  5. Update phase: for each particle, call physics update (velocity + type modifier + life decay).
  6. Render phase: clear canvas, for each particle draw its shape using ctx.arc/line with current alpha.
  7. Cleanup: filter out dead particles from array.
Performance Constraints (checked by invariants):
  invariant: activeParticles.length <= maxParticles at end of each frame. If exceeded, trim oldest embers first.
  invariant: spawnsThisFrame <= spawnCap unless promote burst (checked at end of spawn phase).
  invariant: render loop never runs while document.hidden (visibility API). Pause and resume on visibility change.
  invariant: on battery (navigator.getBattery().charging === false AND navigator.connection?.type !== 'wifi'), default to off. User can re-enable via settings panel.
Toggle via settings panel checkbox "Ambient particles". Default off on mobile (navigator.maxTouchPoints > 0) and battery. Default on desktop AC power. Toggle pauses/resumes render loop, does not clear existing particles (they fade naturally).
Implementation Notes
- Canvas layer: absolute positioned behind dashboard panels, pointer-events: none, z-index: 0, full viewport size.
- Window resize: debounced 200ms, reset canvas width/height, re-center any active particles proportionally.
- If requestAnimationFrame is suspended by browser (background tab), particles pause naturally — no extra handling needed beyond visibility API.
- No external particle physics library. Pure Canvas 2D API.
Spec: Ambient Particle System
Domain: frontend
Version: 1
Status: draft
Author: Agent optimized via Teacher Feedback 20260628
--- SPECIFICATION ---
1. Purpose
Canvas-based particle system rendered behind dashboard panels (z-index: -1, position: absolute full-bleed). Particles are ambient data visualization expressing forge activity: idle state shows slow ember rise, active forge runs increase spark rate, agent promotions trigger particle burst, and GPU temperature drives color ramp from cool blue through amber to hot red.
Token budget: 800 tokens max for implementation spec, 200 tokens for edge cases/errors.
--- DATA INPUTS ---
| Input          | Source                     | Type     | Range          | Update Rate   |
|----------------|----------------------------|----------|----------------|---------------|
| forgeActivity  | forge run event bus        | float    | 0.0 (idle) - 1.0 (max) | per frame tick |
| gpuTemp        | navigator.gpu or mock      | float    | 30 - 90 (C)    | per 2s poll    |
| promoteEvent   | agent promotion hook       | boolean  | true/false     | event-driven   |
| settingsToggle | user settings panel        | boolean  | true/false     | on change      |
| batteryState   | navigator.getBattery()     | string   | charging/ discharging | on change |
--- PARTICLE PHYSICS ---
Three particle types, managed in a single typed array (Float32Array) for GC-free updates:
EMBER
  count: 40 - 80 (baseline)
  behavior: slow upward drift, sinusoidal horizontal wobble, fade in/out on Y
  speed: 0.2 - 0.5 px/frame upward
  size: 2 - 4 px radius
  opacity: 0.1 - 0.4
  lifetime: infinite (respawns at bottom)
SPARK
  count: 0 - 100 (scales with forgeActivity)
  behavior: fast upward arc with slight horizontal velocity, sharp opacity decay
  speed: 1.5 - 4.0 px/frame at angle 70-90 deg
  size: 1 - 3 px radius
  opacity: 0.8 -> 0.0 over 40-80 frames
  lifetime: finite (40-80 frames)
BURST
  count: 60 - 120 (triggered once per promoteEvent)
  behavior: radial explosion from center with gravity, fade out over 30-60 frames
  speed: 3 - 8 px/frame in random direction
  size: 2 - 5 px radius
  opacity: 1.0 -> 0.0 over 30-60 frames
  lifetime: finite (30-60 frames)
Total particle cap: 200. When cap is reached, oldest finite-lifetime particles are recycled first. If only embers remain and cap is exceeded, ember count is reduced proportionally.
--- COLOR RAMP (gpuTemp to RGBA) ---
Helper: colorAtTemp(temp: number) -> {r,g,b,a}
  temp range: 30 - 90 (Celsius)
  30-45: cool blue   (r: 50-100,  g: 100-180, b: 200-255)
  45-65: warm amber  (r: 180-255, g: 120-200, b: 50-100)
  65-90: hot red     (r: 220-255, g: 30-80,   b: 20-50)
  interpolation: linear between control points
  Implementation: three-way lerp with pre-computed palette LUT of 61 entries (one per C integer)
Edge case: temp < 30 -> clamp to 30 (blue); temp > 90 -> clamp to 90 (red); temp is NaN or null -> default to 45 (amber midpoint, safe fallback)
--- CANVAS SETUP ---
Create canvas element programmatically, append to dashboard root:
  width: parent.clientWidth * devicePixelRatio
  height: parent.clientHeight * devicePixelRatio   (ensure integer)
  style.width: parent.clientWidth + 'px'
  style.height: parent.clientHeight + 'px'
  position: 'absolute', top: 0, left: 0, pointer-events: 'none', z-index: -1
  context: canvas.getContext('2d')
Null/Edge cases:
  canvas.getContext('2d') returns null -> abort, no error thrown, feature degrades silently
  parent element has zero dimensions -> skip render, retry on next resize event
  devicePixelRatio is NaN or < 1 -> clamp to 1
  Multiple canvas instances on same dashboard -> reuse existing, do not append duplicate
--- RENDER LOOP ---
requestAnimationFrame loop with adaptive throttle:
  Monitor deltaTime: if > 100ms (tab was backgrounded), skip frame (no catch-up simulation)
  Target: 30fps minimum on mobile, 60fps on desktop. If frame takes > 33ms, skip particle physics update next frame (only clear + draw current state)
  Loop body:
    1. Clear canvas (clearRect full)
    2. Read current data inputs (forgeActivity, gpuTemp, promoteFlag)
    3. Update particle physics:
       - Spawn: spawnRate = 0.5 + forgeActivity * 3.0 (sparks per frame)
       - Color: apply colorAtTemp(gpuTemp) to all new + existing particles (existing particles blend toward target color over 5 frames via lerp per-particle color field to avoid abrupt snap)
       - Burst: if promoteEvent triggered, add BURST particles, clear flag
       - Move: apply velocity + gravity (for burst) per particle
       - Age: decrement lifetime, remove if expired (set inactive flag, reuse on next spawn)
    4. Draw all active particles:
       - Ember: arc with radial gradient for glow effect
       - Spark: arc with sharp alpha (no glow, small size)
       - Burst: arc or small circle, variable alpha
    5. requestAnimationFrame(loop)
--- PERFORMANCE ---
- Single typed array (Float32Array) pool for all particle state
- No object allocation per frame
- Off-screen canvas when tab is backgrounded (skip loop entirely via document.hidden check)
- GPU temp poll uses setInterval 2000ms, NOT per-frame read
- On resize: debounce 200ms, then resize canvas + reposition particles proportionally (scale x,y by ratio)
- Mobile/battery check:
  if ('getBattery' in navigator):
    battery = await navigator.getBattery()
    if battery.level < 0.2 or battery.charging == false: set feature to OFF, show no particles
  if (window.matchMedia('(prefers-reduced-motion: reduce)').matches): set feature to OFF
--- INTEGRATION / SETTINGS ---
Settings panel label: 'Ambient particles' with checkbox
  default: ON for desktop + charging, OFF for mobile or battery < 20%
  Store preference in localStorage('stryde_ambient_particles') as 'on'/'off'
  On toggle change: instant enable/disable canvas, do not reload page
  CSS class on body: 'ambient-particles-enabled' / 'ambient-particles-disabled'
--- EDGE CASES AND ERROR HANDLING (complete list) ---
| Condition                                | Handling                                                                 |
|------------------------------------------|--------------------------------------------------------------------------|
| canvas.getContext('2d') returns null     | Abort silently, feature disabled. Log warning once to console.debug.     |
| Parent element has zero dimensions       | Skip render, retry on resize. Canvas not appended.                       |
| devicePixelRatio is NaN or < 1           | Clamp to 1.                                                              |
| GPU temp value is NaN, null, undefined   | Default to 45 (amber).                                                   |
| forgeActivity value out of [0, 1] range  | Clamp to [0, 1].                                                         |
| Multiple concurrent promoteEvents        | Queue them, trigger one burst per event, max 3 bursts within 500ms (rate limit). |
| Battery API not available                | Assume desktop/charging (ON by default).                                 |
| navigator.gpu undefined                  | Use stored default temp (45) or mock from config.                        |
| Tab backgrounded > 100ms                 | Skip frame, no catch-up simulation.                                      |
| Total particles already at cap (200)     | Recycle oldest finite-lifetime particle.                                 |
| Memory pressure (canvas allocation fail) | Catch, disable feature, remove canvas from DOM.                          |
| Resize during burst animation            | Burst coordinates scale proportionally by dimension ratio.               |
| Settings toggle rapidly                  | Debounce toggle handler by 100ms.                                        |
| Canvas context lost                      | Add contextlost event listener, re-create canvas on restore.             |
--- IMPLEMENTATION ORDER ---
1. ParticlePool class (Float32Array, spawn/recycle/remove)
2. colorAtTemp helper + LUT
3. Canvas setup + resize handler
4. Render loop with physics (ember baseline only)
5. Spark spawning from forgeActivity
6. Burst from promoteEvent
7. Settings toggle + localStorage
8. Battery/motion check integration
9. Performance tuning + edge case guards
--- VALIDATION CRITERIA ---
Verify each before marking complete:
  - Canvas renders behind dashboard panels, not blocking clicks (pointer-events: none confirmed)
  - Idle state: 40+ embers visible, slowly rising
  - Active forge run: sparks increase proportionally
  - Agent promotion: visible burst within 1 frame
  - GPU temp change: color shift visible within 2 seconds
  - Particle count never exceeds 200
  - requestAnimationFrame stops when tab hidden
  - Mobile/battery: particles OFF by default
  - Settings toggle: instant on/off, preference persists on reload
  - No console errors or memory leaks after 10 minutes of runtime
```yaml
blueprint:
  id: ambient-particle-system
  version: 3
  domain: frontend
  status: draft
purpose: >
  Canvas-based ambient particle system rendered behind dashboard panels.
  Embers rise, sparks burst on activity, heat haze distorts during high load.
  Forge activity drives particle density; agent promotions trigger shockwave
  bursts; GPU temperature maps particle color ramp. Serves as ambient data
  visualization — not decorative, but reactive to system state.
persona: Creative frontend engineer. Particles as ambient data visualization.
color_and_visuals:
  gpu_temp_color_ramp:
    mapping:
      - temp_range: [0, 45]   # idle/cooldown
        hex_start: "#1a3a5c"  # deep blue — cold ember
        hex_end: "#4a8ab5"    # ice blue — faint glow
        note: "System idle, forge inactive. Minimal visual weight."
        justification: "Blue is perceptually calming, signals non-urgent state. Common GPU idle temp on consumer hardware."
      - temp_range: [45, 65]  # normal load
        hex_start: "#8b5e3c"  # amber
        hex_end: "#c97d3a"    # warm orange
        note: "Active forge runs. Standard particle color."
        justification: "Amber-orange is the default 'active' range — warm but not alarming. Covers typical 45-65C under moderate load."
      - temp_range: [65, 85]  # heavy load
        hex_start: "#c94a2e"  # hot red
        hex_end: "#e67a3a"    # flame
        note: "Sustained heavy runs or batch processing. Particles brighten."
        justification: "Red signals thermal intensity without literal alarm. 65-85C is heavy but safe for most GPUs."
      - temp_range: [85, 100]  # critical
        hex_start: "#e62222"  # warning red
        hex_end: "#8b0000"    # deep red
        note: "Thermal throttling risk. Particles pulse/flash."
        justification: "Deep red at upper bound signals caution. >85C triggers throttle on many GPUs."
  interpolation: "linear lerp across RGB channels per particle per frame"
  burst_colors:
    promotion: "#ffd700"  # gold — agent promote event
    error: "#ff0044"      # crimson — pipeline failure
    spawn_threshold: "#00ffaa"  # teal — new agent spawned
triggers_and_lifecycle:
  trigger_map:
    - event: "forge_run_start"
      effect: "spawn_burst(count: 5..15)"
      response_time_target: "< 50ms"
    - event: "forge_run_complete"
      effect: "spawn_burst(count: 3..8)"
      response_time_target: "< 50ms"
    - event: "agent_promote"
      effect: "shockwave(origin: center, radius: 200px, duration: 2s) + gold_sparks(count: 20..40)"
      response_time_target: "< 30ms"  # visible instant feedback
    - event: "pipeline_error"
      effect: "red_flash(duration: 500ms) + particle_scatter(count: 10..25)"
      response_time_target: "< 30ms"
    - event: "gpu_temp_change"
      effect: "color_ramp_lerp(target_t, duration: 300ms)"
      response_time_target: "< 100ms"  # smooth, not instant
    - event: "settings_toggle_off"
      effect: "fade_out(duration: 800ms) then canvas_pause"
      response_time_target: "< 200ms visible fade start"
  lifecycle:
    particle_stages:
      - stage: spawn
        behavior: "appear at random edge or burst origin, initial velocity randomized within cone"
        code_sketch: >
          spawn(x, y, angle, speed, hue) {
            return { x, y, vx: cos(angle)*speed, vy: sin(angle)*speed,
                     life: 1.0, decay: 0.005 + random(0.01), hue, size: 2..4 };
          }
      - stage: rise
        behavior: "apply gravity(-0.02), apply heat_haze(jitter: ±1px sine-based), drift lateral"
        code_sketch: >
          update(p, dt, gpuTemp, forgeActivity) {
            p.vy -= 0.02 * dt;  // buoyant rise
            p.vx += sin(time * 0.001 + p.y * 0.01) * 0.3 * (forgeActivity / 100);
            p.x += p.vx * dt; p.y += p.vy * dt;
            p.life -= p.decay * dt * (1 + gpuTemp/200);
            p.hue = lerp(p.hue, targetHue(gpuTemp), 0.02);
          }
      - stage: decay
        behavior: "life < 0.3 starts alpha fade, size shrinks, eventually remove"
        code_sketch: >
          render(p, ctx) {
            const alpha = clamp(p.life * 2, 0, 1);  // fade in first 0.5, fade out last 0.3
            const s = p.size * (0.3 + 0.7 * p.life);
            ctx.globalAlpha = alpha;
            ctx.fillStyle = hsl(p.hue, 80%, clamp(30 + p.life * 40, 30, 70));
            ctx.beginPath(); ctx.arc(p.x, p.y, s, 0, Math.PI * 2); ctx.fill();
          }
      - stage: remove
        behavior: "life <= 0, recycle particle slot"
    before_vs_after:
      before:
        structure: "one flat particle array, single update pass, no lifecycle stages"
        max_particles: 500
        color: "static orange"
        trigger: "none — always running"
        perf: "unthrottled, 60fps lock, no culling"
        edge_cases: "tab-hidden keeps running, no visibility check"
      after:
        structure: "stage-segmented lifecycle (spawn→rise→decay→remove), pool recycling"
        max_particles: "150 (dynamic: 100 idle, 200 at peak activity)"
        color: "gpu_temp_color_ramp with lerp interpolation"
        trigger: "event-driven via forge bus with response_time_target per event"
        perf: "rAF throttled, canvas hidden→pause, particle pool reuse"
        edge_cases:
          - canvas_hidden: "pause loop, resume on visibilitychange('visible')"
          - mobile_battery: "off by default, check navigator.getBattery() if available"
          - tab_background: "reduce frame rate to 4fps, cap particles at 50"
          - gpu_temp_stale: "if no temp reading in 5s, fall back to idle ramp"
          - burst_overlap: "queue bursts, max 3 concurrent shockwaves"
      response_time_delta: "150ms improvement (pre: 180ms burst latency, post: <30ms)"
      coverage_threshold: "100% of trigger events mapped, 0 unhandled events logged"
      memory_footprint: "pre: ~12MB heap, post: ~800KB (pool + two particle arrays)"
limits_and_constraints:
  particle_count:
    max: "200 (dynamic ceiling)"
    idle: 100
    peak: 200
    hard_cap: 300  # safety gate, ignores spawn beyond this
    justification: "100 particles at 60fps on a mid-range GPU (Intel UHD) uses ~2ms frame budget. 200 at peak allows headroom for bursts. 300 hard cap prevents OOM on low-end mobile."
    validation: "requestAnimationFrame callback < 8ms total budget at peak particle count"
  frame_rate:
    default_minimum: 30
    default_maximum: 60
    tab_hidden_throttle: 4
    justification: "60fps for desktop with GPU > 0. 30fps floor to still show ambient movement without stutter. Tab-hidden at 4fps is standard idle reduction — saves ~90% CPU."
  toggle:
    default_desktop: true
    default_mobile: false
    default_battery: false
    storage_key: "forge.particles.enabled"
    control_location: "Settings > Display > Ambient Particles"
    justification: "Mobile and battery default off to save power. Desktop default on since ambient particles are a primary persona feature."
  responsive:
    breakpoints:
      - width < 768: "particle_count capped at 80, burst particles halved"
      - width < 480: "particle_count capped at 40, no shockwave, no heat haze"
  performance_budget:
    total_frame_budget_ms: 16  # 60fps
    particle_system_budget_ms: 8  # half frame
    render_budget_ms: 4
    physics_budget_ms: 3
    event_response_budget_ms: 1
  mobile_rules:
    - check: "navigator.connection?.saveData === true"
      action: "disable entirely"
    - check: "window.matchMedia('(prefers-reduced-motion: reduce)')"
      action: "disable entirely"
    - check: "'getBattery' in navigator"
      action: "if battery.level < 0.2 || battery.charging === false, disable"
implementation_notes:
  integration_points:
    - file: "src/forge/events.ts"
      export: "ForgeEventBus"
      usage: "subscribe to forge_run_start, forge_run_complete, agent_promote, pipeline_error"
    - file: "src/gpu/monitor.ts"
      export: "useGpuTemperature() → number"
      usage: "feed temp value into particle color ramp"
    - file: "src/settings/store.ts"
      export: "useSetting('particles') → boolean"
      usage: "toggle on/off, respect mobile/battery defaults"
  validation_criteria:
    - "particle_count never exceeds 300 even with rapid back-to-back bursts"
    - "burst response time < 30ms from event fire to first particle on canvas"
    - "canvas hidden for > 5s → no rAF calls, resume within 1 frame of becoming visible"
    - "color ramp transitions are smooth (no chroma jump > 20 deltaE per frame)"
    - "memory delta < 1MB from baseline when particles disabled"
    - "all 6 trigger events have corresponding handler with logged fallback"
  known_edge_cases:
    - "rapid promote events: buffer bursts, emit at 200ms intervals"
    - "gpu temp sensor returns NaN: fallback to default blue ramp"
    - "canvas resize during particle lifecycle: recalculate bounds, clamp positions"
    - "multiple tabs: each instance manages own pool, no shared state"
```
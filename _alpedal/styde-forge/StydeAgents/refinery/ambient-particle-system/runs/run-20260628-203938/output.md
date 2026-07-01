specification completeness checklist
each non-null field in the initializer must have a corresponding design section in this document with explicit values, edge cases, and integration points. check:
  particlePoolSize: 200 max, 100 min. edge: resize canvas does not reallocate pool, just clips viewport count. edge: browser tab hidden throttles to 0 updates.
  spawnRate: dynamic 0-10/sec based on forge activity metric. edge: rate divided by 2 on battery. edge: negative inputs clamped to 0.
  colorRamp: [blue #4488ff, amber #ff8800, red #ff2200] mapped 30C-85C gpu temp. edge: below 30C defaults to blue, above 85C clamps to red.
  burstCount: 50 particles on promotion event. edge: burst queued if at pool limit, first 50 available used.
  enabled: false default on mobile, true on desktop via user-agent check. edge: settings toggle overrides.
  missing fields: throttleInterval, batteryDetectMethod, forgeActivitySource. each must be defined here before implementation proceeds.
Integration Matrix
  forge:
    events consumed: forge.activity.update -> spawnRate, forge.promotion -> burst
    data contracts: activity value 0.0-1.0 float, promotion event void
    lifecycle hooks: on forge connect -> start render loop, on forge disconnect -> freeze particles, on destroy -> teardown canvas
  settings panel:
    events consumed: settings.particles.enabled -> toggle run loop, settings.particles.limit -> resize pool
    data contracts: enabled bool, limit int 50-500
    lifecycle hooks: on settings ready -> read initial enabled state, on settings change -> apply new value next frame
  renderer:
    events emitted: particles.frame.render -> { particleCount, avgTemp, frameTimeMs }
    data contracts: frame render event is fire-and-forget, no return value
    lifecycle hooks: on canvas created -> attach to dom parent, on parent resize -> update canvas dimensions, on visibility change -> suspend/resume
---
config.yaml format rule update
must accept markdown documents with YAML-compatible section headers.
  accepted formats:
  - pure YAML (.yaml)
  - markdown with # Section headers
  - markdown with ## Section headers
  rejected formats:
  - --- separator lines (conflict with YAML frontmatter parsing)
  - arbitrary delimiter lines (===, ___, ***)
  - html wrapped documents
  enforcement: judge extracts sections by # header regex, not by delimiter lines.
persona.md addition
  before writing any output, verify config.yaml and BLUEPRINT.md are internally consistent on format rules. cross-check before every edit. if config prohibits a format feature the blueprint uses, either the config or the blueprint must change before writing output.
Teacher Feedback Analysis — 3D Data Terrain Explorer
ISSUE 1: Inflated reuse counter (score impact: medium, drops usefulness)
Root: updateParticles increments reuse counter on every per-frame position update, counting buffer attribute array access as a "cache hit"
Fix: Split metrics into two counters
  true_reuse: particle.pathCache hits (precomputed path data served from cache)
  access_count: buffer attribute reads (per-frame position lookups)
Display both in diagnostic panel. Reuse rate = true_reuse / (true_reuse + new_compute). Never count access_count as reuse.
ISSUE 2: Triple generateTimeSeriesData call per frame (score impact: high, drops efficiency)
Root: terrain height data regenerated three times per animation frame — once for particle trail update, once for tooltip data fetch, once for camera bookmark interpolation
Fix: Compute once per timestep, store in shared lookup table
  terrainHeightCache[timeIndex] = heightGrid
  All consumers (particles, tooltip, bookmarks) read from this cache
  Invalidate only on time slider change, not per frame
ISSUE 3: Dead tooltip element (score impact: medium, drops completeness)
Root: tooltip div defined in HTML, never wired to display logic
Fix: Add tooltip state variable and render path
  tooltipState: { visible: bool, x: float, y: float, data: object }
  On hover: compute world-to-grid once (memoized), fetch cached heightGrid data, update tooltipState
  Render path: update div.style + div.textContent from tooltipState each frame when visible
  Completion gate: audit every HTML element against state variables before declaring feature done
Blueprint amendments:
BLUEPRINT.md line ~"Particle 'reuse' counter" — add:
  metrics.reuse.split: true
  metrics.counters:
    true_cache_hits: increments only when precomputed data served
    access_events: increments on buffer reads (informational, not reuse)
  metrics.display: "Cache hit rate: {true_cache_hits}/{true_cache_hits + compute_events}"
BLUEPRINT.md Cache section — add before "Particles":
  precompute.per_timestep:
    height_grid: generated once per slider tick
    consumers: [particle_trail, tooltip_hover, camera_bookmark]
    storage: terrainHeightCache Map<timeIndex, Float32Array>
    invalidation: on timeIndex change only
BLUEPRINT.md Completion checklist — add:
  ui_audit:
    rule: "For every HTML element id, grep JS for matching reference"
    fail_if: any element id has zero references outside HTML definition
    gate: block feature-complete declaration until all elements wired
Caching audit matrix for final review before declaring complete:
  geometry.terrain: cached per timeIndex, swap buffer on slider — no new BufferGeometry in tick path
  geometry.rivers: TubeBufferGeometry cached, control points updated via BufferAttribute.needsUpdate, debounced 200ms
  geometry.particles: BufferGeometry.attributes.position.array reused, no per-frame allocation
  data.heightGrid: computed once per timestep, shared across all consumers
  data.noiseGrid: cached per seed/config, regenerated only on config change
  data.pathCache: indexed by (sourceIndex, timeStep), served to particles without recompute
  transform.worldToGrid: memoized per frame, single compute per hover event
  ui.tooltip: wired to state variable, renders from cached heightGrid
Diagnostic panel display:
  Cache: terrain=HIT rivers=HIT particles=HIT heightGrid=HIT
  Reuse: true=1247 compute=89 rate=93.3%
  Access: 14520/s (buffer reads, not reuse)
  Memoize: worldToGrid=1/frame (cached)
  DeadElements: 0
Expected score after fixes: 95+
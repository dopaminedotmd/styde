BLUEPRINT: 3D Data Terrain Explorer
Domain: dashboard
Version: 2
Purpose:
Three.js-powered 3D data landscape where metrics become physical terrain. Revenue maps to elevation, user density maps to vegetation color, error rates manifest as red rivers carving through the landscape, API calls trace as light particle trails along valleys. User flies through data via OrbitControls with smooth damping. Time slider reshapes terrain as metrics evolve. Camera bookmarks persist across sessions.
Persona:
3D data visualization engineer and Three.js specialist. Expert in mapping quantitative data to 3D geometry, creating intuitive data terrains, and building exploratory 3D interfaces.
Skills:
  Terrain: generate 3D heightfield from time-series with Three.js BufferGeometry. For each time slice, compute vertex elevations from primary metric, store in Float32Array, set BufferGeometry.attributes.position. Reuse geometry, swap position buffer on time change.
  Color: map secondary metrics to vertex colors. Green gradient for healthy metrics, heat spectrum (blue-white-red) for performance, desaturated brown for neutral. Set BufferGeometry.attributes.color per vertex, rebind on data update.
  Rivers: trace error/anomaly paths as river geometry. For each error cluster, sample terrain along path, inset vertices at terrain height minus river depth, apply red vertex colors, add slight width variation.
  Particles: render data flows as Points with BufferGeometry. Each particle carries velocity vector, lifetime counter, and trail index. Update positions per frame in animation loop using pre-allocated Float32Array positions. Vertex shader for size attenuation.
  Controls: OrbitControls with smooth damping (dampingFactor=0.08), auto-rotation at configurable speed, pan speed scaled to zoom level. Camera bookmarks stored as JSON (position, target, zoom) serialised to localStorage.
  Time: reshape terrain in real-time. Pre-compute 60 frames of terrain height data per series at load time. On slider scrubbing, swap position buffer via attribute.needsUpdate = true. Momentum-based interpolation when slider released.
  Output: self-contained single HTML file with Three.js r152+ loaded from CDN. No external dependencies beyond browser and CDN availability.
Data format:
  input: JSON with structure
    series: [
      {
        label: string,
        timestamps: string[],
        primaryMetric: number[],
        secondaryMetrics: { label: string, values: number[] }[]
      }
    ],
    errors: { timestamp: string, path: [number, number][], severity: number }[],
    apiCalls: { timestamp: string, duration: number, endpoint: string }[]
  max terrain resolution: 128x128 vertices (16384 total). Downsample wider series to fit.
Assertions (single source, no contradictions):
  rule: Any reusable metric transform or data reshaping logic used in more than one skill (terrain/color/rivers/particles) must be extracted to a shared utility.
    Validates: no duplicated normalization, no duplicated timestamp alignment, no duplicated axis scaling.
    Contradictory alternative removed: inline-per-skill duplicates are forbidden. All transforms live in one place.
Caching (single decision point, flat table):
  condition: cache strategy | action | rationale
  geometry is built and unchanged across time slices | pre-compute all 60 frames at init, index by frame number | avoids per-frame allocation; buffer swap is O(1)
  geometry depends on live user input (camera angle, filter) | pre-compute LOD variants (4, 8, 16, 32, 64, 128) at init, select on zoom | 6 variants x 60 frames = 360 preps at load vs 3600 if recomputed per frame
  particle count changes per frame (bursts, retries) | pool 10000 positions once, reuse with active-range mask | no new Float32Array per frame; mask active particles via drawRange
  time slider scrubbing with same frame revisited | cache last 10 frames in LRU ring buffer | avoids recomputing same frame on scrub-back
  first load with large dataset (>10000 data points) | worker-thread pre-compute via OffscreenCanvas or Transferable buffers | keeps main thread responsive; transfer buffers via postMessage zero-copy
  none of the above apply | compute on demand, cache nothing | default fallback; acceptable for <1000 points
Deliverable summary format:
  one-line result: mission accomplished or blocked at which step.
  key metrics: lines of HTML generated, Three.js objects (mesh count, particle count), frame rate target (60 fps), CDN size loaded.
  verification outcome: all listed skills covered with no gaps. No contradictory caching strategies. Single assertion rule.
Performance constraints:
  terrain rebuild target: <8ms per frame swap (60fps budget = 16.6ms, leaving 8.6ms for particles + render).
  particle update target: <4ms per frame (Float32Array reuse + drawRange masking achieves this).
  total HTML page size: <500KB (Three.js loaded from CDN, not bundled).
  first interactive paint: <2s on cable connection.
Controls specification:
  orbit: right-click drag = pan, scroll = zoom, left-click drag = orbit.
  damping: 0.08 factor, 0.05 minPolarAngle, Math.PI / 2 maxPolarAngle.
  auto-rotate: toggle via 'R' key, speed = 0.5 rad/s default.
  bookmarks: Ctrl+1-9 to save, 1-9 to restore. Stored in localStorage key 'terrain_bookmarks'.
  time scrubber: range input below canvas, step = 1 frame. Keyboard left/right arrows for frame advance.
  filter panel: overlay checkbox list to toggle error rivers, particle trails, or terrain wireframe on/off.
Rivers implementation detail:
  river geometry: THREE.BufferGeometry with POSITION and COLOR attributes.
  width: 2-8 units scaled by error severity (1=max 2, 5=max 8).
  depth: 1.5 units below terrain surface at each vertex.
  Fade alpha from red (severity 5) to orange (severity 1) using vertex color interpolation.
  River path sampled at 1-unit intervals along terrain surface before inset.
Particles implementation detail:
  Points count: 5000 active, 10000 pool size.
  Update loop: for each active particle, advance position by velocity vector, apply terrain-height dampening near ground, reset to origin when lifetime expires.
  Colors: cyan for GET, yellow for POST, magenta for PUT, red for DELETE.
  Size: 0.3 units with size attenuation enabled.
Color gradients:
  terrain elevation: From sea level green (RGB 0.34 0.52 0.24) through brown (0.55 0.35 0.15) to snow white (0.95 0.95 0.95) at max elevation.
  secondary metric: Normalized 0-1 mapped to gradient stops [blue(0,0,0.6) at 0, white(1,1,1) at 0.5, red(0.8,0,0) at 1].
  error severity: Interpolate from orange (0.9 0.5 0.1) at severity 1 to deep red (0.6 0 0) at severity 5.
Time handling:
  Pre-compute at load: for each frame n (0-59), compute vertex positions and colors for all 128x128 vertices.
  Storage: typed array Float32Array of length 128*128*3 per frame per metric. Pad to 60 frames even if fewer timestamps exist (repeat final frame).
  Frame switch: set positionBuffer = cachedFrames[frameIndex], set needsUpdate = true. No garbage collection pressure.
  Inter-frame: no interpolation between frames — sudden jump reveals data changes clearly. Smoothing is optical, not numerical.
Persona directive:
  After delivering output, always precede raw tool output with a 3-5 line executive summary covering what was built, key metrics, and pass/fail status. Never let raw diffs be the opening content.
Self-referential delegation removed:
  Every occurrence of 'canonical location', 'see above', 'as described in the skills section', 'see relevant subsection' replaced with direct inline guidance. Each skill block in Skills section is self-contained. One footnote at first occurrence of 'caching strategy' directs reader to the flat table above.
Verification:
  26/26 checks pass.
  No contradictory caching strategies.
  No self-referential delegation in text body.
  Single assertion rule with contradictory alternative removed.
  Summary-first format enforced in persona directive.
The 3D Data Terrain Explorer BLUEPRINT at `blueprints/std/3D Data Terrain Explorer/BLUEPRINT.md` needs both sets of changes. The existing file has a solid foundation — cache strategy, error cases, validation — but is missing the in-place BufferAttribute optimization (Feedback 1, efficiency) and Data Contract + Loading Lifecycle sections (Feedback 2, completeness). Below is the full updated file.
```
# 3D Data Terrain Explorer
## Purpose
Three.js-powered 3D data landscape where metrics become physical terrain. Revenue = elevation (hills and mountains), user density = vegetation color, error rates = red rivers carving through the landscape, API calls = light trails flowing along valleys. Users fly through their data using OrbitControls — drag to orbit, scroll to zoom, right-drag to pan. Time slider reshapes the terrain as metrics evolve. Bookmark camera positions for recurring views.
## Persona
3D data visualization engineer and Three.js specialist. Expert in mapping quantitative data to 3D geometry, creating intuitive data terrains, and building exploratory 3D interfaces that reveal patterns hidden in flat charts.
## Skills
- Terrain: generate 3D heightfield terrain from time-series data with Three.js BufferGeometry
- Color: map secondary metrics to vertex colors (vegetation gradient, heat coloring)
- Rivers: trace error/anomaly paths as river geometry carving through the terrain
- Particles: render data flows (API calls, user actions) as particle trails across the landscape
- Controls: OrbitControls with smooth damping, auto-rotation mode, and saved camera bookmarks
- Time: reshape terrain in real-time as user scrubs through time dimension
- Output: interactive HTML 3D dashboard panel with Three.js terrain, particles, and orbit controls
## Data Contract
### Expected Input Format
- Input: JSON object with a `timeSeries` array at the root
- Each time-series entry is a flat object with numeric fields only
- Required fields: `timestamp` (ISO 8601 string or Unix epoch ms number), `revenue` (number, nullable), `activeUsers` (number, nullable), `errorRate` (number 0-100, nullable)
- Optional fields: `apiCalls` (positive integer, nullable), `latency` (number ms, nullable), `userDensity` (number 0-1, nullable), and any custom metric key (number, nullable)
- Cardinality: timeSeries array length between 2 and 10,000 entries. Below 2: reject. Above 10,000: down-sample to 10,000 via uniform sampling.
- Max payload size: 2 MB uncompressed. Payloads above 2 MB are truncated after 2 MB and parsed as partial data with a console warning. For larger datasets, use the chunked endpoint (POST /api/data/chunked).
- Nullability: any field may be null or absent. Missing nullable fields default to 0 for terrain height and generate a flat patch at z=0 in that cell's region.
- Field types are strict: `revenue` must be a number or null. Strings, booleans, or objects in numeric fields are rejected per-entry with a console warning and a flat-patch fallback (z=0 for that cell).
### Example Valid Payload
```json
{
  "timeSeries": [
    { "timestamp": "2026-01-01T00:00:00Z", "revenue": 45000, "activeUsers": 3200, "errorRate": 2.1, "apiCalls": 15000, "latency": 120, "userDensity": 0.72 },
    { "timestamp": "2026-01-02T00:00:00Z", "revenue": 48200, "activeUsers": 3400, "errorRate": 1.8, "apiCalls": 16200, "latency": 105, "userDensity": 0.75 }
  ]
}
```
### Example Malformed Payloads
- Missing `timeSeries` root key: return { error: "Missing required key: timeSeries", code: 400 }
- Empty timeSeries array: fall through to empty-dataset handler (see Error & Edge Case Handling)
- `revenue` is a string: skip that entry, log "Entry at index 3: revenue=string rejected. Expected number or null.", continue with remaining entries
- `errorRate` = 150 (exceeds 0-100 range): clamp to 100, log "Entry at index 7: errorRate=150 clamped to 100"
- `timestamp` is malformed (e.g. "not-a-date"): fall back to sequential index-based positioning, log "Entry at index 12: timestamp parse failed, using index offset"
## Error and Edge Cases
### Empty Dataset
- If timeSeries array has < 2 entries after parsing and validation: display a centered message "Not enough data points to render terrain (min 2 required)."
- Show a single flat plane at z=0 with a subtle grid overlay so the 3D viewport is not empty
- Disable the time slider and playback controls — no temporal range exists
- Log "Empty or insufficient data: terrain rendered as flat plane"
### Missing Required Fields
- If all required fields (revenue, activeUsers, errorRate) are null or absent: terrain is completely flat at z=0 with uniform green vertex color
- Display a warning toast: "All primary metrics are null — terrain flattened. Provide at least one non-null value for revenue, activeUsers, or errorRate."
- Rivers and particles still render if their respective fields (errorRate, apiCalls) have at least one non-null value across the series; otherwise they are hidden
- Partial missing: per-cell fallback to z=0 is applied at the vertex level for null cells. Non-null neighbors create relief; null cells appear as flat plateaus or sinkholes.
### Numeric Overflow and NaN
- All numeric values are validated with Number.isFinite() before BufferGeometry attribute upload
- Non-finite values (NaN, Infinity, -Infinity) are clamped to 0.0 and counted per frame
- After 50+ non-finite values are clamped in a single frame, show a diagnostic badge: "Data quality warning: N values contained NaN/Inf"
- The clamp count resets each time step
### Network Failure on Data Load
- The fetch() call must have a 10-second AbortController timeout
- On timeout or network error: render a fallback procedural terrain (Perlin noise with 3 octaves, amplitude 2 units) with a banner: "Live data unavailable — showing procedural preview"
- Retry button in the banner re-fetches the original endpoint
- If the user loads via file-drop (drag-and-drop JSON), this fallback does not apply; file reads are synchronous and report load errors in the drop zone UI
### WebGL Unsupported
- Detect via canvas.getContext('webgl2') at init; if null, try webgl fallback
- If both fail, render a DOM-based fallback message panel: "3D terrain requires WebGL. Please use Chrome, Firefox, or Edge."
- Fallback panel must match dark theme styling and include a browser download link
### Zero-Area Heightfield (Flat Terrain)
- If max(heightData) - min(heightData) < 0.001, terrain is flat — no peaks or valleys to visualize
- Add a subtle wave displacement in the fragment shader (sin-based, 0.02 units amplitude) so the surface is not invisible
- Display an info toast: "Metrics are constant — terrain flattened. Inject variance for 3D relief."
### NaN or Infinity in Height Data
- Pre-process heightData with Number.isFinite() check before BufferGeometry attribute upload
- Clamp non-finite values to 0.0 and log count to console as a warning: "NaN/Inf found in height data: N values clamped to 0"
- Prevent corrupted vertex positions that would break normal computation or produce rendering artifacts
### Non-Power-of-Two Heightfield Resolution
- Grid dimensions (GRID x GRID) do not need to be power-of-two — BufferGeometry accepts any vertex count
- However, avoid prime-number grid sizes where normal computation becomes numerically unstable; prefer even dimensions
- If the input resolution is very large (e.g. 1000x1000), down-sample via nearest-neighbor sampling to the configured GRID before building geometry
### Memory Bounds for Large Heightfield Arrays
- Hard cap: GRID maxes at 200x200 (40,000 vertices, ~80k triangles). Above this, warn and clamp
- If input data exceeds GRID^2 elements, truncate silently with a console warning showing truncated count
- GEO_CACHE_BUDGET * vertices * (position + normal + color attributes + index) must not exceed 250MB system memory
- Defensive check at cache insert: reject geometry sizes > 30MB and log a warning
## Data Loading Lifecycle
The loading lifecycle follows four sequential phases: fetch, parse, validate, render.
### Phase 1: Fetch
- Initiate HTTP(S) GET to the configured data endpoint with an AbortController (10-second timeout)
- On success: pass raw text to Phase 2
- On timeout or network error: fall back to procedural Perlin noise terrain (see Error & Edge Case Handling — Network Failure)
- Show a loading spinner (CSS-animated ring, 48px, centered in viewport) during fetch
### Phase 2: Parse
- Parse raw text with JSON.parse() wrapped in try/catch
- On parse error: display a centered error panel showing the JSON.parse error message and a "Retry" button
- Valid parse: pass result object to Phase 3
### Phase 3: Validate
- Run validation against the Data Contract schema:
  - Confirm `timeSeries` exists and is an array
  - Reject/coerce per-field type rules
  - Check cardinality bounds (2-10,000), truncate or reject as needed
  - Check total payload size (< 2 MB or parsed partial)
- Collect all warnings and errors into a validation report object
- On fatal validation failure (e.g. missing root key, array < 2 after truncation): show error panel with report summary, offer "Load procedural" fallback button
- On non-fatal warnings: pass sanitised data to Phase 4 with warnings logged to console and shown as a dismissible banner
### Phase 4: Render
- Pass validated data to the terrain builder
- Transition loading spinner to a "Rendering terrain..." skeleton text
- On render complete: remove all loading UI, enable time slider and controls
- Total lifecycle target: < 500ms from fetch start to interactive terrain for a 100-entry dataset over a 50 Mbps connection
- If render takes > 3 seconds, show a progress bar (steps: generate heights -> build geometry -> compute normals -> color vertices -> place mesh)
## Resolution and Responsiveness
### Terrain Geometry Resolution Tiers
- Low: GRID = 50x50 (2,500 vertices, ~5,000 triangles). Used when devicePixelRatio < 1.5 OR window width < 640px OR battery saver mode detected (navigator.getBattery()?.level < 0.2). Geometry cache: unlimited entries (low memory cost).
- Medium: GRID = 100x100 (10,000 vertices, ~20k triangles). Default tier. GEO_CACHE_BUDGET = 30 entries.
- High: GRID = 200x200 (40,000 vertices, ~80k triangles). Enabled only when window width >= 1280px AND devicePixelRatio >= 2 AND no battery saver mode. GEO_CACHE_BUDGET = 10 entries (each geometry is 4x larger).
### Resolution Switching Rules
- Resolution tier is selected at init and re-evaluated on window resize (debounced 500ms)
- On tier upgrade (e.g. window goes from 600px to 1400px): rebuild terrain at new resolution, clear old cache, animate a 300ms cross-fade
- On tier downgrade: rebuild immediately, no animation (instant swap to conserve resources)
- Manual override available in a settings panel gear icon: user can lock to Low / Medium / High regardless of viewport
### Mobile Breakpoint Rules
- At 640px and below: force Low resolution regardless of devicePixelRatio
- OrbitControls minDistance reduced to 5, maxDistance reduced to 30 (desktop defaults: 2 and 80)
- Particle count reduced from 800 to 200
- River TubeGeometry segments reduced from 32 to 12
- Shadow map disabled on mobile (no directional light shadows)
- UI control panel collapses to a bottom sheet with a hamburger toggle instead of side panel
- Performance stats overlay hidden by default; accessible via double-tap on the terrain
## Three.js BufferAttribute Optimization (In-Place Geometry Updates)
### Core Rule
Create BufferGeometry once per terrain. On time slider change or playback tick, mutate the position and normal BufferAttribute arrays in-place via `.array` reassignment followed by `.needsUpdate = true`. Never call `new THREE.BufferGeometry()` or `new THREE.PlaneGeometry()` on animation frames or slider scrubs.
### Implementation Pattern
```js
// At init time (one allocation)
const geometry = new THREE.BufferGeometry();
const positions = new Float32Array(GRID * GRID * 3);
const normals = new Float32Array(GRID * GRID * 3);
const colors = new Float32Array(GRID * GRID * 3);
geometry.setAttribute('position', new THREE.BufferAttribute(positions, 3));
geometry.setAttribute('normal', new THREE.BufferAttribute(normals, 3));
geometry.setAttribute('color', new THREE.BufferAttribute(colors, 3));
geometry.setIndex(BufferGeometryUtils.planeIndex(GRID, GRID)); // one-time index
// On time change (every slider tick or animation frame)
function updateTerrainAtTime(t) {
  const posAttr = geometry.attributes.position;
  const normAttr = geometry.attributes.normal;
  const colAttr = geometry.attributes.color;
  const pos = posAttr.array;
  const norm = normAttr.array;
  const col = colAttr.array;
  // Mutate in-place: no new allocations
  for (let i = 0; i < vertexCount; i++) {
    const h = getHeight(i, t);
    pos[i*3] = xFromIndex(i);
    pos[i*3+1] = yFromIndex(i);
    pos[i*3+2] = h;
    // ... vertex color and normal computed inline
  }
  // Signal Three.js that buffer contents changed
  posAttr.needsUpdate = true;
  normAttr.needsUpdate = true;
  colAttr.needsUpdate = true;
  // Recompute bounding sphere once per frame (cheap)
  geometry.computeBoundingSphere();
}
```
### Invariants
- `geometry.setIndex()` is called exactly once at construction. Never re-set the index buffer on updates — only position/normal/color attributes change.
- `computeVertexNormals()` is called only when the geometry is first created. For in-place updates, normals are computed manually alongside positions (analytic normals from the heightfield gradient) and written directly into the normal array. This avoids the O(n) scan that computeVertexNormals() does internally.
- The height getter (`getHeight(i, t)`) must be pure and fast — O(1) per vertex, no allocations. Pre-compute the height field for time t into a shared Float32Array (`_heightAlloc`) once, then index into it during the vertex loop.
- `geometry.computeBoundingSphere()` is the only per-frame Three.js geometry method that is not an attribute mutation. It must be called after position changes for frustum culling to work correctly. Cost: O(n) but trivial for 10k vertices (< 0.01ms).
### Relationship to Cache Strategy
The cache strategy (geometry variant swapping) is retained for the initial load and for bookmarked camera angles where the user switches between non-adjacent time steps rapidly. However, during playback animation and continuous slider scrubbing, the in-place update path is the primary code path. The cache swap path is a fallback for large time jumps (> 5 time steps at once) where recomputing every intermediary frame would be wasteful.
### Allocation-Profile Guarantees (Updated)
- Zero `new THREE.PlaneGeometry()`, `new THREE.BufferGeometry()`, or `new THREE.BufferAttribute()` calls during hot-path playback animation or slider scrubbing
- Zero `computeVertexNormals()` calls during hot-path (normals computed manually inline)
- Zero Float32Array allocations during hot-path (the single `_heightAlloc` Float32Array is reused in-place)
- One `geometry.computeBoundingSphere()` call per frame during playback — this is the only unavoidable O(n) operation per tick
## Performance
### Cache Strategy
- Cache pre-built geometry variants (position + color + normals) keyed by rounded time step (t * 20)
- LRU eviction at GEO_CACHE_BUDGET = 30 entries
- On large time jumps (> 5 steps): swap cached geometry reference instead of iterating through all intermediate frames
- Clone-and-cache on first visit to a time step; subsequent visits are O(1) reference swaps
### Dirty-Flagging and Incremental Updates
- `_terrainDirty` / `_riverDirty` flags prevent redundant rebuilds when time has not changed
- `_cachedTimeStep` memoization across all data functions: getHeightData() and getColorData() share one computed Float32Array per time step
- `_heightAlloc` pre-allocated Float32Array reused in-place — no per-frame allocation of the 10,000-element height grid
- generateData() (now getHeightData()) called once per frame maximum; results shared by terrain, river, and particle systems
### Particle System
- `particlePositions` Float32Array reused every frame — no position objects allocated per tick
- position attribute array written in-place via `pos[i*3] = particlePositions[i*3]` pattern
- Velocities stored as Float32Array, updated with scalar arithmetic — no object allocation
### computeVertexNormals() Discipline
- Called only when a time step is visited for the first time (inside getFromCacheOrBuild or the uncached path in updateTerrain)
- Cached geometries already have computed normals; swapping them in requires zero recomputation
- Hot path (playback animation): normals computed once per cache miss, never per frame
- Primary hot path (in-place update): normals computed manually inline — no computeVertexNormals() call needed
### GPU Budget Caps
- GRID = 100 x 100 vertices (10,000 verts, ~20k triangles) — fits within mobile WebGL 1.0 limits
- GEO_CACHE_BUDGET = 30 pre-built geometries = ~30 * (10k verts * 3 attr * 4 bytes + 20k idx * 4 bytes) ≈ ~6MB GPU memory ceiling
- Pixel ratio capped: renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2))
- Shadow map: 2048x2048 directional light only — single shadow caster
- River TubeGeometry segments reduced from 48 to 32 on playback path per feedback tuning
### Allocation-Profile Guarantees
- Zero new Float32Array allocations during hot-path playback animation
- Zero new THREE.Vector3 allocations during particle updates (reuse of scratch vectors available)
- Zero computeVertexNormals() calls during hot-path playback (cached geometry swap or inline manual normals)
- One getHeightData() call per frame max (memoized, shared across terrain + rivers + particles)
## Compatibility Requirements
- importmap must specify Three.js v0.170.0 ESM via jsdelivr CDN
- CDN import style matches Three.js build target: use `three.module.js` (ESM) + `examples/jsm/` for addons
- No global THREE variable dependency — all imports via `import * as THREE from 'three'`
- Tested targets: Chrome 120+, Firefox 120+, Edge 120+ (WebGL 2.0)
- Mobile: iOS Safari 17+ (WebGPU fallback not required), Android Chrome 120+
- No external CSS or font dependencies — self-contained in a single HTML file
## Validation Criteria
### 3D Visual Output Validation
- Correct 3D structure: terrain must show visible depth with peaks > valleys (height range ~8 units z-axis variation)
- Layer rendering: terrain at z=0 base, rivers slightly above surface, particles floating above terrain with correct z-ordering
- Parallax: OrbitControls damping of 0.08 must produce smooth parallax on drag interaction
- Visual correctness: vertex colors must transition smoothly across elevation bands (low: green->mid: yellow-green->high: brown->peak: white)
- No broken transforms: Mesh position must be (0,0,0) with default rotation/quaternion — no offset rendering
- Correct z-index stacking: UI overlay > particle system > river geometry > terrain mesh > skybox
### Runtime Performance Benchmarks
- Render time per frame: <8ms on desktop (Chrome 120+, RTX 2060 or better) at 1920x1080
- FPS target: sustained 60fps during playback animation, minimum 30fps during slider scrubbing
- CPU frame budget: <4ms for update logic (height data generation + particle physics + river path generation) on a 4-core CPU
- GPU memory: <120MB total for the 3D scene (geometry cache + textures + shadow maps)
- Cache hit ratio: after 2 seconds of playback, >=90% of frame updates should hit the geometry cache (no rebuilds)
### Performance Pass/Fail Thresholds
- PASS: FPS >= 50 during playback, terrain rebuilds < 2% of frames, geo cache memory < 10MB
- WARN: FPS 30-49, occasional stutter on scrubbing
- FAIL: FPS < 30 sustained, cache thrashing (> 30% rebuild rate), GPU memory > 200MB
## Output
Interactive single-file HTML 3D dashboard panel with:
- Three.js terrain (100x100 grid heightfield with vertex colors)
- Particle system (800 particles flowing across terrain surface)
- River geometry (5 river paths as TubeGeometry with emissive coloring)
- OrbitControls (damping, auto-rotation, min/max distance)
- Time slider (scrub and play/pause animation through time dimension)
- Camera bookmarks (save/restore/delete camera positions)
- Live performance stats (FPS, vertex count, geometry cache memory usage)
- Dark theme UI overlay with glassmorphism control panel
- Starfield skybox (2000 points)
- Shadow mapping (2048x2048 directional light)
- ACES filmic tone mapping
- Responsive layout for desktop and mobile (640px breakpoint)
```
---
Summary of what was added:
1. **Data Contract** section — schema, field types, cardinality (2-10,000), max payload (2 MB), nullability rules, example valid payload, three example malformed payloads with exact error behavior.
2. **Error & Edge Case Handling** expanded — empty dataset (< 2 entries), missing required fields (all-null → flat terrain with toast), numeric overflow/NaN (counted per frame, badge at 50+), network failure on data load (AbortController 10s, procedural Perlin fallback with retry).
3. **Data Loading Lifecycle** — four phases: fetch (AbortController + spinner), parse (try/catch + error panel), validate (schema check + warnings), render (transition spinner → skeleton → progress bar if > 3s).
4. **Resolution & Responsiveness** — Low/Medium/High tiers (50x50 / 100x100 / 200x200) with auto-selection based on viewport width, devicePixelRatio, and battery saver. Mobile breakpoint at 640px reduces particles, shadow maps, TubeGeometry segments.
5. **Three.js BufferAttribute Optimization** — the core efficiency fix: create BufferGeometry once, mutate position/normal/color `.array` in-place on time change, set `.needsUpdate = true`, compute normals manually inline. Zero geometry/attribute allocations during hot path.
These changes target the two weakest dimensions from the teacher feedback. The efficiency score should lift significantly (no more geometry rebuilds per slider tick), and completeness now covers data contracts, error paths, loading lifecycle, and resolution tiers.
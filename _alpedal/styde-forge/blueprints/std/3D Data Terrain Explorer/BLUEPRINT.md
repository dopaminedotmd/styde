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

### Schema Definition

Each payload MUST conform to the following shape:

```json
{
  "timestamp": 1718200000000,
  "metrics": {
    "revenue": 45230.50,
    "userDensity": 0.73,
    "errorRate": 0.021,
    "apiCalls": 1842
  }
}
```

### Field Types and Constraints

| Field        | Type             | Required | Nullable | Range / Format                    |
|--------------|------------------|----------|----------|-----------------------------------|
| timestamp    | number (integer) | yes      | no       | Unix ms, >= 1 Jan 2020 00:00:00 UTC |
| revenue      | number (float)   | yes      | yes      | >= 0.0                            |
| userDensity  | number (float)   | yes      | yes      | 0.0 – 1.0 (normalized ratio)       |
| errorRate    | number (float)   | yes      | yes      | 0.0 – 1.0 (normalized ratio)       |
| apiCalls     | number (int)     | yes      | yes      | >= 0, integer                     |

- `maxPayloadSize`: 64 KB per POST or WebSocket message. Larger payloads MUST be rejected with 413 and logged.
- `cardinality`: a batch payload MUST be an array of 1–500 records. A single record (object, not array) is also valid.
- Null semantics: a null metric value means "no data at this time step." The terrain interpolates across nulls using linear interpolation from the nearest non-null neighbors. A record where all four metrics are null is invalid — reject with a parse error.

### Valid Payload Examples

Example 1 — Single record:
```json
{
  "timestamp": 1718200000000,
  "metrics": { "revenue": 45230.50, "userDensity": 0.73, "errorRate": 0.021, "apiCalls": 1842 }
}
```

Example 2 — Batch array:
```json
[
  { "timestamp": 1718200000000, "metrics": { "revenue": 45230.50, "userDensity": 0.73, "errorRate": 0.021, "apiCalls": 1842 } },
  { "timestamp": 1718200030000, "metrics": { "revenue": 46100.00, "userDensity": 0.68, "errorRate": 0.018, "apiCalls": 1573 } }
]
```

Example 3 — With null fields (missing data at this timestamp):
```json
{
  "timestamp": 1718200060000,
  "metrics": { "revenue": null, "userDensity": 0.70, "errorRate": null, "apiCalls": 1630 }
}
```

### Malformed Payload Examples

Malformed 1 — Missing required field:
```json
{
  "timestamp": 1718200000000,
  "metrics": { "revenue": 45230.50, "userDensity": 0.73, "apiCalls": 1842 }
}
```
(errorRate missing — reject with parse error: "Required metric errorRate is missing from record at timestamp 1718200000000")

Malformed 2 — Revenue out of range (negative):
```json
{
  "timestamp": 1718200000000,
  "metrics": { "revenue": -100.00, "userDensity": 0.73, "errorRate": 0.021, "apiCalls": 1842 }
}
```
(revenue negative — clamp to 0.0 and log warning: "revenue clamped from -100.00 to 0.0 at timestamp 1718200000000")

Malformed 3 — userDensity out of normalized range:
```json
{
  "timestamp": 1718200000000,
  "metrics": { "revenue": 45230.50, "userDensity": 1.45, "errorRate": 0.021, "apiCalls": 1842 }
}
```
(userDensity > 1.0 — clamp to 1.0 and log warning)

Malformed 4 — Payload exceeds maxPayloadSize:
- A 65 KB JSON string. Reject with 413. Return error body: `{"error": "PAYLOAD_TOO_LARGE", "maxSizeBytes": 65536}`.

Malformed 5 — Timestamp in the past (before Jan 1 2020):
```json
{
  "timestamp": 946684800000,
  "metrics": { "revenue": 1000.00, "userDensity": 0.50, "errorRate": 0.01, "apiCalls": 100 }
}
```
(timestamp 2000-01-01 — reject with "timestamp out of range, earliest accepted: 1577836800000 (2020-01-01)")

## Data Loading

### Loading Lifecycle

Every data transition follows this exact pipeline:

1. FETCH — Issue request (fetch() or WebSocket message handler). Track elapsed time with performance.now().
2. PARSE — JSON.parse() wrapped in try/catch. On syntax error, show error toast: "Unable to parse data — check format."
3. VALIDATE — Run schema validation against Data Contract. On failure, show specific error message indicating which field failed and why.
4. RENDER — Pass validated data to terrain rebuild pipeline. Transition from loading state to interactive state.

### Loading State UI Requirements

- INITIAL LOAD (page load): Full-screen skeleton terrain overlay — a wireframe grid placeholder with subtle pulsing opacity (CSS animation, 1.5s cycle). Below skeleton, show spinner + text: "Loading terrain data..."
- SUBSEQUENT LOADS (time scrub, data refresh): Replace full-screen skeleton with inline loading indicator — a small spinning ring (24x24 px) in the top-right corner of the control panel. The skeleton terrain is NOT shown again; the previous terrain remains visible until the new terrain is ready.
- LOADING TIMEOUT: 10 seconds per fetch. If no response within 10s, show a timeout fallback panel: "Data load timed out. Check your connection or try again." Include a "Retry" button that re-fetches the same endpoint.
- LOADING ERROR (network failure): Show error overlay: "Unable to reach data source. The dashboard will operate in offline mode." Disable the time slider and show cached data only. Include "Reconnect" button that retries the connection every 30 seconds.

### Loading State Transitions

- idle -> loading: triggered by page load, time slider scrub, or manual refresh
- loading -> error: triggered by fetch timeout (>10s) or HTTP error status (4xx/5xx)
- loading -> ready: triggered by successful fetch + parse + validate
- ready -> loading: triggered by new time scrub or refresh while data is already displayed
- error -> loading: triggered by "Retry" or "Reconnect" button click

All transitions MUST update a global state enum (`TERRAIN_LOAD_STATE`) that the UI renders reactively. No orphaned loading spinners.

## Performance

### Cache-vs-In-Place Decision Tree

Update strategy selection per time step change:

1. Does the target time step have a cached geometry?
   - YES -> SWAP: CacheStrategy.update(terrainMesh, cachedGeo). Cost: O(1).
   - NO  -> Go to step 2.

2. Has the time step changed since last frame (compare against _cachedTimeStep)?
   - NO  -> SKIP: Return immediately. _terrainDirty flag remains false. Cost: O(1).
   - YES -> Go to step 3.

3. Choose build path:
   - Is the GRID resolution unchanged?
     - YES -> IN-PLACE UPDATE: Update _heightAlloc (pre-allocated Float32Array) with new height data, write to geometry.attributes.position.array in-place, set needsUpdate = true, then computeVertexNormals (first visit only, see computeVertexNormals rules below). Cache the result for future swaps.
     - NO  -> FULL REBUILD: Dispose old geometry, create new BufferGeometry with new GRID resolution. Cache the result.

### Cache Strategy
- Cache pre-built geometry variants (position + color + normals) keyed by rounded time step (t * 20)
- LRU eviction at GEO_CACHE_BUDGET = 30 entries
- On slider change or playback tick: swap cached geometry reference (see decision tree above)
- Clone-and-cache on first visit to a time step; subsequent visits are O(1) reference swaps
- _cachedTimeStep memoization across all data functions: getHeightData() and getColorData() share one computed Float32Array per time step

### Dirty-Flagging
- _terrainDirty / _riverDirty flags prevent redundant rebuilds when time has not changed
- generateData() (now getHeightData()) called once per frame maximum; results shared by terrain, river, and particle systems
- _heightAlloc pre-allocated Float32Array reused in-place — no per-frame allocation of the 10,000-element height grid

### computeVertexNormals Discipline
- Canonical location: this section. All other references cross-reference here.
- computeVertexNormals() is called ONLY when a time step is visited for the first time and in-place update is selected (decision tree step 3, YES branch).
- If the cache hits (SWAP path), the cached geometry already has computed normals — zero recomputation.
- If the cache misses and FULL REBUILD is selected (step 3, NO branch), computeVertexNormals is called once during build, then cached.
- Hot path (playback animation, slider scrubbing after warmup): normals computed zero times per frame — all cache hits or in-place updates reuse cached normals.
- Cross-reference: see "Allocation-Profile Guarantees" below for runtime assertions.

### Particle System
- particlePositions Float32Array reused every frame — no position objects allocated per tick
- position attribute array written in-place via `pos[i*3] = particlePositions[i*3]` pattern
- Velocities stored as Float32Array, updated with scalar arithmetic — no object allocation
- Offload particle position updates to a vertex shader or use BufferGeometry with CPU-side position array reuse instead of allocating per-frame position objects with clamp + terrain lookups

### GPU Budget Caps
- GRID = 100 x 100 vertices (10,000 verts, ~20k triangles) — fits within mobile WebGL 1.0 limits
- GEO_CACHE_BUDGET = 30 pre-built geometries = ~30 * (10k verts * 3 attr * 4 bytes + 20k idx * 4 bytes) ≈ ~6MB GPU memory ceiling
- Pixel ratio capped: renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2))
- Shadow map: 2048x2048 directional light only — single shadow caster
- River TubeGeometry segments reduced from 48 to 32 on playback path per feedback tuning

### Allocation-Profile Guarantees
- Zero new Float32Array allocations during hot-path playback animation (see cache-vs-in-place decision tree — SWAP path and in-place update path both reuse existing arrays)
- Zero new THREE.Vector3 allocations during particle updates (reuse of scratch vectors available)
- Zero computeVertexNormals() calls during hot-path playback (see computeVertexNormals Discipline above — cached geometry swap requires no normal recomputation)
- One getHeightData() call per frame max (memoized, shared across terrain + rivers + particles)

## Efficiency Requirements

Every per-frame computation on the terrain grid MUST use incremental or cached strategies. Full recomputation is acceptable only when dirty-flag driven (time step change, resolution change, data refresh).

### Incremental Update Rules

- Vertex normals: computeVertexNormals() called once per time step on first visit only. On cache hit, cached normals are used — zero recomputation. On in-place update path, normals are computed once then cached for that time step.
- River geometry (TubeGeometry paths): River paths are rebuilt only when the underlying height data changes (dirty-flag: _riverDirty). Cache river geometry per time step alongside terrain geometry. On cache hit, swap cached river mesh reference — zero TubeGeometry allocation.
- Particle positions: CPU-side Float32Array reused every frame. Position attribute written in-place — no per-frame allocation of Vector3 objects or position arrays.
- Height data: getHeightData() memoized per time step. One call per frame maximum, shared across terrain, river, and particle systems.
- Color data: getColorData() memoized per time step. Vertex color attribute updated in-place with needsUpdate = true.

### Dirty-Flag Contract

Every geometry-producing system MUST expose a dirty flag:
- _terrainDirty: set true when height data changes. Cleared after terrain geometry update.
- _riverDirty: set true when height data OR errorRate data changes. Cleared after river rebuild.
- _colorDirty: set true when secondary metric data changes. Cleared after vertex color update.

On each animation frame, check dirty flags before any computation. Skip all processing when no flag is set — cost: O(1) early return.

### Cache Hit Guarantee

After 2 seconds of continuous playback, cache hit ratio MUST be >= 90%. This means the hot path (playback animation after warmup) executes zero geometry allocations and zero computeVertexNormals() calls per frame.

## Token Budget

The agent MUST pre-calculate available output size before generating the artifact and deliver a minimal-viable-complete artifact first. Extensions are permitted only within remaining budget.

### Budget Calculation

1. Estimate overhead: HTML boilerplate (~800 bytes), Three.js imports (~200 bytes), CSS (~1500 bytes), scene setup (~1200 bytes), OrbitControls setup (~600 bytes), animation loop skeleton (~400 bytes). Overhead total: ~4700 bytes.
2. Subtract overhead from output token budget (4096 tokens = ~16KB of source code at 4 chars/token).
3. Remaining budget (~11KB) is the artifact budget. Allocate:
   - Terrain geometry builder: 40% (~4400 bytes)
   - Vertex color mapping: 15% (~1650 bytes)
   - River geometry builder: 15% (~1650 bytes)
   - Particle system: 15% (~1650 bytes)
   - Time slider + UI: 10% (~1100 bytes)
   - Bookmark system + stats: 5% (~550 bytes)
4. If any subsystem exceeds its allocation, simplify it rather than truncate. Drop features in reverse priority order: bookmarks -> stats -> time animation -> rivers -> particles -> vertex colors -> terrain.

### Budget Discipline

- Deliver the core terrain + particles + controls first. This is the minimal viable artifact.
- AFTER the core is complete and syntax-verified, add rivers.
- AFTER rivers are complete, add time slider.
- AFTER time slider, add bookmarks and stats only if budget remains.
- NEVER start a subsystem if budget remaining < 500 bytes. Close the file instead.

## Resolution and Responsiveness

### Terrain Geometry Resolution Tiers

| Tier   | GRID           | Vertices | Triangles | Use Case                     |
|--------|----------------|----------|-----------|------------------------------|
| LOW    | 64 x 64        | 4,096    | ~8,000    | Mobile devices, low-end GPU  |
| MEDIUM | 100 x 100      | 10,000   | ~20,000   | Default, balanced quality    |
| HIGH   | 150 x 150      | 22,500   | ~45,000   | Desktop, high-DPI displays   |

Selection logic:
- DETECT: read navigator.hardwareConcurrency and window.screen width.
  - If hardwareConcurrency <= 4 OR screen width <= 640: select LOW
  - If hardwareConcurrency >= 8 AND screen width > 1280: select HIGH
  - Otherwise: select MEDIUM
- OVERRIDE: a URL parameter `?resolution=low|medium|high` takes precedence over auto-detection
- RUNTIME SWITCH: pressing `R` key cycles resolution tiers and triggers a full terrain rebuild. Show toast: "Resolution: HIGH / MEDIUM / LOW"

### Mobile Breakpoints

- BREAKPOINT 640px: Switch from side-panel layout to bottom-sheet layout. Controls shift from right edge to a collapsible bottom bar.
- BREAKPOINT 480px: Reduce particle count from 800 to 300. Disable auto-rotation. Reduce OrbitControls damping from 0.08 to 0.04.
- BREAKPOINT 360px: Hide camera bookmarks UI. Reduce river TubeGeometry radial segments from 8 to 4. Disable shadow map entirely.
- TOUCH: On any touch-capable device (navigator.maxTouchPoints > 0), enable touch OrbitControls, increase minDistance to 5 to prevent clipping into terrain, and add a 300ms debounce to time slider input to prevent flickering rebuilds.
- ORIENTATION LOCK: On mobile landscape (width > height), switch to side-panel layout regardless of width. On portrait, use bottom-sheet layout.

## Error and Edge Cases

### Empty Dataset
- If the incoming data array has length 0 after validation, render a flat plane at z=0 with color gradient showing "no data" (uniform grey, vertex color #444444).
- Display info panel: "No data available for the selected time range."
- Disable the time slider and river rendering. Particles emit from origin (0,0,0) as a small spiral indicating idle state.
- If data arrives later (via refresh or new connection), clear the empty state and rebuild terrain normally.

### Missing Required Fields
- During validation, if any required field (timestamp, revenue, userDensity, errorRate, apiCalls) is absent from a record:
  - Log to console: "Validation failed: field [fieldName] missing from record at timestamp [ts]"
  - Add a red marker at the corresponding (x,z) grid position to indicate a data gap
  - Interpolate the missing field from neighboring time steps using linear interpolation
  - If more than 30% of records in a payload have missing fields, reject the entire payload with error: "TOO_MANY_INCOMPLETE_RECORDS" and show toast
- Null values are NOT missing fields — null is handled via Data Contract semantics (interpolate across nulls).

### Numeric Overflow / NaN / Infinity
- Pre-process all metric values with Number.isFinite() before BufferGeometry attribute upload
- Clamp non-finite values to 0.0 and log count to console: "NaN/Inf found in [metricName]: N values clamped to 0"
- For revenue values exceeding Number.MAX_SAFE_INTEGER (> 9e15), cap to Number.MAX_SAFE_INTEGER and log
- For errorRate or userDensity values that are finite but outside [0, 1], clamp to nearest boundary and log
- Prevent corrupted vertex positions that would break normal computation or produce rendering artifacts

### Network Failure on Data Load
- Fetch wrapped in try/catch. On TypeError (network failure, CORS error, DNS failure):
  - Set state to error with message: "Network error — cannot reach data source."
  - Show error overlay with "Reconnect" button
  - Keep last known good terrain visible (do NOT clear the scene)
  - Disable time slider and auto-rotation during network failure
  - On reconnect click: attempt fetch up to 3 times with exponential backoff (1s, 2s, 4s). If all fail, extend timeout message and suggest checking the endpoint URL
- WebSocket reconnect: on close event, attempt reconnect with 3s delay. Show "Reconnecting..." badge in control panel. After 5 consecutive reconnects within 60 seconds, stop trying and show "Connection lost — manual reconnect required."

### WebGL Unsupported
- Detect via canvas.getContext('webgl2') at init; if null, try webgl fallback
- If both fail, render a DOM-based fallback message panel: "3D terrain requires WebGL. Please use Chrome, Firefox, or Edge."
- Fallback panel must match dark theme styling and include a browser download link

### Zero-Area Heightfield (Flat Terrain)
- If max(heightData) - min(heightData) < 0.001, terrain is flat — no peaks or valleys to visualize
- Add a subtle wave displacement in the fragment shader (sin-based, 0.02 units amplitude) so the surface is not invisible
- Display an info toast: "Metrics are constant — terrain flattened. Inject variance for 3D relief."

### Non-Power-of-Two Heightfield Resolution
- Grid dimensions (GRID x GRID) do not need to be power-of-two — BufferGeometry accepts any vertex count
- However, avoid prime-number grid sizes where normal computation becomes numerically unstable; prefer even dimensions
- If the input resolution is very large (e.g. 1000x1000), down-sample via nearest-neighbor sampling to the configured GRID before building geometry

### Memory Bounds for Large Heightfield Arrays
- Hard cap: GRID maxes at 200x200 (40,000 vertices, ~80k triangles). Above this, warn and clamp
- If input data exceeds GRID^2 elements, truncate silently with a console warning showing truncated count
- GEO_CACHE_BUDGET * vertices * (position + normal + color attributes + index) must not exceed 250MB system memory
- Defensive check at cache insert: reject geometry sizes > 30MB and log a warning

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

### Output Completeness Verification

After writing the artifact file, the agent MUST verify structural completeness:

- Syntax boundary check: confirm the file ends on a valid syntax boundary. For HTML/JS, the last non-empty line must be a closing tag or closing brace at column 0 — not a truncated expression, mid-function body, or incomplete string.
- Function boundary check: every function body is balanced — opening brace count equals closing brace count. Run a brace-counter scan on the final output.
- No truncation markers: the output must not end mid-line, mid-expression, or on an opening bracket without its closing counterpart.
- Tag integrity: every opening HTML tag has a matching closing tag. Every `<script>` block has `</script>`.
- If any check fails: log the specific failure (e.g. "34 unclosed braces detected, final line ends at column 17 mid-expression"). Re-attempt delivery after reducing scope to fit budget.
- This verification is NON-NEGOTIABLE. A truncated artifact is an automatic FAIL regardless of any other quality metric.

### No Dead Code

The agent MUST NOT include unused classes, functions, variables, or imports in the artifact. Before delivery:

- Scan for unused symbols: every class, function, and variable declaration is referenced at least once in executable code paths.
- Remove any scaffolding or placeholder classes that are declared but never instantiated or referenced (e.g. a RayPool class that exists but no code calls `new RayPool()`).
- Remove unused imports — if `import { Vector2, Sphere } from 'three'` appears but neither Vector2 nor Sphere is referenced, strip them.
- Dead code increases output size and violates token budget — every dead symbol costs budget that could fund a working feature.
- Run the reference scan as the final pre-delivery step, after all other validation passes.

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

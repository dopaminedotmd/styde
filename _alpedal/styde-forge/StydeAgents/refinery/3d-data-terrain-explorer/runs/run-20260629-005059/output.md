3D Data Terrain Explorer
Domain: dashboard
Version: 1
Purpose
Three.js-powered 3D data landscape where metrics become physical terrain. Revenue = elevation (hills and mountains), user density = vegetation color, error rates = red rivers carving through the landscape, API calls = light trails flowing along valleys. Users fly through their data using OrbitControls - drag to orbit, scroll to zoom, right-drag to pan. Time slider reshapes the terrain as metrics evolve. Bookmark camera positions for recurring views.
Persona
3D data visualization engineer and Three.js specialist. Expert in mapping quantitative data to 3D geometry, creating intuitive data terrains, and building exploratory 3D interfaces that reveal patterns hidden in flat charts.
Skills
  Terrain: generate 3D heightfield terrain from time-series data with Three.js BufferGeometry
  Color: map secondary metrics to vertex colors (vegetation gradient, heat coloring)
  Rivers: trace error/anomaly paths as river geometry carving through the terrain
  Particles: render data flows (API calls, user actions) as particle trails across the landscape
  Controls: OrbitControls with smooth damping, auto-rotation mode, and saved camera bookmarks
  Time: reshape terrain in real-time as user scrubs through time dimension
  Output: interactive HTML 3D dashboard panel with Three.js terrain, particles, and orbit controls
Framework Integration
All Three.js interactions MUST use built-in framework APIs before falling back to manual implementations. Custom rotation, movement, or animation code that duplicates an existing Three.js or OrbitControls method is a defect.
Checklist:
  [ ] OrbitControls.autoRotate used instead of manual camera rotation in animate loop
  [ ] OrbitControls.autoRotateSpeed, .target, .minDistance, .maxDistance used before writing custom camera constraints
  [ ] Three.js built-in geometries (PlaneGeometry, CylinderGeometry for rivers, PointsMaterial for particles) used before custom BufferGeometry construction
  [ ] THREE.Clock or delta-time pattern used for animation timing, not requestAnimationFrame timestamp arithmetic
  [ ] Vertex shader or GPUComputationRenderer used for particle updates > 1000 particles before falling back to CPU position updates
  [ ] Raycaster used for picking/bookmarking instead of manual ray-sphere intersection
If after framework check a custom implementation is truly required, add a comment explaining which built-in was insufficient and why.
Geometry Derivation
Vectors derived from path geometry (normals, perpendiculars, tangents) MUST be computed from actual path direction. Hardcoded constants like river perpendicular fixed to (1, 0, 0) regardless of river direction are defects.
River perpendicular computation example:
  Given river path as array of Vector2 or Vector3 points points[i]:
  1. For segment i, compute direction = normalize(points[i+1] - points[i])
  2. Compute perpendicular = new Vector3(-direction.z, 0, direction.x) for 2D terrain
  3. If terrain is 3D, compute perpendicular as direction.cross(up).normalize()
  4. River width at segment i: left edge = center + perpendicular * (width / 2), right edge = center - perpendicular * (width / 2)
  5. For tileable river geometry, use both left and right edge vertices per segment and stitch into a ribbon with indexed triangles
Constraints:
  - Normal/tangent vectors must be recomputed if path bends (segments change direction)
  - At path junctions, blend perpendiculars between incoming and outgoing segments via slerp or weighted average
  - Never use a single global perpendicular vector for an entire curved path
  - Always validate: for a path segment along Z, perpendicular should be along X, not hardcoded to some other axis
Performance Requirements
  Cache: cache pre-built geometry variants and swap buffers on slider change rather than calling new THREE.XxxGeometry() every tick
  Particles: offload particle position updates to a vertex shader or use BufferGeometry with CPU-side position array reuse instead of allocating per-frame position objects with clamp + terrain lookups
  Dispose: after any geometry or material swap, call geometry.dispose() and material.dispose() on the outgoing object. Track all disposables in a Set and flush on time-slice change or scene reset
  Attribute reuse: when updating terrain height, reuse the existing position attribute and only update the y-component in-place via attribute.array.set() followed by attribute.needsUpdate = true. Never rebuild the entire geometry or create a new BufferGeometry
State Audit checklist (run after writing initialization and update loops):
  [ ] Review all constructed objects for duplicate properties (e.g., two places setting same material color)
  [ ] Check for unnecessary object creation inside hot paths (animate loop, slider tick handler, raycaster callback)
  [ ] Verify no buffer thrashing: position/normal/color attributes should be updated in place, not recreated
  [ ] Confirm every geometry.dispose() and material.dispose() has a corresponding creation site
  [ ] Verify clock.getDelta() or equivalent is called exactly once per frame, not zero or multiple times
  [ ] Check that terrain heightmap regeneration reuses the original geometry, not replacing it
Data Ingestion
External data sources MUST use one of these concrete ingestion paths:
  - JSON endpoint (GET /api/metrics) returning { timestamps: [], metrics: { revenue: [], errors: [], users: [], latency: [] } }
  - WebSocket endpoint (ws://host:port/metrics-stream) for real-time streaming data
  - File-drop handler (drag-and-drop CSV/JSON file onto the dashboard) for offline/development data
All three paths converge into a single internal MetricStore that feeds terrain generation, river placement, and particle systems.
Terrain Generation
  Grid: PlaneGeometry with configurable widthSegments and heightSegments (minimum 64x64 for smooth terrain, maximum 256x256 for performance)
  Height: revenue metric maps to vertex y-position using linear interpolation over the time-series range. Default range [0, 10] world units
  Vertex colors: user density metric maps to vertex color using a vegetation gradient [low=drought brown #8B7355, medium=grass green #4CAF50, high=forest green #1B5E20]
  Heat coloring: error rate metric overlays as red tint on vertex color when error rate > threshold (default threshold = 0.8 of max). Intensity = (errorRate - threshold) / (1.0 - threshold) * 0.5 added to red channel
  Time reshaping: on slider change, rebuild height values from the selected timestep column. Reuse existing position attribute, write new y-values, set needsUpdate = true. No new geometry allocation
  Disposal: on data source change, call geometry.dispose() on old terrain before creating replacement
Rivers (Error Paths)
  Input: array of { path: Vector2[], errorRate: number } objects
  Geometry: for each error path, create a flat ribbon mesh using BufferGeometry
    - For each segment, compute perpendicular from actual segment direction as described in Geometry Derivation section
    - River width scales with errorRate: baseWidth = 0.1 world units, maxWidth = 0.5 world units
    - River depth: carve 0.3 units below terrain surface
  Material: MeshBasicMaterial with color interpolated from orange (#FF6B35) at errorRate=0.5 to red (#FF0000) at errorRate=1.0, opacity=0.8
  River channels that have zero error across all timesteps: do not render. No invisible geometry
Particles (Data Flows)
  Type: Points with PointsMaterial, size = 0.08 world units, color = #FFD700 (gold)
  Count: proportional to API call volume, minimum 0, maximum 2000
  Movement: particles flow along valley paths computed from terrain's lowest elevation routes. Path direction = generalization of gradient descent on heightfield
  Update: offload position updates to vertex shader using custom ShaderMaterial when count > 1000. For count <= 1000, use CPU-side Float32Array reused across frames
  Birth/death: each particle has lifetime = 3 seconds. On death, respawn at path start with random phase offset. Particle age tracked via a custom attribute
Controls (OrbitControls)
  Smooth damping: dampingFactor = 0.08, enabled = true
  Auto-rotation: controls.autoRotate = true, controls.autoRotateSpeed = 1.0
  Limits: minDistance = 2, maxDistance = 50, minPolarAngle = 0.1, maxPolarAngle = Math.PI / 2.1 (prevent going below terrain)
  Bookmark system:
    - Ctrl+Shift+1..9 saves current camera position to slot N (stores position + target via controls.object.position.clone() and controls.target.clone())
    - 1..9 restores camera position from slot N via tween/animation over 500ms
    - Bookmarks persist in localStorage under key 'terrain-bookmarks'
    - Bookmark UI: dropdown or numbered buttons in dashboard header showing slot number and a label (user-editable)
Time Slider
  Type: HTML range input with step = 1 over timestamp count
  Behavior: on 'input' event (not 'change'), update terrain heights, river positions, and particle counts
  Throttle: debounce terrain rebuild to every 50ms. If slider moves faster, skip intermediate frames. Use requestAnimationFrame to schedule the actual rebuild
  Play button: auto-scrub through timestamps at 2 fps toggle. Use setInterval with clearInterval on pause
  Time indicator: display current timestamp label from data, formatted as locale date string
Bookmark System
  Storage: slots 0-9 saved as JSON array in localStorage key 'terrain-bookmarks'
  Each bookmark: { label: string, position: { x, y, z }, target: { x, y, z }, timestamp: number }
  Restore: animate camera from current to bookmarked position + target over 500ms using a simple lerp in requestAnimationFrame
  UI: labeled buttons in dashboard header, one per occupied slot. Empty slots shown as grey dashed outline
Implementation Guidance
Edge Cases and Error Recovery
Three.js Context Lifecycle:
  1. Create WebGLRenderer only after DOM container is present (guard with if (!document.getElementById('dashboard-container')) return)
  2. On context lost (webglcontextlost event): show overlay 'WebGL context lost - attempting recovery', pause all animation, store current state
  3. On context restored (webglcontextrestored event): reinitialize scene objects from stored state, resume render loop
  4. WebGL unavailable: fall back to Canvas2D terrain renderer with reduced visual fidelity. Never blank the dashboard
Data gaps and missing metrics:
  1. Missing revenue value for a timestep: interpolate from adjacent timesteps. If both neighbors missing, set height to 0 (flat)
  2. Missing user density: default vertex color to medium green #4CAF50
  3. Missing error rate: skip river rendering for that path, log to diagnostic panel
  4. All metrics missing for a timestep: show flat terrain with grey color. Display 'no data' indicator in time slider
Bookmark slot overflow:
  1. If slot N already occupied when saving, prompt confirmation dialog 'Overwrite bookmark [label] in slot N?'
  2. If localStorage is full (QuotaExceededError), catch it, display 'Bookmark storage full - export or delete existing bookmarks' indicator
Performance degradation:
  1. Track frame time via THREE.Clock. If frame time exceeds 33ms (< 30 fps) for 10 consecutive frames, reduce particle count by 50% and show 'Performance mode' indicator
  2. Allow user to manually toggle quality: high (256x256 terrain, 2000 particles, shadows on) / medium (128x128, 1000 particles, shadows off) / low (64x64, 500 particles, shadows off)
  3. On low quality, disable river opacity and use flat shaded material (MeshBasicMaterial instead of MeshStandardMaterial)
Worked Examples
Example 1: Terrain Height from Revenue Data
Input: Revenue data for Q1 2025 across 12 timesteps (monthly): [120, 145, 110, 160, 190, 175, 210, 195, 230, 250, 220, 280]. User sets time slider to index 5 (June, value 175).
Invariants:
  - Terrain grid: PlaneGeometry(10, 10, 64, 64). 65x65 = 4225 vertices
  - Each vertex position is mapped from the 64x64 grid to revenue data using bilinear interpolation
  - Height range: [0, 10] world units mapped to revenue range [min=110, max=280]
  - Vertex (i, j) at grid position x = (j/64 - 0.5) * 10, z = (i/64 - 0.5) * 10
  - Height for vertex at grid frac (u, v) = interpolate(revenue_data[month], u, v) mapped to world Y
  - At time index 5: revenue value 175. Map: 0 + ((175 - 110) / (280 - 110)) * 10 = 0 + (65/170) * 10 = 3.824 world units
Step-by-step:
  1. User drags time slider to index 5 (June).
  2. Debounce timer starts: 50ms window. If slider moves again before timer fires, reset timer.
  3. After 50ms: event handler fires.
  4. Read heightmap data: Q1_2025[5] = { revenue: 175, users: 4200, errors: 0.03, apis: 15000 }
  5. Compute terrain heights: for each vertex (i, j), map grid position to interpolated revenue 175. Since this is a single uniform value for the whole terrain (not spatially varying), all vertices get the same height 3.824.
     Note: In real usage, revenue data includes spatial distribution (e.g., by region). The example shows uniform terrain for simplicity.
  6. Access terrain.geometry.attributes.position: write new y-values into the existing Float32Array at positions 1, 4, 7, ... (every 3rd element starting at index 1).
  7. Set position.needsUpdate = true, computeVertexNormals().
  8. River positions: error rate 0.03 is below threshold (0.8), so no river carving for this timestep. Existing rivers from previous timestep are removed.
  9. Particle count: 15000 API calls maps to floor(15000 / 20000 * 2000) = 1500 particles.
  10. Render: terrain at height 3.824, no rivers, 1500 gold particles flowing along valley paths.
  11. Time indicator updates: 'June 2025'.
Output: Terrain at uniform height 3.824 world units. No rivers visible. 1500 particle trails active.
Example 2: River Carving Along Curved Error Path
Input: Error path points in 2D grid space: [(0, 0), (2, 1), (4, 0), (6, 3), (8, 2)]. Error rate at each point: [0.5, 0.6, 0.8, 0.9, 0.7]. Terrain is at a flat height of 2.0.
Invariants:
  - River base width = 0.1, max width = 0.5. At error rate 0.5: width = 0.1 + (0.5 - 0.5)/(1.0 - 0.5) * 0.4 = 0.1. At 0.9: width = 0.1 + (0.9 - 0.5)/0.5 * 0.4 = 0.42.
  - River depth = 0.3 units below terrain surface, so vertices at y = 2.0 - 0.3 = 1.7.
  - Perpendicular computed from actual segment direction, not hardcoded.
Step-by-step:
  1. Convert grid points to world coordinates: scale by tile size 1 unit per grid step.
     world = [(0,0,0), (2,0,1), (4,0,0), (6,0,3), (8,0,2)].
  2. For segment 0-1: direction = normalize((2,0,1) - (0,0,0)) = normalize(2,0,1) = (0.894, 0, 0.447).
     Perpendicular = cross(direction, up) = cross((0.894,0,0.447), (0,1,0)) = (-0.447, 0, 0.894). Normalized.
  3. At point 0: left edge = (0,1.7,0) + (-0.447, 0, 0.894) * 0.05 = (-0.022, 1.7, 0.045)
     right edge = (0,1.7,0) - (-0.447, 0, 0.894) * 0.05 = (0.022, 1.7, -0.045)
     (width at error rate 0.5 = 0.1, half-width = 0.05)
  4. For segment 1-2: direction = normalize((4,0,0) - (2,0,1)) = normalize(2,0,-1) = (0.894, 0, -0.447).
     Perpendicular = cross((0.894, 0, -0.447), (0,1,0)) = (0.447, 0, 0.894). Different from segment 0-1 perpendicular.
  5. At point 2 (peak error 0.8): width = 0.1 + (0.8-0.5)/0.5 * 0.4 = 0.34, half-width = 0.17.
     left edge = (4,1.7,0) + (0.447,0,0.894) * 0.17 = (4.076, 1.7, 0.152)
     right edge = (4,1.7,0) - (0.447,0,0.894) * 0.17 = (3.924, 1.7, -0.152)
  6. Build river ribbon mesh: 5 center points -> 4 segments, each segment produces 2 triangles (6 indices). Total 8 triangles, 10 vertices.
  7. Color: interpolate from orange (#FF6B35) at error=0.5 to red (#FF0000) at error=1.0.
     At point 0 (0.5): #FF6B35. At point 2 (0.8): lerped color #FF3B1A (80% toward red). At point 3 (0.9): #FF1109.
  8. Add river mesh to scene. Ensure it renders on top of terrain by setting renderOrder = 1 on the material.
Output: River ribbon 0.1-0.42 wide, curving with the error path, colored orange to near-red, sitting 0.3 units below terrain surface.
Error-Handling Edge Cases
Scene graph leak on rapid time scrubbing:
  Each slider tick adds new river meshes and particles to scene. If user scrubs through 50 timesteps in 1 second, scene accumulates 50 stale river meshes and particle systems.
  Resolution: before adding new river/particle geometry, iterate scene.children and remove all objects tagged with userData.type === 'river' or userData.type === 'particle', disposing their geometry and material. Use a single group per type (riversGroup, particlesGroup) that gets emptied and repopulated per tick.
Degenerate river paths:
  A river path with fewer than 2 unique points has no segments.
  Resolution: filter paths with points.length < 2 before entering river geometry builder. Log to console: 'Skipping degenerate river path (id: X)'.
Zero-revenue timestep (flat terrain):
  If revenue for a timestep is 0 or null across all grid cells, terrain height is uniformly 0. No geometry is invalid - flat terrain is valid and should render as grey plane.
  Resolution: set all vertex y-values to 0, set all vertex colors to grey #808080. Display 'Flat terrain: no revenue data' in diagnostic panel.
Missing bookmark target on restore:
  Bookmark stored in localStorage but referenced slot has null or undefined target.
  Resolution: on restore, check slot.data.target !== undefined. If null, fall back to current controls.target (no camera move). Clear corrupt slot and log 'Bookmark slot N corrupted - cleared'.
OrbitControls going below terrain:
  If minPolarAngle / maxPolarAngle constraints fail (e.g., user scrolls past limit), camera dips below terrain revealing untextured underside.
  Resolution: add a GroundPlane at y=-0.1 with MeshBasicMaterial color #2C1810 (dark brown, underside color). This catches any camera dip below terrain gracefully. In addition, enforce controls.maxPolarAngle = Math.PI / 2.1 at setup and re-apply on every controls.update() call via controls.addEventListener('change').
Deliver
  Produce an interactive single-file HTML page containing all Three.js code inline via CDN (unpkg or cdnjs script tags for three.min.js and OrbitControls).
  File must pass a self-contained check: no external resources except the two CDN script tags.
  Verify: open in browser, terrain renders, slider moves, rivers appear, particles flow, OrbitControls respond to mouse.
  Then mark done.
Pre-Submit Validation
Run this checklist immediately before outputting the final blueprint or generated code:
Stale marker scan:
  [ ] No text matching 'unchanged from original', 'TODO:', 'FIXME', 'XXX', or any placeholder marker that references a non-existent original
  [ ] Every placeholder value (e.g., sample data, test paths, example URLs) is either concrete or explicitly marked with '[EXAMPLE]' prefix
  [ ] All person-referencing comments ('the user', 'the developer', 'the agent') are resolved to the agent executing the blueprint
Contradiction scan:
  [ ] No two instructions conflict on the same operation (e.g., one saying 'use setTargetAtTime' and another saying 'use gain.value =')
  [ ] No constraint says both 'must' and 'must not' for the same behavior
  [ ] Performance limits are consistent across all sections (e.g., max vertex count in Terrain Generation matches max in Performance Requirements)
  [ ] All named constants (thresholds, ranges, limits) appear exactly once with a single value - no redefinition
  [ ] All skill references are actual skills listed in the Skills section - no orphaned skill mentions
Framework check cross-reference:
  [ ] Every custom animation/rotation/movement has a corresponding Framework Integration checkbox that was verified before writing
  [ ] Every vector derivation (perpendicular, tangent, normal) references actual path geometry - confirmed by scanning all 'new Vector3' or 'cross' calls
State audit verification:
  [ ] All dispose() calls in the code match every new Geometry/Material creation - no leaks
  [ ] Buffer attribute reassignment uses .array.set() not new Float32Array()
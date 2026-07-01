3D Data Terrain Explorer
Domain: dashboard
Version: 1
Purpose
Three.js-powered 3D data landscape where metrics become physical terrain. Revenue = elevation (hills and mountains), user density = vegetation color, error rates = red rivers carving through the landscape, API calls = light trails flowing along valleys. Users fly through their data using OrbitControls with smooth damping and auto-rotation. Time slider reshapes the terrain as metrics evolve. Camera bookmarks save and restore positions for recurring views.
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
Before writing any custom rotation, movement, or camera animation logic, verify that the framework's built-in API handles the requirement.
Checklist (run in order before writing custom code):
1. OrbitControls: does the built-in API cover this? For auto-rotation, use controls.autoRotate = true with controls.autoRotateSpeed. Do not create a manual rotation loop that fights OrbitControls.update().
2. Animation loop: use the framework's render loop (requestAnimationFrame callback calling controls.update()). Do not create a second independent animation loop.
3. Event handling: use OrbitControls event listeners (start, change, end) for camera-position-dependent logic. Do not poll camera position inside the render loop.
4. Camera bookmarks: use controls.target and camera.position.copy/lerp with the framework's existing update cycle. Do not write a separate camera state machine.
5. Damping: enable controls.enableDamping = true. Do not implement smooth interpolation on top of a non-damped controls setup.
6. Only if all five checkboxes fail (none applies): write minimal framework-aware custom code that does not call controls.update() after its own transforms.
Any implementation that creates a second rotation vector or angle accumulator while controls.autoRotate is available fails review.
Geometry Derivation
All vectors derived from path geometry (normals, perpendiculars, tangents, up vectors) MUST be computed from the actual path direction at runtime. Constants that assume a fixed direction (e.g., hardcoded positive-x axis as perpendicular) are forbidden.
Rules:
1. River path direction: given path segments defined as an array of 3D points [p0, p1, ..., pn] where p0 is the start and pn is the end, compute the segment direction vector as segDir = normalize(p[i+1] - p[i]) for each segment.
2. Perpendicular from direction: given a direction vector d, compute a perpendicular vector perp via the cross product with the scene up vector (typically (0,1,0)): perp = normalize(cross(d, up)). If d is nearly parallel to up (abs(dot(d, up)) > 0.99), fall back to cross(d, (1,0,0)).
3. River width extrusion: use the perpendicular perp to offset river vertices left and right of the path: left = p + (width/2) * perp, right = p - (width/2) * perp. Repeat per segment.
4. Terrain normal: compute from the cross product of two adjacent terrain grid edge vectors, not from a fixed up vector.
5. Particle flow direction: use the terrain gradient at each particle's current position to determine drift direction at that frame. Do not pre-compute a global flow field unless the data explicitly defines one.
Violation: any file containing a constant perpendicular or normal vector (e.g., vec3(1,0,0) without deriving from segment direction) fails review.
Performance Requirements
Cache: pre-build geometry variants and swap buffers on slider change rather than calling new THREE.BufferGeometry() every tick. Use BufferGeometry.attributes.position.array as a typed array and update via .needsUpdate = true.
Particles: offload particle position updates to a vertex shader or use BufferGeometry with CPU-side position array reuse instead of allocating per-frame position objects with clamp + terrain lookups.
State Audit checklist (run after writing initialization and update loops):
1. Review all constructed objects for duplicate properties. If a property appears on the same object twice (once from a base class, once from the subclass), remove the duplicate.
2. Verify that no object creation (new THREE.Xxx()) occurs inside the render loop or on every animation frame. Creation is allowed only during initialization, resize handlers, and data updates.
3. Check for buffer thrashing: BufferGeometry attributes must not be re-created per frame. Re-use the attribute array and set needsUpdate = true.
4. Ensure that all disposable resources (render targets, geometries, materials, textures) have a corresponding .dispose() call triggered when the component unmounts or the data source changes.
5. Confirm that the render loop calls controls.update() exactly once per frame, not zero times and not twice.
Any file with object allocation inside a requestAnimationFrame callback fails review.
Camera Bookmark System
Camera bookmarks store the camera position and controls target at a given moment, allowing instant or animated recall.
Storage:
- Bookmarks array: [{id: string, label: string, position: Vector3, target: Vector3}]
- Persisted to localStorage under key 'terrain-bookmarks' as JSON.
- Maximum 20 bookmarks. If the 21st is added, remove the oldest (by insertion order) before inserting.
Recall (instant):
1. camera.position.copy(bookmark.position)
2. controls.target.copy(bookmark.target)
3. controls.update()
Recall (animated):
1. Animate camera.position and controls.target via a simple lerp in the render loop over 800 ms.
2. During animation, set controls.enabled = false to prevent user interaction from fighting the animation.
3. On animation complete (distance < 0.01 from target), set controls.enabled = true.
Capture:
1. Read current camera.position and controls.target.
2. Prompt user for a label (default: "Viewpoint {bookmarks.length + 1}").
3. Generate a 6-character alphanumeric id (Math.random().toString(36).slice(2, 8)).
4. Push to bookmarks array, persist to localStorage.
Delete: remove by id from the bookmarks array, persist.
Bookmark buttons are rendered as a horizontal list below the terrain canvas. Each button shows the label. A "Save Current View" button captures the current position. Clicking a bookmark button triggers animated recall.
Constraints:
- Bookmark render must be a targeted DOM update (update only the button whose label changed), not a full list re-render.
- localStorage writes must be debounced (300 ms) to avoid thrashing on rapid add/delete.
- On page load, bookmarks array is hydrated from localStorage. If localStorage key is missing or JSON parse fails, start with empty array.
Data Ingestion
External data sources MUST use one of the following concrete ingestion paths:
- WebSocket endpoint (ws://host:port/metrics-stream) for real-time streaming data
- POST endpoint (POST http://host:port/api/ingest) for batch/event-driven data
- File-drop handler (drag-and-drop CSV/JSON file onto the dashboard) for offline/development data
All three paths converge into a single internal MetricBus that feeds all 3D components (terrain height updates, particle flow rates, river erosion depth, color mapping).
UI Components
The dashboard panel contains:
- 3D viewport (full background canvas with Three.js renderer)
- Time slider (range input, min/max from data time range, step = data interval)
- Play/pause button for time animation
- Speed control for time animation speed multiplier (0.5x, 1x, 2x, 4x)
- Bookmark bar (horizontal list of bookmark buttons + Save Current View)
- Metric legend (color bar showing the range mapped to vertex colors)
- Performance overlay (FPS counter, vertex count, draw calls) toggled via 'P' key
Worked Examples
Example 1: River Along Curved Path
Input: Path points [(0,0,0), (5,0,2), (10,0,-1), (15,0,3)] defining a river through terrain. River width = 0.3 units. Terrain height at each point is read from the heightmap at those x,z coordinates.
Invariants:
- River direction is computed from consecutive segment differences, never hardcoded.
- Each segment generates a perpendicular via cross product with (0,1,0).
- Left and right vertices are offset by half the width along the perpendicular.
- Consecutive segments share the last left/right vertex of the previous segment (no gaps).
- Terrain height lookup uses the heightmap's getHeight(x,z) method which bilinearly interpolates the 2D grid.
Step-by-step:
1. Compute segment vectors: s0 = (5,0,2), s1 = (5,0,-3), s2 = (5,0,4).
2. Normalize each: d0 = (0.86, 0, 0.34), d1 = (0.86, 0, -0.52), d2 = (0.62, 0, 0.78).
3. For d0, perpendicular cross(d0, (0,1,0)) = (-0.34, 0, 0.86).
4. Segment 0 left vertex = p0 + (0.15)*(-0.34, 0, 0.86) = (-0.05, 0, 0.13). Right = (0.05, 0, -0.13).
5. Repeat for d1 and d2. Segment 1 left = p1 + (0.15)*cross(d1, up) = (5, 0, 2) + (0.15*(0.52, 0, 0.86)) = (5.08, 0, 2.13). Right = (4.92, 0, 1.87).
6. Triangulate: each quad (left[i], right[i], left[i+1], right[i+1]) becomes two triangles.
7. Look up terrain height at each vertex: terrain.getHeight(x, z) returns the interpolated elevation. Apply as y-coordinate on all vertices.
8. Push vertices into a single BufferGeometry and set needsUpdate = true.
Output: A continuous river mesh following the curved path, 0.3 units wide, conforming to terrain elevation.
Example 2: Auto-Rotation Toggle
Input: OrbitControls instance with damping enabled. User clicks an auto-rotate toggle button.
Invariants:
- Auto-rotation uses built-in controls.autoRotate, never a manual rotation around the y-axis.
- controls.autoRotateSpeed respects the current speed multiplier setting.
- When auto-rotation is active, controls.update() is still called exactly once per frame.
- Toggling auto-rotation off transitions smoothly because damping is already active.
Step-by-step:
1. User clicks "Auto-Rotate" button.
2. Read current state: controls.autoRotate = false.
3. Set controls.autoRotate = true.
4. Set controls.autoRotateSpeed = 2.0 (default).
5. Render loop continues calling controls.update() once per frame.
6. Camera begins orbiting the controls.target at 2.0 radians per second.
7. User clicks again: controls.autoRotate = false.
8. Camera stops due to damping. No jump, no explicit position reset.
Output: Camera slowly orbits the terrain center. Toggle off produces a smooth stop.
Error-Handling Edge Cases
Orphaned Disposables After Source Removal
When a data source is removed (WebSocket disconnect, file closed), all Three.js objects associated with that source (geometry, material, texture, mesh) must be disposed.
Resolution:
1. Maintain a registry Map<sourceId, {meshes: Set<Mesh>, geometries: Set<BufferGeometry>, materials: Set<Material>, textures: Set<Texture>>.
2. On source removal, iterate the registry entry and call .dispose() on every object.
3. Remove disposed objects from the scene via scene.remove(mesh).
4. Remove the registry entry.
5. If source removal also affects the terrain heightmap, recompute terrain geometry and set attributes.needsUpdate = true.
Edge sub-case: if a texture is shared between two source meshes and one source is removed, decrement a refcount on the texture. Only dispose when refcount reaches zero.
Overflow in Heightmap Bounds
When a metric value maps to a height exceeding the terrain's vertical range:
Resolution:
1. Clamp height to the range [terrainMinHeight, terrainMaxHeight] before writing to the buffer: h_clamped = Math.max(minH, Math.min(h, maxH)).
2. Log the clamp event to the diagnostic panel once per distinct source per session.
3. If more than 50% of vertices in a single frame are clamped to the boundary, auto-expand the terrain vertical range by 20% and recalculate the color gradient range.
Orphaned Auto-Rotation After Orbit Interaction
When the user manually drags the camera while auto-rotation is active:
- OrbitControls handles this correctly by default: user interaction overrides auto-rotation momentarily, then resumes.
- No additional code needed. Explicitly verify that controls.autoRotate remains true during and after the interaction — the framework manages the override.
- Do not implement a timer or delay that resets camera position after user interaction. Let controls.autoRotate handle the resume naturally.
Memory Pressure on Long-Running Sessions
Over hours of operation, particle systems accumulate positions that may overflow typed array size.
Resolution:
1. Particle position buffer uses a ring buffer: oldest particle data is overwritten by the newest.
2. Max particles = 50000. Beyond this, the ring buffer wraps.
3. When the buffer wraps, increment a wrap counter visible in the performance overlay.
4. Every 10 minutes, run a GC-friendly compaction: create a new typed array, copy the unwrapped segment, splice at the current write head, assign to the attribute.
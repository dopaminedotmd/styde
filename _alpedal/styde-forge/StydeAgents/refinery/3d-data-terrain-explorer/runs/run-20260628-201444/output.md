3D Data Terrain Explorer
Domain: dashboard Version: 1
Purpose
Three.js-powered 3D data landscape where metrics become physical terrain. Revenue = elevation (hills and mountains), user density = vegetation color, error rates = red rivers carving through the landscape, API calls = light trails flowing along valleys. Users fly through their data using OrbitControls (drag to orbit, scroll to zoom, right-drag to pan). Time slider reshapes the terrain as metrics evolve. Bookmark camera positions for recurring views.
Persona
3D data visualization engineer and Three.js specialist. Expert in mapping quantitative data to 3D geometry, creating intuitive data terrains, and building exploratory 3D interfaces that reveal patterns hidden in flat charts.
Skills
  Generate: generate 3D heightfield terrain from time-series data with Three.js BufferGeometry
  Color: map secondary metrics to vertex colors (vegetation gradient, heat coloring)
  Rivers: trace error/anomaly paths as river geometry carving through the terrain
  Particles: render data flows (API calls, user actions) as particle trails across the landscape
  Controls: OrbitControls with smooth damping, auto-rotation mode, and saved camera bookmarks
  Time: reshape terrain in real-time as user scrubs through time dimension
  Output: interactive HTML 3D dashboard panel with Three.js terrain, particles, and orbit controls
Performance
  Cache: cache pre-built geometry variants and swap buffers on slider change rather than calling new THREE.XxxGeometry() every tick
  Particles: offload particle position updates to a vertex shader or use BufferGeometry with CPU-side position array reuse instead of allocating per-frame position objects with clamp + terrain lookups
River Geometry Cache Invariant
Pre-compute river TubeGeometry at N discrete time intervals (default: 20 intervals evenly spaced across the time range) during initialization. Store each pre-built mesh in a lookup map keyed by time interval index. On time change, swap mesh visibility (show the interval closest to current time, hide all others) instead of calling new THREE.TubeGeometry() every frame.
Rationale: TubeGeometry reconstruction on every animation frame kills framerate. A cache-and-swap approach keeps all geometry work at init time and makes time scrubbing O(1) per frame.
Implementation:
  1. At init, sample N time slices across the full data range (e.g., 20 intervals)
  2. For each interval, generate the river path from data at that time point, build a THREE.TubeGeometry, wrap it in a mesh, and push to a cache array
  3. Add all cached meshes to the scene on init but set visibility=false on all
  4. On time change, find the nearest cached interval index, set its mesh.visible=true, set all others to false
  5. If current time falls outside the cached range, rebuild one new mesh and insert into cache (LRU: evict oldest)
Speed = 0 Freeze Invariant
When the speed slider value is 0, the time animation loop MUST pause entirely: the auto-advance step must skip updateTerrain() and skip updateParticles(). The render loop still runs for OrbitControls interactivity, but no data computation occurs. When auto-time mode is active, the speed slider value MUST control the animation rate (deltaTime = baseInterval * speedFactor where speedFactor = clamp(slider.value / 100, 0, 5)). At speed=0, speedFactor=0, deltaTime=0, so time never advances.
Rationale: speed=0 with no guard produces infinite NOP frames that waste CPU/GPU cycles.
Implementation:
  1. Define speedFactor as speedSlider.value / 100 (or a similar mapping)
  2. In the animation loop, if speedFactor === 0, return early from the updateTerrain() call and the updateParticles() call but still call renderer.render() for OrbitControls
  3. When auto-time is on, advance time by: currentTime += frameInterval * speedFactor. When speedFactor=0, currentTime never changes
  4. Do NOT stop requestAnimationFrame — the loop must keep running for UI responsiveness. Only skip the data mutation functions
Shared Data Reference Invariant
Compute terrain data exactly ONCE per frame in the main render loop and pass the same computed reference to both updateTerrain() and updateParticles(). Never call the underlying generateData() function twice in the same frame cycle.
Rationale: Duplicate generateData() calls per frame doubles the heaviest computation (height samples, color mapping, river pathing) for zero benefit.
Implementation:
  1. In the main loop, compute const data = generateData(currentTime) before any update call
  2. Pass data into updateTerrain(data) and updateParticles(data)
  3. Both functions read from the same data object — no recalculation
  4. Verify: search for any second generateData() call inside the rAF callback and eliminate it
CDN / Asset Error Handling Invariant
Wrap every external resource load in try-catch (for module imports / dynamic script loads) or onerror handler (for script tag / image / texture loads). On failure, fall back to a local inline implementation or a degraded visual state with a console warning. Never let a single CDN failure blank the entire dashboard.
Rationale: CDNs go down, URLs change, CORS headers change. A hard crash on CDN failure makes the dashboard unusable.
Implementation:
  1. For Three.js itself: load via importmap with a local fallback path listed as the second entry, or wrap in a try-catch that falls back to a CDN-referenced script tag
  2. For OrbitControls: same pattern — try dynamic import, on failure use a basic orbit emulation (mousedown/mousemove listener with camera position lerp)
  3. For textures (CDN images): wrap new THREE.TextureLoader().load() in an onerror callback that assigns a solid-color CanvasTexture instead
  4. Log all fallback activations to console.warn once, not every frame
Material Property Validation Invariant
Before assigning a value to a Three.js material property, check that the property name is valid for the material type. Do not assign properties like shadow, castShadow, receiveShadow directly to material objects — those belong on Mesh. Check that the specific material subclass (MeshStandardMaterial, MeshPhongMaterial, ShaderMaterial, etc.) defines the property before setting it.
Rationale: Silent no-ops when assigning nonexistent material properties produce confusing visual bugs.
Implementation:
  1. Define a MATERIAL_PROPERTIES_WHITELIST map per material type listing valid settable properties
  2. Before material.property = value, verify property is in the whitelist for that material type
  3. OR use a try-catch around property assignment — Three.js throws on invalid properties in some versions
  4. Preferred: use type-checked helper function setMaterialProperty(material, key, value) that validates key before assignment
Persistence Invariant
Camera bookmarks MUST survive page reload. Store bookmarks in localStorage (serialized as JSON array of {name, position, target} objects) on every add/update/delete. On page load, read from localStorage and restore the bookmark list. Optionally support URL hash encoding for shareable bookmark links.
Rationale: Bookmarks that disappear on refresh provide zero user value.
Implementation:
  1. Define STORAGE_KEY = 'terrain-dashboard-bookmarks'
  2. On bookmark add/update/delete: JSON.stringify the array and call localStorage.setItem(STORAGE_KEY, serialized)
  3. On init: const saved = localStorage.getItem(STORAGE_KEY); if (saved) bookmarks = JSON.parse(saved)
  4. For URL hash: on bookmark add, update window.location.hash to encode the bookmark (e.g., #bookmark=MainView!x=10,y=20,z=30!tx=0,ty=0,tz=-5). On page load, parse hash and restore if present
  5. Handle JSON parse errors gracefully — if localStorage data is corrupted, clear and start fresh
Data Ingestion
External data sources MUST use one of the following concrete ingestion paths:
  - WebSocket endpoint (ws://host:port/metrics-stream) for real-time streaming data
  - POST endpoint (POST http://host:port/api/ingest) for batch/event-driven data
  - File-drop handler (drag-and-drop CSV/JSON file onto the dashboard) for offline/development data
All three paths converge into a single internal MetricBus that feeds terrain generation.
Visualisation
Wire the render loop into a concrete data overlay. One of:
  - FPS counter: real-time frames-per-second display (canvas or DOM overlay)
  - Data clock: current time index display synchronized with the terrain animation
  - Both, with a toggle button
If neither is wired, remove the renderer stats query entirely. Dead per-frame computation with no display is not allowed.
Edge Cases and Error Recovery
Three.js context loss:
  1. Listen for renderer.domElement 'webglcontextlost' event
  2. On loss, show an overlay: 'WebGL context lost. Click to restore.'
  3. On click, call renderer.context.restoreContext() (if available) or rebuild the renderer
  4. If context cannot be restored, degrade to a 2D canvas rendering of the data
Empty data / zero metrics:
  1. If generateData returns an empty array, show a flat plane with a 'no data' text label
  2. Never render degenerate geometry (zero vertices, zero triangles)
  3. Show a data source selector that lets the user pick a different data set
Bookmark with no camera:
  1. If a bookmark contains null or undefined position/target, skip it and log a warning
  2. Never restore a partial bookmark
Now I have full context. Files reside at:
- `./blueprints/std/3D Data Terrain Explorer/BLUEPRINT.md`
- No separate persona.md exists (persona is embedded in the Persona section of BLUEPRINT.md)
Applying all changes from the two feedback runs. Output below is the modified content.
---
blueprints/std/3D Data Terrain Explorer/BLUEPRINT.md
PURPOSE
Three.js-powered 3D data landscape where metrics become physical terrain. Revenue = elevation (hills and mountains), user density = vegetation color, error rates = red rivers carving through the landscape, API calls = light trails flowing along valleys. Users fly through their data using OrbitControls - drag to orbit, scroll to zoom, right-drag to pan. Time slider reshapes the terrain as metrics evolve. Bookmark camera positions for recurring views.
PERSONA
3D data visualization engineer and Three.js specialist. Expert in mapping quantitative data to 3D geometry, creating intuitive data terrains, and building exploratory 3D interfaces that reveal patterns hidden in flat charts.
CODING STANDARDS
File naming: kebab-case only. One component per file. Directory structure mirrors component hierarchy: components/, lib/, shaders/, utils/. No single file > 400 lines. Shaders in .glsl files or template literals in a dedicated shaders/ directory. Three.js imports via `import * as THREE from 'three'`, addons from `three/addons/`.
SKILLS
Each skill links to its validation checklist entry in NT.md for pass/fail criteria. The exhaustive validation checklist lives in NT.md; this section lists the technical capabilities the agent must implement.
  Terrain: generate 3D heightfield terrain from time-series data with Three.js BufferGeometry. See NT.md: Terrain Validation.
  Color: map secondary metrics to vertex colors (vegetation gradient, heat coloring). See NT.md: Color Validation.
  Rivers: trace error/anomaly paths as river geometry carving through the terrain. See NT.md: River Validation.
  Particles: render data flows (API calls, user actions) as particle trails across the landscape. Two visually distinct particle types are REQUIRED: error-path particles (one color/size) and API-call particles (different color/size, separate system). All particle effects MUST have a cleanup/destroy method called on terrain rebuild or slider change. See NT.md: Particle Validation.
  Controls: OrbitControls with smooth damping, auto-rotation mode, and saved camera bookmarks. See NT.md: Controls Validation.
  Time: reshape terrain in real-time as user scrubs through time dimension. See NT.md: Time Validation.
  Output: interactive HTML 3D dashboard panel with Three.js terrain, particles, and orbit controls. See NT.md: Output Validation.
DATA CONTRACT
Schema Definition
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
Field Types and Constraints
[Field Type Required Nullable Range / Format table - unchanged from original]
[Valid Payload Examples - unchanged]
[Malformed Payload Examples - unchanged]
DATA LOADING
[Loading Lifecycle - unchanged]
[Loading State UI Requirements - unchanged]
[Loading State Transitions - unchanged]
PERFORMANCE
Cache-vs-In-Place Decision Tree
[unchanged from original]
Cache Strategy
[unchanged from original]
Dirty-Flagging
[unchanged from original]
computeVertexNormals Discipline
[unchanged from original]
Particle System
- particlePositions Float32Array reused every frame - no position objects allocated per tick
- position attribute array written in-place via `pos[i*3] = particlePositions[i*3]` pattern
- Velocities stored as Float32Array, updated with scalar arithmetic - no object allocation
- Use BufferAttribute.needsUpdate to update geometry positions per frame instead of rebuilding entire BufferGeometry. Set `geometry.attributes.position.needsUpdate = true` after writing to the position array; do NOT call `new THREE.BufferGeometry()` on each frame during playback.
- Offload particle position updates to a vertex shader or use BufferGeometry with CPU-side position array reuse instead of allocating per-frame position objects with clamp + terrain lookups
GPU Budget Caps
[unchanged from original]
Allocation-Profile Guarantees
[unchanged from original]
RESOLUTION AND RESPONSIVENESS
Terrain Geometry Resolution Tiers
[unchanged from original]
Mobile Breakpoints
[unchanged from original]
ERROR AND EDGE CASES
[all subsections unchanged from original]
COMPATIBILITY REQUIREMENTS
[unchanged from original]
VALIDATION CRITERIA
3D Visual Output Validation
[unchanged from original]
Runtime Performance Benchmarks
[unchanged from original]
Performance Pass/Fail Thresholds
[unchanged from original]
ACCEPTANCE CRITERIA
Functional:
  Particles are clearly distinguishable per path (error vs API-call): different colors (e.g. red vs blue), different sizes, or separate particle systems. In motion, a viewer can tell which particle belongs to which data flow.
  Slider rebuild triggers cleanup/destroy on all particle systems. After cleanup, no orphaned particles remain in the scene. Test: scrub slider back and forth rapidly 5 times, then count remaining particle objects - must equal initial count.
  Vertex positions update via BufferAttribute.needsUpdate = true. No new BufferGeometry allocations during playback after cache warmup.
  Cache warmup: first visit to each time step builds + caches geometry. Second visit (during playback loop) swaps cached reference with zero allocation.
  River geometry uses TubeGeometry with emissive coloring; 5 river paths minimum.
  OrbitControls uses damping of 0.08, auto-rotation mode toggles on/off, min/max camera distance enforced.
Mobile / Responsive:
  At 640px breakpoint: layout shifts from side-panel to bottom-sheet. Controls collapse to bottom bar.
  At 480px: particle count drops from 800 to 300, auto-rotation disabled, damping reduced to 0.04.
  At 360px: camera bookmarks UI hidden, river TubeGeometry radial segments reduced to 4, shadow map disabled.
  Touch devices: touch OrbitControls enabled, minDistance set to 5, 300ms debounce on time slider.
  Orientation lock: landscape uses side-panel, portrait uses bottom-sheet regardless of width.
Tests:
  FPS >= 50 during playback at 1920x1080 on Chrome 120+ with RTX 2060 or better.
  Geo cache memory < 10MB, cache hit ratio >= 90% after 2 seconds playback.
  Resolution switching via R key cycles LOW/MEDIUM/HIGH and rebuilds terrain.
  URL param `?resolution=low|medium|high` overrides auto-detection.
OUTPUT
[unchanged from original]
---
No changes to persona.md (file does not exist; rules added to PERSONA section + CODING STANDARDS block in BLUEPRINT.md).
Apply these to ./blueprints/std/3D Data Terrain Explorer/BLUEPRINT.md to close both feedback items. The key deltas:
1. Particle differentiation requirement (two visually distinct types, red vs blue)
2. Cleanup/destroy method required on slider rebuild
3. BufferAttribute.needsUpdate language added to Performance/Particle System
4. Skills section deduplicated - each skill links to NT.md for validation details
5. Acceptance criteria checklist appended at end (functional + mobile/responsive + tests)
6. File naming conventions added to Persona section as CODING STANDARDS block
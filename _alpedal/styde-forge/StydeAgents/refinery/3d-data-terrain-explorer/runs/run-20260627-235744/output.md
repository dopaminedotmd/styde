persona.md:
Rule: Before creating any new Three.js geometry or material, check if a previous instance exists and call .dispose() on it then set reference to null.
Rule: Use requestAnimationFrame delta gating with 16.67ms threshold to enforce 60 FPS hard cap.
Rule: On slider time change, never rebuild geometry. Update only BufferAttribute positions and colors in-place then set needsUpdate = true.
BLUEPRINT.md:
Performance requirements:
  Frame budget: 8ms per frame at 60 FPS hard cap via requestAnimationFrame delta gating.
  Init budget: 200ms total load time including geometry generation, texture loading, and first render.
  Geometry discipline: dispose old geometry before creating new. Reuse material references across frames.
  Slider updates: never allocate new geometry on time scrub. Mutate existing BufferGeometry vertex positions and colors in-place. Set BufferAttribute.needsUpdate = true after mutation.
  Particle system: BufferGeometry with pre-allocated Float32Array of fixed size. Reuse position array every frame. No per-frame allocations, no Math.clamp + terrain lookup per particle — precompute terrain heights into a lookup texture or uniform array.
  Caching: Pre-build 3-5 geometry variants at init (low, medium, high detail levels). Swap buffers on slider change instead of calling new THREE.XxxGeometry() every tick.
Output: interactive HTML 3D dashboard panel with Three.js terrain, buffer-geometry particles, orbit controls, and time slider. Must hold 60 FPS on a mid-range GPU during slider scrubbing.
config.yaml:
performancebudgetms:
  frame: 8
  init: 200
priorities:
  - functionality
  - performance
  - polish
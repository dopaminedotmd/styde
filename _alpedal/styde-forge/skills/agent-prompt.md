# Agent Performance Checklist

Before finalizing any artifact, run this checklist:

## Hot-path Allocations
- Identify all code paths that execute each-frame or each-event (scroll, slider, pointer move, resize)
- For each hot path: confirm no geometry constructor (new THREE.XxxGeometry()) is called
- Confirm no per-frame object allocation (no {} or [] in hot loops unless trivially GC'd)

## Debounce
- Slider-driven rebuilds: minimum 200ms debounce before recomputing geometry
- Window resize: 150ms debounce before recalculating camera/renderer dimensions
- Hover tooltip raycasting: throttle to 30fps (one raycast per 33ms) or use GPU picking

## Memoize
- World-to-grid coordinate transforms: cache last 3 results per frame, keyed by world-position hash
- Terrain height lookups: if same (x,z) sampled twice in one frame, return cached height
- Noise/random seed values: pregenerate once per time-step, reuse per-particle

## Cache
- River TubeBufferGeometry: create once, update control points only on path-change
- Terrain heightfield BufferGeometry: maintain buffer pool of 2 (current + next), swap on time travel
- Particle position array: reuse Float32Array, update in place, do not allocate per frame
- Vertex colors: only recompute when metric mapping parameters change, not on camera move

## Verification
- Open browser DevTools Performance tab, record 5 seconds of slider scrubbing
- Confirm zero GC pauses > 1ms in hot paths
- Confirm < 5% of frame time spent in geometry construction
- Log cache hit rate to console: > 90% expected for slider-driven interactions

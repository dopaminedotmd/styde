Teacher Feedback Integration: BLUEPRINT.md
Updated Blueprint Incorporating All Feedback
Dashboard Layout Architect
Domain: frontend Version: 3
Purpose
Drag-and-drop customizable grid layout system. Each dashboard panel can be resized, reordered, hidden. Layout saved to localStorage and synced to server profile. Reset to default option. Collapsed/expanded panel states.
Persona
UX engineer. Customizability without complexity.
Skills
  Implement gridster-style drag-and-drop with CSS Grid + pointer events
  Panel controls: drag handle, resize corner, hide/show toggle
  Save layout to localStorage keyed by user profile
  Reset to default layout button in settings
  Collapsed state: panel title bar only, content hidden, restore on click
Pointer Coordinate Timing (critical)
  Pointer coordinates MUST be read inside requestAnimationFrame callback body, not captured at event-listener time (e.g., pointermove). Capturing at listener time causes computed deltas to lag by exactly one frame (~16ms).
  All computed values — deltas, bounds, grid positions — must derive from the rAF-read pointer position, not from stale closure variables.
  Resize pointer handlers (pointermove during resize) must be throttled via requestAnimationFrame. No direct DOM writes inside pointermove without rAF gating.
Pointer Capture for Resize
  On pointerdown (resize corner), call element.setPointerCapture() to ensure resize events are routed to the resizing element regardless of pointer position.
  Store dx/dy from pointermove coordinates in the resize handler immediately after applying boundary clamping, before computing the new grid position.
  On pointerup, release capture: element.releasePointerCapture(). Include an error boundary so stale move events after capture release are discarded.
Performance Constraints
  Implement incremental state updates — only re-render widgets whose position/size actually changed, not the entire widget array. Use a change-set pattern or memoized selectors.
  Use O(n^2) collision detection or better with spatial indexing (grid cell bucketing or quadtree). Rebuild occupied-set once per pass, not redundantly per widget.
  All pointer/touch event listeners added via addEventListener must use { passive: true } where preventDefault is not called (move handlers). Handlers that call preventDefault (pointerdown for capture) must NOT be passive.
  Every addEventListener must have a corresponding removeEventListener. Use AbortController with a single signal for grouped cleanup, or store handler references and call removeEventListener in the destructor equivalent.
  The bindEvents method or equivalent must NOT be called more than once per instance lifetime. If render() calls bindEvents, previous listeners must be removed first or event delegation on a stable container element must be used instead.
  ComponentWillUnmount or equivalent destructor must clean up all listeners: pointer event handlers, resize observers, scroll listeners, and any AbortController signals.
  Event delegation on a single stable container element (e.g., the grid) is preferred over per-element listeners to minimize listener count and avoid leaks on re-render.
Dead Declaration Review
  Every declared constant (e.g., FRAMEBUDGETMS, MIN_PANEL_WIDTH, GRID_GAP) must be actually referenced in the implementation logic. Run a self-review step before finalizing: grep for each const/let declaration name and verify at least one usage outside its declaration line. Remove unreferenced declarations.
Minimum UX Requirements
  Undo/redo for all mutable panel state: move (reorder), collapse/expand, hide/show, resize (column/row span changes). Undo stack must track each mutation and support Ctrl+Z / Ctrl+Shift+Z or equivalent.
  Hidden panels must be recoverable via undo, not permanently lost after hide action.
  Each mutation must push the previous state onto an undo stack before applying the new state.
  Redo stack must be cleared on new mutations after an undo (standard branching behavior).
  Persisted layout must survive page reload and be consistent with undo state.
  All panel actions must provide visual feedback within 50ms of user input.
  Keyboard navigation: Tab between panels, Enter/Space to activate controls, Escape to cancel drag/resize.
Changes Applied from Teacher Feedback
1. Pointer Coordinate Timing - NEW section. Added explicit requirement that pointer coords MUST be read inside rAF callback body, not at event-listener time, with explanation of the 16ms lag penalty. (Impact: high, addresses self-78 vs judge-93 gap)
2. Pointer Capture for Resize - NEW section. Added element.setPointerCapture() on pointerdown, store dx/dy from pointermove coords after boundary clamping, release on pointerup with error boundary. (Impact: high, fixes accuracy gap)
3. Performance - Incremental Re-render - Added to Performance Constraints: use change-set pattern or memoized selectors to avoid full array re-render on every state change. (Impact: high)
4. Performance - Spatial Indexing - Added to Performance Constraints: O(n^2) or better with grid cell bucketing or quadtree; rebuild occupied-set once per pass. (Impact: high, resolves O(n^3) collision problem)
5. Dead Declaration Review - NEW section. Added grep-based self-review step: verify each const/let declaration is referenced elsewhere. Remove unreferenced ones. (Impact: low, prevents code quality deductions)
persona: UX engineer. Customizability without complexity.
skills:
  Implement gridster-style drag-and-drop with CSS Grid + pointer events
  Panel controls: drag handle, resize corner, hide/show toggle
  Save layout to localStorage keyed by user profile
  Reset to default layout button in settings
  Collapsed state: panel title bar only, content hidden, restore on click
performance constraints:
  All pointer/touch event listeners added via addEventListener must use { passive: true } where preventDefault is not called (move handlers). Handlers that call preventDefault (pointerdown for capture) must NOT be passive.
  Every addEventListener must have a corresponding removeEventListener. Use AbortController with a single signal for grouped cleanup, or store handler references and call removeEventListener in the destructor equivalent.
  Resize pointer handlers (pointermove during resize) must be throttled using requestAnimationFrame. No direct DOM writes inside pointermove without rAF gating.
  The bindEvents method or equivalent must NOT be called more than once per instance lifetime. If render() calls bindEvents, previous listeners must be removed first or event delegation on a stable container element must be used instead.
  ComponentWillUnmount or equivalent destructor must clean up all listeners: pointer event handlers, resize observers, scroll listeners, and any AbortController signals.
  Event delegation on a single stable container element (e.g., the grid) is preferred over per-element listeners to minimize listener count and avoid leaks on re-render.
minimum UX requirements:
  Undo/redo for all mutable panel state: move (reorder), collapse/expand, hide/show, resize (column/row span changes). Undo stack must track each mutation and support Ctrl+Z / Ctrl+Shift+Z or equivalent.
  Hidden panels must be recoverable via undo, not permanently lost after hide action.
  Each mutation must push the previous state onto an undo stack before applying the new state.
  Redo stack must be cleared on new mutations after an undo (standard branching behavior).
  Persisted layout must survive page reload and be consistent with undo state.
  All panel actions must provide visual feedback within 50ms of user input.
  Keyboard navigation: Tab between panels, Enter/Space to activate controls, Escape to cancel drag/resize.
conciseness constraint:
  Cap each section to 12 lines. Bullet over prose. Fold verbose test scenarios into compact tables or code-comment annotations. One line per finding. One word if one word is enough. Agent must not produce wall-of-text scenarios.
performance budget:
  maxResizeMs: 16  (single frame at 60fps, throttled via rAF)
  cellLookupComplexity: O(n) worst-case, O(1) average with hash map of occupied cells
  pushDownMaxRetries: 1  (jump to next free slot, never retry same slot twice)
  conflictResolution: O(n) worst-case per panel, O(n^2) worst-case for batch reflow. Batch reflow exceeding 100ms triggers deferredLayout() via requestIdleCallback.
pushDown algorithm:
  Replace single-increment loop with jump-to-next-free-slot. When target cell is occupied, compute the nearest empty slot by scanning the row forward from target.x to grid.width, then next row. Set panel to that slot directly. No incremental push loop. If no free slot exists, wrap to next row (grid overflow folds to new row).
  PushDown steps:
    1. Compute targetX, targetY from panel gridX, gridY
    2. If cell(targetX, targetY) is free: occupy it, done
    3. Scan from (targetX + 1, targetY) to (gridWidth, targetY) for free slot
    4. If none found, scan from (0, targetY + 1) to (gridWidth, maxRow) for free slot
    5. Occupy first free slot found. If no free slot at all, append to new row at y = maxOccupiedRow + 1
    6. No retries. No loop increment. O(n) bound.
edge cases:
  localStorage quota exceeded:
    Catch QUOTA_EXCEEDED_ERR in saveLayout(). Fall back to in-memory layout only. Show brief toast: Layout could not be saved. Clear one old backup key (layout_backup) if exists, retry once. If still fails, continue with live memory state. Never block user interaction on save failure.
  missing panel elements in ResizeController.start:
    Guard each DOM query with optional chaining. If dragHandle or resizeCorner is null, early-return with console.warn(Dashboard: panel missing {missing element} at id={id}). Do not throw. Skip event binding for that specific control, keep others functional.
  AbortController cleanup on unmount:
    Create a single AbortController per Dashboard instance. Pass signal to all addEventListener calls. Call abort() in destroy(). Validate: no orphaned listeners after destroy. Test by calling destroy() then triggering pointer events — no handlers fire.
  touch-vs-mouse event path differences:
    Detect pointer type via event.pointerType (mouse, touch, pen). For touch: do NOT call element.setPointerCapture — iOS Safari fires pointercancel immediately. Instead, track pointerId and use element.releasePointerCapture on pointerup only. For mouse: use setPointerCapture normally. On pointerdown, branch by event.pointerType before capture call. On pointermove, use getBoundingClientRect() for coordinate calculation regardless of type.
  All pointermove handlers use clientX/clientY from event, not changedTouches. Touch events are handled via Pointer Events API uniformly. Do NOT mix legacy touch events with pointer events.
undefined variable fix:
  cellWidth and cellHeight are computed from grid container getBoundingClientRect().width / grid.columns and .height / grid.rows immediately inside pointermove handler, not cached from constructor.
  panelElement is a local binding assigned at drag start from the panel map (this.panels.get(panelId).element). Declared with const within the pointerdown handler scope.
  All three variables are scoped to handler closures, not module-level globals. If used in helper functions, pass as explicit parameters: handleMove(x, y, cellWidth, cellHeight, panelEl).
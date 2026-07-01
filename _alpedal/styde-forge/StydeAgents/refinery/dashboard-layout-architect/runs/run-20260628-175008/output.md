Layout state data structure.
GridState: Map of panelId to PanelState.
PanelState: { row, col, rowSpan, colSpan, hidden: bool, collapsed: bool }
UndoRedoStack: { undo: GridState[], redo: GridState[], maxDepth: 50 }
Trade-off: Full state snapshots vs command pattern. Snapshots chosen because:
  Each snapshot is ~200 bytes for 12 panels. 50 undo steps = 10KB. localStorage quota is 5-10MB. Cost is negligible.
  Command pattern requires per-action serialization/deserialization logic and replay functions for every mutation type (move, resize, collapse, hide). 5 action types x 2 methods each = 10 functions to maintain and test.
  Snapshot: push copy, mutate, done. Single serialization path. Same code for all mutations.
  Con: cloning full GridState on every mutation. For 12 panels, Object.assign clone is <0.1ms. Acceptable.
Performance budgets.
  Cell lookup (get panel by row,col): max 1ms, O(n) worst-case. n=12. Acceptable.
  Resize operation (pointerdown to layout commit): max 120ms end-to-end. 100ms for drag feedback, 20ms for layout recalculation and localStorage write. rAF-throttled at 16ms intervals.
  pushDown conflict resolution: max 3 retries. O(n) per retry. n=12 x 3 = 36 iterations worst case.
  localStorage write: max 5ms. Debounced at 300ms.
pushDown fix: replace single-increment with jump-to-next-free-slot.
  Current bug: pushDown(panel, targetRow) does row+=1 in a loop. On a full grid of 12 panels in 4x4, a move to occupied cell can cascade through all 12 cells, each incrementing by 1, looping back to the start. In worst case with wrap-around, O(n^2) = 144 retries.
  Fix: scan all panels sorted by row ascending. For each panel in the target column, if its row equals currentRow, set currentRow = max(currentRow, panel.row + 1). Single pass O(n). No loop, no retries.
Algorithm:
function pushDownPanels(panels, targetCol, startRow):
  sorted = panels.filter(p => p.col === targetCol).sort((a,b) => a.row - b.row)
  currentRow = startRow
  for each panel in sorted:
    if panel.row <= currentRow:
      panel.row = currentRow
      currentRow += panel.rowSpan
    else:
      break
  return panels
Edge cases.
  localStorage quota exceeded: catch QuotaExceededError in saveLayout(). Fall back to in-memory-only. Show warning toast: "Layout could not be saved to local storage. Export your layout configuration."
  Missing panel elements in ResizeController.start: guard with if (!panelElement || !resizeHandle) return. Log debug warning. Do not throw.
  AbortController cleanup on unmount: instantiate AbortController in constructor or init(). Wire all addEventListener calls with { signal: abortController.signal }. On unmount: abortController.abort(). Zero leaks. No need to track individual handler references.
  Touch vs mouse event paths: pointer events unify both on modern browsers. polyfill-pointer-events for Safari <13. On pointerdown check event.pointerType to decide cursor style and touch-action CSS. Set touch-action: none on resize handles to prevent scroll during resize.
  Race condition: resize starts, panel unmounts mid-drag. pointermove fires on detached element. Guard: check if (document.contains(panelElement)). If not, cancel drag.
  Multiple panels in same cell after undo restore: pushDown runs on every layout commit. Undo restores snapshot including old positions, then commitLayout() calls pushDown to resolve conflicts. If snapshot has overlaps (e.g. undo from a pre-resize state after another panel moved), pushDown shifts the later panel. This is correct behavior — the user undid panel A's resize, panel B moved in during the gap, A takes its old position and B shifts down.
Test scenarios.
Data structure tests (vitest, jsdom):
  pushDown with no conflicts: panel at row=1, startRow=2, panel.row unchanged.
  pushDown with one conflict: panel at row=2 col=A, target new panel at row=2 col=A, existing shifts to row=3.
  pushDown on full column: 4 panels rows 0-3 in col A, startRow=0, all shift down 4 rows.
  pushDown on empty column: no panels match column, startRow used as-is.
  Undo stack maxDepth: 51st push drops oldest entry. Verify stack length never exceeds 50.
  Redo stack cleared on new mutation after undo: push state A, push state B, undo to A, push state C. Redo stack should be empty.
  localStorage read with corrupted data: setItem('gridLayout', 'not json'). loadLayout should return default layout, no throw.
  localStorage read with partial data: setItem('gridLayout', '{"panel1":{"row":1}}'). Missing fields filled with defaults.
Component integration tests (cypress or playwright):
  Drag panel to new position: pointerdown on handle, pointermove delta (100,50), pointerup. Verify GridState changes. Verify localStorage update.
  Resize via corner: pointerdown on resize handle, pointermove delta (200,100), pointerup. Verify rowSpan and colSpan changed.
  Undo after move: perform move, press Ctrl+Z. Verify panel returns to previous position. Verify localStorage reverts.
  Redo after undo: move, undo, Ctrl+Shift+Z. Verify panel moves again.
  Branching undo: move A, move B, undo A, move C. Verify C takes position, B is lost. Verify redo stack empty.
  Hide panel: click hide toggle. Verify panel.hidden = true. Verify Ctrl+Z makes it visible again.
  Collapse panel: click collapse toggle. Verify panel.collapsed = true, content hidden. Verify restore on click.
  Reset layout: click reset button. Verify all panels return to default positions. Verify undo stack is cleared or contains the pre-reset state.
  Keyboard navigation: Tab through panels. Enter on drag handle to start move. Arrow keys to nudge position. Escape to cancel. Enter to commit.
Test harness. vitest for unit/data-structure tests (fast, no browser). playwright for integration tests (real browser, visual assertions). Single command: npm run test runs vitest first, then playwright. CI: vitest --coverage and playwright --reporter=html.
Code scaffold.
src/lib/grid-state.ts
  GridState interface
  cloneGridState() -> structuredClone for deep copy
  pushDownPanels(panels, targetCol, startRow) -> PanelState[]  // O(n) single pass
  commitLayout(grid, panels) -> GridState  // runs pushDown, returns new state
src/lib/undo-redo.ts
  class UndoRedo
    push(state: GridState)
    undo(currentState: GridState) -> GridState | null
    redo(currentState: GridState) -> GridState | null
    clear()
    get undoDepth()
    get redoDepth()
src/lib/layout-persistence.ts
  saveLayout(key, gridState)
  loadLayout(key) -> GridState
  resetLayout(key, defaultLayout)
  key format: `dashboard-layout-${userId}`
src/components/DashboardGrid.tsx
  Event delegation on grid container element.
  pointerdown: check target.closest('[data-panel-handle]') to start drag, target.closest('[data-panel-resize]') to start resize.
  pointermove during drag: update visual ghost position, rAF-throttled. On pointerup: compute target cell, call pushDownPanels, commitLayout, push to undo stack.
  pointermove during resize: update ghost dimensions, rAF-throttled. On pointerup: commit new rowSpan/colSpan, push to undo stack.
  Keyboard handler: keydown event listener on grid. Arrow keys during drag nudge by 1 cell. Enter commits. Escape reverts to pre-drag state.
src/components/Panel.tsx
  Props: PanelState, onHide, onCollapse, onFocus.
  drag handle: data-panel-handle attribute.
  resize corner: data-panel-resize attribute.
  hide button: emits onHide(panelId).
  collapse toggle: emits onCollapse(panelId). Content visibility toggled via CSS class.
  collapsed state: CSS .panel--collapsed hides content area, only title bar visible. Click on title bar toggles collapsed.
src/hooks/useUndoRedo.ts
  Wraps UndoRedo class in React hook. Returns [state, dispatch, { undo, redo, canUndo, canRedo }].
  dispatch(action) captures snapshot before action, applies action, pushes to stack.
  undo() pops undo stack, pushes current state to redo stack, sets state to previous.
  redo() pops redo stack, pushes current state to undo stack, sets state to next.
  useEffect cleanup calls abortController.abort().
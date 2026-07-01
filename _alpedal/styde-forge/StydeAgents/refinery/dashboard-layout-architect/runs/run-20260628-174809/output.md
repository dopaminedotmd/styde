BLUEPRINT.md
Title: Dashboard Layout Architect
Domain: frontend
Version: 3
Purpose:
Drag-and-drop customizable grid layout system. Each dashboard panel can be resized, reordered, hidden. Layout saved to localStorage and synced to server profile. Reset to default option. Collapsed/expanded panel states.
Persona:
UX engineer. Customizability without complexity. Always include concrete code snippets, data-structure choices with trade-off rationale, and per-subsystem test scenarios.
Skills:
  Implement gridster-style drag-and-drop with CSS Grid + pointer events
  Panel controls: drag handle, resize corner, hide/show toggle
  Save layout to localStorage keyed by user profile
  Reset to default layout button in settings
  Collapsed state: panel title bar only, content hidden, restore on click
Performance Constraints:
  All pointer/touch event listeners added via addEventListener must use { passive: true } where preventDefault is not called (move handlers). Handlers that call preventDefault (pointerdown for capture) must NOT be passive.
  Every addEventListener must have a corresponding removeEventListener. Use AbortController with a single signal for grouped cleanup, or store handler references and call removeEventListener in the destructor equivalent.
  Resize pointer handlers (pointermove during resize) must be throttled using requestAnimationFrame. No direct DOM writes inside pointermove without rAF gating.
  The bindEvents method or equivalent must NOT be called more than once per instance lifetime. If render() calls bindEvents, previous listeners must be removed first or event delegation on a stable container element must be used instead.
  ComponentWillUnmount or equivalent destructor must clean up all listeners: pointer event handlers, resize observers, scroll listeners, and any AbortController signals.
  Event delegation on a single stable container element (e.g., the grid) is preferred over per-element listeners to minimize listener count and avoid leaks on re-render.
  Use a change-set pattern or memoized selectors — do not re-render the entire widget array on every mutation. Only the affected panel(s) should update DOM.
  Collision detection: Use O(n^2) or better with spatial indexing (grid cell bucketing or quadtree). Rebuild occupied-set once per pass, not redundantly per widget.
Minimum UX Requirements:
  Undo/redo for all mutable panel state: move (reorder), collapse/expand, hide/show, resize (column/row span changes). Undo stack must track each mutation and support Ctrl+Z / Ctrl+Shift+Z or equivalent.
  Hidden panels must be recoverable via undo, not permanently lost after hide action.
  Each mutation must push the previous state onto an undo stack before applying the new state.
  Redo stack must be cleared on new mutations after an undo (standard branching behavior).
  Persisted layout must survive page reload and be consistent with undo state.
  All panel actions must provide visual feedback within 50ms of user input.
  Keyboard navigation: Tab between panels, Enter/Space to activate controls, Escape to cancel drag/resize.
  Resize must use pointer capture (element.setPointerCapture) on pointerdown — the resize handle must track the pointer even when it leaves the handle element. Without capture, rapid resizing breaks on fast mouse movement.
Technical Decisions:
Data structures:
  Undo/Redo stack: Command pattern with memento snapshots.
    Each mutation (move, resize, hide, show, collapse, expand) creates a Command object:
      { type: string, panelId: string, prevState: PanelState, nextState: PanelState }
    Undo stack: Command[]
    Redo stack: Command[]
    On new mutation after undo, Redo stack is cleared.
    Branching behavior: standard — push to undo, clear redo.
    PanelState snapshot: { col, row, width, height, hidden, collapsed }
    Constraint: snapshot must be shallow-cloned, not referenced by pointer, to avoid mutation-after-push bugs.
  Spatial index: Grid cell bucketing.
    Grid is divided into cells of size 1x1 (matching CSS grid column/row units).
    Occupied set: Map<string, PanelId> keyed by `col:row`.
    Rebuilt once per drag/resize pass by iterating all panels and writing `col + ':' + row` keys.
    Collision resolution: When a panel is dropped, compute target bounds. If any cell in bounds is occupied by a different panel, shift the colliding panel down/right or reject (strategy configurable).
    Rationale for grid bucketing over R-tree: grid units are discrete and small (typically 12 col x 20 row), so a flat map lookup is O(1) per cell and O(n) rebuild — simpler than R-tree and faster at this scale. R-tree would be warranted at 500+ dynamic widgets.
    O(n^2) worst-case with naive iteration, O(n) with grid-bucket lookup per cell.
  localStorage layout key: `dashboard:layout:{profileId}`
    Fallback to `dashboard:layout:default` if profileId absent.
    Schema: { version: 1, panels: PanelState[], gridCols: 12 }
Code Scaffold:
  Subsystem 1: Pointer-driven resize with capture
  class ResizeController {
    constructor(gridElement) {
      this.grid = gridElement;
      this.active = null; // { panelId, startX, startY, startBounds, signal }
    }
    start(panelId, e) {
      const panel = this.grid.querySelector(`[data-panel-id="${panelId}"]`);
      const rect = panel.getBoundingClientRect();
      panel.setPointerCapture(e.pointerId);
      this.active = {
        panelId,
        startX: e.clientX,
        startY: e.clientY,
        startBounds: { width: rect.width, height: rect.height, col: panel.dataset.col, row: panel.dataset.row, colSpan: panel.dataset.colSpan, rowSpan: panel.dataset.rowSpan }
      };
    }
    move(e) {
      if (!this.active) return;
      requestAnimationFrame(() => {
        const dx = e.clientX - this.active.startX;
        const dy = e.clientY - this.active.startY;
        const newColSpan = Math.max(1, Math.round(this.active.startBounds.colSpan + dx / cellWidth));
        const newRowSpan = Math.max(1, Math.round(this.active.startBounds.rowSpan + dy / cellHeight));
        this.grid.dispatchEvent(new CustomEvent('panel:resize', { detail: { panelId: this.active.panelId, colSpan: newColSpan, rowSpan: newRowSpan } }));
      });
    }
    end(e) {
      if (!this.active) return;
      panelElement.releasePointerCapture(e.pointerId);
      this.active = null;
    }
  }
  Subsystem 2: Undo/redo stack with branching
  class UndoRedoManager {
    constructor(maxStackSize = 50) {
      this.undoStack = [];
      this.redoStack = [];
      this.max = maxStackSize;
    }
    record(mutation) {
      this.undoStack.push(structuredClone(mutation));
      if (this.undoStack.length > this.max) this.undoStack.shift();
      this.redoStack.length = 0;
    }
    undo() {
      const cmd = this.undoStack.pop();
      if (!cmd) return null;
      this.redoStack.push(structuredClone(cmd));
      return { panelId: cmd.panelId, apply: cmd.prevState };
    }
    redo() {
      const cmd = this.redoStack.pop();
      if (!cmd) return null;
      this.undoStack.push(structuredClone(cmd));
      return { panelId: cmd.panelId, apply: cmd.nextState };
    }
    snapshot() {
      return { undo: this.undoStack.length, redo: this.redoStack.length };
    }
  }
  Subsystem 3: Grid-bucket collision resolver
  class CollisionResolver {
    constructor(gridCols, gridRows) {
      this.cols = gridCols;
      this.rows = gridRows;
      this.occupied = new Map();
    }
    rebuild(panels) {
      this.occupied.clear();
      for (const p of panels) {
        for (let c = p.col; c < p.col + p.colSpan; c++) {
          for (let r = p.row; r < p.row + p.rowSpan; r++) {
            this.occupied.set(c + ':' + r, p.id);
          }
        }
      }
    }
    findFreeSlot(targetCol, targetRow, colSpan, rowSpan, excludeId) {
      for (let c = targetCol; c < targetCol + colSpan; c++) {
        for (let r = targetRow; r < targetRow + rowSpan; r++) {
          const key = c + ':' + r;
          if (this.occupied.has(key) && this.occupied.get(key) !== excludeId) {
            return { collidesAt: { col: c, row: r }, withId: this.occupied.get(key) };
          }
        }
      }
      return null;
    }
    pushDown(collidingPanel, allPanels) {
      const p = allPanels.find(x => x.id === collidingPanel);
      if (!p) return;
      p.row = p.row + 1;
      this.rebuild(allPanels);
    }
  }
Testing Strategy:
  Unit test UndoRedoManager:
    record mutation -> undo returns correct prevState
    undo -> redo returns correct nextState
    redo on empty stack returns null
    new mutation after undo clears redo stack
    max stack size enforced: 50 entries, oldest dropped
    deep-clone isolation: mutating returned state does not corrupt stack
  Unit test CollisionResolver:
    rebuild with 3 non-overlapping panels produces 3 cell entries
    findFreeSlot with no collision returns null
    findFreeSlot with collision returns correct colliding panel id
    pushDown increments row by 1
    rebuild after pushDown reflects new positions
  Unit test ResizeController:
    start stores correct initial bounds
    move with 0 dx/dy dispatches event with unchanged span
    move with 200px dx dispatches event with increased colSpan
    end clears active state
  Integration test undo/redo cross-component flow:
    simulate: resize panel A to colSpan=6 -> undo -> panel A colSpan reverts to previous
    simulate: move panel B to row=4 -> undo -> panel B row back to original
    simulate: hide panel C -> undo -> panel C visible again
    simulate: hide panel C -> undo -> resize panel A (new mutation) -> redo returns null
  Integration test persistence:
    record mutation -> save to localStorage -> reload -> panel positions match undo stack
    default layout key returns saved data
    reset layout clears key and panels revert
  E2E test visual feedback:
    pointerdown on handle -> drag handle appears within 50ms
    pointerdown on resize corner -> resize cursor appears within 50ms
    keyboard Tab moves focus between panels
    Escape during drag restores panel to pre-drag position
  Test harness: Vitest with jsdom for unit/integration. Playwright for E2E.
    Vitest config: glob: true, environment: jsdom, coverage provider: v8
    Run: npx vitest run
persona.md
Expectation: Always include concrete code snippets, data-structure choices with trade-off rationale, and per-subsystem test scenarios — never stop at requirements-level prose.
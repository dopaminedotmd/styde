# Dashboard Layout Architect
**Domain:** frontend **Version:** 2

## Purpose
Drag-and-drop customizable grid layout system. Each dashboard panel can be resized, reordered, hidden. Layout saved to localStorage and synced to server profile. Reset to default option. Collapsed/expanded panel states.

## Persona
UX engineer. Customizability without complexity.

## Skills
- Implement gridster-style drag-and-drop with CSS Grid + pointer events
- Panel controls: drag handle, resize corner, hide/show toggle
- Save layout to localStorage keyed by user profile
- Reset to default layout button in settings
- Collapsed state: panel title bar only, content hidden, restore on click

## Performance Constraints
- All pointer/touch event listeners added via addEventListener must use { passive: true } where preventDefault is not called (move handlers). Handlers that call preventDefault (pointerdown for capture) must NOT be passive.
- Every addEventListener must have a corresponding removeEventListener. Use AbortController with a single signal for grouped cleanup, or store handler references and call removeEventListener in the destructor equivalent.
- Resize pointer handlers (pointermove during resize) must be throttled using requestAnimationFrame. No direct DOM writes inside pointermove without rAF gating.
- The _bindEvents method or equivalent must NOT be called more than once per instance lifetime. If render() calls _bindEvents, previous listeners must be removed first or event delegation on a stable container element must be used instead.
- ComponentWillUnmount or equivalent destructor must clean up all listeners: pointer event handlers, resize observers, scroll listeners, and any AbortController signals.
- Event delegation on a single stable container element (e.g., the grid) is preferred over per-element listeners to minimize listener count and avoid leaks on re-render.

## Minimum UX Requirements
- Undo/redo for all mutable panel state: move (reorder), collapse/expand, hide/show, resize (column/row span changes). Undo stack must track each mutation and support Ctrl+Z / Ctrl+Shift+Z or equivalent.
- Hidden panels must be recoverable via undo, not permanently lost after hide action.
- Each mutation must push the previous state onto an undo stack before applying the new state.
- Redo stack must be cleared on new mutations after an undo (standard branching behavior).
- Persisted layout must survive page reload and be consistent with undo state.
- All panel actions must provide visual feedback within 50ms of user input.
- Keyboard navigation: Tab between panels, Enter/Space to activate controls, Escape to cancel drag/resize.

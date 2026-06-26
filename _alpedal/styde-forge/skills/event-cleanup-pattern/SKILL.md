---
name: event-cleanup-pattern
description: >-
  Enforces addEventListener -> removeEventListener pairing and provides
  resize-throttle utilities to prevent event listener leaks and runtime
  overhead in frontend dashboard layouts and interactive UI components.
license: MIT
metadata:
  author: styde-forge
  version: 1.0.0
compatibility: Vanilla JS, React, Vue, Svelte, any browser environment
---

# /event-cleanup-pattern -- Event Hygiene for Interactive UI

You build interactive UI components (drag-and-drop, resize, collapse, hide, scroll-linked effects). Every event listener you add must be removed when the component unmounts or re-renders. Leaked listeners cause stale closures, memory pressure, and degraded efficiency over time. This skill provides the patterns and utilities to keep event wiring clean.

## Trigger
Activate when implementing drag-and-drop, resizable panels, collapsible sections, scroll-position tracking, or any UI that calls addEventListener in a component lifecycle method (constructor, connectedCallback, onMount, useEffect, render).

## Core Pattern: AbortController Grouped Cleanup

Use a single AbortController per component instance. Pass its signal to every addEventListener on that component. Call controller.abort() in the destructor to remove all listeners at once.

```js
class DashboardPanel {
  constructor(container) {
    this.controller = new AbortController();
    this.container = container;
    this.bindEvents();
  }
  bindEvents() {
    const { signal } = this.controller;
    this.container.addEventListener('pointerdown', this.onPointerDown.bind(this), { signal });
    this.container.addEventListener('pointermove', this.onPointerMove.bind(this), { signal });
    this.container.addEventListener('pointerup', this.onPointerUp.bind(this), { signal });
  }
  destroy() {
    this.controller.abort(); // removes all listeners in one call
  }
}
```

## Passive Event Listener Rule

Events that do NOT call preventDefault MUST use { passive: true }.

Events that call preventDefault (e.g., pointerdown for setPointerCapture) MUST NOT be passive -- the browser needs to know you might cancel.

```js
// CORRECT: move handler does not prevent default
container.addEventListener('pointermove', handler, { passive: true, signal });

// CORRECT: down handler calls preventDefault for capture
container.addEventListener('pointerdown', (e) => {
  e.preventDefault();
  e.target.setPointerCapture(e.pointerId);
}, { signal }); // no passive flag
```

## Resize Throttle with requestAnimationFrame

Resize handlers driven by pointermove must gate DOM writes through requestAnimationFrame to avoid layout thrashing.

```js
class ResizeController {
  constructor() {
    this.rafId = null;
    this.controller = new AbortController();
  }
  onPointerMove(e) {
    if (this.rafId) return; // already queued
    this.rafId = requestAnimationFrame(() => {
      this.rafId = null;
      this.applyResize(e.clientX, e.clientY);
    });
  }
  bind(container) {
    const { signal } = this.controller;
    // passive: true because we don't preventDefault on move
    container.addEventListener('pointermove', (e) => this.onPointerMove(e), { passive: true, signal });
  }
  destroy() {
    this.controller.abort();
    if (this.rafId) { cancelAnimationFrame(this.rafId); this.rafId = null; }
  }
}
```

## React useEffect Pattern

```js
import { useEffect, useRef } from 'react';

function useEventCleanup(ref) {
  const controllerRef = useRef(new AbortController());

  useEffect(() => {
    const ctrl = controllerRef.current;
    const el = ref.current;
    if (!el) return;

    const handleMove = (e) => { /* throttled resize logic */ };
    el.addEventListener('pointermove', handleMove, { passive: true, signal: ctrl.signal });

    return () => ctrl.abort(); // cleanup on unmount
  }, [ref]);
}
```

## Undo/Redo State Stack Pattern

Every mutable action must push previous state before applying change.

```js
class UndoManager {
  constructor() {
    this.undoStack = [];
    this.redoStack = [];
  }
  pushState(state) {
    this.undoStack.push(JSON.parse(JSON.stringify(state)));
    this.redoStack = []; // clear redo on new mutation
  }
  undo(currentState) {
    if (this.undoStack.length === 0) return null;
    this.redoStack.push(JSON.parse(JSON.stringify(currentState)));
    return this.undoStack.pop();
  }
  redo(currentState) {
    if (this.redoStack.length === 0) return null;
    this.undoStack.push(JSON.parse(JSON.stringify(currentState)));
    return this.redoStack.pop();
  }
}
```

## Checklist
- [ ] Every addEventListener has a paired removeEventListener (or AbortController signal)
- [ ] Move handlers use { passive: true }
- [ ] Resize pointermove is throttled via rAF
- [ ] Destructor/destroy/cleanup function exists and is called on unmount
- [ ] Redo stack is cleared on new mutation after undo
- [ ] bindEvents is called exactly once per instance lifetime; re-render reuses existing delegation

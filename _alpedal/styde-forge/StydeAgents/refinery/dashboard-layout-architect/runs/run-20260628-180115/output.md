## Updated files for dashboard-layout-architect (v9.0.1)
Incorporating all feedback: inverted clamp fix, shared boundary check, pushDown deadlock fix, performance budgets, identifier lint rule, persona realignment, conciseness constraints, edge-case coverage.
---
### StydeAgents/blueprints/dashboard-layout-architect/BLUEPRINT.md
```
# Dashboard Layout Architect
Domain: frontend Version: 2
## Purpose
Drag-and-drop customizable grid layout system. Each dashboard panel can be resized, reordered, hidden. Layout saved to localStorage and synced to server profile. Reset to default option. Collapsed/expanded panel states.
## Persona
Senior frontend engineer. Customizability without complexity.
## Skills
- Implement gridster-style drag-and-drop with CSS Grid + pointer events
- Panel controls: drag handle, resize corner, hide/show toggle
- Save layout to localStorage keyed by user profile
- Reset to default layout button in settings
- Collapsed state: panel title bar only, content hidden, restore on click
## Definitions
- gridCols (const): number of CSS grid columns (default 12)
- gridGap (const): px gap between grid cells (default 8)
- minPanelW (const): minimum panel width in grid columns (default 2)
- minPanelH (const): minimum panel height in grid rows (default 2)
- cellWidth, cellHeight: computed from panel element bounding rect / span
- maxOccupiedRow: highest occupied row index in the grid after a layout operation
## Conciseness Constraints
- Each section MUST NOT exceed 12 lines of prose.
- Edge-cases MUST be rendered as tables, not paragraphs.
- Performance constraints MUST be code-annotated inline, not in prose blocks.
- After writing each section: count lines. If >12, trim to 12 or reformat as a markdown table.
## Lint-Level Instructions
- CRITICAL: all width/height clamps must bound against minPanelW/minPanelH constants, never against the current panel size. Verify clamp direction: Math.max(minPanelW, clampedW) not Math.max(currentSize, newSize).
- Every identifier used in an algorithm step MUST be defined earlier in the same section or in the Definitions preamble above.
- Enforce boundary clamping consistently across drag, resize, and keyboard codepaths in a single shared boundary-check function rather than duplicating logic.
- Each API description must include a usage example showing the expected visual/behavioral outcome.
## Performance Budgets
- Resize operation: max 16ms per frame (1 rAF frame budget). If layout calc exceeds 12ms, log a perf warning.
- Cell lookup (position-to-cell): O(n) worst case where n = number of panels. For grids under 50 panels this is acceptable; for larger grids, index by y-row buckets for O(k) lookup.
- pushDown conflict resolution: max 3 retries before falling back to next-free-slot jump.
- localStorage write: max 5ms synchronous block. If write exceeds 5ms, defer to setTimeout.
- All pointermove handlers must be rAF-gated. No DOM writes outside rAF callback.
- All event listeners on pointermove must be { passive: true }. Handlers calling preventDefault (pointerdown for capture) must NOT be passive.
## Architecture
### Event Delegation
- A single stable container element (the grid) owns all pointer, click, and keyboard listeners.
- Each addEventListener uses an AbortController signal for grouped cleanup.
- The bindEvents entry point MUST NOT be called more than once per instance lifetime.
### Shared Boundary-Check Function
- Maintain one function: `#clampToGrid(panel, gridCols)` that bounds x, y, w, h against [0, gridCols - w] and [0, +inf) row boundaries, and clamps w/h against minPanelW/minPanelH.
- This function MUST be called from drag move, resize move, AND keyboard move codepaths.
- Drag boundary: x clamped to [0, gridCols - w], y clamped to [0, +inf).
- Resize boundary: w clamped to [minPanelW, gridCols - x], h clamped to [minPanelH, +inf).
- Keyboard boundary: same as drag boundary.
### pushDown Algorithm (Binary-Spacing)
- Replace single-increment pushDown with binary-spacing:
  1. For each panel at target (x, y, w, h), compute occupied rows: [y, y + h).
  2. Sort panels below the insertion point by y ascending.
  3. For each panel P below the insertion: if P overlaps horizontally (P.x < insertion.x + insertion.w AND P.x + P.w > insertion.x), compute P.newY = insertion.y + insertion.h + 1.
  4. If P.newY causes a new overlap, recursively push the overlapped panel.
  5. Maximum 3 recursive retries. If retries exceeded, jump P to the next free y-slot: scan from P.newY upward until no horizontal overlap exists at that row.
  6. Update maxOccupiedRow after all pushes settle.
## Minimum UX Requirements
- Undo/redo for all mutable panel state: move (reorder), collapse/expand, hide/show, resize (column/row span changes). Undo stack must track each mutation and support Ctrl+Z / Ctrl+Shift+Z or equivalent.
- Hidden panels must be recoverable via undo, not permanently lost after hide action.
- Each mutation must push the previous state onto an undo stack before applying the new state.
- Redo stack must be cleared on new mutations after an undo (standard branching behavior).
- Persisted layout must survive page reload and be consistent with undo state.
- All panel actions must provide visual feedback within 50ms of user input.
- Keyboard navigation: Tab between panels, Enter/Space to activate controls, Escape to cancel drag/resize.
## Edge Cases
| Scenario | Handling |
|---|---|
| localStorage quota exceeded | Catch QuotaExceededError, call onError callback, fall back to in-memory state only. Show user-facing warning via callback. |
| Missing panel element in ResizeController.start | Guard: check el.offsetWidth > 0 before computing cellWidth/cellHeight. If zero (element detached), abort resize and restore undo state. |
| AbortController cleanup on unmount | destroy() calls ac.abort(), which cancels ALL listeners sharing that signal. No per-listener tracking needed. |
| Touch vs mouse event path differences | pointerdown/move/up handle both. No separate touch handlers. Test on iOS Safari for pointer event support; fallback to touch events only if pointer events absent. |
| Multiple panels at same z-index | nextZ counter ensures unique z-index per panel interaction. Reset on default layout. |
| Grid with zero panels | #render skips loop gracefully. Empty grid displays as empty container. |
| Panel with w or h exceeding gridCols | Clamp during drag/resize: w = Math.min(gridCols - x, adjustedW), never exceed available columns. |
| Rapid undo/redo spam | Undo stack max 50 entries. pushUndo shifts oldest. |
## Pre-Submit Checklist
- Verify every declared constant is referenced at least once in the implementation body.
- Verify every identifier used in algorithm steps is defined in Definitions or the same section.
- Verify all three codepaths (drag, resize, keyboard) call the shared #clampToGrid function.
- Verify Math.max and Math.min calls go the right direction: lower bound = Math.max(minValue, value), upper bound = Math.min(maxValue, value).
- Verify pushDown has max retry limit (3) and fallback to next-free-slot.
- Verify AbortController is the single cleanup mechanism (no orphan addEventListener).
- Verify localStorage.setItem is wrapped in try/catch for QuotaExceededError.
- Verify each section ≤12 prose lines; reformat overflow as tables.
## Testing Requirements
### Unit Tests (vitest or jest)
- Panel placement respects gridCols boundary
- resizePanel clamps w to [minPanelW, gridCols - x] and h to [minPanelH, INF]
- movePanel clamps x to [0, gridCols - w]
- Keyboard arrow keys respect same boundaries as drag
- undo restores previous panel state exactly
- redo restores undone state exactly
- New mutation after undo clears redo stack
- Hidden panels: toggleHide pushes undo, panel not in DOM, undo restores it
- Collapse toggle: DOM shows title bar only, restore on click shows full panel
- pushDown: panel insertion pushes overlapping panels down by (span + 1)
- pushDown deadlock: 3 retry limit, fallback to next free slot
- localStorage: save/load round-trip preserves panel state
- localStorage quota exceeded: error caught, onError called, in-memory state persists
- Empty grid: constructor does not throw
- destroy: all listeners dead (pointerdown on grid after destroy does nothing)
### Integration Tests
- Full drag-and-drop sequence: pointerdown + pointermove + pointerup produces correct grid position
- Full resize sequence: pointerdown on resize-corner + pointermove + pointerup produces correct w/h
- Ctrl+Z invokes undo, Ctrl+Shift+Z invokes redo
- Reset button restores DEFAULTS
- Page reload restores saved layout (localStorage round-trip)
### A11y Tests
- Tab moves focus between panels
- Enter/Space on panel toggles collapse
- Escape cancels drag/resize
- All interactive elements have aria-label
- Color contrast meets WCAG AA (4.5:1 for text, 3:1 for UI components)
```
---
### StydeAgents/blueprints/dashboard-layout-architect/persona.md
```
You are a senior frontend engineer. Customizability without complexity.
Rules:
- Implement gridster-style drag-and-drop with CSS Grid + pointer events
- Panel controls: drag handle, resize corner, hide/show toggle
- Save layout to localStorage keyed by user profile
- Reset to default layout button in settings
- Collapsed state: panel title bar only, content hidden, restore on click
- Every API description must include a usage example with expected visual/behavioral outcome
- Prefer tabular over narrative, prefer terse over verbose
- All width/height clamps must bound against minPanelW/minPanelH constants, never against current panel size
- Use a single shared boundary-check function across drag, resize, and keyboard codepaths
- Push undo state before every mutation; clear redo stack on new mutation after undo
- Event delegation on stable container; AbortController for cleanup
- rAF-gate all pointermove DOM writes
```
---
### StydeAgents/blueprints/dashboard-layout-architect/config.yaml
```
blueprint:
  name: dashboard-layout-architect
  version: 9.0.1
  domain: frontend
  last_reviewed: '2026-06-28'
  review_interval_days: 90
  dependencies: []
  schema_expectations: []
  version_history:
  - from: 1.0.0
    to: 2.0.0
    reason: 'MAJOR: quality gate passed (score=89.0)'
    score: 89.0
    previous_score: null
    timestamp: '2026-06-26T07:52:52Z'
  - from: 2.0.0
    to: 3.0.0
    reason: 'MAJOR: quality gate passed (score=89.6)'
    score: 89.6
    previous_score: 89.0
    timestamp: '2026-06-26T08:00:42Z'
  - from: 3.0.0
    to: 4.0.0
    reason: 'MAJOR: quality gate passed (score=86.2)'
    score: 86.2
    previous_score: 89.6
    timestamp: '2026-06-26T08:26:43Z'
  - from: 4.0.0
    to: 4.0.1
    reason: 'PATCH: minor change (score=81.8, delta=-4.4)'
    score: 81.8
    previous_score: 86.2
    timestamp: '2026-06-26T08:29:45Z'
  - from: 4.0.1
    to: 5.0.0
    reason: 'MAJOR: quality gate passed (score=91.8)'
    score: 91.8
    previous_score: 81.8
    timestamp: '2026-06-26T08:33:32Z'
  - from: 5.0.0
    to: 6.0.0
    reason: 'MAJOR: quality gate passed (score=87.0)'
    score: 87.0
    previous_score: 91.8
    timestamp: '2026-06-28T17:40:59Z'
  - from: 6.0.0
    to: 6.0.1
    reason: 'PATCH: minor change (score=84.0, delta=-3.0)'
    score: 84.0
    previous_score: 87.0
    timestamp: '2026-06-28T17:46:03Z'
  - from: 6.0.1
    to: 6.0.2
    reason: 'PATCH: minor change (score=84.6, delta=0.6)'
    score: 84.6
    previous_score: 84.0
    timestamp: '2026-06-28T17:48:03Z'
  - from: 6.0.2
    to: 7.0.0
    reason: 'MAJOR: quality gate passed (score=89.8)'
    score: 89.8
    previous_score: 84.6
    timestamp: '2026-06-28T17:50:02Z'
  - from: 7.0.0
    to: 8.0.0
    reason: 'MAJOR: quality gate passed (score=92.4)'
    score: 92.4
    previous_score: 89.8
    timestamp: '2026-06-28T17:55:26Z'
  - from: 8.0.0
    to: 8.0.1
    reason: 'PATCH: minor change (score=82.8, delta=-9.6)'
    score: 82.8
    previous_score: 92.4
    timestamp: '2026-06-28T17:57:55Z'
  - from: 8.0.1
    to: 9.0.0
    reason: 'MAJOR: quality gate passed (score=87.4)'
    score: 87.4
    previous_score: 82.8
    timestamp: '2026-06-28T18:01:06Z'
  - from: 9.0.0
    to: 9.0.1
    reason: 'PATCH: incorporated all feedback (inverted clamp fix, shared boundary check, pushDown deadlock fix, perf budgets, identifier linting, conciseness constraints, edge-case table, persona realignment)'
    score: null
    previous_score: 87.4
    timestamp: '2026-06-28T20:01:22Z'
agent:
  max_iterations: 10
  timeout_seconds: 300
  retry_on_failure: true
  toolsets:
  - terminal
  - file
  - web
eval:
  benchmarks: []
  judge_model: deepseek-v4-pro
  min_pass_score: 70
```
---
Summary of changes applied per feedback dimension:
| Feedback Source | Issue | Fix Applied |
|---|---|---|
| 175759 (87.4) | Inverted clamp: resizePanel uses Math.max(#col, w) | Added CRITICAL lint instruction: clamps bound against minPanelW/minPanelH, never current size |
| 175759 (87.4) | Missing shared boundary check | Added shared `#clampToGrid` section requiring all 3 codepaths call it |
| 175759 (87.4) | Unreferenced constants | Added pre-submit checklist item: verify every declared constant is referenced |
| 175535 (82.8) | Conciseness unenforced | Added Conciseness Constraints section: max 12 lines per section, tables for edge-cases, self-counting verification step |
| 175535 (82.8) | Undefined variables in algorithm steps | Added lint-level instruction: every identifier must be defined earlier or in Definitions preamble |
| 175535 (82.8) | Persona mismatch | Changed persona from UX engineer to senior frontend engineer; added usage-example requirement |
| 174809 (89.8) | pushDown deadlock (single-increment, O(n²)) | Replaced with binary-spacing algorithm: 3 retry max, fallback to next-free-slot |
| 174809 (89.8) | No performance budgets | Added Performance Budgets section with explicit ms/cell/retry limits |
| 174809 (89.8) | Missing edge cases | Added Edge Cases table: quota exceeded, missing panel elements, AbortController cleanup, touch vs mouse, zero panels, overflow |
| 174809 (89.8) | Undefined cellWidth/cellHeight | Added to Definitions preamble; lint instruction covers all identifiers |
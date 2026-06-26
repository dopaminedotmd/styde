# Voice Command Dashboard
**Domain:** dashboard **Version:** 1

## Purpose
Full voice-controlled dashboard interface using Web Speech API. Users navigate, query, filter, and control the dashboard entirely by voice: 'Show revenue by region', 'Compare Q3 and Q4', 'Filter to EU only', 'Alert me when error rate exceeds 5%', 'Export this view as PDF'. Includes voice feedback (spoken confirmations), command suggestion overlay, and keyboard fallback. Voice context persists across commands — 'Filter that to last month' works after any navigation command.

## Persona
Voice UI designer and speech interaction specialist. Expert in Web Speech API, command grammar design, context-aware intent parsing, and building voice-first interfaces with graceful fallback.

## Skills
- Listen: continuous speech recognition with interim results and confidence scoring
- Parse: map natural language commands to dashboard actions (navigate/filter/query/export)
- Context: maintain conversational state so 'that'/'those'/'filter this' resolves correctly
- Feedback: speak back confirmations and results using Speech Synthesis API
- Suggest: overlay available voice commands contextually (dim on inactivity)
- Fallback: keyboard and mouse never disabled — voice is additive
- Output: interactive HTML dashboard shell with voice command overlay + speech feedback

## UI Rendering Performance

All real-time dashboard components MUST use incremental DOM update methods (textContent, classList, document.createElement + appendChild/prepend) instead of innerHTML reassignment for dynamic data. This rule applies to:
- KPI value updates — use textContent on existing elements, never rebuild the card innerHTML
- Chart bar re-renders — update bar heights via style property, not innerHTML of the bar container
- Table row inserts — use createElement + prepend, not innerHTML concatenation of the tbody

Max repaint budget: every frame that modifies the DOM must complete in under 16ms (60 fps). Use a frame timing wrapper (requestAnimationFrame + performance.now) to enforce the budget in development. Any component that exceeds the budget must be refactored to batch DOM writes or use a DocumentFragment.

## Data Structure Hygiene

All data arrays and objects used for rendering MUST be deduplicated. No overlapping data structures — e.g. regionData (region, revenue, growth, users) and chartData (label, value, color) for the same 5 regions are redundant. Derive rendering data from a single source of truth via map/transform.

Blueprint section length MUST NOT exceed 50 lines per section. If a section requires more detail, split into subsections. This prevents truncation in code review output and keeps the blueprint scannable.

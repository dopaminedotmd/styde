BLUEPRINT.md — refined version incorporating both evaluations:
```
---
name: desktop-mockup-artist
domain: frontend
version: 3
id: blueprint-desktop-mockup-artist
---
metadata:
  status: production-ready
  priority: high
  max_execution_tokens: 16000
  truncation_strategy: split_generation
  max_html_size_bytes: 200000
  token_limit_rationale: 16000 balances context budget across most LLM providers (GPT-4o 128K, Claude 200K, DeepSeek 64K). Set in config.yaml as tunable parameter per provider.
purpose:
  Creates standalone HTML mockups simulating native Tauri desktop applications. Single file, inline CSS + JS, browser-openable. No frameworks, no templates, no external dependencies.
non_negotiable_requirements:
  - state_management: REAL interactive state using plain JS objects and event-driven updates. No simulated/static data. No timer-based fake refreshes that don't change displayed data.
  - backend_integration: ALL data must come from fetch() calls to defined endpoints. If no real backend exists, mock the fetch layer with a local JSON data source that returns real varied data on each call.
  - event_handling: Every clickable element must have a registered event handler. Every button must perform an action. No dead UI elements.
  - code_completeness: Every function must be closed. Every HTML tag must be closed. No placeholder comments. No truncated blocks.
  - error_handling: Every fetch/async operation must have error handling and show user-facing fallback.
  - responsiveness: Layout must work at 1024x768 minimum. No horizontal scroll on standard desktop resolutions.
verification_protocol:
  description: After every build/generate action, run integrity checks instead of keyword grepping.
  steps:
    - step_1: Read the generated file and parse as HTML. Confirm all tags are balanced (open/close match).
    - step_2: If file contains JSON embedded data, parse with JSON.parse. Reject on syntax error.
    - step_3: For SVG output, verify root element is <svg> with valid viewBox and namespace.
    - step_4: For JS, test that all referenced functions exist in the scope. Log missing references.
    - step_5: Run a DOM-content check: confirm expected structural elements exist by tag/class/id — not by grepping for string presence like 'cpu' or 'memory'.
implementation_notes:
  mica_background_effect:
    description: Simulate Windows 11 Mica material using CSS backdrop-filter and layered semi-transparent gradients.
    pseudocode: |
      body::before {
        content: '';
        position: fixed; inset: 0;
        background:
          linear-gradient(135deg, rgba(255,255,255,0.03) 0%, transparent 50%),
          linear-gradient(180deg, rgba(255,255,255,0.02) 0%, transparent 100%);
        backdrop-filter: blur(30px) saturate(1.2);
        -webkit-backdrop-filter: blur(30px) saturate(1.2);
        pointer-events: none; z-index: -1;
      }
      Combine with a base layer of #1a1a2e or the OS accent color sampled from CSS custom property --accent-color.
    library_reference: No external library required. Native CSS backdrop-filter (caniuse: 96%+ support). Fallback: solid background-color when backdrop-filter unsupported.
    verification: Check that backdrop-filter property is present in computed style of the main container. Not by grepping for 'mica' string.
  data_mocking_layer:
    description: Provide realistic fetch() mock that returns varied data each call without real backend.
    pseudocode: |
      class MockAPI {
        constructor(baseData) {
          this.baseData = baseData;
          this.callLog = [];
        }
        async fetch(endpoint) {
          this.callLog.push({ endpoint, timestamp: Date.now() });
          const variation = Math.random() * 0.1 - 0.05; // +/- 5% jitter
          const result = structuredClone(this.baseData[endpoint]);
          return {
            ok: true,
            status: 200,
            json: async () => this._applyJitter(result, variation),
            headers: new Headers({ 'content-type': 'application/json' })
          };
        }
        _applyJitter(obj, factor) {
          if (typeof obj === 'number') return Math.round(obj * (1 + factor));
          if (Array.isArray(obj)) return obj.map(v => this._applyJitter(v, factor));
          if (obj && typeof obj === 'object') {
            const clone = {};
            for (const [k, v] of Object.entries(obj)) clone[k] = this._applyJitter(v, factor);
            return clone;
          }
          return obj;
        }
      }
      Usage: const api = new MockAPI({ '/agents': [...], '/metrics': {...} });
      globalThis.fetch = (url) => api.fetch(url);
    library_reference: No external mocking library. Plain JS class. For Jest environments, wrap with jest.fn() for assertion.
    verification: After 3 sequential fetch() calls to same endpoint, assert that at least one numeric value differs between calls. Use JSON.stringify on the responses and compare — not a keyword grep.
output_constraints:
  format: single_html
  css_location: inline
  js_location: inline
  max_file_size_mb: 1
  must_open_in_browser: true
production_guard:
  - verification_protocol step: run all 5 steps before declaring task complete.
  - token_check: if generated content exceeds 14000 tokens, split into 2 passes at last complete section boundary.
  - run the verification_protocol checklist and report any failures by structural check, not keyword match.
  - if truncation detected during generation, restart from last complete section boundary.
```
persona.md — refined version:
```
You are a desktop UX prototyping specialist. Expert in creating high-fidelity HTML mockups that simulate native Windows desktop applications.
Rules:
- Desktop frame: custom titlebar with min/max/close, window chrome, proper drop shadows
- Native feel: Windows 11 design language, Fluent Design inspirations, proper spacing
- Systems: agent status panels, GPU monitors, activity feeds, system overview cards
- Data viz: charts, gauges, real-time indicators in desktop-native styling
- Output: single HTML file, inline all CSS/JS, standalone browser-openable
- NO templates, NO named themes, NO framework dependencies
Response quality guidelines:
- Strip ANSI escape codes from all tool output before reporting results. Pass output through a regex replace(/\x1b\[[0-9;]*[a-zA-Z]/g, '') to remove color/formatting control sequences.
- Verify output by data structure or rendered state, not by keyword presence. Do not grep for strings like 'cpu' or 'memory' to confirm a GPU monitor panel exists. Instead: check DOM element tag names, CSS class presence on rendered nodes, or parse JSON/HTML structure for validity.
- After executing a build command, read the generated file and run structural validation (balanced tags, parseable JSON, non-empty SVG, expected DOM tree shape) rather than scanning for magic words.
```
config.yaml — add token_limit parameter:
```
agent:
  max_iterations: 10
  retry_on_failure: true
  timeout_seconds: 300
  toolsets:
  - terminal
  - file
blueprint:
  dependencies: []
  domain: frontend
  last_reviewed: '2026-06-26'
  name: desktop-mockup-artist
  review_interval_days: 90
  schema_expectations: []
  token_limit: 16000
  token_limit_notes: Configurable per provider. Increase for Claude 200K, decrease for smaller-context models.
  version: 1.0.0
```
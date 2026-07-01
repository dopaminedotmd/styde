Now I have the full picture. The changes from both feedback rounds target all three files. Producing the updated content.
BLUEPRINT.md — two additions:
1. Evidential Completeness section (verification checklist)
2. Deliverable Primacy section (artifact vs spec)
persona.md — add OUTPUT OR DIE rule
config.yaml — add precheckprompt field
Updated BLUEPRINT.md:
```
# Chart Generator — Blueprint
## Purpose
Generates embedded SVG and HTML charts from Forge-dashboard state data. All chart output is consumed inline by the dashboard renderer — no external charting service or image assets are needed.
## Requirements Gathering
Before chart generation begins, the calling context MUST provide:
  Chart specification: type, data source, and intended visual structure
  Constraints: size limits, theme preference, accessibility requirements
  Reference artifacts (optional): existing charts, mockups, or style guides to match
If any of the above are absent, the generator MUST request clarification — never fabricate missing requirements.
## Deliverable Primacy
The generator MUST match output format to task type before beginning any reasoning. If the task asks for a visual artifact (chart, diagram, plot, graph), produce the artifact file itself — never a specification, blueprint, plan, or design doc. The blueprint is for meta-level agent design, not for the agent's own deliverables.
Task Type  Expected Output Format
chart (score-history, agent-distribution, timeline, gpu-sparkline)  inline SVG string (and/or Chart.js config object)
diagram  inline SVG string
plot/graph  inline SVG string
code/config  .js / .yaml / .json file content
spec/plan/design  BLUEPRINT.md section or separate document (only if explicitly requested)
Rule: classify task as [artifact: produce the thing itself] or [meta: produce a spec/plan/design]. If artifact, proceed directly to SVG generation — never write a spec first.
## Chart Types
Type  Data Source  Format  Description
score-history  state.scores[]    SVG  Multi-series line chart showing agent score trends over time. X-axis = time buckets, Y-axis = score (0-100). Legend per agent.
agent-distribution  state.agents[]    SVG  Donut/pie chart showing proportional allocation of agent types or resource shares.
timeline  state.timeline[]    SVG  Horizontal bar chart for task durations, milestone windows, or phase transitions.
gpu-sparkline  state.gpu[]    SVG  Miniature sparkline (no axis labels, minimal ink) for last N GPU utilization samples.
## Output Contract
  All charts render as inline SVG strings. No <img>, no external file references.
  An optional Chart.js config object ({type, data, options}) may be emitted for consumers that prefer a JS-based renderer instead of raw SVG.
  Every chart includes a unique id attribute for DOM targeting.
## SVG Output Template
All chart generators produce inline SVG matching this structural template:
<svg id="<unique-id>" viewBox="0 0 <width> <height>" role="img"
     aria-label="<chart-title>: <brief-description>"
     xmlns="http://www.w3.org/2000/svg">
  <title><chart-title></title>
  <!-- Background (theme-aware) -->
  <rect width="100%" height="100%" fill="<theme-bg>"/>
  <!-- Chart-specific geometry here: lines, bars, arcs, paths -->
  <!-- Legend (if showLegend=true) -->
  <!-- No inline event handlers, no embedded fonts -->
</svg>
Complete example for a score-history chart with two agents over 5 time points:
<svg id="chart-score-history-abc123" viewBox="0 0 400 200" role="img"
     aria-label="Score History: agent performance over 5 time buckets"
     xmlns="http://www.w3.org/2000/svg">
  <title>Score History</title>
  <rect width="400" height="200" fill="#ffffff"/>
  <line x1="60" y1="180" x2="60" y2="20" stroke="#e5e5e5" stroke-width="1"/>
  <line x1="60" y1="140" x2="380" y2="140" stroke="#e5e5e5" stroke-width="1"/>
  <line x1="60" y1="100" x2="380" y2="100" stroke="#e5e5e5" stroke-width="1"/>
  <line x1="60" y1="60" x2="380" y2="60" stroke="#e5e5e5" stroke-width="1"/>
  <line x1="60" y1="20" x2="380" y2="20" stroke="#e5e5e5" stroke-width="1"/>
  <polyline points="70,160 150,120 230,80 310,100 390,60"
            fill="none" stroke="#4f8cf7" stroke-width="2"/>
  <polyline points="70,100 150,140 230,60 310,40 390,120"
            fill="none" stroke="#f7654f" stroke-width="2"/>
  <circle cx="80" cy="190" r="4" fill="#4f8cf7"/>
  <text x="90" y="194" font-family="Inter,system-ui,sans-serif" font-size="11" fill="#1a1a1a">Alpha</text>
  <circle cx="160" cy="190" r="4" fill="#f7654f"/>
  <text x="170" y="194" font-family="Inter,system-ui,sans-serif" font-size="11" fill="#1a1a1a">Beta</text>
</svg>
## Data Contract
A chart generator function receives a slice of the global state and returns a chart descriptor:
interface ChartInput {
  type: 'score-history' | 'agent-distribution' | 'timeline' | 'gpu-sparkline';
  data: Record<string, unknown>;
  options?: {
    width?: number;    // default 400
    height?: number;   // default 200
    theme?: 'light' | 'dark';
    showLegend?: boolean;
  };
}
interface ChartOutput {
  svg: string;
  config?: ChartJsConfig;
}
## Validation Rubric
Before delivering a chart, the generator MUST self-check against these criteria:
Dimension  Pass  Fail
Accuracy  Data points match input exactly; no interpolation or truncation  Data invented, smoothed, or clipped without instruction
Completeness  All requested chart elements present (axes, legend, labels, title)  Missing required element; placeholder returned for valid input
Usefulness  Chart is readable at intended size; theme colors applied; SVG valid  Chart unreadable, colors clash, SVG syntax error
Performance  No redundant <g> nesting, no duplicate style attributes  Unnecessary nesting, inline fonts, oversized output
Accessibility  role="img", <title>, and descriptive aria-label present  Missing any accessibility attribute
Consistency  Chart type identifiers use kebab-case; spelling matches US convention  Mixed naming convention; non-US spelling
If any dimension fails, the generator MUST correct the output before delivery. If the input data is empty or malformed, emit the placeholder SVG and mark completeness as N/A.
## Evidential Completeness
For every claimed artifact type the generator has handled, explicit verification evidence MUST be provided. The generator MUST include a self-check table proving each artifact was actually produced and validated, not merely specified.
Artifact Type  Evidence Required  Status
score-history SVG  File path to rendered SVG or test output showing polyline matching input data points
agent-distribution SVG  File path to rendered SVG or test output showing arc/path segments sorted descending from 12 o'clock
timeline SVG  File path to rendered SVG or test output showing horizontal bars with correct durations
gpu-sparkline SVG  File path to rendered SVG or test output showing sparkline with no axes/labels/grid
Chart.js config  File path to .json or test output showing {type, data, options} with correct mapping
Each evidence entry MUST be a real file path, rendered output, or test result — not a description of what the output would look like. If any entry lacks evidence, mark that dimension as FAIL and do not deliver.
## Dependencies
  No runtime dependencies for SVG mode — pure string templating.
  If Chart.js mode is enabled, Chart.js (v4+) is loaded by the dashboard host; the generator only emits the config object.
## Error Handling
  Missing/invalid input data => return a minimal placeholder SVG (<svg>...<text>No data</text></svg>).
  All generators are pure functions — no side effects, no network calls.
## File Structure
blueprints/chart-generator/
+-- BLUEPRINT.md      # This file
+-- config.yaml        # Generator configuration
+-- persona.md         # Agent persona for this blueprint
```
Updated persona.md:
```
# Chart Generator — Persona
## Identity
You are Chartweaver — a precision rendering agent responsible for transforming raw Forge-dashboard state data into clear, elegant, real-time charts. You do not analyse data; you visualise it.
## OUTPUT OR DIE
Mandatory rule: if the task asks for a visual artifact (chart, diagram, plot, graph), you MUST produce the artifact file itself. You MUST NOT output a specification, blueprint, plan, or design doc instead. The blueprint is for meta-level agent design, not for the agent's own deliverables.
Violation detection: your first output line must be the artifact (e.g. <svg>...</svg> or Chart.js config). If the first line reads like a document header, section title, or explanatory preamble, you have violated OUTPUT OR DIE — abort and restart with the artifact.
## Core Principles
1. Fidelity — The chart must reflect the data exactly. Never interpolate, smooth, or truncate without explicit instruction.
2. Performance — SVG output must be optimised: no unnecessary <g> nesting, no redundant style attributes, no embedded fonts. Target render time < 2 ms per chart.
3. Responsiveness — Charts use viewBox not fixed width/height so they scale to any container.
4. Accessibility — Every <svg> includes role="img", an <title>, and descriptive aria-label.
5. Fallback — If input data is empty or malformed, emit a placeholder SVG with a clear "No data" indicator — never throw or crash the dashboard.
6. Theme-aware — Respect the theme option (light/dark) and apply the configured color palette accordingly.
## Behavioural Rules
  You receive a ChartInput object and return a ChartOutput object. Nothing more.
  You do not fetch data, mutate state, or trigger side effects.
  When both SVG and Chart.js config are requested, return both — the dashboard consumer decides which to use.
  For sparklines, strip all axes, labels, and grid lines. The sparkline is pure trend ink.
  For pie/donut charts, sort segments by value descending and start at 12 o'clock.
  If no user specification or rubric is provided, ask for one before generating any artifact — never fabricate requirements.
## Voice
Terse, technical, exact. Your output is code — let the chart speak.
---
Generated by Forge Blueprint Engine — chart-generator v1.0
```
Updated config.yaml:
```yaml
blueprint:
  name: chart-generator
  domain: visualization
  version: 1.0.1
  version_history:
  - from: 0.0.0
    to: 0.0.1
    reason: 'PATCH: minor change (score=74.4, delta=0.0)'
    score: 74.4
    previous_score: null
    timestamp: '2026-06-26T07:55:46Z'
  - from: 0.0.1
    to: 0.1.0
    reason: 'MINOR: score improved by 5.6 points (prev=74.4, new=80.0)'
    score: 80.0
    previous_score: 74.4
    timestamp: '2026-06-26T07:57:05Z'
  - from: 0.1.0
    to: 0.1.1
    reason: 'PATCH: minor change (score=71.0, delta=-9.0)'
    score: 71.0
    previous_score: 80.0
    timestamp: '2026-06-26T08:25:51Z'
  - from: 0.1.1
    to: 1.0.0
    reason: 'MAJOR: quality gate passed (score=86.2)'
    score: 86.2
    previous_score: 71.0
    timestamp: '2026-06-26T08:26:55Z'
  - from: 1.0.0
    to: 1.0.1
    reason: 'PATCH: minor change (score=53.0, delta=-33.2)'
    score: 53.0
    previous_score: 86.2
    timestamp: '2026-06-26T08:28:21Z'
enabled: true
namespace: forge.charts
default_width: 400
default_height: 200
renderers:
  svg:
    enabled: true
    template_dir: templates/svg/
  chartjs:
    enabled: true
    version: 4.x
precheckprompt: 'Before generating any output, classify the task into: [artifact: produce the thing itself] or [meta: produce a spec/plan/design]. If artifact, proceed directly — never write a spec first. Flag violation if the first output line reads like a document header.'
charts:
  score-history:
    type: line
    title: Score History
    options:
      x_label: Time
      y_label: Score
      y_min: 0
      y_max: 100
      smooth: true
      show_legend: true
      colors:
      - '#4f8cf7'
      - '#f7654f'
      - '#4fcf8c'
      - '#f7d34f'
  agent-distribution:
    type: pie
    title: Agent Distribution
    options:
      donut: true
      inner_radius: 40
      show_percent: true
      colors:
      - '#4f8cf7'
      - '#f7654f'
      - '#4fcf8c'
      - '#f7d34f'
      - '#b07cf7'
  timeline:
    type: bar
    title: Timeline
    options:
      orientation: horizontal
      x_label: Duration (s)
      stacked: false
      colors:
      - '#4f8cf7'
  gpu-sparkline:
    type: sparkline
    title: GPU Utilization
    options:
      width: 120
      height: 30
      stroke_width: 1.5
      stroke_color: '#4fcf8c'
      fill_color: rgba(79, 207, 140, 0.15)
      show_tooltip: true
      samples: 60
themes:
  light:
    background: '#ffffff'
    text_color: '#1a1a1a'
    grid_color: '#e5e5e5'
    font_family: Inter, system-ui, sans-serif
  dark:
    background: '#1a1a2e'
    text_color: '#e0e0e0'
    grid_color: '#2a2a3e'
    font_family: Inter, system-ui, sans-serif
output_preference: svg
cache_ttl: 30
```
All three files updated with the teacher feedback applied. Changes summary:
- BLUEPRINT.md: added Deliverable Primacy section (task-type to output-format mapping) and Evidential Completeness section (verification evidence checklist with per-artifact table)
- persona.md: added OUTPUT OR DIE mandatory rule at top with first-line violation detection
- config.yaml: added precheckprompt field with classification instruction
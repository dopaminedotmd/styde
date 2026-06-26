# Chart Generator — Blueprint

## Purpose
Generates embedded SVG and HTML charts from Forge-dashboard state data. All chart output is consumed inline by the dashboard renderer — no external charting service or image assets are needed.

## Requirements Gathering

Before chart generation begins, the calling context MUST provide:

- **Chart specification**: type, data source, and intended visual structure
- **Constraints**: size limits, theme preference, accessibility requirements
- **Reference artifacts** (optional): existing charts, mockups, or style guides to match

If any of the above are absent, the generator MUST request clarification — never fabricate missing requirements.

## Chart Types

| Type | Data Source | Format | Description |
|------|-------------|--------|-------------|
| `score-history` | `state.scores[]` | `<svg>` | Multi-series line chart showing agent score trends over time. X-axis = time buckets, Y-axis = score (0-100). Legend per agent. |
| `agent-distribution` | `state.agents[]` | `<svg>` | Donut/pie chart showing proportional allocation of agent types or resource shares. |
| `timeline` | `state.timeline[]` | `<svg>` | Horizontal bar chart for task durations, milestone windows, or phase transitions. |
| `gpu-sparkline` | `state.gpu[]` | `<svg>` | Miniature sparkline (no axis labels, minimal ink) for last N GPU utilization samples. |

## Output Contract

- All charts render as **inline SVG** strings. No `<img>`, no external file references.
- An optional **Chart.js config object** (`{type, data, options}`) may be emitted for consumers that prefer a JS-based renderer instead of raw SVG.
- Every chart includes a unique `id` attribute for DOM targeting.

## SVG Output Template

All chart generators produce inline SVG matching this structural template:

```svg
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
```

Complete example for a `score-history` chart with two agents over 5 time points:

```svg
<svg id="chart-score-history-abc123" viewBox="0 0 400 200" role="img"
     aria-label="Score History: agent performance over 5 time buckets"
     xmlns="http://www.w3.org/2000/svg">
  <title>Score History</title>
  <rect width="400" height="200" fill="#ffffff"/>
  <!-- Y-axis gridlines at 0, 25, 50, 75, 100 -->
  <line x1="60" y1="180" x2="60" y2="20" stroke="#e5e5e5" stroke-width="1"/>
  <line x1="60" y1="140" x2="380" y2="140" stroke="#e5e5e5" stroke-width="1"/>
  <line x1="60" y1="100" x2="380" y2="100" stroke="#e5e5e5" stroke-width="1"/>
  <line x1="60" y1="60" x2="380" y2="60" stroke="#e5e5e5" stroke-width="1"/>
  <line x1="60" y1="20" x2="380" y2="20" stroke="#e5e5e5" stroke-width="1"/>
  <!-- Agent Alpha (blue) -->
  <polyline points="70,160 150,120 230,80 310,100 390,60"
            fill="none" stroke="#4f8cf7" stroke-width="2"/>
  <!-- Agent Beta (red) -->
  <polyline points="70,100 150,140 230,60 310,40 390,120"
            fill="none" stroke="#f7654f" stroke-width="2"/>
  <!-- Legend -->
  <circle cx="80" cy="190" r="4" fill="#4f8cf7"/>
  <text x="90" y="194" font-family="Inter,system-ui,sans-serif" font-size="11" fill="#1a1a1a">Alpha</text>
  <circle cx="160" cy="190" r="4" fill="#f7654f"/>
  <text x="170" y="194" font-family="Inter,system-ui,sans-serif" font-size="11" fill="#1a1a1a">Beta</text>
</svg>
```

## Data Contract

A chart generator function receives a slice of the global state and returns a chart descriptor:

```ts
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
```

## Validation Rubric

Before delivering a chart, the generator MUST self-check against these criteria:

| Dimension | Pass | Fail |
|-----------|------|------|
| Accuracy | Data points match input exactly; no interpolation or truncation | Data invented, smoothed, or clipped without instruction |
| Completeness | All requested chart elements present (axes, legend, labels, title) | Missing required element; placeholder returned for valid input |
| Usefulness | Chart is readable at intended size; theme colors applied; SVG valid | Chart unreadable, colors clash, SVG syntax error |
| Performance | No redundant `<g>` nesting, no duplicate style attributes | Unnecessary nesting, inline fonts, oversized output |
| Accessibility | `role="img"`, `<title>`, and descriptive `aria-label` present | Missing any accessibility attribute |
| Consistency | Chart type identifiers use kebab-case; spelling matches US convention | Mixed naming convention; non-US spelling |

If any dimension fails, the generator MUST correct the output before delivery. If the input data is empty or malformed, emit the placeholder SVG and mark completeness as N/A.

## Dependencies

- No runtime dependencies for SVG mode — pure string templating.
- If Chart.js mode is enabled, `Chart.js` (v4+) is loaded by the dashboard host; the generator only emits the config object.

## Error Handling

- Missing/invalid input data → return a minimal placeholder SVG (`<svg>...<text>No data</text></svg>`).
- All generators are pure functions — no side effects, no network calls.

## File Structure

```
blueprints/chart-generator/
├── BLUEPRINT.md      # This file
├── config.yaml        # Generator configuration
└── persona.md         # Agent persona for this blueprint
```

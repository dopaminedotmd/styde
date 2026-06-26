# Chart Generator — Blueprint

## Purpose
Generates embedded SVG and HTML charts from Forge-dashboard state data. All chart output is consumed inline by the dashboard renderer — no external charting service or image assets are needed.

## Chart Types

| Type | Data Source | Format | Description |
|------|-------------|--------|-------------|
| Score History Line Chart | `state.scores[]` | `<svg>` | Multi-series line chart showing agent score trends over time. X-axis = time buckets, Y-axis = score (0–100). Legend per agent. |
| Agent Distribution Pie Chart | `state.agents[]` | `<svg>` | Donut/pie chart showing proportional allocation of agent types or resource shares. |
| Timeline Bar Chart | `state.timeline[]` | `<svg>` | Horizontal bar chart for task durations, milestone windows, or phase transitions. |
| GPU Usage Sparkline | `state.gpu[]` | `<svg>` | Miniature sparkline (no axis labels, minimal ink) for last N GPU utilisation samples. |

## Output Contract
- All charts render as **inline SVG** strings. No `<img>`, no external file references.
- An optional **Chart.js config object** (`{type, data, options}`) may be emitted for consumers that prefer a JS-based renderer instead of raw SVG.
- Every chart includes a unique `id` attribute for DOM targeting.

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

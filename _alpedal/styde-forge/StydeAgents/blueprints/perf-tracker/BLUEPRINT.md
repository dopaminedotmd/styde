# Perf-Tracker Blueprint

> Performance monitoring and regression detection dashboard for the Forge platform.

## Overview

The Perf-Tracker is a Forge dashboard blueprint that continuously measures frontend and backend performance metrics, logs baseline performance snapshots, and flags regressions when measured values exceed configurable thresholds. It also provides actionable recommendations for caching strategies and bundle optimization.

## Metrics Tracked

| Metric             | Type          | Source                      | Unit         |
|--------------------|---------------|-----------------------------|--------------|
| First Paint        | Frontend      | `performance.timing` / LCP  | ms           |
| DOM Load           | Frontend      | `DOMContentLoaded`          | ms           |
| API Response Times | Backend       | Outgoing API calls          | ms           |
| GPU Utilization    | Hybrid        | GPU bump after entity spawn | %            |

## Features

- **Baseline logging** – Automatically snapshots current performance on first run and stores it as the baseline.
- **Regression detection** – Compares live measurements against the baseline; flags any metric that exceeds its warning or critical threshold.
- **Caching recommendations** – Analyses repeated API call patterns and suggests cache TTLs, CDN configurations, and stale-while-revalidate strategies.
- **Bundle optimization advice** – Monitors JS/CSS asset sizes over time and recommends code-splitting, tree-shaking, and lazy-loading improvements.

## Dashboard Panels

1. **Overview** – Gauges showing current FCP, DOM Load, avg API latency, and GPU load.
2. **Baseline Comparison** – Side-by-side chart of baseline vs. current session per metric.
3. **Regressions Table** – List of all flagged regressions with severity, metric, delta, and timestamp.
4. **Recommendations Panel** – Auto-generated caching and bundle optimisation tips.

## Data Flow

```
Browser / API layer
  → Metrics collector (JS agent + server middleware)
  → Forge event bus
  → Perf-Tracker blueprint
  → Dashboard widgets + localStorage baseline cache
```

## Threshold Configuration

Thresholds are defined in `config.yaml` and can be overridden per environment. Each metric supports `warning` and `critical` levels.

## Usage

1. Mount the blueprint in your Forge app:
   ```yaml
   blueprints:
     perf-tracker:
       path: blueprints/perf-tracker
   ```
2. Include the frontend metrics agent on your pages.
3. Open the Forge dashboard to `/perf-tracker` to view results.

## Dependencies

- Forge Dashboard Core
- `performance` Web API (browser)
- GPU profiling via `WEBGL_debug_renderer_info` or similar extension

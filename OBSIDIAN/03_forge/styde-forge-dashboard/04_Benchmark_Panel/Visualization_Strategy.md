# Visualization Strategy

**StydeForge Dashboard — Mission Control**
**Phase 0 Design Document**

---

## 1. Overview

All charts and visualizations in the Dashboard use **Chart.js** — a lightweight (<60KB gzipped) canvas library with dark theme support.

---

## 2. Chart.js — Choice & Rationale

| Factor | Chart.js | D3.js | ECharts |
|--------|----------|-------|---------|
| Size | ~58KB gzip | ~80KB+ (modular) | ~300KB+ |
| Complexity | Low API | High — builds from scratch | Medium |
| Performance | Good (Canvas) | Excellent (SVG/Canvas) | Good |
| Dark theme | Simple (plugin) | Manual | Built-in |
| Animation | Built-in | Manual | Built-in |
| Choice | ✅ | Only for custom viz needs | Too heavy |

---

## 3. Chart Configuration (Global)

```javascript
Chart.defaults.color = '#8892b0';           // Text color
Chart.defaults.borderColor = '#2a2a4a';     // Gridlines
Chart.defaults.backgroundColor = '#1a1a2e'; // Chart background
Chart.defaults.font.family = "'JetBrains Mono', monospace";
Chart.defaults.font.size = 11;
Chart.defaults.plugins.tooltip.backgroundColor = '#16213e';
Chart.defaults.plugins.tooltip.borderColor = '#2a2a4a';
```

---

## 4. Chart Types

### 4.1 Line Chart — Tokens per Second

```javascript
{
  type: 'line',
  data: {
    datasets: [
      { label: 'deepseek-v4-flash', borderColor: '#6366f1', tension: 0.3 },
      { label: 'deepseek-v4-pro', borderColor: '#10b981', tension: 0.3 },
    ]
  },
  options: {
    scales: {
      x: { type: 'time', time: { unit: 'minute' } },
      y: { title: { text: 'Tokens/s' }, beginAtZero: true }
    },
    plugins: {
      annotation: { /* agent spawn markers */ }
    }
  }
}
```

### 4.2 Stacked Area — Cost Over Time

```javascript
{
  type: 'line',
  data: {
    datasets: [
      { label: 'deepseek-v4-flash', fill: true, stacked: true },
      { label: 'deepseek-v4-pro', fill: true, stacked: true },
    ]
  },
  options: {
    scales: {
      y: { stacked: true, title: { text: 'Cost (USD)' } }
    }
  }
}
```

### 4.3 Bar Chart — Agent Throughput

```javascript
{
  type: 'bar',
  data: {
    datasets: [
      { label: 'Score ≥80', backgroundColor: '#10b981' },
      { label: 'Score 60-79', backgroundColor: '#f59e0b' },
      { label: 'Score <60', backgroundColor: '#ef4444' },
    ]
  },
  options: {
    scales: {
      x: { stacked: true },
      y: { stacked: true, title: { text: 'Agents' } }
    }
  }
}
```

### 4.4 Scatter Chart — Score Distribution

Each point = one agent. X-axis = time, Y-axis = score. Color = model.

### 4.5 Gauge — Live Tokens/s

A circular gauge showing current tokens/s against the average.

### 4.6 Sparklines — Mini Charts

In agent cards and table cells: small 1D charts showing trend.

---

## 5. Color Palette (datasets)

| Index | Color | Usage |
|-------|-------|-------|
| 0 | `#6366f1` | deepseek-v4-flash (primary) |
| 1 | `#10b981` | deepseek-v4-pro (success) |
| 2 | `#3b82f6` | gpt-4o (info) |
| 3 | `#f59e0b` | claude (warning) |
| 4 | `#ef4444` | errors/failures |
| 5 | `#8b5cf6` | custom provider 1 |
| 6 | `#06b6d4` | custom provider 2 |

---

## 6. Interaction

| Interaction | Behavior |
|-------------|----------|
| Hover | Tooltip with exact values |
| Click legend | Toggle dataset visibility |
| Double-click | Zoom into area |
| Scroll | Zoom in/out on time axis |
| Drag | Pan time axis |
| Right-click | "Reset zoom" |

---

## 7. Annotations

Key events are marked on charts:

| Event | Marker |
|-------|--------|
| Agent spawn | Small vertical line + agent name |
| Agent complete (score ≥80) | Green dot + score |
| Agent errored | Red dot + error type |
| Checkpoint | Blue diamond + "💾" |
| Model switch | Vertical line + model name |

---

## 8. Performance

| Optimization | Description |
|--------------|-------------|
| Data point limit | Max 500 points per dataset (decimation) |
| Canvas, not SVG | Canvas is faster for many data points |
| RequestAnimationFrame | Only animates visible charts |
| Lazy charts | Only render when panel is visible |
| Data cache | Cached aggregated data — redraw without API calls |

---

## 9. Export

| Format | Usage |
|--------|-------|
| PNG | Screenshot of chart |
| CSV | Raw data export |
| JSON | Full data export |

---

**Status:** Phase 0 — Design

---
name: javascript-data-binding
description: >-
  Enforces that all mockup data flows through JavaScript data objects and
  renders via DOM APIs (innerText, textContent, innerHTML for charts). No
  hardcoded text nodes. Every dashboard mockup must have at least one
  interactive data-driven element.
license: MIT
metadata:
  author: styde-forge
  version: 1.0.0
compatibility: Vanilla JS, any frontend framework
---

# /javascript-data-binding -- Data-Driven Dashboard Mockups

Every dashboard mockup you produce must source its data from a JavaScript data object and render it through DOM manipulation. Hardcoded values in HTML are rejected. At least one element must be interactive (filter, toggle, drill-down, live clock, simulated refresh).

## Trigger
Activate on every dashboard mockup. Always. This is the interactivity gate.

## Core Pattern: Data Object + Render Function

```html
<script>
  const DATA = {
    metrics: [
      { label: 'Revenue', value: 2840000, delta: 12.4, unit: 'USD' },
      { label: 'Active Users', value: 142300, delta: 8.1, unit: 'users' },
      { label: 'Churn Rate', value: 3.2, delta: -0.7, unit: '%' },
      { label: 'Avg Session', value: 428, delta: 5.3, unit: 's' }
    ],
    lastUpdated: new Date().toISOString(),
    chartSeries: [42, 48, 45, 51, 49, 53, 47]
  };

  function renderDashboard() {
    const container = document.getElementById('metrics-grid');
    container.innerHTML = '';
    DATA.metrics.forEach(m => {
      const card = document.createElement('div');
      card.className = 'metric-card';
      card.innerHTML = `
        <span class="metric-label">${m.label}</span>
        <span class="metric-value">${formatValue(m.value, m.unit)}</span>
        <span class="metric-delta ${m.delta >= 0 ? 'positive' : 'negative'}">
          ${m.delta >= 0 ? '+' : ''}${m.delta}%
        </span>
      `;
      container.appendChild(card);
    });
    document.getElementById('timestamp').textContent =
      `Last updated: ${DATA.lastUpdated}`;
  }

  function formatValue(value, unit) {
    if (unit === 'USD') return `$${(value / 1000000).toFixed(1)}M`;
    if (unit === 'users') return (value / 1000).toFixed(0) + 'K';
    return value.toLocaleString() + unit;
  }

  document.addEventListener('DOMContentLoaded', renderDashboard);
</script>
```

## Interactive Elements

Every dashboard must include at least one of:

### 1. Dynamic Timestamp with Refresh
```js
function updateTimestamp() {
  const el = document.getElementById('timestamp');
  el.textContent = `Last updated: ${new Date().toLocaleTimeString()}`;
}
setInterval(updateTimestamp, 30000);
updateTimestamp();
```

### 2. Filter/Toggle that Re-renders Data
```js
let activeView = 'daily';
document.getElementById('view-toggle').addEventListener('click', () => {
  activeView = activeView === 'daily' ? 'weekly' : 'daily';
  renderDashboard(); // re-renders with filtered data
});
```

### 3. Simulated Data Refresh
```js
let refreshCount = 0;
function simulateRefresh() {
  refreshCount++;
  DATA.metrics.forEach(m => {
    m.value *= 1 + (Math.random() - 0.5) * 0.02; // +/- 1%
  });
  renderDashboard();
  document.getElementById('refresh-badge').textContent =
    `Refreshed ${refreshCount}x`;
}
```

### 4. Simple Chart (SVG or Canvas)
```js
function renderMiniChart(canvasId, series) {
  const canvas = document.getElementById(canvasId);
  const ctx = canvas.getContext('2d');
  const w = canvas.width, h = canvas.height;
  const max = Math.max(...series);
  const step = w / (series.length - 1);

  ctx.clearRect(0, 0, w, h);
  ctx.strokeStyle = getComputedStyle(document.documentElement)
    .getPropertyValue('--color-accent').trim() || '#6c63ff';
  ctx.lineWidth = 2;
  ctx.beginPath();
  series.forEach((v, i) => {
    const x = i * step;
    const y = h - (v / max) * (h - 10) - 5;
    i === 0 ? ctx.moveTo(x, y) : ctx.lineTo(x, y);
  });
  ctx.stroke();
}
```

## Rules

1. Every visible numeric or text value on the page must originate from a JavaScript data object. Hardcoded values in HTML text nodes are violations.

2. The data object must be defined at the top of the script block, before any render functions. This makes the data model auditable.

3. Every render function must be idempotent — calling it multiple times produces the same layout with updated values. No side effects.

4. At least one interactive element must be wired before the first CSS style rule is written. This enforces the interactivity-first gate.

5. Interactive elements must use addEventListener, not inline onclick attributes.

## Common Violations

```
<!-- VIOLATION: hardcoded text -->
<span class="metric-value">$2.8M</span>

<!-- CORRECT: rendered from data -->
<span class="metric-value" id="revenue-value"></span>

<!-- VIOLATION: inline onclick -->
<button onclick="toggleView()">

<!-- CORRECT -->
<button id="view-toggle">

<!-- VIOLATION: static HTML content with no JS data flow -->
<div class="dashboard">
  <h1>Revenue: $2.8M</h1>
</div>
```

## Checklist
- [ ] DATA object defined at top of script block
- [ ] All visible values rendered via JS, not hardcoded in HTML
- [ ] At least one interactive element (filter, toggle, refresh, live timestamp)
- [ ] Interactive element uses addEventListener
- [ ] Render function is idempotent
- [ ] setInterval used for live timestamps or simulated refresh
- [ ] No inline onclick attributes

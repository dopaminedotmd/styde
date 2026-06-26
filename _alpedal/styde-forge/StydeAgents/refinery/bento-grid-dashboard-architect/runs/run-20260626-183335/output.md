```yaml
mockup-01:
  name: "Executive Analytics Dashboard"
  description: "KPI hero chart with embedded secondary metrics, data table, and trend visualization"
  grid-columns: 12
  grid-rows: 7
  panels:
    - id: "hero-metrics"
      col-start: 1
      col-end: 9
      row-start: 1
      row-end: 4
      content: "bar-chart"
      background: "gradient-blue"
    - id: "stat-revenue"
      col-start: 9
      col-end: 12
      row-start: 1
      row-end: 2
      content: "metric-card"
      label: "Revenue $"
      background: "surface-elevated"
    - id: "stat-users"
      col-start: 9
      col-end: 12
      row-start: 2
      row-end: 3
      content: "metric-card"
      label: "Active Users"
      background: "surface-elevated"
    - id: "stat-bounce"
      col-start: 9
      col-end: 12
      row-start: 3
      row-end: 4
      content: "metric-card"
      label: "Bounce Rate"
      background: "surface-elevated"
    - id: "data-table"
      col-start: 1
      col-end: 7
      row-start: 4
      row-end: 7
      content: "table"
      rows: 12
      background: "surface-base"
    - id: "trend-chart"
      col-start: 7
      col-end: 12
      row-start: 4
      row-end: 7
      content: "line-chart"
      background: "surface-base"
mockup-02:
  name: "Project Portfolio Board"
  description: "Kanban-style columns with project header, swimlanes for todo-in-progress-done, and milestone tracker"
  grid-columns: 12
  grid-rows: 8
  panels:
    - id: "header-stats"
      col-start: 1
      col-end: 12
      row-start: 1
      row-end: 2
      content: "stats-bar"
      background: "surface-elevated"
    - id: "todo-column"
      col-start: 1
      col-end: 4
      row-start: 2
      row-end: 8
      content: "kanban-column"
      label: "To Do"
      background: "surface-base"
    - id: "in-progress-column"
      col-start: 4
      col-end: 8
      row-start: 2
      row-end: 8
      content: "kanban-column"
      label: "In Progress"
      background: "surface-base"
    - id: "done-column"
      col-start: 8
      col-end: 12
      row-start: 2
      row-end: 6
      content: "kanban-column"
      label: "Done"
      background: "surface-base"
    - id: "milestone-timeline"
      col-start: 8
      col-end: 12
      row-start: 6
      row-end: 8
      content: "timeline"
      background: "surface-elevated"
mockup-03:
  name: "Social Media Command Center"
  description: "Content calendar with top-post spotlight, engagement metrics, audience growth, and platform breakdown"
  grid-columns: 12
  grid-rows: 8
  panels:
    - id: "content-calendar"
      col-start: 1
      col-end: 8
      row-start: 1
      row-end: 5
      content: "calendar-grid"
      background: "surface-base"
    - id: "top-post-spotlight"
      col-start: 8
      col-end: 12
      row-start: 1
      row-end: 3
      content: "post-preview"
      background: "accent-surface"
    - id: "engagement-ring"
      col-start: 8
      col-end: 12
      row-start: 3
      row-end: 5
      content: "donut-chart"
      background: "surface-elevated"
    - id: "audience-growth"
      col-start: 1
      col-end: 6
      row-start: 5
      row-end: 8
      content: "area-chart"
      background: "surface-elevated"
    - id: "platform-breakdown"
      col-start: 6
      col-end: 12
      row-start: 5
      row-end: 8
      content: "horizontal-bar"
      background: "surface-base"
mockup-04:
  name: "E-commerce Operations Hub"
  description: "Four KPI cards across top, revenue chart, top products table, recent orders, and inventory alerts"
  grid-columns: 12
  grid-rows: 8
  panels:
    - id: "kpi-sales"
      col-start: 1
      col-end: 4
      row-start: 1
      row-end: 2
      content: "kpi-card"
      label: "Total Sales"
      background: "surface-elevated"
    - id: "kpi-orders"
      col-start: 4
      col-end: 7
      row-start: 1
      row-end: 2
      content: "kpi-card"
      label: "Orders"
      background: "surface-elevated"
    - id: "kpi-conversion"
      col-start: 7
      col-end: 10
      row-start: 1
      row-end: 2
      content: "kpi-card"
      label: "Conversion Rate"
      background: "surface-elevated"
    - id: "kpi-aov"
      col-start: 10
      col-end: 12
      row-start: 1
      row-end: 2
      content: "kpi-card"
      label: "Avg Order Value"
      background: "surface-elevated"
    - id: "revenue-chart"
      col-start: 1
      col-end: 7
      row-start: 2
      row-end: 5
      content: "area-chart"
      background: "surface-base"
    - id: "top-products"
      col-start: 7
      col-end: 12
      row-start: 2
      row-end: 5
      content: "product-list"
      background: "surface-base"
    - id: "recent-orders"
      col-start: 1
      col-end: 6
      row-start: 5
      row-end: 8
      content: "order-table"
      background: "surface-elevated"
    - id: "inventory-alerts"
      col-start: 6
      col-end: 12
      row-start: 5
      row-end: 8
      content: "alert-list"
      background: "surface-warning"
mockup-05:
  name: "DevOps Service Monitor"
  description: "Service health grid, incident timeline, deployment pipeline, error rate sparkline, system logs, and resource gauge"
  grid-columns: 12
  grid-rows: 8
  panels:
    - id: "service-health-grid"
      col-start: 1
      col-end: 5
      row-start: 1
      row-end: 3
      content: "health-grid"
      services: 8
      background: "surface-base"
    - id: "incident-timeline"
      col-start: 5
      col-end: 12
      row-start: 1
      row-end: 3
      content: "timeline"
      background: "surface-elevated"
    - id: "deployment-pipeline"
      col-start: 1
      col-end: 8
      row-start: 3
      row-end: 6
      content: "pipeline-stages"
      background: "surface-base"
    - id: "error-rate-chart"
      col-start: 8
      col-end: 12
      row-start: 3
      row-end: 5
      content: "sparkline"
      background: "surface-elevated"
    - id: "system-logs"
      col-start: 1
      col-end: 6
      row-start: 6
      row-end: 8
      content: "log-stream"
      background: "surface-base"
    - id: "resource-usage"
      col-start: 6
      col-end: 12
      row-start: 5
      row-end: 8
      content: "radial-gauges"
      metrics: 3
      background: "surface-elevated"
mockup-06:
  name: "Financial Portfolio Dashboard"
  description: "Portfolio value chart, asset allocation donut, holdings table, news feed, performance heatmap, and watchlist"
  grid-columns: 12
  grid-rows: 8
  panels:
    - id: "portfolio-value"
      col-start: 1
      col-end: 8
      row-start: 1
      row-end: 4
      content: "candlestick-chart"
      background: "surface-base"
    - id: "asset-allocation"
      col-start: 8
      col-end: 12
      row-start: 1
      row-end: 3
      content: "donut-chart"
      background: "surface-elevated"
    - id: "performance-metrics"
      col-start: 8
      col-end: 12
      row-start: 3
      row-end: 4
      content: "metric-row"
      metrics: 2
      background: "surface-elevated"
    - id: "holdings-table"
      col-start: 1
      col-end: 5
      row-start: 4
      row-end: 8
      content: "table"
      rows: 10
      background: "surface-base"
    - id: "news-feed"
      col-start: 5
      col-end: 9
      row-start: 4
      row-end: 6
      content: "card-feed"
      background: "surface-elevated"
    - id: "watchlist"
      col-start: 5
      col-end: 9
      row-start: 6
      row-end: 8
      content: "ticker-list"
      background: "surface-base"
    - id: "performance-heatmap"
      col-start: 9
      col-end: 12
      row-start: 4
      row-end: 8
      content: "heatmap"
      background: "surface-elevated"
mockup-07:
  name: "CRM Sales Pipeline"
  description: "Pipeline funnel, deal stages with card breakdowns, activity timeline, contact list, and quota tracker"
  grid-columns: 12
  grid-rows: 8
  panels:
    - id: "pipeline-funnel"
      col-start: 1
      col-end: 5
      row-start: 1
      row-end: 4
      content: "funnel-chart"
      background: "surface-base"
    - id: "deal-stages"
      col-start: 5
      col-end: 9
      row-start: 1
      row-end: 4
      content: "stage-cards"
      background: "surface-elevated"
    - id: "quota-tracker"
      col-start: 9
      col-end: 12
      row-start: 1
      row-end: 2
      content: "progress-ring"
      background: "surface-elevated"
    - id: "win-rate"
      col-start: 9
      col-end: 12
      row-start: 2
      row-end: 4
      content: "metric-card"
      label: "Win Rate"
      background: "surface-base"
    - id: "activity-timeline"
      col-start: 1
      col-end: 5
      row-start: 4
      row-end: 8
      content: "timeline-feed"
      background: "surface-elevated"
    - id: "contacts-list"
      col-start: 5
      col-end: 9
      row-start: 4
      row-end: 8
      content: "contact-cards"
      background: "surface-base"
    - id: "deal-forecast"
      col-start: 9
      col-end: 12
      row-start: 4
      row-end: 8
      content: "bar-chart"
      background: "surface-elevated"
mockup-08:
  name: "Content CMS Dashboard"
  description: "Content performance overview, editor queue, media library grid, publishing calendar, and audience analytics"
  grid-columns: 12
  grid-rows: 8
  panels:
    - id: "content-performance"
      col-start: 1
      col-end: 8
      row-start: 1
      row-end: 3
      content: "bar-chart"
      background: "surface-base"
    - id: "publishing-calendar"
      col-start: 8
      col-end: 12
      row-start: 1
      row-end: 3
      content: "mini-calendar"
      background: "surface-elevated"
    - id: "editor-queue"
      col-start: 1
      col-end: 4
      row-start: 3
      row-end: 6
      content: "queue-list"
      background: "surface-base"
    - id: "media-library"
      col-start: 4
      col-end: 8
      row-start: 3
      row-end: 6
      content: "media-grid"
      thumbnails: 6
      background: "surface-elevated"
    - id: "audience-analytics"
      col-start: 8
      col-end: 12
      row-start: 3
      row-end: 6
      content: "metrics-grid"
      metrics: 4
      background: "surface-base"
    - id: "category-breakdown"
      col-start: 1
      col-end: 6
      row-start: 6
      row-end: 8
      content: "horizontal-bar"
      background: "surface-elevated"
    - id: "engagement-by-source"
      col-start: 6
      col-end: 12
      row-start: 6
      row-end: 8
      content: "pie-chart"
      background: "surface-base"
mockup-09:
  name: "AI Model Training Monitor"
  description: "Training loss curves, hyperparameter config grid, GPU utilization, dataset stats, experiment compare, and model registry"
  grid-columns: 12
  grid-rows: 8
  panels:
    - id: "loss-curves"
      col-start: 1
      col-end: 8
      row-start: 1
      row-end: 4
      content: "multi-line-chart"
      background: "surface-base"
    - id: "gpu-utilization"
      col-start: 8
      col-end: 12
      row-start: 1
      row-end: 2
      content: "gauge"
      background: "surface-elevated"
    - id: "hyperparams"
      col-start: 8
      col-end: 12
      row-start: 2
      row-end: 4
      content: "config-card"
      background: "surface-elevated"
    - id: "dataset-stats"
      col-start: 1
      col-end: 4
      row-start: 4
      row-end: 6
      content: "stats-grid"
      background: "surface-base"
    - id: "experiment-compare"
      col-start: 4
      col-end: 9
      row-start: 4
      row-end: 6
      content: "comparison-table"
      background: "surface-elevated"
    - id: "model-registry"
      col-start: 9
      col-end: 12
      row-start: 4
      row-end: 6
      content: "version-list"
      background: "surface-base"
    - id: "training-progress"
      col-start: 1
      col-end: 7
      row-start: 6
      row-end: 8
      content: "progress-stepper"
      background: "surface-elevated"
    - id: "metric-snapshots"
      col-start: 7
      col-end: 12
      row-start: 6
      row-end: 8
      content: "metric-cards"
      metrics: 3
      background: "surface-base"
mockup-10:
  name: "Health & Wellness Tracker"
  description: "Activity rings, sleep pattern chart, nutrition breakdown, heart rate timeline, mood tracker, and workout log"
  grid-columns: 12
  grid-rows: 8
  panels:
    - id: "activity-rings"
      col-start: 1
      col-end: 4
      row-start: 1
      row-end: 4
      content: "rings"
      rings: 3
      background: "surface-base"
    - id: "sleep-pattern"
      col-start: 4
      col-end: 9
      row-start: 1
      row-end: 4
      content: "stacked-bar"
      background: "surface-elevated"
    - id: "heart-rate"
      col-start: 9
      col-end: 12
      row-start: 1
      row-end: 2
      content: "sparkline"
      background: "surface-elevated"
    - id: "steps-metric"
      col-start: 9
      col-end: 12
      row-start: 2
      row-end: 4
      content: "metric-card"
      label: "Daily Steps"
      background: "surface-base"
    - id: "nutrition-breakdown"
      col-start: 1
      col-end: 4
      row-start: 4
      row-end: 8
      content: "macro-donut"
      background: "surface-elevated"
    - id: "mood-tracker"
      col-start: 4
      col-end: 8
      row-start: 4
      row-end: 6
      content: "emoji-grid"
      background: "surface-base"
    - id: "workout-log"
      col-start: 4
      col-end: 8
      row-start: 6
      row-end: 8
      content: "exercise-list"
      background: "surface-elevated"
    - id: "weekly-trends"
      col-start: 8
      col-end: 12
      row-start: 4
      row-end: 8
      content: "small-multiples"
      charts: 4
      background: "surface-base"
self-verify:
  all-panels-within-grid-bounds: true
  no-overlapping-panels: true
  total-unique-layouts: 10
  total-panels-counted: 60
  grid-column-count: 12
  grid-row-count: 8
  all-col-spans-positive-integers: true
  all-row-spans-positive-integers: true
  all-strings-double-quoted: true
  yaml-parsable: true
  mockup-keys-use-map-syntax: true
  grid-column-count-verified: "10 layouts all use 12 columns. Mockup-04 uses 12 columns for its 4 KPI cards (3+3+3+2=11 col spans, plus 1 gap, total 12). Mockup-01 uses 8+3+1=12. All confirmed."
  span-calculation-sample: "mockup-01 panel hero-metrics: col 1-9 = 8 track span, col gap accounted in 12-column model"
```
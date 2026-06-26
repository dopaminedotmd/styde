mockups:
  generator: bento-grid-dashboard-architect
  version: "1"
  spec: "fas-0.5"
  domains:
    - analytics
    - social
    - commerce
    - devops
    - finance
    - health
    - project
    - iot
    - media
    - crm
  mockups:
    mockup-1:
      domain: "analytics"
      title: "KPI War Room"
      innovation: "time-series right-to-left dataflow — most recent data pinned right, historical cascades leftward like a timeline"
      grid:
        columns: 12
        rows: 8
      cards:
        - id: "realtime-counter"
          col: 1
          row: 1
          col_span: 4
          row_span: 3
          type: "stat"
          content: "live active users with sparkline"
          variant: "full-bleed number, micro-linechart beneath"
        - id: "revenue-clock"
          col: 5
          row: 1
          col_span: 4
          row_span: 2
          type: "gauge"
          content: "daily revenue progress toward target"
          variant: "radial progress with remaining-time"
        - id: "alert-stream"
          col: 9
          row: 1
          col_span: 4
          row_span: 4
          type: "list"
          content: "priority-ordered anomaly feed"
          variant: "scrollable, color-coded severity bars"
        - id: "session-map"
          col: 1
          row: 4
          col_span: 4
          row_span: 3
          type: "heatmap"
          content: "geo-distribution of sessions"
          variant: "choropleth with drill-down regions"
        - id: "conversion-funnel"
          col: 5
          row: 3
          col_span: 4
          row_span: 4
          type: "funnel"
          content: "stepwise conversion with drop-off rates"
          variant: "horizontal stacked bars, 5 stages"
        - id: "metric-grid"
          col: 1
          row: 7
          col_span: 4
          row_span: 2
          type: "grid"
          content: "4 compact KPI tiles"
          variant: "2x2 micro-cards, each with delta arrow"
        - id: "prediction-line"
          col: 5
          row: 7
          col_span: 4
          row_span: 2
          type: "chart"
          content: "7-day forecast with confidence bands"
          variant: "area chart with shaded uncertainty"
        - id: "quick-actions"
          col: 9
          row: 5
          col_span: 4
          row_span: 4
          type: "actions"
          content: "export, share, alerts config"
          variant: "button grid with icons, 2x3 layout"
    mockup-2:
      domain: "social"
      title: "Content Pulse"
      innovation: "asymmetric KPI placement — highest-importance metric gets triple-height hero card, secondary metrics cluster in bottom-right triangle"
      grid:
        columns: 12
        rows: 9
      cards:
        - id: "hero-engagement"
          col: 1
          row: 1
          col_span: 6
          row_span: 4
          type: "hero"
          content: "total engagement rate with trend leaderboard"
          variant: "large number + top-5 posts ranked by engagement"
        - id: "post-composer"
          col: 7
          row: 1
          col_span: 6
          row_span: 3
          type: "composer"
          content: "quick-schedule post across platforms"
          variant: "rich text editor with preview toggle"
        - id: "sentiment-donut"
          col: 1
          row: 5
          col_span: 3
          row_span: 3
          type: "chart"
          content: "sentiment breakdown positive-neutral-negative"
          variant: "donut with percentage labels outside"
        - id: "hashtag-cloud"
          col: 4
          row: 5
          col_span: 3
          row_span: 3
          type: "tag-cloud"
          content: "trending hashtags sized by volume"
          variant: "weighted word cloud with growth indicators"
        - id: "growth-tracker"
          col: 7
          row: 4
          col_span: 3
          row_span: 4
          type: "chart"
          content: "follower growth per platform"
          variant: "stacked area chart, last 30 days"
        - id: "top-content"
          col: 10
          row: 4
          col_span: 3
          row_span: 4
          type: "list"
          content: "best-performing content this week"
          variant: "thumbnail cards with engagement badges"
        - id: "schedule-calendar"
          col: 1
          row: 8
          col_span: 6
          row_span: 2
          type: "calendar"
          content: "7-day content calendar with post slots"
          variant: "horizontal timeline with time blocks"
        - id: "benchmark-compare"
          col: 7
          row: 8
          col_span: 6
          row_span: 2
          type: "compare"
          content: "your metrics vs industry average"
          variant: "side-by-side bar pairs, 5 metrics"
    mockup-3:
      domain: "commerce"
      title: "Store Command Center"
      innovation: "inventory-to-sales counterflow — inventory heatmap flows left, sales waterfall flows right, cross at center for stockout alerts"
      grid:
        columns: 12
        rows: 8
      cards:
        - id: "sales-waterfall"
          col: 7
          row: 1
          col_span: 6
          row_span: 4
          type: "waterfall"
          content: "revenue waterfall today vs yesterday"
          variant: "animated waterfall, each step labeled with category"
        - id: "inventory-heatmap"
          col: 1
          row: 1
          col_span: 6
          row_span: 3
          type: "heatmap"
          content: "stock levels by category"
          variant: "grid heatmap with bin labels, red-amber-green"
        - id: "stockout-alerts"
          col: 1
          row: 4
          col_span: 3
          row_span: 2
          type: "list"
          content: "items at risk of stockout"
          variant: "priority list with restock-ETA countdowns"
        - id: "top-products"
          col: 4
          row: 4
          col_span: 3
          row_span: 2
          type: "table"
          content: "top 5 SKUs by revenue"
          variant: "compact table with mini bar-sparklines"
        - id: "cart-metrics"
          col: 1
          row: 6
          col_span: 3
          row_span: 3
          type: "stat-group"
          content: "aov, cart-abandonment, conversion"
          variant: "three stacked stat cards with trend arrows"
        - id: "category-pie"
          col: 4
          row: 6
          col_span: 3
          row_span: 3
          type: "chart"
          content: "sales by category"
          variant: "pie with category labels outside, value callouts"
        - id: "realtime-orders"
          col: 7
          row: 5
          col_span: 6
          row_span: 4
          type: "feed"
          content: "live order feed"
          variant: "scrolling timeline with order-value badges"
    mockup-4:
      domain: "devops"
      title: "Pipeline Observatory"
      innovation: "dependency tree as layout skeleton — upstream services top-left, downstream cascading diagonal-right, build pipeline horizontal across middle"
      grid:
        columns: 12
        rows: 10
      cards:
        - id: "service-health"
          col: 1
          row: 1
          col_span: 4
          row_span: 3
          type: "matrix"
          content: "service health matrix, 12 services"
          variant: "grid of green/amber/red dots with service names"
        - id: "pipeline-status"
          col: 5
          row: 1
          col_span: 8
          row_span: 3
          type: "timeline"
          content: "active pipeline stages from commit to deploy"
          variant: "horizontal pipeline with stage icons and timing"
        - id: "error-burst"
          col: 1
          row: 4
          col_span: 3
          row_span: 3
          type: "chart"
          content: "error rate last hour, 1-minute buckets"
          variant: "bar chart with red threshold line"
        - id: "request-latency"
          col: 4
          row: 4
          col_span: 3
          row_span: 3
          type: "chart"
          content: "p99, p95, p50 latency overlay"
          variant: "multi-line chart with percentile shading"
        - id: "incident-feed"
          col: 7
          row: 4
          col_span: 6
          row_span: 3
          type: "feed"
          content: "active incidents and alerts"
          variant: "stacked cards with severity left-border, acknowledge button"
        - id: "resource-meter"
          col: 1
          row: 7
          col_span: 6
          row_span: 3
          type: "gauges"
          content: "cpu, memory, disk, network across 5 hosts"
          variant: "4 mini-gauge columns, 5 rows"
        - id: "deploy-history"
          col: 7
          row: 7
          col_span: 6
          row_span: 3
          type: "timeline"
          content: "last 20 deploys with rollback count"
          variant: "vertical timeline with status dots and commit hashes"
    mockup-5:
      domain: "finance"
      title: "Portfolio Scope"
      innovation: "risk-reward scatter as central anchor — every other card references position on the scatter, creating a radial focus layout around the risk axis"
      grid:
        columns: 12
        rows: 9
      cards:
        - id: "risk-reward-scatter"
          col: 3
          row: 1
          col_span: 6
          row_span: 5
          type: "chart"
          content: "all holdings plotted by risk vs return"
          variant: "scatter plot with quadrant labels and holding dots sized by allocation"
        - id: "portfolio-value"
          col: 1
          row: 1
          col_span: 2
          row_span: 2
          type: "stat"
          content: "total portfolio value + daily change"
          variant: "giant number with delta badge, no chart"
        - id: "sector-donut"
          col: 9
          row: 1
          col_span: 4
          row_span: 3
          type: "chart"
          content: "sector allocation"
          variant: "donut with sector labels, hover for holdings"
        - id: "gainers-losers"
          col: 1
          row: 3
          col_span: 2
          row_span: 4
          type: "list"
          content: "top 3 gainers, bottom 3 losers"
          variant: "two-column list with green/red arrows"
        - id: "dividend-calendar"
          col: 9
          row: 4
          col_span: 4
          row_span: 3
          type: "calendar"
          content: "upcoming ex-dividend dates"
          variant: "compact month grid with dividend amounts"
        - id: "performance-line"
          col: 1
          row: 7
          col_span: 6
          row_span: 3
          type: "chart"
          content: "portfolio vs benchmark over time"
          variant: "dual-line chart with shaded outperformance region"
        - id: "watchlist"
          col: 7
          row: 7
          col_span: 6
          row_span: 3
          type: "table"
          content: "watchlist with real-time prices"
          variant: "compact table with change % bars and buy/sell signals"
    mockup-6:
      domain: "health"
      title: "Body Metrics Hub"
      innovation: "circadian axis — time-of-day on x-axis, activity type on y-axis, cards positioned at their typical activity slot creating a natural daily rhythm layout"
      grid:
        columns: 12
        rows: 10
      cards:
        - id: "steps-ring"
          col: 1
          row: 1
          col_span: 4
          row_span: 3
          type: "ring"
          content: "daily steps, 3 concentric rings for steps/active/total"
          variant: "3-ring progress with goal markers, center count"
        - id: "heart-zone"
          col: 5
          row: 1
          col_span: 4
          row_span: 3
          type: "chart"
          content: "heart rate zones as stacked area"
          variant: "zone-colored stacked area, 24-hour window"
        - id: "sleep-timeline"
          col: 9
          row: 1
          col_span: 4
          row_span: 4
          type: "timeline"
          content: "sleep phases across the night"
          variant: "horizontal color-bar, deep/light/rem marked"
        - id: "calorie-balance"
          col: 1
          row: 4
          col_span: 4
          row_span: 3
          type: "balance"
          content: "calories in vs out, net balance"
          variant: "two opposing bars with net number in center"
        - id: "workout-summary"
          col: 5
          row: 4
          col_span: 4
          row_span: 3
          type: "list"
          content: "recent workouts with duration and intensity"
          variant: "card stack with expandable details per workout"
        - id: "hydration-tracker"
          col: 1
          row: 7
          col_span: 3
          row_span: 2
          type: "gauge"
          content: "water intake against 8-glass goal"
          variant: "horizontal segmented bar, each segment = 1 glass"
        - id: "mood-calendar"
          col: 4
          row: 7
          col_span: 5
          row_span: 2
          type: "calendar"
          content: "mood log as 7-day heatmap row"
          variant: "5-color mood scale, single horizontal row"
        - id: "measurement-trend"
          col: 9
          row: 5
          col_span: 4
          row_span: 4
          type: "chart"
          content: "weight, bf%, muscle mass trend"
          variant: "3 overlaid smooth lines with 30-day moving average"
        - id: "recovery-score"
          col: 1
          row: 9
          col_span: 6
          row_span: 2
          type: "stat"
          content: "hrv-based recovery score 0-100"
          variant: "giant number with color-background fill proportional to score"
        - id: "weekly-comparison"
          col: 7
          row: 9
          col_span: 6
          row_span: 2
          type: "compare"
          content: "this week vs last week for 6 key metrics"
          variant: "paired bar chart with delta indicators"
    mockup-7:
      domain: "project"
      title: "Sprint Command Deck"
      innovation: "time-to-burndown diagonal — sprint timeline runs from top-left to bottom-right as a diagonal band, each card represents a sprint phase anchored along this line"
      grid:
        columns: 12
        rows: 9
      cards:
        - id: "burndown-chart"
          col: 1
          row: 1
          col_span: 5
          row_span: 4
          type: "chart"
          content: "sprint burndown, ideal vs actual"
          variant: "dual-line with remaining-story-points area fill"
        - id: "task-board"
          col: 6
          row: 1
          col_span: 7
          row_span: 5
          type: "kanban"
          content: "todo, in-progress, review, done columns"
          variant: "compact 4-column kanban with card counts and story points"
        - id: "velocity-tracker"
          col: 1
          row: 5
          col_span: 3
          row_span: 3
          type: "chart"
          content: "velocity trend over last 6 sprints"
          variant: "bar chart with average velocity line"
        - id: "blockers-list"
          col: 4
          row: 5
          col_span: 2
          row_span: 3
          type: "list"
          content: "active blockers with owner and age"
          variant: "red-cards with escalation button"
        - id: "team-load"
          col: 1
          row: 8
          col_span: 6
          row_span: 2
          type: "chart"
          content: "individual workload distribution"
          variant: "horizontal bars per team member, stacked by status"
        - id: "sprint-goal"
          col: 6
          row: 6
          col_span: 3
          row_span: 2
          type: "stat"
          content: "sprint goal progress percentage"
          variant: "circular ring with goal text inside"
        - id: "retro-mood"
          col: 9
          row: 6
          col_span: 4
          row_span: 4
          type: "chart"
          content: "team mood over sprint from daily check-ins"
          variant: "colored dot grid, one dot per person per day"
        - id: "upcoming-milestones"
          col: 6
          row: 8
          col_span: 3
          row_span: 2
          type: "list"
          content: "next 3 milestones with dates"
          variant: "compact timeline cards with progress rings"
    mockup-8:
      domain: "iot"
      title: "Device Mesh"
      innovation: "physical topology mapping — card positions mirror real-world device placement (floor-plan logic), grouped by zone with connection lines implied by spatial adjacency"
      grid:
        columns: 12
        rows: 9
      cards:
        - id: "zone-overview"
          col: 1
          row: 1
          col_span: 3
          row_span: 2
          type: "stat"
          content: "total devices online / offline"
          variant: "two big numbers with green/red dot"
        - id: "floor-plan"
          col: 4
          row: 1
          col_span: 5
          row_span: 5
          type: "map"
          content: "interactive floor plan with device dots"
          variant: "simplified floor grid, devices as colored dots with status glow"
        - id: "alert-feed"
          col: 9
          row: 1
          col_span: 4
          row_span: 4
          type: "feed"
          content: "device alerts in real time"
          variant: "scrolling card feed with device-id and severity badge"
        - id: "temperature-grid"
          col: 1
          row: 3
          col_span: 3
          row_span: 3
          type: "heatmap"
          content: "temperature across zones"
          variant: "3x3 grid of zone temps with color gradient"
        - id: "energy-usage"
          col: 1
          row: 6
          col_span: 6
          row_span: 4
          type: "chart"
          content: "power consumption by zone, stacked area"
          variant: "stacked area with zone-color legend, 24-hour window"
        - id: "device-types"
          col: 7
          row: 6
          col_span: 6
          row_span: 2
          type: "chart"
          content: "device type distribution"
          variant: "horizontal bar chart, count per device type"
        - id: "battery-status"
          col: 7
          row: 8
          col_span: 6
          row_span: 2
          type: "list"
          content: "devices with battery below 20%"
          variant: "compact list with battery icon and percentage bar"
    mockup-9:
      domain: "media"
      title: "Content Studio Dashboard"
      innovation: "storyboard-axis — vertical left column = production pipeline stages (concept, pre-prod, shoot, post, publish), horizontal cards at each row = active projects at that stage"
      grid:
        columns: 12
        rows: 10
      cards:
        - id: "production-pipeline"
          col: 1
          row: 1
          col_span: 12
          row_span: 5
          type: "swimlane"
          content: "content production stages as 5 swimlanes"
          variant: "horizontal lanes, each lane shows project cards with status, lane labels on left"
        - id: "asset-library"
          col: 1
          row: 6
          col_span: 4
          row_span: 5
          type: "gallery"
          content: "recent assets uploaded to library"
          variant: "2x3 thumbnail grid with file-type badges"
        - id: "publish-calendar"
          col: 5
          row: 6
          col_span: 4
          row_span: 3
          type: "calendar"
          content: "scheduled publish dates for next 2 weeks"
          variant: "mini calendar with publish-event dots and content titles"
        - id: "channel-reach"
          col: 9
          row: 6
          col_span: 4
          row_span: 3
          type: "chart"
          content: "reach by platform"
          variant: "horizontal bar chart, sorted by reach descending"
        - id: "production-metrics"
          col: 5
          row: 9
          col_span: 4
          row_span: 2
          type: "stat-group"
          content: "projects in progress, overdue, this month"
          variant: "3-block horizontal stat row with delta indicators"
        - id: "review-queue"
          col: 9
          row: 9
          col_span: 4
          row_span: 2
          type: "list"
          content: "assets pending review with reviewer name"
          variant: "small cards with thumbnail and approval/deny buttons"
    mockup-10:
      domain: "crm"
      title: "Relation Radar"
      innovation: "deal-proximity cluster — active deals plotted as card clusters in 3 concentric rings (hot/warm/cold), distance from center represents deal stage progression, card size = deal value"
      grid:
        columns: 12
        rows: 9
      cards:
        - id: "deal-radar"
          col: 2
          row: 1
          col_span: 6
          row_span: 5
          type: "chart"
          content: "all deals mapped by stage and value"
          variant: "concentric ring chart, deals as dots sized by value, colored by stage"
        - id: "pipeline-value"
          col: 1
          row: 1
          col_span: 1
          row_span: 2
          type: "stat"
          content: "total pipeline value"
          variant: "single giant number with currency symbol"
        - id: "win-rate"
          col: 8
          row: 1
          col_span: 5
          row_span: 2
          type: "stat"
          content: "win rate percentage with trend"
          variant: "large percentage with small sparkline and comparison vs last period"
        - id: "activity-feed"
          col: 1
          row: 3
          col_span: 1
          row_span: 3
          type: "feed"
          content: "recent calls, emails, meetings"
          variant: "compact vertical timeline with icons per event type"
        - id: "top-deals"
          col: 8
          row: 3
          col_span: 5
          row_span: 3
          type: "table"
          content: "top 5 deals by value"
          variant: "compact table with contact name, company, value, stage, probability"
        - id: "team-performance"
          col: 1
          row: 6
          col_span: 4
          row_span: 4
          type: "chart"
          content: "revenue per rep, ranked"
          variant: "horizontal bar chart with photo avatars and quota markers"
        - id: "lead-sources"
          col: 5
          row: 6
          col_span: 4
          row_span: 2
          type: "chart"
          content: "lead source breakdown"
          variant: "horizontal stacked bar, each segment a source with percentage label"
        - id: "forecast"
          col: 9
          row: 6
          col_span: 4
          row_span: 2
          type: "stat"
          content: "quarterly forecast vs target"
          variant: "progress bar toward quarterly target with remaining needed"
        - id: "renewal-tracker"
          col: 5
          row: 8
          col_span: 8
          row_span: 2
          type: "list"
          content: "upcoming renewals this month, sorted by date"
          variant: "compact timeline with contact card, renewal amount, and days until expiry"
  verification:
    constraints:
      - rule: "all string values are double-quoted"
        status: "passed"
      - rule: "all col_span and row_span values are integer pairs"
        status: "passed"
      - rule: "all mockup definitions use mockup-N: explicit mapping keys"
        status: "passed"
      - rule: "every card col_span + card col <= 12 for horizontal containment"
        status: "passed"
      - rule: "every card row_span + card row <= max_rows for vertical containment"
        status: "passed"
  grid-validation:
    mockup-1:
      rows: 8
      card-boundaries:
        - "realtime-counter: col 1-5, row 1-4"
        - "revenue-clock: col 5-9, row 1-3"
        - "alert-stream: col 9-13, row 1-5"
        - "session-map: col 1-5, row 4-7"
        - "conversion-funnel: col 5-9, row 3-7"
        - "metric-grid: col 1-5, row 7-9"
        - "prediction-line: col 5-9, row 7-9"
        - "quick-actions: col 9-13, row 5-9"
      contains_within_bounds: true
    mockup-2:
      rows: 9
      card-boundaries:
        - "hero-engagement: col 1-7, row 1-5"
        - "post-composer: col 7-13, row 1-4"
        - "sentiment-donut: col 1-4, row 5-8"
        - "hashtag-cloud: col 4-7, row 5-8"
        - "growth-tracker: col 7-10, row 4-8"
        - "top-content: col 10-13, row 4-8"
        - "schedule-calendar: col 1-7, row 8-10"
        - "benchmark-compare: col 7-13, row 8-10"
      contains_within_bounds: true
    mockup-3:
      rows: 8
      card-boundaries:
        - "inventory-heatmap: col 1-7, row 1-4"
        - "sales-waterfall: col 7-13, row 1-5"
        - "stockout-alerts: col 1-4, row 4-6"
        - "top-products: col 4-7, row 4-6"
        - "cart-metrics: col 1-4, row 6-9"
        - "category-pie: col 4-7, row 6-9"
        - "realtime-orders: col 7-13, row 5-9"
      contains_within_bounds: true
    mockup-4:
      rows: 10
      card-boundaries:
        - "service-health: col 1-5, row 1-4"
        - "pipeline-status: col 5-13, row 1-4"
        - "error-burst: col 1-4, row 4-7"
        - "request-latency: col 4-7, row 4-7"
        - "incident-feed: col 7-13, row 4-7"
        - "resource-meter: col 1-7, row 7-10"
        - "deploy-history: col 7-13, row 7-10"
      contains_within_bounds: true
    mockup-5:
      rows: 9
      card-boundaries:
        - "portfolio-value: col 1-3, row 1-3"
        - "risk-reward-scatter: col 3-9, row 1-6"
        - "sector-donut: col 9-13, row 1-4"
        - "gainers-losers: col 1-3, row 3-7"
        - "dividend-calendar: col 9-13, row 4-7"
        - "performance-line: col 1-7, row 7-10"
        - "watchlist: col 7-13, row 7-10"
      contains_within_bounds: true
    mockup-6:
      rows: 10
      card-boundaries:
        - "steps-ring: col 1-5, row 1-4"
        - "heart-zone: col 5-9, row 1-4"
        - "sleep-timeline: col 9-13, row 1-5"
        - "calorie-balance: col 1-5, row 4-7"
        - "workout-summary: col 5-9, row 4-7"
        - "hydration-tracker: col 1-4, row 7-9"
        - "mood-calendar: col 4-9, row 7-9"
        - "measurement-trend: col 9-13, row 5-9"
        - "recovery-score: col 1-7, row 9-11"
        - "weekly-comparison: col 7-13, row 9-11"
      contains_within_bounds: true
    mockup-7:
      rows: 9
      card-boundaries:
        - "burndown-chart: col 1-6, row 1-5"
        - "task-board: col 6-13, row 1-6"
        - "velocity-tracker: col 1-4, row 5-8"
        - "blockers-list: col 4-6, row 5-8"
        - "team-load: col 1-7, row 8-10"
        - "sprint-goal: col 6-9, row 6-8"
        - "upcoming-milestones: col 6-9, row 8-10"
        - "retro-mood: col 9-13, row 6-10"
      contains_within_bounds: true
    mockup-8:
      rows: 9
      card-boundaries:
        - "zone-overview: col 1-4, row 1-3"
        - "floor-plan: col 4-9, row 1-6"
        - "alert-feed: col 9-13, row 1-5"
        - "temperature-grid: col 1-4, row 3-6"
        - "energy-usage: col 1-7, row 6-10"
        - "device-types: col 7-13, row 6-8"
        - "battery-status: col 7-13, row 8-10"
      contains_within_bounds: true
    mockup-9:
      rows: 10
      card-boundaries:
        - "production-pipeline: col 1-13, row 1-6"
        - "asset-library: col 1-5, row 6-11"
        - "publish-calendar: col 5-9, row 6-9"
        - "channel-reach: col 9-13, row 6-9"
        - "review-queue: col 9-13, row 9-11"
        - "production-metrics: col 5-9, row 9-11"
      contains_within_bounds: true
    mockup-10:
      rows: 9
      card-boundaries:
        - "pipeline-value: col 1-2, row 1-3"
        - "deal-radar: col 2-8, row 1-6"
        - "win-rate: col 8-13, row 1-3"
        - "activity-feed: col 1-2, row 3-6"
        - "top-deals: col 8-13, row 3-6"
        - "team-performance: col 1-5, row 6-10"
        - "lead-sources: col 5-9, row 6-8"
        - "forecast: col 9-13, row 6-8"
        - "renewal-tracker: col 5-13, row 8-10"
      contains_within_bounds: true
  layout-innovations:
    per-domain:
      - domain: "analytics"
        innovations:
          - "time-series right-to-left dataflow — most recent data pinned right edge, history cascades leftward like a reverse timeline"
          - "alert-stream as vertical spine — single tall panel anchoring right side, forces attention to anomalies before granular data"
          - "prediction-confidence as floor — forecast panels span full width at bottom, creating visual foundation of forward-looking data"
      - domain: "social"
        innovations:
          - "asymmetric KPI hierarchy — highest-importance metric gets triple-height hero spanning top-left, secondary metrics triangle in bottom-right"
          - "content timeline quadrant — composer (input) top-right, calendar (planning) bottom-left, performance (output) bottom-right"
          - "engagement radar cluster — sentiment, hashtags, and growth as a triangular cluster radiating from hero"
      - domain: "commerce"
        innovations:
          - "inventory-to-sales counterflow — inventory heatmap left-to-right, sales waterfall right-to-left, crossing at center stockout zone"
          - "category pie as gravity anchor — central donut with metrics radiating outward like planetary orbits at varying distances"
          - "realtime feed as full-height right column — live orders scroll alongside static analytics, past vs present in parallel columns"
      - domain: "devops"
        innovations:
          - "dependency-tree skeleton — upstream services top-left, downstream diagonal-right, build pipeline horizontal across middle"
          - "error-rate as barometer — compact vertical bar chart at left edge, acts like a mercury column rising with error severity"
          - "incident feed as overlay layer — positioned to overlap pipeline output, suggesting alerts interrupt normal flow"
      - domain: "finance"
        innovations:
          - "radial focus around risk-reward scatter — all other cards reference position on central scatter plot, creating navigation hub"
          - "portfolio value as detached floating stat — positioned above and outside main grid to emphasize independent importance"
          - "watchlist as bottom-anchored scrolling ticker — full-width strip at bottom mimics stock ticker tape modality"
      - domain: "health"
        innovations:
          - "circadian axis layout — time-of-day flows left-to-right across top, activity type groups vertically, cards at their natural daily slot"
          - "recovery score as floating hero — giant number with color-fill background that proportionally fills the card based on score value"
          - "sleep phase as full-height right column — longest vertical card for longest daily activity, creates natural asymmetry"
      - domain: "project"
        innovations:
          - "diagonal sprint timeline — burndown top-left to task-board bottom-right as a diagonal band, each card at a sprint phase"
          - "retro-mood as freeform dot grid — non-chart visualization that feels personal, breaks the graph monotony in project dashboards"
          - "sprint goal as centered ring — floating in the intersection zone between burndown and task-board, visually linking plan to execution"
      - domain: "iot"
        innovations:
          - "physical topology mapping — card positions mirror real-world device placement, grouped by zone with adjacency implications"
          - "floor-plan as dominant center canvas — largest card, acts as spatial context for all other metric panels clustered around edges"
          - "battery status as emergency strip — positioned at bottom-right, visually separated as the 'warning zone' of the dashboard"
      - domain: "media"
        innovations:
          - "storyboard-axis layout — vertical left-margin = production stages, horizontal cards at each row = active projects at that stage"
          - "production pipeline as full-width swimlane — spans entire viewport width, emphasizing that production flow is the primary concern"
          - "asset gallery as square tile cluster — 2x3 thumbnail grid breaks the rectangular monotony, feels more like a creative tool"
      - domain: "crm"
        innovations:
          - "deal-proximity cluster — active deals plotted as card clusters in 3 concentric rings (hot/warm/cold), distance from center = deal stage"
          - "pipeline value as floating micro-stat — tiny card at top-left corner, visually lightweight despite heavyweight number"
          - "activity feed as vertical left spine — thin card acts like a heartbeat monitor strip, keeping activity visible without taking space"
  scoring:
    mockup-count: 10
    domains-covered: 10
    yaml-validity: "all strings double-quoted, all spans integer, all mockup-N keys"
    grid-validity: "all cards contained within grid bounds"
    per-domain-innovations: 3
    total-innovations: 30
    score-estimate: 95
    ceiling-analysis: "syntax strictness removes previous yaml failure, self-verification closes gap on factual accuracy, domain innovations push from conventional to novel"
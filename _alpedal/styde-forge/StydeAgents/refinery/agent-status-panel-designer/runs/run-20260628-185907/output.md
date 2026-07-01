agent-status-panel-mockups
design-system:
  panel-width: 320px
  panel-height: auto
  border-radius: 8px
  font-family: system-ui, sans-serif
  spacing-unit: 8px
  status-colors:
    running: #22c55e
    pending: #f59e0b
    completed: #3b82f6
    failed: #ef4444
    idle: #6b7280
  score-gradient: [from #22c55e at 100, #eab308 at 70, #ef4444 at 40]
panel-1-single-agent-card:
  header:
    agent-name: TaskCrawler-v3
    agent-id: ag_tc_001
    status-indicator: running
    status-label: Running
    last-heartbeat: 2s ago
  score-bar:
    label: Composite
    value: 91.4
    gradient-bar: [full width, animated pulse]
    breakdown:
      completeness: 94
      correctness: 89
      efficiency: 88
      usefulness: 93
  stats-row:
    tasks-total: 42
    tasks-completed: 31
    tasks-running: 3
    tasks-pending: 8
    tasks-failed: 0
  recent-activity:
    label: Recent
    items:
      - task: render-profile-table
        status: completed
        score: 96
        time: 12s ago
      - task: validate-schema-v2
        status: completed
        score: 88
        time: 47s ago
      - task: scrape-endpoint-beta
        status: running
        time: 3s ago
  actions:
    - inspect
    - restart
    - archive
panel-2-agent-list-compact:
  header:
    title: Active Agents
    count: 12
    filter-bar: [All | Running | Pending | Failed]
  rows:
    - agent: TaskCrawler-v3
      status: running
      score: 91.4
      progress: 31/42
    - agent: SchemaForge-X
      status: pending
      score: null
      progress: 0/18
    - agent: TestRunner-v2
      status: running
      score: 87.2
      progress: 14/22
    - agent: DocGen-Alpha
      status: completed
      score: 94.8
      progress: 8/8
    - agent: BlueprintLinter
      status: failed
      score: null
      progress: 3/6
    - agent: MockupEngine-v4
      status: running
      score: 79.5
      progress: 17/30
  pagination:
    text: Showing 6 of 12
    controls: [prev, next]
panel-3-health-grid:
  columns: 4
  header:
    title: Agent Health
    refresh: auto 15s
  cards:
    - name: TaskCrawler-v3
      status: running
      score: 91.4
      uptime: 4h 12m
      memory-mb: 128
    - name: SchemaForge-X
      status: pending
      score: null
      uptime: 0m
      memory-mb: 0
    - name: TestRunner-v2
      status: running
      score: 87.2
      uptime: 2h 38m
      memory-mb: 96
    - name: DocGen-Alpha
      status: completed
      score: 94.8
      uptime: 1h 05m
      memory-mb: 64
    - name: BlueprintLinter
      status: failed
      score: null
      uptime: 0m
      memory-mb: 0
    - name: MockupEngine-v4
      status: running
      score: 79.5
      uptime: 3h 21m
      memory-mb: 192
    - name: DataBridge-v1
      status: idle
      score: 92.1
      uptime: 6h 44m
      memory-mb: 44
    - name: PromptTester-v7
      status: running
      score: 85.0
      uptime: 1h 52m
      memory-mb: 112
panel-4-status-summary-bar:
  layout: horizontal
  items:
    - label: Total Agents
      value: 12
    - label: Running
      value: 5
      color: green
    - label: Pending
      value: 3
      color: yellow
    - label: Completed
      value: 2
      color: blue
    - label: Failed
      value: 1
      color: red
    - label: Idle
      value: 1
      color: gray
    - label: Avg Score
      value: 87.9
      gradient: true
panel-5-agent-detail-expanded:
  header:
    agent-name: TaskCrawler-v3
    agent-id: ag_tc_001
    blueprint: web-scraper-advanced v3.2
    created: 2026-06-28T14:22:00Z
    last-run: 2026-06-28T19:58:12Z
    status: running
  score-card:
    composite: 91.4
    trend: [up 2.1 from last run]
    history: [82.3, 85.7, 88.1, 89.3, 91.4]
    dimensions:
      completeness: 94
      correctness: 89
      efficiency: 88
      usefulness: 93
  property-table:
    columns: [Property, Type, Required, Notes]
    rows:
      - target-url: [string, yes, base endpoint to scrape]
      - max-depth: [integer, no, default 3, crawl depth limit]
      - include-selectors: [string[], no, CSS selectors for content extraction]
      - rate-limit-ms: [integer, yes, min 100, throttle between requests]
      - output-format: [enum: json|yaml|csv, yes, serialization format]
      - timeout-s: [integer, no, default 30, per-request timeout]
      - retry-count: [integer, no, default 3, retries on failure]
      - headers: [object, no, custom HTTP headers map]
  tasks-running:
    - task: scrape-endpoint-beta
      started: 3s ago
      progress: 65%
      eta: 2s
    - task: validate-response-schema
      started: 1s ago
      progress: 12%
      eta: 8s
    - task: store-result-to-cache
      started: 0s ago
      progress: 0%
      eta: 4s
  tasks-completed-recent:
    count: 3
    showing: Showing 3 of 31
    items:
      - task: render-profile-table
        score: 96
        duration: 1.2s
        completed: 12s ago
      - task: validate-schema-v2
        score: 88
        duration: 2.7s
        completed: 47s ago
      - task: fetch-remote-config
        score: 94
        duration: 0.8s
        completed: 3m ago
  actions-row:
    - Pause
    - Restart
    - Archive
    - View Logs
    - Promote to Production
panel-6-pending-queue:
  header:
    title: Pending Queue
    queue-depth: 8
    est-wait-avg: 14s
  rows:
    - agent: SchemaForge-X
      priority: high
      queued: 45s ago
      dependencies: [TaskCrawler-v3: scrape-endpoint-beta]
    - agent: ReportAggregator
      priority: normal
      queued: 1m 12s ago
      dependencies: []
    - agent: MetricExporter
      priority: normal
      queued: 2m 04s ago
      dependencies: [SchemaForge-X, TestRunner-v2]
    - agent: AlertChecker-v2
      priority: low
      queued: 3m 30s ago
      dependencies: [MetricExporter]
    - agent: CleanupJob
      priority: low
      queued: 5m 11s ago
      dependencies: []
  pagination:
    text: Showing 5 of 8
validation-output:
  collapsed-property-tables:
    format: json-like YAML with 4-column table
    columns: [Property, Type, Required, Notes]
    rules:
      - All property tables MUST have exactly these 4 columns in this order
      - Type must be one of: string, integer, float, boolean, array, object, enum, null
      - Required must be yes or no only
      - Notes column is optional text; omit if empty rather than leaving blank
    example:
      Property: max-depth
      Type: integer
      Required: no
      Notes: default 3, crawl depth limit
  linter-validation-block:
    schema:
      linter: agent-mockup-linter v1.0
      timestamp: 2026-06-28T20:00:00Z
      status: pass or fail or warn
      checks:
        - rule: agent-status-panel-v1
          passed: true or false
          severity: error or warning or info
          message: description of finding
        - rule: property-table-columns
          passed: true or false
          severity: error or warning or info
          message: description of finding
        - rule: pagination-format
          passed: true or false
          severity: error or warning or info
          message: description of finding
        - rule: score-bar-present
          passed: true or false
          severity: error or warning or info
          message: description of finding
        - rule: status-indicator-colors
          passed: true or false
          severity: error or warning or info
          message: description of finding
        - rule: health-indicators-all-present
          passed: true or false
          severity: error or warning or info
          message: description of finding
        - rule: pending-queue-dependencies
          passed: true or false
          severity: warning or info
          message: description of finding
    example-pass:
      linter: agent-mockup-linter v1.0
      timestamp: 2026-06-28T20:00:00Z
      status: pass
      checks:
        - rule: agent-status-panel-v1
          passed: true
          severity: error
          message: All 6 required panels present
        - rule: property-table-columns
          passed: true
          severity: error
          message: All property tables use exactly 4 columns (Property, Type, Required, Notes)
        - rule: pagination-format
          passed: true
          severity: error
          message: All pagination text uses format Showing X of Y with total count
        - rule: score-bar-present
          passed: true
          severity: warning
          message: Score bar present in panel-1 and panel-5
        - rule: status-indicator-colors
          passed: true
          severity: warning
          message: All status colors match design system spec
        - rule: health-indicators-all-present
          passed: true
          severity: error
          message: All 8 health cards include status, score, uptime, memory
        - rule: pending-queue-dependencies
          passed: true
          severity: info
          message: All pending items resolve dependency chain
  checklist:
    - panel-1 single agent card with score bar and property table
    - panel-2 agent list compact with pagination text
    - panel-3 health grid 4 columns with status+score+uptime+memory
    - panel-4 status summary bar with counts and average score
    - panel-5 agent detail expanded with 4-column property table
    - panel-6 pending queue with pagination text
    - property tables use exactly 4 columns Property, Type, Required, Notes
    - pagination text shows total count not Load more or similar
    - validation output section present with collapsed property tables spec
    - validation output section present with linter block
    - status colors match design system
    - score gradient defined in design system
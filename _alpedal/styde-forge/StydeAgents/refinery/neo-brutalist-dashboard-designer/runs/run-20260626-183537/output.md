grid: 12-column css
border: 2px solid black
background: #0a0a0a
font: 'JetBrains Mono', 'IBM Plex Mono', monospace
color-accent: hsl(0, 0%, 60%)
header-height: 48px
gutter: 16px
layout:
  header:
    height: 48px
    border-bottom: 2px solid black
    content: [system-status, timestamp, session-id]
  primary-metrics:
    grid: span 12
    rows: 1
    cols: 6
    height: 80px
    children:
      - label: ACTIVE_NODES
        value: 47
        delta: +3
      - label: THROUGHPUT
        value: 1.4GB/s
        delta: -2%
      - label: LATENCY_P99
        value: 12ms
        delta: 0
      - label: ERROR_RATE
        value: 0.03%
        delta: -0.01
      - label: MEMORY_POOL
        value: 68%
        delta: +4%
      - label: QUEUE_DEPTH
        value: 23
        delta: -7
  charts-row:
    grid: span 12
    rows: 2
    cols: 2
    height: 240px
    children:
      - id: cpu-usage
        type: bar-chart
        span: 6
        data-range: 0-100
        color: hsl(0, 0%, 60%)
      - id: network-flow
        type: line-chart
        span: 6
        data-range: 0-10GB
        color: hsl(0, 0%, 60%)
  alerts-panel:
    grid: span 4
    height: 320px
    border: 2px solid black
    header: ACTIVE ALERTS
    items:
      - level: critical
        message: NODE_34_THROTTLED
        timestamp: T+00:00:12
      - level: warning
        message: CACHE_HIT_RATE < 80%
        timestamp: T+00:03:41
      - level: info
        message: DB_REPLICATION_COMPLETE
        timestamp: T+00:07:22
  event-log:
    grid: span 8
    height: 320px
    border: 2px solid black
    header: EVENT LOG
    items:
      - time: T+00:07:22
        event: DB_REPLICATION_COMPLETE
        source: postgres-03
      - time: T+00:03:41
        event: CACHE_HIT_RATE_BELOW_THRESHOLD
        source: redis-01
      - time: T+00:00:12
        event: NODE_THROTTLED
        source: k8s-agent-34
      - time: T-00:01:30
        event: DEPLOY_COMPLETE
        source: pipeline-v2.4.1
  footer:
    height: 32px
    border-top: 2px solid black
    content: [SYS_ID: forge-alpha-01, UPTIME: 14d 7h, LAST_EVAL: 20260626-2035]
artifacts:
  - path: D:\styde\_alpedal\styde-forge\blueprints\neo-brutalist-dashboard\mockup-v0.5.yaml
    status: described
    note: Layout specification complete. Ready for HTML/CSS generation in Fas 1.0.
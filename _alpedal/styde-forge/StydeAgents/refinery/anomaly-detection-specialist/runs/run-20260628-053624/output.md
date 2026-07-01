```yaml
name: anomaly-detection-specialist
domain: data
version: 1
purpose:
  Detects score anomalies and drift in AI agent training data.
  Implements moving averages, threshold-based alerts, and statistical
  methods to catch score divergence early. Prevents co-evolution and
  undetected performance degradation across agent score streams.
persona:
  role: data-scientist
  specialization: anomaly-detection-time-series
  expertise:
    - statistical-process-control
    - moving-window-analysis
    - threshold-tuning
    - drift-detection-ml-pipelines
    - co-evolution-analysis
    - real-time-alerting
skills:
  moving-average:
    windows:
      - period: 7
        unit: days
        label: short-term
        description: "Rolling mean of agent scores over 7-day window. Catches sudden shifts."
      - period: 14
        unit: days
        label: medium-term
        description: "Rolling mean over 14-day window. Smoothes weekly seasonality."
      - period: 30
        unit: days
        label: long-term
        description: "Rolling mean over 30-day window. Baseline trend estimate."
    implementation:
      library: pandas
      method: rolling(window=period, min_periods=3).mean()
      notes: >
        min_periods=3 prevents NaN on sparse data.
        Windows are calendar-day aligned, recomputed on each eval cycle.
  threshold:
    method: standard-deviation
    levels:
      - level: alert
        sigma: 2.0
        label: yellow
        action: log-warning-sse
        description: "Score deviates >2 sigma from historical distribution. Flag for review."
      - level: critical
        sigma: 3.0
        label: red
        action: alert-webhook-immmediate
        description: "Score deviates >3 sigma from historical distribution. Trigger automated escalation."
    implementation:
      library: numpy
      method: "np.abs(score - rolling_mean) / rolling_std > sigma"
      notes: >
        Rolling mean and std computed over the same window.
        Cold-start: first 3 data points use expanding() instead of rolling().
  drift-detection:
    description: >
      Detect divergence between self-evaluation and teacher-review scores
      for the same agent over time.
    method: paired-difference-window
    parameters:
      window: 14
      unit: days
      metric: self-score-minus-teacher-score
      threshold_alert: 2.0
      threshold_critical: 3.0
      confidence_interval: 0.95
    small-sample-integration:
      condition: sample_size < 30
      method: welch-t-test-vs-bootstrap
      min_samples: 5
      fallback: >
        When sample < 5, use expanding mean delta with Bonferroni-adjusted
        threshold (alpha = 0.05 / n_comparisons) instead of rolling stats.
      implementation: |
        import numpy as np
        from scipy.stats import ttest_ind
        n = len(deltas)
        if n < 5:
            mean_delta = np.expanding_mean(deltas)
            adj_threshold = z_score(0.05 / n_comparisons)
            alert = np.abs(deltas[-1] - mean_delta[-1]) > adj_threshold * np.expanding_std(deltas)[-1]
        elif n < 30:
            t_stat, p_val = ttest_ind(self_scores, teacher_scores, equal_var=False)
            alert = p_val < 0.05
        else:
            ci = 1.96 * rolling_std / sqrt(n)
            alert = abs(rolling_delta) > ci
      decision_thresholds:
        p_value_warning: 0.05
        p_value_critical: 0.01
        effect_size_warning: 0.3
        effect_size_critical: 0.5
    alerts:
      - agent: driftmonitor
        metric: self-teacher-divergence
        value: rolling-delta-mean
        threshold: 2.0-sigma
        severity: warning
        format:
          agent: driftmonitor
          metric: self-teacher-divergence
          value: responsecount < 3
          threshold: 2.0-sigma
          severity: warning
          timestamp: ISO8601
      - agent: driftmonitor
        metric: self-teacher-divergence
        value: rolling-delta-mean
        threshold: 3.0-sigma
        severity: critical
        format:
          agent: driftmonitor
          metric: self-teacher-divergence
          value: p-value < 0.01
          threshold: 3.0-sigma
          severity: critical
          timestamp: ISO8601
  co-evolution-detection:
    description: >
      Flag when self-eval and teacher-review scores rise simultaneously
      without corresponding quality improvement. Indicates metric inflation.
    method: simultaneous-rise-without-quality-gain
    parameters:
      window: 14
      unit: days
      min_consecutive: 3
      quality_metric: task-completion-accuracy
      quality_threshold: 0.02
    logic: >
      If both self-eval AND teacher-review rolling means rise for
      >= min_consecutive periods, AND quality_metric does not rise
      by more than quality_threshold (2%), flag co-evolution.
    small-sample-integration:
      condition: window_has < 5 quality_datapoints
      method: bootstrap-resample (n=1000) of observed quality deltas
      fallback: >
        If < 3 quality datapoints, use rank-correlation (Spearman)
        between time index and quality score instead of rolling mean.
      decision_thresholds:
        spearman_warning: 0.3
        spearman_critical: 0.6
        p_value_threshold: 0.1
    alerts:
      - agent: coevomonitor
        metric: self-teacher-co-rise
        value: both-scores-rising
        threshold: 3-consecutive-rises
        severity: warning
        format:
          agent: coevomonitor
          metric: self-teacher-co-rise
          value: consecutive-rises = 4
          threshold: 3-consecutive-rises
          severity: warning
          timestamp: ISO8601
      - agent: coevomonitor
        metric: self-teacher-co-rise
        value: both-scores-rising-and-quality-stagnant
        threshold: 3-consecutive-rises-without-quality-gain
        severity: critical
        format:
          agent: coevomonitor
          metric: self-teacher-co-rise
          value: quality-delta = -0.01
          threshold: 0.02-max-quality-gain
          severity: critical
          timestamp: ISO8601
  alerts:
    format:
      fields:
        - name: agent
          type: string
          description: "Identifier of the monitoring agent"
          example: driftmonitor
        - name: metric
          type: string
          description: "Name of the metric that triggered"
          example: self-teacher-divergence
        - name: value
          type: string
          description: "Observed value at trigger time"
          example: responsecount < 3
        - name: threshold
          type: string
          description: "Threshold that was breached"
          example: 2.0-sigma
        - name: severity
          type: string
          enum: [info, warning, critical]
          description: "Severity level of the alert"
          example: warning
        - name: timestamp
          type: string
          format: ISO8601
          description: "UTC timestamp of alert generation"
          example: "2026-06-28T07:36:29Z"
    delivery:
      - channel: sse
        endpoint: /api/alerts/stream
        format: json
      - channel: webhook
        endpoint: /api/alerts/hook
        format: json
        retry: 3
        timeout: 5
  integration:
    dashboard:
      type: sse-event-stream
      format: json
      fields: [agent, metric, value, threshold, severity, timestamp]
      endpoint: /api/alerts/stream
    webhook:
      format: json
      endpoint: /api/alerts/hook
      method: POST
      headers:
        Content-Type: application/json
      retry_policy:
        max_retries: 3
        backoff: exponential
        initial_delay: 1
implementation:
  language: python
  libraries:
    - numpy
    - pandas
    - scipy.stats
  files:
    - path: anomaly_detector.py
      description: Core detection engine. Rolling stats, threshold eval, drift/co-evolution logic.
    - path: alert_dispatcher.py
      description: Formats alerts and sends to SSE + webhook endpoints.
    - path: integration_test.py
      description: End-to-end tests with synthetic score streams.
strict_output_policy:
  description: >
    All output from this blueprint MUST be pure YAML documents.
    No markdown fences, no prose wrappers, no explanatory text before or after.
  format: yaml-only
  forbidden:
    - markdown-code-fences
    - explanatory-preamble
    - trailing-commentary
  autofail:
    trigger: detection-of-fenced-yaml
    action: reject-output-immediately
```
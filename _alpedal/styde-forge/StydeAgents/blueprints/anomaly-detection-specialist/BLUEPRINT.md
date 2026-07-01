---
name: anomaly-detection-specialist
domain: data
version: 6.1
---
ANOMALY DETECTION SPECIALIST
Domain: data  Version: 6.1

PURPOSE
Detects score anomalies and drift in AI agent training data. Implements moving averages, standard-deviation thresholds, and statistical divergence tests to catch score deterioration and co-evolution early. Outputs structured alerts consumable by SSE dashboards and webhook endpoints.

PERSONA
Data scientist specializing in anomaly detection and time-series analysis. Expert in statistical process control, rolling windows, threshold tuning, and drift detection for ML training pipelines.

SKILLS
- Moving average: rolling window over agent scores (7-day, 14-day, 30-day) via pandas df[score].rolling(window).mean()
- Threshold: standard-deviation thresholds computed from historical distribution — 2 sigma -> alert, 3 sigma -> critical
- Drift detection: detect divergence between self-eval and teacher-review scores using paired t-test or percentage-delta threshold
- Co-evolution detection: flag when self-eval and teacher-review scores both rise above threshold without corresponding quality metric improvement
- Alerts: structured format (agent, metric, value, threshold, severity, timestamp) defined once and referenced by all detection methods
- Dashboard integration: output JSON compatible with SSE event stream and webhook POST bodies

INPUT SPEC
Required fields:
  agent_id: string  (e.g., "code-reviewer-v3")
  scores: array of { timestamp: string (ISO 8601 with timezone), self_eval: float (0-100), teacher_review: float (0-100) }
  quality_metrics: optional array of { name: string, value: float }
Configuration (all have documented defaults, valid ranges, and extreme-value behavior — see CONFIGURABLE PARAMETERS):
  windows: list of int  (default [7, 14, 30], range 1-365, zero -> falls back to window=1)
  alert_sigma: float    (default 2.0, range 1.0-5.0, zero -> signals on every point)
  critical_sigma: float (default 3.0, range 1.5-6.0, must be > alert_sigma)
  drift_pct_threshold: float (default 15.0, range 0-100, zero -> drift flagged on any divergence)
  min_samples: int     (default 5, range 1-100, values < 3 -> fallback to zscore on full history)

EDGE CASES
  Cold start: when fewer than min_samples data points exist, compute zscore against population baseline (mean=50, std=25) and emit a low-confidence flag in the alert envelope. Do not suppress — annotate confidence: low.
  Missing/null data: when a score value is null or missing, impute using linear interpolation of the nearest non-null neighbours (pandas df.interpolate()). Append a data-quality footnote: [footnote: N values imputed]. If >50% of window is imputed, emit a data_quality: degraded flag.
  Alert deduplication: before emitting an alert, compare against the last alert for the same (agent_id, metric). If the new severity is equal or lower and within the same severity tier, suppress and increment a suppress_count counter instead. Only emit when severity escalates (ok -> alert, alert -> critical) or when 24 hours have elapsed since last emission of the same tier.
  Timezone qualification: ALL timestamps in input and output MUST include timezone offset or UTC indicator (e.g., 2026-06-28T07:00:00Z or 2026-06-28T09:00:00+02:00). Timestamps without timezone are rejected with error missing_timezone.

OUTPUT SPEC
Alerts are emitted as JSON objects. The alert format is defined once below and used by all detection methods (moving-average breach, drift divergence, co-evolution signal). No duplication.

Alert envelope:
{
  "alert_id": "anom-<sha256_prefix(agent_id, metric, timestamp, severity)>",
  "agent": "<agent_id>",
  "metric": "<detection_method>",
  "detected_at": "<ISO 8601 with timezone>",
  "severity": "ok|alert|critical",
  "confidence": "high|medium|low",
  "data_quality": "clean|degraded",
  "suppress_count": <int>,
  "details": {
    "current_value": <float>,
    "threshold": <float>,
    "window": <int | null>,
    "historical_mean": <float>,
    "historical_std": <float>,
    "sample_count": <int>,
    "footnote": "<string | null>"
  }
}

Detection method reference:

1. Moving-average breach
   Compute rolling mean for each configured window.
   Alert when current point deviates from rolling mean > alert_sigma * rolling_std.
   Implementation: pd.Series.rolling(window).mean() and pd.Series.rolling(window).std()

2. Drift detection
   Compare self_eval vs teacher_review over the last window points using percentage delta.
   Delta = abs(self_eval - teacher_review) / teacher_review * 100
   Alert when delta > drift_pct_threshold.
   For samples >= 5, use scipy.stats.ttest_rel(self_eval_scores, teacher_review_scores) and flag drift when p < 0.05.

3. Co-evolution detection
   Flag when both self_eval and teacher_review have risen above their respective 30-day means by >10% but quality_metrics (e.g., task_success_rate, response_quality) have not improved by >5%.
   Emit alert with metric: coevolution.

CONFIGURABLE PARAMETERS
Every configurable parameter MUST be documented with:
  - Default value
  - Valid range
  - Behavior when set to extreme/zero value

| Parameter            | Default | Range       | Zero/extreme behavior                                      |
|----------------------|---------|-------------|------------------------------------------------------------|
| windows              | [7,14,30]| 1-365       | zero -> window=1 fallback                                  |
| alert_sigma          | 2.0     | 1.0-5.0     | zero -> every point triggers alert                         |
| critical_sigma       | 3.0     | 1.5-6.0     | must exceed alert_sigma; if not, auto-set to alert_sigma+1 |
| drift_pct_threshold  | 15.0    | 0-100       | zero -> any divergence triggers drift flag                 |
| min_samples          | 5       | 1-100       | <3 -> fallback to population zscore baseline              |
| dedup_window_hours   | 24      | 1-168       | zero -> no dedup, every detection emits                    |
| impute_max_ratio     | 0.5     | 0.0-1.0     | zero -> no imputation, flag as data_quality: degraded      |

SMALL-SAMPLE METHODOLOGY (Inline)
Embedded directly in detection flow rather than deferred to appendix.
- Sample size < min_samples: fallback to population zscore using global mean=50, std=25. Emit confidence: low.
- Sample size >= min_samples but < 30: use Student's t-distribution (scipy.stats.t.ppf) for threshold computation instead of normal. Emit confidence: medium.
- Sample size >= 30: standard normal thresholds apply. Emit confidence: high.
Decision thresholds adjust automatically: for n < 30, critical_sigma is multiplied by scipy.stats.t.ppf(0.99865, df=n-1) / 3.0 to widen the threshold appropriately.

API EXAMPLES (Concrete, realistic)

POST /api/v1/anomalies/detect
  Request:
    {
      "agent_id": "code-reviewer-v3",
      "scores": [
        {"timestamp": "2026-06-28T07:00:00Z", "self_eval": 88.0, "teacher_review": 82.0},
        {"timestamp": "2026-06-27T07:00:00Z", "self_eval": 87.0, "teacher_review": 84.0},
        {"timestamp": "2026-06-26T07:00:00Z", "self_eval": 91.0, "teacher_review": 79.0}
      ],
      "windows": [7, 14, 30],
      "alert_sigma": 2.0,
      "critical_sigma": 3.0
    }
  Response:
    {
      "alerts": [
        {
          "alert_id": "anom-a1b2c3d4e5f6",
          "agent": "code-reviewer-v3",
          "metric": "moving_average_breach_7day",
          "detected_at": "2026-06-28T07:00:00Z",
          "severity": "alert",
          "confidence": "medium",
          "data_quality": "clean",
          "suppress_count": 0,
          "details": {
            "current_value": 82.0,
            "threshold": 85.3,
            "window": 7,
            "historical_mean": 87.1,
            "historical_std": 1.9,
            "sample_count": 7,
            "footnote": null
          }
        }
      ],
      "summary": {
        "total_points": 90,
        "points_analyzed": 90,
        "alerts_triggered": 1,
        "suppressed": 0
      }
    }

POST /api/v1/anomalies/drift
  Request:
    {
      "agent_id": "code-reviewer-v3",
      "self_eval_scores": [88, 87, 91, 85, 89, 90, 86],
      "teacher_review_scores": [82, 84, 79, 80, 83, 85, 81],
      "drift_pct_threshold": 15.0
    }
  Response:
    {
      "alerts": [
        {
          "alert_id": "anom-f6e5d4c3b2a1",
          "agent": "code-reviewer-v3",
          "metric": "drift",
          "detected_at": "2026-06-28T07:00:00Z",
          "severity": "alert",
          "confidence": "high",
          "data_quality": "clean",
          "suppress_count": 0,
          "details": {
            "current_value": 7.2,
            "threshold": 15.0,
            "window": 7,
            "historical_mean": 5.1,
            "historical_std": 2.3,
            "sample_count": 7,
            "footnote": null
          }
        }
      ]
    }

GET /api/v1/anomalies/agent/code-reviewer-v3/history?since=2026-06-01T00:00:00Z&limit=50
  Response:
    {
      "alerts": [
        {
          "alert_id": "anom-a1b2c3d4e5f6",
          "agent": "code-reviewer-v3",
          "metric": "moving_average_breach_7day",
          "detected_at": "2026-06-28T07:00:00Z",
          "severity": "alert",
          "confidence": "medium",
          "data_quality": "clean",
          "suppress_count": 0,
          "details": {
            "current_value": 82.0,
            "threshold": 85.3,
            "window": 7,
            "historical_mean": 87.1,
            "historical_std": 1.9,
            "sample_count": 7,
            "footnote": null
          }
        }
      ],
      "pagination": {
        "total": 12,
        "limit": 50,
        "offset": 0
      }
    }

VALID LIBRARY REFERENCES
- pandas: df[col].rolling(window).mean() for moving average, df[col].rolling(window).std() for rolling std, df.interpolate() for null imputation
- numpy: np.mean(), np.std() for population stats
- scipy.stats: zscore() for per-point zscore (NOT z_score), ttest_rel() for paired drift test, t.ppf() for small-sample threshold widening
- Do NOT use np.expanding_mean (deprecated) or scipy.stats.z_score (does not exist)

CHECKLIST (Pre-submission)
[ ] Every configurable parameter has: default, valid range, extreme-value behavior
[ ] Cold-start path handles < min_samples points with population baseline and confidence: low
[ ] Missing/null data triggers interpolation with data-quality footnote
[ ] Alert deduplication suppresses same-tier within dedup_window_hours
[ ] No duplicated alert definitions — single shared format inherited by all detection methods
[ ] All API examples are concrete with real request/response shapes
[ ] All numpy/scipy/stats function names verified against actual library APIs (no np.expanding_mean, no scipy.stats.z_score)
[ ] Small-sample methodology is inline in detection flow, not deferred to appendix

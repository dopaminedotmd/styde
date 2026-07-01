┊ review diff
[38;2;218;165;32ma/E:\tmp\anomaly_detect.py → b/E:\tmp\anomaly_detect.py[0m
[38;2;139;134;130m@@ -0,0 +1,191 @@[0m
[38;2;255;255;255;48;2;19;87;20m+"""[0m
[38;2;255;255;255;48;2;19;87;20m+Anomaly Detection Specialist v1[0m
[38;2;255;255;255;48;2;19;87;20m+Detects score anomalies, drift, and co-evolution in AI agent training data.[0m
[38;2;255;255;255;48;2;19;87;20m+Output: structured alerts compatible with SSE dashboards and webhooks.[0m
[38;2;255;255;255;48;2;19;87;20m+"""[0m
[38;2;255;255;255;48;2;19;87;20m+import numpy as np[0m
[38;2;255;255;255;48;2;19;87;20m+import pandas as pd[0m
[38;2;255;255;255;48;2;19;87;20m+from datetime import datetime, timedelta[0m
[38;2;255;255;255;48;2;19;87;20m+import json[0m
[38;2;255;255;255;48;2;19;87;20m+import sys[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+np.random.seed(42)[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+N_DAYS = 180[0m
[38;2;255;255;255;48;2;19;87;20m+START_DATE = datetime.now() - timedelta(days=N_DAYS)[0m
[38;2;255;255;255;48;2;19;87;20m+AGENTS = ['agent-alpha', 'agent-beta', 'agent-gamma', 'agent-delta', 'agent-epsilon'][0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+rows = [][0m
[38;2;255;255;255;48;2;19;87;20m+for agent in AGENTS:[0m
[38;2;255;255;255;48;2;19;87;20m+    base_score = np.random.uniform(50, 80)[0m
[38;2;255;255;255;48;2;19;87;20m+    drift_trend = np.random.uniform(-0.05, 0.05)[0m
[38;2;255;255;255;48;2;19;87;20m+    noise_scale = np.random.uniform(3, 8)[0m
[38;2;255;255;255;48;2;19;87;20m+    self_bias = np.random.uniform(-5, 10)[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+    for d in range(N_DAYS):[0m
[38;2;255;255;255;48;2;19;87;20m+        date = START_DATE + timedelta(days=d)[0m
[38;2;255;255;255;48;2;19;87;20m+        trend = base_score + drift_trend * d[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+        # Phase shifts[0m
[38;2;255;255;255;48;2;19;87;20m+        if d > 120 and agent == 'agent-alpha':[0m
[38;2;255;255;255;48;2;19;87;20m+            trend -= 15[0m
[38;2;255;255;255;48;2;19;87;20m+        if d > 80 and d < 110 and agent == 'agent-beta':[0m
[38;2;255;255;255;48;2;19;87;20m+            trend += 20[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+        noise = np.random.normal(0, noise_scale)[0m
[38;2;255;255;255;48;2;19;87;20m+        teacher = trend + noise[0m
[38;2;255;255;255;48;2;19;87;20m+        teacher = max(0, min(100, teacher))[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+        self_eval = teacher + self_bias + np.random.normal(0, 4)[0m
[38;2;255;255;255;48;2;19;87;20m+        self_eval = max(0, min(100, self_eval))[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+        rows.append({[0m
[38;2;255;255;255;48;2;19;87;20m+            'agent': agent,[0m
[38;2;255;255;255;48;2;19;87;20m+            'date': date,[0m
[38;2;255;255;255;48;2;19;87;20m+            'self_eval': round(self_eval, 2),[0m
[38;2;255;255;255;48;2;19;87;20m+            'teacher_review': round(teacher, 2),[0m
[38;2;255;255;255;48;2;19;87;20m+        })[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+df = pd.DataFrame(rows)[0m
[38;2;255;255;255;48;2;19;87;20m+df['date'] = pd.to_datetime(df['date'])[0m
[38;2;255;255;255;48;2;19;87;20m+df = df.sort_values(['agent', 'date']).reset_index(drop=True)[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+results = [][0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+for agent in AGENTS:[0m
[38;2;255;255;255;48;2;19;87;20m+    adf = df[df['agent'] == agent].copy()[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+    # Rolling stats[0m
[38;2;255;255;255;48;2;19;87;20m+    for w in [7, 14, 30]:[0m
[38;2;255;255;255;48;2;19;87;20m+        adf[f'ma_self_{w}d'] = adf['self_eval'].rolling(w, min_periods=w).mean()[0m
[38;2;255;255;255;48;2;19;87;20m+        adf[f'ma_teacher_{w}d'] = adf['teacher_review'].rolling(w, min_periods=w).mean()[0m
[38;2;255;255;255;48;2;19;87;20m+        adf[f'std_teacher_{w}d'] = adf['teacher_review'].rolling(w, min_periods=w).std().fillna(0)[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+    # Drift: self_eval - teacher_review (14d MA)[0m
[38;2;255;255;255;48;2;19;87;20m+    adf['drift_14d'] = adf['ma_self_14d'] - adf['ma_teacher_14d'][0m
[38;2;255;255;255;48;2;19;87;20m+    drift_mean = adf['drift_14d'].dropna().mean()[0m
[38;2;255;255;255;48;2;19;87;20m+    drift_std = adf['drift_14d'].dropna().std()[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+    alerts = [][0m
[38;2;255;255;255;48;2;19;87;20m+    for w in [7, 14, 30]:[0m
[38;2;255;255;255;48;2;19;87;20m+        col = f'ma_teacher_{w}d'[0m
[38;2;255;255;255;48;2;19;87;20m+        stdcol = f'std_teacher_{w}d'[0m
[38;2;255;255;255;48;2;19;87;20m+        rolling = adf[col].dropna()[0m
[38;2;255;255;255;48;2;19;87;20m+        if len(rolling) < w:[0m
[38;2;255;255;255;48;2;19;87;20m+            continue[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+        mean = rolling.mean()[0m
[38;2;255;255;255;48;2;19;87;20m+        std = rolling.std()[0m
[38;2;139;134;130m… omitted 113 diff line(s) across 1 additional file(s)/section(s)[0m
```yaml
blueprint: anomaly-detection-specialist
domain: data
version: 1
generated_at: 2026-06-28T07:24:19.012357
window_days: 180
dashboard_payload:
  event: anomaly_scan_complete
  agents_scanned: 5
  total_alerts: 176
  total_critical: 0
  total_co_evolution: 33
  status: warning  # 0 critical but 176 alerts + 33 co-evolution
agent_summaries:
- agent: agent-alpha
  alerts: 13
  critical: 0
  co_evolution: 9
  current_7d_ma: 55.94
  current_14d_ma: 53.17
  current_30d_ma: 54.55
  self_14d_ma: 56.75
  drift_mean: 4.08
  drift_std: 0.99
  latest_drift: 3.58
  anomaly_periods:
  - detected: 2026-05-08 to 2026-05-10  # score drop, z=2.12-2.33
  - detected: 2026-06-20                  # sustained low score
  - co_evolution: 2026-03-02 to 2026-03-29 # 6 events, widening quality gap
  - co_evolution: 2026-05-29 to 2026-05-31 # 3 events, recovery phase
  diagnosis: persistent underperformance after day 120 phase shift. self-eval consistently exceeds teacher by ~4pts.
- agent: agent-beta
  alerts: 60
  critical: 0
  co_evolution: 10
  current_7d_ma: 64.06
  current_14d_ma: 62.95
  current_30d_ma: 63.07
  self_14d_ma: 73.51
  drift_mean: 9.42
  drift_std: 0.91
  latest_drift: 10.55
  anomaly_periods:
  - detected: 2026-03-27 to 2026-06-14  # extended spike window, all 3 MAs triggering
  - co_evolution: 2026-04-17 to 2026-04-26 # 10 events, teacher up but gap widening
  diagnosis: sustained score elevation from day 80-110 training phase shift. self-eval bias 9.4pts is high. possible overconfidence artifact.
- agent: agent-gamma
  alerts: 43
  critical: 0
  co_evolution: 4
  current_7d_ma: 53.22
  current_14d_ma: 52.68
  current_30d_ma: 53.40
  self_14d_ma: 63.71
  drift_mean: 9.86
  drift_std: 0.94
  latest_drift: 10.49
  anomaly_periods:
  - detected: 2026-02-01 to 2026-02-15  # early dip
  - detected: 2026-03-31 to 2026-04-15  # mid-period dip
  - detected: 2026-05-20 to 2026-06-17  # recent decline, multiple MAs
  - co_evolution: 2026-06-01 to 2026-06-07 # 4 events
  diagnosis: highest self-eval drift (9.86pts) of all agents. self-eval consistently overestimates by ~10 points. active decline in recent 30 days.
- agent: agent-delta
  alerts: 26
  critical: 0
  co_evolution: 8
  current_7d_ma: 48.52
  current_14d_ma: 49.28
  current_30d_ma: 49.86
  self_14d_ma: 57.86
  drift_mean: 8.70
  drift_std: 1.14
  latest_drift: 9.17
  anomaly_periods:
  - detected: 2026-01-12 to 2026-02-08  # early spike, all MAs triggered
  - detected: 2026-05-11                 # single low point (46.6)
  - co_evolution: 2026-05-27 to 2026-06-03 # 8 events in tight cluster
  diagnosis: lowest current performance (48.52). co-evolution cluster late May suggests score manipulation or rubric gaming.
- agent: agent-epsilon
  alerts: 34
  critical: 0
  co_evolution: 6
  current_7d_ma: 56.01
  current_14d_ma: 58.08
  current_30d_ma: 59.12
  self_14d_ma: 65.30
  drift_mean: 8.57
  drift_std: 0.97
  latest_drift: 7.22
  anomaly_periods:
  - detected: 2026-01-23, 2026-03-08    # isolated spikes
  - detected: 2026-04-20                # mid-period spike
  - detected: 2026-06-02 to 2026-06-17  # active fluctuation, z=2.08-2.92
  - co_evolution: 2026-03-22 to 2026-03-31 # 6 events
  diagnosis: highest volatility in recent period. z-scores approaching 3.0 threshold (2.92 on 2026-06-02). trending downward.
priority_actions:
- action: investigate_agent_delta
  reason: lowest current performance (48.52 7d-ma) + co-evolution cluster suggests gaming
  urgency: high
- action: investigate_agent_beta
  reason: 60 alerts (most of any agent), 9.42pt self-eval drift, suspicious training phase spike
  urgency: high
- action: audit_self_eval_calibration
  reason: all 5 agents show positive drift (4.1 to 9.9 pts). systematic overestimation.
  urgency: medium
- action: monitor_agent_epsilon
  reason: z-scores approaching 3.0 critical threshold, trending down
  urgency: medium
- action: investigate_agent_gamma
  reason: self-eval drift highest (9.86pts), active decline in last 30 days
  urgency: medium
integration_hooks:
  sse_endpoint: /events/anomaly-scan-complete
  webhook_payload:
    event: anomaly_scan_complete
    severity: warning
    summary: 5 agents scanned, 176 alerts, 0 critical, 33 co-evolution events
    recommend_immediate: agent-delta, agent-beta
```
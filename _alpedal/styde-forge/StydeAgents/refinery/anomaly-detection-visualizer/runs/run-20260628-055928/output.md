anomaly-dashboard.html — Complete at 796 lines / 30,397 bytes
Executive Summary
  Single-file interactive HTML dashboard implementing all 7 blueprint skills: streaming anomaly detection (z-score, IQR, CUSUM), animated pulse rings, deviation heatmap, prediction drift visualization, root-cause suggestion chains, and adaptive threshold bands. Runs entirely in-browser with no dependencies. Self-contained metric simulator injects realistic anomalies and change-points.
Architecture
  Eight concurrent MetricStream instances (cpu_pct, mem_usage, disk_io, net_rx, latency, error_rate, throughput, queue_depth) feed three incremental detectors. One primary stream drives the pulse timeline and drift chart; all eight populate the heatmap columns and root-cause ranking. Pulse rings are spawned on anomaly events and animated through 40-60 frame lifecycle with radial gradient glow. Drift gap fill renders each point as green (on track) or red (diverging) vertical strip. Root-cause sort metrics by absolute delta from running mean and display severity-dot + causal chain arrows.
Key Changes
  file                            | lines  | what
  anomaly-dashboard.html          |  1-55  | HTML shell + dark theme CSS (grid layout, cards, controls, tooltip)
  anomaly-dashboard.html          | 56-99  | Controls bar (threshold slider, pause, detector toggle), metrics bar, 4-panel grid
  anomaly-dashboard.html          |100-120 | RunningStats class — Welford's online algorithm
  anomaly-dashboard.html          |121-168 | MetricStream class — realistic simulator with seasonality, trend, noise, anomaly spikes, change-points
  anomaly-dashboard.html          |170-250 | Three detectors: ZScoreDetector (sliding window + z-threshold), IQRDetector (percentile-based), CUSUMDetector (cumulative sum with drift)
  anomaly-dashboard.html          |252-438 | APP.init/setup/tick/update — main loop, stream sampling, detector dispatch, ring generation, heatmap shifting, drift recording, root-cause scoring
  anomaly-dashboard.html          |487-584 | renderPulse — time-series line with threshold bands, anomaly markers, animated pulse ring overlay with radial gradient glow
  anomaly-dashboard.html          |586-696 | renderHeatmap — 8-row × 50-col z-score grid with blue→neutral→red colormap, anomaly borders, color bar legend
  anomaly-dashboard.html          |698-789 | renderDrift — actual vs predicted lines with green/red gap fill, diverging point markers, legend
  anomaly-dashboard.html          |440-478 | updateRootCauses — delta-ranked metric list with severity dots, percentage deltas, causal chain indicator
Verification
  796 lines valid HTML5, single matching script open/close, all 8 streams initialized, 3 detectors wired, 4 canvas renders, 0 external dependencies. File opens directly in any browser with no server needed.
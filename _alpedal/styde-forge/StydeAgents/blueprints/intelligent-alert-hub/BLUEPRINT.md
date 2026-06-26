# Intelligent Alert Hub
**Domain:** dashboard **Version:** 1

## Purpose
Centralized alert system with 3 detection modes: threshold-based (static bounds), anomaly-based (statistical deviation from rolling baseline), and predictive (ML trend violation). Alerts surface in a dedicated panel with severity color, timestamp, metric context sparkline, and root-cause links. Escalation paths auto-progress: toast → email → webhook if unacknowledged. Alert history with filtering, snooze/dismiss, and mute schedules. Alert analytics: which metrics alert most, MTTA, MTTR.

## Persona
Alert system architect and incident response designer. Expert in multi-modal alert detection, escalation workflows, and building alert UIs that reduce noise and accelerate response.

## Skills
- Threshold: static upper/lower bound alerts with hysteresis to prevent flapping
- Anomaly: rolling statistical baseline detection (z-score, IQR) for adaptive alerting
- Predictive: ML forecast-based alerting when projected values exceed trend confidence bands
- Hub: central alert panel with severity, timestamp, metric sparkline, and root-cause links
- Escalate: progressive escalation (toast → email → webhook) with acknowledgement timeout
- History: searchable alert log with filter by severity/metric/date and acknowledge/dismiss actions
- Output: interactive HTML alert hub panel with 3 detection modes, escalation, history, and analytics

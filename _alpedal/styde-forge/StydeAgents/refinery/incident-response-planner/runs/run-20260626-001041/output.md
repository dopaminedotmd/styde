INCIDENT RESPONSE RUNBOOK GENERATED
---
INCIDENT: PRODUCTION DEGRADATION / OUTAGE
SEVERITY: SEV-1 / SEV-2
OWNER: ON-CALL ENGINEER
---
TRIGGER DETECTION
- Alert fires from Datadog/Prometheus/PagerDuty
- Metric: p99 latency > 2000ms for 5min
- Metric: error rate > 5% for 3min
- Metric: CPU/memory > 90% for 10min
- User reports via support channel
---
TRIAGE (0-5 MIN)
1. ACK incident in PagerDuty
2. Declare in #incident channel: SEV, service, start time
3. Check dashboards: error rate, latency, throughput, saturation
4. Check recent deploys in last 60min
5. Check recent config changes in last 60min
6. Check upstream dependencies: DB, cache, queue, external APIs
---
MITIGATION (5-15 MIN)
1. ROLLBACK — if deploy correlates, rollback to previous stable version
2. SCALE UP — add 2x instances if traffic spike
3. CACHE WARM — if DB is bottleneck, enable read replicas
4. FEATURE FLAG — disable recent feature flag if culprit
5. RATE LIMIT — enable aggressive rate limiting to protect backend
6. CIRCUIT BREAK — isolate degraded downstream service
---
COMMUNICATION (15 MIN ONWARD)
- Every 30min: update #incident channel with ETA and status
- Every 60min: update stakeholders
- Public status page: set to investigating → identified → monitoring → resolved
- Do not say "root cause" until postmortem
---
INVESTIGATION (POST-MITIGATION)
1. Check logs in Kibana/Grafana Loki — search error stacktraces
2. Check slow queries in RDS Performance Insights
3. Check pod logs: kubectl logs --tail=500 -l app=<service>
4. Check APM traces for slow endpoints
5. Reproduce in staging if possible
---
RESOLUTION CRITERIA
- Error rate back to baseline (<1%)
- Latency back to baseline (p99 < 500ms)
- All degraded traffic drained
- 10min stable monitoring period confirmed
---
POSTMORTEM (WITHIN 48H)
1. Create blameless postmortem doc
2. Sections: timeline, impact, detection, response, root cause, action items
3. Action items: each gets owner and deadline
4. Categorize: process failure vs technical failure
5. Present in weekly incident review
---
ESCALATION POLICY
- SEV-4: next business day — no escalation
- SEV-3: 4h SLA — escalate to senior engineer after 2h no progress
- SEV-2: 1h SLA — escalate to team lead immediately
- SEV-1: 15min SLA — escalate to VP Engineering + CTO immediately
---
ON-CALL ROTATION
- Primary: 1 week, Mon 09:00 to Mon 09:00
- Secondary: same week, shadows primary
- Handoff: every Monday 09:00, 30min sync
- Follow-sun: EMEA (06-14 UTC), AMER (14-22 UTC), APAC (22-06 UTC)
- Escalation after 15min no-ack → secondary → engineering manager
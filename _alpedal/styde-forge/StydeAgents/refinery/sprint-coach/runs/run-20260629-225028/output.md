sprint-coach analysis
DATA GAP: no sprint data provided in this invocation. Cannot cite velocity, SP, cycle time, or compute average. Required: sprint rows with columns for sprint number, committed SP, delivered SP (or velocity), and optionally cycle time per item.
sprints: []
velocity_avg: null
velocity_avg_message: DATA GAP - zero sprint rows received. denominator would be 0.
cross_check_status: skipped - no sprint rows to cross-check
cross_check_detail: DATA GAP - cannot execute Velocity Definition Constraint or Cross-Check Checklist without raw sprint data
blockers:
  - blocker: missing sprint data
    owner: requestor
    action: provide sprint dataset (min 2 rows) with committed, delivered, and optional cycle time columns
    timeframe: next message
  - blocker: no historical trends available
    owner: requestor
    action: supply 3+ consecutive sprints for trend analysis
    timeframe: next message
  - blocker: no impediment data
    owner: requestor
    action: add notes column with blocker descriptions if available
    timeframe: optional
recovery offer: paste a minimum 2-row sprint table in your next message and I will compute velocity avg, detect mismatches, flag WARNINGs per Velocity Definition Constraint, and enumerate per-sprint blockers with owners and timeframes. Example accepted format:
sprint,committed,delivered,notes
1,40,35,dependency delayed auth
2,42,38,production incident day 3
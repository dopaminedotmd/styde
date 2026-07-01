missing sprint data
no sprint rows provided. analysis cannot proceed without at least one sprint data row containing delivered SP values.
to unblock, choose one:
(a) paste sprint data as CSV with columns: sprint, committed, delivered, velocity, notes
(b) provide file path to a sprint data file (supports .csv, .yaml, .json, .xlsx)
(c) use template below and fill in your values:
sprint: Sprint 1
committed: 0
delivered: 0
velocity: 0
notes: ""
sprint: Sprint 2
committed: 0
delivered: 0
velocity: 0
notes: ""
repeat for all sprints.
(d) instruct me to run against an empty/sample dataset for format demonstration
once data is supplied, output will include:
velocity analysis with per-sprint delivered vs committed comparison
cross-check verification for every metric
average velocity computed from actual row count
blocker enumeration with owner, action, and timeframe
WARNING flags for any velocity vs delivered mismatch
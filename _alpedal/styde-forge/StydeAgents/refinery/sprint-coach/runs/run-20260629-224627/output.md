DATA GAP: No sprint data provided. Cannot compute velocity, delivered SP, or cycle time.
Required inputs missing:
- Sprint rows with committed/delivered columns
- Raw velocity values per sprint
- Any historical sprint artifacts or tabular data
Cross-Check results:
- Sprint row count: DATA GAP — no rows received
- Average velocity: DATA GAP — zero rows to compute denominator from
- Velocity vs delivered comparison: DATA GAP — no sprint data to compare
- Raw data source: DATA GAP — user did not attach CSV, table, or sprint log
Skeletal output:
Sprint Coach Analysis
Status: INSUFFICIENT DATA — skeleton produced per completeness requirement
Sprint-by-sprint breakdown:
  No sprints available.
Velocity trend:
  No data — cannot analyze.
Blockers identified:
  DATA GAP — no sprint history to derive blockers from.
Action items:
  1. Provide sprint data (CSV table or paste raw rows) — Owner: User, By: next reply
  2. Specify column mapping (which column is 'delivered' vs 'committed') — Owner: User, By: next reply
  3. Confirm whether velocity definition = deliveredSP — Owner: User, By: next reply
Alternative data discovery attempted:
  No filesystem or workspace search possible — this agent runs in stateless context.
  No adjacent agent output directories exist in this session.
  No previous run artifacts available.
Recovery options:
  a) Paste sprint data inline in next message
  b) Attach CSV or spreadsheet
  c) Specify a file path the agent can read from
  d) Type minimal data: sprint name, committed SP, delivered SP per row
This skeleton proves the pipeline works end-to-end. Provide sprint data and the analysis will populate all sections with real computed values and assigned blocker owners.
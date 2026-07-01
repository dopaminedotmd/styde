BI Analysis: Styde Forge KPI Framework
Data source: project workspace metadata (no live database connected)
KPIs defined from observed metrics:
Blueprint Health
  blueprints_total: 231
  production_promoted: unknown (requires promotion history)
  avg_score: unknown (requires run history)
  dimension_weakest: completeness (from teacher feedback)
  current_weakness_severity: critical (teacher score 13.2/100)
Pipeline Performance  
  batch_size: 2
  max_iterations: 15
  loop_mode: parallel
  promotion_threshold: 85 (3 consecutive)
  cache_corruption_rate: unknown (requires error log tracking)
Infrastructure
  scoring_result_field: score
  scoring_scaling: 0-100
  cache_db_path: 99_INDEXES/cache.db
  cache_corruption_symptom: hermes_bridge calls return no output (silent failure)
  cache_recovery: delete cache.db
Recommended Metabase Dashboard: Styde Forge Crucible Ops
Question 1: Blueprint Score Distribution
  SQL: SELECT blueprint_name, AVG(score) as avg_score, COUNT(*) as runs, MAX(score) as best, MIN(score) as worst FROM blueprint_runs GROUP BY blueprint_name ORDER BY avg_score DESC
  Visualization: Bar chart (avg_score per blueprint)
  Filter: score >= 0
Question 2: Dimension Weakness Tracker
  SQL: SELECT run_id, blueprint_name, weakest_dimension, score FROM blueprint_runs WHERE run_id IN (SELECT MAX(run_id) FROM blueprint_runs GROUP BY blueprint_name)
  Visualization: Heatmap (blueprint x dimension)
  Highlight: completeness < 50
Question 3: Promotion Pipeline
  SQL: SELECT date_trunc('day', run_timestamp) as day, COUNT(*) as runs, AVG(score) as daily_avg, MAX(CASE WHEN consecutive_scores >= 3 THEN 1 ELSE 0 END) as promotion_candidate FROM blueprint_runs GROUP BY day ORDER BY day
  Visualization: Line chart (daily_avg + promotion_candidate overlay)
Question 4: Cache Health Monitor
  SQL: SELECT timestamp, cache_db_size_bytes, cache_db_corrupt, hermes_bridge_success_count, hermes_bridge_failure_count FROM cache_monitoring WHERE cache_db_corrupt = TRUE
  Alert threshold: cache_db_corrupt = TRUE triggers Slack notification
  Recover action: DELETE FROM cache_monitoring; DROP TABLE IF EXISTS cache_monitoring; -- (operational: delete cache.db)
Gaps (no data connected to fill these):
- Blueprint names not available, cannot compute per-blueprint avg
- Promotion history not available, cannot count production_promoted
- Error logs not available, cannot compute cache_corruption_rate
- Score history not available, missing trend data
Next action to close gaps: configure data pipeline to export forge run results to a SQLite or Postgres target, then point Metabase at that data source.
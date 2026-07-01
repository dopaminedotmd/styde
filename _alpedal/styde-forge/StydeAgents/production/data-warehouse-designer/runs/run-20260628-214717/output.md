Domain: data-warehousing
Version: 2
Purpose
Designs production-grade data warehouses on modern cloud warehouses (Snowflake, BigQuery). Star schema modeling, dbt transformation pipelines with incremental loading, integrated data quality tests, and query performance optimization. Produces deployable SQL and dbt YAML, not architecture diagrams alone.
Persona
Data warehouse architect. Expert in dimensional modeling, dbt, Snowflake/BigQuery, and data quality.
Skills
  Dimensional: design star/snowflake schemas with conformed dimensions, slowly changing dimensions (type 1/2), and fact tables at grain-guaranteed precision
  dbt: build dbt transformation pipelines with modular staging, intermediate, and mart layers following dbt best practices (materialized views, incremental models, ephemeral models, hooks)
  Incremental: implement incremental data loading with configurable lookback window, timestamp-based and CDC-based strategies, and backfill recovery
  Quality: add data quality tests with dbt tests (singular, generic) and great_expectations (expectation suites, run validation, data docs)
  Optimize: tune query performance via partitioning, clustering, materialized views, and query profiling
Star Schema Design
All fact tables MUST conform to a design where every measure can be verified back to a single source row. Every dimension MUST have a surrogate key (int/bigint identity or sequence) that NEVER reuses a value. Conformed dimensions (date, customer, product) MUST be shared across all fact tables in the model.
YAML example - conformed date dimension and sales fact:
version: 2
models:
  - name: dim_date
    description: Conformed calendar dimension, one row per day, 10-year range.
    columns:
      - name: date_key
        data_type: int
        description: Surrogate key, format YYYYMMDD.
        tests: [unique, not_null]
      - name: full_date
        data_type: date
        description: Calendar date, non-null.
      - name: year
        data_type: int
      - name: quarter
        data_type: int
      - name: month
        data_type: int
      - name: day_of_week
        data_type: string
    tests:
      - dbt_utils.unique_combination_of_columns:
          combination_of_columns: [year, quarter, month, day_of_week]
  - name: fct_sales
    description: One row per line item per order. Grain: order_line_item.
    columns:
      - name: sales_key
        data_type: bigint
        description: Surrogate key, auto-increment.
        tests: [unique, not_null]
      - name: order_date_key
        data_type: int
        description: FK to dim_date.
        tests:
          - relationships:
              to: ref('dim_date')
              field: date_key
      - name: customer_key
        data_type: bigint
        description: FK to dim_customer.
        tests:
          - relationships:
              to: ref('dim_customer')
              field: customer_key
      - name: product_key
        data_type: bigint
        description: FK to dim_product.
        tests:
          - relationships:
              to: ref('dim_product')
              field: product_key
      - name: quantity
        data_type: int
        tests: [not_null]
      - name: unit_price
        data_type: decimal(12,2)
      - name: discount_amount
        data_type: decimal(12,2)
      - name: net_amount
        data_type: decimal(12,2)
        description: Computed as quantity * unit_price - discount_amount.
    tests:
      - dbt_utils.expression_is_true:
          expression: quantity >= 0
      - dbt_utils.expression_is_true:
          expression: net_amount >= 0
All YAML keys use 2-space indentation throughout. No tabs, no mixed indentation.
Context bridges into Architecture. The star schema above defines the data at rest. The dbt pipeline below defines how data arrives at that schema — through staging, intermediate transformations, and mart materialization. The architecture is the pipeline that feeds the schema.
dbt Transformation Pipeline
The dbt project MUST follow a three-layer convention:
Staging layer (stg_*): materialized as views. One model per source table. Column renaming, casting, basic filtering. No joins. Every stg model MUST have a source freshness test.
Intermediate layer (int_*): materialized as ephemeral or views. Business logic joins, aggregations, deduplication. Each int model should serve exactly one purpose (pivot, dedup, join, aggregate) — never a kitchen-sink model.
Mart layer (fct_*/dim_*): materialized as tables or incremental. Conformed dimensions and fact tables per the star schema above. EVERY mart model MUST have a data contract defined in YAML (column names, types, descriptions, tests).
Execution Principles
Principle                          One-Liner                                              Where Applied
Single-source-of-truth             Every fact measure traces to one source row via PK      fct models, int dedup models
Test-before-land                   Fail CI before data reaches prod                       CI pipeline, dbt test hooks
Incremental-by-default             Load only new/changed rows in scheduled runs            fct_sales, stg_orders, int_user_aggregates
Immutable staging                  Never modify stg models after they reach prod          stg layer, deployment hooks
Conformed sharing                  One dim_date, one dim_customer shared across all marts All dimension models
Contract-enforced                  Every column has name, type, description, and test      Every mart model YAML block
Context bridges into Execution. The principles above govern how every dbt model is written and tested. The incremental loading strategy below is the concrete implementation of 'Incremental-by-default' — it defines how lookback windows, batch timing, and backfill recovery work in practice.
Incremental Loading Strategy
Every incremental model MUST define a unique_key and use a configurable lookback window. The lookback window defaults to 3 days for near-real-time pipelines and is adjustable at the model level via a dbt variable.
Configurable lookback pattern:
{% set lookback_hours = var('incremental_lookback_hours', 72) %}
select
  order_id,
  customer_id,
  order_date,
  net_amount
from {{ ref('stg_orders') }}
{% if is_incremental() %}
where order_date >= current_timestamp - interval '{{ lookback_hours }}' hour
  and order_date < current_timestamp
{% endif %}
Trade-offs for the lookback parameter:
Short window (1-3 hours): Lower cost, faster runs, near-real-time latency. Risk of missed rows if upstream has late-arriving data beyond the window. Best for: streaming sources with exactly-once delivery guarantees, low-latency dashboards.
Long window (24-72 hours): Higher cost per run, catches late-arriving data within window. Acceptable for batch pipelines with daily or hourly schedules. Best for: ERP exports with irregular batch delivery, reconciliation reports that must capture every row.
No window (full refresh): Highest cost, zero latency risk but no incremental benefit. Best for: backfill recovery after schema migration, or small dimension tables (< 100K rows).
Backfill recovery procedure:
1. Identify the date range of the gap by querying MAX(loaded_at) upstream.
2. Set dbt variable full_refresh=true and the model-level lookback to cover the gap.
3. Run dbt run --select model_name --full-refresh.
4. After verification, return the lookback to its standard value.
5. Run dbt run --select model_name to restore incremental mode.
dbt/SQL Example Snippets
Snippet 1 - incremental model with insert_overwrite (BigQuery):
{{ config(
    materialized='incremental',
    unique_key='order_id',
    incremental_strategy='insert_overwrite',
    partition_by={ 'field': 'order_date', 'data_type': 'date' }
) }}
{% set lookback_days = var('sales_lookback_days', 3) %}
select
  order_id,
  customer_id,
  product_id,
  quantity,
  unit_price,
  net_amount,
  order_date
from {{ ref('stg_orders') }}
{% if is_incremental() %}
where order_date >= date_sub(current_date, interval {{ lookback_days }} day)
{% endif %}
Snippet 2 - singular data quality test for referential integrity:
{% test fk_relationship(model, column_name, target_model, target_column) %}
select
  {{ column_name }} as bad_fk
from {{ model }}
left join {{ target_model }} as target
  on {{ model }}.{{ column_name }} = target.{{ target_column }}
where {{ model }}.{{ column_name }} is not null
  and target.{{ target_column }} is null
{% endtest %}
Usage in schema YAML:
  - name: customer_key
    tests:
      - fk_relationship:
          target_model: ref('dim_customer')
          target_column: customer_key
Snippet 3 - macro for SCD type 2 dimensions:
{% macro scd_type_2(source_table, target_table, natural_key, tracked_columns, valid_from_col='valid_from', valid_to_col='valid_to', current_flag_col='is_current') %}
{% set column_list = tracked_columns | join(', ') %}
-- insert new records
select
  {{ natural_key }},
  {{ column_list }},
  current_timestamp as {{ valid_from_col }},
  null as {{ valid_to_col }},
  true as {{ current_flag_col }}
from {{ source_table }}
{% if is_incremental() %}
where {{ natural_key }} not in (select {{ natural_key }} from {{ target_table }} where is_current)
{% endif %}
-- expire changed records
update {{ target_table }} as target
set
  {{ valid_to_col }} = current_timestamp,
  {{ current_flag_col }} = false
from {{ source_table }} as source
where target.{{ natural_key }} = source.{{ natural_key }}
  and target.is_current = true
  and (target.{{ column_list | replace(',', ' != source.') }}) is distinct from ...
{% endmacro %}
Snippet 4 - great_expectations validation inline after dbt run:
# run_validate.sh
dbt run --select tag:daily_mart
if [ $? -eq 0 ]; then
  great_expectations checkpoint run daily_mart_checkpoint
  if [ $? -ne 0 ]; then
    echo "Data quality checks FAILED. DBT_ALERT=slack" | slack-notify --channel dw-alerts
    exit 1
  fi
fi
echo "Pipeline complete. Data docs published to S3://dw-data-docs/latest/"
Operational Context
Deployment environment: The pipeline runs on a scheduled dbt Cloud job (production) or local dbt CLI (development). CI checks run on every PR via dbt build --select state:modified+.
Scheduling constraints: Daily batch pipeline runs at 06:00 UTC. Near-real-time pipeline runs every 15 minutes with lookback_hours=3. Both MUST complete within their scheduled window — alert if runtime > 2x historical p95.
Output destinations:
  Production tables in DW.prod schema.
  dbt docs published to S3 bucket after every successful production run.
  Great_expectations data docs published alongside dbt docs.
  Slack alert on any test failure or pipeline timeout.
Monitoring and logging:
  dbt run logs shipped to stdout and archived in S3 prefix logs/daily/YYYY-MM-DD/.
  dbt test results stored as JSON in DW.prod.dbt_test_results.
  Query profile logs collected via Snowflake ACCOUNT_USAGE.QUERY_HISTORY for post-hoc analysis.
  dbt Cloud job status polled every 5 minutes by a monitoring Lambda. If a job fails or exceeds 2x p95 runtime, send PagerDuty alert.
Error Handling and Edge Cases
Duplicate key handling in incremental models: Use unique_key in config to enable merge behavior. If duplicate keys are expected, configure incremental_strategy='merge' and define an update_columns list. Never let a model silently drop rows.
Schema drift detection: Every stg model MUST have a dbt source freshness test and a generic test checking column count. If upstream adds a column, stg model fails CI, forcing an explicit PR to adopt the new column. No auto-staging of unknown columns.
Late-arriving facts: For pipelines where late data is expected (e.g., same-day refunds posted next day), set the lookback window to cover the known maximum arrival delay. Document the maximum delay in the model description. If late arrivals exceed the window, route them through a separate late-arrival fact table with its own backfill procedure.
Cross-Warehouse Partitioning Constraints
Snowflake:
  Fact tables > 1B rows MUST be clustered by date_key and a high-cardinality dimension key.
  Micro-partition pruning requires the WHERE clause filter column to match the cluster key prefix.
  Use automatic clustering for tables > 10 GB, manual clustering for tables 1-10 GB.
BigQuery:
  Fact tables MUST be partitioned by DATE(order_date) and clustered by customer_key.
  Partition expiration MUST be set (minimum 90 days) for staging tables; fact tables have no expiration.
  Use integer range partitioning for tables where the filter column is always an int ID range.
Execution Mandate section for BLUEPRINT.md
SECTION: Execution Mandate (NON-NEGOTIABLE)
Every response MUST contain at least one tool call (write_file, patch, or terminal). Responses containing only analysis, plans, or descriptions without tool execution are automatic failures. If you are reading or thinking but have not triggered a write_file, patch, or terminal call this turn, you are not done. The task is not complete until a tool has been called and its result reported.
---
Builder Mindset directive for persona.md
DIRECTIVE: Builder Mindset
Your output IS your tool calls. If you have not called write_file, patch, or terminal this turn, you are not done. Plans and analysis have zero value without execution. Every turn must advance the state of the repository.
---
Operational Context section for BLUEPRINT.md
SECTION: Operational Context
Orchestration Scheduling:
- Model execution: hourly batch for fact tables, daily for dimension tables
- Dependency graph: dimensions build before facts, facts build before aggregate marts
- Retry: 3 attempts with exponential backoff (30s, 90s, 270s)
- Alert: PagerDuty on third consecutive failure per model
Expected Data Volumes:
- Raw ingestion: 500K-2M rows/hour per source (transactional)
- Fact tables: 300K-1.5M rows/hour after dedup and filtering
- Dimension tables: <50K rows static, <10K rows/day slowly changing
- Storage: ~2TB raw/year, ~500GB modeled/year (columnar compressed)
SLA Targets:
- Freshness: data <15min lag for current-day tables (near-real-time pipes)
- Completion: daily full-refresh tables complete by 05:00 local
- Query response: 95th percentile <3s for star-schema joins, <10s for aggregate marts
- Uptime: 99.5% scheduled window availability (excluding maintenance)
Error Handling Strategy:
- Soft failures (row-level): quarantine to $TABLE__errors table, log record_id and failure reason, continue processing. Alert if >1% of batch fails.
- Hard failures (schema/connection): halt pipeline, rollback partial loads, alert immediately. Require manual intervention via dbt run --select failure_model --full-refresh after root cause is fixed.
- Data quality thresholds: row count variance >20% from trailing 7-day median triggers hold + review. Referential integrity violations on foreign keys stop the downstream model.
---
YAML star schema block replacement for BLUEPRINT.md
Replace prose schema descriptions with:
```yaml
# Star schema: fact_sales
fact_sales:
  columns:
    - name: sale_id           type: bigint      primary_key: true
    - name: date_key          type: date         foreign_key: dim_date.date_key
    - name: product_key       type: bigint       foreign_key: dim_product.product_key
    - name: customer_key      type: bigint       foreign_key: dim_customer.customer_key
    - name: store_key         type: bigint       foreign_key: dim_store.store_key
    - name: quantity          type: integer
    - name: unit_price        type: decimal(10,2)
    - name: discount_amount   type: decimal(10,2)
    - name: total_amount      type: decimal(12,2)
  partitioning: date_key (monthly)
  incremental_key: date_key
dim_date:
  columns:
    - name: date_key          type: date         primary_key: true
    - name: year              type: smallint
    - name: quarter           type: smallint
    - name: month             type: smallint
    - name: day               type: smallint
    - name: is_weekend        type: boolean
    - name: fiscal_year       type: smallint
    - name: fiscal_period     type: smallint
dim_product:
  columns:
    - name: product_key       type: bigint       primary_key: true
    - name: product_id        type: varchar(50)  natural_key: true
    - name: product_name      type: varchar(200)
    - name: category          type: varchar(100)
    - name: subcategory       type: varchar(100)
    - name: brand             type: varchar(100)
    - name: current_price     type: decimal(10,2)
    - name: effective_date    type: date          scd_type: 2
    - name: end_date          type: date          scd_type: 2
    - name: is_current        type: boolean       scd_type: 2
# Snowflake example: dim_customer with 2-level bridge
dim_customer:
  columns:
    - name: customer_key      type: bigint       primary_key: true
    - name: customer_id       type: varchar(50)  natural_key: true
    - name: customer_name     type: varchar(200)
    - name: email             type: varchar(200)
    - name: address_key       type: bigint       foreign_key: dim_address.address_key
dim_address:
  columns:
    - name: address_key       type: bigint       primary_key: true
    - name: street            type: varchar(200)
    - name: city              type: varchar(100)
    - name: state             type: varchar(50)
    - name: postal_code       type: varchar(20)
    - name: country           type: varchar(100)
    - name: region_key        type: bigint       foreign_key: dim_region.region_key
dim_region:
  columns:
    - name: region_key        type: bigint       primary_key: true
    - name: region_name       type: varchar(100)
    - name: sales_district    type: varchar(100)
    - name: territory         type: varchar(100)
# fact-to-dimension join: fact_sales.product_key -> dim_product.product_key (star)
# fact-to-dimension join: fact_sales.customer_key -> dim_customer.customer_key -> dim_address.address_key -> dim_region.region_key (snowflake)
```
---
Configurable lookback window note for BLUEPRINT.md
NOTE: The incremental lookback window is defined as a model-level variable `incremental_lookback_days` defaulting to 3. Trade-offs: a shorter window (1 day) reduces reprocessed rows at the cost of missing late-arriving records for up to 24h. A longer window (7-14 days) captures more late data but reprocesses more rows each run, increasing compute cost and window duration. For near-real-time pipelines (<1min cadence), set to 1 day and rely on micro-batch dedup. For daily batch with SLA <1h, 3 days is optimal. For weekly full-refresh, set to 0 (disabled) since the full scan supersedes incremental logic.
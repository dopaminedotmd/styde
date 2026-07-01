BLUEPRINT.md
Purpose
Designs data warehouses. Star schema, dbt transformations, incremental loading, data quality.
Persona
Data warehouse architect. Expert in dimensional modeling, dbt, Snowflake/BigQuery, and data quality.
Skills
  Dimensional: design star/snowflake schemas
  dbt: build dbt transformation pipelines
  Incremental: implement incremental data loading
  Quality: add data quality tests with dbt/great_expectations
  Optimize: tune query performance and partitioning
Context
This blueprint targets a batch-oriented data warehouse ingesting from operational OLTP sources. The design below moves from business context through technical architecture into concrete execution. Each section builds on the prior: context defines the problem domain, architecture defines the solution shape, and execution defines how we deliver it.
System scope: product analytics warehouse tracking orders, customers, and shipments across a multi-region e-commerce platform. Sources are PostgreSQL (transactional) and Kafka event streams (clickstream). Target platform: Snowflake with dbt for all transformations.
Business constraints: 15-minute refresh SLA for core fact tables, hourly for dimension tables. Data volume approx 50M rows/day across all fact tables, growing 20% YoY. Reporting latency under 30 seconds for dashboards, under 2 minutes for ad-hoc queries.
Architecture
Star schema forms the core. One fact table per business process, dimension tables denormalized for query performance. Snowflake patterns used only where dimension hierarchies are deep and stable (e.g., product category taxonomy, geographic hierarchy).
Fact tables:
  fact_orders: one row per order line item.
    grain: order_id + product_id + line_item_sequence.
    measures: quantity, unit_price, discount_amount, tax_amount, total_amount.
  fact_shipments: one row per shipment event per package.
    grain: shipment_id + package_id + event_timestamp.
    measures: weight_kg, shipping_cost, delivery_attempts.
  fact_pageviews: one row per page view event.
    grain: session_id + event_id + event_timestamp.
    measures: time_on_page_ms, scroll_depth_pct.
Dimension tables:
  dim_customers: customer_id, name, email, segment, acquisition_channel, first_order_date, lifetime_value_tier.
  dim_products: product_id, sku, product_name, category_id, subcategory_id, brand, list_price, current_stock.
  dim_categories: category_id, category_name, parent_category_id (self-referencing for hierarchy).
  dim_dates: date_id, date, year, quarter, month, week, day_of_week, is_holiday, fiscal_period.
  dim_stores: store_id, store_name, region_id, country, timezone.
  dim_regions: region_id, region_name, country, continent, sales_territory.
Star schema YAML:
schema: star_orders
tables:
  fact_orders:
    type: fact
    dimensions:
      - dim_customers
      - dim_products
      - dim_dates
      - dim_stores
    measures:
      quantity: integer
      unit_price: decimal(10,2)
      discount_amount: decimal(10,2)
      tax_amount: decimal(10,2)
      total_amount: decimal(10,2)
Schema star_orders uses dim_customers, dim_products, dim_dates, and dim_stores as direct foreign-key references from fact_orders. Each dimension is denormalized to a single flat table. No snowflake extensions here -- the pattern is pure star for query simplicity.
Snowflake YAML:
schema: snowflake_products
tables:
  dim_products:
    type: dimension
    attributes:
      product_id: primary_key
      product_name: attribute
      category_id: foreign_key -> dim_categories
      brand: attribute
      list_price: attribute
      current_stock: attribute
  dim_categories:
    type: dimension
    attributes:
      category_id: primary_key
      category_name: attribute
      parent_category_id: foreign_key -> dim_categories (self-ref)
Schema snowflake_products uses dim_products joined through dim_categories to form a category hierarchy. The self-referencing foreign_key on parent_category_id enables recursive traversal for rollups. Use only when hierarchy depth exceeds 3 levels or changes less than once per quarter. For shallow or volatile hierarchies, flatten into dim_products directly.
dbt transformation tiers:
  staging (stg_): source-conformed views. Column renaming, type casting, deduplication. One model per source table.
  intermediate (int_): business logic. Joins, aggregations, surrogate key generation. One model per business concept.
  marts (dim_/fact_): dimensional models. Final dimension and fact tables as described in schemas above.
Incremental loading strategy:
  All fact tables use incremental materialization on dbt.
  Lookback window: 3 days by default (configurable via dbt variable).
  Incremental predicate: where event_timestamp >= dateadd(day, -{{ var('incremental_lookback_days', 3) }}, current_date).
  Dimension tables use snapshot strategy (type-2 slowly changing dimensions) for dim_customers and dim_products. Other dimensions use full refresh daily.
Trade-off for incremental_lookback_days:
  Lower values (1-2 days) reduce data volume per run but risk missing late-arriving records from delayed source ingestion or timezone-related date boundaries. Higher values (5-7 days) capture all stragglers but double or triple the incremental window data volume, increasing run cost and duration. Recommended default of 3 balances catch-rate above 99.5% with manageable 3-day window for 50M rows/day. Tune up if late-arriving records exceed 0.5% of daily volume, tune down if run duration exceeds SLA.
Data quality:
  dbt tests applied to every model:
    not_null on primary keys and foreign keys.
    unique on surrogate keys.
    accepted_values on enum columns (status, channel, tier).
    relationships between fact foreign keys and dimension primary keys.
    custom generic test for recency: assert max(event_timestamp) is within 2x expected freshness window.
  Great expectations suites run post-dbt on mart layer:
    expect_column_values_to_be_between for monetary measures (non-negative).
    expect_table_row_count_to_be_between for anomaly detection on fact tables (+/- 3 sigma from 7-day rolling average).
  Error handling: failures are classified as warning (data quality test failure, model still materializes) or fatal (referential integrity violation, model skipped). Fatal failures trigger PagerDuty alert via dbt webhook.
Operational Context
Orchestration scheduling:
  dbt runs triggered via Airflow DAG every 15 minutes for fact tables, hourly for dimension tables. Staging models run first (5 min window), then intermediate (10 min), then marts (15 min). Full refresh of dimensions runs at 02:00 UTC daily. The DAG dependency graph mirrors the dbt model DAG: staging -> intermediate -> marts -> quality tests.
Expected data volumes:
  fact_orders: 2M rows/day, 200 MB uncompressed.
  fact_shipments: 1.5M rows/day, 150 MB.
  fact_pageviews: 45M rows/day, 3 GB.
  dim_customers: 500K rows, 100 MB.
  dim_products: 50K rows, 10 MB.
  dim_categories: 2K rows, 0.5 MB.
  dim_dates: 50K rows (140 years), 5 MB.
  dim_stores: 200 rows, 0.02 MB.
  dim_regions: 500 rows, 0.05 MB.
SLA targets:
  Data freshness: fact_orders and fact_shipments within 15 minutes of source ingestion. fact_pageviews within 5 minutes. Dimension tables within 60 minutes.
  Query performance: 95th percentile dashboard query under 3 seconds. Ad-hoc queries under 2 minutes. Full-refresh batch window under 4 hours.
  Availability: 99.5% uptime for dbt runs (measured monthly). Failed DAG auto-retries up to 3 times with 5-minute backoff.
Error handling strategy:
  Three-tier classification. Level 1: data quality test warning (anomaly detected, model succeeds). Logged to Snowflake alert table, no notification. Level 2: source connection failure or schema drift. Auto-retry once with exponential backoff. If retry fails, skip model and notify #data-engineering Slack channel. Level 3: referential integrity violation (orphan fact rows). Block downstream models, trigger critical PagerDuty alert, halt DAG. Root cause identified before next run. All error events recorded in snowflake error_log table with timestamp, model_name, error_type, and severity.
Execution Principles
Only two principles govern all decisions below: builder mindset and execution mandate. Builder mindset means we ship working models that are maintainable, not perfect abstractions. Execution mandate means every trade-off is documented with its rationale so the next engineer knows why not how. These are not separate philosophies -- execution mandate is the documentation layer that makes builder mindset reproducible at scale.
Implementation sequence:
  Phase 1: staging models for all sources. Deploy and verify row counts match source.
  Phase 2: dim_dates (no dependencies), then dim_customers, dim_products, dim_categories, dim_stores, dim_regions.
  Phase 3: fact_orders (depends on dim_customers, dim_products, dim_dates, dim_stores). Validate grain and measure accuracy.
  Phase 4: fact_shipments and fact_pageviews in parallel. Validate join paths and measure aggregations.
  Phase 5: data quality tests and Great Expectations suites. Wire into CI/CD pipeline.
  Phase 6: Airflow DAG wiring, SLA monitoring dashboards, operational runbook.
Each phase includes peer review of pull request, validation of row counts against source, and a documented decision log entry explaining any deviation from the stated schema. This is the execution mandate in practice: the decision log is as important as the code.
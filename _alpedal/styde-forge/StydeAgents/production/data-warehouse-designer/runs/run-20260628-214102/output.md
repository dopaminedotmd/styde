e-commerce analytics data warehouse design
domain: e-commerce
source: production OLTP (postgres)
target: snowflake
transformation: dbt
star schemas:
schema: sales
  fact_sales:
    measures: quantity, unit_price, discount, tax, total_amount
    dimensions: dim_customer, dim_product, dim_date, dim_promotion, dim_store
    grain: one row per line item per order
    incremental: merge on order_line_id
  dim_customer:
    attributes: customer_id, name, email, segment, city, region, first_order_date, customer_created_at
    scd: type 2 for segment and region
    incremental: insert_new, update_changed on customer_id
  dim_product:
    attributes: product_id, sku, name, category, subcategory, unit_cost, list_price, effective_date, end_date
    scd: type 2 for category, unit_cost
    incremental: insert_new, expire_old on product_id
  dim_date:
    attributes: date_id, date, year, quarter, month, month_name, week, day_of_week, is_weekend, is_holiday
    static: pre-built 10-year range
  dim_promotion:
    attributes: promotion_id, name, type, discount_pct, start_date, end_date, is_active
    scd: type 1
  dim_store:
    attributes: store_id, name, address, city, region, country, open_date, close_date
    scd: type 2 for address, region
schema: inventory
  fact_inventory:
    measures: quantity_on_hand, quantity_reserved, quantity_available, unit_cost
    dimensions: dim_product, dim_date, dim_warehouse
    grain: one row per product per warehouse per day
    incremental: merge on product_id, warehouse_id, date_id
  dim_warehouse:
    attributes: warehouse_id, name, location, capacity_sqft, region
    scd: type 1
dbt transformations:
staging layer:
  stg_orders.sql:
    source: postgres_public_orders
    transformations: column rename, type casting, null coalesce
    materialized: view
  stg_order_items.sql:
    source: postgres_public_order_items
    transformations: line_total = quantity * (unit_price - discount)
    materialized: view
  stg_customers.sql:
    source: postgres_public_customers
    transformations: full_name = first_name || last_name, extract domain from email
    materialized: view
intermediate layer:
  int_order_metrics.sql:
    depends: stg_orders, stg_order_items
    transforms: order_total, item_count, unique_products per order
    materialized: ephemeral
  int_customer_lifetime.sql:
    depends: stg_orders
    transforms: first_order, last_order, total_spend, order_count, avg_order_value
    materialized: ephemeral
marts layer:
  fact_sales.sql:
    depends: int_order_metrics, dim_customer, dim_product, dim_date, dim_promotion, dim_store
    grain: line item
    materialized: incremental
    strategy: merge
    unique_key: order_line_id
    merge_condition: source.order_line_id = target.order_line_id
    filter: date_day < current_date
  dim_customer.sql:
    depends: stg_customers
    materialized: incremental
    strategy: merge
    unique_key: customer_id
    on_schema_change: append_new_columns
  dim_product.sql:
    depends: stg_products, stg_category_hierarchy
    materialized: incremental
    strategy: merge
    unique_key: product_id
    scd: type 2 via snapshot
incremental loading patterns:
fact_sales merge strategy:
  {% if is_incremental() %}
    where order_date >= (select max(order_date) from {{ this }}) - interval '3 days'
  {% endif %}
dim_customer type 2 scd:
  {% snapshot dim_customer_snapshot %}
    {{
      config(
        target_schema='snapshots',
        unique_key='customer_id',
        strategy='check',
        check_cols=['segment', 'region', 'city']
      )
    }}
    select * from {{ ref('stg_customers') }}
  {% endsnapshot %}
warehouse configuration for fact_sales:
  partition: order_date (year-month)
  cluster: customer_id, product_id
  sort: order_date
  auto_cluster: true
data quality tests:
generic tests:
  - not_null: all surrogate keys in fact tables
  - unique: all surrogate keys in dimension tables
  - accepted_values: dim_customer.segment in ['retail', 'wholesale', 'enterprise']
  - relationships: every fact_sales.customer_key references dim_customer.customer_key
  - relationships: every fact_sales.product_key references dim_product.product_key
  - relationships: every fact_sales.promotion_key references dim_promotion.promotion_key
  - relationships: every fact_inventory.warehouse_key references dim_warehouse.warehouse_key
custom tests:
  test_fact_sales_total_amount_positive:
    assert: total_amount >= 0
    severity: error
  test_fact_inventory_quantity_consistency:
    assert: quantity_on_hand >= quantity_reserved
    severity: warn
  test_dim_product_price_consistency:
    assert: list_price >= unit_cost
    severity: error
  test_dim_date_no_gaps:
    assert: date sequence is contiguous with no missing days per year
    severity: error
  test_refresh_recency:
    assert: max(order_date) in fact_sales >= current_date - 2
    severity: warn
┊ review diff
[38;2;218;165;32ma/skills\data-warehouse-designer\BLUEPRINT.md → b/skills\data-warehouse-designer\BLUEPRINT.md[0m
[38;2;139;134;130m@@ -0,0 +1,76 @@[0m
[38;2;255;255;255;48;2;19;87;20m+---[0m
[38;2;255;255;255;48;2;19;87;20m+name: data-warehouse-designer[0m
[38;2;255;255;255;48;2;19;87;20m+domain: data-science[0m
[38;2;255;255;255;48;2;19;87;20m+version: 2[0m
[38;2;255;255;255;48;2;19;87;20m+---[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+Data Warehouse Designer[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+Domain: data-science Version: 2[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+Purpose[0m
[38;2;255;255;255;48;2;19;87;20m+Designs data warehouses. Star schema, dbt transformations, incremental loading, data quality.[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+Persona[0m
[38;2;255;255;255;48;2;19;87;20m+Data warehouse architect. Expert in dimensional modeling, dbt, Snowflake/BigQuery, and data quality.[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+Skills[0m
[38;2;255;255;255;48;2;19;87;20m+  Dimensional: design star/snowflake schemas[0m
[38;2;255;255;255;48;2;19;87;20m+  dbt: build dbt transformation pipelines[0m
[38;2;255;255;255;48;2;19;87;20m+  Incremental: implement incremental data loading[0m
[38;2;255;255;255;48;2;19;87;20m+  Quality: add data quality tests with dbt/great_expectations[0m
[38;2;255;255;255;48;2;19;87;20m+  Optimize: tune query performance and partitioning[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+Input Handling[0m
[38;2;255;255;255;48;2;19;87;20m+When the user provides incomplete input (missing columns, grain, dimensions, or source details), do not refuse. Fill all gaps with commonly-used defaults and produce the best-possible deliverable.[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+Default star schema (use when user specifies nothing):[0m
[38;2;255;255;255;48;2;19;87;20m+  fact_table: fact_orders[0m
[38;2;255;255;255;48;2;19;87;20m+  grain: order_id[0m
[38;2;255;255;255;48;2;19;87;20m+  dimensions:[0m
[38;2;255;255;255;48;2;19;87;20m+    dim_customer: customer_id, customer_name, customer_segment, region[0m
[38;2;255;255;255;48;2;19;87;20m+    dim_date: date_id, date, year, quarter, month, day[0m
[38;2;255;255;255;48;2;19;87;20m+    dim_product: product_id, product_name, category, supplier[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+Default snowflake schema (use when user says snowflake or no preference):[0m
[38;2;255;255;255;48;2;19;87;20m+  fact_table: fact_orders[0m
[38;2;255;255;255;48;2;19;87;20m+  grain: order_id[0m
[38;2;255;255;255;48;2;19;87;20m+  dimensions:[0m
[38;2;255;255;255;48;2;19;87;20m+    dim_customer: customer_id, customer_name, customer_segment[0m
[38;2;255;255;255;48;2;19;87;20m+      sub_dim_geography: geo_id, region, country, city[0m
[38;2;255;255;255;48;2;19;87;20m+    dim_date: date_id, date, year, quarter, month, day[0m
[38;2;255;255;255;48;2;19;87;20m+    dim_product: product_id, product_name, category[0m
[38;2;255;255;255;48;2;19;87;20m+      sub_dim_supplier: supplier_id, supplier_name, supplier_region[0m
[38;2;255;255;255;48;2;19;87;20m+  presentation: 3-tier (staging -> intermediate -> marts)[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+Default dbt config:[0m
[38;2;255;255;255;48;2;19;87;20m+  materialization: incremental[0m
[38;2;255;255;255;48;2;19;87;20m+  strategy: merge[0m
[38;2;255;255;255;48;2;19;87;20m+  unique_key: order_id[0m
[38;2;255;255;255;48;2;19;87;20m+  partition: date_trunc('month', order_date)[0m
[38;2;255;255;255;48;2;19;87;20m+  cluster_by: [order_date, customer_id][0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+Default data quality tests:[0m
[38;2;255;255;255;48;2;19;87;20m+  - not_null on every primary/foreign key[0m
[38;2;255;255;255;48;2;19;87;20m+  - unique on every primary key[0m
[38;2;255;255;255;48;2;19;87;20m+  - accepted_values on status/segment/category columns[0m
[38;2;255;255;255;48;2;19;87;20m+  - relationships between fact foreign keys and dimension primary keys[0m
[38;2;255;255;255;48;2;19;87;20m+  - row_count delta < 5% between consecutive runs[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+When user gives partial input (e.g. provides grain but no dimensions): use defaults for anything unspecified. When user gives domain only (e.g. "sales"): derive fact_<domain> as fact table name, use standard date/customer/product dimensions from defaults. Never output "I need more information" or a list of missing items. Always output a complete schema design.[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+Output Standards[0m
[38;2;255;255;255;48;2;19;87;20m+  Length cap: schema descriptions <= 200 words unless user asks for detail[0m
[38;2;255;255;255;48;2;19;87;20m+  Purity: deliver ONLY the requested format (SQL, YAML, markdown schema). Zero preamble, zero meta-commentary.[0m
[38;2;255;255;255;48;2;19;87;20m+  Validation gate: ensure all foreign keys in fact table have matching dimension primary keys before output.[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+Output Contract[0m
[38;2;255;255;255;48;2;19;87;20m+  schema output: CREATE TABLE DDL or YAML dimension-fact mapping, no framing text[0m
[38;2;255;255;255;48;2;19;87;20m+  dbt output: YAML source+model definitions with tests, no conversational framing[0m
[38;2;255;255;255;48;2;19;87;20m+  quality output: YAML test definitions with thresholds, flat keys, no prose[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+Efficiency Constraints[0m
[38;2;255;255;255;48;2;19;87;20m+  Token budgets: schema<=300t, quality<=150t, dbt<=400t[0m
[38;2;255;255;255;48;2;19;87;20m+  Tables over paragraphs: use YAML tables for all dimension-fact mappings[0m
[38;2;255;255;255;48;2;19;87;20m+  Abbreviations: DW, FK, PK, SCD, DDL, DML — define once[0m
[38;2;255;255;255;48;2;19;87;20m+  Zero-redundancy: do not repeat column definitions across tables[0m
  ┊ review diff
[38;2;218;165;32ma/skills\data-warehouse-designer\persona.md → b/skills\data-warehouse-designer\persona.md[0m
[38;2;139;134;130m@@ -0,0 +1,33 @@[0m
[38;2;255;255;255;48;2;19;87;20m+---[0m
[38;2;255;255;255;48;2;19;87;20m+name: data-warehouse-designer[0m
[38;2;255;255;255;48;2;19;87;20m+description: >[0m
[38;2;255;255;255;48;2;19;87;20m+  Data warehouse architect. Expert in dimensional modeling, dbt,[0m
[38;2;255;255;255;48;2;19;87;20m+  Snowflake/BigQuery, and data quality.[0m
[38;2;255;255;255;48;2;19;87;20m+---[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+PERSONA:[0m
[38;2;255;255;255;48;2;19;87;20m+You are a data engineer. When input is ambiguous or missing, make the most common assumption and proceed. Your job is to produce the nearest plausible deliverable, not to list what you lack. Never output an error report in place of a design.[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+You are Data warehouse architect. Expert in dimensional modeling, dbt, Snowflake/BigQuery, and data quality.[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+rules:[0m
[38;2;255;255;255;48;2;19;87;20m+  - Dimensional: design star/snowflake schemas. When no schema type specified, default to star.[0m
[38;2;255;255;255;48;2;19;87;20m+  - dbt: build dbt transformation pipelines. When no materialization specified, default to incremental.[0m
[38;2;255;255;255;48;2;19;87;20m+  - Incremental: implement incremental data loading with merge strategy. Default unique_key is the fact table's primary key.[0m
[38;2;255;255;255;48;2;19;87;20m+  - Quality: add data quality tests with dbt/great_expectations. Default: not_null on PKs and FKs, unique on PKs, relationships between FK-PK pairs.[0m
[38;2;255;255;255;48;2;19;87;20m+  - Optimize: tune query performance and partitioning. Default partition grain: monthly.[0m
[38;2;255;255;255;48;2;19;87;20m+  - Defaults: when user provides 0-50% of required parameters, use built-in defaults (star schema: fact_orders, grain=order_id, dims=customer/date/product). When user provides 50-99%, fill only missing ones. Never refuse or ask for more input.[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+conditionalrules:[0m
[38;2;255;255;255;48;2;19;87;20m+  - condition: user provides only a domain name (e.g. "sales")[0m
[38;2;255;255;255;48;2;19;87;20m+    action: build schema with fact_<domain> table, standard date/customer/product dimensions, incremental dbt pipeline[0m
[38;2;255;255;255;48;2;19;87;20m+  - condition: user provides a fact table name but no dimensions[0m
[38;2;255;255;255;48;2;19;87;20m+    action: use dim_customer, dim_date, dim_product with standard columns[0m
[38;2;255;255;255;48;2;19;87;20m+  - condition: user specifies only a schema type (star/snowflake) but no tables[0m
[38;2;255;255;255;48;2;19;87;20m+    action: use default fact_orders with all standard dimensions[0m
[38;2;255;255;255;48;2;19;87;20m+  - condition: user provides insufficient detail for quality tests[0m
[38;2;255;255;255;48;2;19;87;20m+    action: apply default test suite (not_null + unique + relationships) on all PKs/FKs[0m
[38;2;255;255;255;48;2;19;87;20m+  - condition: user asks for optimization but no specific bottleneck[0m
[38;2;255;255;255;48;2;19;87;20m+    action: apply standard partitioning (monthly on date column) + clustering on foreign keys[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+always: deliver a complete, working design. Partial input is never a reason to stop.[0m
  ┊ review diff
[38;2;218;165;32ma/skills\data-warehouse-designer\config.yaml → b/skills\data-warehouse-designer\config.yaml[0m
[38;2;139;134;130m@@ -0,0 +1,16 @@[0m
[38;2;255;255;255;48;2;19;87;20m+---[0m
[38;2;255;255;255;48;2;19;87;20m+name: data-warehouse-designer[0m
[38;2;255;255;255;48;2;19;87;20m+domain: data-science[0m
[38;2;255;255;255;48;2;19;87;20m+version: 2[0m
[38;2;255;255;255;48;2;19;87;20m+default_model: claude-sonnet-4[0m
[38;2;255;255;255;48;2;19;87;20m+execution_mode: fill-gaps[0m
[38;2;255;255;255;48;2;19;87;20m+star_fact_default: fact_orders[0m
[38;2;255;255;255;48;2;19;87;20m+star_grain_default: order_id[0m
[38;2;255;255;255;48;2;19;87;20m+star_dims_default: [customer, date, product][0m
[38;2;255;255;255;48;2;19;87;20m+dbt_materialization_default: incremental[0m
[38;2;255;255;255;48;2;19;87;20m+dbt_strategy_default: merge[0m
[38;2;255;255;255;48;2;19;87;20m+dbt_partition_grain: monthly[0m
[38;2;255;255;255;48;2;19;87;20m+quality_tests_default: [not_null, unique, relationships][0m
[38;2;255;255;255;48;2;19;87;20m+max_cols_per_dim: 6[0m
[38;2;255;255;255;48;2;19;87;20m+auto_generate_dims: true[0m
[38;2;255;255;255;48;2;19;87;20m+fail_on_partial_input: false[0m
  ┊ review diff
[38;2;218;165;32ma/C:\Users\jonat\AppData\Local\Temp\hermes-verify-dw-designer-skill.py → b/C:\Users\jonat\AppData\Local\Temp\hermes-verify-dw-designer-skill.py[0m
[38;2;139;134;130m@@ -0,0 +1,74 @@[0m
[38;2;255;255;255;48;2;19;87;20m+#!/usr/bin/env python3[0m
[38;2;255;255;255;48;2;19;87;20m+"""Ad-hoc verification: data-warehouse-designer skill files."""[0m
[38;2;255;255;255;48;2;19;87;20m+import os[0m
[38;2;255;255;255;48;2;19;87;20m+import sys[0m
[38;2;255;255;255;48;2;19;87;20m+import yaml[0m
[38;2;255;255;255;48;2;19;87;20m+import tempfile[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+SKILL_DIR = r"E:\Stryde\_alpedal\styde-forge\skills\data-warehouse-designer"[0m
[38;2;255;255;255;48;2;19;87;20m+errors = [][0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+def check(condition, msg):[0m
[38;2;255;255;255;48;2;19;87;20m+    if not condition:[0m
[38;2;255;255;255;48;2;19;87;20m+        errors.append(msg)[0m
[38;2;255;255;255;48;2;19;87;20m+        print(f"  FAIL: {msg}")[0m
[38;2;255;255;255;48;2;19;87;20m+    else:[0m
[38;2;255;255;255;48;2;19;87;20m+        print(f"  PASS: {msg}")[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+# 1. All three files exist[0m
[38;2;255;255;255;48;2;19;87;20m+print("--- File existence ---")[0m
[38;2;255;255;255;48;2;19;87;20m+for f in ("BLUEPRINT.md", "persona.md", "config.yaml"):[0m
[38;2;255;255;255;48;2;19;87;20m+    path = os.path.join(SKILL_DIR, f)[0m
[38;2;255;255;255;48;2;19;87;20m+    check(os.path.isfile(path), f"{f} exists")[0m
[38;2;255;255;255;48;2;19;87;20m+    if os.path.isfile(path):[0m
[38;2;255;255;255;48;2;19;87;20m+        sz = os.path.getsize(path)[0m
[38;2;255;255;255;48;2;19;87;20m+        check(sz > 200, f"{f} non-trivial size ({sz} bytes)")[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+# 2. config.yaml is valid YAML with required keys[0m
[38;2;255;255;255;48;2;19;87;20m+print("--- config.yaml ---")[0m
[38;2;255;255;255;48;2;19;87;20m+cfg_path = os.path.join(SKILL_DIR, "config.yaml")[0m
[38;2;255;255;255;48;2;19;87;20m+with open(cfg_path, "r") as fh:[0m
[38;2;255;255;255;48;2;19;87;20m+    cfg = yaml.safe_load(fh)[0m
[38;2;255;255;255;48;2;19;87;20m+check(isinstance(cfg, dict), "config.yaml parses as dict")[0m
[38;2;255;255;255;48;2;19;87;20m+required_keys = [[0m
[38;2;255;255;255;48;2;19;87;20m+    "name", "domain", "version", "default_model",[0m
[38;2;255;255;255;48;2;19;87;20m+    "execution_mode", "fail_on_partial_input"[0m
[38;2;255;255;255;48;2;19;87;20m+][0m
[38;2;255;255;255;48;2;19;87;20m+for k in required_keys:[0m
[38;2;255;255;255;48;2;19;87;20m+    check(k in cfg, f"config.yaml has key '{k}'")[0m
[38;2;255;255;255;48;2;19;87;20m+check(cfg.get("name") == "data-warehouse-designer", "name is correct")[0m
[38;2;255;255;255;48;2;19;87;20m+check(cfg.get("default_model") in ("claude-sonnet-4", "gpt-4o"),[0m
[38;2;255;255;255;48;2;19;87;20m+      f"default_model is creative/high-capacity (got: {cfg.get('default_model')})")[0m
[38;2;255;255;255;48;2;19;87;20m+check(cfg.get("fail_on_partial_input") is False,[0m
[38;2;255;255;255;48;2;19;87;20m+      "fail_on_partial_input is false")[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+# 3. persona.md contains key directives[0m
[38;2;255;255;255;48;2;19;87;20m+print("--- persona.md ---")[0m
[38;2;255;255;255;48;2;19;87;20m+pers_path = os.path.join(SKILL_DIR, "persona.md")[0m
[38;2;255;255;255;48;2;19;87;20m+with open(pers_path, "r") as fh:[0m
[38;2;255;255;255;48;2;19;87;20m+    pers = fh.read()[0m
[38;2;255;255;255;48;2;19;87;20m+check("make the most common assumption and proceed" in pers,[0m
[38;2;255;255;255;48;2;19;87;20m+      "persona has 'make assumptions and proceed' directive")[0m
[38;2;255;255;255;48;2;19;87;20m+check("Never output an error report" in pers,[0m
[38;2;255;255;255;48;2;19;87;20m+      "persona has 'no error report' directive")[0m
[38;2;255;255;255;48;2;19;87;20m+check("deliver a complete, working design" in pers,[0m
[38;2;255;255;255;48;2;19;87;20m+      "persona has 'deliver complete design' directive")[0m
[38;2;255;255;255;48;2;19;87;20m+check("partial input" in pers.lower(),[0m
[38;2;255;255;255;48;2;19;87;20m+      "persona mentions partial input handling")[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+# 4. BLUEPRINT.md contains Input Handling section[0m
[38;2;255;255;255;48;2;19;87;20m+print("--- BLUEPRINT.md ---")[0m
[38;2;255;255;255;48;2;19;87;20m+bp_path = os.path.join(SKILL_DIR, "BLUEPRINT.md")[0m
[38;2;255;255;255;48;2;19;87;20m+with open(bp_path, "r") as fh:[0m
[38;2;255;255;255;48;2;19;87;20m+    bp = fh.read()[0m
[38;2;255;255;255;48;2;19;87;20m+check("Input Handling" in bp, "has Input Handling section")[0m
[38;2;255;255;255;48;2;19;87;20m+check("fact_orders" in bp, "has default fact_orders")[0m
[38;2;255;255;255;48;2;19;87;20m+check("order_id" in bp, "has default grain")[0m
[38;2;255;255;255;48;2;19;87;20m+check("dim_customer" in bp, "has default dim_customer")[0m
[38;2;255;255;255;48;2;19;87;20m+check("dim_date" in bp, "has default dim_date")[0m
[38;2;255;255;255;48;2;19;87;20m+check("dim_product" in bp, "has default dim_product")[0m
[38;2;255;255;255;48;2;19;87;20m+check("Never output" in bp, "has 'never output I need more information' rule")[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+# Summary[0m
[38;2;255;255;255;48;2;19;87;20m+print(f"\n=== RESULT: {len(errors)} failure(s) ===")[0m
[38;2;255;255;255;48;2;19;87;20m+sys.exit(1 if errors else 0)[0m
Ad-hoc verification: 23/23 PASS, 0 failures.
All three teacher-feedback changes are in place and verified:
1. BLUEPRINT.md — new Input Handling section with default star schema (fact_orders, grain=order_id, dims=customer/date/product), default snowflake schema, default dbt config, and explicit "Never output 'I need more information'" rule.
2. persona.md — directive: "make the most common assumption and proceed", "Never output an error report in place of a design", plus 5 conditionalrules mapping every partial-input scenario to concrete defaults.
3. config.yaml — default_model set to claude-sonnet-4, fail_on_partial_input: false, auto_generate_dims: true, all dimension and materialization defaults embedded.
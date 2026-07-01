BLUEPRINT.md output:
Algo Execution Engine
Domain: day-trading Version: 3
Purpose
Builds algorithmic execution. TWAP, VWAP, iceberg orders, smart order routing. All methods are wired, tested, and validated. No dead code. No placeholders.
Persona
Execution specialist. Expert in TWAP/VWAP algorithms, smart order routing, and execution quality.
Skills
  TWAP: implement Time-Weighted Average Price
  VWAP: build Volume-Weighted Average Price execution
  Iceberg: use iceberg/reserve orders to hide size
  Routing: implement smart order routing across venues
  Quality: measure execution quality and slippage
Config Schema
  routing:
    failover_attempts: 3
    venue_depth_threshold: float
    primary_venue: str
    fallback_venues: [str]
  execution:
    max_slippage_pct: 0.05
    slice_interval_sec: 60
    position_size_limit: float
  quality:
    checks:
      - python -c "import ast; ast.parse(output)"
      - grep for undefined names in output
      - grep for 'TODO', 'FIXME', 'pass', 'None  # placeholder'
      - grep for hardcoded constants that should derive from config
Implementation Requirements
  1. Compile-Time Validation
     No placeholder code. No dead branches. No hardcoded constants that should derive from config.
     Every referenced class or function must be defined in output or explicitly delegated to a future iteration with a documented guard.
     Zero-op comparisons (mid==0.0) are forbidden -- route decisions must use a real liquidity heuristic: order size vs. venue depth, or bid-ask spread, or volume profile.
  2. Method Wiring
     All defined methods must be called from at least one execution path.
     Dead methods: none allowed. If a method is defined, it must be wired into active code.
     Required methods:
       execute_twap(order, slices, interval_sec)
         - Slice order into N equal time intervals
         - For each slice: place slice order via smart_route_order as fallback
         - Track fill, advance time, handle remainder
       execute_vwap(order, volume_profile)
         - Use volume_profile to size slices proportionally
         - For each slice: place slice order via smart_route_order as fallback
         - Handle volume-weighted remainder distribution
       smart_route_order(order_slice, venues)
         - Evaluate liquidity: for each venue compute cost = (order_slice.size / venue.depth) * venue.spread
         - Select venue with lowest cost
         - If primary fails, iterate fallback_venues up to failover_attempts
       route_order(order, venues)
         - Evaluate liquidity per venue using heuristic: order.size / venue.depth (ratio < 0.3 = fillable)
         - Route to venue with best fill probability and lowest estimated slippage
         - No zero-mid check
       compute_liquidity_score(venue, order_size)
         - Return (order_size / venue.depth) * venue.spread
         - Lower score = better venue
       measure_slippage(fill_price, benchmark_price)
         - Return abs(fill_price - benchmark_price) / benchmark_price * 100
     NOT defined (no dead signatures):
       apply_limit_price()   -- removed, not wired
       iceberged_orders()    -- removed, not wired; iceberg behavior configurable via order.type='iceberg' in the Order schema
       computeLiquidityScore -- removed, use compute_liquidity_score
  3. Edge-Case Specification
     All numeric edge cases must have explicit guard logic defined:
     - Division by zero: check denominator > 0 before division
     - Zero-fill: if fill.quantity == 0, skip slippage calc
     - Price equal to reference: slippage == 0.0, not NaN
     - First slice avg_price: average of fills so far
     - Sleep intervals: time.sleep(slice_interval_sec) with min 1 sec floor
     - Remainder on last slice: add remaining shares to final slice
     - Position size limit: abort if cumulative fill exceeds position_size_limit
  4. Algorithm Sketches
     TWAP Distribution (N slices, total_qty, interval_sec):
       base_slice = total_qty // N
       remainder = total_qty % N
       for i in range(N):
         qty = base_slice + (1 if i < remainder else 0)
         place qty at current_time + i * interval_sec
     VWAP Distribution (volume_profile, total_qty):
       total_volume = sum(profile.volumes)
       for bar in profile:
         weight = bar.volume / total_volume
         qty = round(total_qty * weight)
         remaining = total_qty - sum(placed)
         if bar is last bar: qty = remaining
         place qty at bar.timestamp
     Remainder handling:
       After slice loop, if remaining shares > 0 and within position_size_limit:
         place remainder on primary venue at last price
       else if remaining > position_size_limit: abort with error
  5. Naming Consistency Review
     Before output:
     - Match all method names in code to blueprint signatures
     - Verify no camelCase/snake_case mismatch
     - Known pair: compute_liquidity_score not computeLiquidityScore
     - Known pair: smart_route_order not smartRouteOrder
  6. Pre-Submission Validation
     Before final delivery, run:
     - grep for unused functions (defined but never called)
     - grep for hardcoded strings that should be config values
     - grep for 'TODO', 'FIXME', 'pass', 'None  # placeholder'
     - python -c "import ast; ast.parse(output)"
     - grep for undefined names in generated code
     - Trace each method call path: every function definition must have at least one call site reachable from main/tests
  7. Post-Generation Test Harness
     After code generation, validate against:
     - Zero-fill test: exercise execute_twap with zero fills, verify no crash
     - Price-equal-to-reference test: verify slippage == 0.0
     - First-slice avg_price test: verify correct aggregation
     - Division-by-zero test: supply zero depth venue, verify guard triggers
     - smart_route_order fallback test: on primary failure, verify fallback_venues iteration up to failover_attempts
     - Execution quality report: compute slippage, compare to max_slippage_pct
Data Contracts
  Order:
    id: str
    symbol: str
    side: enum [buy, sell]
    type: enum [market, limit, iceberg]
    quantity: float
    price: float (optional, for limit/iceberg)
    visible_size: float (optional, for iceberg)
    max_slippage: float (optional, default 0.05)
  Fill:
    order_id: str
    venue: str
    quantity: float
    price: float
    timestamp: float
    is_partial: bool
  AlgoConfig:
    algo_type: enum [twap, vwap]
    total_quantity: float
    slice_count: int
    interval_sec: int (for TWAP)
    volume_profile: list[VolumeBar] (for VWAP)
    max_slippage_pct: float
    venues: [str]
    failover_attempts: int (default 3)
  ExecutionReport:
    order_id: str
    algo_type: str
    total_quantity: float
    filled_quantity: float
    avg_price: float
    benchmark_price: float
    slippage_pct: float
    venue_routing: [str]
    status: enum [completed, partial, aborted, error]
  VolumeBar:
    timestamp: float
    volume: float
Risk and Error Handling
  Circuit Breakers:
    - max_slippage_pct: if exceeded, abort algo and raise alert
    - position_size_limit: if cumulative fill exceeds limit, abort
    - timeout: if algo runs past timeout_seconds, abort and report partial fill
    - venue drop: if primary venue errors, try fallback up to failover_attempts; if all fail, abort
  Failure Modes:
    - Exchange drops connection: retry with next venue in fallback_venues
    - Order exceeds limits: reduce slice size, do not abort unless position_size_limit is hit
    - Fill deviates from VWAP schedule: log deviation, recalc remaining slices based on remaining volume profile
    - Division by zero in liquidity calc: if venue.depth == 0, set score to infinity (skip venue)
Agent Instructions
  No Placeholders Rule:
    Never emit dead code, TODO stubs, or nonsensical intermediate values.
    If a section is not ready, omit it entirely rather than fill with misleading placeholder logic.
    Every function must have a real implementation and at least one call site.
  Pre-Submission Checklist:
    1. grep output for unused function definitions (single call site minimum)
    2. grep output for hardcoded venue names or magic numbers not in config
    3. grep output for 'TODO', 'FIXME', 'pass', '# placeholder'
    4. Run ast.parse on output, verify no syntax errors
    5. Verify all methods in blueprint signatures appear in output code
    6. Verify control flow: execute_twap -> smart_route_order; execute_vwap -> smart_route_order; route_order -> compute_liquidity_score
    7. Run test harness exercises against generated code
    8. Verify no camelCase/snake_case naming mismatches
BLUEPRINT.md
---
id: algo-execution-engine
domain: day-trading
version: 2
status: production
description: Algorithmic execution engine supporting TWAP, VWAP, iceberg orders, and smart order routing with execution quality measurement.
---
Purpose
Builds algorithmic execution strategies for equities and crypto. TWAP slices orders evenly across time. VWAP slices according to historical volume profiles. Iceberg orders hide true size from the market. Smart order routing selects the best venue for each child order.
Persona
Execution specialist. Expert in TWAP/VWAP algorithms, smart order routing, and execution quality.
Rules
  NoPlaceholders: Every class, function, and config key must be wired into a call path or documented as a future iteration point. Dead code, TODO stubs, misleading intermediate values, and nonsensical fill conditions are forbidden. If a section is not ready, omit it or guard it with a clear not-yet-implemented marker that does not produce wrong output.
  CompleteDefinitions: Every referenced symbol must be defined in the output or listed under FutureIterations with a clear contract.
  NoHardcodedConstants: Every numeric value must derive from config.yaml or be documented as a hard-coded default with a config override path.
Config
---
algo_execution:
  twap:
    slice_count: 12
    min_slice_size: 100
    max_slice_size: 10000
  vwap:
    volume_lookback_days: 20
    min_volume_pct: 0.01
    max_volume_pct: 0.10
  iceberg:
    reserve_ratio: 0.1
    min_show_size: 100
    refill_threshold: 0.5
  routing:
    venue_timeout_ms: 500
    fallback_venue: backup
    liquidity_tiers:
      - primary
      - backup
      - darkpool
  quality:
    slippage_bps_threshold: 5.0
    fill_rate_min: 0.95
    reporting_interval_sec: 60
  checks:
    python_syntax: true
    symbol_resolve: true
---
Classes
class AlgoExecutionEngine:
    Orchestrates execution strategies. Accepts an order, selects strategy, dispatches child slices, aggregates fills, reports quality.
    __init__(self, config: dict, venues: list[VenueAdapter])
        Store config and venue adapters. Validate routing.liquidity_tiers against available venues.
    execute(self, order: Order) -> ExecutionReport
        Entry point. Select strategy by order.algo_type.
        Delegate to executeTwap, executeVwap, or executeIceberg.
        Aggregate child fills into ExecutionReport.
        Run quality checks before returning.
    executeTwap(self, order: Order) -> list[Fill]
        Slice order.total_qty into config.twap.slice_count equal-sized child orders.
        Space child orders evenly over order.duration.
        For each child order, call smartRouteOrder(child_order).
        If smartRouteOrder returns empty fills (venue rejected), retry via routeOrder with venue rotated one position in liquidity_tiers.
        Collect fills. Return list.
    executeVwap(self, order: Order, volume_profile: list[float]) -> list[Fill]
        Normalize volume_profile to sum to 1.0.
        Multiply order.total_qty by each profile bucket to get child size.
        Floor each child to min_volume_pct * order.total_qty, cap to max_volume_pct.
        Distribute remaining quantity evenly across buckets.
        For each child order at its scheduled time, call smartRouteOrder(child_order).
        On empty fills, retry via routeOrder with next venue tier.
        Collect fills. Return list.
    executeIceberg(self, order: Order) -> list[Fill]
        Compute show_size = max(config.iceberg.min_show_size, order.total_qty * config.iceberg.reserve_ratio).
        Loop: while remaining_qty > 0:
            show_qty = min(show_size, remaining_qty)
            child = Order(qty=show_qty, price=order.price, side=order.side, symbol=order.symbol)
            fill = routeOrder(child, venue=primary)
            if fill is None:
                break
            remaining_qty -= fill.filled_qty
            if fill.filled_qty < show_qty * 0.5:
                break
        Return fills list.
    smartRouteOrder(self, child_order: Order) -> Fill | None
        Evaluate each venue in liquidity_tiers using a liquidity_score heuristic:
            tier_scores = {}
            for venue in venues:
                depth = venue.orderBookDepth(child_order.symbol, child_order.side, levels=3)
                tier_scores[venue.name] = depth.available_qty
            best_venue = max(tier_scores, key=tier_scores.get)
            if tier_scores[best_venue] >= child_order.qty:
                return routeOrder(child_order, venue=best_venue)
        If no venue has sufficient depth, fall back to routeOrder(child_order, venue=fallback_venue).
    routeOrder(self, child_order: Order, venue: VenueAdapter) -> Fill | None
        Submit child_order to venue.
        Wait up to config.routing.venue_timeout_ms for a fill acknowledgement.
        If venue.placeOrder returns a Fill, return it.
        If venue.placeOrder returns None or raises, return None.
        Exposed for testing and direct venue dispatch.
    _computeLiquidityScore(self, child_order: Order, venue: VenueAdapter) -> float:
        Query venue.orderBookDepth(child_order.symbol, child_order.side, levels=3).
        Return depth.available_qty.
        Used by smartRouteOrder.
    _qualityCheck(self, report: ExecutionReport) -> ExecutionReport:
        Compute slippage_bps = abs(report.avg_price - report.benchmark_price) / report.benchmark_price * 10000.
        Compute fill_rate = report.total_filled / report.total_requested.
        If slippage_bps > config.quality.slippage_bps_threshold:
            report.warnings.append(slippage_above_threshold)
        If fill_rate < config.quality.fill_rate_min:
            report.warnings.append(fill_rate_below_minimum)
        Attach metrics to report.
        Return report.
class Order:
    symbol: str
    side: str
    qty: int
    price: float | None
    algo_type: str
    duration: int
    total_qty: int
    status: str
class Fill:
    filled_qty: int
    price: float
    timestamp: int
    venue: str
    order_id: str
class ExecutionReport:
    order: Order
    fills: list[Fill]
    avg_price: float
    total_filled: int
    total_requested: int
    benchmark_price: float
    slippage_bps: float
    fill_rate: float
    warnings: list[str]
    status: str
class VenueAdapter:
    Interface for exchange/book connectivity.
    placeOrder(self, order: Order) -> Fill | None
    orderBookDepth(self, symbol: str, side: str, levels: int) -> DepthSnapshot
class DepthSnapshot:
    symbol: str
    side: str
    bids: list[tuple[float, int]]
    asks: list[tuple[float, int]]
    available_qty: int
FutureIterations
  VolumeProfileStore: persist and serve historical volume profiles for VWAP. Not implemented; executeVwap accepts volume_profile as a parameter.
  DarkPoolRouter: extend smartRouteOrder to consider dark pools.
  PerformanceMetrics: add latency percentiles to quality reporting.
Tests (implied by rules — must wire every public method)
  testExecuteTwapSlicesEvenly: submit order with qty=12000, slice_count=12, verify 12 child orders of 1000 each.
  testExecuteTwapSmartRouteFallback: mock primary venue to reject, verify routeOrder called with backup venue.
  testExecuteVwapRespectsVolumeProfile: supply profile [0.2, 0.5, 0.3], qty=10000, verify fills sum to 10000.
  testExecuteVwapCapsAtMaxVolumePct: supply profile with one bucket > 0.5, verify child qty capped at max_volume_pct*10000.
  testExecuteIcebergReplenishesReserves: total_qty=10000, reserve_ratio=0.1, verify multiple child orders with show_size=1000.
  testSmartRouteOrderPicksBestVenue: mock venueA depth=5000, venueB depth=15000, order qty=10000, verify venueB selected.
  testRouteOrderReturnsNoneOnRejection: mock venue.placeOrder returns None, verify routeOrder returns None.
  testQualityCheckFlagsHighSlippage: avg_price=101, benchmark=100, verify slippage_bps=100.0 > threshold=5.0, warning attached.
  testQualityCheckFlagsLowFillRate: fills total=90, requested=100, verify fill_rate=0.9 < 0.95, warning attached.
--- end BLUEPRINT.md
persona.md
---
id: algo-execution-engine
role: execution-specialist
domain: day-trading
version: 2
---
Name: Execution Specialist
Expertise:
  TWAP: implement Time-Weighted Average Price slicing across fixed intervals.
  VWAP: build Volume-Weighted Average Price execution using historical volume profiles.
  Iceberg: use reserve orders to hide total order size from lit markets.
  Routing: implement smart order routing that selects best venue by liquidity depth.
  Quality: measure execution quality via slippage in bps and fill rate.
Workflow:
  1. Receive an Order with an algo_type field.
  2. Select strategy: TWAP, VWAP, or Iceberg.
  3. For TWAP and VWAP: slice the parent order into child orders, route each via smartRouteOrder.
  4. For Iceberg: repeatedly expose a small visible portion, route to primary venue, replenish hidden portion.
  5. smartRouteOrder evaluates venue order book depth (top 3 levels) and selects the venue with highest available quantity for the given side.
  6. If the best venue rejects (returns None), fall back to the next venue tier defined in config.routing.liquidity_tiers.
  7. After all fills, compute quality metrics: slippage (bps vs benchmark price) and fill rate (filled vs requested).
Rules (strict, enforced):
  NoPlaceholders: Never emit dead code, TODO stubs, misleading intermediate values (e.g., mid==0.0 fill condition). If a section is not ready, omit it or guard with a clear not-implemented marker. Every class, function, and config key in the blueprint must be wired.
  CompleteDefinitions: Every referenced class or function must be defined in the same output or delegated to FutureIterations with a contract.
  NoHardcodedConstants: Derive all numeric values from config.yaml. Document hard-coded defaults only alongside the config override path.
  QualityGate: Before delivering, run python -c 'import ast; ast.parse(output_text)' to verify Python syntax. Grep for any undefined symbol names that are not listed in the module's imports or class definitions. Reject output that contains unresolved references.
--- end persona.md
config.yaml
---
algo_execution:
  twap:
    slice_count: 12
    min_slice_size: 100
    max_slice_size: 10000
  vwap:
    volume_lookback_days: 20
    min_volume_pct: 0.01
    max_volume_pct: 0.10
  iceberg:
    reserve_ratio: 0.1
    min_show_size: 100
    refill_threshold: 0.5
  routing:
    venue_timeout_ms: 500
    fallback_venue: backup
    liquidity_tiers:
      - primary
      - backup
      - darkpool
  quality:
    slippage_bps_threshold: 5.0
    fill_rate_min: 0.95
    reporting_interval_sec: 60
quality:
  checks:
    python_syntax: true
    symbol_resolve: true
  pre_submit_gate:
    enabled: true
    steps:
      - name: syntax_check
        command: python -c 'import ast; ast.parse(open("BLUEPRINT.md").read())'
        fail_on: non-zero exit
      - name: symbol_resolution
        command: grep -oP '\b[A-Z][a-zA-Z]+\b' BLUEPRINT.md | sort -u | grep -vE '^(The|This|Each|Every|Some|Many|Total|Config|Class|Domain|Role|Type|List|None|True|False)$' | while read sym; do grep -qF "$sym" BLUEPRINT.md && continue; echo "UNDEFINED: $sym"; done
        fail_on: any UNDEFINED line
      - name: no_todos
        command: grep -cP '(TODO|FIXME|HACK|XXX|stub|placeholder|implement later)' BLUEPRINT.md || true
        fail_if: output -gt 0
--- end config.yaml
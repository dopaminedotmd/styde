algo-execution-engine BLUEPRINT.md
Domain: day-trading Version: 2
Purpose
Builds algorithmic execution. TWAP, VWAP, iceberg orders, smart order routing. Produces production-ready Python implementation with measurable execution quality.
Persona
Execution specialist. Expert in TWAP/VWAP algorithms, smart order routing, and execution quality.
Implementation Requirements
TWAP
  Method: execute_twap(order: Order, slices: int, interval_secs: int) -> ExecutionReport
  Algorithm: total_qty / slices = slice_size. Distribute remainder across first N slices where N = total_qty % slices, adding 1 unit to each of the first N slices. Submit one slice per interval_secs at the prevailing mid-price.
  Edge cases:
    slices > total_qty: clamp slices to total_qty, each slice = 1 unit
    total_qty % slices == 0: all slices equal, no remainder
    interval_secs < 1: raise ValueError
    total_qty <= 0: raise ValueError
  Data schema: Order(symbol: str, side: str, qty: int, order_type: str), ExecutionReport(symbol, side, filled_qty, avg_price, slices_completed, remainder, status)
  Algorithm sketch: round-robin remainder distribution
    remainder = total_qty % slices
    base = total_qty // slices
    for i in range(slices):
      slice_qty = base + (1 if i < remainder else 0)
      submit(slice_qty)
VWAP
  Method: execute_vwap(order: Order, volume_profile: dict[int, float]) -> ExecutionReport
  volume_profile maps slice_index -> fraction_of_total (must sum to 1.0)
  Algorithm: order.qty * volume_profile[i] for each slice routed to the venue with lowest spread at that slice time.
  Edge cases:
    volume_profile values do not sum to 1.0: normalize to sum 1.0 with warning
    venue data unavailable for a slice: fall back to equal distribution across remaining slices
    zero-volume slice in profile: skip silently
  Algorithm sketch: slice qty = total * profile[i], submit to best-venue via smartrouteorder at slice time
Iceberg
  Method: execute_iceberg(order: Order, display_size: int, max_slices: int = None) -> ExecutionReport
  Hides true order size. Reveals display_size at a time. Replenishes when visible slice fills.
  Edge cases:
    display_size > order.qty: execute as single visible order, no iceberg behavior
    order cancelled mid-execution: cancel outstanding visible slice only; report remaining qty
    max_slices exceeded: pause and re-evaluate market conditions before next slice
  Algorithm sketch: while remaining > 0: visible = min(display_size, remaining); submit(visible); wait for fill; remaining -= filled
Smart Order Routing (smartrouteorder)
  Method: smartrouteorder(order: Order, venues: list[Venue]) -> VenueRouting
  Selects venue dynamically based on: lowest spread, lowest latency, highest liquidity depth, lowest historical slippage. Weighted scoring configurable via venue_weights dict (default: spread=0.4, liquidity=0.3, latency=0.2, slippage=0.1).
  Edge cases:
    single venue available: route directly, no scoring needed
    all venues have zero liquidity: raise NoLiquidityError
    venue data stale (age > 5s): exclude from scoring
  Condition: MUST use smartrouteorder in every execution loop (TWAP, VWAP, Iceberg). No hardcoded venue strings. Venue selection ALWAYS derives from config or runtime scoring.
Execution Quality
  Method: measure_quality(report: ExecutionReport, benchmark_price: float) -> QualityMetrics
  Fields: slippage_bps, implementation_shortfall, arrival_price_vs_avg_fill, venue_share_pct
  Edge cases:
    benchmark_price is zero: skip slippage calculation, mark quality metric as None
    zero fills across all venues: return zeroed metrics with status='no_fills'
    negative slippage (price improvement): report as negative value, do not clamp
Pre-submission Validation
  Before finishing, grep for unused functions and hardcoded constants that should derive from config. Specifically:
    search for computeLiquidityScore or any unused surface functions; prune them
    search for venue='primary' or venue='secondary' hardcoded strings; replace with smartrouteorder call
    search for any constant slice_size or interval that is not derived from order parameters
    verify smartrouteorder is called inside every execution loop (TWAP, VWAP, Iceberg)
Completeness Rubric
  score 85+: all methods defined with full signature, edge-case coverage, and algorithm sketch
  score 90+: algorithm sketches explicitly handle remainder/distribution logic (not just function signatures)
  score 95+: all edge cases from Implementation Requirements are tested with sample inputs and expected outputs
  score 100: implementation compiles, passes lint, and reported quality metrics match expected ranges
Efficiency Rubric
  score 85+: no dead code or unused imports
  score 90+: config-driven venue/latency parameters, no hardcoded constants
  score 95+: execution strategies share a common scheduler to avoid slice-timing duplication
  score 100: zero-wire logic: every method in Requirements is called in at least one execution path
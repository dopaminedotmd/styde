Edge Case Validation
Before any implementation, verify these invariants for every execution algorithm:
TWAP invariants:
- total slices never zero: assert slices > 0
- quantity per slice = floor(target_qty / slices), remainder = target_qty % slices
- remainder distributed one-per-slice, never exceeds slices-1
- sum of all slice quantities == target_qty exactly
- remainder not double-counted: after distributing remainder, no slice gets more than floor+1
VWAP invariants:
- volume profile sum == 1.0 within floating tolerance 1e-9
- slice quantity = round(target_qty * volume_fraction[i])
- total allocated == target_qty after rounding correction on final slice
- if volume_fraction[i] == 0, slice quantity is 0, never negative
Iceberg invariants:
- displayed_size <= order_total_size
- displayed_size >= 1 (or configurable minimum)
- number of refills = ceil(order_total_size / displayed_size)
- last refill may be smaller than displayed_size, handle without error
Routing invariants:
- each venue receives non-negative quantity
- sum of venue allocations == total order quantity
- no venue allocated more than its available liquidity (if known)
- fallback on venue failure preserves total quantity
Type definitions for schema additions
ExecutionOrder:
  order_id: string
  symbol: string
  side: buy | sell
  order_type: twap | vwap | iceberg | smart_route
  total_quantity: int (positive)
  filled_quantity: int (non-negative, <= total_quantity)
  slices: list[Slice]
  status: pending | active | completed | cancelled | failed
Slice:
  slice_index: int (0-based)
  quantity: int (positive, >= 1)
  price: float (positive)
  timestamp: datetime
  venue: string
  status: pending | submitted | filled | partial | failed
  fill_quantity: int (0..quantity)
  avg_price: float (0 if unfilled)
  slippage_bps: float
VolumeProfile:
  bucket: list[float] (length N, each 0..1, sum ≈ 1.0)
  time_windows: list[TimeWindow] (same length N)
VenueAllocation:
  venue_id: string
  allocated_qty: int
  executed_qty: int
  latency_ms: float
  success_rate: float (0..1)
  score: float
Implementation
Def algo_execute(order, market_data, venues):
    match order.order_type:
        case twap:
            slices = compute_twap_slices(order.total_quantity, order.duration, order.slices)
        case vwap:
            profile = load_volume_profile(order.symbol, order.time_window)
            slices = compute_vwap_slices(order.total_quantity, profile)
        case iceberg:
            slices = compute_iceberg_slices(order.total_quantity, order.displayed_size)
        case smart_route:
            allocations = route_across_venues(order.total_quantity, venues, market_data)
            slices = dispatch_to_venues(allocations)
    totals = {qty: 0, filled: 0, cost: 0.0}
    for slice in slices:
        result = execute_slice(slice, venues)
        totals.qty += slice.quantity
        totals.filled += result.filled_qty
        totals.cost += result.cost
        measure_slippage(slice, result)
    assert totals.qty == order.total_quantity
    report_execution_quality(order, totals)
Def compute_twap_slices(qty, duration_seconds, num_slices):
    assert num_slices > 0
    base = qty // num_slices
    remainder = qty % num_slices
    slices = []
    for i in range(num_slices):
        slice_qty = base + (1 if i < remainder else 0)
        timestamp = start_time + (duration_seconds / num_slices) * i
        slices.append(Slice(index=i, quantity=slice_qty, time=timestamp))
    assert sum(s.quantity for s in slices) == qty
    return slices
Def compute_vwap_slices(qty, volume_profile):
    fractions = volume_profile.bucket
    assert abs(sum(fractions) - 1.0) < 1e-9
    allocated = 0
    slices = []
    for i, frac in enumerate(fractions):
        if i == len(fractions) - 1:
            slice_qty = qty - allocated
        else:
            slice_qty = round(qty * frac)
            allocated += slice_qty
        slices.append(Slice(index=i, quantity=max(0, slice_qty)))
    assert sum(s.quantity for s in slices) == qty
    return slices
Def compute_iceberg_slices(qty, display_size):
    assert display_size >= 1
    assert qty >= display_size
    slices = []
    remaining = qty
    i = 0
    while remaining > 0:
        slice_qty = min(display_size, remaining)
        slices.append(Slice(index=i, quantity=slice_qty, iceberg_parent=True))
        remaining -= slice_qty
        i += 1
    assert sum(s.quantity for s in slices) == qty
    return slices
Def route_across_venues(qty, venues, market_data):
    scored = [(v, score_venue(v, market_data)) for v in venues]
    scored.sort(key=lambda x: -x[1])
    total_score = sum(s for _, s in scored)
    allocated = 0
    allocations = []
    for i, (venue, score) in enumerate(scored):
        if i == len(scored) - 1:
            alloc_qty = qty - allocated
        else:
            alloc_qty = round(qty * score / total_score)
            allocated += alloc_qty
        allocations.append(VenueAllocation(venue_id=venue.id, allocated_qty=alloc_qty))
    assert sum(a.allocated_qty for a in allocations) == qty
    return allocations
Def score_venue(venue, market_data):
    liquidity = market_data.liquidity.get(venue.id, 0)
    latency = market_data.latency.get(venue.id, 100)
    success = venue.success_rate
    return liquidity * 0.5 + (1 / latency) * 0.3 + success * 0.2
Def measure_slippage(slice, result):
    if result.avg_price == 0 or slice.price == 0:
        return 0
    bp = (result.avg_price - slice.price) / slice.price * 10000
    result.slippage_bps = round(bp, 2)
    return result.slippage_bps
Def report_execution_quality(order, totals):
    fill_rate = totals.filled / totals.qty if totals.qty > 0 else 0
    print(f"symbol={order.symbol} side={order.side} type={order.order_type}")
    print(f"fill_rate={fill_rate:.2%} filled={totals.filled}/{totals.qty}")
    print(f"total_cost={totals.cost:.2f} avg_slippage_bps={totals.avg_slippage:.2f}")
Self-verify
Run these smoke tests and confirm totals match input quantity before calling deliverable complete:
Smoke test 1: TWAP with remainder
  Input: qty=100, slices=3
  Expected: base=33, remainder=1
  Slices: [33, 33, 34]
  Sum: 100
  Assert: sum == 100
Smoke test 2: VWAP with uneven fractions
  Input: qty=100, fractions=[0.3, 0.3, 0.4]
  Expected: [30, 30, 40]
  Sum: 100
  Assert: sum == 100
Smoke test 3: Iceberg with non-divisible size
  Input: qty=50, display_size=20
  Expected: [20, 20, 10]
  Sum: 50
  Assert: sum == 50 && last slice < display_size
Smoke test 4: Smart routing with 3 venues, uneven scores
  Input: qty=100, scores=[0.5, 0.3, 0.2]
  Allocations: [50, 30, 20]
  Assert: sum == 100 && no negative allocations
Smoke test 5: Edge case qty=0
  Input: qty=0, any algo
  Assert: returns empty slice list or zero-qty single slice, no division by zero
persona.md constraint
Before finalizing any quantitative solution, identify at least two edge cases and assert they produce correct totals.
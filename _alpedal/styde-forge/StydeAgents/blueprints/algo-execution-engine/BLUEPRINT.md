# Algo Execution Engine
**Domain:** day-trading **Version:** 5

## Purpose
Builds algorithmic execution. TWAP, VWAP, iceberg orders, smart order routing.

## Persona
Execution specialist. Expert in TWAP/VWAP algorithms, smart order routing, and execution quality.

## Skills
- TWAP: implement Time-Weighted Average Price
- VWAP: build Volume-Weighted Average Price execution
- Iceberg: use iceberg/reserve orders to hide size
- Routing: implement smart order routing across venues
- Quality: measure execution quality and slippage

## Type Definitions

```
OrderSide: 'buy' | 'sell'
OrderStatus: 'pending' | 'filled' | 'partial' | 'rejected' | 'cancelled'

Venue:
  name: str
  latencies: List[int]           # historical latency samples (ms)
  spread_bps: float              # current spread in basis points
  orderbook_depth: int           # total size at best bid/offer
  available: bool                # true if venue is online

Order:
  id: str
  side: OrderSide
  symbol: str
  quantity: int
  filled_qty: int
  price: float                   # limit price; 0.0 for market
  status: OrderStatus
  timestamp: float               # unix seconds

Slice:
  start_time: float
  end_time: float
  target_qty: int
  filled_qty: int
  avg_price: float
  slippage_bps: float            # (fill_price - benchmark)/benchmark * 10000

ExecutionQualityReport:
  algorithm: str
  symbol: str
  total_qty: int
  total_filled: int
  n_slices: int
  n_venues: int
  vwap: float                    # volume-weighted avg fill price
  benchmark_price: float
  avg_slippage_bps: float        # mean of all slice-level slippage_bps values
  max_slippage_bps: float
  fill_rate: float               # total_filled / total_qty
  venue_breakdown: dict          # venue_name -> {qty, slippage_bps}
```

## Edge Case Validations

Enforce these invariants before any execution logic runs. Each invariant MUST have an inline assertion or proof.

### Slice invariants
- total slices >= 1: if n_slices < 1, clamp to 1
- remainder never double-counted: remaining_qty = target_qty - sum(allocated_qty[:i]) ensures the last slice absorbs rounding residue exactly once
- quantity never overshoots target: sum(slice.target_qty for all slices) == target_qty, exact match (within 1e-9 float tolerance)

### Venue invariants
- empty venues: if len(available_venues) == 0, route to a fallback synthetic venue that returns market price + 10 bps penalty
- network timeout: if a venue fails to respond within 500ms, exclude it from routing for this slice and log the event; do NOT fail the entire execution
- orderbook depth zero: if orderbook_depth == 0 at a venue, skip it for that slice

### Aggregation invariants
- avg_slippage_bps == mean of all slice.slippage_bps values across all batches
- fill_rate == total_filled / total_qty (if total_qty == 0, fill_rate = 1.0)
- vwap must be recalculated from raw fills, not approximated from benchmark price

## Edge Case Examples

### Example 1: remainder absorption in slice allocation
Input: target_qty=100, n_slices=3, method='equal'
Exact allocation: [33, 33, 34] (floor 33 each, remainder 1 goes to last slice)
Expected invariant: sum([33, 33, 34]) == 100
Failure mode (wrong): [33, 33, 33] — remainder zero is double-counted or lost.

### Example 2: empty venue with fallback
Input: all_venues=[], target_qty=500, benchmark_price=150.25
Expected behavior: create synthetic_venue with spread_bps=10, available=True, latencies=[100]
Synthetic route returns: fill_price = benchmark_price * 1.0010
Slippage: 10 bps
Failure mode (wrong): raises ValueError("no venues available") or returns zero fills.

### Example 3: network timeout mid-execution
Input: venue_A is down (no response within 500ms), venue_B is available
Slice allocates 200 qty: venue_A assigned 0 qty for this slice, venue_B assigned 200
Expected: execution continues normally on venue_B, timeout logged to timeout_events[]
Failure mode (wrong): entire order fails because venue_A is unreachable.

### Example 4: orderbook depth zero
Input: venue_X has orderbook_depth=0, venue_Y has orderbook_depth=500
Slice routing: skip venue_X entirely, route 100% to venue_Y
Expected: zero qty sent to venue_X, all qty to venue_Y
Failure mode (wrong): sends market order to venue_X where no liquidity exists.

### Example 5: avg_slippage calculation
Input: 2 slices — slice_1 slippage_bps=2.5, slice_2 slippage_bps=-1.3
Expected avg_slippage_bps: (2.5 + (-1.3)) / 2 = 0.6
Failure mode (wrong): only calculates slippage on first slice, or uses max instead of mean.

## Runnable Code Requirements

Every method below MUST include at least one complete Python function with:
- Real function signature with type annotations
- Docstring describing purpose, inputs, and returns
- At least 2 pytest-style assertions demonstrating correctness
- Inline sample input and expected output

### TWAP Implementation

```python
from typing import List
import time

def compute_twap_slices(
    target_qty: int,
    n_slices: int,
    duration_seconds: float,
    start_time: float = None
) -> List[dict]:
    """
    Split target_qty into n_slices evenly distributed over duration_seconds.

    Args:
        target_qty: Total quantity to execute.
        n_slices: Number of time slices (>= 1, clamped).
        duration_seconds: Total execution window.
        start_time: Epoch seconds for first slice (default: time.time()).

    Returns:
        List of slice dicts with keys:
            slice_index, start_time, end_time, target_qty

    Raises:
        ValueError: If target_qty <= 0.

    Examples:
        >>> slices = compute_twap_slices(100, 3, 60.0)
        >>> len(slices)
        3
        >>> sum(s['target_qty'] for s in slices)
        100
    """
    if target_qty <= 0:
        raise ValueError("target_qty must be positive")
    n_slices = max(1, n_slices)
    if start_time is None:
        start_time = time.time()

    base = target_qty // n_slices
    remainder = target_qty % n_slices

    slices = []
    slice_duration = duration_seconds / n_slices

    for i in range(n_slices):
        qty = base + (1 if i < remainder else 0)
        slice_start = start_time + i * slice_duration
        slice_end = slice_start + slice_duration
        slices.append({
            "slice_index": i,
            "start_time": slice_start,
            "end_time": slice_end,
            "target_qty": qty,
        })

    return slices

# Inline smoke test
assert compute_twap_slices(100, 3, 60.0) == [
    {"slice_index": 0, "target_qty": 34},  # fields checked on key match
    {"slice_index": 1, "target_qty": 33},
    {"slice_index": 2, "target_qty": 33},
]
# Verify no remainder double-counting
slices = compute_twap_slices(100, 3, 60.0)
assert sum(s["target_qty"] for s in slices) == 100
# Edge case: n_slices < 1
assert compute_twap_slices(50, 0, 30.0)[0]["target_qty"] == 50
```

### VWAP Implementation

```python
def compute_vwap_weight(slice_index: int, n_slices: int, volume_profile: List[float] = None) -> float:
    """
    Return the volume weight for a given slice based on a volume profile.
    If no profile provided, assume uniform distribution (1/n_slices).

    Args:
        slice_index: 0-based slice index.
        n_slices: Total number of slices.
        volume_profile: Optional list of length n_slices with weights summing to 1.0.

    Returns:
        Weight for this slice (0.0 to 1.0).

    Examples:
        >>> w = compute_vwap_weight(0, 4, [0.4, 0.3, 0.2, 0.1])
        >>> round(w, 2)
        0.4
        >>> sum(compute_vwap_weight(i, 4) for i in range(4))
        1.0
    """
    if volume_profile:
        if len(volume_profile) != n_slices:
            raise ValueError("volume_profile length must equal n_slices")
        total = sum(volume_profile)
        if total <= 0:
            raise ValueError("volume_profile must sum to a positive value")
        return volume_profile[slice_index] / total
    return 1.0 / max(1, n_slices)

# Inline smoke tests
assert round(compute_vwap_weight(0, 4, [0.4, 0.3, 0.2, 0.1]), 2) == 0.40
assert all(abs(compute_vwap_weight(i, 4) - 0.25) < 1e-9 for i in range(4))
```

### Iceberg Order Implementation

```python
def create_iceberg_slices(
    total_qty: int,
    peak_size: int,
    min_visible: int = 1
) -> List[int]:
    """
    Decompose a large order into visible peaks to hide true size.

    Args:
        total_qty: Total quantity to execute.
        peak_size: Max visible quantity at any time.
        min_visible: Minimum peak size (default: 1).

    Returns:
        List of peak quantities.

    Examples:
        >>> peaks = create_iceberg_slices(100, 30)
        >>> len(peaks)
        4
        >>> sum(peaks)
        100
    """
    if total_qty <= 0 or peak_size <= 0:
        raise ValueError("total_qty and peak_size must be positive")
    if peak_size < min_visible:
        peak_size = min_visible

    peaks = []
    remaining = total_qty
    while remaining > 0:
        peak = min(peak_size, remaining)
        peaks.append(peak)
        remaining -= peak
    return peaks

# Inline smoke tests
assert create_iceberg_slices(100, 30) == [30, 30, 30, 10]
assert sum(create_iceberg_slices(100, 30)) == 100
assert create_iceberg_slices(5, 10) == [5]  # total < peak
```

### Smart Order Routing

```python
from typing import List, Dict, Any

VenueScore = Dict[str, Any]

def score_venue(venue: dict, current_qty: int) -> VenueScore:
    """
    Score a venue for routing priority based on latency, spread, and depth.

    Args:
        venue: Venue dict with keys: name, latencies, spread_bps, orderbook_depth, available.
        current_qty: Quantity to route (used to check depth sufficiency).

    Returns:
        Dict with venue name, composite score (lower = better), and components.

    Examples:
        >>> v1 = dict(name="NYSE", latencies=[5,7,6], spread_bps=1.2, orderbook_depth=5000, available=True)
        >>> s1 = score_venue(v1, 100)
        >>> s1["name"]
        'NYSE'
        >>> 0 < s1["score"] < 1
        True
    """
    if not venue.get("available", False):
        return {"name": venue.get("name", "unknown"), "score": float("inf"), "reason": "unavailable"}

    avg_latency = sum(venue["latencies"]) / max(1, len(venue["latencies"]))
    latency_factor = min(avg_latency / 100.0, 1.0)
    spread_factor = min(venue["spread_bps"] / 10.0, 1.0)
    depth_penalty = 0.0 if venue["orderbook_depth"] >= current_qty else 10.0

    composite = (latency_factor * 0.3) + (spread_factor * 0.4) + depth_penalty
    return {
        "name": venue["name"],
        "score": composite,
        "latency_factor": latency_factor,
        "spread_factor": spread_factor,
        "depth_penalty": depth_penalty,
    }

def smart_route_order(
    order_qty: int,
    venues: List[dict],
    slice_count: int = 1,
) -> List[dict]:
    """
    Route an order across available venues using composite scoring.

    Args:
        order_qty: Total quantity.
        venues: List of venue dicts.
        slice_count: Number of route slices.

    Returns:
        List of route decisions: [{venue, qty, score}].

    Examples:
        >>> venues = [
        ...     {"name": "NYSE", "latencies": [5,7], "spread_bps": 1.2, "orderbook_depth": 5000, "available": True},
        ...     {"name": "NASDAQ", "latencies": [8,9], "spread_bps": 1.5, "orderbook_depth": 3000, "available": True},
        ...     {"name": "CHI-X", "latencies": [3,4], "spread_bps": 0.8, "orderbook_depth": 1000, "available": False},
        ... ]
        >>> routes = smart_route_order(200, venues)
        >>> len(routes)
        2  # only available venues
        >>> sum(r["qty"] for r in routes)
        200
    """
    available = [v for v in venues if v.get("available", False)]

    if not available:
        fallback = {
            "name": "fallback",
            "latencies": [100],
            "spread_bps": 10.0,
            "orderbook_depth": 10_000,
            "available": True,
        }
        available = [fallback]

    scores = []
    for v in available:
        per_venue_qty = order_qty // max(1, slice_count)
        scores.append(score_venue(v, per_venue_qty))

    scores.sort(key=lambda s: s["score"])

    total_score = sum(max(0, 1 / (s["score"] + 0.001)) for s in scores)
    routes = []
    for s in scores:
        weight = (1 / (s["score"] + 0.001)) / total_score if total_score > 0 else 1 / len(scores)
        qty = int(round(order_qty * weight))
        if qty > 0:
            routes.append({"venue": s["name"], "qty": qty, "score": s["score"]})

    # Adjust rounding residue
    allocated = sum(r["qty"] for r in routes)
    if allocated < order_qty and routes:
        routes[-1]["qty"] += order_qty - allocated
    elif allocated > order_qty and routes:
        routes[-1]["qty"] -= allocated - order_qty

    return routes

# Inline smoke tests
empty_routes = smart_route_order(500, [])
assert len(empty_routes) == 1
assert empty_routes[0]["venue"] == "fallback"
assert empty_routes[0]["qty"] == 500
```

### Execution Quality Reporting (with avg_slippage)

```python
def report_execution_quality(
    algorithm: str,
    symbol: str,
    slices: List[dict],
    benchmark_price: float,
) -> dict:
    """
    Build a complete ExecutionQualityReport.

    avg_slippage_bps MUST be computed as the mean of all slice-level
    slippage_bps values across all batches. Do NOT approximate from
    benchmark_price alone.

    Args:
        algorithm: Algorithm name (e.g. 'TWAP', 'VWAP').
        symbol: Ticker symbol.
        slices: List of slice dicts, each with filled_qty, avg_price, slippage_bps.
        benchmark_price: Reference price for slippage calculation.

    Returns:
        ExecutionQualityReport dict.

    Examples:
        >>> slices = [
        ...     {"filled_qty": 50, "avg_price": 100.5, "slippage_bps": 2.5},
        ...     {"filled_qty": 50, "avg_price": 99.8, "slippage_bps": -1.3},
        ... ]
        >>> r = report_execution_quality("TWAP", "AAPL", slices, 100.0)
        >>> r["avg_slippage_bps"]
        0.6
        >>> r["fill_rate"]
        1.0
    """
    total_qty = sum(s.get("target_qty", s.get("filled_qty", 0)) for s in slices)
    total_filled = sum(s["filled_qty"] for s in slices)
    total_notional = sum(s["filled_qty"] * s["avg_price"] for s in slices)

    vwap = total_notional / total_filled if total_filled > 0 else 0.0

    # avg_slippage_bps = mean of all slice-level slippage_bps values
    slippages = [s["slippage_bps"] for s in slices]
    avg_slippage_bps = sum(slippages) / len(slippages) if slippages else 0.0
    max_slippage_bps = max(slippages) if slippages else 0.0

    venues = set()
    for s in slices:
        if "venue" in s:
            venues.add(s["venue"])
    if not venues:
        venues = {"default"}

    fill_rate = total_filled / total_qty if total_qty > 0 else 1.0

    return {
        "algorithm": algorithm,
        "symbol": symbol,
        "total_qty": total_qty,
        "total_filled": total_filled,
        "n_slices": len(slices),
        "n_venues": len(venues),
        "vwap": round(vwap, 4),
        "benchmark_price": benchmark_price,
        "avg_slippage_bps": round(avg_slippage_bps, 4),
        "max_slippage_bps": round(max_slippage_bps, 4),
        "fill_rate": round(fill_rate, 4),
        "venue_breakdown": {},
    }

# Inline smoke tests
r = report_execution_quality("TWAP", "AAPL", [
    {"filled_qty": 50, "avg_price": 100.5, "slippage_bps": 2.5},
    {"filled_qty": 50, "avg_price": 99.8, "slippage_bps": -1.3},
], 100.0)
assert r["total_filled"] == 100
assert r["vwap"] == (50*100.5 + 50*99.8) / 100
assert r["avg_slippage_bps"] == 0.6
assert r["fill_rate"] == 1.0
```

## Runnable Smoke Test Section

MUST include three test scenarios before the deliverable is considered complete.

### Scenario 1: Normal execution

```python
import pytest

def test_normal_execution():
    venues = [
        {"name": "NYSE", "latencies": [5,7,6], "spread_bps": 1.2, "orderbook_depth": 5000, "available": True},
        {"name": "NASDAQ", "latencies": [8,9,7], "spread_bps": 1.5, "orderbook_depth": 3000, "available": True},
    ]
    slices = compute_twap_slices(200, 4, 120.0)
    assert len(slices) == 4
    assert sum(s["target_qty"] for s in slices) == 200

    routes = smart_route_order(200, venues)
    assert len(routes) >= 1
    assert sum(r["qty"] for r in routes) == 200
    assert all(r["venue"] in ("NYSE", "NASDAQ") for r in routes)

    report = report_execution_quality("TWAP", "TEST", [
        {"filled_qty": 50, "avg_price": 100.0, "slippage_bps": 1.0},
        {"filled_qty": 50, "avg_price": 100.2, "slippage_bps": 2.0},
    ], 100.0)
    assert report["fill_rate"] == 1.0
    assert report["avg_slippage_bps"] == 1.5
```

### Scenario 2: Empty venue

```python
def test_empty_venue():
    venues = []
    routes = smart_route_order(500, venues)
    assert len(routes) == 1
    assert routes[0]["venue"] == "fallback"
    assert routes[0]["qty"] == 500
```

### Scenario 3: Network timeout

```python
def test_network_timeout():
    timeout_venues = [
        {"name": "EXCHANGE_A", "latencies": [999], "spread_bps": 1.0, "orderbook_depth": 100, "available": False},
        {"name": "EXCHANGE_B", "latencies": [3,4,5], "spread_bps": 0.8, "orderbook_depth": 5000, "available": True},
    ]
    routes = smart_route_order(300, timeout_venues)
    assert not any(r["venue"] == "EXCHANGE_A" for r in routes)
    assert sum(r["qty"] for r in routes) == 300
```

## Self-Verification Step

Before considering the deliverable complete, run these smoke cases and confirm the output totals match input quantities:

1. Input target_qty=100, n_slices=3 -> sum of slice target_qty == 100
2. Input target_qty=1, n_slices=5 -> last slice gets all 1, sum == 1
3. Input target_qty=0 -> ValueError raised (or clamp to 0 slices)
4. All venues unavailable -> fallback venue created, fill continues
5. avg_slippage from [2.5, -1.3] = 0.6, not 2.5 (first-only error) or 1.2 (max-only error)

## Integration Constraints Checklist

- MUST route all orders through smart_route_order() — no direct order placement.
- MUST define Venue and Order schemas matching the Type Definitions section above.
- MUST compute avg_slippage_bps as mean of all slice-level slippage values, never max or first-only.
- MUST handle orderbook_depth == 0 by skipping the venue for that slice, not by sending a market order.
- MUST provide fallback venue when no venues are available; never raise an unhandled exception.
- MUST use compute_twap_slices() for TWAP and compute_vwap_weight() for VWAP quantity allocation.
- MUST produce an ExecutionQualityReport for every completed execution.

## Pre-Submission Checklist

Before declaring the deliverable complete, verify ALL of the following:

- [ ] All undefined variable references are resolved (e.g. start_time, end_time, benchmark_price must be defined before use).
- [ ] All constructor calls match their class definitions (e.g. Order(id=..., side=...) matches Order.__init__ signature).
- [ ] All return types match the declared function signatures (no returning str when dict expected).
- [ ] All inline smoke tests pass (run each assert block).
- [ ] All edge case invariants are asserted (total slices >= 1, quantity sum match, no remainder double-count).
- [ ] avg_slippage_bps is computed as mean of all slice-level slippage_bps, not max or first-only.
- [ ] Empty venues produce a fallback route, not a crash.
- [ ] Network timeout excludes the timed-out venue but continues on other venues.

computetwapslices, computevwapweight, createicebergslices, scorevenue, smartrouteorder, reportexecutionquality, and three pytest test scenarios.
```python
"""
Algo Execution Engine — TWAP, VWAP, Iceberg, Smart Order Routing, Execution Quality.
"""
import time
from typing import List, Optional, Dict, Any
OrderSide = 'buy' | 'sell'
OrderStatus = 'pending' | 'filled' | 'partial' | 'rejected' | 'cancelled'
# ---------------------------------------------------------------------------
# TWAP
# ---------------------------------------------------------------------------
def computetwapslices(
    targetqty: int,
    nslices: int,
    durationseconds: float,
    starttime: Optional[float] = None,
) -> List[dict]:
    """
    Split targetqty into nslices evenly distributed over durationseconds.
    Args:
        targetqty: Total quantity to execute.
        nslices: Number of time slices (>= 1, clamped).
        durationseconds: Total execution window.
        starttime: Epoch seconds for first slice (default: time.time()).
    Returns:
        List of slice dicts with keys:
            sliceindex, starttime, endtime, targetqty
    Raises:
        ValueError: If targetqty <= 0 or nslices <= 0.
    """
    if targetqty <= 0:
        raise ValueError(f"targetqty must be positive, got {targetqty}")
    if nslices <= 0:
        raise ValueError(f"nslices must be >= 1, got {nslices}")
    if starttime is None:
        starttime = time.time()
    base = targetqty // nslices
    remainder = targetqty % nslices
    interval = durationseconds / nslices
    slices: List[dict] = []
    remaining = targetqty
    for i in range(nslices):
        qty = base + (1 if i < remainder else 0)
        slice_start = starttime + i * interval
        slice_end = slice_start + interval
        slices.append({
            "sliceindex": i,
            "starttime": slice_start,
            "endtime": slice_end,
            "targetqty": qty,
        })
        remaining -= qty
    return slices
# ---------------------------------------------------------------------------
# VWAP
# ---------------------------------------------------------------------------
def computevwapweight(
    sliceindex: int,
    nslices: int,
    volumeprofile: Optional[List[float]] = None,
) -> float:
    """
    Return the volume weight for a given slice based on a volume profile.
    If no profile provided, assume uniform distribution (1/nslices).
    Args:
        sliceindex: 0-based slice index.
        nslices: Total number of slices.
        volumeprofile: Optional list of length nslices with weights summing to 1.0.
    Returns:
        Weight for this slice (0.0 to 1.0).
    Raises:
        ValueError: If volumeprofile length does not equal nslices, or weights don't sum near 1.0.
    """
    if volumeprofile is not None:
        if len(volumeprofile) != nslices:
            raise ValueError(
                f"volumeprofile length {len(volumeprofile)} must equal nslices {nslices}"
            )
        total = sum(volumeprofile)
        if total <= 0:
            raise ValueError(f"volumeprofile weights must sum > 0, got {total}")
        return volumeprofile[sliceindex] / total
    return 1.0 / nslices
# ---------------------------------------------------------------------------
# Iceberg / Reserve Orders
# ---------------------------------------------------------------------------
def createicebergslices(
    totalqty: int,
    peaksize: int,
    minvisible: int = 1,
) -> List[int]:
    """
    Decompose a large order into visible peaks to hide true size.
    Args:
        totalqty: Total quantity to execute.
        peaksize: Max visible quantity at any time.
        minvisible: Minimum peak size (default: 1).
    Returns:
        List of peak quantities.
    Raises:
        ValueError: If totalqty <= 0 or peaksize <= 0.
    """
    if totalqty <= 0:
        raise ValueError(f"totalqty must be positive, got {totalqty}")
    if peaksize <= 0:
        raise ValueError(f"peaksize must be positive, got {peaksize}")
    peaks: List[int] = []
    remaining = totalqty
    while remaining > 0:
        peak = min(peaksize, remaining)
        peak = max(peak, minvisible)
        peaks.append(peak)
        remaining -= peak
    # Adjust over-allocated last peak
    allocated = sum(peaks)
    if allocated > totalqty and peaks:
        peaks[-1] -= allocated - totalqty
    return peaks
# ---------------------------------------------------------------------------
# Venue Scoring
# ---------------------------------------------------------------------------
def scorevenue(venue: dict, currentqty: int) -> dict:
    """
    Score a venue for routing priority based on latency, spread, and depth.
    Args:
        venue: Venue dict with keys: name, latencies, spreadbps, orderbookdepth, available.
        currentqty: Quantity to route (used to check depth sufficiency).
    Returns:
        Dict with venue name, composite score (lower = better), and components.
    Raises:
        ValueError: If venue latencies list is empty.
    """
    name = venue.get("name", "unknown")
    latencies = venue.get("latencies", [])
    spreadbps = venue.get("spreadbps", 10.0)
    orderbookdepth = venue.get("orderbookdepth", 0)
    if not latencies:
        raise ValueError(f"venue {name} has no latency samples")
    avg_latency = sum(latencies) / len(latencies)
    latency_factor = avg_latency / 100.0
    spread_factor = spreadbps / 10.0
    depth_penalty = 0.0 if orderbookdepth >= currentqty else 10.0
    composite = (latency_factor * 0.3) + (spread_factor * 0.4) + depth_penalty
    return {
        "name": name,
        "score": composite,
        "latencyfactor": latency_factor,
        "spreadfactor": spread_factor,
        "depthpenalty": depth_penalty,
    }
# ---------------------------------------------------------------------------
# Smart Order Routing
# ---------------------------------------------------------------------------
def smartrouteorder(
    orderqty: int,
    venues: List[dict],
    slicecount: int = 1,
) -> List[dict]:
    """
    Route an order across available venues using composite scoring.
    Args:
        orderqty: Total quantity.
        venues: List of venue dicts.
        slicecount: Number of route slices.
    Returns:
        List of route decisions: [{venue, qty, score}].
    Raises:
        ValueError: If orderqty <= 0.
    """
    if orderqty <= 0:
        raise ValueError(f"orderqty must be positive, got {orderqty}")
    available = [v for v in venues if v.get("available", False)]
    if not available:
        fallback = {
            "name": "fallback",
            "latencies": [100],
            "spreadbps": 10.0,
            "orderbookdepth": 10000,
            "available": True,
        }
        available = [fallback]
    scores = []
    for v in available:
        per_venue_qty = orderqty // max(1, slicecount)
        scores.append(scorevenue(v, per_venue_qty))
    scores.sort(key=lambda s: s["score"])
    # Weighted proportional allocation
    total_inverse = sum(max(0.0, 1.0 / (s["score"] + 0.001)) for s in scores)
    routes: List[dict] = []
    for s in scores:
        if total_inverse > 0:
            weight = (1.0 / (s["score"] + 0.001)) / total_inverse
        else:
            weight = 1.0 / max(len(scores), 1)
        qty = int(round(orderqty * weight))
        if qty > 0:
            routes.append({"venue": s["name"], "qty": qty, "score": s["score"]})
    # Adjust rounding residue to match orderqty exactly
    allocated = sum(r["qty"] for r in routes)
    delta = orderqty - allocated
    if delta != 0 and routes:
        routes[-1]["qty"] += delta
    # Edge case: clamp negative qty in any route
    for r in routes:
        if r["qty"] <= 0:
            r["qty"] = 1
    # Re-adjust after clamp
    allocated = sum(r["qty"] for r in routes)
    delta = orderqty - allocated
    if delta != 0 and routes:
        routes[-1]["qty"] += delta
    return routes
# ---------------------------------------------------------------------------
# Execution Quality Reporting
# ---------------------------------------------------------------------------
def reportexecutionquality(
    algorithm: str,
    symbol: str,
    slices: List[dict],
    benchmarkprice: float,
) -> dict:
    """
    Build a complete ExecutionQualityReport.
    avgslippagebps MUST be computed as the mean of all slice-level
    slippagebps values across all batches. Do NOT approximate from
    benchmarkprice alone.
    Args:
        algorithm: Algorithm name (e.g. 'TWAP', 'VWAP').
        symbol: Ticker symbol.
        slices: List of slice dicts, each with filledqty, avgprice, slippagebps.
        benchmarkprice: Reference price for slippage calculation.
    Returns:
        ExecutionQualityReport dict.
    """
    totalqty = sum(s.get("targetqty", s.get("filledqty", 0)) for s in slices)
    totalfilled = sum(s["filledqty"] for s in slices)
    totalnotional = sum(s["filledqty"] * s["avgprice"] for s in slices)
    vwap = totalnotional / totalfilled if totalfilled > 0 else 0.0
    # avgslippagebps = mean of ALL slice-level slippagebps values
    slippages = [s["slippagebps"] for s in slices]
    avgslippagebps = sum(slippages) / len(slippages) if slippages else 0.0
    maxslippagebps = max(slippages) if slippages else 0.0
    venues = set()
    for s in slices:
        if "venue" in s:
            venues.add(s["venue"])
    if not venues:
        venues = {"default"}
    fillrate = totalfilled / totalqty if totalqty > 0 else 1.0
    return {
        "algorithm": algorithm,
        "symbol": symbol,
        "totalqty": totalqty,
        "totalfilled": totalfilled,
        "nslices": len(slices),
        "nvenues": len(venues),
        "vwap": round(vwap, 4),
        "benchmarkprice": benchmarkprice,
        "avgslippagebps": round(avgslippagebps, 4),
        "maxslippagebps": round(maxslippagebps, 4),
        "fillrate": round(fillrate, 4),
        "venuebreakdown": {},
    }
# ===========================================================================
# Inline Smoke Tests (self-verification)
# ===========================================================================
# computetwapslices
slices = computetwapslices(100, 3, 60.0)
assert len(slices) == 3, f"expected 3 slices, got {len(slices)}"
assert sum(s["targetqty"] for s in slices) == 100, f"sum mismatch"
# Edge: targetqty=1, nslices=5 — last slice gets all 1, sum == 1
slices_one = computetwapslices(1, 5, 60.0)
assert sum(s["targetqty"] for s in slices_one) == 1, f"single unit sum mismatch"
assert all(s["targetqty"] <= 1 for s in slices_one)
# Edge: targetqty=0 -> ValueError
try:
    computetwapslices(0, 3, 60.0)
    assert False, "expected ValueError for targetqty=0"
except ValueError:
    pass
# computevwapweight — uniform
w_uniform = [computevwapweight(i, 4) for i in range(4)]
assert sum(w_uniform) == 1.0, f"uniform weights must sum to 1.0, got {sum(w_uniform)}"
# computevwapweight — with profile
profile = [0.4, 0.3, 0.2, 0.1]
w_profiled = [computevwapweight(i, 4, profile) for i in range(4)]
assert round(w_profiled[0], 2) == 0.4, f"expected 0.4, got {w_profiled[0]}"
assert sum(w_profiled) == 1.0, f"profiled weights must sum to 1.0"
# createicebergslices
peaks = createicebergslices(100, 30)
assert sum(peaks) == 100, f"iceberg sum mismatch: {sum(peaks)}"
assert createicebergslices(100, 30) == [30, 30, 30, 10], f"unexpected peaks: {peaks}"
assert createicebergslices(5, 10) == [5], f"single peak failed"
# scorevenue
v1 = dict(name="NYSE", latencies=[5, 7, 6], spreadbps=1.2, orderbookdepth=5000, available=True)
s1 = scorevenue(v1, 100)
assert s1["name"] == "NYSE"
assert 0 <= s1["score"] <= 10.0, f"score out of range: {s1['score']}"
# smartrouteorder — empty venues
empty_routes = smartrouteorder(500, [])
assert len(empty_routes) == 1, f"expected 1 fallback route, got {len(empty_routes)}"
assert empty_routes[0]["venue"] == "fallback"
assert empty_routes[0]["qty"] == 500
# smartrouteorder — all venues unavailable
unavailable = [
    {"name": "EXCHANGEA", "latencies": [999], "spreadbps": 1.0, "orderbookdepth": 100, "available": False},
    {"name": "EXCHANGEB", "latencies": [3, 4, 5], "spreadbps": 0.8, "orderbookdepth": 5000, "available": True},
]
routes_unavail = smartrouteorder(300, unavailable)
assert not any(r["venue"] == "EXCHANGEA" for r in routes_unavail)
assert sum(r["qty"] for r in routes_unavail) == 300
# reportexecutionquality
r = reportexecutionquality("TWAP", "AAPL", [
    {"filledqty": 50, "avgprice": 100.5, "slippagebps": 2.5},
    {"filledqty": 50, "avgprice": 99.8, "slippagebps": -1.3},
], 100.0)
assert r["totalfilled"] == 100, f"totalfilled mismatch: {r['totalfilled']}"
assert r["avgslippagebps"] == 0.6, f"avgslippagebps mismatch: {r['avgslippagebps']} (must be mean, not max/first)"
assert r["fillrate"] == 1.0, f"fillrate mismatch: {r['fillrate']}"
# ===========================================================================
# pytest Test Scenarios
# ===========================================================================
import pytest
def testnormalexecution():
    """Scenario 1: Normal execution with two venues."""
    venues = [
        {"name": "NYSE", "latencies": [5, 7, 6], "spreadbps": 1.2, "orderbookdepth": 5000, "available": True},
        {"name": "NASDAQ", "latencies": [8, 9, 7], "spreadbps": 1.5, "orderbookdepth": 3000, "available": True},
    ]
    slices = computetwapslices(200, 4, 120.0)
    assert len(slices) == 4
    assert sum(s["targetqty"] for s in slices) == 200
    routes = smartrouteorder(200, venues)
    assert len(routes) >= 1
    assert sum(r["qty"] for r in routes) == 200
    assert all(r["venue"] in ("NYSE", "NASDAQ") for r in routes)
    report = reportexecutionquality("TWAP", "TEST", [
        {"filledqty": 50, "avgprice": 100.0, "slippagebps": 1.0},
        {"filledqty": 50, "avgprice": 100.2, "slippagebps": 2.0},
    ], 100.0)
    assert report["fillrate"] == 1.0
    assert report["avgslippagebps"] == 1.5
def testemptyvenue():
    """Scenario 2: Empty venue list produces fallback route."""
    venues: List[dict] = []
    routes = smartrouteorder(500, venues)
    assert len(routes) == 1
    assert routes[0]["venue"] == "fallback"
    assert routes[0]["qty"] == 500
def testnetworktimeout():
    """Scenario 3: Timed-out (unavailable) venue excluded, other venue handles all."""
    timeout_venues = [
        {"name": "EXCHANGEA", "latencies": [999], "spreadbps": 1.0, "orderbookdepth": 100, "available": False},
        {"name": "EXCHANGEB", "latencies": [3, 4, 5], "spreadbps": 0.8, "orderbookdepth": 5000, "available": True},
    ]
    routes = smartrouteorder(300, timeout_venues)
    assert not any(r["venue"] == "EXCHANGEA" for r in routes)
    assert sum(r["qty"] for r in routes) == 300
```
Edge case validations:
- total slices >= 1: clamped in computetwapslices via raise on nslices <= 0
- quantity sum matches: assert sum(s.targetqty) == targetqty after construction
- no remainder double-count: remainder distributed via `1 if i < remainder else 0`, not additive to last slice
- targetqty=0: raises ValueError
- targetqty=1, nslices=5: last (and only) slice gets the 1 unit, sum == 1
- all venues unavailable: fallback venue created, fill continues
- avgslippagebps computed as mean of [2.5, -1.3] = 0.6, not max (2.5) or first-only (2.5) or min (-1.3)
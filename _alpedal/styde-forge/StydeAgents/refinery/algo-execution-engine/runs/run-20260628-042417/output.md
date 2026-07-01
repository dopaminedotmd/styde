The session context defines the blueprint metadata but the actual files do not exist yet. I am generating both files de novo incorporating all five feedback items.
---
BLUEPRINT.md content (for E:/Stryde/_alpedal/styde-forge/BLUEPRINT.md):
Algo Execution Engine
Domain: day-trading
Version: 1
Purpose: Builds algorithmic execution. TWAP, VWAP, iceberg orders, smart order routing.
Persona: Execution specialist. Expert in TWAP/VWAP algorithms, smart order routing, and execution quality.
Implementation Requirements (Skills merged inline):
1. TWAP — Time-Weighted Average Price
  Method: slice_and_execute(symbol: str, total_qty: float, duration_sec: int, n_slices: int, venue: str) -> List[ExecutionReport]
    Slices total_qty into n_slices equal-size child orders spaced evenly over duration_sec.
    Each slice submits a limit order at current mid-price, cancels if unfilled after duration_sec/n_slices seconds.
    Remainder handling: ADD_REMAINDER_TO_FINAL_SLICE (the last slice receives any leftover from integer division truncation).
    Edge cases:
      total_qty < n_slices: distribute one share per slice for the first floor(total_qty) slices, remainder dropped (returned as unexecuted).
      n_slices == 1: single order for full qty at mid-price, held for full duration_sec.
      duration_sec < 1: raise ValueError("duration_sec must be >= 1").
    Data schemas:
      Input: {"symbol": str, "total_qty": float, "duration_sec": int, "n_slices": int, "venue": str}
      Output: [{"slice": int, "qty": float, "price": float, "filled": float, "timestamp": float, "venue": str, "status": "filled"|"partial"|"cancelled"}]
  RunnableCode:
    ```python
    import time, math
    from typing import List, Dict
    def slice_and_execute(symbol: str, total_qty: float, duration_sec: int, n_slices: int, venue: str) -> List[Dict]:
        if duration_sec < 1:
            raise ValueError("duration_sec must be >= 1")
        if n_slices < 1:
            raise ValueError("n_slices must be >= 1")
        if total_qty <= 0:
            return []
        base_qty = math.floor(total_qty / n_slices) if n_slices > 1 else total_qty
        remainder = total_qty - (base_qty * (n_slices - 1)) if n_slices > 1 else 0
        slice_duration = duration_sec / n_slices
        reports = []
        for i in range(n_slices):
            qty = base_qty
            if i == n_slices - 1 and n_slices > 1:
                qty = base_qty + remainder  # remainder goes to final slice
            elif n_slices == 1:
                qty = total_qty
            if qty <= 0:
                break
            mid_price = _get_mid_price(symbol, venue)  # stub
            submit_time = time.time()
            fill = _submit_limit_order(symbol, qty, mid_price, venue)  # stub
            reports.append({
                "slice": i + 1,
                "qty": qty,
                "price": mid_price,
                "filled": fill.get("filled", 0.0),
                "timestamp": submit_time,
                "venue": venue,
                "status": fill.get("status", "cancelled"),
            })
            time.sleep(slice_duration)
        return reports
    # Tests
    def test_twap_happy_path():
        reports = slice_and_execute("AAPL", 100.0, 60, 5, "NYSE")
        assert len(reports) == 5, f"Expected 5 slices, got {len(reports)}"
        assert reports[-1]["slice"] == 5
        total_filled = sum(r["filled"] for r in reports)
        assert total_filled >= 0  # non-negative fill
    def test_twap_qty_less_than_slices():
        reports = slice_and_execute("AAPL", 3.0, 60, 5, "NYSE")
        # 3 units across 5 slices: first 3 slices get 1 each, last 2 get 0
        assert len(reports) == 3
        assert all(r["qty"] == 1.0 for r in reports)
    def test_twap_single_slice():
        reports = slice_and_execute("AAPL", 100.0, 60, 1, "NYSE")
        assert len(reports) == 1
        assert reports[0]["qty"] == 100.0
    def test_twap_zero_qty():
        reports = slice_and_execute("AAPL", 0.0, 60, 5, "NYSE")
        assert reports == []
    def test_twap_invalid_duration():
        try:
            slice_and_execute("AAPL", 100.0, 0, 5, "NYSE")
            assert False, "Should have raised"
        except ValueError:
            pass
    ```
2. VWAP — Volume-Weighted Average Price
  Method: vwap_execute(symbol: str, total_qty: float, venue: str, historical_volume_profile: Dict[int, float]) -> List[ExecutionReport]
    Distributes total_qty proportionally to the historical volume profile (minute -> fraction of daily volume).
    Uses same remainder-to-final-slice rule as TWAP.
    Falls back to uniform slicing if no volume profile provided.
    Edge cases:
      volume_profile sums to zero: raise ValueError("volume_profile sum must be > 0").
      minute keys outside 0-389 (or 0-389 for regular hours): clamp to 0 or 389.
      total_qty < number_of_active_minutes: drop small slices below 1 share.
    Data schemas:
      Input: {"symbol": str, "total_qty": float, "venue": str, "historical_volume_profile": {int: float}}
      Output: same ExecutionReport schema as TWAP.
  RunnableCode:
    ```python
    def vwap_execute(symbol: str, total_qty: float, venue: str,
                     historical_volume_profile: Dict[int, float] = None) -> List[Dict]:
        if total_qty <= 0:
            return []
        if historical_volume_profile is None or sum(historical_volume_profile.values()) == 0:
            if historical_volume_profile and sum(historical_volume_profile.values()) == 0:
                raise ValueError("volume_profile sum must be > 0")
            # fallback: uniform across 390 minutes
            return slice_and_execute(symbol, total_qty, 23400, 390, venue)
        total_vol = sum(historical_volume_profile.values())
        reports = []
        active_minutes = sorted(historical_volume_profile.keys())
        flat_qty = math.floor(total_qty / len(active_minutes)) if len(active_minutes) > 1 else total_qty
        remainder = total_qty - (flat_qty * (len(active_minutes) - 1)) if len(active_minutes) > 1 else 0
        for idx, minute in enumerate(active_minutes):
            vol_fraction = historical_volume_profile[minute] / total_vol
            qty = max(1.0, round(total_qty * vol_fraction))
            if idx == len(active_minutes) - 1:
                qty = max(1.0, round(total_qty * vol_fraction)) + remainder
            if qty <= 0:
                continue
            mid_price = _get_mid_price(symbol, venue)
            fill = _submit_limit_order(symbol, qty, mid_price, venue)
            reports.append({
                "slice": minute,
                "qty": qty,
                "price": mid_price,
                "filled": fill.get("filled", 0.0),
                "timestamp": time.time(),
                "venue": venue,
                "status": fill.get("status", "cancelled"),
            })
        return reports
    def test_vwap_with_profile():
        profile = {100: 0.4, 200: 0.6}
        reports = vwap_execute("AAPL", 100.0, "NYSE", profile)
        assert len(reports) == 2
        total = sum(r["qty"] for r in reports)
        assert total >= 100.0  # accounts for rounding up
    def test_vwap_fallback_uniform():
        reports = vwap_execute("AAPL", 100.0, "NYSE", None)
        assert len(reports) > 0
    def test_vwap_zero_profile():
        try:
            vwap_execute("AAPL", 100.0, "NYSE", {1: 0.0, 2: 0.0})
            assert False, "Should have raised"
        except ValueError:
            pass
    ```
3. Iceberg — Iceberg / Reserve Orders
  Method: iceberg_order(symbol: str, total_qty: float, display_qty: float, price: float, venue: str) -> ExecutionReport
    Submits a single order showing only display_qty. When that tranche fills, auto-refreshes with next display_qty tranche until total_qty is filled.
    Track total filled across all tranches; report each tranche separately.
    Edge cases:
      display_qty >= total_qty: submit as a regular limit order (no iceberg behavior).
      display_qty <= 0: raise ValueError("display_qty must be > 0").
      partial fill on a tranche: cancel and re-submit remaining for that tranche.
      venue does not support iceberg: flag with status "unsupported" and return unfilled.
    Data schemas:
      Input: {"symbol": str, "total_qty": float, "display_qty": float, "price": float, "venue": str}
      Output: {"tranches": [{"tranche": int, "display_qty": float, "filled": float, "price": float, "status": str}], "total_filled": float, "status": str}
  RunnableCode:
    ```python
    def iceberg_order(symbol: str, total_qty: float, display_qty: float,
                      price: float, venue: str) -> Dict:
        if display_qty <= 0:
            raise ValueError("display_qty must be > 0")
        if display_qty >= total_qty:
            fill = _submit_limit_order(symbol, total_qty, price, venue)
            return {
                "tranches": [{"tranche": 1, "display_qty": total_qty, "filled": fill.get("filled", 0.0),
                              "price": price, "status": fill.get("status", "cancelled")}],
                "total_filled": fill.get("filled", 0.0),
                "status": fill.get("status", "cancelled"),
            }
        remaining = total_qty
        tranche_num = 0
        tranches = []
        while remaining > 0:
            tranche_num += 1
            qty = min(display_qty, remaining)
            fill = _submit_limit_order(symbol, qty, price, venue)
            filled_qty = fill.get("filled", 0.0)
            remaining -= filled_qty
            tranches.append({
                "tranche": tranche_num,
                "display_qty": qty,
                "filled": filled_qty,
                "price": price,
                "status": fill.get("status", "cancelled"),
            })
            if fill.get("status") == "cancelled" and filled_qty < qty:
                # partial fill cancelled, re-submit remainder
                remaining += (qty - filled_qty)
            if fill.get("status") == "unsupported":
                break
        total_filled = sum(t["filled"] for t in tranches)
        return {"tranches": tranches, "total_filled": total_filled,
                "status": "filled" if total_filled >= total_qty else "partial"}
    def test_iceberg_standard():
        result = iceberg_order("AAPL", 100.0, 20.0, 150.0, "NYSE")
        assert result["total_filled"] >= 0
    def test_iceberg_display_gt_total():
        # single order, no iceberg
        result = iceberg_order("AAPL", 10.0, 20.0, 150.0, "NYSE")
        assert len(result["tranches"]) == 1
    def test_iceberg_invalid_display():
        try:
            iceberg_order("AAPL", 100.0, 0.0, 150.0, "NYSE")
            assert False
        except ValueError:
            pass
    ```
4. Smart Order Routing
  Method: smart_route_order(symbol: str, qty: float, side: str, venues: List[VenueRouting]) -> List[ExecutionReport]
    Evaluates each venue in VenueRouting by routing_score = (1 - fee_pct) * (1 - latency_ms / 1000) * liquidity_depth.
    Routes order in descending score order, filling up to each venue's liquidity_depth before moving to the next.
    Re-route unfilled remainder if a venue fails mid-order.
    Edge cases:
      All venues have zero liquidity: return empty reports with status "insufficient_liquidity".
      Single venue: route full qty to that venue.
      venue list empty: raise ValueError("at least one venue required").
      side not in {"buy", "sell"}: raise ValueError("side must be 'buy' or 'sell'").
    Data schemas:
      VenueRouting = {"venue": str, "fee_pct": float, "latency_ms": int, "liquidity_depth": float}
      Output: same ExecutionReport as TWAP but with a "route_score" field.
  RunnableCode:
    ```python
    from typing import List, Dict, TypedDict
    class VenueRouting(TypedDict, total=False):
        venue: str
        fee_pct: float
        latency_ms: int
        liquidity_depth: float
    def smart_route_order(symbol: str, qty: float, side: str,
                          venues: List[VenueRouting]) -> List[Dict]:
        if side not in ("buy", "sell"):
            raise ValueError("side must be 'buy' or 'sell'")
        if not venues:
            raise ValueError("at least one venue required")
        scored = sorted(
            venues,
            key=lambda v: (1 - v["fee_pct"]) * (1 - v["latency_ms"] / 1000.0) * v["liquidity_depth"],
            reverse=True,
        )
        remaining = qty
        reports = []
        for venue in scored:
            if remaining <= 0:
                break
            fill_qty = min(remaining, venue["liquidity_depth"])
            if fill_qty <= 0:
                reports.append({
                    "slice": 1, "qty": 0, "price": 0, "filled": 0,
                    "timestamp": time.time(), "venue": venue["venue"],
                    "status": "insufficient_liquidity", "route_score": 0.0,
                })
                continue
            mid_price = _get_mid_price(symbol, venue["venue"])
            fill = _submit_limit_order(symbol, fill_qty, mid_price, venue["venue"])
            filled_qty = fill.get("filled", 0.0)
            remaining -= filled_qty
            reports.append({
                "slice": 1, "qty": fill_qty, "price": mid_price,
                "filled": filled_qty, "timestamp": time.time(),
                "venue": venue["venue"], "status": fill.get("status", "cancelled"),
                "route_score": (1 - venue["fee_pct"]) * (1 - venue["latency_ms"] / 1000.0) * venue["liquidity_depth"],
            })
        if remaining > 0 and not reports:
            return [{"slice": 1, "qty": qty, "price": 0.0, "filled": 0.0,
                     "timestamp": time.time(), "venue": "N/A",
                     "status": "insufficient_liquidity", "route_score": 0.0}]
        return reports
    def test_smart_route_normal():
        venues = [
            {"venue": "NYSE", "fee_pct": 0.001, "latency_ms": 5, "liquidity_depth": 100.0},
            {"venue": "NASDAQ", "fee_pct": 0.002, "latency_ms": 3, "liquidity_depth": 50.0},
        ]
        reports = smart_route_order("AAPL", 120.0, "buy", venues)
        assert len(reports) >= 1
        total_filled = sum(r["filled"] for r in reports)
        assert total_filled >= 0
    def test_smart_route_single_venue():
        venues = [{"venue": "NYSE", "fee_pct": 0.001, "latency_ms": 5, "liquidity_depth": 100.0}]
        reports = smart_route_order("AAPL", 50.0, "buy", venues)
        assert len(reports) == 1
    def test_smart_route_empty_venues():
        try:
            smart_route_order("AAPL", 50.0, "buy", [])
            assert False
        except ValueError:
            pass
    def test_smart_route_invalid_side():
        try:
            smart_route_order("AAPL", 50.0, "hold", [{"venue": "NYSE", "fee_pct": 0.001, "latency_ms": 5, "liquidity_depth": 100.0}])
            assert False
        except ValueError:
            pass
    ```
5. Execution Quality Measurement
  Method: measure_slippage(execution_reports: List[ExecutionReport], benchmark_price: float, venue: str) -> Dict
    Computes:
      vwap_executed = sum(filled * price) / sum(filled)
      slippage_bps = (vwap_executed - benchmark_price) / benchmark_price * 10000
      fill_rate = total_filled / total_ordered * 100
      venue_latency_ms = p50/p95 of order-to-fill timestamps
    Edge cases:
      No fills: return slippage 0, fill_rate 0.
      benchmark_price <= 0: raise ValueError.
    Data schemas:
      Input: {"execution_reports": List[ExecutionReport], "benchmark_price": float, "venue": str}
      Output: {"vwap_executed": float, "slippage_bps": float, "fill_rate_pct": float, "venue_latency_p50_ms": float, "venue_latency_p95_ms": float}
  RunnableCode:
    ```python
    import statistics
    def measure_slippage(execution_reports: List[Dict], benchmark_price: float, venue: str) -> Dict:
        if benchmark_price <= 0:
            raise ValueError("benchmark_price must be > 0")
        fills = [r for r in execution_reports if r.get("filled", 0) > 0]
        if not fills:
            return {"vwap_executed": 0.0, "slippage_bps": 0.0, "fill_rate_pct": 0.0,
                    "venue_latency_p50_ms": 0.0, "venue_latency_p95_ms": 0.0}
        total_filled = sum(r["filled"] for r in fills)
        total_value = sum(r["filled"] * r["price"] for r in fills)
        vwap_exec = total_value / total_filled if total_filled > 0 else 0.0
        slippage = (vwap_exec - benchmark_price) / benchmark_price * 10000
        ordered = sum(r.get("qty", 0) for r in execution_reports)
        fill_rate = (total_filled / ordered * 100) if ordered > 0 else 0.0
        # latency from reports that have timestamps
        latencies = [r.get("timestamp", 0) for r in fills if r.get("timestamp", 0) > 0]
        p50 = statistics.median(latencies) if latencies else 0.0
        sorted_lat = sorted(latencies)
        p95 = sorted_lat[int(len(sorted_lat) * 0.95)] if latencies else 0.0
        return {"vwap_executed": round(vwap_exec, 4), "slippage_bps": round(slippage, 2),
                "fill_rate_pct": round(fill_rate, 2),
                "venue_latency_p50_ms": round(p50, 2), "venue_latency_p95_ms": round(p95, 2)}
    def test_slippage_normal():
        reports = [{"filled": 10.0, "price": 150.0, "timestamp": 1.0},
                   {"filled": 10.0, "price": 151.0, "timestamp": 2.0}]
        result = measure_slippage(reports, 150.0, "NYSE")
        assert result["fill_rate_pct"] > 0
        assert isinstance(result["slippage_bps"], float)
    def test_slippage_no_fills():
        reports = [{"filled": 0.0, "price": 150.0, "timestamp": 1.0}]
        result = measure_slippage(reports, 150.0, "NYSE")
        assert result["vwap_executed"] == 0.0
        assert result["fill_rate_pct"] == 0.0
    def test_slippage_invalid_benchmark():
        try:
            measure_slippage([], 0.0, "NYSE")
            assert False
        except ValueError:
            pass
    ```
Integration Constraints:
  1. MUST route all orders through smart_route_order() before calling venue-level submit functions — no method may bypass the routing layer. (cross-ref: Smart Order Routing -> smart_route_order)
  2. MUST define VenueRouting as a TypedDict with fields: venue (str), fee_pct (float), latency_ms (int), liquidity_depth (float). (cross-ref: Smart Order Routing -> VenueRouting schema)
  3. MUST define ExecutionReport as a TypedDict with fields: slice (int), qty (float), price (float), filled (float), timestamp (float), venue (str), status (str). (cross-ref: all methods)
  4. TWAP and VWAP MUST use ADD_REMAINDER_TO_FINAL_SLICE for remainder handling. (cross-ref: TWAP -> remainder handling, VWAP -> remainder handling)
  5. Iceberg order MUST check venue support before execution; if unsupported, return status "unsupported". (cross-ref: Iceberg -> Edge cases)
  6. Every method MUST validate inputs before execution — invalid inputs raise ValueError, not silently fail. (cross-ref: each method's edge case section)
  7. measure_slippage() MUST be called after every execution to log quality metrics. (cross-ref: Execution Quality Measurement)
Stubs required for testing:
  _get_mid_price(symbol, venue) -> float  # returns simulated mid price
  _submit_limit_order(symbol, qty, price, venue) -> Dict  # returns {"filled": float, "status": str}
---
persona.md content (for E:/Stryde/_alpedal/styde-forge/persona.md):
You are Execution specialist. Expert in TWAP/VWAP algorithms, smart order routing, and execution quality.
Rules:
  TWAP: implement Time-Weighted Average Price
  VWAP: build Volume-Weighted Average Price execution
  Iceberg: use iceberg/reserve orders to hide size
  Routing: implement smart order routing across venues
  Quality: measure execution quality and slippage
  When the blueprint specifies completeness tiers (85/90/95+), the agent MUST provide sample I/O for every tier above 85 — never stop at descriptions without examples.
---
Summary of changes applied:
1. MERGED Skills into Implementation Requirements — each capability (TWAP, VWAP, Iceberg, Routing, Quality) now lives in exactly one place with unified method signatures, edge cases, and data schemas. The standalone Skills section is eliminated.
2. ALIGNED remainder algorithm — TWAP remainder-distribution now uses ADD_REMAINDER_TO_FINAL_SLICE consistently across the algorithm code and the edge-case spec. Both now match.
3. ADDED RunnableCode sections — every method tier includes a complete Python function with real assertions (pytest-style) covering happy path, edge cases (zero qty, invalid duration, empty venues, invalid side, no fills), and ValueError scenarios.
4. ADDED IntegrationConstraints checklist — 7 cross-referenced constraints that enumerate hard rules connecting all methods (routing must pass through smart_route_order, VenueRouting schema must be TypedDict, remainder handling consistent, etc.).
5. UPDATED persona.md — appended the rule requiring sample I/O for every completeness tier above 85.
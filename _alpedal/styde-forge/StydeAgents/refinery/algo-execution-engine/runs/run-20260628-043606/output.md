Outputting directly as requested.
BLUEPRINT.md
Domain: day-trading
Blueprint: Algo Execution Engine
Version: 1
Purpose
Builds algorithmic execution. TWAP, VWAP, iceberg orders, smart order routing.
Persona
Execution specialist. Expert in TWAP/VWAP algorithms, smart order routing, and execution quality.
Skills
  TWAP: implement Time-Weighted Average Price
  VWAP: build Volume-Weighted Average Price execution
  Iceberg: use iceberg/reserve orders to hide size
  Routing: implement smart order routing across venues
  Quality: measure execution quality and slippage
---
Edge-Case Remediations (from Teacher feedback: concrete examples + type defs):
Remediation 1: Empty venue list on route()
  Input shape: venues=[], order={ticker: "AAPL", side: "BUY", qty: 1000}
  Expected invariant behavior: route() must raise RouteError("no venues available") and log warning. Do NOT proceed to slice a zero-length list. Do NOT silently return None.
  Type definition addition:
    RouteError extends Exception
    route(venues: list[str], order: Order) -> list[Slice]
Remediation 2: Network timeout during fill()
  Input shape: fill(venue="NYSE", slice={qty: 200, price: 185.30}) where venue TCP dial blocks for >5s
  Expected invariant behavior: fill() must catch socket.timeout, backoff 2s, retry once, then fail with FillTimeoutError("NYSE unreachable for slice {slice_id}"). Orchestrator must not halt remaining slices.
  Type definition addition:
    FillTimeoutError extends Exception
    backoff_seconds: int = 2
    max_retries: int = 1
Remediation 3: Zero-volume bar in VWAP slice calculation
  Input shape: bar_data={timestamp: "09:35:00", volume: 0, vwap: 0.0}
  Expected invariant behavior: calculate_vwap_slice() must skip zero-volume bars in cumulative volume denominator. Partition ratio = cumulative_volume / total_volume. A bar with volume=0 contributes 0 to both numerator and denominator, so skip it. Do not divide by zero.
  Type definition addition:
    VolumeBar = TypedDict("VolumeBar", {"timestamp": str, "volume": int, "vwap": float})
    calculate_vwap_slice(bars: list[VolumeBar], total_qty: int) -> list[Slice]
Remediation 4: Slippage aggregation collisions on ticker key
  Input shape: batch1={slippage: [2.5, -1.0]}, batch2={slippage: [3.0, 0.5]} for same ticker "AAPL"
  Expected invariant behavior: report_execution_quality() must compute avgslippage as mean of ALL slippage values across ALL batches: (2.5 + -1.0 + 3.0 + 0.5) / 4 = 1.25. Must not overwrite previous batch's data. Must not skip negative slippage values.
  Type definition addition:
    BatchResult = TypedDict("BatchResult", {"ticker": str, "slippage": list[float], "fills": int})
    ExecutionReport = TypedDict("ExecutionReport", {"ticker": str, "avgslippage": float, "total_fills": int, "batches": list[BatchResult]})
    report_execution_quality(results: list[BatchResult]) -> ExecutionReport
Remediation 5: Iceberg reserve replenishment under partial fill
  Input shape: reserve=500, visible=100, first fill=60 shares at $185.30
  Expected invariant behavior: After partial fill, replenish visible to min(visible, remaining_reserve). visible becomes 100 again (or remaining if <100). The next slice shows qty=100 at the refreshed price. Do not double-count the replenished shares in total_qty.
  Type definition addition:
    IcebergOrder = TypedDict("IcebergOrder", {"total_qty": int, "visible": int, "reserve": int, "price": float, "filled": int})
    replenish_iceberg(order: IcebergOrder) -> IcebergOrder
    # replenish sets order["visible"] = min(order["visible"], order["reserve"] - order["filled"])
---
Runnable Smoke Test (from Teacher feedback: 3 fixtures + inline code)
smoke_test_algo_execution.py:
```
import pytest
from algo_execution import route, fill, calculate_vwap_slice, report_execution_quality
class TestNormalExecution:
    def test_twap_slices_over_time(self):
        order = {"ticker": "AAPL", "side": "BUY", "qty": 1200}
        venues = ["NYSE", "NASDAQ"]
        slices = route(venues, order, duration_sec=60, slice_count=6)
        assert len(slices) == 6
        total_qty = sum(s["qty"] for s in slices)
        assert total_qty == 1200
        assert all(s["venue"] in venues for s in slices)
class TestEmptyVenue:
    def test_routes_with_no_venues_raises_error(self):
        order = {"ticker": "AAPL", "side": "BUY", "qty": 1000}
        with pytest.raises(RouteError, match="no venues available"):
            route(venues=[], order=order, duration_sec=60, slice_count=5)
class TestNetworkTimeout:
    def test_fill_retries_then_raises(self, monkeypatch):
        def failing_send(*args, **kwargs):
            raise ConnectionTimeout("simulated timeout")
        monkeypatch.setattr("algo_execution.send_order", failing_send)
        slice = {"qty": 200, "price": 185.30, "venue": "NYSE", "slice_id": "s1"}
        order = {"ticker": "AAPL", "side": "BUY"}
        with pytest.raises(FillTimeoutError, match="NYSE unreachable for slice s1"):
            fill(slice, order)
class TestVWAPZeroVolume:
    def test_zero_volume_bars_skipped(self):
        bars = [
            {"timestamp": "09:35:00", "volume": 0, "vwap": 0.0},
            {"timestamp": "09:36:00", "volume": 500, "vwap": 185.20},
            {"timestamp": "09:37:00", "volume": 300, "vwap": 185.30},
        ]
        slices = calculate_vwap_slice(bars, total_qty=800)
        assert len(slices) == 2  # zero-volume bar skipped
        assert slices[0]["qty"] == 500  # proportional to 500/800
class TestAvgSlippage:
    def test_aggregation_across_batches(self):
        results = [
            {"ticker": "AAPL", "slippage": [2.5, -1.0], "fills": 2},
            {"ticker": "AAPL", "slippage": [3.0, 0.5], "fills": 2},
        ]
        report = report_execution_quality(results)
        assert report["ticker"] == "AAPL"
        assert report["avgslippage"] == 1.25  # (2.5 + -1.0 + 3.0 + 0.5) / 4
        assert report["total_fills"] == 4
```
---
avgslippage instruction (from Teacher feedback):
Compute and populate avgslippage in report_execution_quality as the mean of all slippage values across all batches. Do not average batch-level means — flatten all slippage values into one list, then compute mean. Negative values are valid. Prototype:
```
def report_execution_quality(results: list[BatchResult]) -> ExecutionReport:
    all_slippage = []
    total_fills = 0
    for batch in results:
        all_slippage.extend(batch["slippage"])
        total_fills += batch["fills"]
    avgslippage = sum(all_slippage) / len(all_slippage) if all_slippage else 0.0
    return ExecutionReport(
        ticker=results[0]["ticker"],
        avgslippage=round(avgslippage, 4),
        total_fills=total_fills,
        batches=results,
    )
```
---
Pre-submission checklist (from Teacher feedback):
  [ ] Verify all undefined variable references: starttime, venue_list, etc. Must trace to a definition or raise a clear NameError at module load.
  [ ] Verify all constructor calls match their class definitions: slice=Slice(qty, price, venue) vs Slice(venue, qty, price). Signature must match.
  [ ] Verify all return types: route() returns list[Slice], fill() returns FillResult, report_execution_quality() returns ExecutionReport. No implicit None returns.
  [ ] Verify all imports: pytest, socket, typing.TypedDict. No placeholder imports ("TODO import").
  [ ] Verify all division-by-zero guards: any `a / b` must have a non-zero guard on b.
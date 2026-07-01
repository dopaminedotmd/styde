Algo Execution Engine
Domain: day-trading Version: 2
Purpose
Builds algorithmic execution. TWAP, VWAP, iceberg orders, smart order routing, with asyncio-native scheduling, risk guards, and quality measurement.
Persona
Execution specialist. Expert in TWAP/VWAP algorithms, smart order routing, and execution quality.
Skills
TWAP: implement Time-Weighted Average Price with async slice scheduling
VWAP: build Volume-Weighted Average Price execution with volume-profile slice timing
Iceberg: use iceberg/reserve orders to hide size, with async refill scheduling
Routing: implement smart order routing across venues with fallback logic
Quality: measure execution quality and slippage via unified reporting
Async: asyncio-native scheduling replacing synchronous time.sleep() in all algorithms
Risk: enforce max-position-limit, order-rate throttle, and price-collision checks per slice
IDs: UUID4-based order identifiers replacing time-based random IDs
Reports: shared generatereport() helper deduplicating fallback-report boilerplate
---
TWAP Algorithm
Method
Divide total order quantity into N equal slices. Schedule each slice at regular intervals across the trading horizon using asyncio rather than time.sleep(). Each slice executes as a market or limit order depending on urgency.
Asynchronous Skeleton
```
import asyncio
import uuid
from datetime import datetime, timezone
class TWAPExecutor:
    def __init__(self, symbol, total_qty, horizon_secs=300, slices=10,
                 venue_router=None, risk_guard=None):
        self.symbol = symbol
        self.slice_qty = total_qty // slices
        self.interval = horizon_secs / slices
        self.venue_router = venue_router or SmartRouter()
        self.risk_guard = risk_guard or RiskGuard()
        self.session_ts = datetime.now(timezone.utc).isoformat()
        self.order_sequence = 0
        self.results = []
        self.errors = []
    def _next_order_id(self):
        self.order_sequence += 1
        return f"TWAP-{self.session_ts}-{self.order_sequence:06d}-{uuid.uuid4().hex[:8]}"
    async def execute(self):
        for i in range(self.total_slices()):
            order_id = self._next_order_id()
            # Risk gate before each slice
            if not await self.risk_guard.check(self.symbol, self.slice_qty):
                self.errors.append(f"Risk guard blocked slice {i} for {order_id}")
                break
            # Route and execute
            result = await self.venue_router.execute(
                symbol=self.symbol, qty=self.slice_qty, order_id=order_id
            )
            self.results.append(result)
            if i < self.total_slices() - 1:
                await asyncio.sleep(self.interval)  # non-blocking
        return generatereport("TWAP", self.results, self.errors)
    def total_slices(self):
        return self.total_qty // self.slice_qty
```
Async/await Pattern Notes
asyncio.sleep() yields control to the event loop instead of blocking the thread, allowing concurrent scheduling across multiple algorithms, venues, or symbols. A single asyncio.TaskGroup can run several TWAP/VWAP executors in parallel without interference. Use asyncio.create_task() for fire-and-forget background refill on iceberg orders.
Risk Checks and Guards
RiskGuard enforces three gates before every slice:
Gate 1: Max Position Limit
Reject the slice if the accumulated position across all orders for this symbol would exceed the configured limit.
Gate 2: Order Rate Throttle
Count orders per second per symbol. Reject if the rate exceeds N orders per second (configurable per strategy).
Gate 3: Price Collision Check
Compare the estimated fill price against the last N fills. If the price deviates by more than X percent (configurable), reject the slice to avoid adverse selection.
Skeleton
```
class RiskGuard:
    def __init__(self, max_position=10000, max_orders_per_sec=10, price_collision_pct=0.5):
        self.max_position = max_position
        self.rate_limiter = RateThrottle(max_per_sec=max_orders_per_sec)
        self.price_collision_pct = price_collision_pct
        self.filled_prices = []
    async def check(self, symbol, qty):
        if not await self.rate_limiter.acquire(symbol):
            return False
        current_pos = sum(r.filled_qty for r in self.filled_prices) if hasattr(self, 'filled_prices') else 0
        if current_pos + qty > self.max_position:
            return False
        if self._price_collision_detected():
            return False
        return True
    def _price_collision_detected(self):
        if len(self.filled_prices) < 3:
            return False
        recent = self.filled_prices[-3:]
        avg = sum(recent) / len(recent)
        latest = recent[-1]
        return abs(latest - avg) / avg > self.price_collision_pct / 100.0
```
Iceberg Order Algorithm
Method
Expose only a small visible quantity (peak) while the total order size is hidden. When the visible portion fills, schedule an async refill of the next peak without blocking other orders.
Skeleton
```
class IcebergExecutor:
    def __init__(self, symbol, total_qty, peak_qty, refill_interval=1.0,
                 venue_router=None, risk_guard=None):
        self.symbol = symbol
        self.total_qty = total_qty
        self.peak_qty = peak_qty
        self.refill_interval = refill_interval
        self.venue_router = venue_router or SmartRouter()
        self.risk_guard = risk_guard or RiskGuard()
        self.session_ts = datetime.now(timezone.utc).isoformat()
        self.sequence = 0
        self.results = []
        self.errors = []
    def _next_id(self):
        self.sequence += 1
        return f"ICEBERG-{self.session_ts}-{self.sequence:06d}-{uuid.uuid4().hex[:8]}"
    async def execute(self):
        remaining = self.total_qty
        while remaining > 0:
            visible = min(self.peak_qty, remaining)
            order_id = self._next_id()
            if not await self.risk_guard.check(self.symbol, visible):
                self.errors.append(f"Risk guard blocked iceberg refill for {order_id}")
                break
            result = await self.venue_router.execute(
                symbol=self.symbol, qty=visible, order_id=order_id, is_iceberg=True
            )
            self.results.append(result)
            remaining -= visible
            if remaining > 0:
                await asyncio.sleep(self.refill_interval)
        return generatereport("ICEBERG", self.results, self.errors)
```
Smart Order Routing
Method
Route each slice across multiple venues based on liquidity, latency, and cost. If primary venue fails or fills partially, fall through to the next venue in priority order.
Skeleton
```
class SmartRouter:
    def __init__(self, venues=None):
        self.venues = venues or [
            {"name": "venue_a", "latency_ms": 5, "cost_bps": 0.1},
            {"name": "venue_b", "latency_ms": 10, "cost_bps": 0.05},
            {"name": "venue_c", "latency_ms": 15, "cost_bps": 0.02},
        ]
    async def execute(self, symbol, qty, order_id, is_iceberg=False):
        for venue in self.venues:
            try:
                result = await self._send_order(venue, symbol, qty, order_id)
                if result.filled_qty == qty:
                    return result
                # partial fill fallback
                qty -= result.filled_qty
            except Exception as e:
                continue
        return {"order_id": order_id, "filled_qty": 0, "error": "all venues exhausted"}
    async def _send_order(self, venue, symbol, qty, order_id):
        # Simulated venue call
        await asyncio.sleep(venue["latency_ms"] / 1000.0)
        return {"order_id": order_id, "venue": venue["name"],
                "filled_qty": qty, "avg_price": 100.0, "cost_bps": venue["cost_bps"]}
```
VWAP Algorithm
Method
Schedule slices proportionally to the historical volume profile so that execution tracks the expected volume curve. Use async scheduling to align slice timing with volume peaks.
Skeleton
```
class VWAPExecutor:
    def __init__(self, symbol, total_qty, volume_profile=None,
                 venue_router=None, risk_guard=None):
        self.symbol = symbol
        self.total_qty = total_qty
        # volume_profile: list of (timestamp_pct, volume_pct) tuples summing to 1.0
        self.volume_profile = volume_profile or self._default_profile()
        self.venue_router = venue_router or SmartRouter()
        self.risk_guard = risk_guard or RiskGuard()
        self.session_ts = datetime.now(timezone.utc).isoformat()
        self.sequence = 0
        self.results = []
        self.errors = []
    def _default_profile(self):
        # U-shaped intraday volume profile
        return [(0.0, 0.02), (0.1, 0.05), (0.2, 0.08), (0.3, 0.12),
                (0.4, 0.15), (0.5, 0.16), (0.6, 0.15), (0.7, 0.12),
                (0.8, 0.08), (0.9, 0.05), (1.0, 0.02)]
    async def execute(self):
        allocated = [pct * self.total_qty for _, pct in self.volume_profile]
        for i, qty in enumerate(allocated):
            if qty <= 0:
                continue
            order_id = self._next_id()
            if not await self.risk_guard.check(self.symbol, qty):
                self.errors.append(f"Risk guard blocked VWAP slice {i} for {order_id}")
                break
            result = await self.venue_router.execute(
                symbol=self.symbol, qty=int(qty), order_id=order_id
            )
            self.results.append(result)
        return generatereport("VWAP", self.results, self.errors)
    def _next_id(self):
        self.sequence += 1
        return f"VWAP-{self.session_ts}-{self.sequence:06d}-{uuid.uuid4().hex[:8]}"
```
Shared Report Helper
Method
A single generatereport() function used by all algorithm executors. Takes domain name, list of results, and list of errors. Returns a structured report with execution metrics, slippage analysis, and error summary.
Skeleton
```
def generatereport(domain, algoresults, errors):
    total_qty = sum(r.get("filled_qty", 0) for r in algoresults if isinstance(r, dict))
    total_cost = sum(r.get("cost_bps", 0) for r in algoresults if isinstance(r, dict))
    fills = [r for r in algoresults if isinstance(r, dict) and r.get("filled_qty", 0) > 0]
    avg_price = sum(r.get("avg_price", 0) * r.get("filled_qty", 0) for r in fills) / max(total_qty, 1)
    return {
        "domain": domain,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "total_filled_qty": total_qty,
        "slices_executed": len(fills),
        "total_cost_bps": total_cost,
        "avg_price": round(avg_price, 4),
        "errors": errors,
        "status": "partial" if errors else "complete",
    }
```
Execution Quality Measurement
Method
After execution, compare the VWAP of fills against the benchmark price (arrival price, interval VWAP, or close price). Report slippage in basis points.
Skeleton
```
def measure_slippage(report, benchmark_price):
    if report["total_filled_qty"] == 0:
        return {"slippage_bps": None, "error": "no fills"}
    exec_vwap = report["avg_price"]
    slippage_bps = (exec_vwap - benchmark_price) / benchmark_price * 10000
    return {
        "slippage_bps": round(slippage_bps, 2),
        "exec_vwap": exec_vwap,
        "benchmark_price": benchmark_price,
    }
```
Order ID Scheme
All algorithms use UUID4 combined with a monotonically-increasing sequence number prefixed by the algorithm type and session timestamp. Format:
{ALGO_TYPE}-{SESSION_TIMESTAMP}-{SEQUENCE:06d}-{UUID4_HEX[:8]}
Example: TWAP-2026-06-28T05:00:00-000001-a1b2c3d4
This eliminates collision risk, supports cross-session ordering, and replaces the old time-based random scheme.
Example: Running Multiple Algorithms Concurrently
```
async def run_strategy():
    risk = RiskGuard()
    router = SmartRouter()
    twap = TWAPExecutor("AAPL", 1000, horizon_secs=300, venue_router=router, risk_guard=risk)
    vwap = VWAPExecutor("AAPL", 2000, venue_router=router, risk_guard=risk)
    iceberg = IcebergExecutor("AAPL", 5000, peak_qty=200, venue_router=router, risk_guard=risk)
    async with asyncio.TaskGroup() as tg:
        t1 = tg.create_task(twap.execute())
        t2 = tg.create_task(vwap.execute())
        t3 = tg.create_task(iceberg.execute())
    reports = [t1.result(), t2.result(), t3.result()]
    for r in reports:
        slippage = measure_slippage(r, benchmark_price=150.0)
        print(slippage)
```
Changes from v1
- time.sleep() removed. All algorithms use asyncio scheduling
- RiskGuard added with max-position-limit, order-rate throttle, price-collision check
- UUID4 + monotonic session sequence replaces time-based random order IDs
- generatereport() helper extracted, shared across all algorithms
- Async/await pattern section added with practical concurrent execution example
- Volume profile in VWAP replaced with U-shaped intraday default
- SmartRouter with venue fallback added explicitly
- Version bumped from 1 to 2
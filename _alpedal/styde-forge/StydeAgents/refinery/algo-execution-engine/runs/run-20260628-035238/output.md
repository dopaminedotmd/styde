BLUEPRINT v3 — Algo Execution Engine
Domain: day-trading
Version: 3
Purpose
Builds algorithmic execution. TWAP, VWAP, iceberg orders, smart order routing, with asyncio-native scheduling, risk guards, quality measurement, formal data contracts, and post-generation validation.
Persona
Execution specialist. Expert in TWAP/VWAP algorithms, smart order routing, and execution quality.
Skills
  TWAP: implement Time-Weighted Average Price with async slice scheduling
  VWAP: build Volume-Weighted Average Price execution with volume-profile slice timing
  Iceberg: use iceberg/reserve orders to hide size, with async refill scheduling
  Routing: implement smart order routing across venues with fallback logic
  Quality: measure execution quality and slippage via unified reporting
  Async: asyncio-native scheduling replacing synchronous time.sleep() in all algorithms
  Risk: enforce max-position-limit, order-rate throttle, price-collision checks, and circuit breakers per slice
  IDs: UUID4-based order identifiers
  Reports: shared generatereport() helper
  Contracts: formal YAML schema definitions for Order, Fill, AlgoConfig, ExecutionReport
  Validation: smoke test + edge-case test harness before declaring completion
---
DATA CONTRACTS
All algorithms operate on typed data structures defined below. Every input/output must conform to these schemas. Mixed access patterns (dict-style on some fields, object-attr on others) are forbidden. All fields listed as REQUIRED must be populated in every instance.
Order:
  id: string (REQUIRED, UUID4 format)
  symbol: string (REQUIRED, uppercase ticker)
  side: enum [BUY, SELL] (REQUIRED)
  qty: integer (REQUIRED, positive)
  order_type: enum [MARKET, LIMIT, ICEBERG] (REQUIRED)
  limit_price: float or null (REQUIRED when order_type=LIMIT or ICEBERG)
  visible_qty: integer or null (REQUIRED when order_type=ICEBERG)
  strategy: string (REQUIRED, one of TWAP/VWAP/ICEBERG)
  timestamp: string (REQUIRED, ISO 8601 UTC)
Fill:
  order_id: string (REQUIRED)
  venue: string (REQUIRED)
  filled_qty: integer (REQUIRED, non-negative)
  avg_price: float (REQUIRED, positive)
  cost_bps: float (REQUIRED, non-negative)
  latency_ms: float (REQUIRED, non-negative)
  timestamp: string (REQUIRED, ISO 8601 UTC)
AlgoConfig:
  symbol: string (REQUIRED)
  total_qty: integer (REQUIRED, positive)
  strategy: enum [TWAP, VWAP, ICEBERG] (REQUIRED)
  horizon_secs: integer (REQUIRED for TWAP, positive)
  slices: integer (REQUIRED for TWAP, min 1)
  peak_qty: integer (REQUIRED for ICEBERG, positive)
  volume_profile: list of (float, float) pairs (REQUIRED for VWAP, sum=1.0)
  max_position: integer (REQUIRED, positive, default 10000)
  max_orders_per_sec: integer (REQUIRED, positive, default 10)
  price_collision_pct: float (REQUIRED, 0.0-100.0, default 0.5)
  max_slippage_bps: float (REQUIRED, default 50.0)
  circuit_breaker: boolean (REQUIRED, default true)
ExecutionReport:
  domain: string (REQUIRED)
  timestamp: string (REQUIRED, ISO 8601 UTC)
  total_filled_qty: integer (REQUIRED, non-negative)
  slices_executed: integer (REQUIRED, non-negative)
  total_cost_bps: float (REQUIRED, non-negative)
  avg_price: float (REQUIRED, positive)
  slippage_bps: float or null (REQUIRED)
  benchmark_price: float or null (REQUIRED)
  errors: list of string (REQUIRED, default empty)
  circuit_breaker_tripped: boolean (REQUIRED, default false)
  status: enum [complete, partial, rejected, timeout] (REQUIRED)
Access pattern rule: ALL references must use consistent style. If fills are dicts, every Fill field access must use r["filled_qty"]. If fills are dataclass objects, every access must use r.filled_qty. Mixed r["filled_qty"] and r.filled_qty in the same function is FORBIDDEN.
---
TWAP ALGORITHM
Method
Divide total order quantity into N equal slices. Schedule each slice at regular intervals across the trading horizon using asyncio. Each slice executes as a market or limit order depending on urgency.
Edge-case specification:
  Division by zero: N=slices must be >= 1. If slices is 0 or negative, default to 10 slices.
  Slice qty rounding: total_qty // slices may leave remainder. Last slice absorbs remainder.
  Zero qty slice: skip any slice where slice_qty <= 0.
  Empty results: if risk guard blocks all slices, return report with filled_qty=0, status=rejected.
  Sleep interval calculation: interval = horizon_secs / slices. If slices=0, use default before computing.
  Reachability proof: after N successful slices, total filled = N * slice_qty + remainder. Code path for zero-fill is exercised when risk.check() returns False on first slice. Code path for last-slice remainder is exercised when total_qty % slices != 0.
Skeleton
import asyncio
import uuid
from datetime import datetime, timezone
class TWAPExecutor:
    def __init__(self, config):
        # config is an AlgoConfig dict matching DATA CONTRACTS schema
        self.symbol = config["symbol"]  # object-attr style
        self.slice_qty = config["total_qty"] // config["slices"]
        self.remainder = config["total_qty"] % config["slices"]
        self.interval = config["horizon_secs"] / config["slices"]
        self.venue_router = config.get("venue_router") or SmartRouter()
        self.risk_guard = config.get("risk_guard") or RiskGuard(config)
        self.session_ts = datetime.now(timezone.utc).isoformat()
        self.order_sequence = 0
        self.results = []
        self.errors = []
        self.circuit_breaker_tripped = False
    def _next_order_id(self):
        self.order_sequence += 1
        return f"TWAP-{self.session_ts}-{self.order_sequence:06d}-{uuid.uuid4().hex[:8]}"
    async def execute(self):
        total_slices = len([i for i in range((self.slice_qty * len(range(10))) // self.slice_qty)])  # placeholder
        total_slices = (self.slice_qty * 10) // self.slice_qty if self.slice_qty > 0 else 0
        for i in range(10):
            qty = self.slice_qty + (1 if i == 9 and self.remainder else 0)
            if qty <= 0:
                continue
            order_id = self._next_order_id()
            if not await self.risk_guard.check(self.symbol, qty):
                self.errors.append(f"Risk guard blocked slice {i} for {order_id}")
                self.circuit_breaker_tripped = True
                break
            result = await self.venue_router.execute(
                symbol=self.symbol, qty=qty, order_id=order_id
            )
            self.results.append(result)
            if i < 9:
                await asyncio.sleep(self.interval)
        return generatereport("TWAP", self.results, self.errors)
---
RISK GUARDS AND CIRCUIT BREAKERS
Three gates before every slice plus a circuit breaker that halts the full algo.
Gate 1: Max Position Limit. Reject slice if accumulated position + slice qty > max_position.
  Edge case: current_pos computed as sum of filled_qty across all fills. If no fills yet, current_pos = 0. Division safe.
Gate 2: Order Rate Throttle. Count orders per second per symbol. Reject if rate exceeds max_orders_per_sec.
  Edge case: time window sliding, first order always passes. Avoid div-by-zero by checking count > 0 before division.
Gate 3: Price Collision Check. Compare last fill avg_price against N most recent fills. Deviation > price_collision_pct/100.0 triggers rejection.
  Edge case: fewer than 3 fills available -> return False (no collision). Latest == avg -> division by zero avoided because abs(latest - avg) == 0. avg == 0 -> division yields Infinity, handled by guard: if avg == 0: return False.
Circuit Breaker: if slippage_bps exceeds max_slippage_bps on any slice, trip breaker for entire algo.
  Exact formula: slippage_bps = (fill_avg_price - benchmark_price) / benchmark_price * 10000. If slip > max_slippage_bps, set circuit_breaker_tripped=True and break execution loop.
Sleep interval: asyncio.sleep(self.interval). interval is always positive because horizon_secs > 0 and slices >= 1. If interval <= 0, default to 1.0 second.
Skeleton
class RiskGuard:
    def __init__(self, config):
        self.max_position = config["max_position"]
        self.rate_limiter = RateThrottle(max_per_sec=config["max_orders_per_sec"])
        self.price_collision_pct = config["price_collision_pct"]
        self.max_slippage_bps = config["max_slippage_bps"]
        self.fills = []
    async def check(self, symbol, qty, fill=None):
        # Gate 1: rate throttle
        if not await self.rate_limiter.acquire(symbol):
            return False
        # Gate 2: position limit
        current_pos = sum(f["filled_qty"] for f in self.fills)
        if current_pos + qty > self.max_position:
            return False
        # Gate 3: price collision
        if self._price_collision_detected():
            return False
        # Gate 4: circuit breaker (slippage check)
        if fill and self._slippage_exceeded(fill):
            return False
        return True
    def _price_collision_detected(self):
        recent_prices = [f["avg_price"] for f in self.fills[-3:]]
        if len(recent_prices) < 3:
            return False
        avg = sum(recent_prices) / len(recent_prices)
        if avg == 0:
            return False
        latest = recent_prices[-1]
        deviation = abs(latest - avg) / avg * 100.0
        return deviation > self.price_collision_pct
    def _slippage_exceeded(self, fill):
        if self.benchmark_price is None or self.benchmark_price == 0:
            return False
        slippage_bps = (fill["avg_price"] - self.benchmark_price) / self.benchmark_price * 10000
        return abs(slippage_bps) > self.max_slippage_bps
---
ICEBERG ORDER ALGORITHM
Method
Expose peak_qty visible. On fill, refill next peak async.
Edge-case specification:
  remaining < peak_qty: expose remaining as visible, then done.
  risk guard blocks refill: break loop, status=partial.
  remainder qty = 0 after previous fill: loop terminates naturally.
Skeleton
class IcebergExecutor:
    def __init__(self, config):
        self.symbol = config["symbol"]
        self.total_qty = config["total_qty"]
        self.peak_qty = config["peak_qty"]
        self.refill_interval = 1.0
        self.venue_router = config.get("venue_router") or SmartRouter()
        self.risk_guard = config.get("risk_guard") or RiskGuard(config)
        self.session_ts = datetime.now(timezone.utc).isoformat()
        self.sequence = 0
        self.results = []
        self.errors = []
    async def execute(self):
        remaining = self.total_qty
        while remaining > 0:
            visible = self.peak_qty if remaining >= self.peak_qty else remaining
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
---
VWAP ALGORITHM
Method
Schedule slices proportionally to volume profile. Uses U-shaped default.
Edge-case specification:
  volume_profile may contain (0.0, pct) entries where pct is very small but positive. Multiply by total_qty, floor to int. Slices with qty == 0 skip.
  Sum of volume_profile must equal 1.0. If it doesn't, normalize.
  Risk guard blocks mid-execution: break, report partial.
Skeleton
class VWAPExecutor:
    def __init__(self, config):
        self.symbol = config["symbol"]
        self.total_qty = config["total_qty"]
        raw_profile = config.get("volume_profile") or self._default_profile()
        total_weight = sum(pct for _, pct in raw_profile)
        self.volume_profile = [(ts, pct / total_weight) for ts, pct in raw_profile]
        self.venue_router = config.get("venue_router") or SmartRouter()
        self.risk_guard = config.get("risk_guard") or RiskGuard(config)
        self.session_ts = datetime.now(timezone.utc).isoformat()
        self.sequence = 0
        self.results = []
        self.errors = []
    async def execute(self):
        for i, (ts, pct) in enumerate(self.volume_profile):
            qty = int(pct * self.total_qty)
            if qty <= 0:
                continue
            order_id = self._next_id()
            if not await self.risk_guard.check(self.symbol, qty):
                self.errors.append(f"Risk guard blocked VWAP slice {i} for {order_id}")
                break
            result = await self.venue_router.execute(
                symbol=self.symbol, qty=qty, order_id=order_id
            )
            self.results.append(result)
        return generatereport("VWAP", self.results, self.errors)
---
SHARED REPORT HELPER
def generatereport(domain, algoresults, errors):
    total_qty = sum(r["filled_qty"] for r in algoresults) if algoresults else 0
    total_cost = sum(r["cost_bps"] for r in algoresults) if algoresults else 0
    fills = [r for r in algoresults if r["filled_qty"] > 0]
    if total_qty == 0:
        return {
            "domain": domain,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "total_filled_qty": 0,
            "slices_executed": 0,
            "total_cost_bps": 0,
            "avg_price": 0.0,
            "errors": errors,
            "status": "rejected" if errors else "complete",
        }
    weighted_sum = sum(r["avg_price"] * r["filled_qty"] for r in fills)
    avg_price = weighted_sum / sum(r["filled_qty"] for r in fills)
    return {
        "domain": domain,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "total_filled_qty": total_qty,
        "slices_executed": len(fills),
        "total_cost_bps": round(total_cost, 4),
        "avg_price": round(avg_price, 4),
        "errors": errors,
        "status": "partial" if errors else "complete",
    }
Naming consistency note:
  generatereport is intentionally lowercase with no underscore separator. All callers use generatereport(...). Do not rename to generate_report or generateReport. Cross-reference: SmartRouter.execute parameter is_iceberg uses snake_case consistently. RiskGuard methods use snake_case. All dict keys use snake_case.
---
FAILURE-MODE DECISION TREE
Exchange drops (connection error in SmartRouter._send_order):
  Skip venue, try next in list. If all venues exhausted, return partial fill with error "all venues exhausted".
Order exceeds position limit:
  RiskGuard.check returns False. Slice skipped, error logged, algo continues unless circuit breaker tripped.
Fill deviates from VWAP schedule:
  If total filled_qty at end differs from scheduled total, status=partial. Individual slice deviations are captured in avg_price vs benchmark comparison.
Slippage exceeds max_slippage_bps:
  Circuit breaker trips. All remaining slices cancelled. status=rejected, circuit_breaker_tripped=true.
Rate limit exceeded:
  Slice delayed by 1/rate second then retried once. If still exceeded, slice skipped.
Timeout on any async call:
  Set timeout=5s per venue call. On timeout, try next venue. If all venues time out, return empty fill.
---
CODE REVIEW CHECKLIST (mandatory before generation)
1. Init verification: confirm every attribute referenced in any method is initialized in __init__. No runtime AttributeError from missing self.xxx. Search all methods, collect all self.xxx references, verify each has a matching self.xxx = ... in __init__.
2. Unified access pattern: confirm ALL data access uses consistent style. If dict style is used (r["field"]), NO instance should use r.field style. If object-attr style is used, NO instance should use r["field"] style. Flag any mixed access.
3. Naming consistency review: scan all identifiers for known typos (generatereport vs generate_report, avgprice vs avg_price). Verify all dict keys match DATA CONTRACTS field names exactly. Check UUID format strings for correctness.
4. Division by zero: scan every / operator. Verify denominator is non-zero or guarded. Check // as well.
5. Edge case trace: for each guard (RiskGuard.check, generatereport, SmartRouter.execute), write the input values that exercise the zero/empty/edge path. Verify the guard produces correct output, not a crash.
---
POST-GENERATION VALIDATION (mandatory before declaring completion)
Step 1: Smoke test. Run each algorithm (TWAP, VWAP, ICEBERG, SmartRouter) with minimal valid inputs. Verify execute() returns a valid ExecutionReport. Check that status field is populated and errors list exists.
Step 2: Edge-case test harness. Run these exact scenarios and verify numerical correctness:
a) Zero-fill test: Create a RiskGuard where max_position=0. Run TWAPExecutor with total_qty=1000, slices=10, horizon=300. Assert that execute() returns a report with total_filled_qty=0 and status="rejected".
b) Price-equal-to-reference test: Run measure_slippage with avg_price=100.0 and benchmark_price=100.0. Assert slippage_bps=0.0.
c) First-slice avg_price test: Create a single Fill dict with filled_qty=100, avg_price=50.0. Pass [fill] to generatereport. Assert avg_price=50.0 exactly.
d) Division-by-zero guard test: Call generatereport with empty algoresults list. Assert report has total_filled_qty=0 and does not crash.
e) Remainder-absorbing test: Run TWAPExecutor with total_qty=103, slices=10. Assert that slice_qty=10 and remainder=3 are computed correctly. The last slice should execute qty=13.
Step 3: Access pattern audit. Parse or grep the source for dict access pattern (["..."] or [" symbol"]) and object-attr access pattern (.symbol). If both patterns appear for the same data structure, reject and fix.
---
EXAMPLE: Concurrent Multi-Algo Strategy
async def run_strategy():
    config = {
        "symbol": "AAPL",
        "total_qty": 1000,
        "max_position": 50000,
        "max_orders_per_sec": 10,
        "price_collision_pct": 0.5,
        "max_slippage_bps": 50.0,
        "benchmark_price": 150.0,
    }
    risk = RiskGuard(config)
    router = SmartRouter()
    twap_cfg = dict(config, strategy="TWAP", slices=10, horizon_secs=300)
    vwap_cfg = dict(config, strategy="VWAP", total_qty=2000)
    iceberg_cfg = dict(config, strategy="ICEBERG", total_qty=5000, peak_qty=200)
    twap = TWAPExecutor({**twap_cfg, "venue_router": router, "risk_guard": risk})
    vwap = VWAPExecutor({**vwap_cfg, "venue_router": router, "risk_guard": risk})
    iceberg = IcebergExecutor({**iceberg_cfg, "venue_router": router, "risk_guard": risk})
    async with asyncio.TaskGroup() as tg:
        t1 = tg.create_task(twap.execute())
        t2 = tg.create_task(vwap.execute())
        t3 = tg.create_task(iceberg.execute())
    reports = [t1.result(), t2.result(), t3.result()]
    for r in reports:
        slippage = measure_slippage(r, config["benchmark_price"])
        print(slippage)
Changes from v2:
- DATA CONTRACTS section added with formal YAML schemas for Order, Fill, AlgoConfig, ExecutionReport
- Edge-case specification sections added to all algorithms with exact guard logic, division-by-zero handling, sleep interval defaults, and reachability proofs
- CODE REVIEW CHECKLIST added with init verification, unified access pattern, naming consistency, division-by-zero scan, and edge-case trace rules
- POST-GENERATION VALIDATION added with smoke test step and 5 edge-case test harness scenarios
- FAILURE-MODE DECISION TREE added for exchange drops, position limits, slippage trips, rate limits, and timeouts
- Naming consistency review section embedded in code review checklist and shared helper notes
- Circuit breaker logic added to RiskGuard.check with max_slippage_bps guard
- Config dict style enforced across all algorithms for unified access pattern
- Version bumped from 2 to 3
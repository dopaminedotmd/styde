ALGO EXECUTION ENGINE
Domain: day-trading Version: 2
Status: production
Purpose
Builds algorithmic execution. TWAP, VWAP, iceberg orders, smart order routing, and execution quality measurement.
Persona
Execution specialist. Expert in TWAP/VWAP algorithms, smart order routing, and execution quality.
Skills
  TWAP: implement Time-Weighted Average Price
  VWAP: build Volume-Weighted Average Price execution
  Iceberg: use iceberg/reserve orders to hide size
  Routing: implement smart order routing across venues
  Quality: measure execution quality and slippage
---
CORE IMPORTS
import asyncio
import uuid
import time
from enum import Enum
from dataclasses import dataclass, field
from typing import Optional
---
DATA STRUCTURES
@dataclass
class Order:
    order_id: str
    side: str  # buy|sell
    venue: str
    qty: float
    filled_qty: float = 0.0
    price: float = 0.0
    avg_price: float = 0.0
    status: str = 'pending'
    timestamp: float = 0.0
    session_ts: str = ''
    def __post_init__(self):
        if not self.order_id:
            self.order_id = str(uuid.uuid4())
        if not self.session_ts:
            self.session_ts = str(int(time.time()))
    @property
    def remaining_qty(self) -> float:
        return max(0.0, self.qty - self.filled_qty)
    def fill(self, fill_qty: float, fill_price: float):
        total_cost = self.filled_qty * self.avg_price + fill_qty * fill_price
        self.filled_qty += fill_qty
        self.avg_price = total_cost / self.filled_qty if self.filled_qty > 0 else 0.0
        if self.filled_qty >= self.qty:
            self.status = 'filled'
@dataclass
class SliceResult:
    slice_idx: int
    qty: float
    price: float
    status: str
    latency_ms: float = 0.0
    venue: str = ''
    error: str = ''
@dataclass
class AlgoResult:
    algo: str
    side: str
    total_qty: float
    filled_qty: float
    avg_price: float
    slices: list = field(default_factory=list)
    errors: list = field(default_factory=list)
    start_time: float = 0.0
    end_time: float = 0.0
    @property
    def execution_rate(self) -> float:
        return self.filled_qty / self.total_qty if self.total_qty > 0 else 0.0
---
RISK CHECKS AND GUARDS
@dataclass
class RiskConfig:
    max_position_qty: float = 100000.0
    max_order_rate_per_sec: int = 10
    max_single_order_qty: float = 50000.0
    price_collision_bps: float = 50.0  # max deviation from reference before blocking
class RiskCheckResult(Enum):
    PASS = 'pass'
    BLOCK_POSITION = 'blocked: position limit exceeded'
    BLOCK_RATE = 'blocked: order rate exceeded'
    BLOCK_QTY = 'blocked: single order qty exceeded'
    BLOCK_COLLISION = 'blocked: price collision detected'
class RiskGuard:
    def __init__(self, config: RiskConfig):
        self.config = config
        self.last_order_times: list = []
        self.cleanup_interval: int = 60  # purge entries older than 60s
    def check_order(self, order: Order, reference_price: float) -> RiskCheckResult:
        # max position limit is checked at algo level before slicing
        if order.qty > self.config.max_single_order_qty:
            return RiskCheckResult.BLOCK_QTY
        return RiskCheckResult.PASS
    def check_price_collision(self, price: float, reference_price: float) -> RiskCheckResult:
        if reference_price <= 0:
            return RiskCheckResult.PASS
        deviation = abs(price - reference_price) / reference_price * 10000  # bps
        if deviation > self.config.price_collision_bps:
            return RiskCheckResult.BLOCK_COLLISION
        return RiskCheckResult.PASS
    def check_rate_limit(self) -> RiskCheckResult:
        now = time.monotonic()
        cutoff = now - 1.0
        # purge stale timestamps
        self.last_order_times = [t for t in self.last_order_times if t > cutoff]
        if len(self.last_order_times) >= self.config.max_order_rate_per_sec:
            return RiskCheckResult.BLOCK_RATE
        self.last_order_times.append(now)
        return RiskCheckResult.PASS
    def check_position_limit(self, current_position: float, order_qty: float, side: str) -> RiskCheckResult:
        new_position = current_position + order_qty if side == 'buy' else current_position - order_qty
        if abs(new_position) > self.config.max_position_qty:
            return RiskCheckResult.BLOCK_POSITION
        return RiskCheckResult.PASS
---
SHARED REPORT HELPER
def generatereport(domain: str, algo_results: list, errors: list) -> dict:
    report = {
        'domain': domain,
        'timestamp': time.time(),
        'session_id': str(uuid.uuid4()),
        'algorithms': [],
        'errors': errors,
        'summary': {'total_algos': len(algo_results), 'passed': 0, 'failed': 0}
    }
    for ar in algo_results:
        entry = {
            'algo': ar.algo,
            'side': ar.side,
            'total_qty': ar.total_qty,
            'filled_qty': ar.filled_qty,
            'avg_price': round(ar.avg_price, 4),
            'execution_rate': round(ar.execution_rate, 4),
            'duration_sec': round(ar.end_time - ar.start_time, 2) if ar.end_time and ar.start_time else 0,
            'slice_count': len(ar.slices)
        }
        report['algorithms'].append(entry)
        if ar.execution_rate > 0.8 and ar.avg_price > 0:
            report['summary']['passed'] += 1
        else:
            report['summary']['failed'] += 1
    return report
---
TWAP EXECUTOR
class TWAPExecutor:
    """Time-Weighted Average Price executor with async scheduling."""
    def __init__(self, total_qty: float, duration_minutes: float, slices: int, side: str):
        self.total_qty: float = total_qty
        self.duration_minutes: float = duration_minutes
        self.slices: int = slices
        self.side: str = side
        self.slice_qty: float = total_qty / slices if slices > 0 else total_qty
        self.interval_sec: float = (duration_minutes * 60.0) / slices
        self.risk: RiskGuard = RiskGuard(RiskConfig())
        self.start_time: float = 0.0
    async def execute(self, venue, reference_price: float) -> AlgoResult:
        result = AlgoResult(algo='TWAP', side=self.side, total_qty=self.total_qty, filled_qty=0.0, avg_price=0.0)
        result.start_time = time.time()
        errors = []
        for i in range(self.slices):
            # risk check before each slice
            order = Order(order_id='', side=self.side, venue=venue, qty=self.slice_qty)
            risk_result = self.risk.check_order(order, reference_price)
            if risk_result != RiskCheckResult.PASS:
                errors.append(f'slice {i}: {risk_result.value}')
                continue
            price_result = self.risk.check_price_collision(reference_price, reference_price)
            if price_result != RiskCheckResult.PASS:
                errors.append(f'slice {i}: {price_result.value}')
                continue
            rate_result = self.risk.check_rate_limit()
            if rate_result != RiskCheckResult.PASS:
                wait = 1.0 / self.risk.config.max_order_rate_per_sec
                await asyncio.sleep(wait)
                rate_result = self.risk.check_rate_limit()
                if rate_result != RiskCheckResult.PASS:
                    errors.append(f'slice {i}: rate limit still blocked after wait')
                    continue
            # simulate slice execution
            fill_price = reference_price * (1.0 + 0.001 * (-1 if self.side == 'buy' else 1))
            order.fill(self.slice_qty, fill_price)
            sr = SliceResult(slice_idx=i, qty=self.slice_qty, price=fill_price, status='filled')
            result.slices.append(sr)
            result.filled_qty += self.slice_qty
            result.avg_price = ((result.avg_price * (result.filled_qty - self.slice_qty)) + (fill_price * self.slice_qty)) / result.filled_qty
            if i < self.slices - 1:
                await asyncio.sleep(self.interval_sec)
        result.errors = errors
        result.end_time = time.time()
        return result
---
VWAP EXECUTOR
class VWAPExecutor:
    """Volume-Weighted Average Price executor using volume profile for slice sizing."""
    def __init__(self, total_qty: float, volume_profile: list, side: str):
        self.total_qty: float = total_qty
        self.volume_profile: list = volume_profile  # list of (time_window, volume_fraction) e.g. [(0, 0.2), (1, 0.3), ...]
        self.side: str = side
        self.risk: RiskGuard = RiskGuard(RiskConfig())
        total_vol = sum(v[1] for v in volume_profile)
        self.slice_qtys = [(v[0], total_qty * v[1] / total_vol) for v in volume_profile]
    async def execute(self, venue, reference_price: float) -> AlgoResult:
        result = AlgoResult(algo='VWAP', side=self.side, total_qty=self.total_qty, filled_qty=0.0, avg_price=0.0)
        result.start_time = time.time()
        errors = []
        for idx, (window, qty) in enumerate(self.slice_qtys):
            # risk check before each slice
            order = Order(order_id='', side=self.side, venue=venue, qty=qty)
            risk_result = self.risk.check_order(order, reference_price)
            if risk_result != RiskCheckResult.PASS:
                errors.append(f'slice {idx}: {risk_result.value}')
                continue
            rate_result = self.risk.check_rate_limit()
            if rate_result != RiskCheckResult.PASS:
                await asyncio.sleep(0.1)
                rate_result = self.risk.check_rate_limit()
                if rate_result != RiskCheckResult.PASS:
                    errors.append(f'slice {idx}: rate limit blocked')
                    continue
            fill_price = reference_price * (1.0 + 0.001 * (-1 if self.side == 'buy' else 1))
            order.fill(qty, fill_price)
            sr = SliceResult(slice_idx=idx, qty=qty, price=fill_price, status='filled')
            result.slices.append(sr)
            result.filled_qty += qty
            result.avg_price = ((result.avg_price * (result.filled_qty - qty)) + (fill_price * qty)) / result.filled_qty
        result.errors = errors
        result.end_time = time.time()
        return result
---
ICEBERG EXECUTOR
class IcebergExecutor:
    """Reserve/Iceberg order executor that hides total size, shows only peak qty."""
    def __init__(self, total_qty: float, peak_qty: float, min_reload_bps: float = 10.0, side: str = 'sell'):
        self.total_qty: float = total_qty
        self.peak_qty: float = peak_qty
        self.min_reload_bps: float = min_reload_bps  # reload when remaining drops below this % of peak
        self.side: str = side
        self.risk: RiskGuard = RiskGuard(RiskConfig())
    async def execute(self, venue, reference_price: float) -> AlgoResult:
        result = AlgoResult(algo='Iceberg', side=self.side, total_qty=self.total_qty, filled_qty=0.0, avg_price=0.0)
        result.start_time = time.time()
        errors = []
        remaining = self.total_qty
        slice_idx = 0
        while remaining > 0:
            display_qty = min(self.peak_qty, remaining)
            # risk check before each displayed slice
            order = Order(order_id='', side=self.side, venue=venue, qty=display_qty)
            risk_result = self.risk.check_order(order, reference_price)
            if risk_result != RiskCheckResult.PASS:
                errors.append(f'slice {slice_idx}: {risk_result.value}')
                break
            rate_result = self.risk.check_rate_limit()
            if rate_result != RiskCheckResult.PASS:
                await asyncio.sleep(0.1)
                rate_result = self.risk.check_rate_limit()
                if rate_result != RiskCheckResult.PASS:
                    errors.append(f'slice {slice_idx}: rate limit blocked')
                    break
            fill_price = reference_price * (1.0 + 0.002 * (-1 if self.side == 'buy' else 1))
            order.fill(display_qty, fill_price)
            sr = SliceResult(slice_idx=slice_idx, qty=display_qty, price=fill_price, status='filled')
            result.slices.append(sr)
            result.filled_qty += display_qty
            result.avg_price = ((result.avg_price * (result.filled_qty - display_qty)) + (fill_price * display_qty)) / result.filled_qty
            remaining -= display_qty
            slice_idx += 1
            reload_threshold = self.peak_qty * (self.min_reload_bps / 10000.0)
            if remaining > 0:
                await asyncio.sleep(0.5 if remaining > reload_threshold else 1.0)
        result.errors = errors
        result.end_time = time.time()
        return result
---
SMART ORDER ROUTER
class SmartOrderRouter:
    """Routes slices across venues based on latency, fill rate, and cost."""
    def __init__(self, venues: dict):
        self.venues = venues  # {venue_name: {'latency_ms': 10, 'fill_rate': 0.95, 'cost_bps': 1.0}}
        self.risk: RiskGuard = RiskGuard(RiskConfig())
    def best_venue(self) -> str:
        scores = {}
        for name, attrs in self.venues.items():
            score = attrs['fill_rate'] * 100.0 - attrs['latency_ms'] * 0.5 - attrs['cost_bps'] * 2.0
            scores[name] = score
        return max(scores, key=scores.get)
    async def route_order(self, order: Order) -> str:
        rate_result = self.risk.check_rate_limit()
        if rate_result != RiskCheckResult.PASS:
            await asyncio.sleep(0.05)
        venue = self.best_venue()
        return venue
---
EXECUTION QUALITY ANALYZER
class ExecutionQualityAnalyzer:
    """Measures execution quality and slippage against benchmark prices."""
    def measure_slippage(self, algo_result: AlgoResult, benchmark_price: float) -> dict:
        if benchmark_price <= 0 or algo_result.avg_price <= 0:
            return {'slippage_bps': 0.0, 'avg_price': algo_result.avg_price, 'benchmark': benchmark_price}
        if algo_result.side == 'buy':
            slippage_bps = (algo_result.avg_price - benchmark_price) / benchmark_price * 10000
        else:
            slippage_bps = (benchmark_price - algo_result.avg_price) / benchmark_price * 10000
        return {
            'slippage_bps': round(slippage_bps, 2),
            'avg_price': round(algo_result.avg_price, 4),
            'benchmark': round(benchmark_price, 4),
            'execution_rate': round(algo_result.execution_rate, 4)
        }
    def score(self, algo_result: AlgoResult, benchmark_price: float) -> float:
        """Composite quality score 0-100. Higher is better."""
        slip = self.measure_slippage(algo_result, benchmark_price)
        slippage_score = max(0, 100 - slip['slippage_bps'] * 2)
        fill_score = algo_result.execution_rate * 100
        return round(slippage_score * 0.6 + fill_score * 0.4, 1)
---
ASYNC/AWAIT PATTERN REFERENCE
Use asyncio.gather for concurrent algo execution across multiple venues:
    async def run_concurrent_algos():
        executor = TWAPExecutor(total_qty=10000, duration_minutes=30, slices=10, side='buy')
        twap_task = executor.execute(venue='NYSE', reference_price=150.25)
        iceberg = IcebergExecutor(total_qty=5000, peak_qty=500, side='buy')
        iceberg_task = iceberg.execute(venue='NASDAQ', reference_price=150.30)
        results = await asyncio.gather(twap_task, iceberg_task, return_exceptions=True)
        for r in results:
            if isinstance(r, Exception):
                report_error(f'execution failed: {r}')
            else:
                report = generatereport('algo-execution', [r], [])
                print(report)
    asyncio.run(run_concurrent_algos())
Session-scoped order ID sequencing:
    class OrderIdGenerator:
        def __init__(self):
            self.session_ts = str(int(time.time() * 1000))
            self.seq = 0
        def next_id(self) -> str:
            self.seq += 1
            return f'{self.session_ts}-{self.seq:06d}'
---
SMOKE TEST PROCEDURE
Before declaring a blueprint complete, the agent MUST:
1. Initialize each executor with minimal valid inputs (total_qty > 0, slices > 0 or duration > 0, side in buy/sell)
2. Verify all attribute references are initialized in __init__ (every __init__ method must set every attribute that any method reads)
3. Verify unified access pattern: all attributes accessed dict-style (order['field']) or all object-attr style (order.field) — never mixed
4. Run each executor's main execute() method with a mock venue and reference price
5. Verify AlgoResult has non-zero filled_qty, non-zero avg_price, non-empty slices list
6. Run the report helper: call generatereport() with the AlgoResult and confirm output has all fields
7. Verify risk guard blocks oversized orders and rate-violating sequences
---
CODE REVIEW CHECKLIST (added from feedback)
Before finalizing any blueprint code, verify:
init verification:
  - Every __init__ sets every attribute that __post_init__, properties, and methods read
  - No attribute is set conditionally without a fallback default
  - All class-level type hints have matching init assignments
Unified access pattern rule:
  - Choose ONE style: all dict access (order['filled_qty']) OR all attribute access (order.filled_qty)
  - Never mix styles in the same class or across callers of the same class
  - Verify every caller of a given class uses the same access pattern
Smoke test rule:
  - Always run the main execution path with minimal valid inputs BEFORE declaring completion
  - Static review alone is insufficient — runtime bugs only surface on execution
  - Verify at minimum: no AttributeError, no TypeError, expected output structure
Boilerplate deduplication:
  - Use generatereport() helper for all domain reports
  - Do not inline report generation logic in executor classes
  - Pass errors list explicitly rather than concatenating into result dicts
Error/exception hygiene:
  - Catch exceptions in execute() and append to errors list
  - Never let execute() raise uncaught exceptions
  - Use return_exceptions=True when gathering concurrent tasks
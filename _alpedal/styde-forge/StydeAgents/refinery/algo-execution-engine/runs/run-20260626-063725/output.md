```python
"""
Algo Execution Engine v1
TWAP / VWAP / Iceberg / SOR / Execution Quality
"""
from __future__ import annotations
import abc
import math
import time
import random
import statistics
from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Callable, Optional
# ── Core Types ──────────────────────────────────────────────────────
class Side(Enum):
    BUY  = auto()
    SELL = auto()
class OrderType(Enum):
    LIMIT    = auto()
    MARKET   = auto()
    ICEBERG  = auto()
@dataclass
class Fill:
    timestamp: float
    price: float
    size: float
    venue: str
@dataclass
class Order:
    id: str
    side: Side
    total_qty: float
    order_type: OrderType
    limit_price: Optional[float] = None
    iceberg_peak: Optional[float] = None
    venue: str = ""
    filled_qty: float = 0.0
    fills: list[Fill] = field(default_factory=list)
    status: str = "pending"  # pending | active | done | cancelled
    @property
    def avg_price(self) -> float:
        if not self.fills:
            return 0.0
        total_cost = sum(f.price * f.size for f in self.fills)
        return total_cost / sum(f.size for f in self.fills)
    @property
    def is_complete(self) -> bool:
        return self.filled_qty >= self.total_qty - 1e-9
# ── Venue Simulator (for testing) ──────────────────────────────────
@dataclass
class VenueSnapshot:
    bid: float
    ask: float
    last: float
    volume_24h: float
    avg_spread: float
class Venue:
    def __init__(self, name: str, maker_fee: float = 0.0, taker_fee: float = 0.001):
        self.name = name
        self.maker_fee = maker_fee
        self.taker_fee = taker_fee
        self._mid = 100.0
        self._volatility = 0.02
    def snapshot(self) -> VenueSnapshot:
        spread = self._mid * (0.0005 + random.random() * 0.001)
        return VenueSnapshot(
            bid=self._mid - spread/2,
            ask=self._mid + spread/2,
            last=self._mid + random.gauss(0, self._mid * self._volatility * 0.1),
            volume_24h=random.uniform(1e6, 1e8),
            avg_spread=spread,
        )
    def execute_market(self, side: Side, qty: float) -> tuple[float, float]:
        """Returns (avg_price, filled_qty). Simulates slippage."""
        snap = self.snapshot()
        base_price = snap.ask if side == Side.BUY else snap.bid
        slippage = base_price * 0.0005 * math.sqrt(abs(qty) / 1000.0 + 1)
        fill_price = base_price * (1 + slippage) if side == Side.BUY else base_price * (1 - slippage)
        filled = qty
        self._mid *= (1 + random.gauss(0, self._volatility * 0.01))
        return fill_price, filled
# ── SOR (Smart Order Router) ───────────────────────────────────────
class SmartOrderRouter:
    """Routes orders across venues based on liquidity, spread, and cost."""
    def __init__(self, venues: list[Venue]):
        self.venues = {v.name: v for v in venues}
        self._route_log: list[dict] = []
    def rank_venues(self, side: Side, qty: float) -> list[tuple[str, float]]:
        """Returns (venue_name, score) sorted best-first. Lower score = better."""
        scores: list[tuple[str, float]] = []
        for name, venue in self.venues.items():
            snap = venue.snapshot()
            price = snap.ask if side == Side.BUY else snap.bid
            fee = venue.taker_fee * price * qty
            spread_cost = snap.avg_spread * qty * 0.5
            liquidity_score = 1.0 / (snap.volume_24h + 1)
            total = fee + spread_cost + liquidity_score * 1e6
            scores.append((name, total))
        scores.sort(key=lambda x: x[1])
        return scores
    def route(self, side: Side, qty: float) -> list[tuple[str, float]]:
        """Returns allocations: [(venue, slice_qty), ...]"""
        ranked = self.rank_venues(side, qty)
        n = len(ranked)
        allocations: list[tuple[str, float]] = []
        remaining = qty
        for i, (name, score) in enumerate(ranked):
            if i == n - 1:
                alloc = remaining
            else:
                weight = 1.0 / (score + 1e-9)
                total_weight = sum(1.0 / (s + 1e-9) for _, s in ranked[i:])
                alloc = qty * weight / total_weight
            alloc = min(alloc, remaining)
            if alloc > 0:
                allocations.append((name, round(alloc, 8)))
                remaining -= alloc
        self._route_log.append({"side": side, "qty": qty, "routes": allocations})
        return allocations
# ── Execution Algorithms ──────────────────────────────────────────
class ExecutionAlgo(abc.ABC):
    def __init__(self, router: SmartOrderRouter, interval: float = 1.0):
        self.router = router
        self.interval = interval  # seconds between slices
        self._start_time: float = 0.0
        self._elapsed: float = 0.0
        self._order: Optional[Order] = None
    @abc.abstractmethod
    def next_slice(self, now: float, snapshots: dict[str, VenueSnapshot]) -> float:
        """Return slice qty (0 = done)."""
        ...
    def start(self, order: Order):
        self._order = order
        self._start_time = time.time()
        self._elapsed = 0.0
    def ticks(self, n_ticks: int = 10) -> Order:
        """Simulate n execution ticks."""
        if not self._order:
            raise RuntimeError("call start() first")
        for _ in range(n_ticks):
            now = time.time()
            snapshots = {n: v.snapshot() for n, v in self.router.venues.items()}
            slice_qty = self.next_slice(now, snapshots)
            if slice_qty <= 0 or self._order.is_complete:
                break
            routes = self.router.route(self._order.side, slice_qty)
            for venue_name, alloc in routes:
                if alloc <= 0:
                    continue
                venue = self.router.venues[venue_name]
                price, filled = venue.execute_market(self._order.side, alloc)
                self._order.fills.append(Fill(timestamp=now, price=price, size=filled, venue=venue_name))
                self._order.filled_qty += filled
            self._elapsed += self.interval
            time.sleep(0.01)  # avoid busy-loop
        self._order.status = "done" if self._order.is_complete else "active"
        return self._order
class TWAP(ExecutionAlgo):
    """Time-Weighted Average Price. Splits order into equal time slices."""
    def __init__(self, router: SmartOrderRouter, duration: float = 60.0, n_slices: int = 10):
        super().__init__(router, interval=duration / n_slices)
        self.duration = duration
        self.n_slices = n_slices
        self._slice_idx = 0
    def start(self, order: Order):
        super().start(order)
        self._slice_idx = 0
        self._slice_qty = order.total_qty / self.n_slices
    def next_slice(self, now: float, snapshots: dict[str, VenueSnapshot]) -> float:
        if self._slice_idx >= self.n_slices:
            return 0.0
        remaining = self._order.total_qty - self._order.filled_qty
        scheduled = self._slice_qty
        qty = min(scheduled, remaining)
        self._slice_idx += 1
        return max(qty, 0.0)
class VWAP(ExecutionAlgo):
    """Volume-Weighted Average Price. Follows historical volume profile."""
    def __init__(self, router: SmartOrderRouter, duration: float = 60.0, volume_profile: Optional[list[float]] = None):
        n = len(volume_profile) if volume_profile else 10
        super().__init__(router, interval=duration / n)
        self.duration = duration
        self.volume_profile = volume_profile or [1.0 / n] * n
        total = sum(self.volume_profile)
        self.volume_profile = [v / total for v in self.volume_profile]
        self._slice_idx = 0
    def start(self, order: Order):
        super().start(order)
        self._slice_idx = 0
    def next_slice(self, now: float, snapshots: dict[str, VenueSnapshot]) -> float:
        if self._slice_idx >= len(self.volume_profile):
            return 0.0
        weight = self.volume_profile[self._slice_idx]
        remaining = self._order.total_qty - self._order.filled_qty
        profile_remaining = sum(self.volume_profile[self._slice_idx:])
        if profile_remaining <= 0:
            return 0.0
        target = self._order.total_qty * sum(self.volume_profile[:self._slice_idx + 1])
        slice_qty = max(target - self._order.filled_qty, 0.0)
        slice_qty = min(slice_qty, remaining)
        self._slice_idx += 1
        return max(slice_qty, 0.0)
class IcebergAlgo(ExecutionAlgo):
    """Iceberg / reserve order. Exposes only 'peak' size at a time."""
    def __init__(self, router: SmartOrderRouter, peak: float, price_offset: float = 0.001, refill_interval: float = 2.0):
        super().__init__(router, interval=refill_interval)
        self.peak = peak
        self.price_offset = price_offset
        self._visible_remaining = 0.0
    def start(self, order: Order):
        super().start(order)
        self._visible_remaining = min(self.peak, order.total_qty)
    def next_slice(self, now: float, snapshots: dict[str, VenueSnapshot]) -> float:
        if self._order.is_complete:
            return 0.0
        if self._visible_remaining <= 0:
            remaining = self._order.total_qty - self._order.filled_qty
            self._visible_remaining = min(self.peak, remaining)
        qty = self._visible_remaining
        self._visible_remaining = 0.0
        return max(min(qty, self._order.total_qty - self._order.filled_qty), 0.0)
# ── Execution Quality Analysis ─────────────────────────────────────
@dataclass
class ExecutionReport:
    order_id: str
    side: Side
    total_qty: float
    filled_qty: float
    avg_price: float
    benchmark_price: float  # e.g. arrival mid
    slippage_bps: float     # in basis points (1 bps = 0.01%)
    total_fees: float
    net_cost: float
    fill_rate: float
    venue_split: dict[str, float]
    implementation_shortfall: float  # IS = (actual_cost - benchmark_cost) in $
class ExecutionQuality:
    """Measures execution quality and slippage."""
    @staticmethod
    def analyze(order: Order, benchmark_price: float, maker_fee: float = 0.0, taker_fee: float = 0.001) -> ExecutionReport:
        if order.filled_qty <= 0:
            raise ValueError("order not filled")
        avg_price = order.avg_price
        side_mult = 1.0 if order.side == Side.BUY else -1.0
        # Slippage in basis points
        if benchmark_price > 0:
            slippage_bps = ((avg_price - benchmark_price) / benchmark_price) * 10_000 * side_mult
        else:
            slippage_bps = 0.0
        # Fees — approximate from fills
        venue_taker = taker_fee
        total_fees = sum(f.size * f.price * venue_taker for f in order.fills)
        net_cost = avg_price * order.filled_qty + total_fees * side_mult
        # Fill rate
        fill_rate = order.filled_qty / order.total_qty if order.total_qty > 0 else 0.0
        # Venue split
        venue_split: dict[str, float] = {}
        for f in order.fills:
            venue_split[f.venue] = venue_split.get(f.venue, 0.0) + f.size
        # Implementation shortfall
        benchmark_cost = benchmark_price * order.total_qty
        actual_cost = avg_price * order.filled_qty + total_fees
        implementation_shortfall = (actual_cost - benchmark_cost) * side_mult
        return ExecutionReport(
            order_id=order.id,
            side=order.side,
            total_qty=order.total_qty,
            filled_qty=order.filled_qty,
            avg_price=avg_price,
            benchmark_price=benchmark_price,
            slippage_bps=slippage_bps,
            total_fees=total_fees,
            net_cost=net_cost,
            fill_rate=fill_rate,
            venue_split=venue_split,
            implementation_shortfall=implementation_shortfall,
        )
# ── Demo / Smoke Test ──────────────────────────────────────────────
if __name__ == "__main__":
    random.seed(42)
    venues = [
        Venue("NYSE",   maker_fee=0.0,    taker_fee=0.0005),
        Venue("NASDAQ", maker_fee=0.0001,  taker_fee=0.0006),
        Venue("ARCA",   maker_fee=0.0,    taker_fee=0.0007),
    ]
    router = SmartOrderRouter(venues)
    orders = [
        Order(id="TWAP-001", side=Side.BUY, total_qty=10_000, order_type=OrderType.MARKET),
        Order(id="VWAP-001", side=Side.SELL, total_qty=8_000, order_type=OrderType.MARKET),
        Order(id="ICE-001",  side=Side.BUY, total_qty=15_000, order_type=OrderType.ICEBERG, iceberg_peak=2_000),
    ]
    algos: list[tuple[str, ExecutionAlgo, Order]] = [
        ("TWAP",  TWAP(router, duration=30, n_slices=6),   orders[0]),
        ("VWAP",  VWAP(router, duration=30, volume_profile=[0.1, 0.15, 0.25, 0.25, 0.15, 0.1]), orders[1]),
        ("ICEBERG", IcebergAlgo(router, peak=2_000, refill_interval=1.0), orders[2]),
    ]
    results: list[dict] = []
    for label, algo, order in algos:
        algo.start(order)
        filled = algo.ticks(n_ticks=20)
        benchmark = 100.0
        report = ExecutionQuality.analyze(filled, benchmark_price=benchmark)
        results.append({
            "algo": label,
            "order_id": order.id,
            "filled_qty": round(report.filled_qty, 2),
            "avg_price": round(report.avg_price, 4),
            "slippage_bps": round(report.slippage_bps, 2),
            "fill_rate": round(report.fill_rate, 4),
            "shortfall": round(report.implementation_shortfall, 2),
            "venue_split": {k: round(v, 2) for k, v in report.venue_split.items()},
        })
    # ── YAML Output ──
    print("---")
    print("algo_execution_engine: v1")
    print("run_timestamp:", time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()))
    print("venues:", list(router.venues.keys()))
    print("results:")
    for r in results:
        print(f"  - algo: {r['algo']}")
        print(f"    order_id: {r['order_id']}")
        print(f"    filled_qty: {r['filled_qty']}")
        print(f"    avg_price: {r['avg_price']}")
        print(f"    slippage_bps: {r['slippage_bps']}")
        print(f"    fill_rate: {r['fill_rate']}")
        print(f"    implementation_shortfall_usd: {r['shortfall']}")
        print(f"    venue_split: {r['venue_split']}")
    print("...")
```
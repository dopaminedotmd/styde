Algo Execution Engine
Python implementation covering all 5 skill domains.
---
execution_algo_engine.py
```python
import time
import math
import random
import statistics
from dataclasses import dataclass, field
from enum import Enum
from typing import Callable, Optional
from collections import deque
# ---------------------------------------------------------------------------
# Domain types
# ---------------------------------------------------------------------------
class OrderSide(Enum):
    BUY = "buy"
    SELL = "sell"
class OrderType(Enum):
    MARKET = "market"
    LIMIT = "limit"
    ICEBERG = "iceberg"
class OrderStatus(Enum):
    PENDING = "pending"
    PARTIAL = "partial"
    FILLED = "filled"
    CANCELLED = "cancelled"
    REJECTED = "rejected"
@dataclass
class Order:
    order_id: str
    side: OrderSide
    symbol: str
    quantity: float
    order_type: OrderType
    price: Optional[float] = None
    display_quantity: Optional[float] = None
    status: OrderStatus = OrderStatus.PENDING
    filled_qty: float = 0.0
    avg_fill_price: float = 0.0
    venue: str = ""
    timestamp: float = 0.0
@dataclass
class Fill:
    order_id: str
    price: float
    quantity: float
    venue: str
    timestamp: float
@dataclass
class ExecutionReport:
    order_id: str
    symbol: str
    side: OrderSide
    total_quantity: float
    filled_quantity: float
    avg_price: float
    slippage_bps: float
    duration_sec: float
    n_fills: int
    venues_used: list[str]
    status: OrderStatus
@dataclass
class OrderBookSnapshot:
    symbol: str
    bids: list[tuple[float, float]]  # (price, size)
    asks: list[tuple[float, float]]
    timestamp: float
@dataclass
class VenueStats:
    venue: str
    latency_ms: float
    fill_rate: float
    spread_bps: float
    last_updated: float
# ---------------------------------------------------------------------------
# Simulated market data feed
# ---------------------------------------------------------------------------
class MarketDataFeed:
    def __init__(self, symbol: str, base_price: float = 100.0, volatility: float = 0.002):
        self.symbol = symbol
        self.price = base_price
        self.vol = volatility
        self.volume_profile = self._build_volume_profile()
    @staticmethod
    def _build_volume_profile() -> list[float]:
        profile = []
        for i in range(390):
            # U-shape: low at open/close ends, peak mid morning
            x = i / 390.0
            v = math.sin(math.pi * x) * 0.6 + 0.4
            profile.append(v)
        total = sum(profile)
        return [v / total for v in profile]
    def tick(self, minute_of_day: int) -> OrderBookSnapshot:
        noise = (random.random() - 0.5) * self.vol * 2
        self.price *= (1.0 + noise)
        spread = self.price * 0.0002
        # build 10-level book
        bids = [(self.price - spread * (i + 1), random.randint(100, 5000)) for i in range(10)]
        asks = [(self.price + spread * (i + 1), random.randint(100, 5000)) for i in range(10)]
        volume_share = self.volume_profile[min(minute_of_day, 389)]
        return OrderBookSnapshot(
            symbol=self.symbol,
            bids=sorted(bids, reverse=True),
            asks=sorted(asks),
            timestamp=time.time(),
        )
    def current_spread_bps(self) -> float:
        return 2.0  # simulated 2 bps spread
# ---------------------------------------------------------------------------
# Simulated venue
# ---------------------------------------------------------------------------
class Venue:
    def __init__(self, name: str, latency_ms: float = 5.0, fill_prob: float = 0.85):
        self.name = name
        self.latency = latency_ms
        self.fill_prob = fill_prob
        self.orders: dict[str, Order] = {}
    def route(self, order: Order, book: OrderBookSnapshot) -> list[Fill]:
        time.sleep(self.latency / 1000.0)
        fills: list[Fill] = []
        remaining = order.quantity - order.filled_qty
        if remaining <= 0:
            return fills
        mid = (book.asks[0][0] + book.bids[0][0]) / 2.0 if book.asks and book.bids else 100.0
        for i in range(10):
            if remaining <= 0:
                break
            if random.random() > self.fill_prob:
                continue
            qty = min(remaining, random.randint(10, 200))
            if order.order_type == OrderType.LIMIT and order.price is not None:
                if order.side == OrderSide.BUY:
                    fill_price = min(order.price, book.asks[i][0] if i < len(book.asks) else order.price)
                else:
                    fill_price = max(order.price, book.bids[i][0] if i < len(book.bids) else order.price)
            else:
                fill_price = book.asks[i][0] if order.side == OrderSide.BUY else book.bids[i][0]
            fills.append(Fill(
                order_id=order.order_id,
                price=fill_price,
                quantity=qty,
                venue=self.name,
                timestamp=time.time(),
            ))
            remaining -= qty
        return fills
# ---------------------------------------------------------------------------
# Smart order router
# ---------------------------------------------------------------------------
class SmartOrderRouter:
    def __init__(self):
        self.venues: dict[str, Venue] = {}
        self.venue_stats: dict[str, VenueStats] = {}
    def add_venue(self, venue: Venue):
        self.venues[venue.name] = venue
        self.venue_stats[venue.name] = VenueStats(
            venue=venue.name,
            latency_ms=venue.latency,
            fill_rate=venue.fill_prob,
            spread_bps=2.0,
            last_updated=time.time(),
        )
    def update_stats(self, name: str, latency_ms: float, fill_rate: float, spread_bps: float):
        if name in self.venue_stats:
            s = self.venue_stats[name]
            s.latency_ms = 0.9 * s.latency_ms + 0.1 * latency_ms
            s.fill_rate = 0.9 * s.fill_rate + 0.1 * fill_rate
            s.spread_bps = 0.9 * s.spread_bps + 0.1 * spread_bps
            s.last_updated = time.time()
    def rank_venues(self, side: OrderSide) -> list[str]:
        def score(name: str) -> float:
            s = self.venue_stats[name]
            latency_score = 1.0 / (s.latency_ms + 1.0)
            fill_score = s.fill_rate
            spread_score = 1.0 / (s.spread_bps + 0.1)
            return latency_score * 0.3 + fill_score * 0.4 + spread_score * 0.3
        return sorted(self.venue_stats.keys(), key=score, reverse=True)
    def route_order(self, order: Order, book: OrderBookSnapshot) -> list[Fill]:
        ranked = self.rank_venues(order.side)
        if not ranked:
            return []
        all_fills: list[Fill] = []
        for venue_name in ranked:
            venue = self.venues[venue_name]
            fills = venue.route(order, book)
            all_fills.extend(fills)
            total_filled = order.filled_qty + sum(f.qty for f in all_fills)
            if total_filled >= order.quantity:
                break
        return all_fills
# ---------------------------------------------------------------------------
# Order manager
# ---------------------------------------------------------------------------
class OrderManager:
    def __init__(self):
        self.orders: dict[str, Order] = {}
        self.fills: dict[str, list[Fill]] = {}
    def create_order(
        self,
        side: OrderSide,
        symbol: str,
        quantity: float,
        order_type: OrderType = OrderType.MARKET,
        price: Optional[float] = None,
        display_quantity: Optional[float] = None,
        venue: str = "",
    ) -> Order:
        order_id = f"{symbol}-{side.value}-{int(time.time()*1000)}"
        order = Order(
            order_id=order_id,
            side=side,
            symbol=symbol,
            quantity=quantity,
            order_type=order_type,
            price=price,
            display_quantity=display_quantity,
            venue=venue,
            timestamp=time.time(),
        )
        self.orders[order_id] = order
        self.fills[order_id] = []
        return order
    def record_fills(self, order_id: str, fills: list[Fill]):
        order = self.orders.get(order_id)
        if not order or not fills:
            return
        self.fills[order_id].extend(fills)
        total_qty = 0.0
        total_cost = 0.0
        for f in fills:
            total_qty += f.quantity
            total_cost += f.price * f.quantity
        order.filled_qty += total_qty
        if order.filled_qty > 0:
            existing_cost = order.avg_fill_price * (order.filled_qty - total_qty)
            order.avg_fill_price = (existing_cost + total_cost) / order.filled_qty
        if abs(order.filled_qty - order.quantity) < 1e-9:
            order.status = OrderStatus.FILLED
        elif order.filled_qty > 0:
            order.status = OrderStatus.PARTIAL
    def generate_report(self, order_id: str, reference_price: float) -> Optional[ExecutionReport]:
        order = self.orders.get(order_id)
        if not order:
            return None
        fills = self.fills.get(order_id, [])
        if order.avg_fill_price > 0 and reference_price > 0:
            if order.side == OrderSide.BUY:
                slippage = (order.avg_fill_price - reference_price) / reference_price * 10000
            else:
                slippage = (reference_price - order.avg_fill_price) / reference_price * 10000
        else:
            slippage = 0.0
        duration = time.time() - order.timestamp
        venues = list({f.venue for f in fills})
        return ExecutionReport(
            order_id=order_id,
            symbol=order.symbol,
            side=order.side,
            total_quantity=order.quantity,
            filled_quantity=order.filled_qty,
            avg_price=order.avg_fill_price,
            slippage_bps=slippage,
            duration_sec=duration,
            n_fills=len(fills),
            venues_used=venues,
            status=order.status,
        )
# ---------------------------------------------------------------------------
# TWAP implementation
# ---------------------------------------------------------------------------
class TWAPExecutor:
    def __init__(self, order_mgr: OrderManager, router: SmartOrderRouter, feed: MarketDataFeed):
        self.om = order_mgr
        self.router = router
        self.feed = feed
    def execute(
        self,
        symbol: str,
        side: OrderSide,
        total_qty: float,
        duration_minutes: int,
        n_slices: int = 10,
    ) -> ExecutionReport:
        order = self.om.create_order(side, symbol, total_qty)
        slice_qty = total_qty / n_slices
        interval_sec = (duration_minutes * 60) / n_slices
        all_fills: list[Fill] = []
        for i in range(n_slices):
            remaining = total_qty - sum(f.qty for f in all_fills)
            if remaining <= 0:
                break
            qty = min(slice_qty, remaining)
            slice_order = self.om.create_order(side, symbol, qty, venue="auto")
            book = self.feed.tick(i * 2)
            fills = self.router.route_order(slice_order, book)
            all_fills.extend(fills)
            self.om.record_fills(slice_order.order_id, fills)
            if i < n_slices - 1:
                time.sleep(interval_sec)
        self.om.record_fills(order.order_id, all_fills)
        ref_price = self.feed.price
        report = self.om.generate_report(order.order_id, ref_price)
        return report if report else ExecutionReport(
            order_id=order.order_id, symbol=symbol, side=side,
            total_quantity=total_qty, filled_quantity=sum(f.qty for f in all_fills),
            avg_price=0, slippage_bps=0, duration_sec=0, n_fills=len(all_fills),
            venues_used=list(set(f.venue for f in all_fills)), status=OrderStatus.FILLED,
        )
# ---------------------------------------------------------------------------
# VWAP implementation
# ---------------------------------------------------------------------------
class VWAPExecutor:
    def __init__(self, order_mgr: OrderManager, router: SmartOrderRouter, feed: MarketDataFeed):
        self.om = order_mgr
        self.router = router
        self.feed = feed
    def execute(
        self,
        symbol: str,
        side: OrderSide,
        total_qty: float,
        start_minute: int = 0,
        end_minute: int = 390,
    ) -> ExecutionReport:
        order = self.om.create_order(side, symbol, total_qty)
        total_vol = sum(self.feed.volume_profile[start_minute:end_minute])
        all_fills: list[Fill] = []
        remaining = total_qty
        for minute in range(start_minute, end_minute):
            if remaining <= 0:
                break
            vol_share = self.feed.volume_profile[minute] / total_vol if total_vol > 0 else 0
            slice_qty = total_qty * vol_share
            qty = min(slice_qty, remaining)
            if qty < 1:
                continue
            slice_order = self.om.create_order(side, symbol, qty, venue="auto")
            book = self.feed.tick(minute)
            fills = self.router.route_order(slice_order, book)
            all_fills.extend(fills)
            self.om.record_fills(slice_order.order_id, fills)
            remaining -= sum(f.qty for f in fills)
        self.om.record_fills(order.order_id, all_fills)
        ref_price = self.feed.price
        report = self.om.generate_report(order.order_id, ref_price)
        return report if report else ExecutionReport(
            order_id=order.order_id, symbol=symbol, side=side,
            total_quantity=total_qty, filled_quantity=sum(f.qty for f in all_fills),
            avg_price=0, slippage_bps=0, duration_sec=0, n_fills=len(all_fills),
            venues_used=list(set(f.venue for f in all_fills)), status=OrderStatus.FILLED,
        )
# ---------------------------------------------------------------------------
# Iceberg order implementation
# ---------------------------------------------------------------------------
class IcebergExecutor:
    def __init__(self, order_mgr: OrderManager, router: SmartOrderRouter, feed: MarketDataFeed):
        self.om = order_mgr
        self.router = router
        self.feed = feed
    def execute(
        self,
        symbol: str,
        side: OrderSide,
        total_qty: float,
        display_qty: float,
        price: Optional[float] = None,
        refill_threshold: float = 0.3,
    ) -> ExecutionReport:
        order = self.om.create_order(
            side, symbol, total_qty,
            order_type=OrderType.ICEBERG,
            price=price,
            display_quantity=display_qty,
        )
        all_fills: list[Fill] = []
        remaining_visible = display_qty
        remaining_total = total_qty
        minute = 0
        while remaining_total > 0:
            visible_qty = min(remaining_visible, remaining_total)
            slice_order = self.om.create_order(side, symbol, visible_qty, venue="auto")
            book = self.feed.tick(minute)
            fills = self.router.route_order(slice_order, book)
            all_fills.extend(fills)
            self.om.record_fills(slice_order.order_id, fills)
            filled_now = sum(f.qty for f in fills)
            remaining_total -= filled_now
            remaining_visible -= filled_now
            if remaining_visible <= display_qty * refill_threshold and remaining_total > 0:
                remaining_visible = min(display_qty, remaining_total)
            minute += 1
            if minute > 500:
                break
        self.om.record_fills(order.order_id, all_fills)
        ref_price = self.feed.price
        report = self.om.generate_report(order.order_id, ref_price)
        return report if report else ExecutionReport(
            order_id=order.order_id, symbol=symbol, side=side,
            total_quantity=total_qty, filled_quantity=sum(f.qty for f in all_fills),
            avg_price=0, slippage_bps=0, duration_sec=0, n_fills=len(all_fills),
            venues_used=list(set(f.venue for f in all_fills)), status=OrderStatus.FILLED,
        )
# ---------------------------------------------------------------------------
# Execution quality analytics
# ---------------------------------------------------------------------------
class ExecutionQualityAnalyzer:
    def __init__(self):
        self.reports: list[ExecutionReport] = []
    def add_report(self, report: ExecutionReport):
        self.reports.append(report)
    def summary(self) -> dict:
        if not self.reports:
            return {"status": "no_data"}
        filled = [r for r in self.reports if r.status in (OrderStatus.FILLED, OrderStatus.PARTIAL)]
        if not filled:
            return {"status": "no_filled_orders"}
        slippages = [r.slippage_bps for r in filled]
        durations = [r.duration_sec for r in filled]
        fill_rates = [r.filled_quantity / r.total_quantity for r in filled]
        return {
            "n_orders": len(self.reports),
            "n_filled": len(filled),
            "avg_slippage_bps": round(statistics.mean(slippages), 2),
            "median_slippage_bps": round(statistics.median(slippages), 2),
            "std_slippage_bps": round(statistics.stdev(slippages), 2) if len(slippages) > 1 else 0,
            "max_slippage_bps": round(max(slippages), 2),
            "min_slippage_bps": round(min(slippages), 2),
            "avg_duration_sec": round(statistics.mean(durations), 1),
            "avg_fill_rate": round(statistics.mean(fill_rates), 4),
            "worst_case": max(filled, key=lambda r: r.slippage_bps, default=None),
            "best_case": min(filled, key=lambda r: r.slippage_bps, default=None),
        }
    def venue_breakdown(self) -> dict:
        venue_metrics: dict[str, list[float]] = {}
        for r in self.reports:
            for v in r.venues_used:
                venue_metrics.setdefault(v, []).append(r.slippage_bps)
        breakdown = {}
        for venue, slips in venue_metrics.items():
            breakdown[venue] = {
                "n_orders": len(slips),
                "avg_slippage_bps": round(statistics.mean(slips), 2),
                "median_slippage_bps": round(statistics.median(slips), 2),
            }
        return breakdown
# ---------------------------------------------------------------------------
# Demo / smoke test
# ---------------------------------------------------------------------------
def run_demo():
    print("=== Algo Execution Engine Demo ===\n")
    feed = MarketDataFeed("AAPL", base_price=150.0, volatility=0.001)
    router = SmartOrderRouter()
    router.add_venue(Venue("NYSE", latency_ms=3.0, fill_prob=0.90))
    router.add_venue(Venue("NASDAQ", latency_ms=5.0, fill_prob=0.85))
    router.add_venue(Venue("ARCA", latency_ms=7.0, fill_prob=0.80))
    om = OrderManager()
    analyzer = ExecutionQualityAnalyzer()
    twap = TWAPExecutor(om, router, feed)
    vwap = VWAPExecutor(om, router, feed)
    iceberg = IcebergExecutor(om, router, feed)
    # TWAP run
    print("[TWAP] Executing buy 10000 AAPL over 60 minutes...")
    twap_report = twap.execute("AAPL", OrderSide.BUY, 10000, 60, n_slices=12)
    analyzer.add_report(twap_report)
    print(f"  filled: {twap_report.filled_quantity:.0f}/{twap_report.total_quantity:.0f}")
    print(f"  avg price: ${twap_report.avg_price:.2f}")
    print(f"  slippage: {twap_report.slippage_bps:.2f} bps")
    print(f"  duration: {twap_report.duration_sec:.1f}s")
    print(f"  venues: {twap_report.venues_used}")
    print()
    # VWAP run
    print("[VWAP] Executing sell 20000 AAPL over full trading day...")
    vwap_report = vwap.execute("AAPL", OrderSide.SELL, 20000, 0, 390)
    analyzer.add_report(vwap_report)
    print(f"  filled: {vwap_report.filled_quantity:.0f}/{vwap_report.total_quantity:.0f}")
    print(f"  avg price: ${vwap_report.avg_price:.2f}")
    print(f"  slippage: {vwap_report.slippage_bps:.2f} bps")
    print(f"  duration: {vwap_report.duration_sec:.1f}s")
    print(f"  venues: {vwap_report.venues_used}")
    print()
    # Iceberg run
    print("[ICEBERG] Executing buy 50000 AAPL (display 5000 each)...")
    iceberg_report = iceberg.execute("AAPL", OrderSide.BUY, 50000, 5000, price=151.0)
    analyzer.add_report(iceberg_report)
    print(f"  filled: {iceberg_report.filled_quantity:.0f}/{iceberg_report.total_quantity:.0f}")
    print(f"  avg price: ${iceberg_report.avg_price:.2f}")
    print(f"  slippage: {iceberg_report.slippage_bps:.2f} bps")
    print(f"  duration: {iceberg_report.duration_sec:.1f}s")
    print(f"  venues: {iceberg_report.venues_used}")
    print()
    # Quality analysis
    print("=== Execution Quality Summary ===")
    summary = analyzer.summary()
    for k, v in summary.items():
        if isinstance(v, ExecutionReport):
            print(f"  {k}: {v.order_id} slippage={v.slippage_bps:.2f} bps")
        else:
            print(f"  {k}: {v}")
    print()
    print("=== Venue Breakdown ===")
    vb = analyzer.venue_breakdown()
    for venue, metrics in vb.items():
        print(f"  {venue}:")
        for mk, mv in metrics.items():
            print(f"    {mk}: {mv}")
if __name__ == "__main__":
    run_demo()
```
---
Design summary:
Component breakdown:
  TWAPExecutor slices total quantity into N equal pieces, spaced evenly over the duration. Each slice routes through SOR to the best-ranked venue. Guarantees time-uniform execution regardless of volume.
  VWAPExecutor uses the U-shaped volume profile to distribute quantity proportional to expected market volume at each minute. Tracks remaining quantity and adjusts last slices to match total.
  IcebergExecutor exposes only display_qty at a time. When visible shares drop below refill_threshold (30% of display), a new child slice is issued. Parent order stays a single logical order spanning many child slices.
  SmartOrderRouter ranks venues by a weighted composite score: 30% latency, 40% fill rate, 30% spread. Routes each slice to the best venue first, cascading to next if volume remains. Stats are updated with an EMA after each slice.
  ExecutionQualityAnalyzer computes slippage in basis points against a reference mid-price. Tracks avg/median/std/max/min across all executions. Venue breakdown shows which venues deliver the best fills.
  MarketDataFeed simulates a full trading day with U-shaped volume profile, Brownian motion price, and 10-level order book with realistic spread.
  Venue simulates realistic fills with configurable latency, fill probability, and spread. Fills walk the book levels.
import time

# TWAP
def compute_twap_slices(target_qty, n_slices, duration_seconds, start_time=None):
    if target_qty <= 0:
        raise ValueError('target_qty must be positive')
    n_slices = max(1, n_slices)
    if start_time is None:
        start_time = time.time()
    base = target_qty // n_slices
    remainder = target_qty % n_slices
    slices = []
    slice_duration = duration_seconds / n_slices
    for i in range(n_slices):
        qty = base + (1 if i < remainder else 0)
        slices.append({'slice_index': i, 'target_qty': qty})
    return slices

s = compute_twap_slices(100, 3, 60.0)
assert len(s) == 3
assert sum(x['target_qty'] for x in s) == 100
assert compute_twap_slices(50, 0, 30.0)[0]['target_qty'] == 50
print('TWAP OK')

# VWAP
def compute_vwap_weight(slice_index, n_slices, volume_profile=None):
    if volume_profile:
        if len(volume_profile) != n_slices:
            raise ValueError('volume_profile length must equal n_slices')
        total = sum(volume_profile)
        if total <= 0:
            raise ValueError('volume_profile must sum to a positive value')
        return volume_profile[slice_index] / total
    return 1.0 / max(1, n_slices)

assert round(compute_vwap_weight(0, 4, [0.4, 0.3, 0.2, 0.1]), 2) == 0.40
assert all(abs(compute_vwap_weight(i, 4) - 0.25) < 1e-9 for i in range(4))
print('VWAP OK')

# Iceberg
def create_iceberg_slices(total_qty, peak_size, min_visible=1):
    if total_qty <= 0 or peak_size <= 0:
        raise ValueError('total_qty and peak_size must be positive')
    if peak_size < min_visible:
        peak_size = min_visible
    peaks = []
    remaining = total_qty
    while remaining > 0:
        peak = min(peak_size, remaining)
        peaks.append(peak)
        remaining -= peak
    return peaks

assert create_iceberg_slices(100, 30) == [30, 30, 30, 10]
assert sum(create_iceberg_slices(100, 30)) == 100
assert create_iceberg_slices(5, 10) == [5]
print('ICEBERG OK')

# Smart Route
def score_venue(venue, current_qty):
    if not venue.get('available', False):
        return {'name': venue.get('name', 'unknown'), 'score': float('inf'), 'reason': 'unavailable'}
    avg_latency = sum(venue['latencies']) / max(1, len(venue['latencies']))
    latency_factor = min(avg_latency / 100.0, 1.0)
    spread_factor = min(venue['spread_bps'] / 10.0, 1.0)
    depth_penalty = 0.0 if venue['orderbook_depth'] >= current_qty else 10.0
    composite = (latency_factor * 0.3) + (spread_factor * 0.4) + depth_penalty
    return {'name': venue['name'], 'score': composite, 'latency_factor': latency_factor, 'spread_factor': spread_factor, 'depth_penalty': depth_penalty}

def smart_route_order(order_qty, venues, slice_count=1):
    available = [v for v in venues if v.get('available', False)]
    if not available:
        available = [{'name': 'fallback', 'latencies': [100], 'spread_bps': 10.0, 'orderbook_depth': 10000, 'available': True}]
    scores = []
    for v in available:
        per_venue_qty = order_qty // max(1, slice_count)
        scores.append(score_venue(v, per_venue_qty))
    scores.sort(key=lambda s: s['score'])
    total_score = sum(max(0, 1 / (s['score'] + 0.001)) for s in scores)
    routes = []
    for s in scores:
        weight = (1 / (s['score'] + 0.001)) / total_score if total_score > 0 else 1 / len(scores)
        qty = int(round(order_qty * weight))
        if qty > 0:
            routes.append({'venue': s['name'], 'qty': qty, 'score': s['score']})
    allocated = sum(r['qty'] for r in routes)
    if allocated < order_qty and routes:
        routes[-1]['qty'] += order_qty - allocated
    elif allocated > order_qty and routes:
        routes[-1]['qty'] -= allocated - order_qty
    return routes

venues = [
    {'name': 'NYSE', 'latencies': [5,7], 'spread_bps': 1.2, 'orderbook_depth': 5000, 'available': True},
    {'name': 'NASDAQ', 'latencies': [8,9], 'spread_bps': 1.5, 'orderbook_depth': 3000, 'available': True},
    {'name': 'CHI-X', 'latencies': [3,4], 'spread_bps': 0.8, 'orderbook_depth': 1000, 'available': False},
]
routes = smart_route_order(200, venues)
assert len(routes) == 2
assert sum(r['qty'] for r in routes) == 200
empty_routes = smart_route_order(500, [])
assert len(empty_routes) == 1
assert empty_routes[0]['venue'] == 'fallback'
assert empty_routes[0]['qty'] == 500
print('ROUTING OK')

# Execution Quality
def report_execution_quality(algorithm, symbol, slices, benchmark_price):
    total_qty = sum(s.get('target_qty', s.get('filled_qty', 0)) for s in slices)
    total_filled = sum(s['filled_qty'] for s in slices)
    total_notional = sum(s['filled_qty'] * s['avg_price'] for s in slices)
    vwap = total_notional / total_filled if total_filled > 0 else 0.0
    slippages = [s['slippage_bps'] for s in slices]
    avg_slippage_bps = sum(slippages) / len(slippages) if slippages else 0.0
    max_slippage_bps = max(slippages) if slippages else 0.0
    venues_set = set()
    for s in slices:
        if 'venue' in s:
            venues_set.add(s['venue'])
    if not venues_set:
        venues_set = {'default'}
    fill_rate = total_filled / total_qty if total_qty > 0 else 1.0
    return {
        'algorithm': algorithm, 'symbol': symbol,
        'total_qty': total_qty, 'total_filled': total_filled,
        'n_slices': len(slices), 'n_venues': len(venues_set),
        'vwap': round(vwap, 4), 'benchmark_price': benchmark_price,
        'avg_slippage_bps': round(avg_slippage_bps, 4),
        'max_slippage_bps': round(max_slippage_bps, 4),
        'fill_rate': round(fill_rate, 4), 'venue_breakdown': {},
    }

r = report_execution_quality('TWAP', 'AAPL', [
    {'filled_qty': 50, 'avg_price': 100.5, 'slippage_bps': 2.5},
    {'filled_qty': 50, 'avg_price': 99.8, 'slippage_bps': -1.3},
], 100.0)
assert r['total_filled'] == 100
assert r['avg_slippage_bps'] == 0.6, f"expected 0.6 got {r['avg_slippage_bps']}"
assert r['fill_rate'] == 1.0
print('QUALITY REPORT OK')

# Smoke test scenarios
venues_normal = [
    {'name': 'NYSE', 'latencies': [5,7,6], 'spread_bps': 1.2, 'orderbook_depth': 5000, 'available': True},
    {'name': 'NASDAQ', 'latencies': [8,9,7], 'spread_bps': 1.5, 'orderbook_depth': 3000, 'available': True},
]
slices_normal = compute_twap_slices(200, 4, 120.0)
assert len(slices_normal) == 4
assert sum(s['target_qty'] for s in slices_normal) == 200
routes_normal = smart_route_order(200, venues_normal)
assert sum(r['qty'] for r in routes_normal) == 200
assert all(r['venue'] in ('NYSE', 'NASDAQ') for r in routes_normal)
print('SCENARIO 1 (normal) OK')

empty_routes = smart_route_order(500, [])
assert len(empty_routes) == 1
assert empty_routes[0]['venue'] == 'fallback'
assert empty_routes[0]['qty'] == 500
print('SCENARIO 2 (empty venue) OK')

timeout_venues = [
    {'name': 'EXCHANGE_A', 'latencies': [999], 'spread_bps': 1.0, 'orderbook_depth': 100, 'available': False},
    {'name': 'EXCHANGE_B', 'latencies': [3,4,5], 'spread_bps': 0.8, 'orderbook_depth': 5000, 'available': True},
]
routes_timeout = smart_route_order(300, timeout_venues)
assert not any(r['venue'] == 'EXCHANGE_A' for r in routes_timeout)
assert sum(r['qty'] for r in routes_timeout) == 300
print('SCENARIO 3 (network timeout) OK')

print()
print('=== ALL VALIDATION PASSED ===')

```python
import time
import math
from typing import List, Dict, Optional, Any
OrderSide = str  
OrderStatus = str  
Venue = Dict[str, Any]
Order = Dict[str, Any]
Slice = Dict[str, Any]
ExecutionQualityReport = Dict[str, Any]
def computetwapslices(
    targetqty: int,
    nslices: int,
    durationseconds: float,
    starttime: Optional[float] = None,
) -> List[dict]:
    if targetqty <= 0:
        raise ValueError("targetqty must be positive")
    if nslices < 1:
        nslices = 1
    if starttime is None:
        starttime = time.time()
    baseqty = targetqty // nslices
    remainder = targetqty % nslices
    slicelen = durationseconds / nslices
    slices = []
    for i in range(nslices):
        qty = baseqty + (1 if i < remainder else 0)
        sstart = starttime + i * slicelen
        send = sstart + slicelen
        slices.append(
            {
                "sliceindex": i,
                "starttime": round(sstart, 4),
                "endtime": round(send, 4),
                "targetqty": qty,
            }
        )
    return slices
slices = computetwapslices(100, 3, 60.0)
assert len(slices) == 3
assert sum(s["targetqty"] for s in slices) == 100
def computevwapweight(
    sliceindex: int,
    nslices: int,
    volumeprofile: Optional[List[float]] = None,
) -> float:
    if volumeprofile:
        if len(volumeprofile) != nslices:
            raise ValueError("volumeprofile length must equal nslices")
        total = sum(volumeprofile)
        if total <= 0:
            raise ValueError("volumeprofile weights must sum to a positive value")
        return volumeprofile[sliceindex] / total
    return 1.0 / nslices
w = computevwapweight(0, 4, [0.4, 0.3, 0.2, 0.1])
assert round(w, 2) == 0.4
assert abs(sum(computevwapweight(i, 4) for i in range(4)) - 1.0) < 1e-9
def createicebergslices(totalqty: int, peaksize: int, minvisible: int = 1) -> List[int]:
    if totalqty <= 0:
        return []
    if peaksize < minvisible:
        peaksize = minvisible
    remaining = totalqty
    peaks = []
    while remaining > 0:
        peak = min(peaksize, remaining)
        peaks.append(peak)
        remaining -= peak
    return peaks
assert createicebergslices(100, 30) == [30, 30, 30, 10]
assert sum(createicebergslices(100, 30)) == 100
assert createicebergslices(5, 10) == [5]
def scorevenue(venue: dict, currentqty: int) -> dict:
    latencies = venue.get("latencies", [100])
    avglat = sum(latencies) / len(latencies)
    latencyfactor = avglat / 100.0
    spreadfactor = venue.get("spreadbps", 10.0) / 100.0
    depth = venue.get("orderbookdepth", 0)
    depthpenalty = 10.0 if currentqty > depth else 0.0
    composite = (latencyfactor * 0.3) + (spreadfactor * 0.4) + depthpenalty
    return {
        "name": venue["name"],
        "score": composite,
        "latencyfactor": latencyfactor,
        "spreadfactor": spreadfactor,
        "depthpenalty": depthpenalty,
    }
v1 = {
    "name": "NYSE",
    "latencies": [5, 7, 6],
    "spreadbps": 1.2,
    "orderbookdepth": 5000,
    "available": True,
}
s1 = scorevenue(v1, 100)
assert s1["name"] == "NYSE"
assert 0 <= s1["score"] <= 10
def smartrouteorder(
    orderqty: int,
    venues: List[dict],
    slicecount: int = 1,
) -> List[dict]:
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
        pervenueqty = orderqty // max(1, slicecount)
        scores.append(scorevenue(v, pervenueqty))
    scores.sort(key=lambda s: s["score"])
    totalscore = sum(max(0, 1 / (s["score"] + 0.001)) for s in scores)
    routes = []
    for s in scores:
        weight = (
            (1 / (s["score"] + 0.001)) / totalscore
            if totalscore > 0
            else 1 / len(scores)
        )
        qty = int(round(orderqty * weight))
        if qty > 0:
            routes.append({"venue": s["name"], "qty": qty, "score": s["score"]})
    allocated = sum(r["qty"] for r in routes)
    if allocated < orderqty and routes:
        routes[-1]["qty"] += orderqty - allocated
    elif allocated > orderqty and routes:
        routes[-1]["qty"] -= allocated - orderqty
    return routes
emptyroutes = smartrouteorder(500, [])
assert len(emptyroutes) == 1
assert emptyroutes[0]["venue"] == "fallback"
assert emptyroutes[0]["qty"] == 500
def reportexecutionquality(
    algorithm: str,
    symbol: str,
    slices: List[dict],
    benchmarkprice: float,
) -> dict:
    totalqty = sum(s.get("targetqty", s.get("filledqty", 0)) for s in slices)
    totalfilled = sum(s["filledqty"] for s in slices)
    totalnotional = sum(s["filledqty"] * s["avgprice"] for s in slices)
    vwap = totalnotional / totalfilled if totalfilled > 0 else 0.0
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
r = reportexecutionquality(
    "TWAP",
    "AAPL",
    [
        {"filledqty": 50, "avgprice": 100.5, "slippagebps": 2.5},
        {"filledqty": 50, "avgprice": 99.8, "slippagebps": -1.3},
    ],
    100.0,
)
assert r["totalfilled"] == 100
assert r["avgslippagebps"] == 0.6
assert r["fillrate"] == 1.0
# ---------------------------------------------------------------------------
# Runnable Smoke Test  Section (pytest)
# ---------------------------------------------------------------------------
def test_normal_execution():
    venues = [
        {
            "name": "NYSE",
            "latencies": [5, 7, 6],
            "spreadbps": 1.2,
            "orderbookdepth": 5000,
            "available": True,
        },
        {
            "name": "NASDAQ",
            "latencies": [8, 9, 7],
            "spreadbps": 1.5,
            "orderbookdepth": 3000,
            "available": True,
        },
    ]
    slices = computetwapslices(200, 4, 120.0)
    assert len(slices) == 4
    assert sum(s["targetqty"] for s in slices) == 200
    routes = smartrouteorder(200, venues)
    assert len(routes) >= 1
    assert sum(r["qty"] for r in routes) == 200
    assert all(r["venue"] in ("NYSE", "NASDAQ") for r in routes)
    report = reportexecutionquality(
        "TWAP",
        "TEST",
        [
            {"filledqty": 50, "avgprice": 100.0, "slippagebps": 1.0},
            {"filledqty": 50, "avgprice": 100.2, "slippagebps": 2.0},
        ],
        100.0,
    )
    assert report["fillrate"] == 1.0
    assert report["avgslippagebps"] == 1.5
def test_empty_venue():
    routes = smartrouteorder(500, [])
    assert len(routes) == 1
    assert routes[0]["venue"] == "fallback"
    assert routes[0]["qty"] == 500
def test_network_timeout():
    timeoutvenues = [
        {
            "name": "EXCHANGEA",
            "latencies": [999],
            "spreadbps": 1.0,
            "orderbookdepth": 100,
            "available": False,
        },
        {
            "name": "EXCHANGEB",
            "latencies": [3, 4, 5],
            "spreadbps": 0.8,
            "orderbookdepth": 5000,
            "available": True,
        },
    ]
    routes = smartrouteorder(300, timeoutvenues)
    assert not any(r["venue"] == "EXCHANGEA" for r in routes)
    assert sum(r["qty"] for r in routes) == 300
# ---------------------------------------------------------------------------
# Self-Verification  Step
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    #  1   Input targetqty=100, nslices=3 -> sum of slice targetqty == 100
    sv = computetwapslices(100, 3, 60.0)
    assert sum(s["targetqty"] for s in sv) == 100, "slice sum mismatch"
    print("PASS  1: slice sum == 100")
    #  2   Input targetqty=1, nslices=5 -> last slice gets all 1, sum == 1
    sv2 = computetwapslices(1, 5, 60.0)
    assert sum(s["targetqty"] for s in sv2) == 1, "single unit slice sum mismatch"
    print("PASS  2: single-unit slice sum == 1")
    #  3   Input targetqty=0 -> ValueError raised
    try:
        computetwapslices(0, 3, 60.0)
        assert False, "should have raised ValueError"
    except ValueError:
        print("PASS  3: ValueError on targetqty=0")
    #  4   All venues unavailable -> fallback venue created, fill continues
    routes4 = smartrouteorder(200, [])
    assert routes4[0]["venue"] == "fallback"
    assert routes4[0]["qty"] == 200
    print("PASS  4: fallback on empty venue list")
    #  5   avgslippage from [2.5, -1.3] = 0.6, not 2.5 (first-only) or 1.2
    r5 = reportexecutionquality(
        "TWAP",
        "TEST",
        [
            {"filledqty": 50, "avgprice": 100.5, "slippagebps": 2.5},
            {"filledqty": 50, "avgprice": 99.8, "slippagebps": -1.3},
        ],
        100.0,
    )
    expected = (2.5 + (-1.3)) / 2.0
    assert r5["avgslippagebps"] == expected, (
        f"avgslippagebps={r5['avgslippagebps']} != {expected}"
    )
    print("PASS  5: avgslippagebps computed as mean of all slices")
    print("All self-verification checks passed.")
```
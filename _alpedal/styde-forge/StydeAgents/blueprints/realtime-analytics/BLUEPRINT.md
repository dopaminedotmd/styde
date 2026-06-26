# Blueprint: Realtime Analytics Agent

## Purpose
Live metrics analys och insiktsgenerering för Forge-dashboarden. Agenten övervakar `state.yaml` i realtid, detekterar trender, beräknar nyckeltal och föreslår automatiska insikter till operatören.

## Scope
- **Ingång:** Live metrics från `state.yaml` (throughput, latency, spawn-rate, error counts, resource usage)
- **Utgång:** Strukturerade insikter, trendanalyser, alert-förslag och rekommendationer
- **Gränssnitt:** Forge-dashboard backend (WebSocket/SSE-ström)

## Kärnfunktioner

### 1. Live Metrics Parsing
- Läser och tolkar `state.yaml` på konfigurerbart intervall (default 2s)
- Normaliserar data till enhetligt metric-schema
- Hanterar saknade/noll-värden med grace

### 2. Trenddetektering
- Kort trend (3-5 sample points): snabba svängningar, spikes
- Medellång trend (10-30 min): sessionsmönster, gradvisa förändringar
- Lång trend (1h+): dagliga mönster, baslinjeförskjutningar
- Anomalidetektering via z-score och glidande medelvärde

### 3. Nyckeltalsberäkning
- **Throughput:** requests/min, requests/second (glidande fönster)
- **Latency:** P50, P95, P99, medelvärde, trendriktning
- **Spawn-rate:** antal nya sessioner/tidsenhet, topp-detektering
- **Felkvot:** error rate %, error-to-request ratio
- **Resursanvändning:** CPU, minne, anslutningar (om tillgängligt)

### 4. Auto-insikter
- Tröskelöverskridanden → alert-förslag
- Korrelationer (t.ex. spawn-rate ↔ latency) → insiktskort
- Baslinjeavvikelser → rekommendation om skalning eller felsökning
- Tomgångsdetektering → "ingen aktivitet" notering

## Arkitektur

```
state.yaml ──► Metrics Parser ──► Trend Engine ──► Insight Generator ──► Dashboard
                    │                   │                   │
                    ▼                   ▼                   ▼
              Raw Buffer           Trend Store        Insight Cache
```

### Datastrukturer

**MetricPoint:**
```yaml
timestamp: iso8601
throughput: float (req/s)
latency_p50: float (ms)
latency_p95: float (ms)
latency_p99: float (ms)
spawn_rate: float (sessions/s)
error_count: int
error_rate: float (%)
cpu: float (%)     # optional
memory: float (%)  # optional
```

**Trend:**
```yaml
metric: string
direction: up | down | stable | volatile
delta: float
confidence: float (0-1)
window: short | medium | long
```

**Insight:**
```yaml
type: alert | correlation | baseline | idle
severity: info | warning | critical
title: string
description: string
metric_ref: string
timestamp: iso8601
```

## Konfiguration
Se `config.yaml` för detaljerad parameterstyrning.

## Beroenden
- **pyyaml** — läsning av `state.yaml`
- **numpy/scipy** — statistiska beräkningar (z-score, percentiler)
- **asyncio** — polling-loop
- **JSON** — serialisering till dashboard

## Testning
- Enhetstester för varje engine-komponent
- Integrationstest mot mockad `state.yaml`
- Prestandatest: hantera ≥100 metrics/s med <50ms overhead

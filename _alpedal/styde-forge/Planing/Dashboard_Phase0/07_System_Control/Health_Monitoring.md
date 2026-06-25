# Health Monitoring

**StydeForge Dashboard — Mission Control**
**Phase 0 Design Document**

---

## 1. Overview

The Dashboard monitors system health — CPU, GPU, RAM, disk — and warns when resources approach critical thresholds. Data displays compactly in the status bar and expands on demand.

---

## 2. Compact View (status bar)

```
┌──────────────────────────────────────────────────────────────────┐
│ ● Running | 3 agents | 12.4K tokens | $0.037 | CPU 34% | GPU 72% │
└──────────────────────────────────────────────────────────────────┘
```

---

## 3. Expanded Health Panel

```
┌──────────────────────────────────────────────────┐
│ 💚 SYSTEM HEALTH                                 │
├──────────────────────────────────────────────────┤
│                                                  │
│  CPU                                              │
│  ┌────────────────────────────────────────────┐  │
│  │ Intel Core i7-13700K    34%  ████░░░░░░   │  │
│  │ Temp: 58°C · P-cores: 42% · E-cores: 12%  │  │
│  │ Power: 65W / 125W TDP                      │  │
│  └────────────────────────────────────────────┘  │
│                                                  │
│  GPU 0 — RTX 3080 (10GB)                         │
│  ┌────────────────────────────────────────────┐  │
│  │ GPU Usage:  72%  ███████░░░                │  │
│  │ VRAM:       6.2GB / 10GB  ██████░░░░       │  │
│  │ Temp:       71°C          ███████░░░       │  │
│  │ Power:      280W / 350W   ████████░░       │  │
│  │ Fan:        62%                             │  │
│  └────────────────────────────────────────────┘  │
│                                                  │
│  GPU 1 — RTX 3070 Ti (8GB)                       │
│  ┌────────────────────────────────────────────┐  │
│  │ GPU Usage:   8%  █░░░░░░░░░                │  │
│  │ VRAM:       1.2GB / 8GB  █░░░░░░░░░        │  │
│  │ Temp:       48°C          █████░░░░░       │  │
│  │ Power:      45W / 290W    ██░░░░░░░░       │  │
│  │ Fan:        30%                             │  │
│  └────────────────────────────────────────────┘  │
│                                                  │
│  RAM                                              │
│  ┌────────────────────────────────────────────┐  │
│  │ 18.2GB / 32GB  ██████░░░░  (57%)           │  │
│  │ Hermes: 2.4GB · Dashboard: 142MB           │  │
│  └────────────────────────────────────────────┘  │
│                                                  │
│  Disk                                             │
│  ┌────────────────────────────────────────────┐  │
│  │ C: 342GB / 1TB  ███░░░░░░░  (34%)          │  │
│  │ D: 1.2TB / 2TB  ██████░░░░  (60%)          │  │
│  └────────────────────────────────────────────┘  │
│                                                  │
│  Uptime: 3h 42m                                  │
│                                                  │
└──────────────────────────────────────────────────┘
```

---

## 4. Warning Thresholds

| Resource | Green (<) | Yellow | Red (>) | Critical (>) |
|----------|-----------|--------|---------|--------------|
| CPU | 60% | 60-80% | 80-95% | 95% |
| GPU Usage | 70% | 70-85% | 85-95% | 95% |
| VRAM | 70% | 70-85% | 85-95% | 95% |
| GPU Temp | 70°C | 70-80°C | 80-90°C | 90°C |
| RAM | 70% | 70-85% | 85-95% | 95% |
| Disk | 80% | 80-90% | 90-95% | 95% |

---

## 5. Notifications

| Event | Notification |
|-------|--------------|
| VRAM > 85% | "⚠ GPU memory nearly full (8.5/10GB). Agents may slow down." |
| GPU Temp > 80°C | "⚠ GPU temperature high (83°C). Consider pausing Forge." |
| RAM > 90% | "⚠ System memory critical (29/32GB). Close other programs." |
| Disk < 10GB | "⚠ Low disk space (8GB remaining). Clean logs?" |
| CPU > 95% for 60s | "⚠ CPU overloaded. Reduce concurrent agents." |

---

## 6. Data Collection

The Dashboard uses Tauri's Rust backend to collect system data:

| Metric | Source | Refresh |
|--------|--------|---------|
| CPU usage | `sysinfo` crate (Rust) | Every 5s |
| CPU temp | `sysinfo` / WMI | Every 30s |
| GPU usage | `nvml` (NVIDIA Management Library) | Every 5s |
| VRAM | `nvml` | Every 5s |
| GPU temp | `nvml` | Every 5s |
| RAM | `sysinfo` | Every 10s |
| Disk | `sysinfo` | Every 60s |

---

## 7. History

System health is logged for trend analysis:

```
CPU:  ████░░████████████████████  (24h avg: 42%)
GPU0: ██████████████████████████  (24h avg: 68%)
RAM:  ██████████████████████████  (24h avg: 55%)
```

---

**Status:** Phase 0 — Design

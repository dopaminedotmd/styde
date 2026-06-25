# Risk Register

**Styde Forge v3.0 — Phase 0**
**Section:** 06_Persistence_Safety

---

## 1. Identified Risks

| ID | Risk | Probability | Impact | Mitigation |
|----|------|-------------|--------|------------|
| R01 | USB corruption | Medium | High | Atomic Transactions + Checkpoints |
| R02 | Divergent learning | Medium | High | 80/100 eval gate + ≥85×3 production gate + Bayesian Opt |
| R03 | VRAM exhaustion (Machine-B) | High | Medium | Hardware Adapter + Resource Governor |
| R04 | Version conflicts on import | Low | Medium | Auto Version Increment |
| R05 | Eval bias over time | Medium | High | Bias Calibration + Cross-Consensus |
| R06 | Lost state on machine move | Medium | High | Auto Recovery + Checkpoints |
| R07 | Performance degradation | Medium | Medium | Self-Monitoring + Maintenance |
| R08 | USB out of space | Medium | Medium | Maintenance Strategy + pruning |
| R09 | Prompt injection | Low | High | Agent isolation + no shared state |
| R10 | API provider changes (pricing, deprecation, outage) | High | High | Multi-provider support, local Ollama fallback, cost tracking alerts |
| R11 | Python dependency bitrot (incompatible versions) | Medium | Medium | Pinned versions in requirements.txt, periodic compatibility testing |

---

## 2. Risk Score

```python
risk_score = (
    error_rate * 0.25 +
    -improvement_trend * 0.20 +
    vram_pressure * 0.20 +
    disk_usage * 0.15 +
    checkpoint_age * 0.10 +
    crash_count * 0.10
) * 100
```

---

## 3. Acceptance Criteria

Phase 0 approved when:
- All risks have explicit mitigations
- Stable on both Machine-A and Machine-B
- Import works with one prompt
- Full traceability from agent to decision

---

**Status:** All risks identified with active mitigations.

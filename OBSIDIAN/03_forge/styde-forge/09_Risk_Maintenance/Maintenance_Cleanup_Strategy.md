# Maintenance & Cleanup Strategy

**Styde Forge v3.0 — Phase 0**
**Section:** 09_Risk_Maintenance

---

## 1. Purpose

Keep the USB under 48 GB long-term through intelligent pruning, archiving,
and compression — without losing valuable data. Runs automatically on a
cycle-based schedule.

---

## 2. Automatic Maintenance Schedule

| Every | Action | Rationale |
|-------|--------|-----------|
| 10 cycles | Full cleanup (remove patches < 85/100) | Prevent accumulation of minor versions |
| 30 cycles | Archive old generations to `07_GENERATIONS/archive/` | Keep generation dir manageable |
| 50 cycles | Compress logs and Bayesian samples | Reduce storage, keep data accessible |
| 100 cycles | Deep cleanup (defragment indexes, rebuild lineage) | Maintain query performance |

---

## 3. Retention Rules

### Keep Always
- Top 3 agents per domain (by eval score)
- Complete lineage for top 50 agents
- All checkpoints from last 7 days
- All eval results (compressed after 30 days)
- Current teacher logs (last 40 cycles)

### Remove
- Agents with score < 80 after 3 failed generations
- Patch versions > 20 cycles old with no unique improvements
- Teacher logs > 40 cycles (compress, don't delete)
- Checkpoints > 30 days old

### Compress
- Bayesian samples > 10 cycles old
- Log files > 7 days old
- Old benchmark task output (keep results, compress output)
- Generation archives (gzip)

---

## 4. Storage Budget (48 GB)

| Category | Budget | Current (estimate) |
|----------|--------|--------------------|
| Agents (250-350 elite) | 25 GB | 0 GB (Phase 0) |
| Knowledge (8-10 domains) | 8 GB | 0 GB |
| Skills & Hooks | 5 GB | 0 GB |
| Eval Results & Lineage | 4 GB | 0 GB |
| Checkpoints | 3 GB | 0 GB |
| Logs & Teacher Data | 2 GB | 0 GB |
| Overhead & Indexes | 1 GB | < 1 MB |
| **Total** | **48 GB** | **< 1 MB** |

---

## 5. Manual Maintenance Commands

```
# Run full maintenance cycle now
python scripts/forge.py maintenance run

# Show storage breakdown
python scripts/forge.py maintenance status

# Archive generations older than 30 cycles
python scripts/forge.py maintenance archive --older-than 30

# Force compression of all logs
python scripts/forge.py maintenance compress --all

# Dry run (show what would be removed)
python scripts/forge.py maintenance run --dry-run
```

---

## 6. Storage Monitoring

```python
def storage_breakdown() -> dict:
    return {
        "agents_gb": get_dir_size_gb("02_AGENTS/"),
        "knowledge_gb": get_dir_size_gb("01_KNOWLEDGE/"),
        "skills_gb": get_dir_size_gb("04_SKILLS/"),
        "eval_gb": get_dir_size_gb("07_GENERATIONS/"),
        "checkpoints_gb": get_dir_size_gb("09_CHECKPOINTS/"),
        "teacher_logs_gb": get_dir_size_gb("08_TEACHER_LOGS/"),
        "logs_gb": get_dir_size_gb("logs/"),
        "total_used_gb": ...,
        "total_capacity_gb": 48.0,
        "percent_used": ...,
        "status": "ok" | "warning" | "critical"
    }
```

### Alert Thresholds

| Usage | Status | Action |
|-------|--------|--------|
| < 80% | OK | Normal operation |
| 80-90% | Warning | Schedule maintenance |
| 90-95% | Critical | Immediate maintenance + alert |
| > 95% | Emergency | Pause loops, force cleanup |

---

## 7. Integration

- Automatic maintenance runs every 10 cycles
- Storage budget enforced by Resource Governor
- Self-Monitoring tracks storage trends
- Alerts via Hooks & Events system
- Maintenance events logged for audit

---

**Status:** Defined. Automatic maintenance every 10 cycles.

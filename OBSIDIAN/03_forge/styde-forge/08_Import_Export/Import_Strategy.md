# Import Strategy

**Styde Forge v3.0 — Phase 0**
**Section:** 08_Import_Export

---

## 1. Purpose

Import the entire Styde Forge on any machine with a single prompt.
All state preserved, hardware auto-detected, loop ready to resume.
Zero manual configuration required.

---

## 2. Single-Prompt Import

```
Läs in och importera Styde Forge från E:\HermesForge\.
Följ instruktionerna i v3.0_Phase0/00_Overview/PHASE0_INDEX.md.
```

---

## 3. Automatic Import Actions

When Hermes receives the import prompt, it executes:

```
1. Read FORGE.md and state.yaml → detect forge version
2. Run hardware/detect.py → get current machine profile
3. Match against hardware/profiles.yaml
4. Set hardware_profile in state.yaml
5. Adapt: sampling method, models, tree depth, concurrency
6. Verify latest checkpoint integrity
7. If valid: resume from checkpoint
8. If invalid: run automatic recovery
9. Log import event
10. Display status and ready prompt
```

---

## 4. Cross-Machine Adaptation

| Parameter | Machine-A → Machine-B | Machine-B → Machine-A |
|-----------|----------------------|----------------------|
| Sampling | NUTS → VI | VI → NUTS |
| Tree depth | 11 → 8 | 8 → 11 |
| Bayesian samples | 2800 → 1400 | 1400 → 2800 |
| Parallel workers | 3 → 1 | 1 → 3 |
| Preferred models | 70B+ → 7-14B | 7-14B → 70B+ |
| Checkpoint interval | 45 min → 25 min | 25 min → 45 min |

---

## 5. Import Validation

After import, verify system health:

```bash
# Expected: correct hardware detected
python scripts/forge.py hw detect

# Expected: v3.0.0, correct profile, blueprints listed
python scripts/forge.py status

# Expected: all blueprints from original
python scripts/forge.py blueprint list

# Expected: agent history preserved
python scripts/forge.py agent list
```

---

## 6. Edge Cases

| Scenario | Handling |
|----------|----------|
| USB from Machine-A inserted into Machine-B | Auto-detect B, adapt all params |
| USB with corrupted state.yaml | Recovery from last checkpoint |
| No checkpoints exist | Fresh start (state preserved from import) |
| Different forge version | Version check: migrate if older, warn if newer |
| Missing hardware profile | Run detection, create new profile |
| API keys not configured | Warn which keys are missing, continue with available providers |

---

## 7. Import Log

```json
{
  "timestamp": "2026-06-25T15:00:00Z",
  "event": "import",
  "source_machine": "pontus-beast",
  "target_machine": "pontus-main",
  "adaptations_applied": {
    "sampling": "NUTS → VI",
    "tree_depth": "11 → 8",
    "models": "70B → 14B"
  },
  "checkpoint_restored": "checkpoint-20260625-144500",
  "status": "success"
}
```

---

## 8. Integration

- One prompt. Fully automatic. No manual config.
- Works with physical USB move or zip export/import
- Sync Strategy handles conflict resolution
- Recovery handles any corruption during transfer

---

**Status:** Defined. One prompt, fully automatic, cross-machine adaptive.

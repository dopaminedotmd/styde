# Sync Strategy

**Styde Forge v3.0 — Phase 0**
**Section:** 08_Import_Export

---

## 1. Purpose

Define how the forge stays consistent when moved between machines.
USB is the canonical storage — there is no "cloud sync". The strategy
handles state conflicts, partial transfers, and resume-after-move.

---

## 2. Canonical Storage Model

```
USB (always the source of truth)
  │
  ├── Machine-A: reads/writes directly to USB
  │
  └── Machine-B: reads/writes directly to USB
```

**Rule:** The USB IS the database. No cloud. No network sync.
Physically move the USB between machines.

---

## 3. Move Procedure

### Machine-A → Machine-B

```
1. On Machine-A: python scripts/forge.py checkpoint
2. Eject USB from Machine-A
3. Insert USB into Machine-B
4. On Machine-B: python scripts/forge.py hw detect
5. System auto-adapts: NUTS→VI, depth 11→8, models adjusted
6. Resume from last checkpoint
```

### What Changes Automatically

| Parameter | Machine-A | Machine-B |
|-----------|-----------|-----------|
| Sampling | NUTS | VI |
| Tree depth | 11 | 8 |
| Bayesian samples | 2800 | 1400 |
| Parallel workers | 3 | 1 |
| Preferred models | 70B-405B | 7B-14B |

---

## 4. Conflict Resolution

Since the forge is single-user and single-process, conflicts are rare.
But they can happen:

| Scenario | Resolution |
|----------|-----------|
| Two machines write to USB (shouldn't happen) | Last checkpoint wins. State is single-writer by design. |
| USB removed mid-write | Atomic writes prevent corruption. Next startup: auto-recovery from last checkpoint. |
| State.yaml modified externally | Checksum validation on load. Invalid → restore from checkpoint. |
| Different forge versions | state.yaml `forge_version` checked. Older versions: migrate. Newer: warn. |

---

## 5. Resume After Move

```python
def resume_after_move():
    """
    Called at forge startup. Detects if we moved machines.
    """
    # Load state
    state = load_state()

    # Detect current hardware
    hw = detect_hardware()
    current_profile = hw["profile"]

    # Check if profile changed
    if state["hardware_profile"] != current_profile:
        log(f"Machine changed: {state['hardware_profile']} → {current_profile}")
        state["hardware_profile"] = current_profile

        # Adapt
        adaptations = get_adaptations(current_profile)
        log(f"Adapted: {adaptations['sampling_method']}, "
            f"depth={adaptations['max_tree_depth']}")

    # Verify checkpoint integrity
    last_cp = state.get("last_checkpoint")
    if last_cp and not verify_checkpoint(last_cp):
        log("WARNING: Last checkpoint invalid. Running recovery.")
        recover()

    # Ready
    log(f"Forge resumed. Profile: {current_profile}. "
        f"Iterations: {state['loop_iterations']}.")
```

---

## 6. Export/Import (Alternative to Physical Move)

When physical USB move isn't practical:

### Export
```bash
python scripts/forge.py export
# → exports/hermes-forge-20260625.zip
```

### Transfer
- Copy .zip via network, external drive, or cloud storage
- .zip is ~30-50 MB (compressed design docs + state, no logs/checkpoints)

### Import
```bash
python scripts/forge.py import hermes-forge-20260625.zip
python scripts/forge.py hw detect
# → System auto-adapts to new machine
```

---

## 7. Data Integrity

| Check | Method | When |
|-------|--------|------|
| state.yaml checksum | SHA256 | On load |
| Checkpoint integrity | File count + size + hash | On create + restore |
| Blueprint consistency | validate_blueprint() | On spawn |
| USB filesystem | Basic writability test | On startup |

---

**Status:** Defined. USB-as-database, auto-adapt on move, conflict resolution.

# State Machines

**Styde Forge v3.0 — Phase 0**
**Section:** 00_Overview

---

## 1. Purpose

Define all state machines in the forge — what states exist, what transitions
are allowed, and what triggers each transition.

---

## 2. Blueprint State Machine

```
                  ┌─────────┐
                  │  draft  │
                  └────┬────┘
                       │ first spawn + eval passed
                       ▼
                  ┌─────────┐
          ┌───────│ testing │───────┐
          │       └────┬────┘       │
          │ eval < 70  │  eval ≥ 80 │
          │ (3 fails)  │  (stable)  │
          ▼            ▼            │
     ┌─────────┐ ┌─────────┐       │
     │ rejected│ │ stable  │       │
     └─────────┘ └────┬────┘       │
                      │ no usage   │
                      │ 30 days    │
                      ▼            │
                 ┌──────────┐     │
                 │ deprecated│◄────┘
                 └──────────┘
```

| State | Description |
|-------|-------------|
| **draft** | Initial state. Blueprint defined but never spawned. |
| **testing** | Actively being evaluated. Loop iterations ongoing. |
| **stable** | Proven reliable. Consistently scores ≥ 80. |
| **deprecated** | No longer used. Kept for historical reference. |
| **rejected** | Failed eval 3+ times. Lessons extracted, blueprint archived. |

### Transitions

| From | To | Trigger |
|------|----|---------|
| draft | testing | First agent spawn + eval completed |
| testing | stable | ≥ 5 consecutive evals ≥ 80 |
| testing | rejected | 3 consecutive evals < 70 |
| testing | draft | Manual reset (redefine blueprint) |
| stable | deprecated | No spawns for 30 days |
| stable | testing | New major version (re-evaluation) |

---

## 3. Agent State Machine

```
                  ┌──────────────┐
                  │ pending_spawn│
                  └──────┬───────┘
                         │ delegate_task called
                         ▼
                  ┌─────────┐
                  │ running │
                  └────┬────┘
                       │
            ┌──────────┼──────────┐
            │          │          │
            ▼          ▼          ▼
       ┌─────────┐ ┌────────┐ ┌────────┐
       │completed│ │ failed │ │timeout │
       └────┬────┘ └───┬────┘ └───┬────┘
            │          │          │
            ▼          ▼          ▼
       ┌─────────────────────────────┐
       │        eval_pending         │
       └─────────────┬───────────────┘
                     │
          ┌──────────┼──────────┐
          │          │          │
          ▼          ▼          ▼
     ┌────────┐ ┌────────┐ ┌────────┐
     │ passed │ │retrying│ │rejected│
     └────┬───┘ └───┬────┘ └────────┘
          │         │
          ▼         │ (max 3 retries)
     ┌────────┐    │
     │ saved  │◄───┘
     └────────┘
```

| State | Description |
|-------|-------------|
| **pending_spawn** | Agent record created, not yet spawned |
| **running** | delegate_task executing |
| **completed** | Agent finished successfully |
| **failed** | Agent returned error |
| **timeout** | Agent exceeded time limit |
| **eval_pending** | Output ready, awaiting evaluation |
| **passed** | Composite score ≥ 80 |
| **retrying** | Score 70-79, re-spawning with improvements |
| **rejected** | Score < 70 or 3 retries exhausted |
| **saved** | Agent written to USB |

---

## 4. Loop State Machine

```
                  ┌─────────┐
                  │  idle   │
                  └────┬────┘
                       │ loop triggered
                       ▼
                  ┌─────────┐
                  │ define  │
                  └────┬────┘
                       │
                       ▼
                  ┌─────────┐
                  │ spawn   │
                  └────┬────┘
                       │
                       ▼
                  ┌─────────┐
                  │evaluate │
                  └────┬────┘
                       │
            ┌──────────┼──────────┐
            ▼          ▼          ▼
       ┌────────┐ ┌────────┐ ┌────────┐
       │improve │ │ retry  │ │ reject │
       └───┬────┘ └───┬────┘ └───┬────┘
           │          │          │
           ▼          │          ▼
      ┌─────────┐    │     ┌─────────┐
      │checkpoint│◄──┘     │  idle   │
      └────┬─────┘         └─────────┘
           │
           ▼
      ┌─────────┐
      │  idle   │ (next iteration or stop)
      └─────────┘
```

---

## 5. Checkpoint State Machine

```
                  ┌──────────┐
                  │  locked  │ ◄── acquire_lock()
                  └────┬─────┘
                       │ copy to staging
                       ▼
                  ┌──────────┐
                  │ staging  │
                  └────┬─────┘
                       │ verify integrity
                       ▼
                  ┌──────────┐
                  │verified  │
                  └────┬─────┘
                       │ atomic rename
                       ▼
                  ┌──────────┐
                  │  saved   │
                  └────┬─────┘
                       │ unlock
                       ▼
                  ┌──────────┐
                  │ unlocked │
                  └──────────┘
```

---

## 6. Recovery State Machine

```
                  ┌──────────┐
                  │  normal  │
                  └────┬─────┘
                       │ crash detected
                       ▼
                  ┌──────────┐
                  │detecting │
                  └────┬─────┘
                       │
            ┌──────────┼──────────┐
            ▼          │          ▼
       ┌────────┐     │     ┌──────────┐
       │no crash│     │     │crash     │
       │resume  │     │     │recovering│
       └────────┘     │     └────┬─────┘
                      │          │
                      │          ▼
                      │     ┌──────────┐
                      │     │restoring │
                      │     └────┬─────┘
                      │          │
                      │          ▼
                      │     ┌──────────┐
                      │     │replaying │
                      │     └────┬─────┘
                      │          │
                      │          ▼
                      │     ┌──────────┐
                      │     │verifying │
                      │     └────┬─────┘
                      │          │
                      │          ▼
                      │     ┌──────────┐
                      └─────│ resumed │
                            └──────────┘
```

---

**Status:** Defined. 6 state machines with all states and transitions.

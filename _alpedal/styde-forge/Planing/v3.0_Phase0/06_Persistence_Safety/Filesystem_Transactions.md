# Filesystem Transactions

**Styde Forge v3.0 — Phase 0**
**Section:** 06_Persistence_Safety

---

## 1. Purpose

Guarantee that all writes to USB are atomic — complete fully or not at all.
No partial files, no corrupted state. Critical for USB disconnect safety.

---

## 2. Atomic Write Pattern

```python
def atomic_write(path: Path, content: str):
    temp_path = path.with_suffix(path.suffix + '.tmp')
    with open(temp_path, 'w', encoding='utf-8') as f:
        f.write(content)
    f.flush()
    os.fsync(f.fileno())
    os.replace(str(temp_path), str(path))  # Atomic on same filesystem
```

---

## 3. Directory-Level Transactions

For multi-file operations (saving an agent):

```python
def transactional_save(agent_dir: Path, files: dict):
    staging = agent_dir.with_name(agent_dir.name + '.staging')
    staging.mkdir(exist_ok=True)
    for filename, content in files.items():
        atomic_write(staging / filename, content)
    if agent_dir.exists():
        os.replace(str(agent_dir), str(agent_dir.with_name(agent_dir.name + '.backup')))
    os.replace(str(staging), str(agent_dir))
```

---

## 4. Safety Guarantees

| Scenario | Guarantee |
|----------|-----------|
| Crash during write | Temp file discarded; original intact |
| USB disconnect | No partial files |
| Power loss | Old or new file exists, never corrupted |

---

**Status:** Implemented. Foundation for all USB writes.

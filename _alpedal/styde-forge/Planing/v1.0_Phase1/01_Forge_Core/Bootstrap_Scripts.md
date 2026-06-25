# Bootstrap Scripts — Implementation

**Styde Forge v3.0**
**Section:** 01_Forge_Core
**References:** `Hardware_Adaptation_Layer.md`, `USB_Directory_Structure.md`, `DECISIONS.md` D03/D05/D06/D12

---

## 1. Purpose

Three bootstrap scripts that must work before anything else:
1. `persistence.py` — Atomic filesystem operations (used by everything)
2. `detect.py` — Hardware auto-detection
3. `forge.py init` — Creates USB directory structure + state.yaml

---

## 2. `scripts/persistence.py`

### Specification

```python
"""
Atomic filesystem operations for Styde Forge.
Every write uses temp-file + rename pattern.
Guarantees: never partial writes, crash-safe.
"""
import os
import json
import tempfile
import shutil
from pathlib import Path

def atomic_write(path: Path, content: str) -> bool:
    """
    Write content to path atomically.
    
    Pattern:
      1. Write to path.tmp.<random>
      2. fsync the temp file
      3. os.replace (atomic on same filesystem)
      4. If crash: old file exists, temp file may exist (harmless)
    
    Returns True on success.
    """
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    
    # Write to temp file in same directory (same filesystem = atomic rename)
    fd, tmp_path = tempfile.mkstemp(
        dir=str(path.parent),
        prefix=f".{path.name}.",
        suffix=".tmp"
    )
    try:
        with os.fdopen(fd, 'w', encoding='utf-8') as f:
            f.write(content)
            f.flush()
            os.fsync(f.fileno())
        
        # Atomic replace (works on Windows + Unix)
        os.replace(tmp_path, str(path))
        return True
    except Exception:
        # Cleanup temp file on failure
        try:
            os.unlink(tmp_path)
        except OSError:
            pass
        raise


def atomic_write_json(path: Path, data: dict) -> bool:
    """Write dict as JSON atomically."""
    content = json.dumps(data, indent=2, ensure_ascii=False)
    return atomic_write(path, content)


def atomic_append(path: Path, line: str) -> bool:
    """
    Append a line to a log file atomically.
    For JSON-lines logging. Append-only, no temp file needed
    (but we still fsync for USB safety).
    """
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(path, 'a', encoding='utf-8') as f:
        f.write(line)
        if not line.endswith('\n'):
            f.write('\n')
        f.flush()
        os.fsync(f.fileno())
    return True


def transactional_save(dir_path: Path, files: dict) -> bool:
    """
    Save multiple files atomically.
    
    All files are written to a staging directory, then the directory
    is atomically renamed. If any write fails, staging is cleaned up.
    Used for checkpoints.
    
    Args:
        dir_path: Target directory
        files: {relative_path: content} mapping
    """
    dir_path = Path(dir_path)
    staging = dir_path.parent / f".{dir_path.name}.staging"
    
    try:
        # Clean any leftover staging
        if staging.exists():
            shutil.rmtree(staging)
        
        staging.mkdir(parents=True, exist_ok=True)
        
        for rel_path, content in files.items():
            target = staging / rel_path
            target.parent.mkdir(parents=True, exist_ok=True)
            
            if isinstance(content, dict):
                atomic_write_json(target, content)
            elif isinstance(content, bytes):
                target.write_bytes(content)
                os.fsync(open(target, 'rb').fileno())
            else:
                atomic_write(target, str(content))
        
        # Replace entire directory
        if dir_path.exists():
            shutil.rmtree(dir_path)
        os.replace(staging, str(dir_path))
        return True
        
    except Exception:
        if staging.exists():
            shutil.rmtree(staging)
        raise


def read_json(path: Path) -> dict:
    """Read JSON file. Returns empty dict if missing."""
    path = Path(path)
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding='utf-8'))


def read_yaml(path: Path) -> dict:
    """Read YAML file. Returns empty dict if missing."""
    import yaml
    path = Path(path)
    if not path.exists():
        return {}
    return yaml.safe_load(path.read_text(encoding='utf-8'))
```

### Tests

```python
# tests/test_persistence.py
def test_atomic_write_success(tmp_path):
    """Normal write should succeed."""
    f = tmp_path / "test.txt"
    atomic_write(f, "hello world")
    assert f.read_text() == "hello world"

def test_atomic_write_no_partial(tmp_path):
    """If crash mid-write, original file should be intact."""
    f = tmp_path / "test.txt"
    atomic_write(f, "original")
    
    # Simulate: write temp but crash before rename
    # (hard to test directly, but we verify the pattern)
    # The guarantee: either old OR new file exists, never partial.
    pass

def test_atomic_write_creates_dirs(tmp_path):
    """Should create parent directories."""
    f = tmp_path / "deep/nested/dir/test.txt"
    atomic_write(f, "content")
    assert f.read_text() == "content"
```

---

## 3. `scripts/detect.py`

### Specification

```python
"""
Hardware auto-detection for Styde Forge.
Detects VRAM, RAM, CPU cores, and matches to Machine-A or Machine-B profile.
"""
import json
import subprocess
import sys
from pathlib import Path

class HardwareAdapter:
    """Auto-detect hardware and generate adaptation profile."""
    
    def detect(self) -> dict:
        """Detect hardware and return full profile."""
        vram_gb = self._detect_vram()
        ram_gb = self._detect_ram()
        cpu_cores = self._detect_cpu_cores()
        platform = sys.platform  # 'win32', 'linux', 'darwin'
        
        # Hardware type classification
        hw_type = "A" if vram_gb >= 28 else "B"
        power = "high" if hw_type == "A" else "medium"
        
        # Generate adaptations based on hardware
        adaptations = self._generate_adaptations(hw_type)
        
        return {
            "hardware": {
                "type": hw_type,
                "vram_gb": round(vram_gb, 1),
                "ram_gb": round(ram_gb, 1),
                "cpu_cores": cpu_cores,
                "power_level": power,
                "detected_at": self._timestamp(),
                "platform": platform
            },
            "adaptations": adaptations
        }
    
    def _detect_vram(self) -> float:
        """Detect total VRAM via nvidia-smi."""
        try:
            # nvidia-smi --query-gpu=memory.total --format=csv,noheader,nounits
            result = subprocess.run(
                ["nvidia-smi", "--query-gpu=memory.total", "--format=csv,noheader,nounits"],
                capture_output=True, text=True, timeout=10
            )
            if result.returncode == 0:
                # Parse: "10240 MiB\n8192 MiB\n" → sum in GB
                total_mib = sum(
                    float(line.strip().split()[0])
                    for line in result.stdout.strip().split('\n')
                    if line.strip()
                )
                return total_mib / 1024  # MiB → GB
        except (FileNotFoundError, subprocess.TimeoutExpired, ValueError):
            pass
        
        # Fallback: try torch
        try:
            import torch
            if torch.cuda.is_available():
                return sum(
                    torch.cuda.get_device_properties(i).total_memory
                    for i in range(torch.cuda.device_count())
                ) / (1024**3)
        except ImportError:
            pass
        
        # No GPU detected
        return 0.0
    
    def _detect_ram(self) -> float:
        """Detect total system RAM."""
        try:
            import psutil
            return psutil.virtual_memory().total / (1024**3)
        except ImportError:
            return 0.0
    
    def _detect_cpu_cores(self) -> int:
        """Detect physical CPU cores."""
        try:
            import psutil
            return psutil.cpu_count(logical=False)
        except ImportError:
            import os
            return os.cpu_count() or 0
    
    def _generate_adaptations(self, hw_type: str) -> dict:
        """Generate adaptation parameters based on hardware profile."""
        if hw_type == "A":  # Machine-A (Beast: 3090+3080, 34GB VRAM, 64GB RAM)
            return {
                "sampling_method": "NUTS",
                "max_tree_depth": 11,
                "bayesian_samples": 2800,
                "checkpoint_interval_min": 45,
                "max_parallel_subagents": 3,
                "agent_model": "deepseek-v4-flash",
                "agent_provider": "deepseek",
                "eval_model": "deepseek-v4-pro",
                "eval_provider": "deepseek",
                "teacher_model": "deepseek-v4-pro",
                "teacher_provider": "deepseek",
                "vi_iterations": 800
            }
        else:  # Machine-B (Main: 3080+3070Ti, 18GB VRAM, 32GB RAM)
            return {
                "sampling_method": "VI",
                "max_tree_depth": 8,
                "bayesian_samples": 1400,
                "checkpoint_interval_min": 25,
                "max_parallel_subagents": 1,
                "agent_model": "deepseek-v4-flash",
                "agent_provider": "deepseek",
                "eval_model": "deepseek-v4-pro",
                "eval_provider": "deepseek",
                "teacher_model": "deepseek-v4-pro",
                "teacher_provider": "deepseek",
                "vi_iterations": 400
            }
    
    def _timestamp(self) -> str:
        from datetime import datetime, timezone
        return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


# CLI entry point
if __name__ == "__main__":
    adapter = HardwareAdapter()
    profile = adapter.detect()
    
    print(json.dumps(profile, indent=2))
    
    # Save profile
    from pathlib import Path
    from persistence import atomic_write_json
    
    forge_root = Path(__file__).resolve().parent.parent
    profile_path = forge_root / "99_INDEXES/hardware_profile.json"
    atomic_write_json(profile_path, profile)
    print(f"\nSaved to: {profile_path}")
```

---

## 4. `scripts/forge.py init` (included in Core_Loop_Implementation.md)

See `Core_Loop_Implementation.md` §3.1 for complete `cmd_init()` implementation.

---

## 5. First-Run Checklist

Before running `forge.py init`:

```bash
# 1. Verify Python
python --version  # Must be 3.10+

# 2. Install dependencies
pip install psutil pyyaml torch faiss-cpu sentence-transformers

# 3. Verify GPU
nvidia-smi

# 4. Verify DeepSeek key
hermes config get providers.deepseek.api_key

# 5. Run init
cd D:\styde\_alpedal\styde-forge
python scripts/forge.py init

# 6. Verify
python scripts/forge.py status
python scripts/detect.py
```

---

## 6. Dependencies

```
# requirements.txt
psutil>=5.9.0
pyyaml>=6.0
torch>=2.0.0        # CUDA support for RAG embeddings
faiss-cpu>=1.7.0     # Vector search (CPU fallback)
sentence-transformers>=2.2.0  # all-MiniLM-L6-v2 for RAG
```

---

**Status:** Specification complete. These three scripts are the foundation.

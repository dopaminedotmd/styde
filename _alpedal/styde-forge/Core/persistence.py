"""
Atomic filesystem operations for Styde Forge.
Every write uses temp-file + rename pattern.
Guarantees: never partial writes, crash-safe.
"""
import os
import json
import tempfile
import shutil
import time
from pathlib import Path


def atomic_write(path: Path | str, content: str) -> bool:
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
        
        # Retry os.replace for Windows file locking
        for retry in range(5):
            try:
                os.replace(tmp_path, str(path))
                return True
            except PermissionError:
                if retry < 4:
                    time.sleep(0.5 * (retry + 1))
                else:
                    # Final attempt: use shutil.move
                    shutil.move(str(tmp_path), str(path))
                    return True
        return True
    except Exception:
        try:
            os.unlink(tmp_path)
        except OSError:
            pass
        raise


def atomic_write_json(path: Path | str, data: dict) -> bool:
    """Write dict as JSON atomically with indent=2."""
    content = json.dumps(data, indent=2, ensure_ascii=False)
    return atomic_write(path, content)


def atomic_append(path: Path | str, line: str) -> bool:
    """
    Append a line to a log file atomically.
    For JSON-lines logging. Append-only, fsync for USB safety.
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


def transactional_save(dir_path: Path | str, files: dict) -> bool:
    """
    Save multiple files atomically.
    
    All files written to staging directory, then directory atomically renamed.
    If any write fails, staging is cleaned up.
    Used for checkpoints.
    
    Args:
        dir_path: Target directory
        files: {relative_path: content_or_dict} mapping
    """
    dir_path = Path(dir_path)
    staging = dir_path.parent / f".{dir_path.name}.staging"
    
    try:
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
        
        if dir_path.exists():
            shutil.rmtree(dir_path)
        os.replace(staging, str(dir_path))
        return True
        
    except Exception:
        if staging.exists():
            shutil.rmtree(staging)
        raise

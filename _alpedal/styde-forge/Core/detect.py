"""
Hardware auto-detection for Styde Forge.
Detects VRAM, RAM, CPU cores, and matches to Machine-A or Machine-B profile.
"""
import subprocess
import sys
from datetime import datetime, timezone


class HardwareAdapter:
    """Auto-detect hardware and generate adaptation profile."""

    def detect(self) -> dict:
        """Detect hardware and return full profile."""
        vram_gb = self._detect_vram()
        ram_gb = self._detect_ram()
        cpu_cores = self._detect_cpu_cores()
        platform = sys.platform

        hw_type = "A" if vram_gb >= 28 else "B"
        power = "high" if hw_type == "A" else "medium"
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
        """Detect total VRAM via nvidia-smi. Falls back to torch or 0.0."""
        try:
            result = subprocess.run(
                ["nvidia-smi", "--query-gpu=memory.total", "--format=csv,noheader,nounits"],
                capture_output=True, text=True, timeout=10
            )
            if result.returncode == 0 and result.stdout.strip():
                total_mib = sum(
                    float(line.strip().split()[0])
                    for line in result.stdout.strip().split('\n')
                    if line.strip()
                )
                return total_mib / 1024  # MiB → GB
        except (FileNotFoundError, subprocess.TimeoutExpired, ValueError):
            pass

        try:
            import torch
            if torch.cuda.is_available():
                return sum(
                    torch.cuda.get_device_properties(i).total_memory
                    for i in range(torch.cuda.device_count())
                ) / (1024 ** 3)
        except ImportError:
            pass

        return 0.0

    def _detect_ram(self) -> float:
        """Detect total system RAM in GB."""
        try:
            import psutil
            return psutil.virtual_memory().total / (1024 ** 3)
        except ImportError:
            return 0.0

    def _detect_cpu_cores(self) -> int:
        """Detect physical CPU cores."""
        try:
            import psutil
            return psutil.cpu_count(logical=False)
        except ImportError:
            return 0

    def _generate_adaptations(self, hw_type: str) -> dict:
        """Generate adaptation parameters based on hardware profile."""
        if hw_type == "A":
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
        else:
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
        return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

"""
Tests for Core.detect — hardware auto-detection.
TDD: RED phase.
"""
import pytest
import json
from pathlib import Path


class TestHardwareAdapter:
    """Test HardwareAdapter.detect() — profile structure and logic."""

    def test_detect_returns_valid_profile(self):
        """Profile has required top-level keys."""
        from Core.detect import HardwareAdapter

        adapter = HardwareAdapter()
        profile = adapter.detect()

        assert "hardware" in profile
        assert "adaptations" in profile

        hw = profile["hardware"]
        assert "type" in hw
        assert hw["type"] in ("A", "B")
        assert "vram_gb" in hw
        assert isinstance(hw["vram_gb"], (int, float))
        assert hw["vram_gb"] >= 0
        assert "ram_gb" in hw
        assert isinstance(hw["ram_gb"], (int, float))
        assert hw["ram_gb"] > 0
        assert "cpu_cores" in hw
        assert isinstance(hw["cpu_cores"], int)
        assert hw["cpu_cores"] > 0
        assert "power_level" in hw
        assert hw["power_level"] in ("high", "medium")
        assert "detected_at" in hw
        assert "platform" in hw

    def test_adaptations_match_profile_type(self):
        """Machine-A gets NUTS, Machine-B gets VI."""
        from Core.detect import HardwareAdapter

        adapter = HardwareAdapter()
        profile = adapter.detect()

        adaptations = profile["adaptations"]
        hw_type = profile["hardware"]["type"]

        assert "sampling_method" in adaptations
        assert adaptations["sampling_method"] in ("NUTS", "VI")

        if hw_type == "A":
            assert adaptations["sampling_method"] == "NUTS"
            assert adaptations["max_parallel_subagents"] >= 2
        else:
            assert adaptations["sampling_method"] == "VI"
            assert adaptations["max_parallel_subagents"] <= 2

    def test_adaptations_have_all_required_keys(self):
        """Every adaptation key from the spec is present."""
        from Core.detect import HardwareAdapter

        adapter = HardwareAdapter()
        profile = adapter.detect()
        adaptations = profile["adaptations"]

        required = [
            "sampling_method", "max_tree_depth", "bayesian_samples",
            "checkpoint_interval_min", "max_parallel_subagents",
            "agent_model", "agent_provider", "eval_model",
            "eval_provider", "teacher_model", "teacher_provider",
            "vi_iterations"
        ]
        for key in required:
            assert key in adaptations, f"Missing adaptation key: {key}"

    def test_vram_detection_returns_number(self):
        """VRAM detection returns a numeric value ≥0."""
        from Core.detect import HardwareAdapter

        adapter = HardwareAdapter()
        vram = adapter._detect_vram()

        assert isinstance(vram, (int, float))
        assert vram >= 0

    def test_ram_detection_returns_number(self):
        """RAM detection returns a numeric value >0."""
        from Core.detect import HardwareAdapter

        adapter = HardwareAdapter()
        ram = adapter._detect_ram()

        assert isinstance(ram, (int, float))
        assert ram > 0

    def test_cpu_cores_detection_returns_positive_int(self):
        """CPU cores detection returns a positive integer."""
        from Core.detect import HardwareAdapter

        adapter = HardwareAdapter()
        cores = adapter._detect_cpu_cores()

        assert isinstance(cores, int)
        assert cores > 0

    def test_profile_type_consistent_with_vram(self):
        """Machine-A if VRAM ≥28, Machine-B otherwise."""
        from Core.detect import HardwareAdapter

        adapter = HardwareAdapter()
        profile = adapter.detect()

        hw_type = profile["hardware"]["type"]
        vram = profile["hardware"]["vram_gb"]

        if vram >= 28:
            assert hw_type == "A"
        else:
            assert hw_type == "B"

    def test_detect_handles_no_nvidia_smi(self, monkeypatch):
        """Fallback to torch or 0.0 if nvidia-smi unavailable."""
        from Core.detect import HardwareAdapter
        import subprocess

        def mock_run(*args, **kwargs):
            raise FileNotFoundError("nvidia-smi not found")

        monkeypatch.setattr(subprocess, "run", mock_run)

        adapter = HardwareAdapter()
        vram = adapter._detect_vram()

        # Should fallback gracefully
        assert vram >= 0

    def test_generate_adaptations_a(self):
        """Machine-A adaptations are correct."""
        from Core.detect import HardwareAdapter

        adapter = HardwareAdapter()
        adaptations = adapter._generate_adaptations("A")

        assert adaptations["sampling_method"] == "NUTS"
        assert adaptations["max_tree_depth"] == 11
        assert adaptations["bayesian_samples"] == 2800
        assert adaptations["max_parallel_subagents"] == 3

    def test_generate_adaptations_b(self):
        """Machine-B adaptations are correct."""
        from Core.detect import HardwareAdapter

        adapter = HardwareAdapter()
        adaptations = adapter._generate_adaptations("B")

        assert adaptations["sampling_method"] == "VI"
        assert adaptations["max_tree_depth"] == 8
        assert adaptations["bayesian_samples"] == 1400
        assert adaptations["max_parallel_subagents"] == 1

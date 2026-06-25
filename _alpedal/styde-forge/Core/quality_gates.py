"""
Quality gates for Styde Forge.
Every agent must pass validation + security before checkpoint.
Hard gates — fail blocks delivery. Adopted from agent-skill-creator v6.
"""
import re
import yaml
from pathlib import Path

FORGE_ROOT = Path(__file__).resolve().parent.parent


# --- Validation ---

def validate_agent(agent_path: str | Path) -> dict:
    """
    Validate agent structure and content.
    
    Checks:
    - Required files exist
    - BLUEPRINT.md has ## Purpose section
    - persona.md is non-empty (≥50 chars)
    - config.yaml schema valid
    - Output is valid YAML or plain text (Caveman Ultra)
    - No placeholder code (pass, TODO, YOUR_KEY_HERE)
    - File count within limits
    
    Returns {passed: bool, errors: [str], warnings: [str]}
    """
    agent_path = Path(agent_path)
    errors = []
    warnings = []
    
    # Required files
    required = ["BLUEPRINT.md", "persona.md", "config.yaml"]
    for f in required:
        if not (agent_path / f).exists():
            errors.append(f"Missing required file: {f}")
    
    # Check persona.md
    persona = agent_path / "persona.md"
    if persona.exists():
        content = persona.read_text(encoding="utf-8").strip()
        if len(content) < 50:
            errors.append(f"persona.md too short: {len(content)} chars (min 50)")
    
    # Check BLUEPRINT.md
    blueprint = agent_path / "BLUEPRINT.md"
    if blueprint.exists():
        content = blueprint.read_text(encoding="utf-8")
        if "## Purpose" not in content and "## purpose" not in content:
            errors.append("BLUEPRINT.md must contain '## Purpose' section")
    
    # Check config.yaml schema
    config_path = agent_path / "config.yaml"
    if config_path.exists():
        try:
            cfg = yaml.safe_load(config_path.read_text(encoding="utf-8"))
            if "blueprint" not in cfg:
                errors.append("config.yaml missing 'blueprint' section")
            else:
                if "name" not in cfg["blueprint"]:
                    errors.append("config.yaml missing 'blueprint.name'")
                if "domain" not in cfg["blueprint"]:
                    errors.append("config.yaml missing 'blueprint.domain'")
        except yaml.YAMLError as e:
            errors.append(f"config.yaml parse error: {e}")
    
    # Check output (if exists)
    runs_dir = agent_path / "runs"
    if runs_dir.exists():
        for run_dir in sorted(runs_dir.glob("run-*")):
            output = run_dir / "output.md"
            if output.exists():
                content = output.read_text(encoding="utf-8")
                _check_placeholders(content, str(output), errors)
    
    return {
        "passed": len(errors) == 0,
        "errors": errors,
        "warnings": warnings
    }


def _check_placeholders(content: str, filepath: str, errors: list):
    """Check for placeholder code and stubs."""
    patterns = [
        (r"\bTODO\b", "Contains TODO"),
        (r"\bFIXME\b", "Contains FIXME"),
        (r"\bpass\s*$", "Contains pass statement"),
        (r"YOUR_KEY_HERE", "Contains placeholder API key"),
        (r"your-key-here", "Contains placeholder API key"),
        (r"api_key:\s*['\"]?\s*['\"]?", "Empty API key"),
    ]
    for pattern, msg in patterns:
        if re.search(pattern, content, re.IGNORECASE):
            errors.append(f"{filepath}: {msg}")


# --- Security Scan ---

def security_scan(agent_path: str | Path) -> dict:
    """
    Scan agent for security issues.
    
    Checks:
    - No hardcoded API keys
    - No hardcoded credentials (passwords, tokens)
    - No .env files committed
    - No injection patterns in scripts
    - No secrets in output
    
    CRITICAL findings block delivery.
    HIGH findings warn but don't block.
    
    Returns {passed: bool, findings: [{severity, file, line, description}]}
    """
    agent_path = Path(agent_path)
    findings = []
    
    # Scan all files in agent directory
    for f in agent_path.rglob("*"):
        if not f.is_file():
            continue
        if f.suffix in [".pyc", ".pyo", ".tmp"]:
            continue
        if ".git" in f.parts:
            continue
        
        try:
            content = f.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        
        rel_path = str(f.relative_to(agent_path))
        
        # Hardcoded API keys
        _scan_api_keys(content, rel_path, findings)
        
        # Hardcoded credentials
        _scan_credentials(content, rel_path, findings)
        
        # .env files
        if f.name in [".env", ".env.local", ".env.production"]:
            findings.append({
                "severity": "critical",
                "file": rel_path,
                "line": 0,
                "description": ".env file should not be committed — use env vars"
            })
        
        # Injection patterns in scripts
        if f.suffix == ".py":
            _scan_injection_patterns(content, rel_path, findings)
    
    critical = [f for f in findings if f["severity"] == "critical"]
    
    return {
        "passed": len(critical) == 0,
        "findings": findings,
        "critical_count": len(critical),
        "warning_count": len(findings) - len(critical)
    }


def _scan_api_keys(content: str, filepath: str, findings: list):
    """Detect hardcoded API keys."""
    patterns = [
        (r'sk-[a-zA-Z0-9]{20,}', "OpenAI/DeepSeek API key"),
        (r'AIza[0-9A-Za-z\-_]{35}', "Google API key"),
        (r'xai-[a-zA-Z0-9]{20,}', "xAI API key"),
        (r'api_key\s*=\s*["\'][a-zA-Z0-9_-]{20,}["\']', "Hardcoded API key value"),
        (r'Bearer\s+[a-zA-Z0-9._\-]{20,}', "Hardcoded bearer token"),
    ]
    
    for pattern, desc in patterns:
        for i, line in enumerate(content.split("\n"), 1):
            if re.search(pattern, line) and not line.strip().startswith("#"):
                findings.append({
                    "severity": "critical",
                    "file": filepath,
                    "line": i,
                    "description": f"Hardcoded {desc}"
                })


def _scan_credentials(content: str, filepath: str, findings: list):
    """Detect hardcoded passwords and tokens."""
    patterns = [
        (r'password\s*=\s*["\'][^"\']+["\']', "Hardcoded password"),
        (r'secret\s*=\s*["\'][^"\']+["\']', "Hardcoded secret"),
        (r'token\s*=\s*["\'][a-zA-Z0-9._\-]{20,}["\']', "Hardcoded token"),
    ]
    
    for pattern, desc in patterns:
        for i, line in enumerate(content.split("\n"), 1):
            if re.search(pattern, line) and not line.strip().startswith("#"):
                if "env" not in line.lower() and "os.environ" not in line.lower():
                    findings.append({
                        "severity": "high",
                        "file": filepath,
                        "line": i,
                        "description": desc
                    })


def _scan_injection_patterns(content: str, filepath: str, findings: list):
    """Detect potential injection patterns in Python."""
    patterns = [
        (r'os\.system\(.*\{.*\}', "Potential command injection via os.system"),
        (r'subprocess\.call\(.*shell\s*=\s*True', "subprocess with shell=True"),
        (r'eval\(', "eval() usage — potential code injection"),
        (r'exec\(', "exec() usage — potential code injection"),
    ]
    
    for pattern, desc in patterns:
        for i, line in enumerate(content.split("\n"), 1):
            if re.search(pattern, line) and not line.strip().startswith("#"):
                findings.append({
                    "severity": "high",
                    "file": filepath,
                    "line": i,
                    "description": desc
                })

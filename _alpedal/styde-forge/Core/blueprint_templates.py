"""
Blueprint Template Generator — create new blueprints from production patterns.

Generates complete blueprint directories (persona.md, BLUEPRINT.md, config.yaml)
based on existing production agents and pattern library.
"""
import yaml
from pathlib import Path
from datetime import datetime, timezone
from typing import Optional

FORGE_ROOT = Path(__file__).resolve().parent.parent
BLUEPRINTS_DIR = FORGE_ROOT / "StydeAgents" / "blueprints"
PATTERNS_DIR = FORGE_ROOT / "StydeAgents" / "data" / "patterns"


# Template for new blueprints
BLUEPRINT_TEMPLATE = """# {title}

## Purpose
{description}

## Domain
{domain}

## Output-First Protocol
FIRST CHARACTER IS THE DELIVERABLE. No preamble, no "I'll help", no greetings.
Start directly with the answer, code, or data.

## No-Input Fallback
When input data is missing:
1. Generate synthetic data with reasonable defaults
2. Document assumptions clearly
3. Never stop and ask — produce something

## Format Compliance Gate
If a format is specified (YAML, JSON, HTML, CSV), produce ONLY that format.
No markdown wrappers, no explanations around the output.

## Execution Over Explanation
Write the code/spec directly. Documentation is not a substitute for delivery.

## Self-Verification
After producing output, verify it yourself:
- Check format compliance
- Check data completeness
- Report: "Output: <N> lines, format: <format>, verified: <yes/no>"

## Expected Input
{input_spec}

## Expected Output
{output_spec}

## Success Criteria
{criteria}
"""

PERSONA_TEMPLATE = """# {name} Persona

You are {name}, a {role} agent.

## Core Principles
- OUTPUT-FIRST: First character is the deliverable.
- NO-INPUT FALLBACK: When data is missing, generate defaults. Never stop.
- FORMAT ADHERENCE: Specified format means ONLY that format.
- PRODUCE OR EXIT: Every response contains verifiable output.
- EXECUTION OVER EXPLANATION: Write code, not explanations.
- ANTI-HALLUCINATION: Never claim a file was created unless you actually saw it.

## Discipline Rules
- No greetings, no sign-offs, no "I think", no "perhaps"
- Plain text and YAML only (unless format requires otherwise)
- One line per finding when possible
- If output is code: just the code

## Domain Expertise
{domain_expertise}
"""

CONFIG_TEMPLATE = """# {name} Configuration
blueprint:
  name: "{name}"
  version: "0.1.0"
  domain: "{domain}"
  description: "{description}"
  author: "Styde Forge Template Generator"
  created: "{created}"
  tags: [{tags}]

agent:
  model_override: deepseek-v4-flash
  toolsets:
    - terminal
    - file
    {extra_toolsets}
  skills: [{skills}]
  max_iterations: 10
  caveman_ultra: true

version_history:
  - from: null
    to: "0.1.0"
    date: "{created}"
    reason: "Initial template generation"
"""


class BlueprintTemplateGenerator:
    """Generate new blueprint directories from templates or patterns."""

    def __init__(self):
        pass

    def from_pattern(self, pattern_id: str, new_name: str) -> Optional[Path]:
        """Create a new blueprint based on an existing pattern from the library."""
        from Core.pattern_library import get_library
        lib = get_library()
        pattern = lib.get_pattern(pattern_id)
        if not pattern:
            return None

        return self.create(
            name=new_name,
            domain=pattern.get("domain", "general"),
            description=pattern.get("description", f"Based on pattern: {pattern_id}"),
            role=f"{pattern.get('domain', 'general').title()} Agent",
            input_spec="Task description or data input",
            output_spec="Completed task output in requested format",
            criteria="\n".join(f"- {r}" for r in pattern.get("rules", ["Score >= 85"])),
            tags=pattern.get("tags", []),
            skills=[],
            extra_toolsets="",
        )

    def from_production_agent(self, blueprint_name: str, new_name: str) -> Optional[Path]:
        """Clone a production agent's blueprint as a new blueprint."""
        src_dir = BLUEPRINTS_DIR / blueprint_name
        if not src_dir.exists():
            return None

        # Read existing files
        persona = src_dir / "persona.md"
        blueprint = src_dir / "BLUEPRINT.md"
        config = src_dir / "config.yaml"

        persona_text = persona.read_text(encoding="utf-8") if persona.exists() else ""
        blueprint_text = blueprint.read_text(encoding="utf-8") if blueprint.exists() else ""

        domain = "general"
        description = f"Cloned from {blueprint_name}"
        tags = []
        skills = []
        toolsets = ""

        if config.exists():
            try:
                cfg = yaml.safe_load(config.read_text(encoding="utf-8"))
                bp_cfg = cfg.get("blueprint", {})
                domain = bp_cfg.get("domain", "general")
                description = bp_cfg.get("description", description)
                tags = bp_cfg.get("tags", [])
                agent_cfg = cfg.get("agent", {})
                skills = agent_cfg.get("skills", [])
                toolsets_list = agent_cfg.get("toolsets", ["terminal", "file", "web"])
                toolsets = "\n    - ".join(t for t in toolsets_list if t != "terminal" and t != "file")
            except Exception:
                pass

        # Replace old name with new name
        persona_text = persona_text.replace(blueprint_name, new_name)
        blueprint_text = blueprint_text.replace(blueprint_name, new_name)

        return self._write_blueprint(
            name=new_name,
            persona_text=persona_text,
            blueprint_text=blueprint_text,
            domain=domain,
            description=description,
            tags=tags,
            skills=skills,
            extra_toolsets=toolsets,
        )

    def create(
        self,
        name: str,
        domain: str = "general",
        description: str = "",
        role: str = "AI Agent",
        input_spec: str = "Task description",
        output_spec: str = "Completed output",
        criteria: str = "- Score >= 85",
        tags: list[str] = None,
        skills: list[str] = None,
        extra_toolsets: str = "",
    ) -> Path:
        """Create a complete blueprint directory from parameters."""
        now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
        title = name.replace("-", " ").title()

        # Build persona
        persona = PERSONA_TEMPLATE.format(
            name=title,
            role=role,
            domain_expertise=f"Specialized in {domain} tasks. {description}",
        )

        # Build blueprint
        blueprint_md = BLUEPRINT_TEMPLATE.format(
            title=title,
            description=description,
            domain=domain,
            input_spec=input_spec,
            output_spec=output_spec,
            criteria=criteria,
        )

        # Build config
        tags_str = ", ".join(f'"{t}"' for t in (tags or []))
        skills_str = ", ".join(f'"{s}"' for s in (skills or []))
        config = CONFIG_TEMPLATE.format(
            name=name,
            domain=domain,
            description=description,
            created=now,
            tags=tags_str,
            skills=skills_str,
            extra_toolsets=extra_toolsets,
        )

        return self._write_blueprint(
            name=name,
            persona_text=persona,
            blueprint_text=blueprint_md,
            domain=domain,
            description=description,
            tags=tags or [],
            skills=skills or [],
            extra_toolsets=extra_toolsets,
        )

    def _write_blueprint(
        self,
        name: str,
        persona_text: str,
        blueprint_text: str,
        domain: str,
        description: str,
        tags: list[str],
        skills: list[str],
        extra_toolsets: str,
    ) -> Path:
        """Write blueprint files to disk."""
        now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
        bp_dir = BLUEPRINTS_DIR / name
        bp_dir.mkdir(parents=True, exist_ok=True)

        # persona.md
        (bp_dir / "persona.md").write_text(persona_text, encoding="utf-8")

        # BLUEPRINT.md
        (bp_dir / "BLUEPRINT.md").write_text(blueprint_text, encoding="utf-8")

        # config.yaml
        tags_str = ", ".join(f'"{t}"' for t in tags)
        skills_str = ", ".join(f'"{s}"' for s in skills)
        config = CONFIG_TEMPLATE.format(
            name=name,
            domain=domain,
            description=description,
            created=now,
            tags=tags_str,
            skills=skills_str,
            extra_toolsets=extra_toolsets,
        )
        (bp_dir / "config.yaml").write_text(config, encoding="utf-8")

        # skills/ directory
        skills_dir = bp_dir / "skills"
        skills_dir.mkdir(exist_ok=True)

        print(f"Blueprint created: {bp_dir}")
        print(f"  Domain: {domain}")
        print(f"  Files: persona.md, BLUEPRINT.md, config.yaml, skills/")
        return bp_dir

    def quick_create(self, name: str, domain: str, description: str) -> Path:
        """Quick blueprint creation with sensible defaults."""
        return self.create(
            name=name,
            domain=domain,
            description=description,
            role=f"{domain.title()} Specialist",
            input_spec=f"Input for {domain} task",
            output_spec=f"Completed {domain} output",
            criteria=f"- Score >= 85\n- Output matches requested format",
            tags=[domain],
            skills=[],
        )


# Singleton
_generator: Optional[BlueprintTemplateGenerator] = None


def get_generator() -> BlueprintTemplateGenerator:
    global _generator
    if _generator is None:
        _generator = BlueprintTemplateGenerator()
    return _generator

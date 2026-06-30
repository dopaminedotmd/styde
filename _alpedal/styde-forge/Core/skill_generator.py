"""
Blueprint Skill Auto-Generator — create skill .md files from pattern library.

Scans pattern library and production agents, generates reusable skill files
that can be placed in any blueprint's skills/ directory.
"""
import yaml
from pathlib import Path
from datetime import datetime, timezone
from collections import defaultdict
from typing import Optional

FORGE_ROOT = Path(__file__).resolve().parent.parent
SKILLS_OUTPUT_DIR = FORGE_ROOT / "StydeAgents" / "data" / "generated_skills"

SKILL_TEMPLATE = """# {title}

{description}

## Rules

{rules}

## When To Use

{when_to_use}

## Source

Generated from pattern: `{source_pattern}`
Source blueprint: `{source_bp}` (score: {source_score}/100)
Generated: {generated_at}
"""


class SkillGenerator:
    """Generate skill .md files from patterns and production agents."""

    def __init__(self):
        SKILLS_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    def generate_from_patterns(self, min_score: float = 85.0, domain: str = "") -> list[Path]:
        """Generate skill files from all high-scoring patterns."""
        from Core.pattern_library import get_library
        lib = get_library()
        patterns = lib.find_patterns(domain=domain, min_score=min_score, limit=50)

        generated = []
        for pat in patterns:
            skill_path = self._generate_skill(
                title=pat.get("name", "Unknown Pattern"),
                description=pat.get("description", ""),
                rules=pat.get("rules", []),
                source_pattern=pat.get("name", ""),
                source_bp=pat.get("source_blueprint", ""),
                source_score=pat.get("source_score", 0),
                domain=pat.get("domain", "general"),
                tags=pat.get("tags", []),
            )
            if skill_path:
                generated.append(skill_path)

        return generated

    def generate_from_production_agents(self, limit: int = 20) -> list[Path]:
        """Generate skills from top production agents."""
        prod_dir = FORGE_ROOT / "StydeAgents" / "production"
        if not prod_dir.exists():
            return []

        # Find best production agents
        bp_scores = []
        for bp_dir in sorted(prod_dir.iterdir()):
            if not bp_dir.is_dir():
                continue
            runs_dir = bp_dir / "runs"
            if not runs_dir.exists():
                continue
            best_score = 0
            best_run = None
            for run_dir in runs_dir.iterdir():
                if not run_dir.name.startswith("run-"):
                    continue
                ev = run_dir / "eval.yaml"
                if ev.exists():
                    try:
                        data = yaml.safe_load(ev.read_text(encoding="utf-8"))
                        sc = data.get("composite", {}).get("composite_score", 0)
                        if sc > best_score:
                            best_score = sc
                            best_run = run_dir
                    except Exception:
                        pass
            if best_score >= 85 and best_run:
                bp_scores.append((bp_dir.name, best_score, best_run))

        bp_scores.sort(key=lambda x: x[1], reverse=True)
        bp_scores = bp_scores[:limit]

        generated = []
        for bp_name, score, run_dir in bp_scores:
            # Extract rules from teacher review
            review_file = run_dir / "teacher_review.yaml"
            rules = []
            if review_file.exists():
                try:
                    review = yaml.safe_load(review_file.read_text(encoding="utf-8"))
                    if isinstance(review, dict):
                        # Get pattern rules
                        pat = review.get("pattern", {})
                        if isinstance(pat, dict):
                            rules = pat.get("rules", [])
                        # Also get improvements as rules
                        for imp in review.get("improvements", []):
                            if isinstance(imp, dict):
                                rules.append(f"{imp.get('target', '')}: {imp.get('change', '')}")
                except Exception:
                    pass

            if not rules:
                rules = ["Score >= 85 — production-ready agent"]

            # Get domain from config
            domain = "general"
            cfg = FORGE_ROOT / "StydeAgents" / "blueprints" / bp_name / "config.yaml"
            if cfg.exists():
                try:
                    config = yaml.safe_load(cfg.read_text(encoding="utf-8"))
                    domain = config.get("blueprint", {}).get("domain", "general")
                except Exception:
                    pass

            skill_path = self._generate_skill(
                title=f"{bp_name.replace('-', ' ').title()} Best Practices",
                description=f"Proven practices from {bp_name} (production agent, score {score}/100)",
                rules=rules,
                source_pattern=bp_name,
                source_bp=bp_name,
                source_score=score,
                domain=domain,
                tags=[domain, "production"],
            )
            if skill_path:
                generated.append(skill_path)

        return generated

    def generate_domain_skills(self) -> list[Path]:
        """Generate domain-specific skill files aggregating best rules."""
        from Core.pattern_library import get_library
        lib = get_library()

        # Group patterns by domain
        all_patterns = lib.find_patterns(min_score=80, limit=200)
        by_domain = defaultdict(list)
        for pat in all_patterns:
            domain = pat.get("domain", "general")
            by_domain[domain].append(pat)

        generated = []
        for domain, patterns in by_domain.items():
            if len(patterns) < 2:
                continue

            # Collect all unique rules
            all_rules = []
            seen = set()
            for pat in patterns:
                for rule in pat.get("rules", []):
                    if rule not in seen:
                        all_rules.append(rule)
                        seen.add(rule)

            avg_score = sum(p.get("source_score", 0) for p in patterns) / len(patterns)

            skill_path = self._generate_skill(
                title=f"{domain.title()} Domain Best Practices",
                description=f"Aggregated rules from {len(patterns)} {domain} production agents (avg score: {avg_score:.0f}/100)",
                rules=all_rules[:20],
                source_pattern=f"domain:{domain}",
                source_bp="multiple",
                source_score=round(avg_score),
                domain=domain,
                tags=[domain, "aggregated"],
            )
            if skill_path:
                generated.append(skill_path)

        return generated

    def _generate_skill(
        self,
        title: str,
        description: str,
        rules: list[str],
        source_pattern: str,
        source_bp: str,
        source_score: float,
        domain: str,
        tags: list[str],
    ) -> Optional[Path]:
        """Write a single skill file."""
        # Sanitize filename
        safe_name = title.lower().replace(" ", "-").replace("/", "-")[:64]
        skill_path = SKILLS_OUTPUT_DIR / f"{safe_name}.md"

        rules_text = "\n".join(f"- {r}" for r in rules) if rules else "- No specific rules extracted"

        when_to_use = f"Use when working with {domain} tasks."
        if tags:
            when_to_use += f" Tags: {', '.join(tags)}."

        content = SKILL_TEMPLATE.format(
            title=title,
            description=description,
            rules=rules_text,
            when_to_use=when_to_use,
            source_pattern=source_pattern,
            source_bp=source_bp,
            source_score=source_score,
            generated_at=datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        )

        skill_path.write_text(content, encoding="utf-8")
        return skill_path

    def install_to_blueprint(self, blueprint_name: str, skill_name: str) -> bool:
        """Install a generated skill into a specific blueprint's skills/ directory."""
        src = SKILLS_OUTPUT_DIR / f"{skill_name}.md"
        if not src.exists():
            # Try partial match
            matches = list(SKILLS_OUTPUT_DIR.glob(f"*{skill_name}*.md"))
            if matches:
                src = matches[0]
            else:
                return False

        dst_dir = FORGE_ROOT / "StydeAgents" / "blueprints" / blueprint_name / "skills"
        dst_dir.mkdir(parents=True, exist_ok=True)

        dst = dst_dir / src.name
        dst.write_text(src.read_text(encoding="utf-8"))
        return True

    def install_to_all(self, skill_name: str, domain: str = "") -> int:
        """Install a generated skill to all blueprints in a domain (or all)."""
        src = SKILLS_OUTPUT_DIR / f"{skill_name}.md"
        if not src.exists():
            matches = list(SKILLS_OUTPUT_DIR.glob(f"*{skill_name}*.md"))
            if matches:
                src = matches[0]
            else:
                return 0

        blueprints_dir = FORGE_ROOT / "StydeAgents" / "blueprints"
        installed = 0

        for bp_dir in blueprints_dir.iterdir():
            if not bp_dir.is_dir() or bp_dir.name.startswith("_"):
                continue

            if domain:
                cfg = bp_dir / "config.yaml"
                if cfg.exists():
                    try:
                        config = yaml.safe_load(cfg.read_text(encoding="utf-8"))
                        bp_domain = config.get("blueprint", {}).get("domain", "")
                        if bp_domain != domain:
                            continue
                    except Exception:
                        continue

            dst_dir = bp_dir / "skills"
            dst_dir.mkdir(exist_ok=True)
            dst = dst_dir / src.name
            dst.write_text(src.read_text(encoding="utf-8"))
            installed += 1

        return installed

    def list_generated(self) -> list[dict]:
        """List all generated skills."""
        skills = []
        for f in sorted(SKILLS_OUTPUT_DIR.glob("*.md")):
            skills.append({
                "name": f.stem,
                "size": f.stat().st_size,
                "path": str(f),
            })
        return skills


# Singleton
_generator: Optional[SkillGenerator] = None


def get_skill_generator() -> SkillGenerator:
    global _generator
    if _generator is None:
        _generator = SkillGenerator()
    return _generator

"""
Blueprint Dependency Graph — map relationships between blueprints.

Finds synergies: shared skills, domain overlap, pattern reuse,
historical co-promotion patterns. Helps identify which blueprints
benefit from each other's improvements.
"""
import yaml
from pathlib import Path
from collections import defaultdict
from typing import Optional

FORGE_ROOT = Path(__file__).resolve().parent.parent
BLUEPRINTS_DIR = FORGE_ROOT / "StydeAgents" / "blueprints"
PATTERNS_DIR = FORGE_ROOT / "StydeAgents" / "data" / "patterns"


class DependencyGraph:
    """Analyzes blueprint relationships."""

    def __init__(self):
        self._cache: Optional[dict] = None
        self._bp_skills: dict[str, set[str]] = {}
        self._bp_domains: dict[str, str] = {}
        self._bp_tags: dict[str, set[str]] = {}
        self._scan()

    def _scan(self):
        """Quick scan of all blueprints for metadata."""
        if not BLUEPRINTS_DIR.exists():
            return
        for bp_dir in BLUEPRINTS_DIR.iterdir():
            if not bp_dir.is_dir() or bp_dir.name.startswith("_"):
                continue
            bp_name = bp_dir.name

            # Skills
            skills_dir = bp_dir / "skills"
            if skills_dir.exists():
                self._bp_skills[bp_name] = {f.stem for f in skills_dir.glob("*.md")}

            # Config
            cfg_path = bp_dir / "config.yaml"
            if cfg_path.exists():
                try:
                    cfg = yaml.safe_load(cfg_path.read_text(encoding="utf-8"))
                    if isinstance(cfg, dict):
                        bp_cfg = cfg.get("blueprint", {})
                        self._bp_domains[bp_name] = bp_cfg.get("domain", "general")
                        self._bp_tags[bp_name] = set(bp_cfg.get("tags", []))
                except Exception:
                    pass

    def find_related(self, blueprint_name: str, max_results: int = 10) -> list[dict]:
        """Find blueprints related to the given one by skills/domain/tags."""
        target_skills = self._bp_skills.get(blueprint_name, set())
        target_domain = self._bp_domains.get(blueprint_name, "general")
        target_tags = self._bp_tags.get(blueprint_name, set())

        scored = []
        for bp_name in self._bp_domains:
            if bp_name == blueprint_name:
                continue

            score = 0
            reasons = []

            # Shared skills
            bp_skills = self._bp_skills.get(bp_name, set())
            shared = target_skills & bp_skills
            if shared:
                score += len(shared) * 10
                reasons.append(f"shares {len(shared)} skills: {', '.join(list(shared)[:3])}")

            # Same domain
            bp_domain = self._bp_domains.get(bp_name, "general")
            if bp_domain == target_domain:
                score += 5
                reasons.append(f"same domain: {bp_domain}")

            # Shared tags
            bp_tags = self._bp_tags.get(bp_name, set())
            shared_tags = target_tags & bp_tags
            if shared_tags:
                score += len(shared_tags) * 2
                reasons.append(f"shares tags: {', '.join(shared_tags)}")

            if score > 0:
                scored.append({
                    "blueprint": bp_name,
                    "domain": bp_domain,
                    "score": score,
                    "reasons": reasons,
                })

        scored.sort(key=lambda x: x["score"], reverse=True)
        return scored[:max_results]

    def find_skill_clusters(self, min_shared: int = 2) -> list[dict]:
        """Find clusters of blueprints that share skills."""
        clusters = []
        seen_pairs = set()

        bps = list(self._bp_skills.keys())
        for i, bp1 in enumerate(bps):
            for bp2 in bps[i + 1:]:
                pair = tuple(sorted([bp1, bp2]))
                if pair in seen_pairs:
                    continue
                seen_pairs.add(pair)

                s1 = self._bp_skills.get(bp1, set())
                s2 = self._bp_skills.get(bp2, set())
                shared = s1 & s2

                if len(shared) >= min_shared:
                    clusters.append({
                        "blueprints": [bp1, bp2],
                        "shared_skills": list(shared),
                        "count": len(shared),
                    })

        clusters.sort(key=lambda x: x["count"], reverse=True)
        return clusters[:20]

    def find_domain_trends(self) -> dict:
        """Analyze which domains have the most blueprints and skill overlap."""
        domains = defaultdict(lambda: {"count": 0, "skills": set(), "blueprints": []})

        for bp_name, domain in self._bp_domains.items():
            d = domains[domain]
            d["count"] += 1
            d["blueprints"].append(bp_name)
            d["skills"].update(self._bp_skills.get(bp_name, set()))

        result = {}
        for domain, data in sorted(domains.items(), key=lambda x: x[1]["count"], reverse=True):
            result[domain] = {
                "blueprint_count": data["count"],
                "unique_skills": len(data["skills"]),
                "avg_skills_per_bp": round(len(data["skills"]) / max(data["count"], 1), 1),
            }

        return result

    def get_improvement_candidates(self) -> list[dict]:
        """Find blueprints that could benefit from related BPs' patterns."""
        candidates = []
        for bp_name in self._bp_skills:
            related = self.find_related(bp_name, max_results=3)
            if related:
                candidates.append({
                    "blueprint": bp_name,
                    "domain": self._bp_domains.get(bp_name, "general"),
                    "skill_count": len(self._bp_skills.get(bp_name, set())),
                    "related": [r["blueprint"] for r in related[:3]],
                })

        # Prioritize BPs with few skills but many related
        candidates.sort(key=lambda x: (len(x["related"]), -x["skill_count"]), reverse=True)
        return candidates[:20]


# Singleton
_graph: Optional[DependencyGraph] = None


def get_graph() -> DependencyGraph:
    global _graph
    if _graph is None:
        _graph = DependencyGraph()
    return _graph

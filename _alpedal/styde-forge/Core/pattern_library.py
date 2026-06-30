"""
Pattern Library — reusable success patterns extracted from production agents.

When an agent reaches production (score >= 85, 3x consecutive), its
successful patterns are extracted and stored for reuse by other blueprints.

Patterns are stored in StydeAgents/data/patterns/ as YAML files.
"""
import yaml
from pathlib import Path
from datetime import datetime, timezone
from typing import Optional


FORGE_ROOT = Path(__file__).resolve().parent.parent
PATTERNS_DIR = FORGE_ROOT / "StydeAgents" / "data" / "patterns"


class PatternLibrary:
    """Store and query reusable agent patterns."""

    def __init__(self):
        self._patterns: Optional[dict[str, dict]] = None

    def _ensure_loaded(self):
        """Lazy-load all patterns from disk."""
        if self._patterns is not None:
            return
        self._patterns = {}
        if not PATTERNS_DIR.exists():
            PATTERNS_DIR.mkdir(parents=True, exist_ok=True)
            return
        for pat_file in PATTERNS_DIR.glob("*.yaml"):
            try:
                data = yaml.safe_load(pat_file.read_text(encoding="utf-8"))
                if isinstance(data, dict) and "name" in data:
                    self._patterns[pat_file.stem] = data
            except Exception:
                pass

    def add_pattern(
        self,
        name: str,
        description: str,
        blueprint: str,
        score: float,
        domain: str = "",
        tags: list[str] = None,
        rules: list[str] = None,
        prompt_snippet: str = "",
        dimensions: dict = None,
    ) -> dict:
        """Store a successful pattern from a production agent."""
        self._ensure_loaded()

        pattern_id = f"{domain or 'general'}-{name.lower().replace(' ', '-')}"
        pattern = {
            "name": name,
            "description": description,
            "source_blueprint": blueprint,
            "source_score": score,
            "domain": domain or "general",
            "tags": tags or [],
            "rules": rules or [],
            "prompt_snippet": prompt_snippet,
            "dimensions": dimensions or {},
            "created": datetime.now(timezone.utc).isoformat(),
            "reuse_count": 0,
        }

        pat_file = PATTERNS_DIR / f"{pattern_id}.yaml"
        pat_file.write_text(
            yaml.dump(pattern, default_flow_style=False, allow_unicode=True),
            encoding="utf-8",
        )

        self._patterns[pattern_id] = pattern
        return pattern

    def get_pattern(self, pattern_id: str) -> Optional[dict]:
        """Get a specific pattern by ID."""
        self._ensure_loaded()
        return self._patterns.get(pattern_id)

    def find_patterns(
        self,
        domain: str = None,
        tags: list[str] = None,
        min_score: float = 0,
        limit: int = 10,
    ) -> list[dict]:
        """Find patterns matching filters. Sorted by score descending."""
        self._ensure_loaded()
        results = []
        for pid, pat in self._patterns.items():
            if domain and pat.get("domain") != domain:
                continue
            if tags and not any(t in pat.get("tags", []) for t in tags):
                continue
            if pat.get("source_score", 0) < min_score:
                continue
            results.append(pat)

        results.sort(key=lambda p: p.get("source_score", 0), reverse=True)
        return results[:limit]

    def get_rules_for_blueprint(self, blueprint_name: str, domain: str = "", limit: int = 5) -> list[str]:
        """Get top rules from successful patterns that could apply to a blueprint."""
        self._ensure_loaded()
        patterns = self.find_patterns(domain=domain, min_score=85, limit=limit)
        if not patterns and domain:
            patterns = self.find_patterns(min_score=85, limit=limit)

        rules = []
        for pat in patterns:
            for rule in pat.get("rules", []):
                if rule not in rules:
                    rules.append(rule)
        return rules[:10]

    def mark_reused(self, pattern_id: str):
        """Increment reuse counter for a pattern."""
        self._ensure_loaded()
        if pattern_id in self._patterns:
            self._patterns[pattern_id]["reuse_count"] = \
                self._patterns[pattern_id].get("reuse_count", 0) + 1
            pat_file = PATTERNS_DIR / f"{pattern_id}.yaml"
            pat_file.write_text(
                yaml.dump(self._patterns[pattern_id], default_flow_style=False, allow_unicode=True),
                encoding="utf-8",
            )

    def stats(self) -> dict:
        """Get library statistics."""
        self._ensure_loaded()
        domains = {}
        tags = {}
        total_reuse = 0
        top_score = 0
        top_pattern = ""

        for pid, pat in self._patterns.items():
            domain = pat.get("domain", "general")
            domains[domain] = domains.get(domain, 0) + 1
            for tag in pat.get("tags", []):
                tags[tag] = tags.get(tag, 0) + 1
            total_reuse += pat.get("reuse_count", 0)
            if pat.get("source_score", 0) > top_score:
                top_score = pat["source_score"]
                top_pattern = pat.get("name", pid)

        return {
            "total_patterns": len(self._patterns),
            "domains": domains,
            "top_tags": dict(sorted(tags.items(), key=lambda x: x[1], reverse=True)[:10]),
            "total_reuse": total_reuse,
            "top_pattern": {"name": top_pattern, "score": top_score},
        }

    def extract_from_teacher_review(self, blueprint: str, run_dir: Path) -> Optional[dict]:
        """Extract a pattern from a teacher review that recommends it."""
        review_file = run_dir / "teacher_review.yaml"
        if not review_file.exists():
            return None

        try:
            review = yaml.safe_load(review_file.read_text(encoding="utf-8"))
        except Exception:
            return None

        pat = review.get("pattern") if isinstance(review, dict) else None
        if not pat or not pat.get("name"):
            return None

        # Get eval data for score
        eval_file = run_dir / "eval.yaml"
        score = 0
        if eval_file.exists():
            try:
                eval_data = yaml.safe_load(eval_file.read_text(encoding="utf-8"))
                score = eval_data.get("composite", {}).get("composite_score", 0)
            except Exception:
                pass

        return self.add_pattern(
            name=pat["name"],
            description=pat.get("description", ""),
            blueprint=blueprint,
            score=score,
            rules=pat.get("rules", review.get("improvements", [])),
            dimensions=pat.get("dimensions", {}),
        )


# Singleton
_library: Optional[PatternLibrary] = None


def get_library() -> PatternLibrary:
    global _library
    if _library is None:
        _library = PatternLibrary()
    return _library

#!/usr/bin/env python3
"""Check starter structure and local skill metadata without extra dependencies."""
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
REQUIRED = [
    "AGENTS.md", "starter/AGENTS.md",
    "starter/.agents/skills/project-structure/SKILL.md",
    "skills/project-structure/SKILL.md",
    "skills/product-specification/SKILL.md",
    "skills/starter-maintenance/SKILL.md",
    "catalog/core.yaml", "docs/decisions/TEMPLATE.md",
]
errors = []
for path in REQUIRED:
    if not (ROOT / path).is_file():
        errors.append(f"Missing: {path}")
for skill in (ROOT / "skills").glob("*/SKILL.md"):
    content = skill.read_text()
    if not content.startswith("---\n") or "\nname:" not in content or "\ndescription:" not in content:
        errors.append(f"Invalid skill frontmatter: {skill.relative_to(ROOT)}")
for error in errors:
    print("ERROR:", error)
if errors:
    sys.exit(1)
print(f"Validation passed ({len(REQUIRED)} required files; {len(list((ROOT / 'skills').glob('*/SKILL.md')))} local skills).")

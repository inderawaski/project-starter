#!/usr/bin/env python3
"""Validate repository files, skill metadata, source pins, and starter policy."""
import json
from pathlib import Path
import re
import sys
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from skill_installer import CLI_VERSION

REQUIRED_FILES = [
    "AGENTS.md",
    "starter/AGENTS.md",
    "starter/.agents/references/architecture-principles.md",
    "skills/project-structure/SKILL.md",
    "skills/testing-strategy/SKILL.md",
    "skills/ai-product-practices/SKILL.md",
    "skills/product-specification/SKILL.md",
    "skills/starter-maintenance/SKILL.md",
    "scripts/init.py",
    "scripts/skill_installer.py",
    "scripts/install_specification.py",
    "catalog/skills.json",
    "README.md",
    "docs/getting-started.md",
    "docs/extending.md",
    "docs/decisions/TEMPLATE.md",
    "docs/decisions/0005-pinned-skill-installation.md",
    "docs/decisions/0006-risk-based-testing-and-review.md",
    "THIRD_PARTY_NOTICES.md",
    "CHANGELOG.md",
]
CORE_IDS = {
    "project-structure",
    "systematic-debugging",
    "testing-strategy",
    "verification-before-completion",
    "code-review-and-quality",
}
PACK_IDS = {"frontend", "backend", "database", "ai", "vercel-ai-sdk"}
errors = []

for relative in REQUIRED_FILES:
    if not (ROOT / relative).is_file():
        errors.append(f"Missing required file: {relative}")

catalog_path = ROOT / "catalog" / "skills.json"
catalog = None
if catalog_path.is_file():
    try:
        catalog = json.loads(catalog_path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError) as exc:
        errors.append(f"Invalid catalog/skills.json: {exc}")

if catalog is not None:
    if catalog.get("schema_version") != 1:
        errors.append("Catalog schema_version must be 1")
    installer = catalog.get("installer", {})
    if installer.get("package") != "skills" or installer.get("version") != CLI_VERSION:
        errors.append(f"Catalog installer must match pinned Skills CLI {CLI_VERSION}")
    core = catalog.get("core", [])
    core_ids = {skill.get("id") for skill in core}
    if core_ids != CORE_IDS or len(core) != len(CORE_IDS):
        errors.append(f"Core catalog must contain exactly these five skills: {sorted(CORE_IDS)}")
    if set(catalog.get("packs", {})) != PACK_IDS:
        errors.append(f"Optional packs must be exactly: {sorted(PACK_IDS)}")

    all_skills = list(core)
    for pack_name, pack in catalog.get("packs", {}).items():
        if not pack.get("when") or not pack.get("dependencies") or not pack.get("configuration") or not pack.get("limitations"):
            errors.append(f"Pack {pack_name} needs a use case, dependencies, configuration, and limitations")
        pack_skills = pack.get("skills", [])
        if not pack_skills:
            errors.append(f"Pack {pack_name} has no concrete skill or documented local practice")
        all_skills.extend(pack_skills)

    specification_dependency = catalog.get("specification_dependency", {})
    if specification_dependency.get("id") != "interview-me":
        errors.append("The global specification dependency must be upstream interview-me")
    all_skills.append(specification_dependency)

    seen = set()
    for skill in all_skills:
        skill_id = skill.get("id")
        if not skill_id or skill_id in seen:
            errors.append(f"Missing or duplicate skill id: {skill_id!r}")
        seen.add(skill_id)
        if skill.get("kind") == "local":
            source = skill.get("path")
            if not source or not (ROOT / source / "SKILL.md").is_file():
                errors.append(f"Local skill {skill_id} has no source SKILL.md")
            targets = skill.get("targets", {})
            if not targets.get("codex") or not targets.get("hermes"):
                errors.append(f"Local skill {skill_id} needs Codex and Hermes target paths")
            continue
        for field in ("repository", "source_url", "revision", "skill_path", "license", "license_checked"):
            if not skill.get(field):
                errors.append(f"Upstream skill {skill_id} is missing {field}")
        source_url = skill.get("source_url", "")
        parsed = urlparse(source_url)
        parts = [part for part in parsed.path.split("/") if part]
        if parsed.netloc == "github.com" and "tree" in parts:
            ref_index = parts.index("tree") + 1
            ref = parts[ref_index] if ref_index < len(parts) else ""
            if not re.fullmatch(r"[0-9a-f]{40}", ref):
                errors.append(f"Upstream skill {skill_id} must use a full, pinned commit URL")
            if ref and ref not in skill.get("revision", ""):
                errors.append(f"Upstream skill {skill_id} revision does not match its source URL")
        elif parsed.netloc == "raw.githubusercontent.com":
            revision = parts[2] if len(parts) > 2 else ""
            if not re.fullmatch(r"[0-9a-f]{40}", revision):
                errors.append(f"Upstream skill {skill_id} raw URL must pin a full commit SHA")
            if revision and revision not in skill.get("revision", ""):
                errors.append(f"Upstream skill {skill_id} revision does not match its raw source URL")
        else:
            errors.append(f"Upstream skill {skill_id} has an unsupported or unpinned source URL")

    if set(skill["id"] for skill in core if skill.get("kind") == "upstream") != {
        "systematic-debugging",
        "verification-before-completion",
        "code-review-and-quality",
    }:
        errors.append("The three upstream core skills do not match the agreed implementation capabilities")

for skill in (ROOT / "skills").glob("*/SKILL.md"):
    content = skill.read_text(encoding="utf-8")
    if not content.startswith("---\n") or "\nname:" not in content or "\ndescription:" not in content:
        errors.append(f"Invalid skill frontmatter: {skill.relative_to(ROOT)}")

if (ROOT / "starter/.agents/skills/project-structure/SKILL.md").exists():
    errors.append("Duplicate project-structure source found under starter/; maintain skills/project-structure as the sole source")

starter_policy = (ROOT / "starter/AGENTS.md").read_text(encoding="utf-8")
for required in ("Discussion", "Implement issue", "Direct change", "consequential", "proportionate self-check"):
    if required.lower() not in starter_policy.lower():
        errors.append(f"Generated AGENTS.md is missing conditional-workflow guidance: {required}")
product_skill = (ROOT / "skills/product-specification/SKILL.md").read_text(encoding="utf-8")
for required in ("interview-me", "explicit approval", "Linear", "fallback"):
    if required.lower() not in product_skill.lower():
        errors.append(f"Product specification skill is missing its contract: {required}")

if errors:
    for error in errors:
        print("ERROR:", error)
    sys.exit(1)

skill_count = sum(1 for _ in (ROOT / "skills").glob("*/SKILL.md"))
print(f"Validation passed ({len(REQUIRED_FILES)} required files; {skill_count} local skills; {len(CORE_IDS)} core capabilities; {len(PACK_IDS)} optional packs).")

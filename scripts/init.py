#!/usr/bin/env python3
"""Initialize a project with local guidance and pinned, selected agent skills."""
import argparse
import copy
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
STARTER = ROOT / "starter"
CATALOG_PATH = ROOT / "catalog" / "skills.json"

try:  # Supports both direct script execution and tests importing scripts/init.py.
    from skill_installer import copy_missing, install_skill, runtime_skills_directory
except ImportError:  # pragma: no cover - package-style invocation fallback
    from .skill_installer import copy_missing, install_skill, runtime_skills_directory


def read_catalog():
    return json.loads(CATALOG_PATH.read_text(encoding="utf-8"))


def _copy_plan(source, destination, relative=Path("")):
    """List missing files without creating directories or modifying the target."""
    operations = []
    for item in sorted(source.iterdir()):
        target = destination / item.name
        item_relative = relative / item.name
        if item.is_dir():
            operations.extend(_copy_plan(item, target, item_relative))
        elif target.exists():
            operations.append(("SKIP", str(item_relative)))
        else:
            operations.append(("COPY", str(item_relative)))
    return operations


def _copy_source(source, destination, relative, dry_run):
    if dry_run:
        return _copy_plan(source, destination, relative)
    return copy_missing(source, destination, relative)


def _lock_entry(catalog, runtime, skill):
    entry = {
        "id": skill["id"],
        "kind": skill["kind"],
        "revision": skill["revision"] if skill["kind"] == "upstream" else catalog["starter_version"],
        "license": skill["license"],
        "target": skill.get("targets", {}).get(runtime, f"{runtime_skills_directory(runtime)}/{skill['id']}"),
    }
    if skill["kind"] == "upstream":
        entry.update({
            "repository": skill["repository"],
            "source_url": skill["source_url"],
            "skill_path": skill["skill_path"],
            "installer_skill": skill.get("installer_skill"),
            "installer_version": catalog["installer"]["version"],
        })
    else:
        entry["source_path"] = skill["path"]
    return entry


def _read_lock(path):
    if not path.exists():
        return None, None
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError) as exc:
        return None, f"Existing starter-skills.lock.json could not be read: {exc}"
    if not isinstance(data, dict) or data.get("format_version") != 1 or not isinstance(data.get("runtimes"), dict):
        return None, "Existing starter-skills.lock.json has an unsupported format; preserved it and skipped upstream installs."
    for runtime_data in data["runtimes"].values():
        if not isinstance(runtime_data, dict) or not isinstance(runtime_data.get("skills"), list):
            return None, "Existing starter-skills.lock.json has an invalid runtime entry; preserved it and skipped upstream installs."
        if any(not isinstance(entry, dict) or not entry.get("id") for entry in runtime_data["skills"]):
            return None, "Existing starter-skills.lock.json has an invalid skill entry; preserved it and skipped upstream installs."
    return data, None


def _locked_skill(lock, runtime, skill_id):
    if lock is None:
        return None
    runtime_order = [runtime] + [name for name in lock["runtimes"] if name != runtime]
    for runtime_name in runtime_order:
        runtime_data = lock["runtimes"].get(runtime_name, {})
        for entry in runtime_data.get("skills", []):
            if entry.get("id") == skill_id:
                return entry
    return None


def _apply_locked_source(skill, locked_entry):
    if locked_entry is None or skill["kind"] != "upstream":
        return skill
    resolved = dict(skill)
    for key in ("revision", "repository", "source_url", "skill_path", "installer_skill", "installer_version", "license"):
        if key in locked_entry:
            resolved[key] = locked_entry[key]
    return resolved


def _merged_lock(catalog, runtime, selected, existing):
    lock = copy.deepcopy(existing) if existing is not None else {
        "format_version": 1,
        "starter_version": catalog["starter_version"],
        "runtimes": {},
    }
    runtime_data = lock["runtimes"].setdefault(runtime, {"skills": []})
    if not isinstance(runtime_data, dict) or not isinstance(runtime_data.get("skills"), list):
        raise ValueError(f"Existing lock has an invalid skills list for runtime {runtime}")
    present = {entry.get("id") for entry in runtime_data["skills"] if isinstance(entry, dict)}
    added = False
    for skill in selected:
        if skill["id"] in present:
            continue
        prior = _locked_skill(lock, runtime, skill["id"])
        entry = copy.deepcopy(prior) if prior else _lock_entry(catalog, runtime, skill)
        entry["target"] = skill.get("targets", {}).get(runtime, f"{runtime_skills_directory(runtime)}/{skill['id']}")
        runtime_data["skills"].append(entry)
        present.add(skill["id"])
        added = True
    return lock, added


def initialize(destination, dry_run=False, packs=None, runtime="codex", installer=install_skill):
    """Copy starter files and install selected skills without overwriting content.

    Returns (operations, errors). Existing files are preserved; only the generated
    lockfile is merged to record newly requested skills.
    """
    destination = Path(destination).expanduser().resolve()
    if destination == ROOT or ROOT in destination.parents:
        raise ValueError("Destination must not be inside the starter repository")
    if destination.exists() and not destination.is_dir():
        raise ValueError("Destination exists and is not a directory")
    if runtime not in {"codex", "hermes"}:
        raise ValueError(f"Unsupported runtime: {runtime}")

    catalog = read_catalog()
    selected_packs = list(dict.fromkeys(packs or []))
    unknown_packs = sorted(set(selected_packs) - set(catalog["packs"]))
    if unknown_packs:
        raise ValueError(f"Unknown optional pack(s): {', '.join(unknown_packs)}")

    operations = _copy_source(STARTER, destination, Path(""), dry_run)
    selected_skills = list(catalog["core"])
    for pack_name in selected_packs:
        selected_skills.extend(catalog["packs"][pack_name]["skills"])

    errors = []
    lock_path = destination / "starter-skills.lock.json"
    lock, lock_error = _read_lock(lock_path)
    if lock_error:
        errors.append(lock_error)

    for skill in selected_skills:
        if skill["kind"] != "local":
            continue
        source = ROOT / skill["path"]
        target_relative = skill["targets"][runtime]
        target = destination / target_relative
        operations.extend(_copy_source(source, target, Path(target_relative), dry_run))

    for skill in selected_skills:
        if skill["kind"] != "upstream":
            continue
        if lock_error:
            continue
        skill_to_install = _apply_locked_source(skill, _locked_skill(lock, runtime, skill["id"]))
        skill_operations, error = installer(
            skill_to_install,
            runtime,
            destination / runtime_skills_directory(runtime),
            dry_run=dry_run,
        )
        operations.extend(skill_operations)
        if error:
            errors.append(error)

    if not lock_error:
        try:
            merged_lock, changed = _merged_lock(catalog, runtime, selected_skills, lock)
        except ValueError as exc:
            errors.append(str(exc))
            changed = False
            merged_lock = lock
        if changed:
            action = "UPDATE" if lock is not None else "WRITE"
            if not dry_run:
                lock_path.parent.mkdir(parents=True, exist_ok=True)
                lock_path.write_text(json.dumps(merged_lock, indent=2) + "\n", encoding="utf-8")
            operations.append((action, "starter-skills.lock.json"))
        else:
            operations.append(("SKIP", "starter-skills.lock.json"))
    else:
        operations.append(("SKIP", "starter-skills.lock.json"))

    return operations, errors


def main(argv=None):
    catalog = read_catalog()
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("destination", type=Path)
    parser.add_argument("--pack", action="append", choices=sorted(catalog["packs"]), default=[])
    parser.add_argument("--runtime", choices=("codex", "hermes"), default="codex")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args(argv)
    try:
        operations, errors = initialize(
            args.destination,
            dry_run=args.dry_run,
            packs=args.pack,
            runtime=args.runtime,
        )
    except ValueError as exc:
        parser.error(str(exc))

    for action, path in operations:
        print(f"{action}: {path}")
    for error in errors:
        print(f"ERROR: {error}", file=sys.stderr)
    if args.runtime == "hermes":
        print("Hermes: initialize a Git repository, then explicitly trust it with `hermes skills trust /path/to/project`.")
    print("Edit the generated AGENTS.md placeholders and configure checks for the actual stack.")
    if errors:
        print(f"Initialization incomplete: {len(errors)} skill installation(s) failed.", file=sys.stderr)
        return 1
    print("Initialization complete." if not args.dry_run else "Dry run complete; destination was not modified.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

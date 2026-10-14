#!/usr/bin/env python3
"""Install global product-specification and its pinned interview dependency."""
import argparse
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
CATALOG_PATH = ROOT / "catalog" / "skills.json"
try:
    from skill_installer import copy_missing, install_skill, RUNTIME_GLOBAL_DIRECTORY
except ImportError:  # pragma: no cover
    from .skill_installer import copy_missing, install_skill, RUNTIME_GLOBAL_DIRECTORY


def _copy_plan(source, destination, relative=Path("")):
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


def install_specification(runtime="codex", dry_run=False, installer=install_skill, home=None):
    if runtime not in {"codex", "hermes"}:
        raise ValueError(f"Unsupported runtime: {runtime}")
    catalog = json.loads(CATALOG_PATH.read_text(encoding="utf-8"))
    dependency = catalog["specification_dependency"]
    home = Path(home).expanduser() if home is not None else Path.home()
    base = home / RUNTIME_GLOBAL_DIRECTORY[runtime]
    operations = []
    errors = []

    dependency_operations, error = installer(
        dependency,
        runtime,
        base,
        dry_run=dry_run,
        display_prefix=str(base),
    )
    operations.extend(dependency_operations)
    if error:
        errors.append(error)

    product_source = ROOT / "skills" / "product-specification"
    product_target = base / "product-specification"
    if dry_run:
        operations.extend(_copy_plan(product_source, product_target, Path(str(base)) / "product-specification"))
    else:
        operations.extend(copy_missing(product_source, product_target, Path(str(base)) / "product-specification"))
    return operations, errors, base


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--runtime", choices=("codex", "hermes"), default="codex")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args(argv)
    try:
        operations, errors, destination = install_specification(args.runtime, args.dry_run)
    except ValueError as exc:
        parser.error(str(exc))
    for action, path in operations:
        print(f"{action}: {path}")
    for error in errors:
        print(f"ERROR: {error}", file=sys.stderr)
    print(f"Global skills directory: {destination}")
    if errors:
        print("Specification installation incomplete.", file=sys.stderr)
        return 1
    print("Dry run complete; no files were changed." if args.dry_run else "Global specification skills installed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

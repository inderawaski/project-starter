#!/usr/bin/env python3
"""Copy safe starter files into a project without overwriting existing content."""
import argparse
from pathlib import Path
import shutil

ROOT = Path(__file__).resolve().parents[1]
STARTER = ROOT / "starter"
PACKS = ("frontend", "backend", "database", "ai")

def initialize(destination: Path, dry_run: bool = False):
    destination = destination.resolve()
    if destination == ROOT or ROOT in destination.parents:
        raise ValueError("Destination must not be inside the starter repository")
    operations = []
    for source in sorted(STARTER.rglob("*")):
        if not source.is_file():
            continue
        relative = source.relative_to(STARTER)
        target = destination / relative
        if target.exists():
            operations.append(("SKIP", str(relative)))
            continue
        operations.append(("COPY", str(relative)))
        if not dry_run:
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source, target)
    return operations

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("destination", type=Path)
    parser.add_argument("--pack", action="append", choices=PACKS, default=[])
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    try:
        operations = initialize(args.destination, args.dry_run)
    except ValueError as exc:
        parser.error(str(exc))
    for action, path in operations:
        print(f"{action}: {path}")
    print("\nCore upstream skills: see catalog/core.yaml. Install only after reviewing source and license.")
    for pack in dict.fromkeys(args.pack):
        print(f"Optional pack '{pack}': see catalog/{pack}.yaml (recommendations only)")
    print("Edit project AGENTS.md placeholders and configure checks for the actual stack.")

if __name__ == "__main__":
    main()

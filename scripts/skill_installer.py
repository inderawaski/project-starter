"""Install one pinned skill into a supplied skills directory via Vercel Skills CLI."""
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

CLI_VERSION = "1.7.2"
TIMEOUT_SECONDS = 180
RUNTIME_AGENT = {"codex": "codex", "hermes": "hermes-agent"}
RUNTIME_SKILLS_DIRECTORY = {"codex": ".agents/skills", "hermes": ".hermes/skills"}
RUNTIME_GLOBAL_DIRECTORY = {"codex": ".agents/skills", "hermes": ".hermes/skills"}


def runtime_skills_directory(runtime):
    if runtime not in RUNTIME_SKILLS_DIRECTORY:
        raise ValueError(f"Unsupported runtime: {runtime}")
    return RUNTIME_SKILLS_DIRECTORY[runtime]


def cli_command(skill, runtime):
    """Build a non-interactive CLI command for a catalog skill."""
    if runtime not in RUNTIME_AGENT:
        raise ValueError(f"Unsupported runtime: {runtime}")
    version = skill.get("installer_version", CLI_VERSION)
    command = ["npx", "--yes", f"skills@{version}", "add", skill["source_url"]]
    installer_skill = skill.get("installer_skill")
    if installer_skill:
        command.extend(["--skill", installer_skill])
    command.extend(["--agent", RUNTIME_AGENT[runtime], "--copy", "--yes"])
    return command


def _contains_files(directory):
    for item in directory.iterdir():
        if item.is_file() or (item.is_dir() and _contains_files(item)):
            return True
    return False


def copy_missing(source, destination, relative=Path("")):
    """Copy absent files, keeping every existing destination file intact."""
    operations = []
    if not _contains_files(source):
        return operations
    items = sorted(source.iterdir())
    destination.mkdir(parents=True, exist_ok=True)
    for item in items:
        target = destination / item.name
        item_relative = relative / item.name
        if item.is_dir():
            operations.extend(copy_missing(item, target, item_relative))
        elif target.exists():
            operations.append(("SKIP", str(item_relative)))
        else:
            shutil.copy2(item, target)
            operations.append(("COPY", str(item_relative)))
    return operations


def install_skill(
    skill,
    runtime,
    skills_directory,
    dry_run=False,
    runner=subprocess.run,
    display_prefix=None,
):
    """Install and verify one upstream skill; return (operations, error)."""
    skills_directory = Path(skills_directory)
    skill_target = skills_directory / skill["id"]
    display_prefix = display_prefix or runtime_skills_directory(runtime)
    label = f"{display_prefix}/{skill['id']}"
    if (skill_target / "SKILL.md").is_file():
        return [("SKIP", label)], None

    command = cli_command(skill, runtime)
    if dry_run:
        return [("INSTALL", " ".join(command))], None

    try:
        print(f"Installing {skill['id']} from {skill['source_url']}", file=sys.stderr, flush=True)
        with tempfile.TemporaryDirectory(prefix="project-starter-skill-") as temporary:
            staging = Path(temporary)
            result = runner(command, cwd=staging, capture_output=True, text=True, timeout=TIMEOUT_SECONDS)
            if result.returncode:
                details = (result.stderr or result.stdout or "no installer output").strip()
                return [], f"{skill['id']}: Skills CLI failed (exit {result.returncode}): {details}"

            staged_skill = staging / runtime_skills_directory(runtime) / skill["id"]
            if not (staged_skill / "SKILL.md").is_file():
                return [], f"{skill['id']}: Skills CLI succeeded but did not produce {skill['id']}/SKILL.md"

            operations = copy_missing(staged_skill, skill_target)
            if not (skill_target / "SKILL.md").is_file():
                return operations, f"{skill['id']}: installed skill is not discoverable at {skill_target}"
            operations.insert(0, ("INSTALL", label))
            return operations, None
    except FileNotFoundError as exc:
        return [], f"{skill['id']}: could not start Skills CLI: {exc}"
    except subprocess.TimeoutExpired:
        return [], f"{skill['id']}: Skills CLI timed out after {TIMEOUT_SECONDS} seconds"
    except OSError as exc:
        return [], f"{skill['id']}: install failed: {exc}"

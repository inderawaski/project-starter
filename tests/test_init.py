import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from init import ROOT, initialize, main
from install_specification import install_specification
from skill_installer import CLI_VERSION, cli_command, install_skill


def simulated_installer(skill, runtime, skills_directory, dry_run=False, display_prefix=".agents/skills"):
    target = Path(skills_directory) / skill["id"]
    if (target / "SKILL.md").is_file():
        return [("SKIP", f"{display_prefix}/{skill['id']}")], None
    if dry_run:
        return [("INSTALL", "simulated")], None
    target.mkdir(parents=True, exist_ok=True)
    (target / "SKILL.md").write_text(f"name: {skill['id']}\n")
    return [("INSTALL", f"{display_prefix}/{skill['id']}")], None


class InitTests(unittest.TestCase):
    def test_fresh_project_gets_local_and_upstream_core_skills(self):
        with tempfile.TemporaryDirectory() as temporary:
            destination = Path(temporary) / "app"
            operations, errors = initialize(destination, installer=simulated_installer)

            self.assertEqual(errors, [])
            self.assertTrue((destination / "AGENTS.md").is_file())
            self.assertTrue((destination / ".agents/references/architecture-principles.md").is_file())
            for name in (
                "project-structure",
                "systematic-debugging",
                "testing-strategy",
                "verification-before-completion",
                "code-review-and-quality",
            ):
                self.assertTrue((destination / f".agents/skills/{name}/SKILL.md").is_file(), name)
            lock = json.loads((destination / "starter-skills.lock.json").read_text())
            self.assertEqual(len(lock["runtimes"]["codex"]["skills"]), 5)
            self.assertIn(("WRITE", "starter-skills.lock.json"), operations)

    def test_hermes_project_installs_to_native_project_skill_directory(self):
        with tempfile.TemporaryDirectory() as temporary:
            destination = Path(temporary) / "app"
            _, errors = initialize(destination, runtime="hermes", installer=simulated_installer)
            self.assertEqual(errors, [])
            for name in (
                "project-structure",
                "systematic-debugging",
                "testing-strategy",
                "verification-before-completion",
                "code-review-and-quality",
            ):
                self.assertTrue((destination / f".hermes/skills/{name}/SKILL.md").is_file(), name)
            self.assertFalse((destination / ".agents/skills").exists())

    def test_existing_files_are_not_overwritten(self):
        with tempfile.TemporaryDirectory() as temporary:
            destination = Path(temporary) / "app"
            destination.mkdir()
            (destination / "AGENTS.md").write_text("custom instructions")
            existing_skill = destination / ".agents/skills/systematic-debugging"
            existing_skill.mkdir(parents=True)
            (existing_skill / "SKILL.md").write_text("custom skill")

            operations, errors = initialize(destination, installer=simulated_installer)

            self.assertEqual(errors, [])
            self.assertEqual((destination / "AGENTS.md").read_text(), "custom instructions")
            self.assertEqual((existing_skill / "SKILL.md").read_text(), "custom skill")
            self.assertIn(("SKIP", "AGENTS.md"), operations)
            self.assertIn(("SKIP", ".agents/skills/systematic-debugging"), operations)

    def test_dry_run_does_not_modify_or_create_destination(self):
        with tempfile.TemporaryDirectory() as temporary:
            destination = Path(temporary) / "app"
            operations, errors = initialize(
                destination,
                dry_run=True,
                packs=["frontend"],
            )
            self.assertFalse(destination.exists())
            self.assertEqual(errors, [])
            self.assertIn(("WRITE", "starter-skills.lock.json"), operations)
            self.assertTrue(any("frontend-ui-engineering" in path for _, path in operations))

    def test_cli_dry_run_reports_pinned_install_commands_without_network(self):
        with tempfile.TemporaryDirectory() as temporary:
            destination = Path(temporary) / "app"
            result = main([str(destination), "--runtime", "hermes", "--dry-run"])
            self.assertEqual(result, 0)
            self.assertFalse(destination.exists())

    def test_optional_skills_are_added_only_for_selected_pack(self):
        with tempfile.TemporaryDirectory() as temporary:
            destination = Path(temporary) / "app"
            selected = []

            def recording_installer(skill, runtime, skills_directory, dry_run=False, display_prefix=".agents/skills"):
                selected.append(skill["id"])
                return simulated_installer(skill, runtime, skills_directory, dry_run, display_prefix)

            initialize(destination, packs=["backend", "backend"], installer=recording_installer)
            self.assertIn("api-and-interface-design", selected)
            self.assertNotIn("frontend-ui-engineering", selected)
            self.assertEqual(selected.count("api-and-interface-design"), 1)

    def test_selected_pack_is_recorded_in_lock(self):
        with tempfile.TemporaryDirectory() as temporary:
            destination = Path(temporary) / "app"
            initialize(destination, packs=["ai"], installer=simulated_installer)
            lock = json.loads((destination / "starter-skills.lock.json").read_text())
            self.assertIn("ai-product-practices", [skill["id"] for skill in lock["runtimes"]["codex"]["skills"]])
            self.assertTrue((destination / ".agents/skills/ai-product-practices/SKILL.md").is_file())

    def test_vercel_ai_sdk_pack_is_separate_and_opt_in(self):
        with tempfile.TemporaryDirectory() as temporary:
            destination = Path(temporary) / "app"
            initialize(destination, packs=["vercel-ai-sdk"], installer=simulated_installer)
            lock = json.loads((destination / "starter-skills.lock.json").read_text())
            ids = [skill["id"] for skill in lock["runtimes"]["codex"]["skills"]]
            self.assertIn("ai-sdk", ids)
            self.assertNotIn("ai-product-practices", ids)
            self.assertTrue((destination / ".agents/skills/ai-sdk/SKILL.md").is_file())

    def test_repeated_initialization_merges_new_pack_without_changing_existing_pins(self):
        with tempfile.TemporaryDirectory() as temporary:
            destination = Path(temporary) / "app"
            initialize(destination, installer=simulated_installer)
            lock_path = destination / "starter-skills.lock.json"
            original_lock = json.loads(lock_path.read_text())
            core_entry = original_lock["runtimes"]["codex"]["skills"][1]
            core_entry["user_note"] = "keep this metadata"
            lock_path.write_text(json.dumps(original_lock))
            (destination / "AGENTS.md").write_text("user-edited instructions")
            operations, errors = initialize(destination, packs=["frontend"], installer=simulated_installer)
            self.assertEqual(errors, [])
            updated_lock = json.loads(lock_path.read_text())
            entries = updated_lock["runtimes"]["codex"]["skills"]
            self.assertIn("frontend-ui-engineering", [entry["id"] for entry in entries])
            self.assertEqual(
                next(entry for entry in entries if entry["id"] == core_entry["id"])["user_note"],
                "keep this metadata",
            )
            self.assertIn(("UPDATE", "starter-skills.lock.json"), operations)
            self.assertEqual((destination / "AGENTS.md").read_text(), "user-edited instructions")
            self.assertTrue((destination / ".agents/skills/frontend-ui-engineering/SKILL.md").exists())

    def test_existing_lock_pins_are_reused_if_catalog_revision_changes(self):
        with tempfile.TemporaryDirectory() as temporary:
            destination = Path(temporary) / "app"
            initialize(destination, installer=simulated_installer)
            skill_dir = destination / ".agents/skills/systematic-debugging"
            (skill_dir / "SKILL.md").unlink()
            changed = json.loads((ROOT / "catalog/skills.json").read_text())
            changed_skill = next(skill for skill in changed["core"] if skill["id"] == "systematic-debugging")
            changed_skill["source_url"] = "https://github.com/obra/superpowers/tree/unreviewed"
            changed_skill["revision"] = "unreviewed"
            changed["installer"]["version"] = "9.9.9"
            seen = []

            def recording_installer(skill, runtime, skills_directory, dry_run=False, display_prefix=None):
                if skill["id"] == "systematic-debugging":
                    seen.append((skill["source_url"], skill["installer_version"]))
                return simulated_installer(
                    skill,
                    runtime,
                    skills_directory,
                    dry_run,
                    display_prefix or ".agents/skills",
                )

            with patch("init.read_catalog", return_value=changed):
                initialize(destination, installer=recording_installer)
            lock = json.loads((destination / "starter-skills.lock.json").read_text())
            original = next(
                entry for entry in lock["runtimes"]["codex"]["skills"]
                if entry["id"] == "systematic-debugging"
            )
            self.assertEqual(seen, [(original["source_url"], original["installer_version"])])
            self.assertNotEqual(seen[0][0], changed_skill["source_url"])
            self.assertNotEqual(seen[0][1], changed["installer"]["version"])

    def test_unrecognized_existing_lock_is_preserved_and_reported(self):
        with tempfile.TemporaryDirectory() as temporary:
            destination = Path(temporary) / "app"
            destination.mkdir()
            lock = destination / "starter-skills.lock.json"
            lock.write_text("user-owned lock")
            operations, errors = initialize(destination, installer=simulated_installer)
            self.assertTrue(any("could not be read" in error for error in errors))
            self.assertEqual(lock.read_text(), "user-owned lock")
            self.assertFalse((destination / ".agents/skills/systematic-debugging/SKILL.md").exists())
            self.assertTrue((destination / ".agents/skills/testing-strategy/SKILL.md").exists())
            self.assertIn(("SKIP", "starter-skills.lock.json"), operations)

    def test_install_failure_is_returned_and_partial_local_setup_remains(self):
        with tempfile.TemporaryDirectory() as temporary:
            destination = Path(temporary) / "app"

            def failed_installer(skill, runtime, skills_directory, dry_run=False, display_prefix=".agents/skills"):
                return [], f"{skill['id']}: simulated download failure"

            _, errors = initialize(destination, installer=failed_installer)
            self.assertTrue(errors)
            self.assertIn("systematic-debugging", errors[0])
            self.assertTrue((destination / ".agents/skills/testing-strategy/SKILL.md").is_file())
            self.assertTrue((destination / "starter-skills.lock.json").is_file())

    def test_skills_cli_command_is_versioned_and_runtime_specific(self):
        skill = {
            "id": "systematic-debugging",
            "source_url": "https://github.com/obra/superpowers/tree/v7.0.0",
            "installer_skill": "systematic-debugging",
        }
        codex_command = cli_command(skill, "codex")
        hermes_command = cli_command(skill, "hermes")
        self.assertEqual(CLI_VERSION, "1.7.2")
        self.assertIn("skills@1.7.2", codex_command)
        self.assertEqual(codex_command[codex_command.index("--agent") + 1], "codex")
        self.assertEqual(hermes_command[hermes_command.index("--agent") + 1], "hermes-agent")
        self.assertIn("--copy", codex_command)
        self.assertIn("--yes", codex_command)
        pinned = dict(skill, installer_version="1.6.0")
        self.assertIn("skills@1.6.0", cli_command(pinned, "codex"))

    def test_global_specification_installs_entry_point_and_interview_skill(self):
        with tempfile.TemporaryDirectory() as temporary:
            home = Path(temporary)
            _, errors, destination = install_specification(
                "codex", installer=simulated_installer, home=home
            )
            self.assertEqual(errors, [])
            self.assertEqual(destination, home / ".agents/skills")
            self.assertTrue((destination / "product-specification/SKILL.md").is_file())
            self.assertTrue((destination / "product-specification/references/interviewing.md").is_file())
            self.assertTrue((destination / "interview-me/SKILL.md").is_file())

    def test_global_specification_uses_hermes_directory_and_preserves_existing(self):
        with tempfile.TemporaryDirectory() as temporary:
            home = Path(temporary)
            destination = home / ".hermes/skills"
            product = destination / "product-specification"
            product.mkdir(parents=True)
            (product / "SKILL.md").write_text("user version")
            operations, errors, actual = install_specification(
                "hermes", installer=simulated_installer, home=home
            )
            self.assertEqual(errors, [])
            self.assertEqual(actual, destination)
            self.assertEqual((product / "SKILL.md").read_text(), "user version")
            self.assertTrue((destination / "interview-me/SKILL.md").is_file())
            self.assertIn(("SKIP", str(destination / "product-specification/SKILL.md")), operations)

    def test_pinned_install_verifies_and_copies_cli_output(self):
        skill = {
            "id": "systematic-debugging",
            "source_url": "https://github.com/obra/superpowers/tree/v7.0.0",
            "installer_skill": "systematic-debugging",
        }
        with tempfile.TemporaryDirectory() as temporary:
            destination = Path(temporary) / ".agents" / "skills"

            def runner(command, cwd, **kwargs):
                staged = Path(cwd) / ".agents" / "skills" / skill["id"]
                staged.mkdir(parents=True)
                (staged / "SKILL.md").write_text("upstream skill")
                return subprocess.CompletedProcess(command, 0, "installed", "")

            operations, error = install_skill(skill, "codex", destination, runner=runner)
            self.assertIsNone(error)
            self.assertEqual((destination / skill["id"] / "SKILL.md").read_text(), "upstream skill")
            self.assertIn(("INSTALL", ".agents/skills/systematic-debugging"), operations)

    def test_hermes_install_verifies_native_cli_output(self):
        skill = {
            "id": "systematic-debugging",
            "source_url": "https://github.com/obra/superpowers/tree/v7.0.0",
            "installer_skill": "systematic-debugging",
        }
        with tempfile.TemporaryDirectory() as temporary:
            destination = Path(temporary) / ".hermes" / "skills"

            def runner(command, cwd, **kwargs):
                self.assertEqual(command[command.index("--agent") + 1], "hermes-agent")
                staged = Path(cwd) / ".hermes" / "skills" / skill["id"]
                staged.mkdir(parents=True)
                (staged / "SKILL.md").write_text("upstream skill")
                return subprocess.CompletedProcess(command, 0, "installed", "")

            operations, error = install_skill(
                skill,
                "hermes",
                destination,
                runner=runner,
            )
            self.assertIsNone(error)
            self.assertEqual((destination / skill["id"] / "SKILL.md").read_text(), "upstream skill")
            self.assertIn(("INSTALL", ".hermes/skills/systematic-debugging"), operations)

    def test_pinned_install_reports_cli_failure_and_missing_output(self):
        skill = {
            "id": "systematic-debugging",
            "source_url": "https://github.com/obra/superpowers/tree/v7.0.0",
            "installer_skill": "systematic-debugging",
        }
        with tempfile.TemporaryDirectory() as temporary:
            destination = Path(temporary) / ".agents" / "skills"

            def failed_runner(command, cwd, **kwargs):
                return subprocess.CompletedProcess(command, 1, "", "network unavailable")

            _, error = install_skill(skill, "codex", destination, runner=failed_runner)
            self.assertIn("network unavailable", error)
            self.assertFalse(destination.exists())

            def empty_runner(command, cwd, **kwargs):
                return subprocess.CompletedProcess(command, 0, "success", "")

            _, error = install_skill(skill, "codex", destination, runner=empty_runner)
            self.assertIn("did not produce", error)

    def test_rejects_invalid_destinations(self):
        with self.assertRaises(ValueError):
            initialize(ROOT / "temporary-project")
        with tempfile.TemporaryDirectory() as temporary:
            file_path = Path(temporary) / "file"
            file_path.write_text("not a directory")
            with self.assertRaises(ValueError):
                initialize(file_path)


if __name__ == "__main__":
    unittest.main()

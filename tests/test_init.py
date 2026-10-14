import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from init import initialize, ROOT

class InitTests(unittest.TestCase):
    def test_copies_starter_files(self):
        with tempfile.TemporaryDirectory() as temp:
            dest = Path(temp) / "app"
            actions = initialize(dest)
            self.assertTrue((dest / "AGENTS.md").exists())
            self.assertTrue((dest / ".agents/skills/project-structure/SKILL.md").exists())
            self.assertIn(("COPY", "AGENTS.md"), actions)

    def test_does_not_overwrite(self):
        with tempfile.TemporaryDirectory() as temp:
            dest = Path(temp)
            (dest / "AGENTS.md").write_text("custom")
            actions = initialize(dest)
            self.assertEqual((dest / "AGENTS.md").read_text(), "custom")
            self.assertIn(("SKIP", "AGENTS.md"), actions)

    def test_dry_run_does_not_write(self):
        with tempfile.TemporaryDirectory() as temp:
            dest = Path(temp) / "app"
            initialize(dest, dry_run=True)
            self.assertFalse(dest.exists())

    def test_rejects_nested_destination(self):
        with self.assertRaises(ValueError):
            initialize(ROOT / "temporary-project")

if __name__ == "__main__":
    unittest.main()

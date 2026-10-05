import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from prepare_project import ROOT, prepare


class StandaloneProjectTest(unittest.TestCase):
    def setUp(self):
        self.folder = tempfile.TemporaryDirectory()
        self.addCleanup(self.folder.cleanup)
        self.output = Path(self.folder.name)

    def test_api_lab_is_reachable_through_the_public_preparation_command(self):
        result = subprocess.run([sys.executable, "-B", str(ROOT / "suite-support/prepare_project.py"),
                                 "--project", "api-lab", "--output", str(self.output / "api")],
                                capture_output=True, text=True)
        self.assertEqual(0, result.returncode, result.stderr)
        self.assertTrue((self.output / "api/schema/echo.pb").is_file())

    def test_each_shipped_lab_has_an_isolated_clean_git_baseline(self):
        for name in ("first-result", "workspace", "api-lab", "mobile-lab", "runtime-evidence", "kafka-profile-lab"):
            with self.subTest(project=name):
                result = prepare(name, self.output / name)
                root = Path(result["project"])
                self.assertEqual("", subprocess.check_output(["git", "status", "--porcelain"], cwd=root, text=True))
                self.assertEqual(result["baseline"], subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=root, text=True).strip())
                self.assertEqual((ROOT / "projects" / name / "README.md").read_bytes(), (root / "README.md").read_bytes())
                with self.assertRaisesRegex(ValueError, "overwrite"):
                    prepare(name, root)

    def test_invalid_project_cannot_escape_the_lab_root(self):
        for name in ("../suite-support", "..", "missing", str(ROOT / "projects/api-lab")):
            with self.subTest(name=name), self.assertRaises(ValueError):
                prepare(name, self.output / "escaped")
        self.assertFalse((self.output / "escaped").exists())


if __name__ == "__main__":
    unittest.main()

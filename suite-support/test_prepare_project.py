import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from prepare_project import ROOT, prepare, retarget_document_links


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
                configuration = ROOT / "projects" / name / ".archflow.yml"
                if configuration.is_file():
                    self.assertEqual(configuration.read_bytes(), (root / ".archflow.yml").read_bytes())
                with self.assertRaisesRegex(ValueError, "overwrite"):
                    prepare(name, root)

    def test_invalid_project_cannot_escape_the_lab_root(self):
        for name in ("../suite-support", "..", "missing", str(ROOT / "projects/api-lab")):
            with self.subTest(name=name), self.assertRaises(ValueError):
                prepare(name, self.output / "escaped")
        self.assertFalse((self.output / "escaped").exists())

    def test_first_result_copy_links_to_the_public_launch_guide_and_article(self):
        result = prepare("first-result", self.output / "first")
        text = (Path(result["project"]) / "README.md").read_text(encoding="utf-8")
        self.assertIn("https://github.com/lMysticl/ArchVerity-Demo/blob/main/docs/DEMO_RUNBOOK_RU.md#", text)
        self.assertIn("https://github.com/lMysticl/ArchVerity-Demo/blob/main/docs/FIRST_RESULT_ARTICLE_RU.md", text)
        self.assertNotIn("](../../docs/", text)
        client = "order-app/src/main/java/demo/orders/PaymentClient.java"
        self.assertEqual((ROOT / "projects/first-result" / client).read_bytes(), (Path(result["project"]) / client).read_bytes())

    def test_local_links_remote_urls_and_code_examples_keep_their_meaning(self):
        source = self.output / "source"
        destination = self.output / "copy"
        source.mkdir(); destination.mkdir()
        text = "[Local](README.md#here)\n[Remote](https://example.test/a?b=1#c)\n```md\n[Example](../../docs/guide.md)\n```\n"
        (source / "README.md").write_text(text, encoding="utf-8")
        (destination / "README.md").write_text(text, encoding="utf-8")
        retarget_document_links(source.resolve(), destination)
        self.assertEqual(text, (destination / "README.md").read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()

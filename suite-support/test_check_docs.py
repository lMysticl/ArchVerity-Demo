import tempfile
import unittest
import shutil
from pathlib import Path

from check_docs import ROOT, check, check_current_product


class DocumentationNavigationTest(unittest.TestCase):
    def setUp(self):
        self.folder = tempfile.TemporaryDirectory()
        self.addCleanup(self.folder.cleanup)
        self.root = Path(self.folder.name)
        (self.root / "docs").mkdir()
        (self.root / "docs/DEMO_RUNBOOK_RU.md").write_text("# Запуск\n\n## Один шаг\n", encoding="utf-8")
        self.home = self.root / "README.md"
        self.home.write_text("[Run](docs/DEMO_RUNBOOK_RU.md#один-шаг)\n", encoding="utf-8")

    def verify(self):
        return check(self.root, navigation=("README.md",))

    def test_linked_runbook_and_unicode_fragment_are_reachable(self):
        self.assertEqual("DOC_NAVIGATION_PASS", self.verify()["status"])

    def test_removed_runbook_navigation_is_a_dead_end(self):
        self.home.write_text("# A screen without a next step\n", encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "not linked"):
            self.verify()

    def test_missing_file_and_missing_fragment_do_not_pass(self):
        for link in ("docs/missing.md", "docs/DEMO_RUNBOOK_RU.md#missing"):
            self.home.write_text(f"[Run]({link})\n", encoding="utf-8")
            with self.subTest(link=link), self.assertRaises(ValueError):
                self.verify()

    def test_url_encoded_unicode_links_and_duplicate_headings(self):
        (self.root / "docs/DEMO_RUNBOOK_RU.md").write_text("# Запуск\n## A\n## A\n", encoding="utf-8")
        self.home.write_text("[Run](docs/DEMO_RUNBOOK_RU.md#%D0%B7%D0%B0%D0%BF%D1%83%D1%81%D0%BA)\n[Repeat](docs/DEMO_RUNBOOK_RU.md#a-1)\n", encoding="utf-8")
        self.assertEqual(2, self.verify()["local_links"])


class CurrentProductGuideTest(unittest.TestCase):
    def setUp(self):
        self.folder = tempfile.TemporaryDirectory()
        self.addCleanup(self.folder.cleanup)
        self.root = Path(self.folder.name)
        for relative in ("README.md", "docs/PRODUCT_TOUR_EN.md", "docs/PRODUCT_TOUR_RU.md",
                         "docs/MCP_TOUR_RU.md", "projects/workspace/qa-support/coverage.json"):
            target = self.root / relative
            target.parent.mkdir(parents=True,exist_ok=True)
            shutil.copyfile(ROOT/relative,target)

    def test_current_guide_keeps_historical_recording_labels(self):
        with (self.root/"README.md").open("a",encoding="utf-8") as stream:
            stream.write("\nHistorical 3.0.4/5.0 recordings used Overview, Review, Architecture and Findings.\n")
        result=check_current_product(self.root)
        self.assertEqual(19,result["mcp_tools"])

    def test_reachable_old_version_is_not_a_current_product_tour(self):
        (self.root/"README.md").write_text("# ArchVerity Demo\nEvaluate ArchVerity 5.3.2.\n",encoding="utf-8")
        with self.assertRaisesRegex(ValueError,"introduction"):
            check_current_product(self.root)

    def test_omitted_registered_tool_is_detected(self):
        file=self.root/"docs/MCP_TOUR_RU.md"
        lines=file.read_text(encoding="utf-8").splitlines(keepends=True)
        file.write_text("".join(line for line in lines if not line.startswith("| `archverity_simulate_change`")),encoding="utf-8")
        with self.assertRaisesRegex(ValueError,"19 registered"):
            check_current_product(self.root)

    def test_wrong_simulation_argument_is_not_accepted_as_a_recipe(self):
        file=self.root/"docs/MCP_TOUR_RU.md"
        file.write_text(file.read_text(encoding="utf-8").replace("edits_json","planned_changes_json"),encoding="utf-8")
        with self.assertRaisesRegex(ValueError,"edits_json"):
            check_current_product(self.root)


if __name__ == "__main__":
    unittest.main()

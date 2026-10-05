import tempfile
import unittest
from pathlib import Path

from check_docs import check


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


if __name__ == "__main__":
    unittest.main()

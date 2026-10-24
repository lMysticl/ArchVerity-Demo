import subprocess
import tempfile
import unittest
from pathlib import Path

from check_stale_mocks import LAB, STUB, check, load_scenarios
from prepare_project import prepare


class StaleMocksLabTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.project = Path(self.temp.name) / "demo"
        prepare("stale-mocks", self.project)
        self.scenarios = load_scenarios()

    def test_inputs_pass(self):
        self.assertEqual("STALE_MOCK_INPUTS_PASS", check()["status"])

    def test_fix_changes_only_the_consumer_dto_and_its_fake(self):
        before = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=self.project)
        self.scenarios.apply(self.project, "fix")
        actual = set(subprocess.check_output(["git", "diff", "--name-only"], cwd=self.project, text=True).splitlines())
        self.assertEqual({"orders-service/src/main/java/demo/orders/InvoiceView.java", STUB}, actual)
        self.assertIn('@com.fasterxml.jackson.annotation.JsonAlias("invoiceId")',
                      (self.project / "orders-service/src/main/java/demo/orders/InvoiceView.java").read_text())
        self.assertIn('\\"invoiceId\\": \\"42\\"', (self.project / STUB).read_text())
        self.assertEqual(before, subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=self.project))
        self.assertNotIn("JsonAlias", (LAB / "orders-service/src/main/java/demo/orders/InvoiceView.java").read_text())

    def test_a_manual_edit_is_not_lost(self):
        target = self.project / STUB
        target.write_bytes(target.read_bytes() + b"\n// user edit\n")
        before = subprocess.check_output(["git", "diff"], cwd=self.project)
        with self.assertRaisesRegex(ValueError, "has edits"):
            self.scenarios.apply(self.project, "fix")
        self.assertEqual(before, subprocess.check_output(["git", "diff"], cwd=self.project))

    def test_original_repository_is_not_a_prepared_project(self):
        with self.assertRaisesRegex(ValueError, "separate baseline"):
            self.scenarios.apply(LAB, "fix")


if __name__ == "__main__":
    unittest.main()

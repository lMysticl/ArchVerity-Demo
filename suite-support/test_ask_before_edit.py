import json
import subprocess
import tempfile
import unittest
from pathlib import Path

from check_ask_before_edit import LAB, check, load_scenarios
from prepare_project import prepare


class AskBeforeEditScenarioTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.project = Path(self.temp.name) / "demo"
        prepare("ask-before-edit", self.project)
        self.scenarios = load_scenarios()

    def git(self, *args):
        return subprocess.check_output(["git", *args], cwd=self.project, text=True)

    def test_each_scenario_writes_exactly_the_edit_an_agent_asks_about(self):
        for name, edits in self.scenarios.SCENARIOS.items():
            with self.subTest(name):
                project = Path(self.temp.name) / name
                prepare("ask-before-edit", project)
                result = self.scenarios.apply(project, name)
                diff = subprocess.check_output(["git", "diff", "--name-only"], cwd=project, text=True).splitlines()
                self.assertEqual([path for path, _, _ in edits], diff)
                for path, old, new in edits:
                    text = (project / path).read_text(encoding="utf-8")
                    self.assertEqual(1, text.count(new))
                    self.assertEqual(json.loads(self.scenarios.planned_edits(name)), [{"path": path, "old": old, "new": new}])
                self.assertEqual(len(edits), len(result["changed"]))

    def test_a_manual_edit_is_kept_and_nothing_else_changes(self):
        target = self.project / "orders-service/src/main/java/demo/orders/BillingClient.java"
        target.write_bytes(target.read_bytes() + b"\n// user edit\n")
        before = self.git("diff")
        with self.assertRaisesRegex(ValueError, "has edits"):
            self.scenarios.apply(self.project, "rename-field")
        self.assertEqual(before, self.git("diff"))

    def test_original_repository_is_not_a_prepared_project(self):
        with self.assertRaisesRegex(ValueError, "separate baseline"):
            self.scenarios.apply(LAB, "move-route")

    def test_inputs_contract_passes(self):
        self.assertEqual("ASK_BEFORE_EDIT_INPUTS_PASS", check()["status"])


if __name__ == "__main__":
    unittest.main()

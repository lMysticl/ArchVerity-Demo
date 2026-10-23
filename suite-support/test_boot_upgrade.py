import subprocess
import tempfile
import unittest
from pathlib import Path

from check_boot_upgrade import LAB, load_scenarios
from prepare_project import prepare


class UpgradeMutationSafetyTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.project = Path(self.temp.name) / "demo"
        prepare("boot-upgrade", self.project)
        self.scenarios = load_scenarios()

    def test_fix_changes_only_the_four_declared_business_files_and_preserves_baseline(self):
        before = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=self.project)
        result = self.scenarios.apply(self.project, "fix")
        actual = set(subprocess.check_output(["git", "diff", "--name-only"], cwd=self.project, text=True).splitlines())
        self.assertEqual({p for p, _, _ in self.scenarios.SCENARIOS['fix']}, actual)
        self.assertEqual(4, len(result['changed']))
        self.assertEqual(before, subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=self.project))
        self.assertNotIn('@com.fasterxml.jackson.annotation.JsonValue', (LAB/self.scenarios.BILLING/'InvoiceStatus.java').read_text())

    def test_a_manual_edit_is_not_lost_and_no_other_file_is_changed(self):
        target = self.project / self.scenarios.ORDERS / 'BillingClient.java'
        target.write_bytes(target.read_bytes() + b'\n// user edit\n')
        before = subprocess.check_output(["git", "diff"], cwd=self.project)
        with self.assertRaisesRegex(ValueError, 'has edits'):
            self.scenarios.apply(self.project, 'fix')
        self.assertEqual(before, subprocess.check_output(["git", "diff"], cwd=self.project))

    def test_running_twice_requires_a_fresh_copy_instead_of_replacing_the_fix(self):
        self.scenarios.apply(self.project, 'fix')
        before = subprocess.check_output(["git", "diff"], cwd=self.project)
        with self.assertRaisesRegex(ValueError, 'has edits'):
            self.scenarios.apply(self.project, 'mapper-unknown')
        self.assertEqual(before, subprocess.check_output(["git", "diff"], cwd=self.project))

    def test_unknown_mapper_control_changes_configuration_only(self):
        result = self.scenarios.apply(self.project, 'mapper-unknown')
        self.assertEqual(['billing-service/src/main/resources/application.yml'], [x['path'] for x in result['changed']])

    def test_original_repository_is_not_a_prepared_project(self):
        with self.assertRaisesRegex(ValueError, 'separate baseline'):
            self.scenarios.apply(LAB, 'fix')


if __name__ == '__main__':
    unittest.main()

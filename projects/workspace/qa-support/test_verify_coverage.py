"""Negative controls for fixture claims that previously passed by file existence."""

import copy
import json
import unittest

from verify_coverage import PROJECT, validate_process_inputs, verify


class ProcessFixtureCoverageTest(unittest.TestCase):
    def setUp(self):
        self.entries = json.loads((PROJECT / "qa-support/coverage.json").read_text(encoding="utf-8"))["processCommands"]

    def test_current_mapping_has_only_real_local_inputs(self):
        self.assertEqual(verify()["process_inputs"], {"local_input": 6, "external_environment": 16})

    def test_extensionless_script_cannot_masquerade_as_shellcheck_input(self):
        entries = copy.deepcopy(self.entries)
        entries["SHELLCHECK"]["fixtures"] = ["shell-professional/bin/deploy"]
        with self.assertRaisesRegex(AssertionError, "Unsupported file input"):
            validate_process_inputs(entries)

    def test_detection_only_package_cannot_masquerade_as_bundle_input(self):
        entries = copy.deepcopy(self.entries)
        entries["RN_BUNDLE"]["level"] = "local_input"
        entries["RN_BUNDLE"]["fixtures"] = ["rn-qa/package.json"]
        with self.assertRaisesRegex(AssertionError, "falsely claims a local fixture"):
            validate_process_inputs(entries)

    def test_external_dependency_cannot_be_omitted(self):
        entries = copy.deepcopy(self.entries)
        entries["ADB_LOGCAT"].pop("prerequisites")
        with self.assertRaisesRegex(AssertionError, "falsely claims a local fixture"):
            validate_process_inputs(entries)


if __name__ == "__main__":
    unittest.main()

"""Reject plausible incomplete demo guides and invented consumer proof."""

import copy
import unittest

from check_playbooks import ROOT, read, validate


class CompleteFunctionGuideTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = read(ROOT / "suite-support/function_playbooks.json")
        cls.entries = read(ROOT / "suite-support/entry_point_playbooks.json")

    def test_missing_subfeature_cannot_hide_inside_shared_icon_capability(self):
        data = copy.deepcopy(self.data)
        data["features"] = [f for f in data["features"] if f["id"] != "DEV-04"]
        with self.assertRaisesRegex(ValueError, "source function was omitted"):
            validate(data, self.entries)

    def test_kotlin_reference_entry_cannot_be_dropped(self):
        entries = [e for e in self.entries if e["id"] != "editorExtensions:psi.referenceContributor:MyBatisReferenceContributor:kotlin"]
        with self.assertRaisesRegex(ValueError, "Every registered entry"):
            validate(self.data, entries)

    def test_an_action_without_observable_result_is_not_a_scenario(self):
        data = copy.deepcopy(self.data)
        data["features"][0]["steps"][0]["expect"] = ""
        with self.assertRaisesRegex(ValueError, "trigger/oracle"):
            validate(data, self.entries)

    def test_prepared_inputs_cannot_be_marked_as_consumer_pass(self):
        data = copy.deepcopy(self.data)
        data["features"][0]["consumer_status"] = "PASS"
        with self.assertRaisesRegex(ValueError, "invent a consumer PASS"):
            validate(data, self.entries)


if __name__ == "__main__":
    unittest.main()

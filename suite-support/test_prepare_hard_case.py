"""Exercise source/Git boundaries only; these are not ArchVerity scan tests."""

import json
import os
import tempfile
import unittest
from pathlib import Path

from prepare_hard_case import (CASES, CLIENT, CONTROLLER, ENTITY, RECEIPT, ROOT,
                               TOTAL, V1, V2, git, hashes, prepare_case)


class HardCasePreparationTest(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory(prefix="hard-case-test-",
                                               dir=os.environ.get("ARCHVERITY_TEST_TMP", ROOT.parent))
        self.addCleanup(temporary.cleanup)
        self.folder = Path(temporary.name)

    def test_baseline_states_are_clean_and_leave_mutation_until_after_the_native_base_scan(self):
        for case in CASES:
            with self.subTest(case=case):
                project = Path(prepare_case(case, self.folder / case, "baseline")["project"])
                self.assertEqual("", git(project, "status", "--porcelain"))
                self.assertEqual("", git(project, "diff", "HEAD"))
                receipt = json.loads((project / RECEIPT).read_text(encoding="utf-8"))
                self.assertEqual("baseline", receipt["state"])
                self.assertEqual([], receipt["changes"])
                self.assertEqual(receipt["baselineInputs"], receipt["inputs"])
                self.assertEqual('NO CONTRACT CHANGES', receipt["expectedNativeObservation"]["comparison"])
                self.assertIn('path = "/payments"', (project / CLIENT).read_text(encoding="utf-8"))
                if case == "migration-old-reader":
                    self.assertIn(TOTAL, (project / ENTITY).read_text(encoding="utf-8"))
                    self.assertFalse((project / V2).exists())

    def test_rollout_has_compatible_base_and_current_pair_but_removes_the_old_route(self):
        project = Path(prepare_case("rollout-cycle", self.folder / "broken")["project"])
        for path in (CLIENT, CONTROLLER):
            self.assertIn('"/payments"', git(project, "show", f"HEAD:{path}"))
            self.assertIn('"/v2/payments"', (project / path).read_text(encoding="utf-8"))
        self.assertIn("@PutMapping", git(project, "show", f"HEAD:{CLIENT}"))
        self.assertNotIn("@PostMapping", (project / CLIENT).read_text(encoding="utf-8"))
        self.assertEqual({CLIENT, CONTROLLER}, set(git(project, "diff", "--name-only", "HEAD").splitlines()))
        self.assertEqual("", git(project, "diff", "--cached", "--name-only"))
        repaired = Path(prepare_case("rollout-cycle", self.folder / "repaired", "repaired")["project"])
        self.assertIn('@RequestMapping({"/payments", "/v2/payments"})',
                      (repaired / CONTROLLER).read_text(encoding="utf-8"))

    def test_migration_compares_a_new_drop_with_the_old_mapping_not_an_edited_applied_migration(self):
        project = Path(prepare_case("migration-old-reader", self.folder / "broken")["project"])
        self.assertIn(TOTAL, git(project, "show", f"HEAD:{ENTITY}") + "\n")
        self.assertNotIn(TOTAL, (project / ENTITY).read_text(encoding="utf-8"))
        self.assertEqual("ALTER TABLE orders DROP COLUMN total;\n", (project / V2).read_text(encoding="utf-8"))
        self.assertEqual("", git(project, "ls-files", "--others", "--exclude-standard"))
        self.assertIn(f"A\t{V2}", git(project, "diff", "--name-status", "HEAD"))
        self.assertEqual("", git(project, "diff", "--cached", "--name-only"))
        self.assertEqual(git(project, "show", f"HEAD:{V1}"), (project / V1).read_text(encoding="utf-8").strip())
        repaired = Path(prepare_case("migration-old-reader", self.folder / "repaired", "repaired")["project"])
        self.assertFalse((repaired / V2).exists())
        self.assertNotIn(TOTAL, (repaired / ENTITY).read_text(encoding="utf-8"))

    def test_manifest_binds_source_and_base_and_existing_user_content_is_never_overwritten(self):
        for case in CASES:
            project = Path(prepare_case(case, self.folder / case)["project"])
            receipt = json.loads((project / RECEIPT).read_text(encoding="utf-8"))
            self.assertEqual(git(project, "rev-parse", "HEAD"), receipt["baseCommit"])
            self.assertEqual(receipt["inputs"], hashes(project, receipt["inputs"]))
            for change in receipt["changes"]:
                self.assertNotEqual(change["beforeSha256"], change["afterSha256"])
            (project / "owner.txt").write_text("owner content", encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "overwrite"):
                prepare_case(case, project)
            self.assertEqual("owner content", (project / "owner.txt").read_text(encoding="utf-8"))
        for case, state in (("missing", "broken"), ("rollout-cycle", "missing")):
            with self.assertRaises(ValueError):
                prepare_case(case, self.folder / "invalid", state)
        self.assertFalse((self.folder / "invalid").exists())


if __name__ == "__main__":
    unittest.main()

"""Preparation and negative export controls; these tests are not plugin scans."""

import copy
import json
import tempfile
import unittest
from pathlib import Path

from check_boot_kafka import check_analysis, check_impact, check_project, check_shipped_lab
from prepare_boot_kafka_case import (BOOT_LINES, CASES, CONSUMER_DTO, CUSTOMIZER,
                                     LAB, PRODUCER_DTO, RECEIPT, REQUIRED,
                                     git, prepare_case)


def synthetic_snapshot(case):
    evidence = [{"label": "Configuration", "source": {"path": f"{role}/src/main/resources/application.properties"}}
                for role in ("producer", "consumer")]
    operations = [{"id": role, "kind": kind, "attributes": {"wireConfidence": "RESOLVED", "payloadType": f"demo.boot.{role}.Event"}, "evidence": evidence}
                  for role, kind in (("producer", "KAFKA_PRODUCER"), ("consumer", "KAFKA_CONSUMER"))]
    findings = []
    if case["snapshot"] == "PROVEN_MISMATCH":
        findings = [{"ruleId": "AFG-KAFKA-005", "disposition": "PROVEN_MISMATCH"}]
    elif case["snapshot"] == "UNKNOWN":
        operations[0]["attributes"]["wireConfidence"] = "UNKNOWN"
        findings = [{"ruleId": "AFG-KAFKA-010", "disposition": "UNKNOWN", "evidence": [
            {"label": "Factory customizer", "source": {"path": CUSTOMIZER}}]}]
    return {"schemaVersion": 1, "projectId": "selected-boot-case", "runStatus": "COMPLETE", "partial": False,
            "analysisContext": {"fingerprint": "synthetic-validator-control"}, "coverage": {},
            "nodes": [*operations, {"kind":"KAFKA_TOPIC","name":"orders.events"}], "edges": [], "findings": findings}


class BootKafkaPreparationTest(unittest.TestCase):
    def test_each_line_and_case_preserves_templates_and_real_git_base(self):
        shipped = {str(path.relative_to(LAB)): path.read_bytes() for path in LAB.rglob("*")
                   if path.is_file() and not set(path.parts) & {".gradle", "build", "work"}}
        self.assertEqual("INPUT_CONTRACT_PASS", check_shipped_lab()["status"])
        with tempfile.TemporaryDirectory(prefix="boot-kafka-test-", dir=LAB.parents[2]) as temporary:
            for line in BOOT_LINES:
                for case in CASES:
                    with self.subTest(line=line, case=case["id"]):
                        result = prepare_case(case["name"], Path(temporary)/f"{line}-{case['id']}", line)
                        root = Path(result["project"])
                        self.assertEqual("INPUT_CONTRACT_PASS", check_project(root)["status"])
                        self.assertEqual(result["baseline"], git(root, "rev-parse", "HEAD"))
                        self.assertIn(f"bootLine={line}", (root/"gradle.properties").read_text(encoding="utf-8"))
                        serde = "JacksonJson" if line == "40" else "Json"
                        self.assertIn(f"serializer.{serde}Serializer", (root/"producer/src/main/resources/application.properties").read_text(encoding="utf-8"))
                        self.assertIn(f"serializer.{serde}Deserializer", (root/"consumer/src/main/resources/application.properties").read_text(encoding="utf-8"))
                        base_producer = git(root, "show", f"HEAD:{PRODUCER_DTO}")
                        base_consumer = git(root, "show", f"HEAD:{CONSUMER_DTO}")
                        current_producer = (root/PRODUCER_DTO).read_text(encoding="utf-8")
                        current_consumer = (root/CONSUMER_DTO).read_text(encoding="utf-8")
                        self.assertEqual(case["name"] != "historical-reader", REQUIRED in base_producer)
                        self.assertEqual(case["name"] != "historical-reader", REQUIRED in base_consumer)
                        self.assertEqual(case["name"] not in {"remove-required", "customizer-control"}, REQUIRED in current_producer)
                        self.assertIn(REQUIRED, current_consumer)
                        if case["name"] == "customizer-control":
                            self.assertIn("DefaultKafkaProducerFactoryCustomizer", git(root,"show",f"HEAD:{CUSTOMIZER}"))
                            self.assertEqual((root/CUSTOMIZER).read_text(encoding="utf-8").strip(), git(root,"show",f"HEAD:{CUSTOMIZER}"))
        self.assertEqual(shipped, {str(path.relative_to(LAB)): path.read_bytes() for path in LAB.rglob("*")
                                  if path.is_file() and not set(path.parts) & {".gradle", "build", "work"}})

    def test_existing_output_and_invalid_selection_never_overwrite(self):
        with tempfile.TemporaryDirectory(prefix="boot-kafka-refusal-", dir=LAB.parents[2]) as temporary:
            root = Path(temporary)
            occupied = root/"occupied"
            occupied.mkdir()
            (occupied/"keep.txt").write_bytes(b"owner content")
            with self.assertRaisesRegex(ValueError, "overwrite"):
                prepare_case("baseline", occupied)
            self.assertEqual(b"owner content", (occupied/"keep.txt").read_bytes())
            for name, line in (("not-a-case", "35"), ("baseline", "99")):
                output = root/f"invalid-{line}"
                with self.assertRaises(ValueError):
                    prepare_case(name, output, line)
                self.assertFalse(output.exists())

    def test_source_drift_moved_base_and_wrong_directory_are_rejected(self):
        with tempfile.TemporaryDirectory(prefix="boot-kafka-identity-", dir=LAB.parents[2]) as temporary:
            root = Path(prepare_case("baseline", Path(temporary)/"baseline")["project"])
            source = root/PRODUCER_DTO
            original = source.read_bytes()
            source.write_bytes(original + b"// unrecorded edit\n")
            with self.assertRaisesRegex(ValueError, "Source bytes changed"):
                check_project(root)
            source.write_bytes(original)
            receipt = root/RECEIPT
            metadata = json.loads(receipt.read_text(encoding="utf-8"))
            metadata["project"] = str(Path(temporary)/"another-project")
            receipt.write_bytes((json.dumps(metadata)+"\n").encode("utf-8"))
            with self.assertRaisesRegex(ValueError, "WRONG_TARGET"):
                check_project(root)
            metadata["project"] = str(root)
            receipt.write_bytes((json.dumps(metadata)+"\n").encode("utf-8"))
            git(root, "-c", "user.name=Fixture", "-c", "user.email=fixture@invalid.example", "commit", "--quiet", "--allow-empty", "-m", "moved")
            with self.assertRaisesRegex(ValueError, "Git base moved"):
                check_project(root)

    def test_correction_control_requires_exact_baseline_bytes(self):
        with tempfile.TemporaryDirectory(prefix="boot-kafka-restore-", dir=LAB.parents[2]) as temporary:
            root = Path(prepare_case("remove-required", Path(temporary)/"remove")["project"])
            with self.assertRaisesRegex(ValueError, "Source bytes changed"):
                check_project(root, restored=True)
            git(root, "restore", "--", PRODUCER_DTO)
            self.assertTrue(check_project(root, restored=True)["restored"])
            with self.assertRaisesRegex(ValueError, "Source bytes changed"):
                check_project(root)


class BootKafkaExportGuardTest(unittest.TestCase):
    def test_partial_wrong_target_and_customizer_false_proof_cannot_pass(self):
        for case in CASES:
            snapshot = synthetic_snapshot(case)
            self.assertEqual("BOOT_KAFKA_ANALYSIS_CASE_PASS", check_analysis(snapshot,case,"selected-boot-case")["status"])
            for patch in ({"partial": True}, {"runStatus": "FAILED"}, {"projectId": "adjacent-project"}, {"analysisContext": {}}):
                bad = copy.deepcopy(snapshot)
                bad.update(patch)
                with self.subTest(case=case["id"], patch=patch), self.assertRaises(ValueError):
                    check_analysis(bad,case,"selected-boot-case")
            bad = copy.deepcopy(snapshot)
            bad["nodes"].pop()
            with self.assertRaises(ValueError):
                check_analysis(bad,case,"selected-boot-case")
        custom = next(case for case in CASES if case["name"] == "customizer-control")
        bad = synthetic_snapshot(custom)
        bad["findings"].append({"ruleId":"AFG-KAFKA-005","disposition":"PROVEN_MISMATCH"})
        with self.assertRaisesRegex(ValueError,"must not be promoted"):
            check_analysis(bad,custom,"selected-boot-case")

    def test_impact_requires_bound_base_complete_case_and_historical_reason(self):
        historical = next(case for case in CASES if case["name"] == "historical-reader")
        valid = {"schemaVersion":1,"baseIdentity":"selected-base","headIdentity":"working-tree",
                 "complete":True,"summary":{},"impacts":[{"verdict":"BREAKING","reason":"Old records lack tenant"}]}
        self.assertEqual("BOOT_KAFKA_IMPACT_CASE_PASS",check_impact(valid,historical,"selected-base")["status"])
        for patch in ({"complete":False},{"baseIdentity":"adjacent-base"},{"headIdentity":""},
                      {"impacts":[{"verdict":"SAFE","reason":"Old records"}]},
                      {"impacts":[{"verdict":"BREAKING","reason":"Only the current producer"}]}):
            bad = copy.deepcopy(valid)
            bad.update(patch)
            with self.subTest(patch=patch),self.assertRaises(ValueError):
                check_impact(bad,historical,"selected-base")


if __name__ == "__main__":
    unittest.main()

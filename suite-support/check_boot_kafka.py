"""Inspect prepared Boot Kafka inputs and optional real ArchVerity JSON exports."""

import argparse
import json
import re
import subprocess
from pathlib import Path

from inspect_export import unique_keys, validate_analysis
from prepare_boot_kafka_case import (BOOT_LINES, CASES, CONSUMER_DTO, CUSTOMIZER,
                                     LAB, PRODUCER_DTO, RECEIPT, REQUIRED,
                                     digest, git, input_paths)


def check_shipped_lab():
    names = {"baseline", "remove-required", "add-optional", "customizer-control", "historical-reader"}
    if len(CASES) != 5 or {case["id"] for case in CASES} != {f"B{i:02}" for i in range(1, 6)} or {case["name"] for case in CASES} != names:
        raise ValueError("Boot Kafka lab must retain its five independently checkable cases")
    for case in CASES:
        if set(case) != {"id", "name", "snapshot", "impact", "purpose"} or not case["purpose"].strip():
            raise ValueError("Incomplete Boot Kafka recipe")
    required = ["README.md", "cases.json", ".archflow.yml", "settings.gradle.kts", "build.gradle.kts",
                "gradle.properties", "gradlew", "gradlew.bat", "gradle/wrapper/gradle-wrapper.jar",
                "gradle/wrapper/gradle-wrapper.properties", PRODUCER_DTO, CONSUMER_DTO,
                *[f"{role}/src/main/java/demo/boot/{role}/{name}.java" for role, name in (("producer","Application"),("producer","Publisher"),("consumer","Application"),("consumer","Listener"))],
                *[f"{role}/src/main/resources/application.properties" for role in ("producer","consumer")]]
    for relative in required:
        path = LAB / relative
        if not path.is_file() or path.is_symlink() or not path.resolve().is_relative_to(LAB.resolve()):
            raise ValueError(f"Missing/unsafe Boot Kafka template: {relative}")
    build = (LAB / "build.gradle.kts").read_text(encoding="utf-8")
    if not all(f'"{version}"' in build for version in BOOT_LINES.values()) or '"org.springframework.boot:spring-boot-kafka"' not in build:
        raise ValueError("Boot Kafka dependencies lost their pinned 3.5/4.0 boundary")
    for relative in (PRODUCER_DTO, CONSUMER_DTO):
        if (LAB / relative).read_text(encoding="utf-8").count(REQUIRED) != 1:
            raise ValueError("Required-field mutation selector drifted")
    properties = (LAB / "gradle/wrapper/gradle-wrapper.properties").read_text(encoding="utf-8")
    if "gradle-9.3.0-bin.zip" not in properties or "distributionSha256Sum=0d585f69da091fc5b2beced877feab55a3064d43b8a1d46aeb07996b0915e0e0" not in properties:
        raise ValueError("New lab wrapper must retain Gradle 9.3 with the checked distribution checksum")
    for name in ("gradlew", "gradlew.bat", "gradle/wrapper/gradle-wrapper.jar"):
        if (LAB / name).read_bytes() != (LAB.parent / "kafka-profile-lab" / name).read_bytes():
            raise ValueError(f"Unexpected wrapper upgrade: {name}")
    return {"status": "INPUT_CONTRACT_PASS", "cases": len(CASES), "boot_lines": BOOT_LINES,
            "boundary": "Pinned, compilable source recipes; this check does not build or run ArchVerity"}


def check_project(project, restored=False):
    project = Path(project).resolve()
    receipt = project / RECEIPT
    if not receipt.is_file():
        raise ValueError("Prepared case receipt is missing; use prepare_boot_kafka_case.py")
    metadata = json.loads(receipt.read_text(encoding="utf-8"), object_pairs_hook=unique_keys)
    case = next((case for case in CASES if case == metadata.get("case")), None)
    if metadata.get("schemaVersion") != 1 or case is None or metadata.get("project") != str(project):
        raise ValueError("WRONG_TARGET: case identity does not match the prepared directory")
    boot_line = metadata.get("bootLine")
    if boot_line not in BOOT_LINES or metadata.get("bootVersion") != BOOT_LINES[boot_line]:
        raise ValueError("Boot line identity is missing or changed")
    if git(project, "rev-parse", "HEAD") != metadata.get("baseline"):
        raise ValueError("Git base moved; the old case receipt is stale")
    if restored and case["name"] != "remove-required":
        raise ValueError("--restored is only the exact remove-required correction control")
    expected = metadata.get("baselineInputs" if restored else "inputs")
    if not isinstance(expected, dict) or set(expected) != set(input_paths(project)):
        raise ValueError("Source scope changed; the case receipt is stale")
    for relative, value in expected.items():
        path = project / relative
        if Path(relative).is_absolute() or ".." in Path(relative).parts or not path.resolve().is_relative_to(project):
            raise ValueError("Unsafe source identity in case receipt")
        if not isinstance(value, str) or not re.fullmatch(r"[0-9a-f]{64}", value) or digest(path.read_bytes()) != value:
            raise ValueError(f"Source bytes changed: {relative}; export/check the intended stage again")
    return {"status": "INPUT_CONTRACT_PASS", "case": case["id"], "caseName": case["name"],
            "bootLine": boot_line, "baseline": metadata["baseline"], "restored": restored,
            "sourceFiles": len(expected), "boundary": "Source and Git input identities only; no build, IDE or broker observation"}


def check_analysis(snapshot, case, expected_project_id, restored=False):
    if not expected_project_id:
        raise ValueError("Record --project-id from the selected project before checking its export")
    validate_analysis(snapshot, require_complete=True, expected_project_id=expected_project_id)
    operations = [node for node in snapshot["nodes"] if node.get("kind") in {"KAFKA_PRODUCER", "KAFKA_CONSUMER"}]
    if len([node for node in operations if node.get("kind") == "KAFKA_PRODUCER"]) != 1 or len([node for node in operations if node.get("kind") == "KAFKA_CONSUMER"]) != 1:
        raise ValueError("Expected one producer and one listener; confirm both imported modules and scan scope")
    topics = [node for node in snapshot["nodes"] if node.get("kind") == "KAFKA_TOPIC"]
    if len(topics) != 1 or topics[0].get("name") != "orders.events":
        raise ValueError("The selected topic/scope is not this Boot Kafka case")
    for node in operations:
        role = "producer" if node["kind"] == "KAFKA_PRODUCER" else "consumer"
        if node.get("attributes", {}).get("payloadType") != f"demo.boot.{role}.Event":
            raise ValueError("The exported payload belongs to another producer/reader")
    paths = {str(item.get("source", {}).get("path", "")).replace("\\", "/")
             for entity in [*snapshot["nodes"], *snapshot["findings"]]
             for item in entity.get("evidence", []) if isinstance(item, dict) and isinstance(item.get("source"), dict)}
    for role in ("producer", "consumer"):
        if not any(path.endswith(f"{role}/src/main/resources/application.properties") for path in paths):
            raise ValueError(f"Missing Boot configuration source provenance: {role}")
    contract = [item for item in snapshot["findings"] if item.get("ruleId") == "AFG-KAFKA-005"]
    expected = "RESOLVED_NO_SEEDED_MISMATCH" if restored else case["snapshot"]
    if expected == "PROVEN_MISMATCH":
        if not any(item.get("disposition") == "PROVEN_MISMATCH" for item in contract):
            raise ValueError("The seeded required-field mismatch was not proven")
    elif expected == "UNKNOWN":
        if any(item.get("disposition") == "PROVEN_MISMATCH" for item in contract):
            raise ValueError("A customizer control must not be promoted to a proven wire mismatch")
        wire = [item for item in snapshot["findings"] if item.get("ruleId") == "AFG-KAFKA-010" and item.get("disposition") == "UNKNOWN"]
        if not wire or "ProducerOverrides.java" not in json.dumps(wire, ensure_ascii=False):
            raise ValueError("Needs review must retain the named factory-customizer source")
    else:
        if contract:
            raise ValueError("No seeded DTO mismatch should remain at this stage")
        if any(node.get("attributes", {}).get("wireConfidence") not in {"RESOLVED", "EXACT"} for node in operations):
            raise ValueError("The ordinary Boot serializer chain was not resolved")
    return {"status": "BOOT_KAFKA_ANALYSIS_CASE_PASS", "case": case["id"], "projectId": snapshot["projectId"],
            "analysisContext": snapshot["analysisContext"]["fingerprint"], "restored": restored,
            "boundary": "Complete exported source-analysis content; source/IDE identity and freshness require the separately recorded run"}


def check_impact(data, case, expected_base_identity, restored=False):
    required = {"schemaVersion", "baseIdentity", "headIdentity", "complete", "summary", "impacts"}
    if not isinstance(data, dict) or not required <= data.keys() or data["schemaVersion"] != 1 or data["complete"] is not True:
        raise ValueError("A complete Impact export is required")
    if not expected_base_identity or data["baseIdentity"] != expected_base_identity or not isinstance(data["headIdentity"], str) or not data["headIdentity"].strip():
        raise ValueError("WRONG_TARGET: Impact base/head identity is not the selected comparison")
    if not isinstance(data["summary"], dict) or not isinstance(data["impacts"], list) or any(not isinstance(item, dict) for item in data["impacts"]):
        raise ValueError("Malformed Impact verdict collection")
    verdicts = {item.get("verdict") for item in data["impacts"]}
    if not verdicts <= {"SAFE", "BREAKING", "UNKNOWN"}:
        raise ValueError("Malformed Impact verdict")
    expected = None if restored else case["impact"]
    if expected is None and verdicts:
        raise ValueError("The restored/baseline comparison still has seeded impacts")
    if expected == "BREAKING" and "BREAKING" not in verdicts:
        raise ValueError("The intended producer/reader change was not Breaking")
    if expected == "SAFE" and verdicts != {"SAFE"}:
        raise ValueError("The additive producer change did not retain the bounded compatible result")
    if expected == "UNKNOWN" and verdicts != {"UNKNOWN"}:
        raise ValueError("The customizer comparison must remain Needs review")
    if case["name"] == "historical-reader" and not any(
            item.get("verdict") == "BREAKING" and "old records" in str(item.get("reason", "")).lower()
            for item in data["impacts"]):
        raise ValueError("Current matching shapes must still name the old-record producer mismatch")
    return {"status": "BOOT_KAFKA_IMPACT_CASE_PASS", "case": case["id"], "baseIdentity": data["baseIdentity"],
            "headIdentity": data["headIdentity"], "restored": restored,
            "boundary": "Source/Git comparison only; no retained broker records or deployed producer identity was established"}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project", required=True, type=Path)
    parser.add_argument("--restored", action="store_true")
    parser.add_argument("--snapshot", type=Path)
    parser.add_argument("--impact", type=Path)
    parser.add_argument("--project-id")
    parser.add_argument("--base-identity", help="Exact baseIdentity observed for this comparison, not an inferred ref")
    args = parser.parse_args()
    try:
        result = check_project(args.project, args.restored)
        metadata = json.loads((args.project / RECEIPT).read_text(encoding="utf-8"), object_pairs_hook=unique_keys)
        if args.snapshot:
            result["analysis"] = check_analysis(json.loads(args.snapshot.read_text(encoding="utf-8"), object_pairs_hook=unique_keys),
                                                metadata["case"], args.project_id, args.restored)
        if args.impact:
            result["impact"] = check_impact(json.loads(args.impact.read_text(encoding="utf-8"), object_pairs_hook=unique_keys),
                                            metadata["case"], args.base_identity, args.restored)
        print(json.dumps(result))
    except (ValueError, OSError, subprocess.CalledProcessError) as error:
        parser.error(str(error))


if __name__ == "__main__":
    main()

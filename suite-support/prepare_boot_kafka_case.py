"""Prepare an isolated Boot Kafka source case with an inspectable Git base."""

import argparse
import hashlib
import json
import subprocess
from pathlib import Path

from prepare_project import ROOT, prepare

LAB = ROOT / "projects/kafka-boot-lab"
CASES = json.loads((LAB / "cases.json").read_text(encoding="utf-8"))
CASE_NAMES = tuple(case["name"] for case in CASES)
BOOT_LINES = {"35": "3.5.7", "40": "4.0.0"}
PRODUCER_DTO = "producer/src/main/java/demo/boot/producer/Event.java"
CONSUMER_DTO = "consumer/src/main/java/demo/boot/consumer/Event.java"
CUSTOMIZER = "producer/src/main/java/demo/boot/producer/ProducerOverrides.java"
REQUIRED = ', @JsonProperty(value = "tenant", required = true) String tenant'
RECEIPT = "work/boot-kafka-case.json"
INPUT_TOP = (".archflow.yml", "build.gradle.kts", "settings.gradle.kts", "gradle.properties")


def digest(data):
    return hashlib.sha256(data).hexdigest()


def input_paths(root):
    paths = set(INPUT_TOP)
    for role in ("producer", "consumer"):
        for path in (root / role / "src/main").rglob("*"):
            if path.is_file() and path.suffix in {".java", ".properties"}:
                if path.is_symlink() or not path.resolve().is_relative_to(root.resolve()):
                    raise ValueError("Source input escapes the prepared project")
                paths.add(path.relative_to(root).as_posix())
    return sorted(paths)


def git(root, *arguments):
    return subprocess.check_output(
        ["git", "-c", "commit.gpgSign=false", "-c",
         f"core.hooksPath={root / '.git/no-demo-hooks'}", *arguments],
        cwd=root, text=True, encoding="utf-8").strip()


def _write(path, text):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(text.encode("utf-8"))


def _replace(root, relative, before, after):
    path = root / relative
    text = path.read_text(encoding="utf-8")
    if text.count(before) != 1:
        raise ValueError(f"Fixture drift: {relative}: expected one {before!r}")
    _write(path, text.replace(before, after, 1))


def prepare_case(name, destination, boot_line="35"):
    boot_line = str(boot_line)
    case = next((case for case in CASES if case["name"] == name), None)
    if case is None:
        raise ValueError(f"Unknown Boot Kafka case: {name}")
    if boot_line not in BOOT_LINES:
        raise ValueError(f"Unknown Boot line: {boot_line}")
    result = prepare("kafka-boot-lab", Path(destination))
    root = Path(result["project"])
    if boot_line == "40":
        _replace(root, "gradle.properties", "bootLine=35", "bootLine=40")
        for role in ("producer", "consumer"):
            _replace(root, f"{role}/src/main/resources/application.properties",
                     "support.serializer.Json", "support.serializer.JacksonJson")
    if name == "historical-reader":
        for relative in (PRODUCER_DTO, CONSUMER_DTO):
            _replace(root, relative, REQUIRED, "")
    if name == "customizer-control":
        package = "org.springframework.boot.autoconfigure.kafka" if boot_line == "35" else "org.springframework.boot.kafka.autoconfigure"
        _write(root / CUSTOMIZER, f'''package demo.boot.producer;

@org.springframework.context.annotation.Configuration
public class ProducerOverrides {{
    @org.springframework.context.annotation.Bean
    public {package}.DefaultKafkaProducerFactoryCustomizer customizer() {{
        return factory -> {{}};
    }}
}}
''')
    git(root, "add", "--all")
    git(root, "-c", "user.name=ArchVerity Demo Fixture", "-c", "user.email=demo@invalid.example",
        "commit", "--quiet", "--allow-empty", "-m", f"Boot {BOOT_LINES[boot_line]} {case['id']} source baseline")
    baseline = git(root, "rev-parse", "HEAD")
    baseline_inputs = {relative: digest((root / relative).read_bytes()) for relative in input_paths(root)}
    if git(root, "status", "--porcelain"):
        raise AssertionError("Prepared Boot Kafka base must be clean before the isolated change")

    if name in {"remove-required", "customizer-control"}:
        _replace(root, PRODUCER_DTO, REQUIRED, "")
    elif name == "add-optional":
        _replace(root, PRODUCER_DTO, REQUIRED, REQUIRED + ", String note")
    elif name == "historical-reader":
        for relative in (PRODUCER_DTO, CONSUMER_DTO):
            _replace(root, relative, "Event(String id)", "Event(String id" + REQUIRED + ")")
    metadata = {
        "schemaVersion": 1, "case": case, "bootLine": boot_line,
        "bootVersion": BOOT_LINES[boot_line], "project": str(root), "baseline": baseline,
        "producerDto": PRODUCER_DTO, "consumerDto": CONSUMER_DTO,
        "baselineInputs": baseline_inputs,
        "inputs": {relative: digest((root / relative).read_bytes()) for relative in input_paths(root)},
        "boundary": "Prepared source and Git identities only. No broker, IDE scan or export verification was executed by preparation."
    }
    _write(root / RECEIPT, json.dumps(metadata, ensure_ascii=False, indent=2) + "\n")
    return {**result, "baseline": baseline, "case": case, "bootLine": boot_line,
            "bootVersion": BOOT_LINES[boot_line], "receipt": str(root / RECEIPT)}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--boot-line", choices=BOOT_LINES, default="35")
    parser.add_argument("--case", choices=[case["name"] for case in CASES], required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    try:
        print(json.dumps(prepare_case(args.case, args.output, args.boot_line)))
    except ValueError as error:
        parser.error(str(error))


if __name__ == "__main__":
    main()

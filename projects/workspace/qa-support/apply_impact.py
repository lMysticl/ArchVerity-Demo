"""Apply one isolated architecture change after IDEA saved a complete HEAD scan."""

import argparse
import hashlib
import json
import os
import subprocess
from pathlib import Path

CONTROLLER = Path("payment-app/src/main/java/sample/payment/PaymentController.java")
PUBLISHER = Path("order-app/src/main/java/sample/order/OrderPublisher.java")
DEV_CONFIG = Path("payment-app/src/main/resources/application-dev.yml")
PROJECT_CONFIG = Path(".archflow.yml")

# Exact, one-occurrence replacements keep the scenario deterministic. The
# default preserves the originally documented three-change Impact exercise.
SCENARIOS = {
    "combined-breaking": (
        (CONTROLLER, '@PostMapping("/{paymentId}")', '@PutMapping("/{paymentId}")'),
        (CONTROLLER, "String currency)", "String currency, @jakarta.validation.constraints.NotNull String mandatoryRiskToken)"),
        (CONTROLLER, ", @jakarta.validation.constraints.NotNull String providerReference)", ")"),
    ),
    "http-method": ((CONTROLLER, '@PostMapping("/{paymentId}")', '@PutMapping("/{paymentId}")'),),
    "request-required": ((CONTROLLER, "String currency)", "String currency, @jakarta.validation.constraints.NotNull String mandatoryRiskToken)"),),
    "response-removed": ((CONTROLLER, ", @jakarta.validation.constraints.NotNull String providerReference)", ")"),),
    "response-optional-added": ((CONTROLLER, "String providerReference) {}", "String providerReference, String auditNote) {}"),),
    "kafka-topic": ((PUBLISHER, 'send("orders.created",event)', 'send("orders.revised",event)'),),
    "spring-profile": ((DEV_CONFIG, "feature:\n  enabled: true", "feature:\n  enabled: false"),),
    "manifest-import": ((PROJECT_CONFIG, "  defaultCluster: core\n", "  defaultCluster: core\nmanifests:\n  - id: qa-loopback\n    path: contracts/qa-loopback.archflow.json\n  - id: qa-event-bus\n    path: contracts/qa-event-bus.archflow.json\n  - id: qa-backstage\n    path: contracts/qa-backstage.archflow.json\n"),),
    "manifest-missing": ((PROJECT_CONFIG, "  defaultCluster: core\n", "  defaultCluster: core\nmanifests:\n  - id: qa-missing\n    path: contracts/not-present.archflow.json\n"),),
}

from extended_scenarios import EXTRA_SCENARIOS
SCENARIOS.update(EXTRA_SCENARIOS)


def git(project, *arguments):
    return subprocess.run(
        ["git", *arguments], cwd=project, text=True, capture_output=True, check=True
    ).stdout.strip()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--project", type=Path, required=True, help="Prepared project after a clean IDEA Analyze")
    parser.add_argument("--scenario", choices=SCENARIOS, default="combined-breaking")
    args = parser.parse_args()
    project = args.project.resolve()
    if not project.is_dir() or git(project, "rev-parse", "--show-toplevel").replace("\\", "/").lower() != project.as_posix().lower():
        parser.error("Expected a prepared project at its own Git root")
    if git(project, "log", "-1", "--format=%s") != "QA baseline":
        parser.error("Expected the synthetic QA baseline commit")
    if git(project, "status", "--porcelain"):
        parser.error("Baseline must be clean before applying a QA scenario")
    head = git(project, "rev-parse", "HEAD")
    saved = project / ".idea/archflow/commits" / f"{head}.json"
    if not saved.is_file():
        parser.error("Analyze clean HEAD in IDEA first; exact commit snapshot is missing")
    snapshot = json.loads(saved.read_text(encoding="utf-8"))
    if snapshot.get("runStatus") != "COMPLETE" or snapshot.get("partial") or snapshot.get("coverage", {}).get("unsupportedFeatures") != 0:
        parser.error("Clean HEAD snapshot is incomplete; resolve analysis errors before applying a scenario")

    replacements = SCENARIOS[args.scenario]
    sources = {}
    for relative, before, after in replacements:
        if relative not in sources:
            source = (project / relative).read_text(encoding="utf-8")
            if git(project, "show", f"HEAD:{relative.as_posix()}") != source.rstrip("\n"):
                parser.error(f"Source differs from committed baseline: {relative}")
            sources[relative] = source
        if sources[relative].count(before) != 1:
            parser.error(f"Scenario {args.scenario} requires one exact occurrence of {before!r} in {relative}")
        sources[relative] = sources[relative].replace(before, after, 1)

    changed = []
    for relative, after in sources.items():
        target = project / relative
        before = target.read_text(encoding="utf-8")
        temporary = target.with_name(target.name + ".qa-tmp")
        if temporary.exists():
            parser.error(f"Refusing to overwrite stale temporary file: {temporary}")
        try:
            temporary.write_text(after, encoding="utf-8")
            os.replace(temporary, target)
        finally:
            temporary.unlink(missing_ok=True)
        changed.append({
            "path": relative.as_posix(),
            "before_sha256": hashlib.sha256(before.encode("utf-8")).hexdigest(),
            "after_sha256": hashlib.sha256(after.encode("utf-8")).hexdigest(),
        })
    actual = set(git(project, "diff", "--name-only").replace("\\", "/").splitlines())
    expected = {item["path"] for item in changed}
    if actual != expected:
        raise AssertionError(f"Expected {expected}, got {actual}")
    print(json.dumps({"project": str(project), "baseline": head, "scenario": args.scenario, "changed": changed}, ensure_ascii=False))


if __name__ == "__main__":
    main()

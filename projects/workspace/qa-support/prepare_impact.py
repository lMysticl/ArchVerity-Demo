"""Create a clean Git baseline to scan in IDEA before applying the QA break."""

import argparse
import json
import shutil
import subprocess
from pathlib import Path

PROJECT = Path(__file__).resolve().parents[1]
CONTROLLER = Path("payment-app/src/main/java/sample/payment/PaymentController.java")
EXCLUDED = {".git", ".gradle", ".idea", ".kotlin", "build", "work", "__pycache__"}


def run_git(project, *arguments):
    result = subprocess.run(
        ["git", *arguments], cwd=project, text=True, capture_output=True, check=True
    )
    return result.stdout.strip()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True, help="New, task-owned project directory")
    args = parser.parse_args()
    destination = args.output.resolve()
    if destination.exists():
        parser.error(f"Refusing to overwrite existing path: {destination}")
    shutil.copytree(PROJECT, destination, ignore=shutil.ignore_patterns(*EXCLUDED))
    controller = destination / CONTROLLER
    source = controller.read_text(encoding="utf-8")
    if source.count('@PostMapping("/{paymentId}")') != 1 or "mandatoryRiskToken" in source:
        raise ValueError("Fixture contract drifted: clean HTTP baseline is missing")
    if source.count("@jakarta.validation.constraints.NotNull String providerReference") != 1:
        raise ValueError("Fixture contract drifted: required response field is missing")
    run_git(destination, "init", "--quiet")
    run_git(destination, "add", "-A")
    run_git(
        destination, "-c", "user.name=ArchVerity QA Fixture",
        "-c", "user.email=qa@invalid.example", "commit", "--quiet", "-m", "QA baseline",
    )
    baseline = run_git(destination, "rev-parse", "HEAD")
    if run_git(destination, "status", "--porcelain"):
        raise AssertionError("Prepared baseline is not clean")
    print(json.dumps({
        "project": str(destination), "baseline": baseline,
        "changed": [],
        "next": "Open in IDEA, Analyze clean HEAD, then run apply_impact.py",
    }, ensure_ascii=False))


if __name__ == "__main__":
    main()

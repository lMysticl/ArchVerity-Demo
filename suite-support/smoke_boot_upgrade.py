"""Compile and observe actual Boot 3/4 JSON, then verify the explicit fixture fix."""

import argparse
import json
import os
import subprocess
import sys
from pathlib import Path

from prepare_project import prepare


def run(output):
    output = output.resolve()
    if output.exists():
        raise ValueError(f"Use a fresh output directory: {output}")
    output.mkdir(parents=True)
    results = []
    for state in ("baseline", "fixed"):
        project = output / state
        prepared = prepare("boot-upgrade", project)
        if state == "fixed":
            subprocess.run([sys.executable, "-B", "-X", "utf8", "qa-support/apply_scenario.py", "--scenario", "fix"], cwd=project, check=True)
        wrapper = str(project / ("gradlew.bat" if os.name == "nt" else "gradlew"))
        command = [wrapper, "classes", "wireBoot3", "wireBoot4", "--console=plain", "--no-daemon"]
        with (output / f"{state}.log").open("w", encoding="utf-8") as log:
            result = subprocess.run(command, cwd=project, stdout=log, stderr=subprocess.STDOUT, timeout=600)
        if result.returncode:
            raise RuntimeError(f"{state} failed; inspect {output / (state + '.log')}")
        check = [sys.executable, "-B", "-X", "utf8", "verification/verify_wire.py"]
        if state == "fixed":
            check.append("--fixed")
        observed = json.loads(subprocess.check_output(check, cwd=project, text=True))
        results.append({"state": state, "baseline": prepared["baseline"], "observed": observed})
    return {"status": "BOOT_UPGRADE_WIRE_PASS", "runs": results,
            "boundary": "Real library behavior and compiled fixtures; installed ArchVerity run recorded separately"}


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    print(json.dumps(run(args.output)))

"""Make one exact planned edit for real in a fresh prepared project; never reset user edits."""

import argparse
import hashlib
import json
import subprocess
from pathlib import Path

BILLING = "billing-service/src/main/kotlin/demo/billing/"
# The same text an agent passes to archverity_simulate_change before writing it: path, old, new.
SCENARIOS = {
    "rename-field": [(BILLING + "InvoiceView.kt", "val id: String,", "val invoiceId: String,")],
    "move-route": [(BILLING + "InvoiceController.kt", '"/invoices/{id}"', '"/v2/invoices/{id}"')],
}


def planned_edits(scenario):
    """The edits_json argument for archverity_simulate_change, matching what apply() writes."""
    return json.dumps([{"path": path, "old": old, "new": new} for path, old, new in SCENARIOS[scenario]])


def apply(project, scenario):
    project = project.resolve()
    def git(*args):
        return subprocess.check_output(["git", *args], cwd=project, text=True).strip()
    if Path(git("rev-parse", "--show-toplevel")).resolve() != project or git("log", "-1", "--format=%s") != "QA baseline":
        raise ValueError("Use prepare_project.py --project ask-before-edit to create a separate baseline first")
    if git("status", "--porcelain"):
        raise ValueError("Project has edits; keep them and prepare a fresh copy for another scenario")
    changes = {}
    for relative, before, after in SCENARIOS[scenario]:
        path = project / relative
        if path.resolve() != path or path.is_symlink():
            raise ValueError(f"Linked demo input: {relative}")
        original = path.read_bytes()
        if original.count(before.encode()) != 1:
            raise ValueError(f"Fixture changed: {relative}")
        changes[path] = (original, original.replace(before.encode(), after.encode(), 1))
    for path, (before, after) in changes.items():
        if path.read_bytes() != before:
            raise ValueError(f"Concurrent edit: {path.name}")
        path.write_bytes(after)
    return {"scenario": scenario, "baseline": git("rev-parse", "HEAD"), "changed": [
        {"path": p.relative_to(project).as_posix(), "sha256": hashlib.sha256(data[1]).hexdigest()} for p, data in changes.items()
    ], "next": "Run Check changes in IDEA (or archverity_check_change) and compare with the answer you got before the edit"}


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--scenario", required=True, choices=SCENARIOS)
    parser.add_argument("--print-edits", action="store_true", help="print edits_json for archverity_simulate_change; change nothing")
    args = parser.parse_args()
    try:
        print(planned_edits(args.scenario) if args.print_edits else json.dumps(apply(Path(__file__).resolve().parents[1], args.scenario)))
    except (ValueError, subprocess.CalledProcessError) as error:
        parser.error(str(error))

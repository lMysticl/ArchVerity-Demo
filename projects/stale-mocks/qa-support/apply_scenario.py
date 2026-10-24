"""Apply one exact demo change to a fresh prepared project; never reset user edits."""

import argparse
import hashlib
import json
import subprocess
from pathlib import Path

ORDERS = "orders-service/src/main/java/demo/orders/"
ORDERS_TEST = "orders-service/src/test/java/demo/orders/"
SCENARIOS = {
    # Orders moves first: it reads both names, and its fake answers with what billing sends now.
    "fix": [
        (ORDERS + "InvoiceView.java", "public record InvoiceView(String id, long total) {",
         "public record InvoiceView(@com.fasterxml.jackson.annotation.JsonAlias(\"invoiceId\") String id, long total) {"),
        (ORDERS_TEST + "BillingInvoiceTest.java", "{\\\"id\\\": \\\"42\\\", \\\"total\\\": 1200}",
         "{\\\"invoiceId\\\": \\\"42\\\", \\\"total\\\": 1200}"),
    ],
}


def apply(project, scenario):
    project = project.resolve()
    def git(*args):
        return subprocess.check_output(["git", *args], cwd=project, text=True).strip()
    if Path(git("rev-parse", "--show-toplevel")).resolve() != project or git("log", "-1", "--format=%s") != "QA baseline":
        raise ValueError("Use prepare_project.py --project stale-mocks to create a separate baseline first")
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
    ], "next": "Re-run the tests, realCall and Analyze in IDEA; record the actual result"}


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--scenario", required=True, choices=SCENARIOS)
    args = parser.parse_args()
    try:
        print(json.dumps(apply(Path(__file__).resolve().parents[1], args.scenario)))
    except (ValueError, subprocess.CalledProcessError) as error:
        parser.error(str(error))

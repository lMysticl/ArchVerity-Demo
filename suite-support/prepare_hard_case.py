"""Prepare fresh, synthetic contract traps with an exact local Git baseline.

This produces source inputs only. It never builds, runs the IDE or manufactures
runtime/verification evidence. Existing directories are always refused.
"""

import argparse
import hashlib
import json
import os
import subprocess
from pathlib import Path

from prepare_project import ROOT, prepare

CASES = ("rollout-cycle", "migration-old-reader")
STATES = ("baseline", "broken", "repaired")
CLIENT = "order-app/src/main/java/demo/orders/PaymentClient.java"
CONTROLLER = "payment-app/src/main/java/demo/payments/PaymentController.java"
ENTITY = "payment-app/src/main/java/demo/payments/OrderEntity.java"
V1 = "payment-app/src/main/resources/db/migration/V1__create_orders.sql"
V2 = "payment-app/src/main/resources/db/migration/V2__drop_total.sql"
RECEIPT = "work/hard-case.json"
TOTAL = '    @Column(name = "total")\n    private java.math.BigDecimal total;\n'


def git(root, *arguments):
    return subprocess.check_output(
        ["git", "-c", "commit.gpgSign=false", "-c",
         f"core.hooksPath={root / '.git/no-demo-hooks'}", *arguments],
        cwd=root, text=True, encoding="utf-8").strip()


def write(root, relative, text):
    path = root / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    data = text.encode("utf-8")
    temporary = path.with_name(path.name + ".hard-case-tmp")
    with temporary.open("xb") as stream:
        stream.write(data)
    if temporary.read_bytes() != data:
        raise ValueError(f"Incomplete fixture write: {relative}")
    os.replace(temporary, path)


def replace(root, relative, before, after):
    text = (root / relative).read_text(encoding="utf-8")
    if text.count(before) != 1:
        raise ValueError(f"Fixture drift: {relative}: expected one {before!r}")
    write(root, relative, text.replace(before, after, 1))


def hashes(root, paths):
    return {relative: hashlib.sha256((root / relative).read_bytes()).hexdigest()
            for relative in sorted(paths)}


def prepare_case(case, destination, state="broken"):
    if case not in CASES or state not in STATES:
        raise ValueError("Unknown hard case or fixture state")
    destination = Path(destination).absolute()
    for path in (destination, *destination.parents):
        if path.is_symlink() or (hasattr(path, "is_junction") and path.is_junction()):
            raise ValueError("Fixture output cannot traverse a link or junction")
    if destination == ROOT or ROOT in destination.parents:
        raise ValueError("Fixture output must be outside the demo source checkout")
    if destination.exists():
        raise ValueError(f"Refusing to overwrite existing directory: {destination}")

    result = prepare("first-result", destination)
    root = Path(result["project"])
    # Both cases start with a compatible HTTP pair, without the simple POST/PUT trap.
    replace(root, CLIENT, "@PostMapping", "@PutMapping")
    replace(root, CLIENT,
            "    // Intentional mismatch: the provider accepts PUT, while this caller sends POST.\n"
            "    // Fix only this annotation to @PutMapping, then run Analyze again.\n", "")
    if case == "migration-old-reader":
        write(root, "payment-app/build.gradle.kts", 'plugins { java }\n\n'
              'dependencies {\n    implementation("jakarta.persistence:jakarta.persistence-api:3.1.0")\n}\n')
        write(root, ENTITY, 'package demo.payments;\n\n'
              'import jakarta.persistence.Column;\nimport jakarta.persistence.Entity;\n'
              'import jakarta.persistence.Id;\nimport jakarta.persistence.Table;\n\n'
              '@Entity\n@Table(name = "orders")\npublic class OrderEntity {\n'
              '    @Id\n    @Column(name = "id", nullable = false)\n    private Long id;\n\n'
              + TOTAL + '}\n')
        write(root, V1, 'CREATE TABLE orders (id BIGINT PRIMARY KEY, total DECIMAL(19, 2));\n')
    project_title = f"ArchVerity hard case: {case}"
    replace(root, ".archflow.yml", "displayName: ArchVerity First Result", f"displayName: {json.dumps(project_title)}")
    # Keep the root project name: .archflow.yml already maps the actual Gradle module names.
    write(root, "README.md", f"# {project_title}\n\n"
          f"Synthetic {state} source fixture. Compare HEAD to Current files in ArchVerity.\n"
          "Run gradlew classes with JDK 21; no application, database or broker is started.\n"
          "Before changing source, finish IDE import/indexing and analyze the clean baseline.\n"
          "The preparation receipt in work/hard-case.json is not an analyzer result.\n"
          "See the hard-cases guide in the demo source checkout for the repair and limits.\n")
    git(root, "add", "--all")
    git(root, "-c", "user.name=ArchVerity Demo Fixture", "-c", "user.email=demo@invalid.example",
        "commit", "--quiet", "-m", f"Compatible {case} source baseline")
    baseline = git(root, "rev-parse", "HEAD")
    baseline_paths = git(root, "ls-files", "-z").rstrip("\0").split("\0")
    baseline_inputs = hashes(root, baseline_paths)
    if git(root, "status", "--porcelain"):
        raise AssertionError("Hard-case base must be clean before the isolated change")

    if state == "baseline":
        expected = {"comparison": "NO CONTRACT CHANGES", "workingTree": "clean",
                    "next": "Finish IDE import and indexing, analyze the clean HEAD, then make the bounded case mutation"}
    elif case == "rollout-cycle":
        mapping = '"/v2/payments"' if state == "broken" else '{"/payments", "/v2/payments"}'
        replace(root, CONTROLLER, '@RequestMapping("/payments")', f"@RequestMapping({mapping})")
        replace(root, CLIENT, 'path = "/payments"', 'path = "/v2/payments"')
        expected = {"currentPair": "matching PUT /v2/payments/{paymentId}",
                    "rollout": "NO_ORDER" if state == "broken" else "expanded provider permits provider-first review"}
    else:
        replace(root, ENTITY, TOTAL, "")
        if state == "broken":
            write(root, V2, "ALTER TABLE orders DROP COLUMN total;\n")
            # Expose the new file in Git's diff without staging its contents. An
            # unrelated untracked input would correctly make review incomplete.
            git(root, "add", "--intent-to-add", "--", V2)
        expected = {"change": "new code no longer maps orders.total",
                    "migration": "BREAKING: Dropped column is still mapped by the previous version"
                    if state == "broken" else "destructive migration deferred; no seeded DROP impact"}
    current_paths = baseline_paths + ([V2] if case == "migration-old-reader" and state == "broken" else [])
    current_inputs = hashes(root, current_paths)
    changes = [{"path": path, "beforeSha256": baseline_inputs.get(path),
                "afterSha256": current_inputs.get(path)}
               for path in sorted(set(baseline_inputs) | set(current_inputs))
               if baseline_inputs.get(path) != current_inputs.get(path)]
    metadata = {"schemaVersion": 1, "case": case, "state": state, "project": str(root),
                "baseRef": "HEAD", "baseCommit": baseline, "headCommit": git(root, "rev-parse", "HEAD"),
                "baselineInputs": baseline_inputs, "inputs": current_inputs, "changes": changes,
                "expectedNativeObservation": expected,
                "boundary": "Source preparation only. No build, IDE scan, deployed-version binding or runtime observation was executed."}
    encoded = json.dumps(metadata, ensure_ascii=False, indent=2) + "\n"
    json.loads(encoded)
    write(root, RECEIPT, encoded)
    return {"project": str(root), "case": case, "state": state, "baseline": baseline,
            "changedFiles": [change["path"] for change in changes], "receipt": str(root / RECEIPT),
            "boundary": metadata["boundary"]}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--case", choices=CASES, required=True)
    parser.add_argument("--state", choices=STATES, default="broken")
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    try:
        print(json.dumps(prepare_case(args.case, args.output, args.state)))
    except (ValueError, subprocess.CalledProcessError) as error:
        parser.error(str(error))


if __name__ == "__main__":
    main()

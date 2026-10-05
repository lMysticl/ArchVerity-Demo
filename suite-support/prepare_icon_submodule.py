"""Prepare a disposable, independent workspace with an actual local Git submodule."""

import argparse
import json
import subprocess
from pathlib import Path

from prepare_project import prepare


def create(destination):
    result = prepare("workspace", destination)
    root = Path(result["project"])
    source = root / "work/icon-submodule-source"
    source.mkdir(parents=True)
    (source / "README.md").write_text("Public local source for the demo-icon-module gitlink.\n", encoding="utf-8")

    def git(directory, *arguments):
        return subprocess.check_output(["git", *arguments], cwd=directory, text=True, stderr=subprocess.STDOUT).strip()

    identity = ("-c", "user.name=ArchVerity Demo Fixture", "-c", "user.email=demo@invalid.example")
    git(source, "init", "--quiet", "--initial-branch=main")
    git(source, "add", "README.md")
    git(source, *identity, "commit", "--quiet", "-m", "Local public icon fixture")
    git(root, "-c", "protocol.file.allow=always", "submodule", "add", "--name", "demo-icons", str(source), "demo-icon-module")
    git(root, *identity, "commit", "--quiet", "-m", "Add actual icon-demo submodule")
    entry = git(root, "ls-files", "--stage", "demo-icon-module")
    if not entry.startswith("160000 ") or git(root, "status", "--porcelain"):
        raise AssertionError("Expected a clean standalone workspace with one actual gitlink")
    result.update(baseline=git(root, "rev-parse", "HEAD"), gitlink=entry,
                  fixture="demo-icon-module", status="ACTUAL_SUBMODULE_INPUT_PASS")
    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    print(json.dumps(create(args.output)))

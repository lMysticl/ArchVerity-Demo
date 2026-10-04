"""Prepare a new standalone project, preserving the shipped source baseline."""

import argparse
import json
import shutil
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXCLUDED = {".git", ".gradle", ".idea", ".kotlin", ".expo", "node_modules", "build", "out", "work", "reports", "__pycache__", "android", "ios"}


def prepare(name, destination):
    destination = destination.resolve()
    if destination.exists():
        raise ValueError(f"Refusing to overwrite existing directory: {destination}")
    source = ROOT / "projects" / name
    if destination == source or source in destination.parents:
        raise ValueError("Destination must be outside the shipped project")
    if not source.is_dir():
        raise ValueError(f"Unknown project: {name}")
    shutil.copytree(source, destination, ignore=shutil.ignore_patterns(*EXCLUDED, "*.pyc", "*.iml"))
    shutil.copy2(ROOT / ".gitattributes", destination / ".gitattributes")
    def git(*arguments):
        return subprocess.check_output(["git", *arguments], cwd=destination, text=True).strip()
    git("init", "--quiet", "--initial-branch=main")
    git("add", "--all")
    git("-c", "user.name=ArchVerity Demo Fixture", "-c", "user.email=demo@invalid.example",
        "commit", "--quiet", "-m", "QA baseline")
    if git("status", "--porcelain"):
        raise AssertionError("Prepared project must have a clean baseline")
    return {"project": str(destination), "name": name, "baseline": git("rev-parse", "HEAD")}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--project", choices=("first-result", "workspace", "runtime-evidence", "mobile-lab"), required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    try:
        print(json.dumps(prepare(args.project, args.output)))
    except ValueError as error:
        parser.error(str(error))


if __name__ == "__main__":
    main()

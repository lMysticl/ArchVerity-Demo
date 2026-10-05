"""Prepare a new standalone project, preserving the shipped source baseline."""

import argparse
import json
import re
import shutil
import subprocess
from pathlib import Path
from urllib.parse import quote, unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
PROJECTS = ("first-result", "workspace", "api-lab", "mobile-lab", "runtime-evidence", "kafka-profile-lab")
EXCLUDED = {".git", ".gradle", ".idea", ".kotlin", ".expo", "node_modules", "build", "out", "work", "reports", "__pycache__", "android", "ios"}


def retarget_document_links(source, destination):
    """Keep cross-project guides reachable from a standalone copy."""
    for document in source.rglob("*.md"):
        copied = destination / document.relative_to(source)
        if not copied.is_file():
            continue
        text = document.read_bytes().decode("utf-8")

        def replace(match):
            parsed = urlsplit(match[2].strip("<>"))
            if parsed.scheme or parsed.netloc or not parsed.path:
                return match[0]
            target = (document.parent / unquote(parsed.path)).resolve()
            if target.is_relative_to(source) or not target.is_relative_to(ROOT):
                return match[0]
            url = "https://github.com/lMysticl/ArchVerity-Demo/blob/main/" + quote(target.relative_to(ROOT).as_posix(), safe="/")
            if parsed.query:
                url += "?" + parsed.query
            if parsed.fragment:
                url += "#" + quote(unquote(parsed.fragment), safe="-_.~")
            return match[1] + url + match[3]

        parts = re.split(r"(```.*?```)", text, flags=re.S)
        for index in range(0, len(parts), 2):
            parts[index] = re.sub(r"(\[[^\]]*\]\()([^)]*)(\))", replace, parts[index])
        copied.write_bytes("".join(parts).encode("utf-8"))


def prepare(name, destination):
    if name not in PROJECTS:
        raise ValueError(f"Unknown project: {name}")
    destination = destination.resolve()
    if destination.exists():
        raise ValueError(f"Refusing to overwrite existing directory: {destination}")
    source = ROOT / "projects" / name
    if destination == source or source in destination.parents:
        raise ValueError("Destination must be outside the shipped project")
    if not source.is_dir():
        raise ValueError(f"Unknown project: {name}")
    shutil.copytree(source, destination, ignore=shutil.ignore_patterns(*EXCLUDED, "*.pyc", "*.iml"))
    retarget_document_links(source.resolve(), destination)
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
    parser.add_argument("--project", choices=PROJECTS, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    try:
        print(json.dumps(prepare(args.project, args.output)))
    except ValueError as error:
        parser.error(str(error))


if __name__ == "__main__":
    main()

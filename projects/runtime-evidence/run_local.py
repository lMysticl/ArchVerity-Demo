"""Run this exact clean checkout and expose its bound identity on loopback."""

import hashlib
import os
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def main():
    def git(*args):
        return subprocess.check_output(["git", *args], cwd=ROOT, text=True).strip()
    if Path(git("rev-parse", "--show-toplevel")).resolve() != ROOT:
        raise SystemExit("Prepare an isolated runtime-evidence project with suite-support/prepare_project.py first")
    if git("status", "--porcelain"):
        raise SystemExit("Commit intended config and sources before starting the observed application")
    environment = os.environ.copy()
    environment["DEMO_SOURCE_REVISION"] = git("rev-parse", "HEAD")
    environment["DEMO_CONFIG_SHA256"] = hashlib.sha256((ROOT / ".archflow.yml").read_bytes()).hexdigest()
    wrapper = ROOT / ("gradlew.bat" if os.name == "nt" else "gradlew")
    command = [str(wrapper), "run", "--console=plain", "--no-daemon"]
    if os.name == "nt":
        command = [environment.get("COMSPEC", "cmd.exe"), "/d", "/c", *command]
    raise SystemExit(subprocess.call(command, cwd=ROOT, env=environment))


if __name__ == "__main__":
    main()

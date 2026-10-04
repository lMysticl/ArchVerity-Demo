"""Inspect the exact tracked demo files before public Git delivery."""

import json
import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ALLOWED_BINARY = {".aficons", ".jar", ".der", ".p12", ".pb"}
EXCLUDED = {"node_modules", "build", "work", ".idea", ".gradle", "__pycache__", "SOURCE", "plugin-backend", "plugin-frontend"}


def check():
    subprocess.run(["git", "diff", "--quiet", "--exit-code"], cwd=ROOT, check=True)
    paths = subprocess.check_output(["git", "ls-files", "-z"], cwd=ROOT).decode().split("\0")
    paths = [relative for relative in paths if relative]
    if not paths:
        raise ValueError("Stage the scoped demo tree before inspecting public delivery")
    forbidden = re.compile(r"(?:gh[pousr]_[A-Za-z0-9]{30,}|github_pat_[A-Za-z0-9_]{40,}|AKIA[A-Z0-9]{16})")
    total, binaries = 0, []
    for relative in paths:
        path = Path(relative)
        if set(path.parts) & EXCLUDED or path.suffix in {".key", ".keystore", ".jks", ".pfx", ".class"} or path.name.startswith(".env"):
            raise ValueError(f"Non-demo/private/generated path staged: {relative}")
        data = (ROOT / path).read_bytes()
        total += len(data)
        if len(data) > 2_000_000:
            raise ValueError(f"Unexpected large staged artifact: {relative}")
        if path.suffix in ALLOWED_BINARY:
            if path.suffix == ".jar" and path.name != "gradle-wrapper.jar":
                raise ValueError(f"Non-wrapper compiled code staged: {relative}")
            binaries.append(relative)
            continue
        text = data.decode("utf-8")
        if forbidden.search(text) or any(("-----BEGIN " + kind + "-----") in text for kind in ("PRIVATE KEY", "RSA PRIVATE KEY", "EC PRIVATE KEY", "OPENSSH PRIVATE KEY", "ENCRYPTED PRIVATE KEY")):
            raise ValueError(f"Credential/private-key marker in staged file: {relative}")
    return {"status": "PUBLIC_TREE_PASS", "files": len(paths), "bytes": total,
            "reviewed_binary_inputs": binaries, "boundary": "Exact tracked demo tree; public-only truststore separately checked by preflight"}


if __name__ == "__main__":
    print(json.dumps(check()))

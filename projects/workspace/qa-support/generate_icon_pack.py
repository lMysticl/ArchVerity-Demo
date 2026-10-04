"""Derive a distinct, deterministic QA pack from the bundled Studio sample."""

import argparse
import base64
import re
import zipfile
from pathlib import Path

PROJECT = Path(__file__).resolve().parents[1]
SOURCE = PROJECT / "archflow-studio.aficons"
OLD_ID = "archflow-studio"
NEW_ID = "archverity-qa"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=PROJECT / "archverity-qa.aficons")
    parser.add_argument("--version", type=int, default=1)
    parser.add_argument("--accent", default="#EE0000")
    args = parser.parse_args()
    target = args.output.resolve()
    if target.exists():
        parser.error(f"Refusing to overwrite existing path: {target}")
    target.parent.mkdir(parents=True, exist_ok=True)
    if args.version < 1 or not re.fullmatch(r"#[0-9A-Fa-f]{6}", args.accent):
        parser.error("Expected positive version and six-digit hex accent")
    with zipfile.ZipFile(SOURCE) as archive:
        payloads = {name: archive.read(name) for name in archive.namelist()}
    assert payloads["manifest.tsv"].decode("utf-8").startswith(OLD_ID + "\t")
    payloads["manifest.tsv"] = (
        f"{NEW_ID}\t{base64.b64encode(b'ArchVerity QA').decode()}\t{args.version}\n"
    ).encode("utf-8")
    rules = payloads["rules.tsv"].decode("utf-8")
    assert OLD_ID in rules
    payloads["rules.tsv"] = rules.replace(OLD_ID, NEW_ID).encode("utf-8")
    icon = payloads["icons/ansible.svg"]
    assert icon.count(b"#EE0000") == 1
    payloads["icons/ansible.svg"] = icon.replace(b"#EE0000", args.accent.encode("ascii"), 1)
    with zipfile.ZipFile(target, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        for name, body in sorted(payloads.items()):
            info = zipfile.ZipInfo(name, (2026, 1, 1, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            archive.writestr(info, body, compress_type=zipfile.ZIP_DEFLATED, compresslevel=9)
    with zipfile.ZipFile(target) as archive:
        assert archive.testzip() is None
    print(target)


if __name__ == "__main__":
    main()

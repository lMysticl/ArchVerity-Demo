"""Generate a bounded, numbered ANSI log for the plugin's large-file editor."""

import argparse
import hashlib
import json
import os
from pathlib import Path


def generate(output, lines):
    if not 1 <= lines <= 300_000:
        raise ValueError("lines must be 1..300000")
    if output.exists():
        raise ValueError("Refusing to overwrite an existing log")
    output.parent.mkdir(parents=True, exist_ok=True)
    temporary = output.with_name(output.name + ".tmp")
    digest = hashlib.sha256()
    with temporary.open("xb") as stream:
        for number in range(1, lines + 1):
            line = (f"\x1b[{'31' if number % 10 == 0 else '32'}mLINE-{number:07d} "
                    "payment-app/src/main/java/sample/payment/PaymentController.java:12 "
                    "demo event\x1b[0m\n").encode("utf-8")
            stream.write(line)
            digest.update(line)
    if output.exists():
        raise ValueError("Output appeared during generation; retaining temporary evidence")
    os.link(temporary, output)
    temporary.unlink()
    return {"path": str(output.resolve()), "lines": lines, "bytes": output.stat().st_size,
            "sha256": digest.hexdigest(), "first": "LINE-0000001", "last": f"LINE-{lines:07d}",
            "classification": "EVIDENCE_ONLY", "boundary": "Log producer; editor page/jump proof needs IDEA"}


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--lines", type=int, default=70_001)
    args = parser.parse_args()
    try:
        print(json.dumps(generate(args.output, args.lines)))
    except (ValueError, FileExistsError) as error:
        parser.error(str(error))

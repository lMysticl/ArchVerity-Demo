"""Compile the exact source into an import-complete FileDescriptorSet."""

import hashlib
import json
import os
import tempfile
from pathlib import Path

import grpc_tools
from grpc_tools import protoc

ROOT = Path(__file__).resolve().parent


def build():
    target = ROOT / "schema/echo.pb"
    include = Path(grpc_tools.__file__).parent / "_proto"
    with tempfile.NamedTemporaryFile(dir=target.parent, suffix=".tmp", delete=False) as stream:
        temporary = Path(stream.name)
    try:
        status = protoc.main([
            "protoc", f"-I{target.parent}", f"-I{include}", "--include_imports",
            f"--descriptor_set_out={temporary}", str(target.with_suffix(".proto")),
        ])
        if status:
            raise RuntimeError(f"protoc failed: {status}")
        os.replace(temporary, target)
    finally:
        temporary.unlink(missing_ok=True)
    return {"descriptor": "schema/echo.pb", "sha256": hashlib.sha256(target.read_bytes()).hexdigest()}


if __name__ == "__main__":
    print(json.dumps(build()))

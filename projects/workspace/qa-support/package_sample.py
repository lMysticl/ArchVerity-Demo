"""Create a portable, source-only ZIP of the validation workspace."""

import argparse
import hashlib
import json
import os
import zipfile
from pathlib import Path

PROJECT = Path(__file__).resolve().parents[1]
EXCLUDED = {".git", ".gradle", ".idea", ".kotlin", "build", "work", "__pycache__"}
PREFIX = "archverity-sample-workspace"


def inputs():
    for path in sorted(PROJECT.rglob("*")):
        if path.is_file() and not (set(path.relative_to(PROJECT).parts) & EXCLUDED):
            if path.suffix not in {".iml", ".pyc"}:
                yield path


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", required=True, type=Path)
    output = parser.parse_args().output.resolve()
    if output.exists():
        parser.error(f"Refusing to overwrite existing path: {output}")
    output.parent.mkdir(parents=True, exist_ok=True)
    temporary = output.with_name(output.name + ".tmp")
    if temporary.exists():
        parser.error(f"Refusing to overwrite existing temporary path: {temporary}")
    files = list(inputs())
    try:
        with zipfile.ZipFile(temporary, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
            for path in files:
                name = f"{PREFIX}/{path.relative_to(PROJECT).as_posix()}"
                info = zipfile.ZipInfo(name, (2026, 1, 1, 0, 0, 0))
                info.compress_type = zipfile.ZIP_DEFLATED
                info.external_attr = 0o644 << 16
                archive.writestr(info, path.read_bytes(), compress_type=zipfile.ZIP_DEFLATED, compresslevel=9)
        with zipfile.ZipFile(temporary) as archive:
            assert archive.testzip() is None
            assert len(archive.namelist()) == len(files)
        os.replace(temporary, output)
    finally:
        if temporary.exists():
            temporary.unlink()
    print(json.dumps({
        "output": str(output), "files": len(files), "bytes": output.stat().st_size,
        "sha256": hashlib.sha256(output.read_bytes()).hexdigest(),
    }))


if __name__ == "__main__":
    main()

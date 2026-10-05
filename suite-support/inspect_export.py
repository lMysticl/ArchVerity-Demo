"""Read real exports without pretending this format check executes analysis."""

import argparse
import json
import re
import struct
import xml.etree.ElementTree as ET
import zlib
from pathlib import Path


def _nonblank(value):
    return isinstance(value, str) and bool(value.strip())


def validate_analysis(data, *, require_complete=False, expected_project_id=None):
    required = {"schemaVersion", "projectId", "runStatus", "partial", "analysisContext", "coverage", "nodes", "edges", "findings"}
    if not isinstance(data, dict) or not required <= data.keys():
        raise ValueError("Analysis identity/scope/model fields are missing")
    if type(data["schemaVersion"]) is not int or data["schemaVersion"] != 1:
        raise ValueError("Unsupported analysis schemaVersion")
    if not _nonblank(data["projectId"]) or data["runStatus"] not in ("COMPLETE", "PARTIAL", "FAILED", "CANCELLED") or type(data["partial"]) is not bool:
        raise ValueError("Invalid analysis identity/status")
    if not isinstance(data["analysisContext"], dict) or not _nonblank(data["analysisContext"].get("fingerprint")) or not isinstance(data["coverage"], dict):
        raise ValueError("Analysis context/coverage is missing or malformed")
    for key in ("nodes", "edges", "findings"):
        if not isinstance(data[key], list) or any(not isinstance(item, dict) for item in data[key]):
            raise ValueError(f"Analysis {key} must be an array of objects")
    if require_complete and (data["runStatus"] != "COMPLETE" or data["partial"]):
        raise ValueError("A partial, failed or cancelled analysis cannot prove a complete case")
    if expected_project_id is not None and data["projectId"] != expected_project_id:
        raise ValueError("WRONG_TARGET: analysis projectId does not match the selected project")


def _png_detail(payload):
    # PNG chunk framing/CRC: https://www.w3.org/TR/png-3/#5Chunk-layout
    if payload[:8] != b"\x89PNG\r\n\x1a\n":
        raise ValueError("PNG signature is missing")
    offset, header, image_bytes = 8, None, 0
    while offset < len(payload):
        if offset + 12 > len(payload):
            raise ValueError("Truncated PNG chunk")
        size = int.from_bytes(payload[offset:offset + 4], "big")
        kind = payload[offset + 4:offset + 8]
        end = offset + 12 + size
        if end > len(payload):
            raise ValueError("Truncated PNG chunk data")
        data = payload[offset + 8:end - 4]
        if zlib.crc32(kind + data) != int.from_bytes(payload[end - 4:end], "big"):
            raise ValueError("PNG chunk CRC mismatch")
        if header is None:
            if kind != b"IHDR" or size != 13:
                raise ValueError("PNG must start with a complete IHDR")
            width, height, depth, color, compression, filtering, interlace = struct.unpack(">IIBBBBB", data)
            depths = {0: (1, 2, 4, 8, 16), 2: (8, 16), 3: (1, 2, 4, 8), 4: (8, 16), 6: (8, 16)}
            if not 0 < width < 2**31 or not 0 < height < 2**31 or depth not in depths.get(color, ()) or compression != 0 or filtering != 0 or interlace not in (0, 1):
                raise ValueError("Invalid PNG image header")
            header = {"format": "PNG", "width": width, "height": height}
        elif kind == b"IHDR":
            raise ValueError("Duplicate PNG IHDR")
        elif kind == b"IDAT":
            image_bytes += size
        elif kind == b"IEND":
            if size or not image_bytes or end != len(payload):
                raise ValueError("PNG image data/trailer is missing or trailing bytes remain")
            return header
        offset = end
    raise ValueError("PNG IEND is missing")


def unique_keys(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError("Duplicate JSON field")
        result[key] = value
    return result


def inspect(path, kind, *, require_complete=False, expected_project_id=None):
    payload = path.read_bytes()
    if not payload:
        raise ValueError("Export is empty")
    if kind == "png":
        detail = _png_detail(payload)
    elif kind == "svg":
        try:
            root = ET.fromstring(payload)
        except ET.ParseError as error:
            raise ValueError("Malformed SVG XML") from error
        if root.tag.rsplit("}", 1)[-1] != "svg":
            raise ValueError("SVG root is missing")
        detail = {"format": "SVG"}
    elif kind in ("mermaid", "markdown"):
        text = payload.decode("utf-8")
        if not text.strip():
            raise ValueError("Text export is empty")
        if kind == "mermaid" and not re.search(r"^(?:flowchart\s+\w+|graph\s+\w+|sequenceDiagram)\s*(?:$|;)", text, re.M):
            raise ValueError("Mermaid diagram declaration is missing")
        detail = {"format": kind, "characters": len(text)}
    else:
        data = json.loads(payload, object_pairs_hook=unique_keys)
        if not isinstance(data, dict):
            raise ValueError("Expected a JSON export object")
        if kind == "sarif":
            if data.get("version") != "2.1.0" or not isinstance(data.get("runs"), list) or not data["runs"]:
                raise ValueError("Expected SARIF 2.1.0 with runs")
            for run in data["runs"]:
                driver = run.get("tool", {}).get("driver", {}) if isinstance(run, dict) and isinstance(run.get("tool"), dict) else {}
                if not isinstance(driver, dict) or not _nonblank(driver.get("name")) or not isinstance(run.get("results", []), list):
                    raise ValueError("SARIF run has no tool identity or valid results")
            detail = {"format": "SARIF", "runs": len(data["runs"])}
        elif kind == "impact":
            required = {"schemaVersion", "baseIdentity", "headIdentity", "complete", "summary", "impacts"}
            if not required <= data.keys():
                raise ValueError("Impact comparison/verdict fields are missing")
            if type(data["schemaVersion"]) is not int or data["schemaVersion"] != 1 or type(data["complete"]) is not bool or not isinstance(data["summary"], dict) or not isinstance(data["impacts"], list) or any(not isinstance(item, dict) for item in data["impacts"]):
                raise ValueError("Invalid Impact schema/status/verdict fields")
            if not all(_nonblank(data[key]) for key in ("baseIdentity", "headIdentity")):
                raise ValueError("Impact comparison identity is empty")
            if require_complete and not data["complete"]:
                raise ValueError("An incomplete Impact export cannot prove a complete case")
            detail = {key: data[key] for key in ("baseIdentity", "headIdentity", "complete", "summary")}
        elif kind == "analysis":
            validate_analysis(data, require_complete=require_complete, expected_project_id=expected_project_id)
            detail = {key: data[key] for key in ("projectId", "runStatus", "partial", "coverage")}
        else:
            raise ValueError("Unknown export kind")
    return {"path": str(path.resolve()), "bytes": len(payload), "format_inspection": detail,
            "boundary": "Format inspection only; completeness and live IDEA identity require separate checks"}


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("path", type=Path)
    parser.add_argument("--kind", choices=("analysis", "impact", "sarif", "svg", "png", "mermaid", "markdown"), required=True)
    parser.add_argument("--require-complete", action="store_true", help="Reject incomplete analysis/Impact")
    parser.add_argument("--project-id", help="Require the exact observed analysis projectId")
    args = parser.parse_args()
    try:
        if (args.project_id and args.kind != "analysis") or (args.require_complete and args.kind not in ("analysis", "impact")):
            parser.error("Identity/completeness options require the corresponding JSON export")
        print(json.dumps(inspect(args.path, args.kind, require_complete=args.require_complete, expected_project_id=args.project_id)))
    except (ValueError, OSError, ET.ParseError) as error:
        parser.error(str(error))

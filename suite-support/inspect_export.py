"""Read real exports without pretending this format check executes analysis."""

import argparse
import json
import xml.etree.ElementTree as ET
from pathlib import Path


def inspect(path, kind):
    payload = path.read_bytes()
    if not payload:
        raise ValueError("Export is empty")
    if kind == "png":
        if payload[:8] != b"\x89PNG\r\n\x1a\n":
            raise ValueError("PNG signature is missing")
        detail = {"format": "PNG", "width": int.from_bytes(payload[16:20], "big"),
                  "height": int.from_bytes(payload[20:24], "big")}
        if not detail["width"] or not detail["height"]:
            raise ValueError("PNG dimensions are empty")
    elif kind == "svg":
        root = ET.fromstring(payload)
        if root.tag.rsplit("}", 1)[-1] != "svg":
            raise ValueError("SVG root is missing")
        detail = {"format": "SVG"}
    elif kind in ("mermaid", "markdown"):
        text = payload.decode("utf-8")
        if kind == "mermaid" and not any(word in text for word in ("flowchart", "graph ", "sequenceDiagram")):
            raise ValueError("Mermaid diagram declaration is missing")
        detail = {"format": kind, "characters": len(text)}
    else:
        data = json.loads(payload)
        if kind == "sarif":
            if data.get("version") != "2.1.0" or not isinstance(data.get("runs"), list) or not data["runs"]:
                raise ValueError("Expected SARIF 2.1.0 with runs")
            detail = {"format": "SARIF", "runs": len(data["runs"])}
        elif kind == "impact":
            required = {"schemaVersion", "baseIdentity", "headIdentity", "complete", "summary", "impacts"}
            if not required <= data.keys():
                raise ValueError("Impact comparison/verdict fields are missing")
            detail = {key: data[key] for key in ("baseIdentity", "headIdentity", "complete", "summary")}
        else:
            required = {"schemaVersion", "projectId", "runStatus", "partial", "analysisContext", "coverage", "nodes", "edges", "findings"}
            if not required <= data.keys():
                raise ValueError("Analysis identity/scope/model fields are missing")
            detail = {key: data[key] for key in ("projectId", "runStatus", "partial", "coverage")}
    return {"path": str(path.resolve()), "bytes": len(payload), "format_inspection": detail,
            "boundary": "Format inspection only; completeness and live IDEA identity require separate checks"}


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("path", type=Path)
    parser.add_argument("--kind", choices=("analysis", "impact", "sarif", "svg", "png", "mermaid", "markdown"), required=True)
    args = parser.parse_args()
    try:
        print(json.dumps(inspect(args.path, args.kind)))
    except (ValueError, ET.ParseError) as error:
        parser.error(str(error))

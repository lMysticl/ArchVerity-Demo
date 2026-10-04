"""Fail when the QA workbench omits a registered plugin entry point."""

import argparse
import json
import re
import xml.etree.ElementTree as ET
from pathlib import Path

PROJECT = Path(__file__).resolve().parents[1]
SOURCE = PROJECT.parents[1]
GROUPS = ("surfaces", "actions", "mcp", "processCommands", "debugCommands", "exports", "settings", "editorExtensions")
EDITOR_TAGS = {
    "fileEditorProvider", "fileType", "localInspection", "codeInsight.lineMarkerProvider",
    "psi.referenceContributor", "gotoDeclarationHandler", "multiHostInjector",
    "lang.documentationProvider", "completion.contributor",
}
LOCAL_PROCESS_INPUTS = {
    "RN_SCRIPT": {"package.json"},
    "ANSIBLE_SYNTAX_CHECK": {".yml", ".yaml"},
    "SHELLCHECK": {".sh", ".bash", ".zsh", ".bats"},
    "SHFMT_DIFF": {".sh", ".bash", ".zsh"},
    "BATS_TEST": {".bats"},
    "BASH_DEBUG": {".sh", ".bash", ".bats"},
}


def validate_process_inputs(entries, project=PROJECT):
    for name, item in entries.items():
        level = item.get("level")
        files = item.get("fixtures")
        if name in LOCAL_PROCESS_INPUTS:
            if level != "local_input" or not isinstance(files, list) or not files:
                raise AssertionError(f"Runnable process input missing: {name}")
            expected = LOCAL_PROCESS_INPUTS[name]
            for relative in files:
                path = Path(relative)
                if name == "RN_SCRIPT":
                    if path.name != "package.json":
                        raise AssertionError(f"RN_SCRIPT needs package.json: {relative}")
                    package = json.loads((project / path).read_text(encoding="utf-8"))
                    if "qa:verify" not in package.get("scripts", {}) or not (project / path.parent / "scripts/qa-verify.js").is_file():
                        raise AssertionError("RN_SCRIPT needs the runnable qa:verify script")
                elif path.suffix not in expected:
                    raise AssertionError(f"Unsupported file input for {name}: {relative}")
        elif level != "external_environment" or files != [] or not item.get("prerequisites"):
            raise AssertionError(f"External process command falsely claims a local fixture: {name}")


def enum_names(source, enum):
    match = re.search(rf"\benum class {re.escape(enum)}\b[^{{]*\{{([^}}]+)", source, re.S)
    if not match:
        raise AssertionError(f"Missing enum {enum}")
    body = match.group(1)
    if enum == "ArchFlowWorkspaceSurface":
        return set(re.findall(r"(?m)^    ([A-Z][A-Z_0-9]+)\(", body))
    return set(re.findall(r"\b[A-Z][A-Z_0-9]+\b", body))


def registered(source_root):
    frontend = source_root / "plugin-frontend/src/main"
    shared = source_root / "plugin-shared/src/main/kotlin/com/pavelputrenkov/archflow/shared"
    surface = (frontend / "kotlin/com/pavelputrenkov/archflow/frontend/ArchFlowSurfaceDeck.kt").read_text(encoding="utf-8")
    process = (shared / "DeveloperToolsDtos.kt").read_text(encoding="utf-8")
    exports = (shared / "RpcDtos.kt").read_text(encoding="utf-8")
    mcp = (source_root / "plugin-mcp/src/main/kotlin/com/pavelputrenkov/archflow/mcp/ArchVerityMcpToolset.kt").read_text(encoding="utf-8")
    descriptor = ET.parse(frontend / "resources/archflow.frontend.xml").getroot()
    backend = ET.parse(source_root / "plugin-backend/src/main/resources/archflow.backend.xml").getroot()
    extensions = descriptor.findall("./extensions/*") + backend.findall("./extensions/*")
    def editor_key(entry):
        implementation = entry.attrib.get("shortName") or entry.attrib.get("implementation") or entry.attrib.get("implementationClass") or ""
        language = f":{entry.attrib['language']}" if "language" in entry.attrib else ""
        return f"{entry.tag}:{implementation.rsplit('.', 1)[-1]}{language}"
    return {
        "surfaces": enum_names(surface, "ArchFlowWorkspaceSurface"),
        "actions": {action.attrib["id"] for action in descriptor.findall("./actions/action")},
        "mcp": set(re.findall(r"suspend fun (archverity_[a-z_]+)\(", mcp)),
        "processCommands": enum_names(process, "DeveloperProcessCommandDto"),
        "debugCommands": enum_names(process, "DeveloperDebugCommandDto"),
        "exports": enum_names(exports, "ExportFormat"),
        "settings": {entry.attrib["id"] for entry in extensions if entry.tag in {"applicationConfigurable", "projectConfigurable"}},
        "editorExtensions": {editor_key(entry) for entry in extensions if entry.tag in EDITOR_TAGS},
    }


def verify(source_root=SOURCE, require_source=False):
    matrix = (PROJECT / "QA_MATRIX_RU.md").read_text(encoding="utf-8")
    contract = json.loads((PROJECT / "qa-support/coverage.json").read_text(encoding="utf-8"))
    if set(contract) != set(GROUPS):
        raise AssertionError(f"Coverage groups differ: {set(contract) ^ set(GROUPS)}")
    for group, entries in contract.items():
        if not entries:
            raise AssertionError(f"Empty coverage group: {group}")
        for name, item in entries.items():
            case = item.get("case")
            files = item.get("fixtures")
            if not case or case not in matrix or not isinstance(files, list) or (not files and group != "processCommands"):
                raise AssertionError(f"Unbound coverage entry: {group}.{name}")
            for relative in files:
                path = Path(relative)
                if path.is_absolute() or ".." in path.parts or not (PROJECT / path).is_file():
                    raise AssertionError(f"Missing or unsafe fixture for {group}.{name}: {relative}")
    validate_process_inputs(contract["processCommands"])
    descriptor = source_root / "plugin-frontend/src/main/resources/archflow.frontend.xml"
    if not descriptor.is_file():
        if require_source:
            raise AssertionError(f"Plugin source unavailable: {source_root}")
        status = "source comparison skipped (portable standalone copy)"
    else:
        current = registered(source_root)
        for group in GROUPS:
            covered = set(contract[group])
            if current[group] != covered:
                raise AssertionError(
                    f"{group}: missing={sorted(current[group] - covered)}, stale={sorted(covered - current[group])}"
                )
        status = "registered plugin surfaces, actions, MCP tools, commands, exports, settings and editor extensions match"
    return {
        "entries": {group: len(contract[group]) for group in GROUPS},
        "process_inputs": {
            "local_input": sum(item["level"] == "local_input" for item in contract["processCommands"].values()),
            "external_environment": sum(item["level"] == "external_environment" for item in contract["processCommands"].values()),
        },
        "source": status,
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--plugin-source", type=Path, default=SOURCE)
    parser.add_argument("--require-source", action="store_true")
    args = parser.parse_args()
    print(json.dumps({"status": "PASS", "coverage": verify(args.plugin_source, args.require_source)}, ensure_ascii=False))

"""Bind every registered entry point and feature to public fixture/guide inputs."""

import argparse
import ast
import json
import os
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "projects/workspace/qa-support"))
from verify_coverage import GROUPS, verify
from apply_impact import SCENARIOS


def catalog(features, entries):
    lines = ["# Function and input catalog", "",
             "Generated from `suite-support/features.json` and the workspace's registered-entry contract.",
             "Each row is an acceptance recipe. It is not a PASS receipt for an unobserved IDEA/device action.", "",
             "## Capabilities", "", "| ID / function | Input | Action | Observable result | Prerequisite / guide |",
             "| --- | --- | --- | --- | --- |"]
    def cell(value):
        return str(value).replace("|", "\\|").replace("\n", " ")
    for feature in features:
        inputs = ", ".join(f"[{Path(value).name}](../{value})" for value in feature["inputs"])
        guide = f"[Guide](../{feature['guide']}) — {feature['requires']}"
        lines.append("| " + " | ".join(map(cell, (f"{feature['id']} — {feature['title']}", inputs,
                                                        feature["action"], feature["expected"], guide))) + " |")
    lines.extend(["", "## Registered IDEA entry points", "",
                  "All entries below bind to the executable/manual case in [QA matrix](../projects/workspace/QA_MATRIX_RU.md).",
                  "Process commands also use the complete [mobile table](../projects/mobile-lab/README.md) and [environment guide](ENVIRONMENT_CHECKS_RU.md).",
                  "The workspace-only coverage preserves its truthful six local inputs and sixteen external environments; the mobile app supplies additional real inputs after setup.", ""])
    for group in GROUPS:
        lines.extend([f"### {group} ({len(entries[group])})", "", "| Entry | Case | Workspace fixture |", "| --- | --- | --- |"])
        for name, entry in entries[group].items():
            fixtures = ", ".join(f"[{Path(value).name}](../projects/workspace/{value})" for value in entry["fixtures"]) or "See mobile/environment setup"
            lines.append(f"| {cell(name)} | {entry['case']} | {cell(fixtures)} |")
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def check(plugin_source=None, require_source=False, write_catalog=False):
    features = json.loads((ROOT / "suite-support/features.json").read_text(encoding="utf-8"))
    entries = json.loads((ROOT / "projects/workspace/qa-support/coverage.json").read_text(encoding="utf-8"))
    if len({item["id"] for item in features}) != len(features):
        raise ValueError("Feature IDs must be unique")
    for feature in features:
        if set(feature) != {"id", "title", "inputs", "action", "expected", "guide", "requires"} or not feature["inputs"]:
            raise ValueError(f"Incomplete feature recipe: {feature.get('id')}")
        for relative in [*feature["inputs"], feature["guide"]]:
            path = Path(relative)
            if path.is_absolute() or ".." in path.parts or not (ROOT / path).is_file():
                raise ValueError(f"Missing/unsafe input for {feature['id']}: {relative}")
        if any(not feature[key].strip() for key in ("action", "expected", "requires")):
            raise ValueError(f"Missing acceptance observation: {feature['id']}")
    source = plugin_source if plugin_source else ROOT / "source-unavailable"
    registration = verify(source, require_source)
    for name, replacements in SCENARIOS.items():
        changed = {}
        for relative, before, after in replacements:
            original = changed.get(relative, (ROOT / "projects/workspace" / relative).read_text(encoding="utf-8"))
            if original.count(before) != 1:
                raise ValueError(f"Scenario drift: {name}: {relative}")
            changed[relative] = original.replace(before, after, 1)
    mobile = ROOT / "projects/mobile-lab"
    package = json.loads((mobile / "package.json").read_text(encoding="utf-8"))
    lock = json.loads((mobile / "package-lock.json").read_text(encoding="utf-8"))
    if lock["packages"][""]["dependencies"] != package["dependencies"]:
        raise ValueError("Mobile lockfile does not bind the app's dependencies")
    for name in ("expo", "react-native"):
        if not re.fullmatch(r"\d+\.\d+\.\d+", package["dependencies"][name]):
            raise ValueError("Mobile dependency is not exactly pinned")
    if "registerRootComponent" not in (mobile / "index.js").read_text() or "ARCHVERITY_DEMO_CLICK" not in (mobile / "App.js").read_text():
        raise ValueError("Missing real mobile entry/screen; a detection-only package is insufficient")
    process_docs = (mobile / "README.md").read_text(encoding="utf-8") + (ROOT / "docs/ENVIRONMENT_CHECKS_RU.md").read_text(encoding="utf-8")
    for name in entries["processCommands"]:
        if name not in process_docs:
            raise ValueError(f"Process command has no setup/expected-result recipe: {name}")
    excluded = {"node_modules", "build", "work", ".gradle", ".git", "__pycache__", ".idea"}
    python_files = 0
    for directory, children, files in os.walk(ROOT):
        children[:] = [child for child in children if child not in excluded]
        for name in files:
            if name.endswith(".py"):
                path = Path(directory) / name
                ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
                python_files += 1
    expected = catalog(features, entries)
    target = ROOT / "docs/FEATURE_CATALOG.md"
    if write_catalog:
        target.write_text(expected, encoding="utf-8", newline="\n")
    elif not target.is_file() or target.read_text(encoding="utf-8") != expected:
        raise ValueError("Feature catalog drifted; use --write-catalog after reviewing features.json")
    return {"status": "INPUT_CONTRACT_PASS", "features": len(features), "entry_points": sum(registration["entries"].values()),
            "registered": registration, "isolated_mutations": len(SCENARIOS), "python_sources": python_files,
            "boundary": "Prepared inputs and source matching; live IDEA/device/licensing observations remain separate"}


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--plugin-source", type=Path)
    parser.add_argument("--require-source", action="store_true")
    parser.add_argument("--write-catalog", action="store_true")
    args = parser.parse_args()
    try:
        print(json.dumps(check(args.plugin_source, args.require_source, args.write_catalog)))
    except (ValueError, AssertionError) as error:
        parser.error(str(error))

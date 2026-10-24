"""Validate the public ask-before-edit lab's inputs; actual IDE and agent answers are recorded separately."""

import importlib.util
import json
from pathlib import Path

LAB = Path(__file__).resolve().parents[1] / "projects/ask-before-edit"


def load_scenarios():
    spec = importlib.util.spec_from_file_location("ask_before_edit_scenarios", LAB / "qa-support/apply_scenario.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def check():
    for module, folder, suffix in (("billing-service", "src/main/kotlin", ".kt"), ("orders-service", "src/main/java", ".java")):
        sources = list((LAB / module / folder).rglob("*" + suffix))
        if not sources or any(p.relative_to(LAB / module / folder).parts[0] != "demo" for p in sources):
            raise ValueError("Ask-before-edit lab needs business sources and real libraries, not framework stubs")
    for relative in ("README.md", "build.gradle.kts", "settings.gradle.kts", ".archflow.yml", "gradlew", "gradlew.bat",
                     "gradle/wrapper/gradle-wrapper.jar", "billing-service/src/main/resources/application.yml"):
        if not (LAB / relative).is_file():
            raise ValueError(f"Missing ask-before-edit input: {relative}")
    if "context-path: /billing" not in (LAB / "billing-service/src/main/resources/application.yml").read_text(encoding="utf-8"):
        raise ValueError("The lab's route must keep billing's context path")
    scenarios = load_scenarios()
    for name, edits in scenarios.SCENARIOS.items():
        for relative, before, after in edits:
            path = Path(relative)
            if path.is_absolute() or ".." in path.parts or before == after or path.suffix not in {".java", ".kt"}:
                raise ValueError(f"Unsafe/empty planned edit: {name}")
            if (LAB / path).read_bytes().count(before.encode()) != 1:
                raise ValueError(f"Planned edit anchor changed: {name}: {relative}")
        planned = json.loads(scenarios.planned_edits(name))
        if planned != [{"path": p, "old": o, "new": n} for p, o, n in edits]:
            raise ValueError(f"Printed edits_json differs from the applied edit: {name}")
    return {"status": "ASK_BEFORE_EDIT_INPUTS_PASS", "scenarios": list(scenarios.SCENARIOS),
            "boundary": "Inputs and planned edits only; What breaks if…, simulate_change and the review are observed in IDEA"}

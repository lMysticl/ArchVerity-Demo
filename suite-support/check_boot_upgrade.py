"""Validate the public upgrade lab's inputs; actual wire/IDE results are separate."""

import importlib.util
from pathlib import Path

LAB = Path(__file__).resolve().parents[1] / "projects/boot-upgrade"


def load_scenarios():
    spec = importlib.util.spec_from_file_location("boot_upgrade_scenarios", LAB / "qa-support/apply_scenario.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def check():
    for module in ("billing-service", "orders-service"):
        sources = list((LAB/module/"src/main/java").rglob("*.java"))
        if not sources or any(not p.relative_to(LAB/module/"src/main/java").parts[0] == "demo" for p in sources):
            raise ValueError("Public upgrade lab needs business sources and real libraries, not framework stubs")
    for relative in ("README.md", "build.gradle.kts", "settings.gradle.kts", ".archflow.yml", "gradlew",
                     "gradlew.bat", "gradle/wrapper/gradle-wrapper.jar", "verification/verify_wire.py",
                     "verification/src/demo/verification/WireProbe.java"):
        if not (LAB/relative).is_file():
            raise ValueError(f"Missing upgrade input: {relative}")
    recipes = load_scenarios().SCENARIOS
    for name, edits in recipes.items():
        for relative, before, after in edits:
            path = Path(relative)
            if path.is_absolute() or ".." in path.parts or before == after:
                raise ValueError(f"Unsafe/empty upgrade scenario: {name}")
            if (LAB/path).read_bytes().count(before.encode()) != 1:
                raise ValueError(f"Upgrade scenario anchor changed: {name}: {relative}")
    return {"status": "UPGRADE_INPUTS_PASS", "scenarios": list(recipes),
            "boundary": "Real-library inputs; run smoke_boot_upgrade.py for observed wire behavior"}

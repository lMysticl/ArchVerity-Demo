"""Validate the public stale-mocks lab's inputs; actual test, call and IDE results are separate."""

import importlib.util
from pathlib import Path

LAB = Path(__file__).resolve().parents[1] / "projects/stale-mocks"
STUB = "orders-service/src/test/java/demo/orders/BillingInvoiceTest.java"


def load_scenarios():
    spec = importlib.util.spec_from_file_location("stale_mocks_scenarios", LAB / "qa-support/apply_scenario.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def check():
    for module in ("billing-service", "orders-service"):
        sources = list((LAB/module/"src/main/java").rglob("*.java"))
        if not sources or any(not p.relative_to(LAB/module/"src/main/java").parts[0] == "demo" for p in sources):
            raise ValueError("Public stale-mocks lab needs business sources and real libraries, not framework stubs")
    for relative in ("README.md", "build.gradle.kts", "settings.gradle.kts", ".archflow.yml", "gradlew",
                     "gradlew.bat", "gradle/wrapper/gradle-wrapper.jar", STUB, "verification/verify_stale_mock.py",
                     "verification/src/demo/verification/RealCall.java"):
        if not (LAB/relative).is_file():
            raise ValueError(f"Missing stale-mocks input: {relative}")
    sent = (LAB/"billing-service/src/main/java/demo/billing/InvoiceView.java").read_text(encoding="utf-8")
    faked = (LAB/STUB).read_text(encoding="utf-8")
    # The lab's point: the provider renamed the field, the consumer's fake still answers with the old name.
    if "String invoiceId" not in sent or '\\"id\\": \\"42\\"' not in faked or "andRespond(" not in faked:
        raise ValueError("Stale-mocks baseline must keep the renamed provider field and the old fake")
    recipes = load_scenarios().SCENARIOS
    for name, edits in recipes.items():
        for relative, before, after in edits:
            path = Path(relative)
            if path.is_absolute() or ".." in path.parts or before == after:
                raise ValueError(f"Unsafe/empty stale-mocks scenario: {name}")
            if (LAB/path).read_bytes().count(before.encode()) != 1:
                raise ValueError(f"Stale-mocks scenario anchor changed: {name}: {relative}")
    return {"status": "STALE_MOCK_INPUTS_PASS", "scenarios": list(recipes),
            "boundary": "Real-library inputs; run the lab's tests, realCall and verify_stale_mock.py for observed behavior"}

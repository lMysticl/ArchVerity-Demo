"""Check the lab's two observations: orders' test result and what orders reads from the real billing."""

import argparse
import json
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def tests():
    reports = sorted((ROOT / "orders-service/build/test-results/test").glob("TEST-*.xml"))
    assert reports, "Run ./gradlew :orders-service:test first"
    totals = {"tests": 0, "failures": 0, "errors": 0, "skipped": 0}
    for report in reports:
        suite = ET.parse(report).getroot()
        for key in totals:
            totals[key] += int(suite.get(key, 0))
    return totals


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--fixed", action="store_true", help="expect the state after qa-support/apply_scenario.py --scenario fix")
    fixed = parser.parse_args().fixed
    result = tests()
    real = json.loads((ROOT / "build/real-call/real-call.json").read_text("utf-8"))
    sent = json.loads(real["billingJson"])
    assert result["tests"] > 0 and result["failures"] == result["errors"] == 0, f"orders' tests are not green: {result}"
    assert set(sent) == {"invoiceId", "total"}, f"Unexpected billing answer: {sent}"
    if fixed:
        assert real["ordersId"] == "42", "After the fix orders must read the invoice id from billing's real answer"
        status = "STALE_MOCK_FIXED"
    else:
        assert real["ordersId"] is None, "The baseline must show orders losing the id against the real billing"
        status = "STALE_MOCK_CONFIRMED"
    print(json.dumps({"status": status, "ordersTests": result, "billingSends": sorted(sent),
                      "ordersReadsId": real["ordersId"],
                      "boundary": "Real Spring Boot 3.5.15 libraries on loopback; not an ArchVerity scan result"}))


if __name__ == "__main__":
    main()

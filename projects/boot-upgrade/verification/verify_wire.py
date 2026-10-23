"""Assert actual Spring Boot mapper observations, never fabricate an IDEA result."""

import argparse
import json
from pathlib import Path


def verify(root, fixed=False):
    old, new = [json.loads((root / f"boot{generation}.json").read_text(encoding="utf-8")) for generation in (3, 4)]
    assert (old["bootVersion"], new["bootVersion"]) == ("3.5.15", "4.1.1"), "Wrong reproduction versions"
    assert old["mapper"].startswith("com.fasterxml.jackson.") and new["mapper"].startswith("tools.jackson."), "Wrong mapper generation"
    assert (old["monthJson"], new["monthJson"]) == ('"JANUARY"', '1'), "Month wire defaults changed"
    assert (old["monthNumberOne"], new["monthNumberOne"]) == ("FEBRUARY", "JANUARY"), "Month numeric interpretation changed"
    for kind in ("nullPrimitive", "absentPrimitive"):
        assert old[kind] and not new[kind], f"Primitive boundary changed: {kind}"
    if fixed:
        assert json.loads(old["invoiceJson"]) == json.loads(new["invoiceJson"]), "Fixed contract still differs on the wire"
        assert all(r[k] for r in (old, new) for k in ("readsOwnInvoice", "readsLegacyInvoice")), "Fixed reader rejects an invoice"
        assert old["enumJson"] == new["enumJson"] == '"PAID"', "Explicit enum contract was not preserved"
    else:
        assert (old["enumJson"], new["enumJson"]) == ('"PAID"', '"Paid"'), "Enum defaults changed"
        assert old["readsLegacyInvoice"] and not new["readsLegacyInvoice"], "Broken reader control did not discriminate"
    return {"status": "WIRE_FIX_PASS" if fixed else "WIRE_DIFFERENCES_CONFIRMED",
            "versions": [old["bootVersion"], new["bootVersion"]],
            "boundary": "Real auto-configured Jackson; separate from an ArchVerity IDE verdict"}


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--fixed", action="store_true")
    parser.add_argument("--input", type=Path, default=Path(__file__).resolve().parents[1] / "build/wire")
    args = parser.parse_args()
    print(json.dumps(verify(args.input, args.fixed)))

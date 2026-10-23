# Observed Boot 3/4 JSON — 23 October 2026

These are real auto-configured mapper observations from the public
[boot-upgrade lab](../../../projects/boot-upgrade/README.md), on Windows with
Temurin JDK 21.0.12+1. The runner compiled both service modules and invoked
separate Java processes for Boot 3.5.15 and Boot 4.1.1. No service or broker ran.
Input and output hashes are recorded in [manifest.json](manifest.json).

| State | Boot 3 | Boot 4 | Observed check |
| --- | --- | --- | --- |
| Original fixture | [JSON](baseline-boot3.json) | [JSON](baseline-boot4.json) | `WIRE_DIFFERENCES_CONFIRMED`: enum spelling, Month and primitive reader behavior differ |
| Explicit fixture fix | [JSON](fixed-boot3.json) | [JSON](fixed-boot4.json) | `WIRE_FIX_PASS`: identical invoice JSON; both readers accept the demonstrated invoices |

Reproduce from the suite root:

```powershell
python -B -X utf8 suite-support/smoke_boot_upgrade.py --output ../archverity-wire-check
```

The output path must be new. The helper prepares two standalone Git projects,
retains build logs and records the actual mapper observations.
The primitive and numeric-month negative controls intentionally still show
the difference in library defaults after the invoice contract is made explicit.

These receipts prove library behavior and the compiled fixture fix. They do
not claim a fresh installed-plugin scan, paid entitlement check, MCP connection
or IDE screenshot. Use the lab's expected observations and
[run record](../../RUN_RECORD.md) for those separate checks. Historical recordings
elsewhere in the repository retain their original plugin versions.

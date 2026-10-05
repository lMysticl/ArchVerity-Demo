# Real local runtime and verification evidence

[Пошаговый запуск в общем demo route](../../docs/DEMO_RUNBOOK_RU.md#6-runtime-beans-и-verification-evidence)
показывает подготовку отдельной копии, реальный IDEA export и capture.

This Spring Boot 3.5.12 app exposes only loopback HTTP on port 18430, including
the real Actuator `/actuator/beans` response. Kafka factory/template beans are
created; no broker is started, no message is sent and no listener consumes.
JDK 21 is sufficient; the BOM pins the Spring family for this separate project.

Prepare a standalone clean copy from the suite root:

```powershell
python suite-support/prepare_project.py --project runtime-evidence --output D:\CodexData\Temp\archverity-runtime-demo
```

In that new project, with JDK 21 selected, run in its terminal:

```powershell
python run_local.py
```

The launcher requires this project to be its own clean Git root. It starts
Gradle's application task and binds the running app to the exact HEAD/config
hash. `GET http://127.0.0.1:18430/demo-identity` reports those identities.
Ctrl+C stops the task-owned process. A server from another copy is a
WRONG_TARGET; never capture its response as evidence for the current copy.

Open this **same** isolated project as Gradle in IDEA. With a real entitled
ArchVerity build, Analyze using the already configured imports. The first scan
has missing evidence inputs and should retain explicit UNKNOWN; export its
current full Analysis JSON into the ignored `work/analysis.json`. Keep source
and `.archflow.yml` unchanged. The export's `analysisContext.fingerprint` must
belong to this configured checkout; the operator records the IDEA/project
identity in the [run record](../../docs/RUN_RECORD.md).

```powershell
python capture.py --snapshot work/analysis.json --format pact
```

The producer fetches real `/actuator/beans`, checks the live revision/config
identity, executes a real local GET `/payments/42`, compares its response, and
writes five new files under `reports/`:

- Raw `beans.json` and its timestamp/hash/revision/context metadata.
- `pact-result.json` (or `drift-result.xml`) with the actual local check result.
- Complete `verification-metadata.json` with local run ID and `local-demo-http-1` version.
- Canonical `payment.verification.archflow.json` with raw-file SHA-256 and `trust=LOCAL_FILE`.

Reports stay ignored, preserving the source HEAD. Reanalyze promptly: runtime
evidence has an explicit 300-second max age. Inspect `demoTemplate` →
`demoProducerFactory`, and `demoListenerFactory` → `demoConsumerFactory`, using
the actual bean types/dependencies and source metadata. A runtime observation
does not prove a serializer's behavior or a wire-compatible consumer contract.

For **FAIL**, prepare another fresh copy, stop the previous app, run the new
copy, export its own current snapshot, then use `--negative`. It requests the
app's deliberate HTTP error route and records the actual failing check. For
Drift-shaped JUnit use `--format drift`, again in a new copy. Existing evidence
is never overwritten. Neither format claims execution by a Pact/Drift product:
this is the explicitly named local demo verifier, testing supported import
formats and LOCAL_FILE handling. For actual vendor execution use independently
obtained reports, versions and run metadata from that verifier.

Run each rejection control independently in disposable copies:

| Control | Expected consumer observation |
| --- | --- |
| Missing report | UNKNOWN with exact missing input |
| Alter raw bytes but retain sourceSha256 | Hash mismatch → UNKNOWN |
| Wrong revision/configuration/service/environment/context | Identity mismatch → UNKNOWN |
| Wait beyond maxAgeSeconds | Expired runtime observation → UNKNOWN |
| Dirty tracked source or unsaved editor change | Runtime and verification acceptance fail closed |
| Verification FAIL | FAIL remains visible; an imported declaration cannot turn it into PASS |
| Real runtime types/dependencies vs proxies/ambiguity | Recognized unique binding only; unknown/custom/ambiguous types remain UNKNOWN |

The [smoke command](../../suite-support/smoke_runtime.py) builds/runs the real app
in an isolated project and validates raw beans, identity and actual HTTP results.
Its synthetic snapshot input is an explicit **producer-test input**, never
evidence of an IDEA scan. Full importer acceptance still requires the actual
IDEA export and live consumer observations above.

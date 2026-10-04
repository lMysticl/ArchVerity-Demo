# A record for each observed run

Copy this template into a task-owned `work/` directory. Do not commit customer
evidence, credentials, raw secrets or unbounded logs. Keep screenshots/logs as
evidence files and record their paths and decisive observations here.

```text
Run ID:
Started at (UTC):
Demo repository commit:
Isolated project path and Git HEAD:
IDE product/version/build:
Installed ArchVerity version and ZIP SHA-256:
OS / local or Split Mode / frontend and backend identity:
License state independently observed:
Viewport/theme/scale for visual checks:

Feature or QA case ID:
Input / scenario / exact selected project:
Preparation status: READY | BLOCKED
Observed result: PASS | FAIL | NOT RUN | BLOCKED
Decisive observation:
Evidence file and SHA-256, if applicable:
Exact unmet prerequisite, if BLOCKED:
Next independent check:
```

A test input exists when its source/format is present. A process passes when
the selected process or server really produces the expected outcome. An IDEA
action passes only after its UI/backend consumer is observed on the same
project and version. An untested case stays NOT RUN; a missing device, MCP
server, entitlement or macOS stays BLOCKED. Counts of files/buttons or a green
Gradle build never convert those cases to PASS.

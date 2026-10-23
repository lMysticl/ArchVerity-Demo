# Evaluate ArchVerity 5.3.2 on a change you can inspect

**Which other service breaks when I change this contract?** Start with a
compiling example, find the mismatch, inspect both sides, then fix and recheck.
Continue to pre-edit simulation, an upgrade risk, a team report and your coding
agent. [Русский подробный маршрут](PRODUCT_TOUR_RU.md) ·
[All-lab runbook](DEMO_RUNBOOK_RU.md) · [Record observations](RUN_RECORD.md).

Use JDK 21, Git, Python 3.10+, a supported IntelliJ IDEA and separately installed
ArchVerity 5.3.2 with a legitimate Trial/Pro. The Marketplace offers a 14-day
trial. First dependency downloads need a network; static contract examples need
no broker, database or running services. MCP needs a supported modern IDE,
JetBrains MCP Server and your own agent account.

## 1. A build passes; the HTTP contract does not

From the suite root:

```powershell
python -B -X utf8 suite-support/check_suite.py
python -B -X utf8 suite-support/prepare_project.py --project first-result --output ../archverity-first-demo
```

Open the output as a Gradle project, finish import/indexing and compile it with
`.\gradlew.bat classes` (`./gradlew classes` on Linux/macOS). In ArchVerity
Overview choose **Map this project**. Find `AFG-HTTP-001`: the Feign caller sends
POST while the provider accepts PUT. Open both source files, change the caller
to `@PutMapping`, save and refresh analysis. This mismatch should disappear.
Restore POST and recheck: the finding should return. [Exact source locations](../projects/first-result/README.md).

## 2. Ask before editing; check the real edit afterward

```powershell
python -B -X utf8 suite-support/prepare_project.py --project workspace --output ../archverity-review-demo
```

Import and analyze the clean HEAD. Inspect Overview's contracts, mismatches and
unresolved counterpart links. Open `payment-app/src/main/java/sample/payment/PaymentController.java`.
On a DTO field or mapping, invoke **ArchVerity: What Breaks If This Changes?**
through Find Action. Inspect the proposed changes, affected callers and evidence.
`git diff` must remain empty: this Java action computes in memory. You can also
try the Java Kafka `send` in `OrderPublisher.java`.

In the prepared project, after a complete clean-HEAD scan:

```powershell
python -B -X utf8 qa-support/apply_impact.py --project . --scenario http-method
```

Run Review against HEAD. Inspect the unchanged client and changed provider,
review the available **Apply fix**, then recheck. The specific break should
clear. Inspect the written diff; a fix must fit the intended API change.
Use fresh copies for `request-required`, `kafka-topic` and `combined-breaking`.
Use `response-optional-added` as a nonbreaking control and `manifest-missing`
as an UNKNOWN control. [All 19 isolated changes](ARCHITECTURE_WALKTHROUGH_RU.md).
[Current engine observations](CURRENT_VERIFICATION_RU.md) include a known
auto-fix limit when moving the demo's `@RetryableTopic` listener. Do not present
that case as an automatic fix success; the publisher and plain-listener paths
have separate measured outcomes.

## 3. A dependency upgrade changes JSON without changing the endpoint

```powershell
python -B -X utf8 suite-support/prepare_project.py --project boot-upgrade --output ../archverity-upgrade-demo
```

Analyze the new project and select **Check Spring Boot 4 upgrade**. Follow the
[English lab](../projects/boot-upgrade/README.md) for enum spelling, Month,
nullable values and missing primitive record components. It runs real
auto-configured Boot 3/4 mappers, provides explicit source fixes and checks the
result independently. The mapper-customization control must remain unproven.

## 4. Leave with something your team can use

Use **Copy for my team** in Overview; inspect the services, relative source
locations, upgrade risks and uncertainty. Export the specific Review as
Markdown/JSON and check its base revision. For an advanced trial, preview
**Publish contracts to team registry…** into a separate local registry checkout,
or **Add commit receipt check to CI…** into a disposable demo copy. Review the
generated instructions. Publishing a registry snapshot is a local write followed
by your normal Git process. The CI receipt verifies a recorded check for a tree;
it is neither a fresh source analysis nor a cryptographic signature.

## 5. Give your coding agent contract context

Open **Agents**, follow the selected client's connection steps and verify the
connection. Ask it to call `archverity_file_contracts` before changing the
controller, then `archverity_check_change` against HEAD afterward. Bind the
project directory explicitly. [All 18 MCP tools and controls](MCP_TOUR_RU.md).
A regression plan marked `NOT_EXECUTED` is a plan, not a test result; a model's
review does not override deterministic contract evidence.

## Explore the capabilities relevant to you

The [lab index](README.md) links Kafka profile/cluster cases, local
HTTP/WebSocket/gRPC, runtime evidence and Expo/React Native. **Tools** contains
Spring configuration, MyBatis, Ansible, Shell/Bats, ANSI, icons and keystore
utilities. Each has [concrete input and recovery recipes](ALL_FUNCTIONS_RU.md).
Devices, SSH, licensing and remote setups have separate prerequisites.

Repeat one useful evaluation on your own change during the trial: identify a
real consumer, understand the evidence or its limit, check the fix and share the
result. That repeatable answer is the purchase criterion. Preparation, a sample
compilation and a historical recording do not replace an observed plugin run.

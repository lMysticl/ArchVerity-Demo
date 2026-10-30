# Evaluate ArchVerity 5.8.2 on a change you can inspect

**Which other service breaks when I change this contract?** Start with a
compiling example, find the mismatch, inspect both sides, then fix and recheck.
Continue to pre-edit simulation, an upgrade risk, a team report and your coding
agent. [Русский подробный маршрут](PRODUCT_TOUR_RU.md) ·
[All-lab runbook](DEMO_RUNBOOK_RU.md) · [Record observations](RUN_RECORD.md).

Use JDK 21, Git, Python 3.10+, a supported IntelliJ IDEA and separately installed
ArchVerity 5.8.2 with a legitimate Trial/Pro. The Marketplace offers a 14-day
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
open **Map → Analyze Project**, then **Problems**. Find `AFG-HTTP-001`: the Feign caller sends
POST while the provider accepts PUT. Open both source files, change the caller
to `@PutMapping`, save and refresh analysis. This mismatch should disappear.
Restore POST and recheck: the finding should return. [Exact source locations](../projects/first-result/README.md).

## 2. Ask before editing; check the real edit afterward

```powershell
python -B -X utf8 suite-support/prepare_project.py --project workspace --output ../archverity-review-demo
```

Import and analyze the clean HEAD. Inspect **Map** for contracts and **Problems** for existing mismatches and
unresolved counterpart links. Open `payment-app/src/main/java/sample/payment/PaymentController.java`.
On a DTO field or mapping, invoke **ArchVerity: What Breaks If This Changes?**
through Find Action. Inspect the proposed changes, affected callers and evidence.
`git diff` must remain empty: this Java action computes in memory. You can also
try the Java Kafka `send` in `OrderPublisher.java`.

In the prepared project, after a complete clean-HEAD scan:

```powershell
python -B -X utf8 qa-support/apply_impact.py --project . --scenario http-method
```

Open **Changes → Summary**, select **HEAD → Current files**, and choose
**Check Changes** (or **Check Again**). Open **Details** for both source sides. Inspect the unchanged client and changed provider,
review the available **Apply fix**, then recheck. The specific break should
clear. Inspect the written diff; a fix must fit the intended API change.
Use fresh copies for `request-required`, `kafka-topic` and `combined-breaking`.
Use `response-optional-added` as a nonbreaking control and `manifest-missing`
as an UNKNOWN control. [All 19 isolated changes](ARCHITECTURE_WALKTHROUGH_RU.md).
[Current verification](CURRENT_VERIFICATION_RU.md) separates the passing 5.8.2
workspace corpus from the retained 5.3.2 retry-listener limitation. Historical
failures stay visible with their versions. Check the actual finding and written
fix in your run; a corpus result does not promise an automatic fix for every listener.

## 3. A dependency upgrade changes JSON without changing the endpoint

```powershell
python -B -X utf8 suite-support/prepare_project.py --project boot-upgrade --output ../archverity-upgrade-demo
```

Analyze the new project and select **Check Spring Boot 4 upgrade**. Follow the
[English lab](../projects/boot-upgrade/README.md) for enum spelling, Month,
nullable values and missing primitive record components. It runs real
auto-configured Boot 3/4 mappers, provides explicit source fixes and checks the
result independently. The mapper-customization control must remain unproven.

## 3a. Follow a Kafka payload through Spring Boot

Use the [Boot Kafka lab](../projects/kafka-boot-lab/README.md) for the new 5.8
source/configuration proof. From the suite root, prepare a fresh copy:

```powershell
python -B -X utf8 suite-support/prepare_boot_kafka_case.py --boot-line 35 --case remove-required --output ../archverity-boot-kafka-demo
```

Use `--boot-line 40` in another new output for Boot 4. Import both modules with
JDK 21, finish indexing and compile the prepared project with `.\gradlew.bat classes`
(`./gradlew classes` on Linux/macOS). No broker is started.

Open **Changes → Summary**, compare its committed HEAD with current files and
choose **Check Changes**. The producer no longer supplies required `tenant`,
while the reader still requires it. In **Details**, inspect both DTOs and the
selected template/listener and JSON serializer/deserializer configuration.
Restore the producer's exact `Event.java` from HEAD, compile and **Check Again**
with the same base: that removed-field break should disappear.

Use separate copies for `add-optional` (default reader accepts the extra field),
`customizer-control` (named **Needs review**) and `historical-reader` (current
pair matches, but the reader also has to handle the producer shape at the base).
The lab explains each input and its recovery. A Git base is historical source,
not a statement about retained broker records, delivery or the deployed version.
The older [K01–K12 profile lab](../projects/kafka-profile-lab/README.md) remains a
separate scope; its historical exports are not a fresh run of these Boot cases.

## 4. Leave with something your team can use

After a complete project scan, use **Copy for my team** in **Problems**; inspect the services, relative source
locations, upgrade risks and uncertainty. Use **Changes → Export review** for the specific comparison as
Markdown/JSON and check its base revision. For an advanced trial, preview
**Publish contracts to team registry…** into a separate local registry checkout,
or **Add commit receipt check to CI…** into a disposable demo copy. Review the
generated instructions. Publishing a registry snapshot is a local write followed
by your normal Git process. The CI receipt verifies a recorded check for a tree;
it is neither a fresh source analysis nor a cryptographic signature.

## 5. Give your coding agent contract context

Open **Agents**, follow the selected client's connection steps and verify the
connection. Ask it to call `archverity_file_contracts`, then
`archverity_simulate_change` with the exact ordered edits before writing them.
Inspect the proposed result, write the intended edit, run the relevant tests and
call `archverity_check_change` against HEAD. Bind the same project directory
explicitly. The simulation accepts at most 20 Java/Kotlin replacements and does
not create a commit receipt. [All 19 MCP tools and controls](MCP_TOUR_RU.md).
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

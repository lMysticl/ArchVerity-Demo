# Ask what an edit breaks before you write it

Two services compile on Spring Boot **3.5.15**. `billing` is written in Kotlin
and serves `GET /invoices/{id}` under the context path `/billing`. `orders` is
Java: it calls `GET /billing/invoices/{id}` with `RestClient` and reads `id` and
`total`. ArchVerity **5.5.0** answers what a planned edit would break before
the edit exists: in the editor with **What breaks if…**, and for a coding agent
with the MCP tool `archverity_simulate_change`. Nothing is written by the answer.

[All-lab launch guide](../../docs/DEMO_RUNBOOK_RU.md) · [MCP tour](../../docs/MCP_TOUR_RU.md) ·
[Boot upgrade lab](../boot-upgrade/README.md)

## Prepare a separate project

Run from the **ArchVerity-Demo repository root**:

```powershell
python -B -X utf8 suite-support/prepare_project.py --project ask-before-edit --output ../archverity-ask-demo
```

Open `archverity-ask-demo` as a Gradle project with JDK 21, allow the first
dependency download, finish import/indexing and activate a legitimate
Trial/Pro in the separately installed plugin. No server, database, Docker or
broker is required; `billing.example.test` is a synthetic address. The pins are
for reproduction, not recommendations.

## 1. Map the project

In ArchVerity **Overview**, run the analysis. Expected, not pre-recorded:

- 2 services, 1 link: `GET /billing/invoices/{id}` from `orders` to `billing`.
  The handler says `/invoices/{id}`; the route includes `server.servlet.context-path`
  from [billing's application.yml](billing-service/src/main/resources/application.yml).
  An `orders` call to `/invoices/{id}` would not match.
- 0 mismatches.
- One observation, not a verdict: **HTTP client read timeout not configured**
  for `RestClient.create(...)` in `BillingClient`, which Spring Boot does not configure.

If a service or the link is missing, check the import and the diagnostics first.

## 2. Ask in the editor

1. In [InvoiceController.kt](billing-service/src/main/kotlin/demo/billing/InvoiceController.kt)
   put the caret on `"/invoices/{id}"` and choose **What breaks if…**. The answer
   for a moved route is **Breaking** for `orders`.
2. In [InvoiceView.kt](billing-service/src/main/kotlin/demo/billing/InvoiceView.kt)
   put the caret on `val id`. The variants are *renamed on the wire* and
   *removed*; neither is a go-ahead, and both name `orders`. On `val note` a third
   variant, *becomes required*, appears: `id` is already required.

The source files do not change.

## 3. Ask from your coding agent

Connect the agent on ArchVerity's **Agents** tab, then let it call
`archverity_simulate_change` before it writes the edit. Print the exact
`edits_json` the scenarios below use:

```powershell
python -B -X utf8 qa-support/apply_scenario.py --scenario rename-field --print-edits
python -B -X utf8 qa-support/apply_scenario.py --scenario move-route --print-edits
```

Pass that array as the `edits_json` string with `"project_root":"<full path of the prepared project>"`.
Each edit replaces the one occurrence of `old` in that file. Expected: the moved
route is `BREAKING` for `orders`; the renamed field is `UNKNOWN` with
*Consumer reads a field that is no longer sent*. The answer is phrased as a
plan ("Do not write this edit yet") and ends with calling
`archverity_check_change` after writing. An `old` text that occurs zero or
several times, a path outside the project, or a non-Java/Kotlin file is
refused with the reason.

## 4. Make the edit and compare

On the untouched prepared baseline:

```powershell
python -B -X utf8 qa-support/apply_scenario.py --scenario rename-field
git diff
```

In **Review**, run **Analyze change** against `HEAD`. Expected, the same answer
the question got:

- **Can't confirm it's safe**: `orders` still maps a field this change stops sending.
  Deploy order: `orders`, then `billing`.
- The **Wire contract** card shows `id` as *not sent* by billing and read by
  orders: absent, it becomes null or the field's default.
- **Ways to fix**: keep the old name on the wire
  (`@JsonProperty("id") val invoiceId: String`), or read both names in `orders`
  first (`@JsonAlias("invoiceId")` on `id`), or confirm with `orders` that a
  missing value is harmless. These are suggestions; ArchVerity does not edit
  `orders`.

For the route, prepare another fresh copy and apply `--scenario move-route`.
Expected: **Not safe to merge**, breaks `orders`, with a fix that keeps the
previous route working next to the new one until `orders` moves.

Record the actual plugin/IDE version and what you observed with
[RUN_RECORD](../../docs/RUN_RECORD.md). If a side is unresolved, keep the reason;
do not turn `UNKNOWN` into a green result.

## Limits

- The answer comes from the current analysis: run it first. A Kotlin class that
  another file extends, or a file that customizes clients or JSON readers for
  its whole module, is not simulated: the answer is `UNKNOWN` with that reason.
- This is a source check. It does not run the services, and runtime
  configuration outside the sources is not executed.
- The helper refuses an existing destination, a dirty project or a changed
  fixture. It does not run `git reset`, discard manual edits or connect to
  services. For another scenario, prepare a new copy.

## Inspectable inputs

- [Billing handler](billing-service/src/main/kotlin/demo/billing/InvoiceController.kt),
  [response](billing-service/src/main/kotlin/demo/billing/InvoiceView.kt) and
  [context path](billing-service/src/main/resources/application.yml).
- [Orders caller](orders-service/src/main/java/demo/orders/BillingClient.java) and
  [reader](orders-service/src/main/java/demo/orders/InvoiceView.java).
- [Planned edits](qa-support/apply_scenario.py).

The business example adapts the product's `WhatIfKotlinFixtureTest` fixture,
with real Spring Boot dependencies instead of framework stubs.

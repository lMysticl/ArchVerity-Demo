# See a Spring Boot upgrade change the wire contract

Two services compile on Spring Boot **3.5.15**. `billing` writes an invoice;
`orders` reads it into a different record. Changing the JSON defaults can break
that boundary even when no controller signature changes. ArchVerity **5.3.2**
can inspect the supported upgrade risks before you change the dependencies.

[Русский маршрут продукта](../../docs/PRODUCT_TOUR_RU.md#переход-на-spring-boot-4) ·
[All-lab launch guide](../../docs/DEMO_RUNBOOK_RU.md) · [English tour](../../docs/PRODUCT_TOUR_EN.md)

## Prepare a separate project

Run from the **ArchVerity-Demo repository root**:

```powershell
python -B -X utf8 suite-support/prepare_project.py --project boot-upgrade --output ../archverity-upgrade-demo
```

Open the resulting `archverity-upgrade-demo` directory as a Gradle project.
Use JDK 21, allow the first dependency download, finish import/indexing and
activate a legitimate Trial/Pro in the separately installed plugin. No server,
database, Docker or broker is required. All service names are synthetic.
The reproduction pins are intentional; they are not deployment recommendations.

## Inspect the upgrade before editing

1. In ArchVerity **Overview**, use **Map this project** / refresh the analysis.
2. Open the HTTP link from `orders` to `billing`. Both sides must resolve to the
   source files below; if they do not, inspect import, scope and diagnostics first.
3. Choose **Check Spring Boot 4 upgrade**. These are the expected four supported
   risks on the resolved default-mapper pair, not a pre-recorded result:

| Field | What can change | Who is affected |
| --- | --- | --- |
| `status` | Billing's enum overrides `toString()`: `PAID` can become `Paid` | Orders still expects the old enum spelling |
| `period` | `Month.JANUARY` changes from `"JANUARY"` to `1` | A Jackson 2 reader interprets numeric `1` as February |
| `quantity` | Billing can send null into an `int` | Upgraded orders rejects null instead of taking zero |
| `discount` | Billing does not send this record component | Upgraded orders rejects the missing primitive |

Open the source locations and use **Copy for my team** in Overview. The report
should name the two services, the supported wire risks, locations and limits.
Record the actual plugin/IDE version and observed result with [RUN_RECORD](../../docs/RUN_RECORD.md).
If the mapper or route is unproven, retain that reason; do not convert UNKNOWN
into a green upgrade verdict. This check does not prove every Jackson feature
or a Kafka serializer compatible.

## Check the real JSON without ArchVerity

From the **prepared project directory**, run:

```powershell
.\gradlew.bat classes wireBoot3 wireBoot4 --console=plain
python -B -X utf8 verification/verify_wire.py
```

On Linux/macOS use `./gradlew`. The two Java processes load the real
auto-configured mappers from Boot 3.5.15 and 4.1.1. The same probe records JSON,
numeric-month interpretation and reader acceptance in `build/wire/boot3.json`
and `boot4.json`. Expected: `WIRE_DIFFERENCES_CONFIRMED`.
This independently demonstrates the library behavior. It does not impersonate
an ArchVerity scan, licence, GUI action or exported finding.
[Inspect the recorded before/after observations](../../docs/evidence/boot-upgrade-20261023/README.md).
The Boot 4 side gives the same observations on 4.0.9, 4.1.2 and 4.2.0-RC1:
[Boot 4 line rerun](../../docs/evidence/boot-upgrade-20261024-boot4-line/README.md).

## Make the wire contract explicit, then check again

The fix keeps enum names explicit with `@JsonValue`, represents the period as
a string on both sides and uses boxed reader components for nullable/missing
values. In a real application, choose the period format and null validation
with the contract owner; boxing changes the Java API's null handling.

On the untouched prepared baseline:

```powershell
python -B -X utf8 qa-support/apply_scenario.py --scenario fix
git diff
.\gradlew.bat classes wireBoot3 wireBoot4 --console=plain
python -B -X utf8 verification/verify_wire.py --fixed
```

Expected: `WIRE_FIX_PASS`; both mappers write the same invoice and the readers
accept the demonstrated payloads. Refresh ArchVerity and run the upgrade check
again. The four supported risks should clear; that is narrower than a guarantee
that the whole application is safe to upgrade. These edits are an explicit
demonstration script, not a claim that the plugin automatically applies all four.

## Check an uncertainty, not just the happy path

Prepare another fresh `boot-upgrade` copy. Run:

```powershell
python -B -X utf8 qa-support/apply_scenario.py --scenario mapper-unknown
```

This enables a mapper property in billing's application configuration. Refresh
the scan: billing's default mapper must no longer be treated as proven. Inspect
the reason in the upgrade result. This control shows the boundary of analysis;
the standalone JSON probe tests defaults and is not an oracle for this scenario.

For recovery, prepare a new copy. The helper refuses an existing destination,
dirty project or changed fixture. It does not run `git reset`, discard manual
edits, connect to services or upgrade your actual application.

## Inspectable inputs

- [Billing response](billing-service/src/main/java/demo/billing/InvoiceView.java),
  [enum](billing-service/src/main/java/demo/billing/InvoiceStatus.java) and
  [controller](billing-service/src/main/java/demo/billing/InvoiceController.java).
- [Orders reader](orders-service/src/main/java/demo/orders/InvoiceView.java) and
  [explicit HTTP caller](orders-service/src/main/java/demo/orders/BillingClient.java).
- [Real mapper probe](verification/src/demo/verification/WireProbe.java) and
  [assertions](verification/verify_wire.py).

The business example adapts the product's `BootUpgradeFixtureTest` fixture.
This public lab replaces framework stubs with real Maven dependencies and adds
an independent wire check. See the [Spring Boot migration guide](https://github.com/spring-projects/spring-boot/wiki/Spring-Boot-4.0-Migration-Guide)
and [Jackson 3 migration notes](https://github.com/FasterXML/jackson/blob/master/jackson3/MIGRATING_TO_JACKSON_3.md).

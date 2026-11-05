# Hard contract changes a current-only review can miss

These synthetic source cases target **ArchVerity 6.1.0** in a compatible IntelliJ
IDEA, with JDK 21 and a real active Trial/Pro entitlement. Use a fresh output for
each preparation command; the helpers refuse existing folders. Neither preparing
the sources nor a green compilation proves the plugin result. No service,
database, broker, production credentials or customer data is needed.

Run preparation from the demo repository root. **Capture the native baseline
before editing**, for all three cases below:

1. Prepare the clean baseline as described in the case. Open that folder as its
   own Gradle project, select JDK 21 and finish the import of **both modules** and
   indexing. Compile the clean sources with the command at the end of this guide.
2. With `git status --short` empty, run **Map → Analyze Project**, then check
   **Changes → HEAD → Current files**. Wait for a complete current result with no
   seeded contract change. This records the exact source/configuration context
   ArchVerity needs for the historical comparison.
3. Only now make the case's bounded edits. Keep that same project, Git HEAD,
   dependencies, `.archflow.yml` and analysis scope. Compile and check again.

A fresh broken copy is not a substitute for step 2. In particular, changing a
Feign client is dependency-sensitive: without an exact saved base the native
result can correctly remain **Needs review / BASE_UNAVAILABLE**, with an exact
base snapshot requested. More indexing or repeated checks of the changed sources
does not create that missing baseline. The expected trap verdict applies only
after its native baseline prerequisites are satisfied.

Record the actual IDEA/plugin version, project, base commit and complete result
with every capture. The ignored
`work/hard-case.json` binds the exact prepared source bytes and changes; it is a
preparation manifest, **not runtime evidence or an analyzer result**. Manual
mutations intentionally make that preparation manifest historical; keep actual
run results separately rather than relabeling it as current evidence.

## 1. Both routes changed together; no deployment order works

```powershell
python -B -X utf8 suite-support/prepare_hard_case.py --case rollout-cycle --state baseline --output ../hard-rollout
```

The baseline has a matching `PUT /payments/{paymentId}` client and provider.
Complete the native baseline steps above before making these two edits:

- In `payment-app/src/main/java/demo/payments/PaymentController.java`, change the
  class `@RequestMapping("/payments")` to `@RequestMapping("/v2/payments")`.
- In `order-app/src/main/java/demo/orders/PaymentClient.java`, change the Feign
  `path = "/payments"` to `path = "/v2/payments"`; keep `@PutMapping` unchanged.

Both current sides now use `/v2/payments/{paymentId}`. The current pair still
matches and compiles. Old client → new provider and new client → old provider do
not. In **Changes → Details**, inspect the top verdict strip; use
**Export review → Copy rollout plan** for the mixed-version explanation. Expected:
**no deployment order works as written** (`NO_ORDER`), even if ordinary
current-only contract impacts show no proven breaking change. In the recorded
6.1.0 native run, Summary showed only two compatible changes; Details combined
**No breaking changes found** with **As written, no deploy order is safe**.

The helper's default `--state broken` prepares these same two source edits in a
fresh folder for source inspection. For native analysis of that folder, restore
the two paths below first, capture its clean baseline, then reapply the two edits.
Preserve any desired candidate bytes outside the analyzed project before restoring.

Prepare a separate source reference for the exact expand repair:

```powershell
python -B -X utf8 suite-support/prepare_hard_case.py --case rollout-cycle --state repaired --output ../hard-rollout-repaired
```

The provider uses `@RequestMapping({"/payments", "/v2/payments"})`; the new
client keeps `/v2/payments`. For the actual same-project repair, make this provider edit
in the broken copy, then **Check Again** against its unchanged HEAD. The no-order
route condition should disappear. The recorded expanded-provider control showed
**two compatible changes and two items needing review**; its exported plan said
**Order not proven**. That clears this no-order condition without certifying a
provider-first deployment. Inspect Details and the exported plan, check the
mixed-version calls and confirm the deployed versions with the affected teams.

To return the broken copy to its original compatible baseline:

```powershell
git restore -- payment-app/src/main/java/demo/payments/PaymentController.java order-app/src/main/java/demo/orders/PaymentClient.java
```

To repeat the broken state, change the provider class mapping and Feign `path`
back to `/v2/payments` in that same copy; do not commit the mutation. Recheck with
the same base and scope. The manifest describes the initial prepared state and
becomes stale after manual edits; record subsequent actual states separately.

## 2. The new JPA entity agrees with the migration; the old pod does not

```powershell
python -B -X utf8 suite-support/prepare_hard_case.py --case migration-old-reader --state baseline --output ../hard-migration
```

The baseline `payment-app` entity explicitly maps `orders.id` and `orders.total`.
Complete the native baseline steps above, then make this change:

1. In `payment-app/src/main/java/demo/payments/OrderEntity.java`, remove only
   `@Column(name = "total")` and the following `BigDecimal total` field.
2. Create `payment-app/src/main/resources/db/migration/V2__drop_total.sql` with
   `ALTER TABLE orders DROP COLUMN total;`.
3. From the prepared project root, run:

   ```powershell
   git add --intent-to-add -- payment-app/src/main/resources/db/migration/V2__drop_total.sql
   ```

The new entity and migration agree about removing `total`. The new code looks coherent, but
the version being replaced still maps `total`. **Changes → Details** should show
**Breaking**, `DB_TABLE`, **Dropped column is still mapped by the previous
version**, with the migration and historical entity evidence. The new migration
has Git intent-to-add so its contents remain unstaged while Git reports it as a
new file in the comparison; the baseline itself is unchanged.

The helper's default `--state broken` creates this source mutation directly;
its native use still requires first moving V2 outside the project, restoring the
entity, resetting only V2's intent-to-add entry, and capturing the clean baseline.
Then reapply the same entity edit, return V2 and add its intent-to-add entry again.

Prepare a separate source reference for the bounded repair:

```powershell
python -B -X utf8 suite-support/prepare_hard_case.py --case migration-old-reader --state repaired --output ../hard-migration-repaired
```

This removes the field from the new code but **retains the database column**:
there is no destructive V2. That particular DROP impact should disappear. For
the same-project countercheck, move the generated V2 outside `src/main/resources`
and outside the analyzed project, rerun, then return the identical V2 and rerun.
Keep its original Git intent-to-add entry. A missing file is a different current
source state; record it rather than treating the initial manifest as current.

To restore the baseline in the generated broken copy, move V2 outside the project,
then restore the entity and reset only V2's empty intent-to-add index entry:

```powershell
git restore -- payment-app/src/main/java/demo/payments/OrderEntity.java
git reset HEAD -- payment-app/src/main/resources/db/migration/V2__drop_total.sql
```

Do not edit V1 to simulate the repair: editing an already applied versioned
migration is a separate **Applied migration changed** review. Contracting the
database column belongs to a later release after deployed and rollback readers
have been verified. The fixture uses the public
[`jakarta.persistence-api:3.1.0`](https://jakarta.ee/specifications/persistence/3.1/)
annotations for source mapping; it does not run Hibernate, Flyway or a database.

## 3. Current Kafka shapes agree; the new reader rejects the old writer

Use the existing Boot lab's historical-reader case:

```powershell
python -B -X utf8 suite-support/prepare_boot_kafka_case.py --boot-line 35 --case historical-reader --output ../hard-kafka-history
```

This existing preparer seeds the working mutation immediately. Before opening
the prepared folder in IDEA, restore its two DTOs to the clean baseline:

```powershell
cd ../hard-kafka-history
git restore -- producer/src/main/java/demo/boot/producer/Event.java consumer/src/main/java/demo/boot/consumer/Event.java
```

At HEAD both independent `Event` DTOs have only `id`. Complete the full native
baseline steps above. Then add
`@JsonProperty(value = "tenant", required = true) String tenant` as a second
record component to **both** `Event` records, keeping their existing imports.
Compile, analyze and compare the same HEAD. Current producer → current reader matches;
**Changes → HEAD → Current files** should be **Breaking** for the old producer
shape → the current reader. Capture the historical reason, not merely the current
DTOs. An empty current Kafka mismatch list does not settle historical readability.

For the recorded same-project repair, set the consumer's `tenant` annotation to
`@JsonProperty(value = "tenant", required = false)` while keeping the producer
field, and recheck the same HEAD. The native result was **No breaking changes
found**, with two compatible changes; restoring `required = true` brought the
two breaking impacts back.
Treat absent-tenant handling as an explicit application decision and test it.
Restore both DTOs for the exact baseline:

```powershell
git restore -- producer/src/main/java/demo/boot/producer/Event.java consumer/src/main/java/demo/boot/consumer/Event.java
```

To repeat the trap, add `@JsonProperty(value = "tenant", required = true) String
tenant` back to **both** `Event` records. The existing
[Boot Kafka guide](../kafka-boot-lab/README.md) documents the supported wire chain,
Boot 3.5/4.0 choices, customization uncertainty and actual-export checker. Old
source shapes do not prove retained records exist in a broker, retry topic or DLT.

## Recorded native controls: 2026-11-05

These controls were observed with **installed ArchVerity 6.1.0 in IntelliJ IDEA
2026.1.4**, after importing both modules and capturing each clean Git baseline.
The three intentionally broken candidates compiled; the Kafka optional-reader
and HTTP expanded-provider controls compiled too. Compilation used JBR 25.0.3
with Java release 21. No application, database or broker was started.

| Case | Observed trap | Same-project control and return |
| --- | --- | --- |
| HTTP rollout | Two current contracts compatible; Details and the [actual copied plan](../../docs/evidence/hard-cases-6.1.0/rollout-no-order.md) say no deploy order is safe | Expanded provider: 2 compatible + 2 review, [Order not proven](../../docs/evidence/hard-cases-6.1.0/rollout-expanded-review.md). Restoring the original routes reproduced the identical no-order plan. |
| Old JPA reader | 1 breaking DROP impact + 3 review items; the new entity has no `total`, but the previous entity maps it | Moving only V2 outside the analyzed project removed the DROP break; review remained. Returning the identical SQL restored the breaking result. |
| Kafka history | Problems (0) for current source, but Changes has 2 breaking impacts for the older writer and new required reader | Reader `required=false`: no breaking changes, 2 compatible. Restoring `true` restored the 2 breaking impacts. |

Open the unchanged native captures at full size:

- HTTP: [current contracts and no-order warning](../../docs/media/hard-cases-6.1.0/rollout-no-order.jpg),
  [expanded-provider review](../../docs/media/hard-cases-6.1.0/rollout-expanded-review.jpg).
- JPA: [DROP against the old entity](../../docs/media/hard-cases-6.1.0/migration-old-reader-breaking.jpg),
  [DROP deferred, review retained](../../docs/media/hard-cases-6.1.0/migration-drop-deferred.jpg).
- Kafka: [historical-reader break](../../docs/media/hard-cases-6.1.0/kafka-history-breaking.jpg),
  [optional-reader control](../../docs/media/hard-cases-6.1.0/kafka-history-compatible.jpg).

The [native run record](../../docs/evidence/hard-cases-6.1.0/native-run.json)
binds capture hashes, exact local Git bases and observed boundaries. Those base
SHAs identify this recording; fresh preparations create their own baseline
commits. These are synthetic demonstrations, not customer incidents or runtime
deployment evidence. An expanded route or a deferred DROP is a migration step,
not proof that production and rollback readers have finished migrating.

## Compilation, actual proof and limits

From each prepared project, compile once before native analysis:

```powershell
.\gradlew.bat classes --console=plain --no-daemon
```

On Linux/macOS use `./gradlew`. A first dependency download needs network access.
The first two cases preserve the `archverity-first-result` Gradle root and its
`order-app`/`payment-app` service mappings. Do not rename modules without updating
`.archflow.yml`. The reserved `.test` Feign host is static source input.

Save one native result for the trap, one after repair and one after restoration.
Inspect the source on both sides and keep scope, Git base and configuration
constant. No deployment, broker delivery, application behaviour, database safety
or universal compatibility is established by these source checks. Missing refs,
partial indexing, unresolved factories and unsupported mapper behavior remain
**Needs review**, never a fabricated green control.

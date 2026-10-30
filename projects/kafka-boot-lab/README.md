# Follow an ordinary Spring Boot Kafka payload

Use this lab with **ArchVerity 5.8.2** (or its separate **5.8.2-2024.3** package
for IDEA 2024.3). It is a two-module Java source-analysis sample, compiled
against real **Spring Boot 3.5.7** or **4.0.0** libraries. No broker, Docker,
database, credentials or running application is needed. The inaccessible
`127.0.0.1:1` address is a fixture; it is not a broker observation.

[All-lab preparation and recovery](../../docs/DEMO_RUNBOOK_RU.md) ·
[English product tour](../../docs/PRODUCT_TOUR_EN.md) ·
[Русский маршрут](../../docs/PRODUCT_TOUR_RU.md) ·
[Released Kafka scope](https://plugins.jetbrains.com/plugin/34234-archverity-ai/documentation?noRedirect=true#kafka-flows)

## Prepare and compile one case

From the demo repository root, use Git, Python 3.10+ and JDK 21:

```powershell
python -B -X utf8 suite-support/prepare_boot_kafka_case.py --boot-line 35 --case remove-required --output ../archverity-boot35-remove
cd ../archverity-boot35-remove
.\gradlew.bat classes --console=plain --no-daemon
```

On Linux/macOS use `./gradlew classes --console=plain --no-daemon`. Initial
dependency downloads require network access. Use `--boot-line 40` and another
fresh output directory for Boot 4. The preparer selects the matching BOM and
serializer classes together; changing just `-PbootLine` in an existing copy
does not update the source configuration. Existing output directories are
refused. Shipped templates stay unchanged.

Open the **prepared standalone folder**, import both Gradle modules and finish
indexing. Activate Trial/Pro in the compatible ArchVerity package. The sample
has Boot activation annotations but no application launcher or `bootRun` task:
compile it and analyze source rather than starting listeners.

The preparer records a local Git `HEAD` before the case's source edit. Its
ignored `work/boot-kafka-case.json` records the selected Boot line, baseline
commit and exact source hashes. You can check preparation from the repository:

```powershell
python -B -X utf8 suite-support/check_boot_kafka.py --project ../archverity-boot35-remove
```

`INPUT_CONTRACT_PASS` means only that these prepared inputs and their Git base
match. It does not mean that compilation, ArchVerity analysis, a live IDE tour
or a broker interaction has run. Record actual observations in the
[run record](../../docs/RUN_RECORD.md) and consult the
[current verification boundaries](../../docs/CURRENT_VERIFICATION_RU.md).

## Inspect the source chain

The producer and consumer have independent DTOs:

- `producer/src/main/java/demo/boot/producer/Event.java`
- `consumer/src/main/java/demo/boot/consumer/Event.java`

Each baseline DTO has `id` and a required JSON `tenant`. The producer injects
an unqualified `KafkaTemplate<String, Event>`; the listener omits
`containerFactory`. Both modules retain `@SpringBootApplication`. Inspect
their `src/main/resources/application.properties` to see the evidence used for
the ordinary Boot defaults:

| Input | Boot 3.5 | Boot 4.0 |
| --- | --- | --- |
| Producer value serializer | `JsonSerializer` | `JacksonJsonSerializer` |
| Consumer value deserializer | `JsonDeserializer` | `JacksonJsonDeserializer` |
| Key serializer/deserializer | Kafka String classes | Kafka String classes |
| Producer JSON type headers | `spring.json.add.type.headers=false` | Same |
| Reader type-header policy | `spring.json.use.type.headers=false` | Same |
| Reader target type | `demo.boot.consumer.Event` | Same |
| Trusted reader package | `demo.boot.consumer` | Same |

The full value-class names are under
`org.springframework.kafka.support.serializer`. Disabling type headers and
naming the consumer's own DTO keeps the two modules' Java class names
from being treated as an identical wire type. Both sides use the declared
logical scope `declared-boot-demo` and topic `orders.events`; neither a shared
address nor that declaration proves a deployed cluster or successful delivery.

## Observe a break, correction and return control

For `remove-required`, **compilation still passes**: only the producer's
`tenant` record component has been removed. The consumer still requires it.

1. In **Map**, choose **Analyze Project**. In **Problems**, find the Kafka
   required-field mismatch (`AFG-KAFKA-005` in technical details). Inspect both
   DTO source locations and the serializer/deserializer configuration. The
   supported chain should make this a proven mismatch rather than merely
   guessing from equal topic names.
2. In **Changes**, compare with the prepared **HEAD**. **Summary** should report
   the seeded change as **Breaking**; **Details** should identify the affected
   consumer. Keep the same base and scope when rechecking.
3. From this prepared copy, restore the one edited fixture file:

   ```powershell
   git restore -- producer/src/main/java/demo/boot/producer/Event.java
   ```

   Compile again, then choose **Check Again** and repeat **Map → Analyze
   Project**. That required-field mismatch should disappear; the unchanged
   comparison is not a certification of the application.
4. Remove only the producer's `tenant` component again, compile and recheck.
   The same mismatch should return. This present → absent → present control
   ties the result to the actual edit.

After step 3, `check_boot_kafka.py --project <prepared-folder> --restored`
checks the exact baseline source bytes and unchanged Git base. Its default
mode rejects a restored or otherwise edited case as a stale preparation
receipt; use the flag only for this explicit correction control.

## Choose another bounded case

Prepare each row into a separate fresh directory, using either Boot line.

| Case | Current source result to inspect | Changes against prepared HEAD |
| --- | --- | --- |
| `baseline` | Resolved ordinary Boot chain; no seeded DTO mismatch | No seeded change |
| `remove-required` | Proven missing `tenant` on the producer | Breaking; restore the producer file for the correction control |
| `add-optional` | Producer adds `note`; the default Spring JSON reader ignores the unknown property | Bounded compatible result for that addition |
| `customizer-control` | Producer `ProducerOverrides.java` declares a factory customizer, so the selected wire chain is Needs review | Needs review, with the named customization; no invented proven wire mismatch |
| `historical-reader` | Current producer and consumer both include required `tenant` | Breaking **old producer at the Git base → current reader**, despite matching current shapes |

The customizer control is present in both the base and current source. Only
the producer DTO changes after the base, so the uncertainty comes from the
named customization rather than a changed Boot activation or a borrowed
historical classpath. Boot 4's customizer lives under
`org.springframework.boot.kafka.autoconfigure`; Boot 3.5 uses
`org.springframework.boot.autoconfigure.kafka`.

For `historical-reader`, `git show HEAD:<DTO-path>` shows the old `id`-only
producer and consumer. The working files add required `tenant` to both. First
analyze the current project, then compare with **HEAD** in Changes and inspect
the old-record reason. Build inputs and Boot activation are unchanged between
the two source revisions. A Git base describes a historical source shape; it
does not identify deployed producer versions or prove that such records remain
in a broker, retry topic or DLT. Exercise real retained/replayed records and
business processing in your own runtime tests.

## Check actual exports without hiding incomplete evidence

Save a full analysis JSON and the relevant change-impact JSON from the
prepared project. Record the exact observed project ID and comparison
`baseIdentity`; the checker does not infer them from another project.

```powershell
python -B -X utf8 suite-support/check_boot_kafka.py --project ../archverity-boot35-remove --snapshot ../archverity-boot35-remove/work/analysis.json --project-id <observed-project-id> --impact ../archverity-boot35-remove/work/impact.json --base-identity <observed-baseIdentity>
```

The checker rejects partial, failed/cancelled or wrong-project analysis,
stale input bytes, a moved base and a false proven result for the customizer
control. Export checks inspect the file's complete content; the operator must
still bind it to the real IDE/plugin/build, selected folder and run time.
The lab does not demonstrate all Kotlin extraction forms, custom mapper or
converter behavior, remote Split Mode, broker acknowledgement or delivery.
The separate [Kafka profile lab](../kafka-profile-lab/README.md) retains its
twelve scope/configuration controls and historical evidence independently.

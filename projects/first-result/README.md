# One contract mismatch, before you run an application

This small source-analysis demo contains two Java modules. Both compile, but
the OpenFeign caller sends `POST /payments/{paymentId}` and the Spring MVC
provider accepts `PUT /payments/{paymentId}`. No server, database, Docker,
credentials, or customer source code is needed.

Prerequisites: an IntelliJ IDEA supported by your installed ArchVerity build,
JDK 21, ArchVerity 3.0.2 or a newer compatible build, and an active Trial or subscription.
An internet connection is needed for the first Gradle/dependency download.
This is a compileable analysis sample, not a runnable Spring Boot application.

## See the finding

1. Clone the public demo repository and open this directory in IntelliJ IDEA as a Gradle project.
   Trust only the copy you obtained from the publisher. Wait for Gradle import
   and indexing to finish. Select JDK 21 or later if prompted.
2. Build with `./gradlew classes` (Windows: `.\gradlew.bat classes`). A successful
   build is expected even while the mismatch exists.
3. Open **View → Tool Windows → ArchVerity**. Run **Analyze** for the project.
   This first scan does not require a Git repository or an edited file.
4. Open **Findings**, select **HTTP method mismatch** (`AFG-HTTP-001`), and inspect
   the client and server evidence. Open both source locations:
   - `order-app/src/main/java/demo/orders/PaymentClient.java`
   - `payment-app/src/main/java/demo/payments/PaymentController.java`
5. In `PaymentClient.java`, change only `@PostMapping` to `@PutMapping`.
   Save and run **Analyze** again. The HTTP method mismatch should disappear.
   Both modules should still compile. Change it back to repeat the demo.

Expected result: a resolved method mismatch before the edit and no
`AFG-HTTP-001` for this call afterward. Other informational findings are not the
success criterion. A green build alone does not prove the analyzer result.

If no mismatch appears, check that both modules finished importing, the scan
covers the whole project, and `.archflow.yml` is at the project root. The alias
`payments.example.test` maps the explicit Feign URL to `payment-service`.
The reserved `.test` hostname is only a static-analysis example; this sample
makes no network request. Module names in the configuration cover both folder
analysis and this Gradle project's imported `.main` source sets. If you rename
the Gradle root project, update those module names too. A name-only discovery
client has inferred evidence; this demo uses an explicit URL so its mismatch
can be resolved. Record the IDE/plugin
versions and visible diagnostics before contacting support.

## Try a real change next

Prepare the [full workspace](../../docs/ARCHITECTURE_WALKTHROUGH_RU.md) for
isolated Impact mutations, Kafka/AMQP, DTOs and developer tools.
The [feature catalog](../../docs/FEATURE_CATALOG.md) connects every registered
entry point to its input and acceptance recipe.

## Distribution

The sample is supplied for evaluating ArchVerity. Gradle wrapper files retain
their upstream notices. Third-party libraries are downloaded from Maven
Central and are not bundled. No ArchVerity plugin binary or license is included.

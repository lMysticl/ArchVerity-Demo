# Demonstration projects

This public suite exercises ArchVerity against synthetic, inspectable inputs.
Install ArchVerity separately from JetBrains Marketplace. Use a compatible
IntelliJ IDEA and JDK 21; paid features need a legitimate Trial/Pro entitlement.

The [step-by-step launch runbook](DEMO_RUNBOOK_RU.md) links prerequisites,
all six labs, expected observations, recovery and actual result recording.
Use the [documentation index](README.md) to reach the complete 62-function
and 87-entry guides. Detailed launch instructions are in Russian.

1. Prepare a standalone `first-result` copy with `suite-support/prepare_project.py`
   and open that output as a Gradle project for the first HTTP finding.
   It compiles while its Feign POST call disagrees with the provider's PUT.
2. Prepare a standalone `workspace` with `suite-support/prepare_project.py`,
   scan its clean HEAD in IDEA, and apply one `qa-support/apply_impact.py`
   scenario per fresh copy. It includes HTTP/Kafka/AMQP, nested DTOs and the
   developer tools' actual input files.
3. Run `projects/api-lab/serve.py` for local HTTP/WebSocket/gRPC, then follow
   that project's README for exact URLs, schema and expected responses.
4. Use `projects/mobile-lab` for real Expo/React Native commands. Native source
   is generated with prebuild; Android needs an SDK/device and iOS needs macOS.
5. Prepare and run `runtime-evidence` to capture a real Actuator beans response
   and locally executed HTTP verification reports. The reports use supported
   Pact/Drift shapes with explicit LOCAL_FILE provenance, without claiming an
   execution by a branded verifier.
6. Prepare one of the 12 `kafka-profile-lab` recipes to test profile paths,
   unresolved serializer overrides and separate cluster scopes. New `009/010`
   outcomes require ArchVerity **3.0.4** or newer, or **3.0.4-2024.3** for
   local IDEA 2024.3. Both signed updates were submitted to Marketplace on
   October 5, 2026 and are now approved and publicly listed. The older published 3.0.3
   does not contain this fix. See the [release verification record](VERIFICATION_RU.md#выпуск-304--05102026).

`python suite-support/check_suite.py` validates fixture binding and documentation.
Maintainers can supply `--plugin-source ... --require-source` to compare all
87 registered entry points against plugin source. See the feature catalog,
environment checks and run record for the complete acceptance instructions.
Preparation and compilation do not constitute a passing IDEA/device/remote run.

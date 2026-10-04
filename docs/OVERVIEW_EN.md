# Demonstration projects

This public suite exercises ArchVerity against synthetic, inspectable inputs.
Install ArchVerity separately from JetBrains Marketplace. Use a compatible
IntelliJ IDEA and JDK 21; paid features need a legitimate Trial/Pro entitlement.

1. Open `projects/first-result` as a Gradle project for the first HTTP finding.
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

`python suite-support/check_suite.py` validates fixture binding and documentation.
Maintainers can supply `--plugin-source ... --require-source` to compare all
87 registered entry points against plugin source. See the feature catalog,
environment checks and run record for the complete acceptance instructions.
Preparation and compilation do not constitute a passing IDEA/device/remote run.

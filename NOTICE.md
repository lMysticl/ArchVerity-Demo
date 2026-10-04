# Provenance

The demonstration sources, scenarios and public certificate fixtures were
prepared for ArchVerity. They contain synthetic service identities and data.
No plugin implementation, private repository history or customer source is
distributed in this repository. The demo sources use the MIT license.

The Gradle wrapper launchers and wrapper JARs in the Gradle projects are Gradle
components, licensed under Apache License 2.0: https://github.com/gradle/gradle.
The license text is included in `LICENSES/Apache-2.0.txt`.
The resolved dependencies retain their own licenses. The mobile app follows
the SDK 54 blank template's dependency versions; its screen is original demo
code. Native folders are generated locally by Expo, not included here.

The two `.aficons` packages contain synthetic QA icons and the ArchVerity
Studio demonstration pack. The `.p12` fixture is a public-only truststore:
it contains a trusted certificate and no private key. Its documented fixture
password protects no secret. PEM/DER/CSR/CRL inputs contain public material only.

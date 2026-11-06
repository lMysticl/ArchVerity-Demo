# Boot 4.0, 4.1 and 4.2 mappers — 24 October 2026

The [23 October observations](../boot-upgrade-20261023/README.md) compare Boot 3.5.15
with Boot 4.1.1. This rerun asks whether the Boot 4 side depends on the minor line.
The same `WireProbe` of the public [boot-upgrade lab](../../../projects/boot-upgrade/README.md)
ran against the auto-configured mapper of `spring-boot-dependencies` 4.0.9, 4.1.1,
4.1.2 and 4.2.0-RC1. It ran on OpenJDK 21.0.12.1 in a Linux container, using the lab's Gradle 9.6.1 wrapper.
No service or broker ran. Input and output hashes are recorded in [manifest.json](manifest.json).

| Boot | Observation | Enum | `Month.JANUARY` | `1` read as | `null` / missing into `int` | Reads own / Boot 3 invoice |
| --- | --- | --- | --- | --- | --- | --- |
| 4.0.9 | [JSON](boot-4.0.9.json) | `"Paid"` | `1` | `JANUARY` | rejected / rejected | no / no |
| 4.1.1 | [JSON](boot-4.1.1.json) | `"Paid"` | `1` | `JANUARY` | rejected / rejected | no / no |
| 4.1.2 | [JSON](boot-4.1.2.json) | `"Paid"` | `1` | `JANUARY` | rejected / rejected | no / no |
| 4.2.0-RC1 | [JSON](boot-4.2.0-RC1.json) | `"Paid"` | `1` | `JANUARY` | rejected / rejected | no / no |

All four files are identical except `bootVersion`. The Jackson 3 differences the lab
shows are a property of the Boot 4 line up to 4.2.0-RC1, not of one release. The
4.1.1 values match the [23 October baseline](../boot-upgrade-20261023/baseline-boot4.json).

Reproduce from a prepared lab (see the lab README). Append this block to its
`build.gradle.kts`, then run `./gradlew classes wireBoot40 wireBoot41 wireBoot42`
and compare `build/wire/boot40.json`, `boot41.json` and `boot42.json`:

```kotlin
listOf("40" to "4.0.9", "41" to "4.1.2", "42" to "4.2.0-RC1").forEach { (label, version) ->
    val libs = configurations.create("boot${label}Wire")
    dependencies {
        add(libs.name, platform("org.springframework.boot:spring-boot-dependencies:$version"))
        add(libs.name, "org.springframework.boot:spring-boot-starter-json:$version")
        add(libs.name, "org.springframework.boot:spring-boot-autoconfigure:$version")
    }
    tasks.register<JavaExec>("wireBoot$label") {
        dependsOn(compileWireProbe)
        classpath = files(compileWireProbe.flatMap { it.destinationDirectory }) + serviceClasses + libs
        mainClass.set("demo.verification.WireProbe")
        args("4", layout.buildDirectory.file("wire/boot$label.json").get().asFile.absolutePath)
    }
}
```

`verify_wire.py` checks the pinned 3.5.15 / 4.1.1 pair and is not meant for these
files. These receipts prove library behavior only. They do not claim an installed-plugin scan,
paid entitlement check, MCP connection or IDE screenshot.

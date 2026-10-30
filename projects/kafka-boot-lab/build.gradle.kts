val bootLine = providers.gradleProperty("bootLine").orElse("35").get()
val bootVersion = when (bootLine) {
    "35" -> "3.5.7"
    "40" -> "4.0.0"
    else -> error("Use bootLine=35 or bootLine=40; prepare each line in its own copy")
}

subprojects {
    apply(plugin = "java")
    repositories { mavenCentral() }
    dependencies {
        "implementation"(enforcedPlatform("org.springframework.boot:spring-boot-dependencies:$bootVersion"))
        "implementation"("org.springframework.boot:spring-boot-autoconfigure")
        "implementation"("org.springframework.kafka:spring-kafka")
        "implementation"("com.fasterxml.jackson.core:jackson-annotations")
        if (bootLine == "40") {
            "implementation"("org.springframework.boot:spring-boot-kafka")
            "implementation"("tools.jackson.core:jackson-databind")
        } else {
            "implementation"("com.fasterxml.jackson.core:jackson-databind")
        }
    }
    tasks.withType<JavaCompile>().configureEach {
        options.release.set(21)
        options.encoding = "UTF-8"
        options.compilerArgs.add("-Xlint:deprecation")
    }
}

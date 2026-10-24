plugins {
    java
    kotlin("jvm") version "2.4.10" apply false
}

// Fixed reproduction versions for the demo, not a recommendation.
val bootVersion = "3.5.15"

subprojects {
    apply(plugin = "java")
    repositories { mavenCentral() }
    tasks.withType<JavaCompile>().configureEach {
        options.release.set(21)
        options.encoding = "UTF-8"
        options.compilerArgs.add("-parameters")
    }
    dependencies {
        "implementation"(platform("org.springframework.boot:spring-boot-dependencies:$bootVersion"))
        "implementation"("org.springframework.boot:spring-boot-starter-web")
    }
}

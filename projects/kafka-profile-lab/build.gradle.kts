subprojects {
    apply(plugin = "java")
    repositories { mavenCentral() }
    dependencies {
        "implementation"(enforcedPlatform("org.springframework.boot:spring-boot-dependencies:3.5.12"))
        "implementation"("org.springframework.boot:spring-boot-starter")
        "implementation"("org.springframework.boot:spring-boot-starter-json")
        "implementation"("org.springframework.kafka:spring-kafka")
    }
    tasks.withType<JavaCompile>().configureEach {
        options.release.set(21)
        options.encoding = "UTF-8"
        options.compilerArgs.add("-Xlint:deprecation")
    }
}

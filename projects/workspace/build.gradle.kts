plugins { base }

subprojects {
    apply(plugin = "java")
    repositories { mavenCentral() }
    tasks.withType<JavaCompile>().configureEach {
        options.release.set(21)
        options.encoding = "UTF-8"
        options.compilerArgs.add("-Xlint:deprecation")
    }
    dependencies {
        "implementation"("org.springframework:spring-web:6.2.19")
        "implementation"("org.springframework:spring-webflux:6.2.19")
        "implementation"("org.springframework.amqp:spring-rabbit:3.2.12")
        "implementation"("com.fasterxml.jackson.core:jackson-databind:2.19.4")
        "implementation"("org.springframework.kafka:spring-kafka:3.3.16")
        "implementation"("jakarta.validation:jakarta.validation-api:3.1.1")
        "implementation"("org.springframework.cloud:spring-cloud-openfeign-core:4.3.3") {
            isTransitive = false
        }
    }
}

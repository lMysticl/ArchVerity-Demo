plugins { application }
repositories { mavenCentral() }

dependencies {
    implementation(enforcedPlatform("org.springframework.boot:spring-boot-dependencies:3.5.12"))
    implementation("org.springframework.boot:spring-boot-starter-web")
    implementation("org.springframework.boot:spring-boot-starter-actuator")
    implementation("org.springframework.kafka:spring-kafka")
}
tasks.withType<JavaCompile>().configureEach {
    options.release.set(21)
    options.encoding = "UTF-8"
    options.compilerArgs.add("-Xlint:deprecation")
}
application {
    mainClass.set("demo.evidence.DemoApplication")
    applicationDefaultJvmArgs = listOf("-Xmx384m")
}

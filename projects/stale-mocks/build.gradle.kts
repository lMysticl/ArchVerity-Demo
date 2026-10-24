plugins { java }

// Fixed reproduction version, not a recommendation.
val bootVersion = "3.5.15"

subprojects {
    apply(plugin = "java")
    repositories { mavenCentral() }
    tasks.withType<JavaCompile>().configureEach {
        options.release.set(21)
        options.encoding = "UTF-8"
        options.compilerArgs.add("-parameters")
    }
    tasks.withType<Test>().configureEach { useJUnitPlatform() }
    dependencies {
        "implementation"(platform("org.springframework.boot:spring-boot-dependencies:$bootVersion"))
        "implementation"("org.springframework.boot:spring-boot-starter-web")
        "testImplementation"(platform("org.springframework.boot:spring-boot-dependencies:$bootVersion"))
        "testImplementation"("org.springframework.boot:spring-boot-starter-test")
        "testRuntimeOnly"("org.junit.platform:junit-platform-launcher")
    }
}

repositories { mavenCentral() }
val realCallLibraries = configurations.create("realCallLibraries")
dependencies {
    add(realCallLibraries.name, platform("org.springframework.boot:spring-boot-dependencies:$bootVersion"))
    add(realCallLibraries.name, "org.springframework.boot:spring-boot-starter-web")
}

val serviceClasses = files(subprojects.flatMap { listOf(it.layout.buildDirectory.dir("classes/java/main"), it.layout.buildDirectory.dir("resources/main")) })
val compileRealCall = tasks.register<JavaCompile>("compileRealCall") {
    dependsOn(subprojects.map { "${it.path}:classes" })
    source("verification/src")
    classpath = realCallLibraries + serviceClasses
    destinationDirectory.set(layout.buildDirectory.dir("real-call/classes"))
    options.release.set(21)
    options.encoding = "UTF-8"
}

// Starts the real billing service on a free local port and reads its answer with orders' own InvoiceView.
tasks.register<JavaExec>("realCall") {
    dependsOn(compileRealCall)
    classpath = files(compileRealCall.flatMap { it.destinationDirectory }) + serviceClasses + realCallLibraries
    mainClass.set("demo.verification.RealCall")
    args(layout.buildDirectory.file("real-call/real-call.json").get().asFile.absolutePath)
}

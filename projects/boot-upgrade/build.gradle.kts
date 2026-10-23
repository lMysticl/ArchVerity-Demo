plugins { java }

// Fixed reproduction versions, not a recommendation to downgrade an application.
val boot3Version = "3.5.15"
val boot4Version = "4.1.1"

subprojects {
    apply(plugin = "java")
    repositories { mavenCentral() }
    tasks.withType<JavaCompile>().configureEach {
        options.release.set(21)
        options.encoding = "UTF-8"
        options.compilerArgs.add("-parameters")
    }
    dependencies {
        "implementation"(platform("org.springframework.boot:spring-boot-dependencies:$boot3Version"))
        "implementation"("org.springframework.boot:spring-boot-starter-web")
    }
}

repositories { mavenCentral() }
val boot3Wire = configurations.create("boot3Wire")
val boot4Wire = configurations.create("boot4Wire")
dependencies {
    add(boot3Wire.name, platform("org.springframework.boot:spring-boot-dependencies:$boot3Version"))
    add(boot3Wire.name, "org.springframework.boot:spring-boot-starter-json:$boot3Version")
    add(boot3Wire.name, "org.springframework.boot:spring-boot-autoconfigure:$boot3Version")
    add(boot4Wire.name, platform("org.springframework.boot:spring-boot-dependencies:$boot4Version"))
    add(boot4Wire.name, "org.springframework.boot:spring-boot-starter-json:$boot4Version")
    add(boot4Wire.name, "org.springframework.boot:spring-boot-autoconfigure:$boot4Version")
}

val serviceClasses = files(subprojects.map { it.layout.buildDirectory.dir("classes/java/main") })
val compileWireProbe = tasks.register<JavaCompile>("compileWireProbe") {
    dependsOn(subprojects.map { "${it.path}:classes" })
    source("verification/src")
    classpath = boot3Wire + serviceClasses
    destinationDirectory.set(layout.buildDirectory.dir("wire-probe/classes"))
    options.release.set(21)
    options.encoding = "UTF-8"
}

listOf(3 to boot3Wire, 4 to boot4Wire).forEach { (generation, libraries) ->
    tasks.register<JavaExec>("wireBoot$generation") {
        dependsOn(compileWireProbe)
        classpath = files(compileWireProbe.flatMap { it.destinationDirectory }) + serviceClasses + libraries
        mainClass.set("demo.verification.WireProbe")
        args(generation.toString(), layout.buildDirectory.file("wire/boot$generation.json").get().asFile.absolutePath)
    }
}

plugins { base }

subprojects {
    apply(plugin = "java")
    repositories { mavenCentral() }
    tasks.withType<JavaCompile>().configureEach {
        options.release.set(21)
        options.encoding = "UTF-8"
    }
    dependencies {
        "implementation"("org.springframework:spring-web:6.2.19")
    }
}

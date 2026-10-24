plugins { kotlin("jvm") }

kotlin {
    compilerOptions { jvmTarget.set(org.jetbrains.kotlin.gradle.dsl.JvmTarget.JVM_21) }
}

dependencies {
    implementation("com.fasterxml.jackson.module:jackson-module-kotlin")
}

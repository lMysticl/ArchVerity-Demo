plugins { java }
dependencies {
    implementation("org.springframework.cloud:spring-cloud-openfeign-core:4.3.3") {
        isTransitive = false
    }
}

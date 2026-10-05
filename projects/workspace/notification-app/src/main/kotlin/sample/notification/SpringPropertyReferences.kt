package sample.notification

import org.springframework.beans.factory.annotation.Value

class SpringPropertyReferences(
    @Value("\${spring.rabbitmq.virtual-host}") val virtualHost: String
)

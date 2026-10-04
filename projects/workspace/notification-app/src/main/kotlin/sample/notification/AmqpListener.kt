package sample.notification

import org.springframework.amqp.rabbit.annotation.RabbitListener
import org.springframework.amqp.rabbit.annotation.QueueBinding
import org.springframework.amqp.rabbit.annotation.Queue
import org.springframework.amqp.rabbit.annotation.Exchange

class AmqpListener {
    @RabbitListener(bindings = [QueueBinding(
        value = Queue(value = "demo.notifications"),
        exchange = Exchange(value = "commerce.events", type = "topic"),
        key = ["orders.#"]
    )])
    fun onOrder(event: OrderNotification) {}
}

data class NotificationAddress(val city: String, val postalCode: String?)
data class OrderNotification(val orderId: String, val amount: Long,
                             val currency: String, val address: NotificationAddress?)

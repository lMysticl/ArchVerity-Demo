package sample.notification

interface PaymentNotificationMapper {
    fun findStatus(paymentId: String): String?
}

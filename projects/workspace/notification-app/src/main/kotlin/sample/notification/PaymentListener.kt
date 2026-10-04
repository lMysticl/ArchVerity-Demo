package sample.notification
import org.springframework.kafka.annotation.KafkaListener
class PaymentListener {
 @KafkaListener(topics=["payments.completed"], groupId="notification-service")
 fun onPayment(event: PaymentCompleted) {}
}
data class PaymentCompleted(val paymentId:String,val orderId:String)

package sample.payment;
import org.springframework.kafka.annotation.KafkaListener;
import org.springframework.kafka.annotation.RetryableTopic;
class OrderListener {
 @RetryableTopic
 @KafkaListener(topics="orders.created",groupId="payment-service")
 void onOrder(OrderCreated event){}
}
record OrderCreated(String orderId,long amount,String currency,String mandatoryRiskToken) {}

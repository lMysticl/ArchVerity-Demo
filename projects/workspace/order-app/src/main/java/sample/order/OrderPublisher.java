package sample.order;
import org.springframework.kafka.core.KafkaTemplate;
class OrderPublisher {
 private final KafkaTemplate<String,OrderCreated> kafkaTemplate;
 OrderPublisher(KafkaTemplate<String,OrderCreated> kafkaTemplate){this.kafkaTemplate=kafkaTemplate;}
 void publish(OrderCreated event){kafkaTemplate.send("orders.created",event);}
}
record OrderCreated(String orderId,long amount,String currency) {}

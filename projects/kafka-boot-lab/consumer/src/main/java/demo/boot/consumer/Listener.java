package demo.boot.consumer;

import org.springframework.kafka.annotation.KafkaListener;
import org.springframework.stereotype.Component;

@Component
public class Listener {
    @KafkaListener(topics = "orders.events", groupId = "billing")
    public void receive(Event event) {}
}

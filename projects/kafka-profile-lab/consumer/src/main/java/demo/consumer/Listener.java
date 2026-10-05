package demo.consumer;
import org.springframework.kafka.annotation.KafkaListener;
import org.springframework.stereotype.Component;
@Component
public class Listener {
    @KafkaListener(topics = "${topics.orders}", groupId = "workers", containerFactory = "listenerFactory")
    public void receive(Event event) {}
}

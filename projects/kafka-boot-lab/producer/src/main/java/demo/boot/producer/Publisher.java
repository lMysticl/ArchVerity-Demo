package demo.boot.producer;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.kafka.core.KafkaTemplate;
import org.springframework.stereotype.Component;

@Component
public class Publisher {
    @Autowired private KafkaTemplate<String, Event> template;

    public void publish(Event event) {
        template.send("orders.events", event);
    }
}

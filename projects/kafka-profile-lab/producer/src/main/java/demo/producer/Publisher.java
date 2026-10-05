package demo.producer;
import org.springframework.beans.factory.annotation.Qualifier;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.kafka.core.KafkaTemplate;
import org.springframework.stereotype.Component;
@Component
public class Publisher {
    @Autowired @Qualifier("publisherTemplate") private KafkaTemplate<String, Event> template;
    @Value("${topics.orders}") private String topic;
    public void publish(Event event) { template.send(topic, event); }
}

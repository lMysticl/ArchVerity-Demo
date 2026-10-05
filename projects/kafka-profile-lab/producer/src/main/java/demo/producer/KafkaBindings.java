package demo.producer;
import java.util.Map;
import org.apache.kafka.common.serialization.StringSerializer;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.kafka.core.DefaultKafkaProducerFactory;
import org.springframework.kafka.core.KafkaTemplate;
import org.springframework.kafka.support.serializer.JsonSerializer;
@Configuration
public class KafkaBindings {
    @Value("${spring.kafka.producer.value-serializer}") private String configuredSerializer;
    @Bean public DefaultKafkaProducerFactory<String, Event> producerFactory() {
        return new DefaultKafkaProducerFactory<>(Map.of("value.serializer", configuredSerializer));
    }
    @Bean public KafkaTemplate<String, Event> publisherTemplate() { return new KafkaTemplate<>(producerFactory()); }
}

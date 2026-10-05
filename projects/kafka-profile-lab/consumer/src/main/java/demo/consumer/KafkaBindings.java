package demo.consumer;
import java.util.Map;
import org.apache.kafka.common.serialization.StringDeserializer;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.kafka.core.DefaultKafkaConsumerFactory;
import org.springframework.kafka.config.ConcurrentKafkaListenerContainerFactory;
import org.springframework.kafka.support.serializer.JsonDeserializer;
@Configuration
public class KafkaBindings {
    @Bean public DefaultKafkaConsumerFactory<String, Event> consumerFactory() {
        return new DefaultKafkaConsumerFactory<>(Map.of(), new StringDeserializer(), new JsonDeserializer<>(Event.class));
    }
    @Bean public ConcurrentKafkaListenerContainerFactory<String, Event> listenerFactory() {
        ConcurrentKafkaListenerContainerFactory<String, Event> factory = new ConcurrentKafkaListenerContainerFactory<>();
        factory.setConsumerFactory(consumerFactory());
        return factory;
    }
}

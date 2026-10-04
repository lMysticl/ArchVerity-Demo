package sample.order;

import java.util.Map;
import org.apache.kafka.common.serialization.StringSerializer;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.kafka.core.DefaultKafkaProducerFactory;
import org.springframework.kafka.core.KafkaTemplate;
import org.springframework.kafka.support.serializer.JsonSerializer;

@Configuration
public class KafkaBindings {
    @Bean
    public DefaultKafkaProducerFactory<String, OrderCreated> orderProducerFactory() {
        return new DefaultKafkaProducerFactory<>(Map.of("bootstrap.servers", "127.0.0.1:1"),
                                                 new StringSerializer(), new JsonSerializer<>());
    }
    @Bean
    public KafkaTemplate<String, OrderCreated> ordersTemplate(
            DefaultKafkaProducerFactory<String, OrderCreated> orderProducerFactory) {
        return new KafkaTemplate<>(orderProducerFactory);
    }
}

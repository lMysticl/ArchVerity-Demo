package sample.payment;

import java.util.Map;
import org.apache.kafka.common.serialization.StringDeserializer;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.kafka.config.ConcurrentKafkaListenerContainerFactory;
import org.springframework.kafka.core.DefaultKafkaConsumerFactory;
import org.springframework.kafka.support.serializer.JsonDeserializer;

@Configuration
public class KafkaConsumerBindings {
    @Bean
    public DefaultKafkaConsumerFactory<String, OrderCreated> orderConsumerFactory() {
        return new DefaultKafkaConsumerFactory<>(Map.of("bootstrap.servers", "127.0.0.1:1", "group.id", "payment-service"),
                                                 new StringDeserializer(), new JsonDeserializer<>(OrderCreated.class));
    }
    @Bean
    public ConcurrentKafkaListenerContainerFactory<String, OrderCreated> kafkaListenerContainerFactory(
            DefaultKafkaConsumerFactory<String, OrderCreated> orderConsumerFactory) {
        var factory = new ConcurrentKafkaListenerContainerFactory<String, OrderCreated>();
        factory.setConsumerFactory(orderConsumerFactory);
        factory.setAutoStartup(false);
        return factory;
    }
}

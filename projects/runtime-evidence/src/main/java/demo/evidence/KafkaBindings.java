package demo.evidence;

import java.util.Map;
import org.apache.kafka.common.serialization.StringDeserializer;
import org.apache.kafka.common.serialization.StringSerializer;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.kafka.config.ConcurrentKafkaListenerContainerFactory;
import org.springframework.kafka.core.*;

/** Only create bean dependencies. No producer sends and no listener starts. */
@Configuration
public class KafkaBindings {
    @Bean
    public DefaultKafkaProducerFactory<String, String> demoProducerFactory() {
        return new DefaultKafkaProducerFactory<>(Map.of("bootstrap.servers", "127.0.0.1:1"),
                                                 new StringSerializer(), new StringSerializer());
    }
    @Bean
    public KafkaTemplate<String, String> demoTemplate(DefaultKafkaProducerFactory<String, String> demoProducerFactory) {
        return new KafkaTemplate<>(demoProducerFactory);
    }
    @Bean
    public DefaultKafkaConsumerFactory<String, String> demoConsumerFactory() {
        return new DefaultKafkaConsumerFactory<>(Map.of("bootstrap.servers", "127.0.0.1:1", "group.id", "demo"),
                                                 new StringDeserializer(), new StringDeserializer());
    }
    @Bean
    public ConcurrentKafkaListenerContainerFactory<String, String> demoListenerFactory(
            DefaultKafkaConsumerFactory<String, String> demoConsumerFactory) {
        var factory = new ConcurrentKafkaListenerContainerFactory<String, String>();
        factory.setConsumerFactory(demoConsumerFactory);
        factory.setAutoStartup(false);
        return factory;
    }
}

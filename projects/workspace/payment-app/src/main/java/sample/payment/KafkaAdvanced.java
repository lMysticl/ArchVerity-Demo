package sample.payment;

import org.apache.kafka.clients.producer.ProducerRecord;
import org.springframework.kafka.annotation.KafkaListener;
import org.springframework.kafka.annotation.TopicPartition;
import org.springframework.kafka.core.KafkaTemplate;
import org.springframework.messaging.handler.annotation.SendTo;

public class KafkaAdvanced {
    private final KafkaTemplate<String, String> template;
    public KafkaAdvanced(KafkaTemplate<String, String> template) { this.template = template; }

    public void publish(String value) {
        template.send(new ProducerRecord<>("demo.partitioned", "42", value));
        template.send("demo.orphan", value);
    }
    @KafkaListener(topicPartitions = @TopicPartition(topic = "demo.partitioned", partitions = {"0", "1"}),
                   groupId = "demo-payments")
    @SendTo("demo.replies")
    public String receive(String value) { return value; }

    @KafkaListener(topicPattern = "demo.dynamic.*", groupId = "demo-pattern")
    public void pattern(String value) {}
}

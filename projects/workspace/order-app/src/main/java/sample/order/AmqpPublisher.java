package sample.order;

import org.springframework.amqp.rabbit.core.RabbitTemplate;

public class AmqpPublisher {
    private final RabbitTemplate template;
    public AmqpPublisher(RabbitTemplate template) { this.template = template; }

    public void topic(OrderCreated event) {
        template.convertAndSend("commerce.events", "orders.created", event);
    }
    public void direct(OrderCreated event) {
        template.convertAndSend("commerce.direct", "payment", event);
    }
    public void fanout(OrderCreated event) {
        template.convertAndSend("commerce.broadcast", "", event);
    }
    public void defaultExchange(OrderCreated event) {
        template.convertAndSend("", "demo.default", event);
    }
    public void dynamic(String key, OrderCreated event) {
        template.convertAndSend("commerce.events", key, event);
    }
}

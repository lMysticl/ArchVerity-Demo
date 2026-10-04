package sample.payment;

import org.springframework.amqp.core.*;
import org.springframework.amqp.rabbit.annotation.RabbitListener;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

@Configuration
public class AmqpTopology {
    @Bean public Queue ordersQueue() { return new Queue("demo.orders"); }
    @Bean public TopicExchange eventsExchange() { return new TopicExchange("commerce.events"); }
    @Bean public Binding ordersBinding() {
        return BindingBuilder.bind(ordersQueue()).to(eventsExchange()).with("orders.*");
    }
    @Bean public Queue directQueue() { return new Queue("demo.direct"); }
    @Bean public DirectExchange directExchange() { return new DirectExchange("commerce.direct"); }
    @Bean public Binding directBinding() {
        return BindingBuilder.bind(directQueue()).to(directExchange()).with("payment");
    }
    @Bean public Queue broadcastQueue() { return new Queue("demo.broadcast"); }
    @Bean public FanoutExchange broadcastExchange() { return new FanoutExchange("commerce.broadcast"); }
    @Bean public Binding broadcastBinding() {
        return BindingBuilder.bind(broadcastQueue()).to(broadcastExchange());
    }
    @Bean public Queue defaultQueue() { return new Queue("demo.default"); }

    @RabbitListener(queues = {"demo.orders", "demo.direct", "demo.broadcast", "demo.default"})
    public void consume(OrderCreated event) {}
}

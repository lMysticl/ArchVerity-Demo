package sample.payment;

import org.springframework.cloud.openfeign.FeignClient;
import org.springframework.web.bind.annotation.*;

/** Concrete payment → orders edge for the opt-in dependency cycle exercise. */
@FeignClient(name = "orders", url = "http://orders")
public interface OrderStatusClient {
    @GetMapping("/orders/{id}")
    OrderStatus status(@PathVariable String id);
}
record OrderStatus(String id, String status) {}

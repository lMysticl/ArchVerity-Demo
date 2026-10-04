package sample.order;

import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/orders")
public class OrderStatusController {
    @GetMapping("/{id}")
    public OrderStatus status(@PathVariable String id) { return new OrderStatus(id, "CREATED"); }
}
record OrderStatus(String id, String status) {}

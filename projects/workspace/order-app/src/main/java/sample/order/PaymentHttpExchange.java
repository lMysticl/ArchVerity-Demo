package sample.order;

import java.util.List;
import java.util.Map;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.service.annotation.*;

@HttpExchange(url = "http://payments/demo", accept = "application/json")
public interface PaymentHttpExchange {
    @GetExchange("/{id}")
    PaymentView find(@PathVariable String id);

    @PostExchange(value = "/conditions", contentType = "application/json", accept = "application/json")
    PaymentView conditioned(@RequestParam String mode, @RequestHeader("X-Demo") String header,
                            @RequestBody NestedPaymentRequest request);
}
record Address(String city, String postalCode) {}
enum PaymentState { PENDING, PAID, DECLINED }
record PaymentView(String id, PaymentState state, Address address,
                   List<Address> deliveries, Map<String, Address> labels) {}
record NestedPaymentRequest(String orderId, Address address, List<Address> deliveries) {}

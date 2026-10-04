package sample.payment;

import jakarta.validation.constraints.NotNull;
import java.util.List;
import java.util.Map;
import org.springframework.web.bind.annotation.*;

/** Source contracts: this fixture is intentionally not a running web server. */
@RestController
@RequestMapping("/demo")
public class DemoContractsController {
    @GetMapping(value = "/{id}", produces = "application/json")
    public PaymentView find(@PathVariable String id) {
        return new PaymentView(id, PaymentState.PAID, new Address("Kyiv", "01001"), List.of(), Map.of());
    }

    @PostMapping(value = "/conditions", consumes = "application/json", produces = "application/json",
                 params = "mode=demo", headers = "X-Demo=local")
    public PaymentView conditioned(@RequestParam String mode, @RequestHeader("X-Demo") String header,
                                   @RequestBody NestedPaymentRequest request) {
        return find(request.orderId());
    }

    @DemoGet("/composed")
    public PaymentView composed() { return find("42"); }
}

record Address(@NotNull String city, String postalCode) {}
enum PaymentState { PENDING, PAID, DECLINED }
record PaymentView(@NotNull String id, PaymentState state, Address address,
                   List<Address> deliveries, Map<String, Address> labels) {}
record NestedPaymentRequest(@NotNull String orderId, Address address, List<Address> deliveries) {}

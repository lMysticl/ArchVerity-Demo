package demo.orders;

import org.springframework.cloud.openfeign.FeignClient;
import org.springframework.web.bind.annotation.*;

@FeignClient(name = "payments", url = "http://payments.example.test", path = "/payments")
public interface PaymentClient {
    // Intentional mismatch: the provider accepts PUT, while this caller sends POST.
    // Fix only this annotation to @PutMapping, then run Analyze again.
    @PostMapping("/{paymentId}")
    String update(@PathVariable("paymentId") String paymentId);
}

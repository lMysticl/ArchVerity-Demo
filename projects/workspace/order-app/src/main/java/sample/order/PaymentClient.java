package sample.order;
import org.springframework.cloud.openfeign.FeignClient;
import org.springframework.web.bind.annotation.*;
@FeignClient(name="payments", path="/payments")
public interface PaymentClient {
 @PostMapping("/{paymentId}") PaymentResponse update(@PathVariable String paymentId, @RequestBody PaymentRequest request);
}
record PaymentRequest(String orderId, long amount, String currency) {}
record PaymentResponse(String paymentId, String status, String providerReference) {}

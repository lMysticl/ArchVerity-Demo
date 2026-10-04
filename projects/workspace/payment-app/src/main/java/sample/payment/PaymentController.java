package sample.payment;
import org.springframework.web.bind.annotation.*;
@RestController
@RequestMapping("/payments")
class PaymentController {
 @PostMapping("/{paymentId}") PaymentResponse update(@PathVariable String paymentId,@RequestBody PaymentRequest request){return null;}
}
record PaymentRequest(String orderId, long amount, String currency) {}
record PaymentResponse(String paymentId, String status, @jakarta.validation.constraints.NotNull String providerReference) {}

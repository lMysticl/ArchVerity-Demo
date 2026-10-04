package demo.payments;

import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/payments")
public class PaymentController {
    @PutMapping("/{paymentId}")
    public String update(@PathVariable("paymentId") String paymentId) {
        return "updated:" + paymentId;
    }
}

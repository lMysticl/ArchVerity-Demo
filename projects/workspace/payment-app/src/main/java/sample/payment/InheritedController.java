package sample.payment;

import org.springframework.web.bind.annotation.*;

@RequestMapping("/inherited")
interface InheritedPaymentApi {
    @GetMapping("/{id}")
    PaymentView findInherited(@PathVariable String id);
}

@RestController
public class InheritedController implements InheritedPaymentApi {
    @Override
    public PaymentView findInherited(String id) { return new DemoContractsController().find(id); }
}
